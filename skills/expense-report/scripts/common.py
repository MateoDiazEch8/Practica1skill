"""Lectura y validación compartida por validate_csv.py y generate_report.py."""
import csv
import sys
import json
from datetime import date, datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SKILL_DIR = Path(__file__).resolve().parent.parent
REQUIRED = ["fecha", "descripcion", "categoria", "monto"]


class FileProblem(Exception):
    """El archivo no existe, está vacío o no se puede leer (exit code 2)."""


def load_categories():
    data = json.loads((SKILL_DIR / "references" / "categories.json").read_text(encoding="utf-8"))
    return set(data["categorias"]), data["alias"]


def read_rows(path):
    p = Path(path)
    if not p.is_file():
        raise FileProblem(f"No existe el archivo: {path}")
    try:
        with p.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            header = [h.strip().lower() for h in (reader.fieldnames or [])]
            rows = [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in reader]
    except UnicodeDecodeError:
        raise FileProblem("El archivo no está en UTF-8.")
    if not header:
        raise FileProblem("El archivo está vacío.")
    return header, rows


def validate(header, rows):
    """Devuelve (errores, advertencias, registros_limpios). Fila 2 = primer dato."""
    errors, warnings, clean = [], [], []
    missing = [c for c in REQUIRED if c not in header]
    if missing:
        return [f"Faltan columnas obligatorias: {', '.join(missing)}"], warnings, clean
    if not rows:
        return ["El archivo no tiene filas de datos."], warnings, clean
    cats, alias = load_categories()
    for n, r in enumerate(rows, start=2):
        row_err = []
        d = m = None
        try:
            d = datetime.strptime(r["fecha"], "%Y-%m-%d").date()
            if d > date.today():
                row_err.append(f"fecha futura '{r['fecha']}'")
        except ValueError:
            row_err.append(f"fecha inválida '{r['fecha']}' (use YYYY-MM-DD)")
        if not r["descripcion"]:
            row_err.append("descripción vacía")
        try:
            m = float(r["monto"])
            if m <= 0:
                row_err.append(f"monto debe ser > 0 (es {r['monto']})")
        except ValueError:
            row_err.append(f"monto no numérico '{r['monto']}'")
        cat = r["categoria"].lower()
        cat = alias.get(cat, cat)
        if cat not in cats:
            warnings.append(f"Fila {n}: categoría desconocida '{r['categoria']}' -> se agrupa en 'otros'")
            cat = "otros"
        if row_err:
            errors.append(f"Fila {n}: " + "; ".join(row_err))
        else:
            clean.append({"fecha": d, "descripcion": r["descripcion"], "categoria": cat, "monto": m})
    return errors, warnings, clean
