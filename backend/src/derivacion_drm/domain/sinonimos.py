from derivacion_drm.domain.models import Medida

# BRD §13.3. Orden de listas: el primero (sigla) suele ser el match más específico,
# pero el orden de iteración por medida importa: LAEIP antes que LAE para evitar
# que el regex de LAE consuma "LAE" dentro de "LAEIP".
SINONIMOS_MEDIDA: dict[Medida, list[str]] = {
    Medida.LAEIP: ["laeip", "lae-ip", "libertad asistida especial con internación parcial",
                   "libertad asistida especial con internacion parcial"],
    Medida.LAE:   ["lae", "libertad asistida especial"],
    Medida.LAS:   ["las", "libertad asistida simple", "l.a.s"],
    Medida.MCA:   ["mca", "medida cautelar ambulatoria", "sujeción a la vigilancia",
                   "sujecion a la vigilancia", "155 letra b"],
    Medida.SBC:   ["sbc", "servicios en beneficio", "prestación de servicios",
                   "prestacion de servicios"],
    Medida.IP:    ["internación provisoria", "internacion provisoria", " ip "],
    Medida.IRC:   ["irc", "crc", "régimen cerrado", "regimen cerrado", "centro cerrado"],
    Medida.SALIDAS_ALTERNATIVAS: ["salidas alternativas", "suspensión condicional",
                                  "suspension condicional", "art. 237", "artículo 237"],
    Medida.PSA:   ["psa", "programa de salidas alternativas"],
}


# Orden de evaluación: más específico primero
ORDEN_MEDIDAS: list[Medida] = [
    Medida.LAEIP, Medida.LAE, Medida.LAS,
    Medida.MCA, Medida.SBC,
    Medida.IRC, Medida.IP,
    Medida.SALIDAS_ALTERNATIVAS, Medida.PSA,
]
