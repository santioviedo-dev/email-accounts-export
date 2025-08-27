#!/usr/bin/env python3
import json
import csv
import argparse
from pathlib import Path
import sys

def main():
    ap = argparse.ArgumentParser(
        description="Exportar cuentas de ugd.edu.ar desde un JSON a CSV."
    )
    ap.add_argument(
        "-i", "--input",
        default="email_accounts.json",
        help="Ruta al JSON de cuentas (por defecto: email_accounts.json)"
    )
    ap.add_argument(
        "-o", "--output",
        default="ugd_usuarios.csv",
        help="Ruta de salida CSV (por defecto: ugd_usuarios.csv)"
    )
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.stderr.write(f"Error: no existe {src}\n")
        sys.exit(1)

    with src.open("r", encoding="utf-8") as f:
        data = json.load(f)

    emails = []
    for domain, info in data.items():
        if "accounts" not in info:
            continue
        for user in info["accounts"].keys():
            emails.append(f"{user}@{domain}")
    emails = sorted(emails)

    outp = Path(args.output)
    with outp.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["email"])
        for e in emails:
            writer.writerow([e])

    print(f"Exportadas {len(emails)} cuentas a {outp}")

if __name__ == "__main__":
    main()
