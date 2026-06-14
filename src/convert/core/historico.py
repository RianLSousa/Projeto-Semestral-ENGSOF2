from datetime import datetime


class Historico:

    def __init__(self):
        self.logs = []

    def registrar(self, evento: str, **dados):

        self.logs.append(
            {
                "evento": evento,
                "timestamp": datetime.now().isoformat(),
                **dados
            }
        )

    def obter_logs(self):

        return self.logs