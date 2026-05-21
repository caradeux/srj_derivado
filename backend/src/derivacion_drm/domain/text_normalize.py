import unicodedata


def strip_acentos(s: str) -> str:
    """Quita tildes y diéresis; preserva ñ→n."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalizar_comuna(s: str) -> str:
    """Normaliza una comuna para comparación: sin tildes, lowercase, sin espacios extra.

    BRD FR-07: 'Peñalolén' ≡ 'Peñalolen' ≡ 'penalolen'.
    """
    return strip_acentos(s).strip().lower()
