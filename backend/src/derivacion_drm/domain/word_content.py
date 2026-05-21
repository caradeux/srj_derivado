from datetime import date

from derivacion_drm.domain.filename import componer_nombre_archivo
from derivacion_drm.domain.models import CasoDerivacion, Genero
from derivacion_drm.domain.word_spec import (
    ParagraphSpec, RunSpec, WordDocumentSpec,
)

_MESES_ES = [
    "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def _fecha_larga(d: date) -> str:
    return f"{d.day} de {_MESES_ES[d.month]} de {d.year}"


def _concordancia(g: Genero | None) -> dict[str, str]:
    """BRD RN-06."""
    if g == Genero.FEMENINO:
        return {
            "tratamiento": "doña", "domiciliado": "domiciliada",
            "derivado": "derivada", "individualizado": "individualizada",
            "adulto_responsable": "adulta responsable",
            "el_la_adolescente": "la adolescente",
        }
    return {
        "tratamiento": "don", "domiciliado": "domiciliado",
        "derivado": "derivado", "individualizado": "individualizado",
        "adulto_responsable": "adulto responsable",
        "el_la_adolescente": "el adolescente",
    }


def _parentesis_adulto(caso: CasoDerivacion, c: dict[str, str]) -> str:
    """RN-07: nunca emite paréntesis vacíos."""
    a = caso.adulto
    if not a or (not a.nombre and not a.telefono):
        return ""
    partes = []
    if a.nombre:
        partes.append(f"{c['adulto_responsable']}: {a.nombre}")
    if a.telefono:
        partes.append(f"teléfono {a.telefono}")
    return " (" + ", ".join(partes) + ")"


def _p(*runs: RunSpec,
       alignment: str = "justify",
       indent: float | None = 1.25) -> ParagraphSpec:
    return ParagraphSpec(
        runs=list(runs), alignment=alignment, indent_first_line_cm=indent,
    )


def _r(text: str, **kw) -> RunSpec:
    return RunSpec(text=text, **kw)


def componer_documento_estandar(
    caso: CasoDerivacion, profesional: str, fecha_emision: date,
) -> WordDocumentSpec:
    """BRD FR-17, §14.1. Formato de párrafos para MCA, SBC, LAS, LAE, LAEIP,
    Salidas Alternativas."""
    c = _concordancia(caso.adolescente.genero)
    paragraphs: list[ParagraphSpec] = []

    # Fecha alineada a la derecha
    paragraphs.append(_p(
        _r(f"Santiago, {_fecha_larga(fecha_emision)}"),
        alignment="right", indent=None,
    ))

    # Título centrado, negrita, subrayado
    paragraphs.append(_p(
        _r("CERTIFICA DERIVACIÓN VIRTUAL", bold=True, underline=True),
        alignment="center", indent=None,
    ))
    paragraphs.append(_p(
        _r("SERVICIO NACIONAL DE REINSERCIÓN SOCIAL JUVENIL (S.N.R.S.J.)",
           bold=True, underline=True),
        alignment="center", indent=None,
    ))

    # Párrafo 1 — presentación del imputado
    parents = _parentesis_adulto(caso, c)
    domicilio_txt = (
        f", domiciliad{'a' if c['domiciliado'] == 'domiciliada' else 'o'} en "
        f"{caso.adolescente.domicilio}, comuna de {caso.adolescente.comuna}"
        if caso.adolescente.domicilio else ""
    )
    paragraphs.append(_p(
        _r(f"Por medio del presente certifico que con esta fecha envío los antecedentes de "
           f"{c['tratamiento']} "),
        _r(caso.adolescente.nombre, bold=True, uppercase=True),
        _r(f", run {caso.adolescente.run}{domicilio_txt}{parents}, siendo "
           f"{c['derivado']} en forma no presencial a la Red del S.N.R.S.J. en los "
           f"siguientes términos:"),
    ))

    # Párrafo 2 — solicitud al director
    paragraphs.append(_p(
        _r(f"Señor(a) director(a) Centro "),
        _r(caso.centro.nombre, bold=True),
        _r(f", solicito a usted ingresar a{' la' if c['el_la_adolescente'] == 'la adolescente' else 'l'} "
           f"{c['individualizado']} a vuestro programa para el fin de implementar la medida "
           f"ordenada en {caso.causa.tipo_resolucion or 'resolución'} de fecha "
           f"{_fecha_larga(caso.causa.fecha_resolucion) if caso.causa.fecha_resolucion else 'S/F'} "
           f"por la {caso.causa.tribunal or 'S/T'}, en causa RUC {caso.causa.ruc or 'S/RUC'}, "
           f"RIT {caso.causa.rit or 'S/RIT'}, por el delito de "
           f"{caso.causa.delito or 'S/delito'}."),
    ))

    # Cita 37 bis — FR-10
    if caso.causa.art_37_bis:
        paragraphs.append(_p(
            _r("Cabe señalar que el tribunal solicita expresamente: \""),
            _r("Evacúese informe Técnico conforme al artículo 37 bis", bold=True),
            _r("\", el cual será elaborado por el equipo regional."),
        ))

    # Datos del centro + email hipervinculado
    paragraphs.append(_p(
        _r(f"Se solicita gestionar el ingreso e informar los resultados. Habilitar la casilla "),
        _r(caso.centro.mail, bold=True, underline=True, hyperlink=f"mailto:{caso.centro.mail}"),
        _r(f" para recibir las actas y resoluciones de la causa. El centro tiene su ubicación en "
           f"{caso.centro.direccion or 'S/dirección'}, fono {caso.centro.telefono}."),
    ))

    # Firma centrada (líneas en blanco + nombre + cargo)
    paragraphs.append(_p(_r(""), alignment="center", indent=None))
    paragraphs.append(_p(_r(""), alignment="center", indent=None))
    paragraphs.append(_p(_r(profesional, bold=True), alignment="center", indent=None))
    paragraphs.append(_p(_r("Profesional de Línea"), alignment="center", indent=None))
    paragraphs.append(_p(
        _r("Coordinación Judicial D.R.M. - S.N.R.S.J."),
        alignment="center", indent=None,
    ))

    return WordDocumentSpec(
        paragraphs=paragraphs,
        incluir_logo=True,
        filename=componer_nombre_archivo(caso),
    )
