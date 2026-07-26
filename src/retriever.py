"""Buscador semántico ligero sobre el corpus de documentos.

Combina dos vistas TF-IDF de los mismos fragmentos:

* palabras y bigramas, que capta la coincidencia de términos y frases;
* n-gramas de caracteres, que tolera errores de tipeo, plurales y variantes de
  acentuación ("señas" vs "senas", "cancelacion" vs "cancelación").

Se eligió TF-IDF en lugar de embeddings neuronales a propósito: el corpus son
cinco documentos, el vocabulario es cerrado, y el resultado corre en la VM
Always Free de OCI sin GPU, sin descargar modelos y con arranque instantáneo.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .ingest import Fragmento, cargar_corpus

STOPWORDS_ES = [
    "a", "al", "algo", "algunos", "ante", "antes", "como", "con", "contra",
    "cual", "cuando", "de", "del", "desde", "donde", "dos", "el", "ella",
    "ellos", "en", "entre", "era", "es", "esa", "ese", "eso", "esta", "este",
    "esto", "ha", "hasta", "hay", "la", "las", "le", "les", "lo", "los", "mas",
    "me", "mi", "mucho", "muy", "no", "nos", "o", "otra", "otro", "para",
    "pero", "poco", "por", "porque", "que", "quien", "se", "sea", "ser", "si",
    "sin", "sobre", "solo", "son", "su", "sus", "tambien", "tanto", "te",
    "tiene", "todo", "un", "una", "uno", "unos", "y", "ya",
]


def normalizar(texto: str) -> str:
    """Minúsculas y sin acentos, para que la comparación no dependa de tildes."""
    texto = texto.lower()
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


@dataclass(frozen=True)
class Resultado:
    fragmento: Fragmento
    score: float

    def to_dict(self) -> dict:
        return self.fragmento.to_dict() | {"score": round(self.score, 4)}


class Buscador:
    """Índice TF-IDF híbrido sobre los fragmentos del corpus."""

    # Peso de cada vista al fusionar los puntajes.
    PESO_PALABRAS = 0.65
    PESO_CARACTERES = 0.35

    # Una consulta ajena al dominio ("receta de milanesas") igual saca ~0.04 de
    # similitud por caracteres, porque comparte trigramas con cualquier texto en
    # español. Lo que la delata es que su similitud POR PALABRAS es exactamente
    # cero. Exigir un mínimo léxico descarta ese ruido sin castigar a las
    # consultas mal tipeadas, que sí conservan alguna palabra reconocible.
    PISO_PALABRAS = 0.01

    def __init__(self, corpus: list[Fragmento] | None = None) -> None:
        self.corpus = corpus if corpus is not None else cargar_corpus()
        if not self.corpus:
            raise ValueError("El corpus está vacío: no hay nada que indexar.")

        textos = [normalizar(f.texto) for f in self.corpus]

        self._vec_palabras = TfidfVectorizer(
            ngram_range=(1, 2), stop_words=STOPWORDS_ES, sublinear_tf=True, min_df=1
        )
        self._mat_palabras = self._vec_palabras.fit_transform(textos)

        self._vec_caracteres = TfidfVectorizer(
            analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=2
        )
        self._mat_caracteres = self._vec_caracteres.fit_transform(textos)

    def __len__(self) -> int:
        return len(self.corpus)

    def buscar(self, consulta: str, top_k: int = 5, umbral: float = 0.05) -> list[Resultado]:
        """Devuelve los `top_k` fragmentos más parecidos a la consulta."""
        consulta = (consulta or "").strip()
        if not consulta:
            return []

        normalizada = normalizar(consulta)
        sim_palabras = cosine_similarity(
            self._vec_palabras.transform([normalizada]), self._mat_palabras
        ).ravel()
        sim_caracteres = cosine_similarity(
            self._vec_caracteres.transform([normalizada]), self._mat_caracteres
        ).ravel()

        if sim_palabras.max(initial=0.0) < self.PISO_PALABRAS:
            return []

        puntajes = self.PESO_PALABRAS * sim_palabras + self.PESO_CARACTERES * sim_caracteres

        mejores = np.argsort(puntajes)[::-1][:top_k]
        return [
            Resultado(self.corpus[i], float(puntajes[i]))
            for i in mejores
            if puntajes[i] >= umbral
        ]

    def contexto(self, consulta: str, top_k: int = 5) -> str:
        """Arma el bloque de contexto que se le pasa al modelo."""
        resultados = self.buscar(consulta, top_k=top_k)
        if not resultados:
            return "SIN RESULTADOS: no se encontró información sobre esa consulta."
        return "\n\n".join(
            f"[Fuente {i}] {r.fragmento.cita}\n{r.fragmento.texto}"
            for i, r in enumerate(resultados, start=1)
        )
