from convert.core.conversor import Conversor
import sys


def main():
    """Ponto de entrada da aplicação."""

    if len(sys.argv) != 4:
        print(
            "Uso: python -m convert "
            "<arquivo> <formato> <saida>"
        )
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


if __name__ == "__main__":
    main()