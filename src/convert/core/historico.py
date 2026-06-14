"""Armazena e consulta eventos do sistema."""

from datetime import datetime


class Historico:
    """Armazene e consulte eventos do sistema."""

    def __init__(self):
        """Inicialize a lista de logs."""
        self.logs = []

    def registrar(self, evento: str, **dados):
        """Registre um evento no histórico."""
        self.logs.append(
            {
                "evento": evento,
                "timestamp": datetime.now().isoformat(),
                **dados,
            }
        )

    def obter_logs(self):
        """Retorne todos os eventos registrados."""
        return self.logs