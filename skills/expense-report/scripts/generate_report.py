#!/usr/bin/env python3
"""Genera un reporte HTML a partir de un CSV de gastos válido."""
import argparse
import html
import sys
from collections import defaultdict
from common import FileProblem, SKILL_DIR, read_rows, validate


def build(clean):
    total = sum(r["monto"] for r in clean)
    by_cat, by_month = defaultdict(float), defaultdict(float)
    for r in clean:
        by_cat[r["categoria"]] += r["monto"]
        by_month[r["fecha"].strftime("%Y-%m")] += r["monto"]
    return total, by_cat, by_month


def table(rows):
    return "\n".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in r) + "</tr>" for r in rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv")
    ap.add_argument("-o", "--output", default="reporte.html")
    a = ap.parse_args()
    try:
        header, rows = read_rows(a.csv)
    except FileProblem as e:
        print(f"ERROR: {e}")
        return 2
    errors, warnings, clean = validate(header, rows)
    if errors:
        print("ERROR: el CSV no es válido; ejecute validate_csv.py y corrija primero.")
        for e in errors:
            print(f"  - {e}")
        return 1
    total, by_cat, by_month = build(clean)
    cats = sorted(by_cat.items(), key=lambda x: -x[1])
    top = sorted(clean, key=lambda r: -r["monto"])[:5]
    tpl = (SKILL_DIR / "assets" / "report_template.html").read_text(encoding="utf-8")
    values = {
        "TOTAL": f"{total:,.2f}",
        "COUNT": str(len(clean)),
        "TOP_CATEGORY": cats[0][0],
        "CATEGORY_ROWS": table([(c, f"{m:,.2f}", f"{m / total:.1%}") for c, m in cats]),
        "MONTH_ROWS": table([(m, f"{v:,.2f}") for m, v in sorted(by_month.items())]),
        "TOP_ROWS": table([(r["fecha"], r["descripcion"], r["categoria"], f"{r['monto']:,.2f}") for r in top]),
        "WARNINGS": "".join(f"<li>{html.escape(w)}</li>" for w in warnings) or "<li>Ninguna</li>",
    }
    for k, v in values.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    with open(a.output, "w", encoding="utf-8") as f:
        f.write(tpl)
    for w in warnings:
        print(f"ADVERTENCIA: {w}")
    print(f"Reporte generado: {a.output} | total {total:,.2f} | categoría principal: {cats[0][0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
