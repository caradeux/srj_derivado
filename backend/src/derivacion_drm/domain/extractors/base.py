from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ExtractedField(BaseModel, Generic[T]):
    """Resultado de un extractor: valor + confianza + procedencia.

    `source` permite que la UI señale al profesional cuando un campo viene
    del fallback regex en lugar de la lectura por tablas (BRD NFR-06).
    """
    value: T | None
    confidence: Literal["high", "low"]
    source: str
