import pytest

from src.python_pdm_template.converter import Converter

def test_arquivo_sem_extensao():
    converter = Converter()

    with pytest.raises(ValueError):
        converter.converter("arquivo", "pdf")