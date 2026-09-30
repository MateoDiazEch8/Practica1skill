# Formato del CSV de gastos

Codificación UTF-8, separador coma, primera fila = encabezado.

| Columna | Obligatoria | Regla |
|---|---|---|
| `fecha` | sí | Formato `YYYY-MM-DD`, fecha real, no futura |
| `descripcion` | sí | Texto no vacío |
| `categoria` | sí | Una de `categories.json` (o un alias). Desconocida = advertencia, se agrupa en `otros` |
| `monto` | sí | Número > 0, con punto decimal (`12.50`) |

Errores que detecta `validate_csv.py`: archivo inexistente o vacío, columnas faltantes, fecha inválida o futura, monto no numérico o ≤ 0, descripción vacía.
