# Business Requirements Document (BRD)
## Sistema de Derivación Virtual — D.R.M.
### Servicio Nacional de Reinserción Social Juvenil (S.N.R.S.J.)

---

**Versión del documento:** 1.0  
**Fecha de emisión:** 20 de mayo de 2026  
**Versión actual de la aplicación:** v15  
**Autor del proyecto:** Juan Manuel Olivares Oyarzún  
**Cargo:** Profesional de Línea, Coordinación Judicial D.R.M.  
**Institución:** Servicio Nacional de Reinserción Social Juvenil (S.N.R.S.J.)  
**Ubicación:** Av. Pedro De Valdivia N° 4070, Ñuñoa, Santiago — Fono: 22.3980.04.00

---

## Tabla de Contenidos

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Contexto y Justificación](#2-contexto-y-justificación)
3. [Objetivos del Proyecto](#3-objetivos-del-proyecto)
4. [Alcance](#4-alcance)
5. [Stakeholders](#5-stakeholders)
6. [Requerimientos de Negocio](#6-requerimientos-de-negocio)
7. [Requerimientos Funcionales](#7-requerimientos-funcionales)
8. [Requerimientos No Funcionales](#8-requerimientos-no-funcionales)
9. [Reglas de Negocio](#9-reglas-de-negocio)
10. [Arquitectura Técnica](#10-arquitectura-técnica)
11. [Flujos de Trabajo](#11-flujos-de-trabajo)
12. [Tipos de Medidas y Sanciones](#12-tipos-de-medidas-y-sanciones)
13. [Catálogos y Bases de Datos](#13-catálogos-y-bases-de-datos)
14. [Salidas del Sistema](#14-salidas-del-sistema)
15. [Casos de Uso](#15-casos-de-uso)
16. [Restricciones y Supuestos](#16-restricciones-y-supuestos)
17. [Roadmap y Estado de Implementación](#17-roadmap-y-estado-de-implementación)
18. [Riesgos](#18-riesgos)
19. [Glosario](#19-glosario)
20. [Anexos](#20-anexos)

---

## 1. Resumen Ejecutivo

El **Sistema de Derivación Virtual** es una aplicación web local desarrollada en Python con framework Streamlit, diseñada para automatizar la generación de certificados de derivación judicial de adolescentes infractores de ley penal a la red del Servicio Nacional de Reinserción Social Juvenil (S.N.R.S.J.), en el marco de la **Ley N° 20.084** sobre Responsabilidad Penal Adolescente (RPA).

La herramienta extrae automáticamente datos clave (nombre, RUN, domicilio, comuna, delito, tribunal, RUC/RIT, medida ordenada) desde documentos judiciales en formato PDF o Word — actas de audiencia, oficios, sentencias y certificados de ejecutoria — y produce un certificado de derivación oficial en Word con el formato institucional del S.N.R.S.J., asignando automáticamente el centro de cumplimiento correspondiente según la comuna de residencia del adolescente y el tipo de medida impuesta.

El sistema reduce el tiempo de elaboración de un certificado de derivación de aproximadamente 15-25 minutos (proceso manual) a menos de 2 minutos, eliminando errores de transcripción y estandarizando el formato de todos los documentos remitidos a la red de centros.

---

## 2. Contexto y Justificación

### 2.1 Contexto institucional

El **Servicio Nacional de Reinserción Social Juvenil (S.N.R.S.J.)**, creado por la Ley N° 21.527, asume las funciones que anteriormente correspondían al Servicio Nacional de Menores (SENAME) en materia de adolescentes infractores de ley penal. Su misión es la reinserción social efectiva de jóvenes condenados o imputados bajo la Ley N° 20.084.

La **Coordinación Judicial D.R.M. (Dirección Regional Metropolitana)** es la unidad responsable de derivar a los adolescentes desde los tribunales hacia los programas de la red — administración directa o colaboradores acreditados — según la medida cautelar o sanción dictada.

### 2.2 Problemática

Antes de la implementación de este sistema, el proceso de derivación se realizaba enteramente de forma manual:

- Lectura completa de cada documento judicial recibido (acta, oficio, sentencia)
- Transcripción manual de datos del imputado (frecuentemente con errores tipográficos)
- Consulta manual a la planilla de oferta programática para determinar el centro asignado
- Redacción del certificado de derivación reproduciendo un formato estándar
- Riesgo alto de errores en RUC/RIT (números de 10-12 dígitos) y de confusión entre datos del imputado vs. víctima vs. adulto responsable
- Inconsistencias en el formato de los documentos remitidos a los centros

### 2.3 Justificación del proyecto

Esta aplicación responde a la necesidad de:

- **Reducir tiempo administrativo** del profesional de línea para que pueda dedicarse a funciones de mayor valor agregado (coordinación con tribunales y centros, análisis de casos complejos)
- **Estandarizar el formato** de todos los certificados de derivación emitidos por la D.R.M.
- **Minimizar errores** de transcripción de datos sensibles (RUN, RUC, RIT, nombres, direcciones)
- **Centralizar el conocimiento** de la oferta programática en una sola base de datos consultable automáticamente
- **Garantizar trazabilidad** mediante un nombre de archivo estructurado que identifica unívocamente cada derivación

---

## 3. Objetivos del Proyecto

### 3.1 Objetivo general

Implementar una herramienta digital que automatice el proceso de derivación virtual de adolescentes desde la Coordinación Judicial D.R.M. hacia la red de centros del S.N.R.S.J., reduciendo errores y tiempos del proceso administrativo.

### 3.2 Objetivos específicos

1. Extraer automáticamente datos del imputado y de la causa desde documentos judiciales en PDF y Word
2. Asignar automáticamente el centro de cumplimiento correspondiente según comuna del adolescente y tipo de medida
3. Generar un certificado de derivación en formato Word con el formato institucional oficial
4. Soportar todas las medidas y sanciones contempladas en la Ley N° 20.084 (MCA, SBC, LAS, LAE, LAEIP, IP, IRC, salidas alternativas y combinaciones mixtas)
5. Operar localmente, sin requerir conexión a Internet ni infraestructura de servidor
6. Ser usable por personal no técnico mediante una interfaz gráfica web ejecutable desde el computador del profesional

---

## 4. Alcance

### 4.1 Dentro del alcance (In Scope)

- Lectura de documentos judiciales en formato **PDF y .docx**
- Extracción automática de datos del imputado (nombre, RUN, género, domicilio, comuna)
- Extracción automática de datos de la causa (RUC, RIT, tribunal, delito, tipo de resolución, fechas)
- Extracción automática del adulto responsable (nombre, teléfono)
- Detección automática de coimputados con selección manual del adolescente a derivar
- Asignación automática del centro según planilla de oferta programática (CONSOLIDADO OFERTA DRM V2)
- Soporte de selección manual cuando varios centros son aplicables a una misma comuna
- Catálogo separado para centros de Internación Provisoria (IP) e Internación en Régimen Cerrado (IRC)
- Generación de Word con formato institucional oficial (Bookman Old Style, márgenes 2.5 cm, interlineado 1.15)
- Pie de página con dirección y teléfono institucional
- Inclusión automática de logo del S.N.R.S.J. cuando se dispone del archivo PNG
- Soporte para campos opcionales: abonos, observaciones, audiencia PII (Plan de Intervención Individual)
- Nombre de archivo Word estructurado y trazable
- Botonera de medidas como atajo visual
- Limpieza del formulario para iniciar un nuevo caso

### 4.2 Fuera del alcance (Out of Scope)

- Conexión directa con el sistema del Poder Judicial (SITPJ) o con el sistema interno de gestión del S.N.R.S.J.
- Almacenamiento persistente o histórico de derivaciones generadas (no hay base de datos)
- Envío automático del certificado al centro (esto sigue siendo manual por correo electrónico)
- OCR para PDFs escaneados (solo PDFs de texto)
- Multiusuario o multinodal (operación local de un usuario a la vez)
- Firma electrónica del certificado
- Validación legal del contenido por parte del sistema (sigue siendo responsabilidad del profesional)
- Generación de formato definitivo para PSA (Programa de Salidas Alternativas) — pendiente de definición
- Generación de formato para combinaciones mixtas (IRC+LAEIP, IRC+LAE, IRC+LAS, LAEIP+LAE, LAEIP+LAS) — pendiente

---

## 5. Stakeholders

| Rol | Responsabilidad | Interés en el sistema |
|---|---|---|
| **Profesional de Línea D.R.M.** | Usuario principal. Recibe documentos del tribunal, genera derivaciones | Reducir tiempo y errores en su trabajo cotidiano |
| **Coordinación Judicial D.R.M.** | Supervisa la calidad de las derivaciones emitidas | Garantizar estandarización y trazabilidad |
| **Dirección Regional Metropolitana** | Responsable del cumplimiento de plazos y volumen de derivaciones | Métricas de productividad y calidad |
| **Centros de cumplimiento (administración directa y colaboradores)** | Receptores del certificado de derivación | Recibir información completa, legible y oportuna |
| **Tribunales de Garantía / Unidad Especializada RPA** | Emisores de las resoluciones que originan la derivación | Que sus oficios sean correctamente procesados |
| **Adolescentes y sus familias** | Beneficiarios finales del proceso | Que la derivación sea correcta y oportuna |
| **S.N.R.S.J. (institución)** | Custodio del proceso de reinserción | Garantizar cumplimiento normativo de Ley N° 20.084 |

---

## 6. Requerimientos de Negocio

### BR-01: Reducción de tiempo administrativo
El sistema debe permitir generar un certificado de derivación completo en **menos de 2 minutos** desde la recepción del documento judicial, comparado con el tiempo manual de 15-25 minutos.

### BR-02: Cero errores de transcripción
Los campos sensibles del certificado (RUN, RUC, RIT) deben ser extraídos directamente desde el documento fuente sin intervención manual de transcripción.

### BR-03: Cumplimiento del formato institucional
Cada certificado generado debe cumplir exactamente con el formato visual y estructural definido por la Coordinación Judicial D.R.M. (fuente Bookman Old Style, encabezado, pie de página, firma centrada, etc.).

### BR-04: Trazabilidad de derivaciones
El nombre del archivo Word generado debe contener identificadores únicos del caso: nombre del adolescente, sigla de la medida, tribunal, RIT, RUC y — para IP/IRC — sigla del centro de ingreso.

### BR-05: Operación autónoma
El sistema debe poder operar sin conexión a Internet una vez instalado, y sin depender de servicios externos de pago.

### BR-06: Soporte legal completo
El sistema debe soportar todas las medidas cautelares y sanciones contempladas en la Ley N° 20.084 y el Código Procesal Penal aplicables a adolescentes infractores.

### BR-07: Facilidad de uso para usuarios no técnicos
El profesional usuario no requiere conocimientos de programación. La operación se realiza enteramente mediante una interfaz gráfica accesible vía navegador web.

---

## 7. Requerimientos Funcionales

### FR-01: Carga de documentos
- El sistema acepta carga de **uno o más archivos** simultáneamente en formato PDF o .docx
- Permite "arrastrar y soltar" archivos sobre una zona destacada
- Muestra una tarjeta visual por cada archivo cargado con su nombre y tamaño

### FR-02: Extracción de RUC
- Detecta el número RUC (Rol Único de Causa) en formato `XXXXXXXXXX-X` (10-12 dígitos con dígito verificador)
- Prioriza coincidencias precedidas por la palabra "RUC"

### FR-03: Extracción de RIT
- Detecta el número RIT (Rol Interno del Tribunal) en formato `NNNN-AAAA` (número-año)
- Prioriza coincidencias precedidas por la palabra "RIT" para evitar confusión con fechas

### FR-04: Extracción del RUN del imputado
- Detecta números de RUN en formato chileno con o sin puntos y guion
- **Formatea automáticamente** el RUN a `XX.XXX.XXX-X` eliminando ceros iniciales y agregando puntos cada 3 dígitos
- Distingue el RUN del imputado del RUC de la causa
- Descarta RUN de víctimas o adultos responsables

### FR-05: Extracción del nombre del imputado
- Lee el nombre desde las tablas del Acta de Audiencia (columna "NOMBRE IMPUTADO")
- Maneja nombres con saltos de línea entre palabras
- **Limpia paréntesis y comas** que aparezcan después del nombre (ej. "Juan Pérez (ip San Bernardo)" → "Juan Pérez")
- Aplica capitalización tipo Title Case con minúsculas para conectores ("de", "del", "la", "los", etc.)

### FR-06: Inferencia del género
- A partir del primer nombre detectado, infiere género del adolescente (Masculino o Femenino)
- Utiliza un catálogo de aproximadamente 60 nombres femeninos comunes en Chile
- Permite corrección manual mediante un selector

### FR-07: Extracción del domicilio y comuna
- Lee el domicilio desde la celda contigua al RUN en las tablas del acta
- Maneja el caso especial donde RUN, dirección y comuna vienen pegados en una sola celda
- Detecta comunas considerando variantes con/sin tildes ("Peñalolén" / "Peñalolen")
- Descarta direcciones precedidas por las palabras "víctima" o "victima"

### FR-08: Detección de coimputados
- Si los documentos contienen más de un imputado válido (no víctima, no adulto), muestra un **selector tipo radio** con todas las personas detectadas
- Al seleccionar una persona, se autocompletan automáticamente sus datos (nombre, RUN, domicilio, comuna, género)

### FR-09: Extracción de datos de la causa
- Tribunal: detecta Juzgado de Garantía, Tribunal de Juicio Oral en lo Penal, Unidad Especializada RPA
- Tipo de resolución: oficio, sentencia ejecutoriada, sentencia no ejecutoriada
- Delito: catálogo de aproximadamente 50 delitos comunes RPA + fallback por regex
- Fechas: detecta todas las fechas del documento (formatos "DD de MES de AAAA" y "DD/MM/AAAA")
- Si hay varias fechas, muestra un selector para que el usuario elija la del oficio o resolución

### FR-10: Detección automática de Art. 37 bis
- Si el documento menciona "37 bis", marca automáticamente la casilla correspondiente en el formulario
- En el Word generado, incluye la cita textual entre comillas: *"Evacúese informe Técnico conforme al artículo 37 bis"*

### FR-11: Extracción del adulto responsable
- Detecta nombre y teléfono del adulto responsable desde una tabla con encabezado "ADULTO RESPONSABLE"
- Los datos se insertan entre paréntesis en el certificado, con texto adaptado al género del adolescente ("adulto responsable" / "adulta responsable")

### FR-12: Botonera de medidas
- Botones individuales para cada medida: **PSA, MCA, IP, SBC, LAS, LAE, LAEIP, IRC**
- Botón especial **"🔀 Mixtas"** que despliega las combinaciones válidas
- Botones de medidas pendientes (PSA y mixtas) aparecen **deshabilitados** con tooltip explicativo
- El botón activo se destaca visualmente con color azul institucional
- Convive con el selectbox tradicional abajo en el formulario (ambos comparten el mismo estado)

### FR-13: Asignación de centro según medida y comuna
Para medidas estándar (MCA, SBC, LAS, LAE, LAEIP, SALIDAS ALTERNATIVAS):
- Busca en la planilla `CONSOLIDADO_OFERTA_DRM_V2.xlsx` el centro correspondiente
- Hace match por **sinónimos de la medida** (acepta "LAS", "Libertad Asistida Simple", "L.A.S")
- Hace match por **comuna normalizada** (ignora tildes y mayúsculas)
- Si hay un solo centro → lo asigna automáticamente
- Si hay varios → muestra un selector tipo radio para elegir
- Si no hay ninguno → muestra error y permite continuar sin centro

### FR-14: Selección de centro IP/IRC
Para medidas IP e IRC (que no dependen de la comuna del adolescente):
- Muestra un **selectbox** con los 4 centros disponibles: San Joaquín, San Bernardo, C.M.N. Til Til, Santiago
- Datos del centro (director, mail, teléfono) provienen del catálogo `CENTROS_IP_IRC` hardcodeado en el código

### FR-15: Campo de Abonos
- Para medidas LAS, LAE, LAEIP e IRC, aparece un campo de texto opcional "Abonos"
- Si se completa, el Word generado incluye el texto al final del párrafo principal:  
  *"Se hace presente al tribunal que el o la adolescente cuenta con **X días** de abono."*

### FR-16: Audiencia PII (Plan de Intervención Individual)
- Para medidas LAS, LAE, LAEIP e IRC, aparece una sección "Audiencia de Aprobación de PII"
- Checkbox para indicar si se fijó audiencia
- Si se marca, aparecen 5 campos: Fecha, Hora (default 11:00), Sala (default 802), Piso (default 8°), Edificio (default E)

### FR-17: Generación del Word de derivación
Para medidas distintas a IP/IRC, genera un Word con:
- Fecha alineada a la derecha
- Título centrado en negrita y subrayado: "CERTIFICA DERIVACIÓN VIRTUAL"
- Subtítulo centrado en negrita y subrayado: "SERVICIO NACIONAL DE REINSERCIÓN SOCIAL JUVENIL (S.N.R.S.J.)"
- Párrafo 1 justificado con sangría 1.25 cm: presentación del imputado con nombre en MAYÚSCULAS y negrita
- Párrafo 2: solicitud al director del centro con especificación legal en negrita y subrayado
- Email del centro como hipervínculo (azul + negrita + subrayado)
- Firma centrada con nombre del profesional, "Profesional de Línea" y "Coordinación Judicial D.R.M. - S.N.R.S.J."
- Logo institucional (si está disponible como `logo_snrsj.png` en la carpeta)
- Pie de página fijo en todas las páginas

### FR-18: Generación del Word para IP/IRC (con tabla)
Para medidas IP e IRC, genera un Word con formato distinto:
- Título: "DETERMINA I.R.C. PARA INGRESO" o "DETERMINA INTERNACIÓN PROVISORIA (I.P.) PARA INGRESO"
- Párrafo introductorio con referencias legales (art. 468 C.P.P. y art. 79 C.P. para IRC)
- **Tabla con estilo "Table Grid"** con las siguientes filas:
  - TRIBUNAL
  - NOMBRE
  - R.U.N
  - RUC
  - RIT
  - DELITO
  - RESOLUCIÓN
  - AUDIENCIA PII
  - FECHA DE RESOLUCIÓN
  - OBSERVACIONES
  - DURACIÓN Y ABONOS (solo IRC, si están completados)
- Párrafo de certificación
- Nombre del centro centrado, negrita y subrayado
- Detalles del centro con email en hipervínculo
- Cierre "Saluda atte., a VS.,"
- Firma centrada

### FR-19: Nombre del archivo de salida
Formato del nombre:
- **Estándar:** `{Nombre}_{Medida}_{Tribunal}_{RIT}_{RUC}.docx`
- **Para IP/IRC:** `{Nombre}_{Medida}_{Sigla_Centro}_{Tribunal}_{RIT}_{RUC}.docx`
- Las siglas de centro son: `San_Joaquin`, `San_Bernardo`, `Til_Til`, `Santiago`

### FR-20: Limpieza para nuevo caso
- Botón "🧹 Limpiar" en la esquina superior derecha
- Al cliquearlo, borra todos los campos del formulario excepto la fecha de hoy y el nombre del profesional firmante
- Permite iniciar inmediatamente un nuevo caso sin recargar la página

### FR-21: Interlineado 1.15 en el Word generado
- Todos los párrafos del documento Word generado tienen interlineado 1.15

### FR-22: Validación de campos obligatorios
- Antes de habilitar el botón de descarga, valida que estén completos: Nombre, Género, Tipo de Medida
- Para medidas estándar exige también la Comuna; para IP/IRC exige el Centro
- Si faltan campos, muestra un mensaje amarillo con la lista

---

## 8. Requerimientos No Funcionales

### NFR-01: Plataforma
- Sistema operativo: **Windows 10 o Windows 11**
- Compatible con Mac (con ajustes menores documentados)

### NFR-02: Lenguaje y framework
- Lenguaje: **Python 3.10 o superior**
- Framework UI: **Streamlit** (versión actual)
- Bibliotecas: `pdfplumber`, `python-docx`, `PyPDF2`, `pandas`, `openpyxl`

### NFR-03: Rendimiento
- Tiempo de carga inicial de la app: menor a 10 segundos
- Tiempo de procesamiento de documentos PDF/Word: menor a 5 segundos por caso típico (3-5 documentos)
- Tiempo de generación del Word de salida: menor a 2 segundos

### NFR-04: Usabilidad
- Interfaz en español
- Botones y campos con etiquetas claras y tooltips de ayuda
- Mensajes de error en lenguaje no técnico
- Optimización visual para no requerir scroll innecesario (botón Limpiar pequeño, sidebar compacto)

### NFR-05: Seguridad y privacidad
- Operación 100% local: ningún dato sale del computador del usuario
- No requiere autenticación (uso individual en estación de trabajo)
- No envía telemetría ni datos analíticos a terceros
- No utiliza servicios pagos (descartado uso de API de Anthropic/OpenAI por costo y privacidad)

### NFR-06: Robustez
- Manejo de errores graceful: si un PDF falla, la app muestra advertencia pero no se cae
- Fallback automático de detección por tablas → detección por regex
- Validación de extensión de archivo antes de procesar

### NFR-07: Mantenibilidad
- Código fuente versionado (v1 → v15 actualmente)
- Catálogos importantes (medidas, sinónimos, centros IP/IRC) en constantes fácilmente editables al inicio del código
- Comentarios en español indicando qué versión introdujo cada bloque (`# 🆕 V15: ...`)

### NFR-08: Instalabilidad
- Instructivo paso a paso en formato Word incluido en el paquete de entrega
- Archivo `.bat` para iniciar la app con un doble clic
- Comando único de instalación de dependencias

### NFR-09: Compatibilidad de archivos generados
- El Word generado se abre correctamente en Microsoft Word 2016 o superior
- Compatible con LibreOffice Writer
- Formato tamaño Carta (215.9 × 279.4 mm)

---

## 9. Reglas de Negocio

### RN-01: Identificación del imputado
- El imputado se identifica exclusivamente por su RUN (no RUC)
- En tablas con encabezado "VICTIMA", "VÍCTIMA" o "ADULTO RESPONSABLE", las personas listadas **NO** son el imputado

### RN-02: Distinción RUC vs RUN
- El **RUC** tiene 10-12 dígitos y dígito verificador, siempre precedido por la palabra "RUC"
- El **RUN** tiene 7-9 dígitos y dígito verificador, asociado al imputado
- Cuando un RUT aparece sin contexto, primero se verifica que no coincida con el RUC ya detectado

### RN-03: Formato chileno del RUN
- Formato final siempre `XX.XXX.XXX-X` o `X.XXX.XXX-X` (sin ceros iniciales)
- Ejemplos: `0022846782-0` → `22.846.782-0`; `8765432-9` → `8.765.432-9`

### RN-04: Centro según comuna y medida
- Para medidas estándar (MCA, SBC, LAS, LAE, LAEIP, SALIDAS ALTERNATIVAS), el centro se determina por **intersección** de la comuna del adolescente con la medida ordenada por el tribunal, según planilla oficial
- Si la comuna está en "COMUNAS PRIORIZADAS", tipo = "Priorizada"
- Si está en "COMUNAS NO PRIORIZADAS", tipo = "No priorizada"
- Si está en ambas (caso de varios centros), el usuario decide

### RN-05: Centro para IP / IRC
- Los centros de Internación Provisoria (IP) e Internación en Régimen Cerrado (IRC) son centros de **administración directa** del S.N.R.S.J. y NO dependen de la comuna del adolescente
- El profesional elige manualmente entre los 4 centros disponibles: San Joaquín, San Bernardo, C.M.N. Til Til o Santiago

### RN-06: Tratamiento adaptado al género
- Si género = Masculino: "don", "domiciliado", "derivado", "al adolescente individualizado", "adulto responsable"
- Si género = Femenino: "doña", "domiciliada", "derivada", "a la adolescente individualizada", "adulta responsable"

### RN-07: Adulto responsable opcional
- Si los campos del adulto responsable están vacíos, el Word generado **NO debe** incluir paréntesis vacíos
- Si está parcialmente lleno (ej. nombre sin teléfono), se incluye solo lo que está completo

### RN-08: Sin valores por defecto en duración
- El campo "Duración de la sanción" para LAS/LAE/LAEIP no debe tener un valor por defecto (como "6 meses")
- Debe arrancar vacío con un placeholder gris a modo de pista

### RN-09: Trazabilidad por nombre de archivo
- El nombre del archivo debe contener todos los identificadores únicos para que el archivo sea localizable por nombre sin depender de un sistema de gestión documental

### RN-10: Pie de página institucional fijo
- Todos los Word generados deben incluir el pie de página: *"Av. Pedro De Valdivia N° 4070, Ñuñoa. Fono: 22.3980.04.00"*

### RN-11: Formato gráfico oficial
- Fuente: **Bookman Old Style 12 pt**
- Márgenes: **2.5 cm en los 4 bordes**
- Tamaño de página: **Carta (8.5" × 11")**
- Interlineado: **1.15**
- Sangría primera línea de párrafos del cuerpo: **1.25 cm**

### RN-12: Combinaciones mixtas válidas
Las combinaciones de medidas mixtas permitidas son únicamente:
- IRC + LAEIP
- IRC + LAE
- IRC + LAS
- LAEIP + LAE
- LAEIP + LAS

Otras combinaciones (ej. LAS + LAE, MCA + LAS, etc.) **no son válidas** y no aparecen en el botón Mixtas.

---

## 10. Arquitectura Técnica

### 10.1 Diagrama conceptual

```
┌─────────────────────────────────────────────────────────┐
│            ESTACIÓN DE TRABAJO DEL PROFESIONAL          │
│                                                          │
│  ┌──────────────────┐      ┌───────────────────────┐    │
│  │  NAVEGADOR WEB   │◄────►│  STREAMLIT (Python)   │    │
│  │  (localhost:8501)│      │  - Lógica de UI       │    │
│  └──────────────────┘      │  - Extracción datos   │    │
│                            │  - Generación Word    │    │
│                            └──────────┬────────────┘    │
│                                       │                  │
│             ┌────────────────────────┼─────────────┐    │
│             ▼                        ▼             ▼    │
│   ┌──────────────┐         ┌─────────────────┐  ┌──────┐│
│   │ pdfplumber + │         │ CONSOLIDADO_    │  │python││
│   │ PyPDF2       │         │ OFERTA_DRM_V2   │  │-docx ││
│   │ (lectura PDF)│         │ .xlsx           │  │(out) ││
│   └──────────────┘         └─────────────────┘  └──────┘│
│                                                          │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
            ┌────────────────────────────────┐
            │  ARCHIVO WORD DE SALIDA (.docx)│
            │  + nombre estructurado         │
            └────────────────────────────────┘
```

### 10.2 Componentes del sistema

| Componente | Tecnología | Función |
|---|---|---|
| **Interfaz de usuario** | Streamlit (Python) | Renderiza formulario web en localhost:8501 |
| **Lector PDF** | pdfplumber (primario), PyPDF2 (fallback) | Extrae texto y tablas estructuradas |
| **Lector Word** | python-docx | Lee párrafos y tablas de .docx |
| **Extractor de datos** | Funciones Python custom + regex | Aplica reglas de detección por contexto |
| **Catálogo de comunas y centros** | Pandas + openpyxl | Lee `CONSOLIDADO_OFERTA_DRM_V2.xlsx` |
| **Generador Word** | python-docx | Construye certificado con formato institucional |
| **Catálogo IP/IRC** | Constante Python (hardcoded) | Datos de los 4 centros de internación |
| **Lanzador** | iniciar_app.bat | Script Windows para arrancar el servidor local |

### 10.3 Estructura de carpetas

```
DerivacionDRM/
├── app_derivacion_v15.py           ← Código principal de la aplicación
├── CONSOLIDADO_OFERTA_DRM_V2.xlsx  ← Planilla de oferta programática
├── iniciar_app.bat                 ← Lanzador Windows
├── logo_snrsj.png                  ← Logo institucional (opcional)
└── INSTRUCTIVO_INSTALACION.docx    ← Guía paso a paso
```

### 10.4 Modelo de datos en sesión

La aplicación mantiene su estado en `st.session_state` con las siguientes claves principales:

| Clave | Descripción |
|---|---|
| `fe_{ck}` | Fecha de emisión del certificado |
| `pf_{ck}` | Profesional firmante |
| `tr_{ck}` | Tribunal |
| `tpres_{ck}` | Tipo de resolución |
| `ruc_{ck}`, `rit_{ck}`, `del_{ck}` | Datos de la causa |
| `nom_{ck}`, `run_{ck}`, `gen_{ck}` | Datos del adolescente |
| `dom_{ck}`, `com_{ck}` | Domicilio y comuna |
| `med_{ck}` | Medida seleccionada |
| `ar_{ck}`, `ta_{ck}`, `ca_{ck}` | Adulto responsable |
| `dur_ext_{ck}`, `abo_{ck}` | Duración y abonos |
| `fijo_pii_{ck}`, `fpii_{ck}`, etc. | Audiencia PII |
| `centro_ipirc_{ck}` | Centro IP/IRC seleccionado |
| `obs_ipirc_{ck}` | Observaciones IP/IRC |

El sufijo `_{ck}` (siendo `ck` un contador) permite resetear todos los campos cuando se cliquea "Limpiar" sin tener que conocer cada clave individualmente.

---

## 11. Flujos de Trabajo

### 11.1 Flujo principal — derivación estándar (LAS, LAE, LAEIP, MCA, SBC)

```
1. Profesional recibe documentos del tribunal (PDF/Word)
2. Doble clic en iniciar_app.bat
3. Navegador abre http://localhost:8501
4. Arrastra los archivos al panel de carga inteligente
5. La app extrae automáticamente:
   - Datos del imputado
   - Datos de la causa
   - Medida ordenada
6. Si hay coimputados, elige el imputado correcto del radio
7. Revisa que los datos detectados sean correctos
8. Si la medida no se detectó, la elige en la botonera (atajo) o en el selectbox
9. Confirma comuna (autocompletada o manual)
10. Si hay varios centros para esa combinación, elige cuál usar
11. (Opcional) Completa duración, abonos, audiencia PII
12. (Opcional) Completa datos del adulto responsable
13. Cliquea "📥 Procesar Caso y Descargar Word"
14. El Word se descarga con nombre estructurado
15. (Opcional) Cliquea "🧹 Limpiar" para el siguiente caso
```

### 11.2 Flujo IP / IRC

```
1-5. Igual que flujo principal
6. Selecciona IP o IRC en la botonera
7. Aparece selectbox "Centro IP/IRC de ingreso" con 4 opciones
8. Elige: San Joaquín / San Bernardo / Til Til / Santiago
9. (Para IRC) Completa duración y abonos opcionales
10. Si hay audiencia PII, marca casilla y completa
11. Completa observaciones (opcional)
12. Descarga Word con formato de TABLA (no párrafos corridos)
13. Nombre del archivo incluye sigla del centro: ej. "_San_Joaquin_"
```

### 11.3 Flujo manual (sin carga de documentos)

```
1. Doble clic en iniciar_app.bat
2. Salta el panel de carga (lo cierra)
3. Completa manualmente todos los campos del formulario
4. Cliquea descarga
```

---

## 12. Tipos de Medidas y Sanciones

### 12.1 Catálogo completo

| Sigla | Nombre | Base legal | Estado en app v15 |
|---|---|---|---|
| **PSA** | Programa de Salidas Alternativas | Ley N° 20.084 | 🟡 Pendiente formato |
| **MCA** | Sujeción a la Vigilancia de una Autoridad | Art. 155 letra B C.P.P. | ✅ Funcional |
| **IP** | Internación Provisoria | Art. 32 Ley N° 20.084 | ✅ Funcional (con tabla) |
| **SBC** | Prestación de Servicios en Beneficio de la Comunidad | Ley N° 20.084 | ✅ Funcional |
| **LAS** | Libertad Asistida Simple | Art. 13 Ley N° 20.084 | ✅ Funcional |
| **LAE** | Libertad Asistida Especial | Art. 14 Ley N° 20.084 | ✅ Funcional |
| **LAEIP** | Libertad Asistida Especial con Internación Parcial | Ley N° 20.084 | ✅ Funcional |
| **IRC** | Internación en Régimen Cerrado | Art. 17 Ley N° 20.084 | ✅ Funcional (con tabla) |
| **SALIDAS ALTERNATIVAS** | Suspensión Condicional del Procedimiento | Art. 237 C.P.P. | ✅ Funcional |

### 12.2 Combinaciones mixtas (pendientes)

| Combinación | Caso típico |
|---|---|
| **IRC + LAEIP** | Sanción mixta: período en régimen cerrado seguido de LAEIP |
| **IRC + LAE** | Sanción mixta: período en régimen cerrado seguido de LAE |
| **IRC + LAS** | Sanción mixta: período en régimen cerrado seguido de LAS |
| **LAEIP + LAE** | Continuación de programa: LAEIP seguida de LAE |
| **LAEIP + LAS** | Continuación de programa: LAEIP seguida de LAS |

### 12.3 Campos requeridos por medida

| Medida | Comuna | Centro IP/IRC | Duración | Abonos | Audiencia PII | Observaciones |
|---|---|---|---|---|---|---|
| MCA | ✓ | — | — | — | — | — |
| SBC | ✓ | — | ✓ (horas) | — | — | — |
| LAS | ✓ | — | ✓ | ✓ opcional | ✓ opcional | — |
| LAE | ✓ | — | ✓ | ✓ opcional | ✓ opcional | — |
| LAEIP | ✓ | — | ✓ | ✓ opcional | ✓ opcional | — |
| IP | — | ✓ | — | — | ✓ opcional | ✓ opcional |
| IRC | — | ✓ | ✓ | ✓ opcional | ✓ opcional | ✓ opcional |
| Salidas Alternativas | ✓ | — | — | — | — | — |

---

## 13. Catálogos y Bases de Datos

### 13.1 Planilla de oferta programática

**Archivo:** `CONSOLIDADO_OFERTA_DRM_V2.xlsx`  
**Hoja:** `Desacumulado`  
**Mantenedor:** Coordinación Judicial D.R.M.

| Columna | Tipo | Descripción |
|---|---|---|
| PROGRAMA | Texto | Nombre del centro / programa |
| Tipo de medida o sanción | Texto | Medida que atiende (LAS, LAE, MCA, etc.) |
| COMUNAS PRIORIZADAS | Texto | Comunas atendidas con prioridad (separadas por coma) |
| COMUNAS NO PRIORIZADAS | Texto | Comunas atendidas si hay disponibilidad |
| DIRECCION | Texto | Dirección física del centro |
| DIRECTOR | Texto | Nombre del director/a responsable |
| CONTACTO MAIL | Texto | Correo institucional del centro |
| TELEFONO | Texto | Teléfono de contacto |

### 13.2 Catálogo de centros IP/IRC (hardcoded)

| Centro | Director | Mail | Teléfono |
|---|---|---|---|
| **San Joaquín** | Virna Salazar | ingresos.ipircsnjqn@reinsercionjuvenil.cl | +56 9 7835 9080 |
| **San Bernardo** | Miguel González Rubio | estadisticas.sanbdo@reinsercionjuvenil.cl | 22 592 3302 |
| **C.M.N. Til Til** | Eduardo Quevedo | estadisticas.tiltil@reinsercionjuvenil.cl | +56 9 5202 9630 |
| **Santiago** | Paula Alcayaga T. | yemina.vargas@reinsercionjuvenil.cl | — |

### 13.3 Diccionario de sinónimos por medida

Utilizado para buscar en la planilla cuando esta usa el nombre completo en lugar de la sigla:

```python
SINONIMOS_MEDIDA = {
    "MCA": ["mca", "medida cautelar ambulatoria", "sujeción a la vigilancia", "155 letra b"],
    "SBC": ["sbc", "servicios en beneficio", "prestación de servicios"],
    "LAS": ["las", "libertad asistida simple", "l.a.s"],
    "LAE": ["lae", "libertad asistida especial"],
    "LAEIP": ["laeip", "lae-ip", "libertad asistida especial con internación parcial"],
    "IP": ["ip", "internación provisoria"],
    "IRC": ["irc", "crc", "régimen cerrado", "centro cerrado"],
    "SALIDAS ALTERNATIVAS": ["salidas alternativas", "suspensión condicional", "art. 237"],
}
```

### 13.4 Catálogo de nombres femeninos

Lista de aproximadamente 60 nombres femeninos chilenos comunes utilizada para inferir género del adolescente.

### 13.5 Catálogo de delitos

Aproximadamente 50 tipos penales comunes en causas RPA: robo con violencia, robo en lugar habitado, hurto, tráfico ilícito de estupefacientes, lesiones, abuso sexual, homicidio, receptación, amenazas, daños, manejo en estado de ebriedad, entre otros.

---

## 14. Salidas del Sistema

### 14.1 Word de derivación estándar (MCA, SBC, LAS, LAE, LAEIP, SALIDAS ALTERNATIVAS)

Estructura del documento:

```
[Logo S.N.R.S.J. si está disponible]

                                                Santiago, [fecha de emisión]

              CERTIFICA DERIVACIÓN VIRTUAL
SERVICIO NACIONAL DE REINSERCIÓN SOCIAL JUVENIL (S.N.R.S.J.)

    Por medio del presente certifico que con esta fecha envío los
antecedentes de don/doña [NOMBRE EN MAYÚSCULAS], run XX.XXX.XXX-X,
domiciliado/a en [Calle Número Depto], comuna de [Comuna] (adulto
responsable: [Nombre], teléfono [Tel]), siendo derivado/a en forma no
presencial a la Red del S.N.R.S.J. en los siguientes términos:

    Señor(a) director(a) Centro [Nombre del Centro], solicito a usted
ingresar al adolescente individualizado a vuestro programa para el fin
de implementar la medida [...] específicamente la [Especificación legal
en negrita y subrayado], conforme a lo ordenado en [tipo resolución] de
fecha [DD de MES de AAAA] por la [Tribunal], en causa RUC [XXX], RIT
[XXX], por el delito de [delito]. La extensión y duración determinada
para el cumplimiento de esta medida será de: [duración]. Se hace
presente al tribunal que el o la adolescente cuenta con [X] de abono.

[Si Art. 37 bis:]
    Cabe señalar que el tribunal solicita expresamente: "Evacúese
informe Técnico conforme al artículo 37 bis", el cual será elaborado
por el equipo regional.

[Si audiencia PII fijada:]
    El Tribunal fijó audiencia de aprobación de Plan de Intervención
Individual para el día [Fecha], a las [Hora] hrs, en la sala [Sala],
[Piso] piso, edificio [Edif], del Centro de Justicia de Santiago.

    Se solicita gestionar el ingreso informando los resultados [...]
y requerir la habilitación de la casilla [email@centro.cl] para recibir
las actas y resoluciones de la causa.

    El centro tiene su ubicación en [Dirección], fono [Teléfono].



                    [Nombre del Profesional]
                    Profesional de Línea
                Coordinación Judicial D.R.M. - S.N.R.S.J.

────────────────────────────────────────────────────────────────────
Av. Pedro De Valdivia N° 4070, Ñuñoa.  Fono: 22.3980.04.00
```

### 14.2 Word de derivación IP / IRC (con tabla)

Estructura:

```
[Logo S.N.R.S.J. si está disponible]

                                                Santiago, [fecha emisión]


              DETERMINA I.R.C. PARA INGRESO


    Por medio de resolución judicial dictada por VS., según lo
establecido en los artículos 468 del C.P.P y 79 del C.P., se ha
ordenado al Servicio Nacional de Reinserción Social Juvenil
(S.N.R.S.J.) el ingreso a Régimen Cerrado en los siguientes términos:


┌─────────────────────┬─────────────────────────────────────────────┐
│ TRIBUNAL            │ Unidad Especializada RPA                    │
├─────────────────────┼─────────────────────────────────────────────┤
│ NOMBRE              │ JUAN PÉREZ GARCÍA                           │
├─────────────────────┼─────────────────────────────────────────────┤
│ R.U.N               │ 22.846.782-0                                │
├─────────────────────┼─────────────────────────────────────────────┤
│ RUC                 │ 2600664806-0                                │
├─────────────────────┼─────────────────────────────────────────────┤
│ RIT                 │ 2903-2026                                   │
├─────────────────────┼─────────────────────────────────────────────┤
│ DELITO              │ ROBO CON VIOLENCIA                          │
├─────────────────────┼─────────────────────────────────────────────┤
│ RESOLUCIÓN          │ SENTENCIA EJECUTORIADA                      │
├─────────────────────┼─────────────────────────────────────────────┤
│ AUDIENCIA PII       │ 15 de junio de 2026 a las 11:00 hrs...     │
├─────────────────────┼─────────────────────────────────────────────┤
│ FECHA DE RESOLUCIÓN │ 10 de mayo de 2026                          │
├─────────────────────┼─────────────────────────────────────────────┤
│ OBSERVACIONES       │ [Texto libre del usuario]                   │
├─────────────────────┼─────────────────────────────────────────────┤
│ DURACIÓN Y ABONOS   │ Duración: 3 años · Abonos: 180 días         │
└─────────────────────┴─────────────────────────────────────────────┘


    Certifico que en cumplimiento a lo ordenado por VS. y del
artículo 150 inciso 2º del C.P.P. se han remitido los antecedentes
para la ejecución de sentencia e ingreso al siguiente Centro de
Administración Directa de la Red del S.N.R.S.J. de esta Región para
cumplimiento de esta sanción:


              Centro IP - IRC San Joaquín


    El centro se encuentra ubicado en Comuna de San Joaquín, Región
Metropolitana, teléfono +56 9 7835 9080, y su Director(a) responsable
es Virna Salazar, correo electrónico ingresos.ipircsnjqn@reinsercionjuvenil.cl.


Saluda atte., a VS.,


                    [Nombre del Profesional]
                    Profesional de Línea
                Coordinación Judicial D.R.M. - S.N.R.S.J.

────────────────────────────────────────────────────────────────────
Av. Pedro De Valdivia N° 4070, Ñuñoa.  Fono: 22.3980.04.00
```

### 14.3 Convención de nombre de archivo

**Patrón general:**
```
{Nombre_Adolescente}_{Sigla_Medida}[_{Sigla_Centro}]_{Tribunal}_{RIT}_{RUC}.docx
```

**Ejemplos:**
- LAS: `Cristobal_Carrasco_Rodriguez_LAS_Unidad_Especializada_Rpa_2903-2026_2600664806-0.docx`
- IRC: `Juan_Perez_Garcia_IRC_San_Joaquin_Unidad_Especializada_Rpa_2909-2026_2600665257-2.docx`
- IP: `Maria_Gonzalez_Soto_IP_Til_Til_4_Juzgado_Garantia_Santiago_500-2026_2600700000-1.docx`

---

## 15. Casos de Uso

### CU-01: Generar certificado MCA para adolescente único en Lo Espejo

**Actor:** Profesional de Línea D.R.M.  
**Precondición:** App instalada; planilla de oferta cargada en la misma carpeta  
**Flujo principal:**

1. Profesional arrastra al panel: oficio + acta de audiencia
2. App detecta: nombre, RUN, domicilio "Avenida Jose Joaquin Prieto Vial Block 38 Dpto 34", comuna "Lo Espejo", medida MCA (art. 155 letra B), RUC, RIT, delito, tribunal
3. App marca automáticamente "Informe Técnico Art. 37 bis" (detectó la mención en el oficio)
4. Sidebar muestra: ✅ Centro Asignado: "MCA Centro Sur — Av. XYZ"
5. Profesional revisa y confirma datos
6. Cliquea "Descargar Word"
7. Se descarga `Juan_Lopez_Perez_MCA_Unidad_Especializada_Rpa_2903-2026_2600664806-0.docx`

**Post-condición:** Word generado con formato institucional, listo para enviar por correo al centro.

### CU-02: Coimputados (3 personas) — elegir adolescente correcto

**Actor:** Profesional de Línea D.R.M.  
**Precondición:** Acta con 3 imputados, todos adolescentes  
**Flujo principal:**

1. Profesional arrastra el acta
2. App muestra alerta amarilla: "Se detectaron 3 personas. Seleccione el imputado..."
3. Profesional cliquea la opción "2. Jeyson Castro Reyes (22.857.912-2)"
4. App autocompleta: nombre, RUN, domicilio, comuna, género (inferido)
5. Profesional completa el resto del formulario y descarga

### CU-03: IRC para San Joaquín con tabla

**Actor:** Profesional de Línea D.R.M.  
**Precondición:** Sentencia condenatoria a 3 años de régimen cerrado  
**Flujo principal:**

1. Profesional arrastra la sentencia
2. Datos del imputado autocompletados
3. Cliquea botón "IRC" en la botonera (no estaba en el documento la sigla)
4. Aparece selectbox "Centro IRC de ingreso" → elige "San Joaquín"
5. Completa duración "3 años", abonos "180 días"
6. Marca audiencia PII, completa fecha 20 de junio 2026, 10:30 hrs, sala 501, piso 5°, edificio A
7. Escribe en Observaciones: "Caso de alta complejidad, coordinación previa con equipo técnico"
8. Descarga `Cristobal_Garcia_Lopez_IRC_San_Joaquin_4_Juzgado_Garantia_Santiago_321-2026_2600555000-2.docx`
9. Word generado tiene la tabla con 11 filas y los datos del centro San Joaquín

### CU-04: Comuna no tiene oferta de la medida

**Actor:** Profesional de Línea D.R.M.  
**Precondición:** Comuna remota sin centro asignado para esa medida  
**Flujo principal:**

1. Profesional carga documentos, app detecta todo
2. Sidebar muestra error: "⚠️ No se encontró centro para 'Calera de Tango' en medida 'LAS'"
3. Profesional consulta manualmente con Coordinación; recibe instrucción de derivar a centro alternativo
4. Profesional cambia manualmente la comuna a una adyacente cubierta
5. La app vuelve a buscar y asigna nuevo centro
6. Descarga el Word

### CU-05: Múltiples centros para una comuna

**Actor:** Profesional de Línea D.R.M.  
**Precondición:** Comuna cubierta tanto por centro priorizado como no priorizado  
**Flujo principal:**

1. Profesional confirma comuna "Santiago" para medida LAE
2. App muestra: "Se encontraron 2 centros disponibles. Seleccione cuál usar:"
3. Aparecen 2 opciones radio: "1. Centro X (Priorizada)" y "2. Centro Y (No priorizada)"
4. Profesional cliquea opción 1
5. Sidebar muestra centro seleccionado
6. Descarga Word con datos del centro elegido

---

## 16. Restricciones y Supuestos

### 16.1 Restricciones técnicas

- **PDFs deben ser de texto, no escaneados.** Si son escaneados (imagen), el sistema no puede extraer texto y muestra advertencia.
- **Word debe ser .docx (no .doc legacy).** Si el usuario tiene un .doc antiguo, debe convertirlo primero a .docx en Microsoft Word.
- **Tamaño máximo de archivo:** 200 MB por archivo (límite de Streamlit por defecto).
- **No multiusuario:** Cada estación de trabajo corre su propia instancia local; no hay concurrencia.

### 16.2 Restricciones de negocio

- El sistema **NO valida** la legalidad del contenido. Esa responsabilidad sigue siendo del profesional firmante.
- El sistema **NO reemplaza** el juicio profesional sobre casos atípicos o excepcionales.
- El catálogo `CENTROS_IP_IRC` está hardcodeado en el código. Si cambia un director, mail o teléfono, requiere editar el código (no es modificable desde la planilla Excel).

### 16.3 Restricciones operacionales

- La planilla `CONSOLIDADO_OFERTA_DRM_V2.xlsx` debe mantenerse actualizada manualmente cuando hay cambios en la oferta programática.
- El nombre exacto del archivo Excel debe respetarse; si cambia, también debe modificarse en el código de la app.
- El logo `logo_snrsj.png` es opcional pero recomendado; sin él, el Word se genera sin imagen.

### 16.4 Supuestos

- **S-01:** Los documentos judiciales mantienen el formato actual del Poder Judicial chileno (tablas estandarizadas en actas de audiencia con encabezados "NOMBRE IMPUTADO", "RUT", "DIRECCION", "COMUNA").
- **S-02:** Los RUCs en Chile mantienen el formato de 10-12 dígitos con guion y dígito verificador.
- **S-03:** Los nombres de los centros y sus correos institucionales no cambian frecuentemente.
- **S-04:** El profesional cuenta con Microsoft Word 2016+ o LibreOffice para abrir y editar el documento generado antes de enviarlo.
- **S-05:** El profesional tiene permisos de instalación de software en su computador (para instalar Python y librerías).

---

## 17. Roadmap y Estado de Implementación

### 17.1 Versiones desarrolladas

| Versión | Hitos principales |
|---|---|
| **v1-v3** | Prototipo inicial; formulario manual; generación básica del Word |
| **v4** | Carga inteligente de PDFs con PyPDF2; primer intento de extracción |
| **v5** | Auto-llenado del formulario desde session_state; fix bugs de carga |
| **v6** | Mejoras en regex de extracción (nombre, RUC, RIT); detección de fechas múltiples |
| **v7** | Sistema de puntaje (scoring) para elegir comuna correcta evitando víctima |
| **v8** | Intento con API de Anthropic (descartado por costo y dependencia externa) |
| **v9** | Cambio a `pdfplumber` para preservar tablas; extracción por tablas funciona |
| **v10** | Formato Word completo: negrita, subrayado, colores, pie de página, logo, márgenes |
| **v11** | Selector de múltiples personas; selector de múltiples centros; campo Abonos; interlineado 1.15 |
| **v12** | Optimización CSS; fix nombres con paréntesis; sin "6 meses" hardcodeado |
| **v13** | **Botonera de medidas**; activación LAEIP con formato LAS/LAE |
| **v14** | Activación IP/IRC con catálogo de centros y formato de **tabla** en el Word |
| **v15** | Vuelta a v10 limpia + reaplicación de todo; **fix Peñalolén con sinónimos y normalización de tildes** |

### 17.2 Funcionalidades implementadas (✅) y pendientes (🟡)

| Funcionalidad | Estado |
|---|---|
| Carga de PDF y Word | ✅ |
| Extracción automática de datos | ✅ |
| Formato Word con logo y pie de página | ✅ |
| Pantalla optimizada (sin scroll, botones legibles) | ✅ |
| MCA, SBC, LAS, LAE, SALIDAS ALTERNATIVAS | ✅ |
| LAEIP con formato LAS/LAE | ✅ |
| IP e IRC con formato de tabla | ✅ |
| Catálogo de 4 centros IP/IRC | ✅ |
| Selección de coimputado | ✅ |
| Selección de centro entre múltiples opciones | ✅ |
| Campo Abonos | ✅ |
| Sección audiencia PII | ✅ |
| Botonera de medidas | ✅ |
| Interlineado 1.15 | ✅ |
| Nombre de archivo con sigla del centro | ✅ |
| Búsqueda robusta con sinónimos y normalización | ✅ |
| Instructivo de instalación nivel principiante | ✅ |
| **Formato PSA (Programa de Salidas Alternativas)** | 🟡 Pendiente |
| **Formato combinaciones mixtas (IRC+LAEIP, IRC+LAE, etc.)** | 🟡 Pendiente |
| OCR para PDFs escaneados | 🟡 Futuro |
| Validación de dígito verificador RUT/RUC | 🟡 Futuro |
| Historial de derivaciones generadas | 🟡 Futuro |
| Exportar borradores como JSON | 🟡 Futuro |
| Despliegue en servidor compartido del Servicio | 🟡 Futuro |

### 17.3 Próximos pasos sugeridos

1. **Inmediato (cuando se reciban los formatos):**
   - Implementar formato Word para PSA
   - Implementar formato Word para las 5 combinaciones mixtas
2. **Corto plazo:**
   - Refinamiento del CSS según feedback en uso productivo
   - Actualización del instructivo .docx con capturas de v15
3. **Mediano plazo:**
   - Validación automática del dígito verificador de RUN
   - Función "Guardar borrador" para casos a medio completar
4. **Largo plazo:**
   - Integración OCR con Tesseract para PDFs escaneados
   - Modo multiusuario con base de datos centralizada de derivaciones emitidas

---

## 18. Riesgos

| ID | Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|---|
| **R-01** | El Poder Judicial cambia el formato de las actas y la extracción automática deja de funcionar | Alto | Media | Fallback manual: el usuario siempre puede completar a mano; código modular para ajustar regex/parseo |
| **R-02** | La planilla `CONSOLIDADO_OFERTA_DRM_V2.xlsx` queda desactualizada | Medio | Alta | Responsable designado de mantención mensual; alertar al equipo cuando un centro reportado no aparece |
| **R-03** | Un cambio en la directiva o director de un centro IP/IRC no se refleja | Bajo | Media | Catálogo en código fácilmente editable; revisión semestral |
| **R-04** | El usuario olvida marcar la casilla "Add Python to PATH" durante la instalación | Medio | Alta | Instructivo enfatiza este paso en negrita y con captura; sección de problemas frecuentes |
| **R-05** | Un PDF escaneado (no de texto) no se procesa | Bajo | Media | Mensaje claro al usuario; opción manual siempre disponible |
| **R-06** | El sistema operativo del usuario no es Windows | Bajo | Baja | Documentación adicional para Mac; código es multiplataforma |
| **R-07** | Conflicto entre múltiples versiones de Python instaladas | Medio | Media | Documentar uso de `python -m streamlit` en lugar de `streamlit` directo |
| **R-08** | Pérdida del código fuente o de la planilla | Alto | Baja | Respaldo regular del usuario; copia en pendrive o disco institucional |
| **R-09** | Falsos positivos en detección de género desde el nombre (ej. nombres unisex) | Bajo | Media | El usuario siempre puede corregir con el selector; lista de nombres mantenida |
| **R-10** | El profesional firmante cambia y el nombre queda hardcoded en el código | Medio | Media | El campo es editable en el formulario; valor por defecto es solo una conveniencia |

---

## 19. Glosario

| Término | Definición |
|---|---|
| **S.N.R.S.J.** | Servicio Nacional de Reinserción Social Juvenil. Creado por la Ley N° 21.527, sucesor de SENAME en materias de adolescentes infractores |
| **D.R.M.** | Dirección Regional Metropolitana del S.N.R.S.J. |
| **R.P.A.** | Responsabilidad Penal Adolescente; régimen establecido por la Ley N° 20.084 |
| **RUC** | Rol Único de Causa; identificador único de una causa judicial |
| **RIT** | Rol Interno del Tribunal; número correlativo asignado por el tribunal |
| **RUN** | Rol Único Nacional; identificador de la persona natural en Chile (equivalente al RUT) |
| **C.P.P.** | Código Procesal Penal |
| **C.P.** | Código Penal |
| **MCA** | Medida Cautelar Ambulatoria; específicamente, sujeción a la vigilancia de una autoridad (art. 155 letra B C.P.P.) |
| **SBC** | Prestación de Servicios en Beneficio de la Comunidad (sanción) |
| **LAS** | Libertad Asistida Simple (sanción, art. 13 Ley 20.084) |
| **LAE** | Libertad Asistida Especial (sanción, art. 14 Ley 20.084) |
| **LAEIP** | Libertad Asistida Especial con Internación Parcial |
| **IP** | Internación Provisoria (medida cautelar privativa de libertad) |
| **IRC** | Internación en Régimen Cerrado (sanción privativa de libertad, art. 17 Ley 20.084) |
| **CRC** | Sigla alternativa para IRC ("Centro de Régimen Cerrado") |
| **PSA** | Programa de Salidas Alternativas |
| **PII** | Plan de Intervención Individual; instrumento de planificación del trabajo con el adolescente |
| **Art. 37 bis** | Norma de la Ley 20.084 que ordena al tribunal pedir un Informe Técnico al equipo del Servicio |
| **Art. 40 ter** | Norma de la Ley 20.084 que regula la mediación en SBC |
| **Acta de audiencia** | Documento emitido por el tribunal que registra lo ocurrido en una audiencia judicial |
| **Oficio** | Comunicación formal entre instituciones; en este contexto, del tribunal hacia el S.N.R.S.J. |
| **Sentencia ejecutoriada** | Sentencia que ya no admite recursos y debe cumplirse |
| **Adulto responsable** | Persona adulta que el tribunal identifica como referente del adolescente |
| **Streamlit** | Framework de Python para crear aplicaciones web interactivas |
| **pdfplumber** | Biblioteca de Python para extraer texto y tablas estructuradas de PDFs |
| **python-docx** | Biblioteca de Python para crear y editar documentos Word |

---

## 20. Anexos

### Anexo A — Estructura de archivos a entregar al usuario final

```
DerivacionDRM/                                  ← Carpeta principal (en el Escritorio)
├── app_derivacion_v15.py                       ← Código de la app (~1500 líneas)
├── CONSOLIDADO_OFERTA_DRM_V2.xlsx              ← Planilla de oferta programática
├── iniciar_app.bat                             ← Lanzador con doble clic
├── logo_snrsj.png                              ← Logo institucional (opcional)
├── INSTRUCTIVO_INSTALACION.docx                ← Guía paso a paso (~10 páginas)
└── BRD_Sistema_Derivacion_Virtual.md           ← Este documento
```

### Anexo B — Comando de instalación de dependencias

Ejecutar **una sola vez** después de instalar Python:

```bash
python -m pip install streamlit pandas python-docx PyPDF2 pdfplumber openpyxl
```

### Anexo C — Variables de configuración relevantes en el código

| Constante | Ubicación | Modificable |
|---|---|---|
| `NOMBRE_PROFESIONAL_FIJO` | Línea ~20 | ✓ (cuando cambia el firmante) |
| `OPCIONES_MEDIDA` | Línea ~24 | ✗ (orden de medidas en selectbox) |
| `MEDIDAS_PENDIENTES` | Línea ~27 | ✓ (cuando se activa PSA) |
| `COMBINACIONES_MIXTAS` | Línea ~30 | ✓ (cuando se activan formatos mixtos) |
| `SINONIMOS_MEDIDA` | Línea ~40 | ✓ (al agregar nuevas variantes) |
| `TEXTOS_LEGALES` | Línea ~54 | ✓ (cuando cambia la base legal) |
| `CENTROS_IP_IRC` | Línea ~65 | ✓ (cuando cambia director, mail, teléfono) |
| `EXCEL_PATH` | Línea ~620 | ✓ (si cambia el nombre del archivo de oferta) |

### Anexo D — Referencias normativas

- **Ley N° 20.084** — Establece un sistema de responsabilidad de los adolescentes por infracciones a la ley penal
- **Ley N° 21.527** — Crea el Servicio Nacional de Reinserción Social Juvenil
- **Código Procesal Penal** — Especialmente arts. 155, 237, 468
- **Código Penal** — Especialmente art. 79

### Anexo E — Contacto del responsable del sistema

**Juan Manuel Olivares Oyarzún**  
Profesional de Línea  
Coordinación Judicial D.R.M.  
Servicio Nacional de Reinserción Social Juvenil (S.N.R.S.J.)  
Av. Pedro De Valdivia N° 4070, Ñuñoa, Santiago  
Fono: 22.3980.04.00

---

**Fin del documento — BRD Sistema de Derivación Virtual v1.0**

*Este BRD describe el estado actual del proyecto a mayo de 2026 (versión 15 del software). Se actualizará cuando se implementen los formatos de PSA y las combinaciones mixtas, así como cualquier ajuste mayor a la arquitectura o reglas de negocio.*
