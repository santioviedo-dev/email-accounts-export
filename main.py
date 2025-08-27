#!/usr/bin/env python3
import json
import csv
import argparse
from pathlib import Path
import sys

def collect_users(data):
    """Devuelve lista de dicts por usuario con todos sus campos + email/username/domain."""
    rows = []
    for domain, info in (data or {}).items():
        accounts = (info or {}).get("accounts", {})
        for username, meta in accounts.items():
            row = {}
            row["username"] = username
            row["domain"] = domain
            row["email"] = f"{username}@{domain}"
            if isinstance(meta, dict):
                for k, v in meta.items():
                    row[k] = v
            else:
                # Por si algún item fuera solo un string u otro tipo
                row["value"] = meta
            rows.append(row)
    return rows

def main():
    ap = argparse.ArgumentParser(
        description="Exportar todas las cuentas y todos los campos a CSV."
    )
    ap.add_argument("-i", "--input", default="email_accounts.json",
                    help="Ruta al JSON de cuentas (por defecto: email_accounts.json)")
    ap.add_argument("-o", "--output", default="cuentas_todas.csv",
                    help="Ruta de salida CSV (por defecto: cuentas_todas.csv)")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.stderr.write(f"Error: no existe {src}\n")
        sys.exit(1)

    with src.open("r", encoding="utf-8") as f:
        data = json.load(f)

    rows = collect_users(data)
    if not rows:
        sys.stderr.write("No se encontraron cuentas.\n")
        sys.exit(2)

    # Construir encabezados: email, username, domain primero; luego el resto ordenado.
    fixed = ["email", "username", "domain"]
    dynamic = sorted({k for r in rows for k in r.keys()} - set(fixed))
    headers = fixed + dynamic

    outp = Path(args.output)
    with outp.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            # Normalizar valores complejos a string
            clean = {k: ("" if v is None else (v if isinstance(v, (str, int, float, bool)) else json.dumps(v, ensure_ascii=False)))
                     for k, v in r.items()}
            writer.writerow(clean)

    print(f"Exportadas {len(rows)} cuentas a {outp} con {len(headers)} columnas.")

if __name__ == "__main__":
    main()
