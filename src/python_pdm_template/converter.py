class Converter:

    def converter(self, nome_arquivo: str, formato_destino: str) -> str:

        nome = nome_arquivo.split(".")[0]

        return f"{nome}.{formato_destino}"