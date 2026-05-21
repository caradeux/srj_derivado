import re

# BRD FR-10: detecta "37 bis" en cualquier variante
_ART_37_BIS = re.compile(r"\b37\s*bis\b", re.IGNORECASE)


def detectar_art_37_bis(texto: str) -> bool:
    return bool(_ART_37_BIS.search(texto))
