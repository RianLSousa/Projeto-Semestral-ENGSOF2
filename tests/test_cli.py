"""Testes da interface de linha de comando."""

from unittest.mock import Mock, patch

from convert.main import main


def test_cli_sem_argumentos(capsys):
    """Deve exibir mensagem de uso quando faltam argumentos."""

    with patch(
        "sys.argv",
        ["convert"]
    ):
        main()

    saida = capsys.readouterr()

    assert "Uso:" in saida.out


def test_cli_chama_conversor():
    """Deve chamar o método converter com os argumentos informados."""

    conversor_mock = Mock()

    conversor_mock.converter.return_value = {
        "sucesso": True
    }

    with (
        patch(
            "convert.main.Conversor",
            return_value=conversor_mock
        ),
        patch(
            "sys.argv",
            [
                "convert",
                "arquivo.txt",
                "md",
                "saida",
            ]
        ),
    ):
        main()

    conversor_mock.converter.assert_called_once_with(
        "arquivo.txt",
        "md",
        "saida",
    )


def test_cli_exibe_erro(capsys):
    """Deve exibir mensagem amigável quando ocorre erro."""

    with (
        patch(
            "convert.main.Conversor"
        ) as mock_conversor,
        patch(
            "sys.argv",
            [
                "convert",
                "arquivo.txt",
                "md",
                "saida",
            ]
        ),
    ):

        mock_conversor.return_value.converter.side_effect = (
            FileNotFoundError(
                "Arquivo não encontrado"
            )
        )

        main()

    saida = capsys.readouterr()

    assert "Erro:" in saida.out
