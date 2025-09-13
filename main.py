#!/usr/bin/env python3
import json
import csv
import argparse
from pathlib import Path
import sys

def collect_emails(data):
    emails = []
    for domain, info in (data or {}).items():
        if not isinstance(info, dict):
            continue
        accounts = info.get("accounts", {})
        for username in accounts.keys():
            emails.append(f"{username}@{domain}")
    return emails

def main():
    ap = argparse.ArgumentParser(description="Exportar solo las cuentas de email a un CSV (una por línea).")
    ap.add_argument("-i", "--input", default="email_accounts.json", help="Ruta al JSON (por defecto: email_accounts.json)")
    ap.add_argument("-o", "--output", default="cuentas_emails.csv", help="Ruta CSV de salida (por defecto: cuentas_emails.csv)")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        sys.stderr.write(f"Error: no existe {src}\n")
        sys.exit(1)

    with src.open("r", encoding="utf-8") as f:
        data = json.load(f)

    emails = collect_emails(data)
    if not emails:
        sys.stderr.write("No se encontraron cuentas.\n")
        sys.exit(2)

    outp = Path(args.output)
    with outp.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for email in emails:
            writer.writerow([email])

    print(f"Exportadas {len(emails)} cuentas a {outp}.")

if __name__ == "__main__":
    main()
