import pytest

from python_pdm_template.utils import converter_json_para_txt


def test_nome_com_valor():
    """Teste para verificar o comportamento da função converter_json_para_txt quando o nome tem um valor específico."""
    conteudo_json = '{"nome": "Marco"}'
    resultado = converter_json_para_txt(conteudo_json)
    assert resultado == "Marco"


def test_nome_com_espacos():
    """Teste para verificar o comportamento da função converter_json_para_txt quando o nome tem espaços."""
    conteudo_json = '{"nome": "  Marco  "}'
    resultado = converter_json_para_txt(conteudo_json)
    assert resultado == "  Marco  "


def test_nome_com_caracteres_especiais():
    """Teste para verificar o comportamento da função converter_json_para_txt quando o nome tem caracteres especiais."""
    conteudo_json = '{"nome": "M@rc0!"}'
    resultado = converter_json_para_txt(conteudo_json)
    assert resultado == "M@rc0!"
