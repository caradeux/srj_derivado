from pydantic import BaseModel

from derivacion_drm.domain.models import CentroAsignado, CentroIPIRC, Medida
from derivacion_drm.domain.text_normalize import normalizar_comuna


class EntradaOferta(BaseModel):
    """Una fila de CONSOLIDADO_OFERTA_DRM_V2.xlsx hoja 'Desacumulado'."""
    programa: str
    medida: Medida
    comunas_priorizadas: list[str] = []
    comunas_no_priorizadas: list[str] = []
    direccion: str
    director: str
    mail: str
    telefono: str


class CatalogoOferta(BaseModel):
    entradas: list[EntradaOferta]


def resolver_centro_estandar(
    medida: Medida, comuna: str, catalogo: CatalogoOferta,
) -> list[CentroAsignado]:
    """BRD FR-13, RN-04. Devuelve 0, 1 o N centros."""
    c_norm = normalizar_comuna(comuna)
    out: list[CentroAsignado] = []
    for e in catalogo.entradas:
        if e.medida != medida:
            continue
        if any(normalizar_comuna(x) == c_norm for x in e.comunas_priorizadas):
            tipo = "Priorizada"
        elif any(normalizar_comuna(x) == c_norm for x in e.comunas_no_priorizadas):
            tipo = "No priorizada"
        else:
            continue
        out.append(CentroAsignado(
            nombre=e.programa, director=e.director, mail=e.mail,
            telefono=e.telefono, direccion=e.direccion, tipo=tipo,
        ))
    return out


# BRD §13.2 — hardcoded por decisión de mantención (RN-05)
CENTROS_IP_IRC: dict[CentroIPIRC, CentroAsignado] = {
    CentroIPIRC.SAN_JOAQUIN: CentroAsignado(
        nombre="Centro IP - IRC San Joaquín",
        director="Virna Salazar",
        mail="ingresos.ipircsnjqn@reinsercionjuvenil.cl",
        telefono="+56 9 7835 9080",
        direccion="Comuna de San Joaquín, Región Metropolitana",
    ),
    CentroIPIRC.SAN_BERNARDO: CentroAsignado(
        nombre="Centro IP - IRC San Bernardo",
        director="Miguel González Rubio",
        mail="estadisticas.sanbdo@reinsercionjuvenil.cl",
        telefono="22 592 3302",
        direccion="Comuna de San Bernardo, Región Metropolitana",
    ),
    CentroIPIRC.TIL_TIL: CentroAsignado(
        nombre="C.M.N. Til Til",
        director="Eduardo Quevedo",
        mail="estadisticas.tiltil@reinsercionjuvenil.cl",
        telefono="+56 9 5202 9630",
        direccion="Comuna de Til Til, Región Metropolitana",
    ),
    CentroIPIRC.SANTIAGO: CentroAsignado(
        nombre="Centro IP - IRC Santiago",
        director="Paula Alcayaga T.",
        mail="yemina.vargas@reinsercionjuvenil.cl",
        telefono="",
        direccion="Comuna de Santiago, Región Metropolitana",
    ),
}


def centro_ip_irc(opcion: CentroIPIRC) -> CentroAsignado:
    return CENTROS_IP_IRC[opcion]
