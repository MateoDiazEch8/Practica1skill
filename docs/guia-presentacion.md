# Guía de presentación — skill `expense-report`

Presentador: Mateo Israel Diaz Echeverria
Duración objetivo: 3 minutos. Abrir PowerShell en `C:\Certi2\Practica1skill` antes de empezar.

## Guion de demo (3 minutos)

| Tiempo | Qué decir | Comando exacto |
|---|---|---|
| 0:00–0:20 | "Esta skill convierte un CSV de gastos en un reporte HTML. Primero valida, después genera." Mostrar el árbol del repo. | `tree /F skills` |
| 0:20–0:45 | "Este es el CSV de ejemplo: fecha, descripción, categoría y monto." | `Get-Content skills/expense-report/assets/sample_expenses.csv` |
| 0:45–1:05 | **Caso exitoso.** "Exit 0; avisa que `misc` no es una categoría conocida y la agrupa en `otros`." | `python skills/expense-report/scripts/validate_csv.py skills/expense-report/assets/sample_expenses.csv` |
| 1:05–1:30 | **Caso con errores.** "Exit 1: lista las 4 filas con error y no sigue." | `python skills/expense-report/scripts/validate_csv.py skills/expense-report/assets/sample_invalid.csv` |
| 1:30–1:40 | **Archivo inexistente.** "Exit 2: problema de archivo, distinto de un error de datos." | `python skills/expense-report/scripts/validate_csv.py no_existe.csv` y luego `echo $LASTEXITCODE` |
| 1:40–2:10 | **Generar reporte** y abrirlo: total 1,010.50, categoría principal vivienda. | `python skills/expense-report/scripts/generate_report.py skills/expense-report/assets/sample_expenses.csv -o reporte.html` y luego `start reporte.html` |
| 2:10–2:30 | **Pruebas.** "8 verificaciones de extremo a extremo, todas PASS." | `python tests/run_tests.py` |
| 2:30–3:00 | Cerrar con las 4 decisiones de diseño (abajo) y mostrar el `SKILL.md`. | `Get-Content skills/expense-report/SKILL.md` |

Plan B si algo falla en vivo: mostrar las capturas de `docs/01` a `docs/05` desde el README en GitHub.

## Las 4 decisiones de diseño

1. **Solo biblioteca estándar de Python.** No hay `pip install`: la skill funciona en cualquier máquina con Python 3.9+ y Claude no tiene que instalar nada antes de usarla.
2. **Validar antes de generar.** `generate_report.py` vuelve a validar y se niega (exit 1) si hay errores, así el reporte nunca se calcula con datos dudosos. Los códigos de salida (0 válido, 1 datos, 2 archivo) le dicen a Claude qué hacer después: seguir, mostrar los errores al usuario o pedir otro archivo.
3. **Categorías en `references/categories.json`.** Las categorías y sus alias (`taxi` → `transporte`, `alquiler` → `vivienda`) son datos, no código: se agregan editando el JSON, sin tocar Python.
4. **Plantilla HTML en `assets/`.** El diseño del reporte está en `report_template.html` con marcadores `{{TOTAL}}`, `{{CATEGORY_ROWS}}`, etc. Cambiar el aspecto no requiere tocar los scripts, y el test comprueba que no queden marcadores sin reemplazar.

## 5 preguntas probables del docente

1. **¿Por qué una categoría desconocida es advertencia y no error?**
   Porque el dato sigue siendo un gasto real y el total sería incorrecto si se descartara. Se agrupa en `otros` y se avisa, para que el usuario decida si agrega la categoría al JSON.
2. **¿Cómo sabe Claude cuándo usar la skill?**
   Por la `description` del `SKILL.md`: dice cuándo usarla (CSV de gastos, pedir reporte o resumen) y cuándo no (ingresos, facturación, archivos que no son CSV). El cuerpo del `SKILL.md` fija el flujo: validar, generar, informar.
3. **¿Qué pasa si el CSV tiene errores y se ejecuta directo `generate_report.py`?**
   También valida internamente y termina con exit 1 sin crear el HTML. Lo cubre la prueba "reporte con CSV inválido se niega".
4. **¿Por qué tres códigos de salida distintos?**
   Para separar "tus datos tienen errores, corrígelos" (1) de "no pude leer el archivo" (2). Claude responde distinto en cada caso, y las pruebas verifican los tres.
5. **¿Cómo la extenderías?**
   Soportar otros separadores o formatos de fecha, exportar a PDF o agregar un gráfico en la plantilla. Gracias al diseño, casi todo se hace en `references/` y `assets/` sin cambiar la lógica de validación.
