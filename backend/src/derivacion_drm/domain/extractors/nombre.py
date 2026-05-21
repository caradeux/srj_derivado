import re

from derivacion_drm.domain.models import Adolescente, Tabla
from derivacion_drm.domain.run_format import formatear_run
from derivacion_drm.domain.text_normalize import strip_acentos

CONECTORES = {"de", "del", "la", "las", "los", "y", "da", "el"}

# BRD RN-01: tablas con estos encabezados NO contienen al imputado
_ENCABEZADOS_NO_IMPUTADO = {"VICTIMA", "ADULTO RESPONSABLE"}


def normalizar_nombre(raw: str) -> str:
    """Title Case con conectores en minúscula; quita paréntesis y comas trailing.

    BRD FR-05: 'Juan Pérez (ip San Bernardo)' → 'Juan Pérez'.
    """
    s = re.sub(r"\s*\([^)]*\)\s*$", "", raw)        # quita paréntesis trailing
    s = re.sub(r",\s*$", "", s).strip()              # quita coma trailing
    s = re.sub(r"\s+", " ", s)                       # colapsa whitespace
    tokens = []
    for i, tok in enumerate(s.split()):
        low = tok.lower()
        if i > 0 and low in CONECTORES:
            tokens.append(low)
        else:
            tokens.append(tok.capitalize())
    return " ".join(tokens)


def _es_tabla_de_imputados(tabla: Tabla) -> bool:
    enc_norm = {strip_acentos(e).upper().strip() for e in tabla.encabezados}
    if any(e in enc_norm for e in _ENCABEZADOS_NO_IMPUTADO):
        return False
    # Acepta encabezados típicos del Acta de Audiencia
    return any("IMPUTADO" in e or "NOMBRE" in e for e in enc_norm)


def _indices(tabla: Tabla) -> dict[str, int]:
    out = {}
    for i, enc in enumerate(tabla.encabezados):
        e = strip_acentos(enc).upper().strip()
        if "NOMBRE" in e or "IMPUTADO" in e:
            out.setdefault("nombre", i)
        if "RUT" in e or "R.U.N" in e or "RUN" in e:
            out.setdefault("run", i)
        if "DIRECC" in e or "DOMICILIO" in e:
            out.setdefault("domicilio", i)
        if "COMUNA" in e:
            out.setdefault("comuna", i)
    return out


def extraer_imputados_de_tabla(tablas: list[Tabla]) -> list[Adolescente]:
    """Devuelve la lista de adolescentes detectados en las tablas de imputados.

    BRD FR-08 (coimputados), RN-01 (filtra víctima y adulto responsable).
    """
    encontrados: list[Adolescente] = []
    for t in tablas:
        if not _es_tabla_de_imputados(t):
            continue
        idx = _indices(t)
        if "nombre" not in idx:
            continue
        for fila in t.filas:
            if idx["nombre"] >= len(fila):
                continue
            nombre_raw = fila[idx["nombre"]]
            if not nombre_raw or not nombre_raw.strip():
                continue
            nombre = normalizar_nombre(nombre_raw)
            run = formatear_run(fila[idx["run"]]) if "run" in idx and idx["run"] < len(fila) else None
            domicilio = fila[idx["domicilio"]].strip() if "domicilio" in idx and idx["domicilio"] < len(fila) else None
            comuna = fila[idx["comuna"]].strip() if "comuna" in idx and idx["comuna"] < len(fila) else None
            encontrados.append(Adolescente(
                nombre=nombre, run=run or "", domicilio=domicilio, comuna=comuna,
            ))
    return encontrados
