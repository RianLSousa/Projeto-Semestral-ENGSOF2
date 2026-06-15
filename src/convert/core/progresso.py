"""Sistema de eventos de progresso do Convert+."""

import time
from typing import Callable


class Progresso:
    """
    Gerencia quem recebe atualizações durante a conversão.

    Como usar:
        p = Progresso()
        p.registrar(lambda v: print(f"{v}%"))
        p.iniciar()
        p.notificar(50)   # imprime "50%"
        p.notificar(100)  # imprime "100%"
        print(p.tempo_decorrido())  # segundos desde iniciar()
    """

    def __init__(self) -> None:
        """Inicializa com lista vazia de observers."""
        self._callbacks: list[Callable[[int], None]] = []
        self._inicio: float = 0.0

    def registrar(self, callback: Callable[[int], None]) -> None:
        """
        Registra uma função para receber atualizações de progresso.

        Args:
            callback: função que recebe um inteiro de 0 a 100.
                      Exemplo: lambda p: print(f"{p}%")
        """
        self._callbacks.append(callback)

    def iniciar(self) -> None:
        """Marca o momento de início (para calcular tempo decorrido)."""
        self._inicio = time.time()

    def notificar(self, percentual: int) -> None:
        """
        Avisa todos os registrados com o percentual atual.

        Se um callback falhar, os outros continuam sendo notificados.
        O Core não para por causa de erro em observer.

        Args:
            percentual: valor entre 0 e 100.
        """
        # Garante que o valor está dentro do intervalo válido
        valor = max(0, min(100, percentual))

        for callback in self._callbacks:
            try:
                callback(valor)
            except Exception:
                pass  # observer com erro não para a conversão

    def tempo_decorrido(self) -> float:
        """Retorna quantos segundos se passaram desde iniciar()."""
        if self._inicio == 0.0:
            return 0.0
        return time.time() - self._inicio