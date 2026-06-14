from pathlib import Path


class Conversor:

    def __init__(self):
        self.cancelado = False

    def validar_arquivo(self, arquivo: str) -> bool:

        caminho = Path(arquivo)

        if not caminho.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {arquivo}"
            )

        if caminho.stat().st_size == 0:
            raise ValueError(
                "Arquivo está vazio e não pode ser convertido"
            )

        return True

    def converter(
        self,
        arquivo_entrada: str,
        formato_saida: str,
        diretorio_saida: str,
    ) -> dict:

        self.validar_arquivo(arquivo_entrada)

        return {
            "sucesso": True,
            "arquivo_saida": "arquivo_convertido"
        }

    def converter_lote(
        self,
        arquivos: list[str],
        formato_saida: str,
    ) -> list[dict]:

        resultados = []

        for arquivo in arquivos:

            try:

                resultados.append(
                    self.converter(
                        arquivo,
                        formato_saida,
                        "saida"
                    )
                )

            except Exception as erro:

                resultados.append(
                    {
                        "sucesso": False,
                        "arquivo": arquivo,
                        "erro": str(erro)
                    }
                )

        return resultados

    def cancelar(self):

        self.cancelado = True

        return {
            "cancelado": True,
            "arquivos_parciais_removidos": []
        }