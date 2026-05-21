from derivacion_drm.domain.extractors.nombre import normalizar_nombre
from derivacion_drm.domain.models import AdultoResponsable, Tabla
from derivacion_drm.domain.text_normalize import strip_acentos


def _es_tabla_de_adulto(tabla: Tabla) -> bool:
    enc_norm = {strip_acentos(e).upper().strip() for e in tabla.encabezados}
    return any("ADULTO RESPONSABLE" in e for e in enc_norm)


def _indices(tabla: Tabla) -> dict[str, int]:
    out: dict[str, int] = {}
    for i, enc in enumerate(tabla.encabezados):
        e = strip_acentos(enc).upper().strip()
        if "ADULTO" in e or "NOMBRE" in e:
            out.setdefault("nombre", i)
        if "TELEFONO" in e or "TELÉFONO" in e or "FONO" in e:
            out.setdefault("telefono", i)
    return out


def extraer_adulto(tablas: list[Tabla]) -> AdultoResponsable:
    """Lee la tabla con encabezado 'ADULTO RESPONSABLE' (BRD FR-11)."""
    for t in tablas:
        if not _es_tabla_de_adulto(t):
            continue
        idx = _indices(t)
        if not t.filas:
            continue
        fila = t.filas[0]
        nombre = None
        if "nombre" in idx and idx["nombre"] < len(fila):
            raw = fila[idx["nombre"]]
            nombre = normalizar_nombre(raw) if raw and raw.strip() else None
        telefono = None
        if "telefono" in idx and idx["telefono"] < len(fila):
            t_raw = fila[idx["telefono"]].strip()
            telefono = t_raw or None
        return AdultoResponsable(nombre=nombre, telefono=telefono)
    return AdultoResponsable()
