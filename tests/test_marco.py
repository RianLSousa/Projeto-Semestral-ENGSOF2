import pytest

from python_pdm_template.utils import obter_mensagem, somar


def somar(a: int | float, b: int | float):
    """
    Retorna a soma de dois números.

    :param a: Primeiro número.
    :param b: Segundo número.
    :return: A soma de a e b.
    """
    return a + b


def test_somar():
    """Teste simples para a função somar."""
    resultado = somar(2, 3)
    assert resultado == 5


def test_somar_com_floats():
    """Teste para a função somar com números de ponto flutuante."""
    resultado = somar(2.5, 3.5)
    assert resultado == pytest.approx(6)


def test_somar_com_negativos():
    """Teste para a função somar com números negativos."""
    resultado = somar(-2, -3)
    assert resultado == -5


def test_somar_com_mistos():
    """Teste para a função somar com um número inteiro e um número de ponto flutuante."""
    resultado = somar(2, 3.5)
    assert resultado == pytest.approx(5.5)


def test_somar_negativo_com_positivo():
    """Teste para a função somar com um número negativo e um número positivo."""
    resultado = somar(-2, 3)
    assert resultado == 1


def obter_mensagem():
    """
    Retorna uma mensagem de exemplo.

    :return: A mensagem fornecida pelo usuário.
    """
    return input("Digite uma mensagem: ")


def test_obter_mensagem(monkeypatch):  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
    """
    Teste que utiliza monkeypatching para substituir a função input() do Python.

    O objetivo aqui é evitar a necessidade de interação do usuário durante os testes
    automatizados, substituindo a função input() por uma função personalizada que
    retorna uma mensagem pré-definida.
    """

    # Função substituta para o monkeypatch
    def mensagem_alternativa(prompt: str):  # noqa: ARG001
        return "Mensagem modificada"

    # Aplicando o monkeypatch para substituir a função input() do Python por
    # mensagem_alternativa.
    monkeypatch.setattr("builtins.input", mensagem_alternativa)  # pyright: ignore[reportUnknownMemberType]

    # Verificando se a função foi substituída corretamente
    resultado = obter_mensagem()
    assert resultado == "Mensagem modificada"
