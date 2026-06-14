from pathlib import Path


def md_para_txt(
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