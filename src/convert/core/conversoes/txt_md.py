"""Converta arquivos TXT para Markdown."""

from pathlib import Path


def txt_para_md(
    entrada: Path,
    saida: Path,
):
    """Converta um arquivo TXT para Markdown."""
    conteudo = entrada.read_text(
        encoding="utf-8"
    )

    saida.write_text(
        conteudo,
        encoding="utf-8"
    )