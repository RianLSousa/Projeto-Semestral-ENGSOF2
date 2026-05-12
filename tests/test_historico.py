'''
Armazenar informaçoes em um historico
'''


def test_historico():
    from historico import Historico

    historico = Historico()
    historico.add('test.txt', 'test.csv')
    assert historico.get() == [('test.txt', 'test.csv')]
