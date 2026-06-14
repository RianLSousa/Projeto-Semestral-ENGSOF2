from pathlib import Path

from .validacao import validar_arquivo
from .arquivos import gerar_nome_disponivel

from .conversoes.txt_md import txt_para_md
from .conversoes.md_txt import md_para_txt


class Conversor:

    def __init__(self):
        self.cancelado = False

    def converter(
        self,
        arquivo_entrada: str,
        formato_saida: str,
        diretorio_saida: str,
    ) -> dict:

        validar_arquivo(
            arquivo_entrada
        )

        entrada = Path(
            arquivo_entrada
        )

        Path(
            diretorio_saida
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        saida = (
            Path(diretorio_saida)
            / f"{entrada.stem}.{formato_saida}"
        )

        saida = gerar_nome_disponivel(
            saida
        )

        if (
            entrada.suffix.lower() == ".txt"
            and formato_saida == "md"
        ):

            txt_para_md(
                entrada,
                saida
            )

        elif (
            entrada.suffix.lower() == ".md"
            and formato_saida == "txt"
        ):

            md_para_txt(
                entrada,
                saida
            )

        else:

            raise ValueError(
                "Conversão ainda não implementada."
            )

        return {
            "sucesso": True,
            "arquivo_saida": str(saida)
        }

    def cancelar(self):

        self.cancelado = True

        return {
            "cancelado": True,
            "arquivos_parciais_removidos": []
        }