"""Testes da interface de linha de comando."""

import pytest
from unittest.mock import Mock, patch

from convert.cli.main import main


def test_cli_sem_argumentos(capsys):
    """Deve exibir mensagem de uso quando faltam argumentos."""

    with patch(
        "sys.argv",
        ["convert"]
    ):
        with pytest.raises(SystemExit):
            main()

    saida = capsys.readouterr()

    # No Typer, a mensagem padrão de ajuda é exibida se nenhum comando é passado
    assert "Usage:" in saida.out or "Usage:" in saida.err or "converter" in saida.out or "converter" in saida.err


def test_cli_chama_conversor():
    """Deve chamar o método converter com os argumentos informados."""

    conversor_mock = Mock()

    conversor_mock.converter.return_value = {
        "sucesso": True,
        "arquivo_saida": "saida"
    }

    with (
        patch(
            "convert.cli.main.Conversor",
            return_value=conversor_mock
        ),
        patch(
            "sys.argv",
            [
                "convert",
                "converter",
                "arquivo.txt",
                "--formato",
                "md",
                "--saida",
                "saida",
            ]
        ),
    ):
        with pytest.raises(SystemExit):
            main()

    conversor_mock.converter.assert_called_once_with(
        arquivo_entrada="arquivo.txt",
        formato_saida="md",
        diretorio_saida="saida",
    )


def test_cli_exibe_erro(capsys):
    """Deve exibir mensagem amigável quando ocorre erro."""

    with (
        patch(
            "convert.cli.main.Conversor"
        ) as mock_conversor,
        patch(
            "sys.argv",
            [
                "convert",
                "converter",
                "arquivo.txt",
                "--formato",
                "md",
                "--saida",
                "saida",
            ]
        ),
    ):

        mock_conversor.return_value.converter.side_effect = (
            FileNotFoundError(
                "Arquivo não encontrado"
            )
        )

        with pytest.raises(SystemExit) as excinfo:
            main()

        assert excinfo.value.code == 2

    saida = capsys.readouterr()

    assert "Arquivo não encontrado" in saida.out
