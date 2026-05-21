from typing import Literal

from pydantic import BaseModel


class RunSpec(BaseModel):
    text: str
    bold: bool = False
    underline: bool = False
    uppercase: bool = False
    hyperlink: str | None = None


class ParagraphSpec(BaseModel):
    runs: list[RunSpec]
    alignment: Literal["left", "center", "right", "justify"] = "left"
    indent_first_line_cm: float | None = None
    line_spacing: float = 1.15


class TableSpec(BaseModel):
    rows: list[tuple[str, str]]
    style: str = "Table Grid"


class WordDocumentSpec(BaseModel):
    paragraphs: list[ParagraphSpec | TableSpec]
    incluir_logo: bool = True
    footer_text: str = "Av. Pedro De Valdivia N° 4070, Ñuñoa.  Fono: 22.3980.04.00"
    filename: str
