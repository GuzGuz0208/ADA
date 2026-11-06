"""Extrae el texto de PDF y DOCX a .txt (herramienta de lectura para los agentes; no es parte de la solucion).

Uso:  python tools/leer_docs.py <archivo.pdf|archivo.docx> [...] --out <carpeta>
Requiere: pip install -r requirements-dev.txt  (pdfplumber, python-docx).
"""
from __future__ import annotations

import argparse
from pathlib import Path


def pdf_a_texto(ruta: Path) -> str:
    import pdfplumber

    partes = []
    with pdfplumber.open(ruta) as pdf:
        for i, pag in enumerate(pdf.pages, start=1):
            partes.append(f"\n===== pagina {i} =====\n{pag.extract_text() or ''}")
    return "".join(partes)


def docx_a_texto(ruta: Path) -> str:
    import docx

    d = docx.Document(str(ruta))
    lineas = [p.text for p in d.paragraphs]
    for t, tabla in enumerate(d.tables, start=1):
        lineas.append(f"\n===== tabla {t} =====")
        for fila in tabla.rows:
            lineas.append(" | ".join(c.text.strip() for c in fila.cells))
    return "\n".join(lineas)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("archivos", nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for a in map(Path, args.archivos):
        texto = pdf_a_texto(a) if a.suffix.lower() == ".pdf" else docx_a_texto(a)
        destino = out / (a.stem + ".txt")
        destino.write_text(texto, encoding="utf-8")
        print(f"{a} -> {destino} ({len(texto)} caracteres)")


if __name__ == "__main__":
    main()
