"""Gerencie as operações de conversão de arquivos."""

from pathlib import Path

from .validacao import validar_arquivo as _validar_arquivo
from .arquivos import gerar_nome_disponivel
from .progresso import Progresso
from .conversoes.txt_md import txt_para_md
from .conversoes.md_txt import md_para_txt


class Conversor:
    """Gerencie as operações de conversão de arquivos."""

    def __init__(self):
        self.cancelado = False
        self._progresso = Progresso()

    def registrar_progresso(self, callback) -> None:
        """Registra função que recebe atualizações de progresso (0–100)."""
        self._progresso.registrar(callback)

    def validar_arquivo(self, arquivo: str) -> bool:
        """Valida se o arquivo existe, não está vazio e tem formato suportado."""
        return _validar_arquivo(arquivo)

    def converter(
        self,
        arquivo_entrada: str,
        formato_saida: str,
        diretorio_saida: str,
    ) -> dict:
        """Converte um arquivo para o formato desejado."""
        self._progresso.iniciar()
        self._progresso.notificar(0)

        _validar_arquivo(arquivo_entrada)

        entrada = Path(arquivo_entrada)
        Path(diretorio_saida).mkdir(parents=True, exist_ok=True)

        saida = Path(diretorio_saida) / f"{entrada.stem}.{formato_saida}"
        saida = gerar_nome_disponivel(saida)

        self._progresso.notificar(30)

        if entrada.suffix.lower() == ".txt" and formato_saida == "md":
            txt_para_md(entrada, saida)

        elif entrada.suffix.lower() == ".md" and formato_saida == "txt":
            md_para_txt(entrada, saida)

        else:
            raise ValueError("Conversão ainda não implementada.")

        self._progresso.notificar(100)

        return {
            "sucesso": True,
            "arquivo_saida": str(saida),
        }

    def converter_lote(
        self,
        arquivos: list[str],
        formato_saida: str,
        diretorio_saida: str = ".",
        callback_progresso=None,
    ) -> list[dict]:
        """Converte uma lista de arquivos para o mesmo formato."""
        resultados = []
        total = len(arquivos)

        for i, arquivo in enumerate(arquivos):
            if self.cancelado:
                break

            try:
                resultado = self.converter(
                    arquivo_entrada=arquivo,
                    formato_saida=formato_saida,
                    diretorio_saida=diretorio_saida,
                )
                resultados.append({"sucesso": True, "arquivo": arquivo})

            except Exception as e:
                resultados.append({
                    "sucesso": False,
                    "arquivo": arquivo,
                    "erro": str(e),
                })

            if callback_progresso:
                percentual = int(((i + 1) / total) * 100)
                callback_progresso(percentual)

        return resultados

    def cancelar(self, arquivo_em_progresso: str = "") -> dict:
        """Cancela a conversão e remove arquivos parciais."""
        self.cancelado = True
        removidos = []

        if arquivo_em_progresso:
            p = Path(arquivo_em_progresso)
            if p.exists():
                p.unlink()
                removidos.append(arquivo_em_progresso)

        return {
            "cancelado": True,
            "arquivos_parciais_removidos": removidos,
        }