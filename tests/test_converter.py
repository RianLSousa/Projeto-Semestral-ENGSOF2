'''
Ideia principal do programa é converter um arquivo em outro.
Então temos que ter o arquivo que será convertido e em que ele será convertido.
'''


def test_converter():
    from converter import Converter

    converter = Converter()
    converter.convert('test.txt', 'test.csv')
