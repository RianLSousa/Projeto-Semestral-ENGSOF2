from pathlib import Path


def txt_para_md(
    entrada: Path,
    saida: Path
):

    conteudo = entrada.read_text(
        encoding="utf-8"
    )

    saida.write_text(
        conteudo,
        encoding="utf-8"
    )