import pytest
from src.python_pdm_template.converter import Converter


def test_nome_arquivo_vazio():

    converter = Converter()

    with pytest.raises(ValueError):
        converter.converter("", "pdf")
