#!/usr/bin/env python3
"""Pruebas de extremo a extremo: caso exitoso y casos de error."""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "skills" / "expense-report"
V, G = str(S / "scripts" / "validate_csv.py"), str(S / "scripts" / "generate_report.py")
A = S / "assets"


def run(*args):
    p = subprocess.run([sys.executable, *args], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout


def check(name, cond):
    print(("PASS" if cond else "FAIL"), name)
    return cond


with tempfile.TemporaryDirectory() as t:
    out = Path(t) / "r.html"
    empty = Path(t) / "empty.csv"
    empty.write_text("")
    nocol = Path(t) / "nocol.csv"
    nocol.write_text("fecha,monto\n2026-01-01,5\n")
    bad = run(V, str(A / "sample_invalid.csv"))
    ok_gen = run(G, str(A / "sample_expenses.csv"), "-o", str(out))
    html = out.read_text(encoding="utf-8") if out.exists() else ""
    results = [
        check("válido -> exit 0", run(V, str(A / "sample_expenses.csv"))[0] == 0),
        check("inválido -> exit 1 con filas", bad[0] == 1 and "Fila 3" in bad[1] and "Fila 5" in bad[1]),
        check("inexistente -> exit 2", run(V, "nope.csv")[0] == 2),
        check("vacío -> exit 2", run(V, str(empty))[0] == 2),
        check("faltan columnas -> exit 1", (lambda r: r[0] == 1 and "Faltan columnas" in r[1])(run(V, str(nocol)))),
        check("reporte válido -> exit 0", ok_gen[0] == 0),
        check("HTML con total y sin placeholders", "1,010.50" in html and "{{" not in html),
        check("reporte con CSV inválido se niega", run(G, str(A / "sample_invalid.csv"), "-o", str(Path(t) / "x.html"))[0] == 1),
    ]
sys.exit(0 if all(results) else 1)
