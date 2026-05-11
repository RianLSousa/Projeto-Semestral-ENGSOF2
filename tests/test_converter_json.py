import pytest

from python_pdm_template.utils import converter_json_para_txt


def test_json_vazio():
    with pytest.raises(ValueError, match="JSON vazio"):
        converter_json_para_txt("")


def test_nome_vazio():
    with pytest.raises(ValueError, match="Campo 'nome' inválido"):
        converter_json_para_txt('{"nome": ""}')


def test_nome_com_valor():
    resultado = converter_json_para_txt('{"nome": "Marco"}')
    assert resultado == "Marco"
