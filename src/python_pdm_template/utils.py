"""
Módulo com funções utilitárias do projeto.
"""
import json

"""
Este módulo contém funções utilitárias para o projeto.

Funções:
- somar: Retorna a soma de dois números.
- obter_mensagem: Retorna uma mensagem fornecida pelo usuário.
"""


def somar(a: int | float, b: int | float):
    """
    Retorna a soma de dois números.

    :param a: Primeiro número.
    :param b: Segundo número.
    :return: A soma de a e b.
    """
    return a + b


def converter_json_para_txt(conteudo_json: str) -> str:
    """
    Converte um conteúdo JSON para texto retornando o valor do campo "nome".
    """
    if not conteudo_json.strip():
        raise ValueError("JSON vazio.")

    dados: dict[str, object] = json.loads(conteudo_json)

    nome = dados.get("nome")

    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("Campo 'nome' inválido.")

    return nome


def obter_mensagem():
    """
    Retorna uma mensagem de exemplo.

    :return: A mensagem fornecida pelo usuário.
    """
    return input("Digite uma mensagem: ")
