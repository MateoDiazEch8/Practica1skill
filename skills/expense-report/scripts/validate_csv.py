#!/usr/bin/env python3
"""Valida un CSV de gastos. Exit: 0 válido, 1 errores de contenido, 2 problema de archivo."""
import sys
from common import FileProblem, read_rows, validate


def main():
    if len(sys.argv) != 2:
        print("Uso: validate_csv.py <archivo.csv>", file=sys.stderr)
        return 2
    try:
        header, rows = read_rows(sys.argv[1])
    except FileProblem as e:
        print(f"ERROR: {e}")
        return 2
    errors, warnings, clean = validate(header, rows)
    for w in warnings:
        print(f"ADVERTENCIA: {w}")
    if errors:
        print(f"INVÁLIDO: {len(errors)} error(es)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {len(clean)} gastos válidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
