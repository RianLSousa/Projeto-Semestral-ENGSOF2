'''
Ideia principal do programa é converter um arquivo em outro.
Então temos que ter o arquivo que será convertido e em que ele será convertido.
'''

from src.pdm.converter import Converter


def test_converter_txt_para_pdf():
    """Deve converter um arquivo .txt para .pdf corretamente."""
    converter = Converter()
    resultado = converter.converter("arquivo.txt", "pdf")

    assert resultado == "arquivo.pdf"
