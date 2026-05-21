from derivacion_drm.domain.models import Genero
from derivacion_drm.domain.text_normalize import strip_acentos

# ~60 nombres femeninos comunes en Chile (BRD FR-06, §13.4)
NOMBRES_FEMENINOS: frozenset[str] = frozenset(strip_acentos(n).lower() for n in {
    "maria", "ana", "catalina", "javiera", "francisca", "constanza", "valentina",
    "camila", "fernanda", "antonia", "florencia", "isidora", "amanda", "agustina",
    "martina", "emilia", "sofia", "trinidad", "rosario", "paz", "monserrat",
    "ignacia", "magdalena", "anais", "anais", "belen", "renata", "alondra",
    "krishna", "scarlett", "scarlet", "millaray", "rayen", "kiara", "kiara",
    "carla", "carolina", "patricia", "paola", "andrea", "claudia", "veronica",
    "marcela", "lorena", "natalia", "yasna", "ximena", "soledad", "macarena",
    "barbara", "daniela", "alejandra", "pamela", "tamara", "gabriela", "valeria",
    "denisse", "yemina", "virna", "paula", "yohana", "ivonne", "evelyn",
    "jessica", "jocelyn", "katherine", "michelle", "nicole", "stephanie",
})


def inferir_genero(primer_nombre: str) -> Genero | None:
    """Infiere el género desde el primer nombre.

    BRD FR-06, RN-09. Si el nombre no aparece en el catálogo femenino,
    asume masculino (caso mayoritario); devuelve None solo si la entrada
    está vacía o es claramente no-nombre.
    """
    if not primer_nombre or not primer_nombre.strip():
        return None
    primer_token = primer_nombre.strip().split()[0]
    clave = strip_acentos(primer_token).lower()
    if not clave.isalpha():
        return None
    if clave in NOMBRES_FEMENINOS:
        return Genero.FEMENINO
    return Genero.MASCULINO
