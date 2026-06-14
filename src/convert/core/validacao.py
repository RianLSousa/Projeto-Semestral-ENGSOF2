"""Valide arquivos para conversão."""

from pathlib import Path

EXTENSOES_SUPORTADAS = {
    ".txt",
    ".md",
    ".pdf",
    ".docx",
    ".epub"
}


def validar_arquivo(arquivo: str):
    """Valida se o arquivo existe, não está vazio e possui extensão suportada."""
    caminho = Path(arquivo)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo}"
        )

    if caminho.stat().st_size == 0:
        raise ValueError(
            "Arquivo está vazio e não pode ser convertido"
        )

    if caminho.suffix.lower() not in EXTENSOES_SUPORTADAS:
        raise ValueError(
            f"Formato {caminho.suffix} não suportado"
        )

    return True