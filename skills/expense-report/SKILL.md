---
name: expense-report
description: Valida un CSV de gastos personales o de equipo y genera un reporte HTML con totales por categoría y por mes. Úsala cuando el usuario tenga un archivo de gastos/egresos (.csv) y pida un resumen, reporte, análisis o "en qué gasté". No la uses para ingresos, facturación contable ni archivos que no sean CSV.
---

# expense-report

Convierte un CSV de gastos en un reporte HTML autocontenido (totales, porcentajes por categoría, evolución mensual, mayores gastos).

## Cuándo usarla
- El usuario entrega o menciona un `.csv` con gastos y quiere un reporte o resumen.
- Frases típicas: "genera el reporte de mis gastos", "¿en qué categoría gasté más?", "resume este CSV de egresos".

## Requisitos
- Python 3.9+ (solo biblioteca estándar, sin `pip install`).

## Flujo (seguir en orden)
1. **Validar** el archivo. Nunca generar el reporte sin validar primero:
   `python skills/expense-report/scripts/validate_csv.py <archivo.csv>`
   - Código de salida `0`: válido, continuar.
   - Código de salida `1`: hay errores (se listan con número de fila). **Detenerse**, mostrar los errores al usuario y pedir corrección. No inventar ni "arreglar" datos silenciosamente.
   - Código de salida `2`: el archivo no existe, está vacío o no se puede leer.
2. **Generar** el reporte:
   `python skills/expense-report/scripts/generate_report.py <archivo.csv> -o reporte.html`
   Usa `assets/report_template.html` como plantilla.
3. **Informar** al usuario: ruta del HTML, total gastado, categoría principal y cualquier advertencia (p. ej. categorías desconocidas agrupadas en "otros").

## Formato y categorías
- Columnas y reglas del CSV: `references/csv-format.md`
- Categorías válidas (y alias): `references/categories.json` (el validador las lee de aquí).

## Ejemplo
Entrada: `assets/sample_expenses.csv` → Salida: `reporte.html` con total 1,010.50 y categoría principal "vivienda".
Entrada inválida: `assets/sample_invalid.csv` → el validador termina con código 1 y lista las filas incorrectas.
