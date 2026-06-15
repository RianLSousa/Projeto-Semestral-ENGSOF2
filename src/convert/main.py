"""Módulo principal da aplicação de conversão de arquivos."""
import sys
from convert.core.conversor import Conversor

NUMERO_DE_ARGUMENTOS = 4

def main():
    """Ponto de entrada da aplicação."""
    if len(sys.argv) != NUMERO_DE_ARGUMENTOS:
        print("Uso: python -m convert <arquivo> <formato> <saida>")
        return

    arquivo = sys.argv[1]
    formato = sys.argv[2]
    saida = sys.argv[3]

    try:
        conversor = Conversor()
        resultado = conversor.converter(
            arquivo,
            formato,
            saida
        )
        print(resultado)

    except Exception as erro:
        print(f"Erro: {erro}")