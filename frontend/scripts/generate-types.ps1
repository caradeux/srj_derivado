# Regenera src/api/types.ts contra el backend en 127.0.0.1:8000.
# Requiere que el backend esté corriendo en otra ventana.
param([string]$Url = "http://127.0.0.1:8000/openapi.json")
npx openapi-typescript $Url -o src/api/types.ts
