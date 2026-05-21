from derivacion_drm.domain.extractors.art_37_bis import detectar_art_37_bis


def test_detecta_mencion_directa():
    assert detectar_art_37_bis("conforme al artículo 37 bis se solicita...") is True


def test_detecta_variantes():
    assert detectar_art_37_bis("Art. 37 Bis Ley N° 20.084") is True
    assert detectar_art_37_bis("artículo 37bis") is True


def test_no_detecta_si_ausente():
    assert detectar_art_37_bis("texto sin mención del artículo") is False
    assert detectar_art_37_bis("artículo 37") is False
