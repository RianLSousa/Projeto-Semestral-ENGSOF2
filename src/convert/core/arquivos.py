from pathlib import Path


def gerar_nome_disponivel(
    caminho_saida: Path
) -> Path:

    if not caminho_saida.exists():
        return caminho_saida

    contador = 1

    while True:

        novo_nome = (
            caminho_saida.parent
            / f"{caminho_saida.stem}({contador}){caminho_saida.suffix}"
        )

        if not novo_nome.exists():
            return novo_nome

        contador += 1