import re

_RUN_RE = re.compile(r"^(\d{1,9})-([0-9kK])$")


def formatear_run(raw: str | None) -> str | None:
    """Devuelve el RUN en formato XX.XXX.XXX-X, sin ceros iniciales.

    BRD FR-04, RN-03. Acepta entradas con o sin puntos, con o sin guion.
    """
    if not raw:
        return None
    s = raw.strip().replace(".", "").replace(" ", "")
    if "-" not in s and len(s) >= 2:
        s = f"{s[:-1]}-{s[-1]}"
    # Split on dash to normalise leading zeros before regex match
    parts = s.split("-", 1)
    if len(parts) != 2:
        return None
    cuerpo_raw, dv_raw = parts
    cuerpo_raw = cuerpo_raw.lstrip("0") or "0"
    s = f"{cuerpo_raw}-{dv_raw}"
    m = _RUN_RE.match(s)
    if not m:
        return None
    cuerpo, dv = m.group(1), m.group(2).upper()
    rev = cuerpo[::-1]
    grupos = [rev[i:i+3][::-1] for i in range(0, len(rev), 3)][::-1]
    return f"{'.'.join(grupos)}-{dv}"
