from datetime import date, time
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


class Medida(StrEnum):
    MCA = "MCA"
    SBC = "SBC"
    LAS = "LAS"
    LAE = "LAE"
    LAEIP = "LAEIP"
    IP = "IP"
    IRC = "IRC"
    PSA = "PSA"
    SALIDAS_ALTERNATIVAS = "SALIDAS_ALTERNATIVAS"


class Genero(StrEnum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


class CentroIPIRC(StrEnum):
    SAN_JOAQUIN = "San_Joaquin"
    SAN_BERNARDO = "San_Bernardo"
    TIL_TIL = "Til_Til"
    SANTIAGO = "Santiago"


class Adolescente(BaseModel):
    nombre: str
    run: str
    genero: Genero | None = None
    domicilio: str | None = None
    comuna: str | None = None


class Causa(BaseModel):
    tribunal: str | None = None
    tipo_resolucion: str | None = None
    ruc: str | None = None
    rit: str | None = None
    delito: str | None = None
    fecha_resolucion: date | None = None
    art_37_bis: bool = False


class AdultoResponsable(BaseModel):
    nombre: str | None = None
    telefono: str | None = None


class AudienciaPII(BaseModel):
    fecha: date
    hora: time = time(11, 0)
    sala: str = "802"
    piso: str = "8°"
    edificio: str = "E"


class CentroAsignado(BaseModel):
    nombre: str
    director: str
    mail: str
    telefono: str
    direccion: str | None = None
    tipo: Literal["Priorizada", "No priorizada"] | None = None


class CasoDerivacion(BaseModel):
    adolescente: Adolescente
    causa: Causa
    medida: Medida
    adulto: AdultoResponsable | None = None
    duracion: str | None = None
    abonos: str | None = None
    audiencia_pii: AudienciaPII | None = None
    observaciones: str | None = None
    centro: CentroAsignado
