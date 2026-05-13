"""
Arquivo de configuração do pytest para o pacote de testes.

Este arquivo pode ser usado para:
- Definir fixtures globais para os testes.
- Configurar hooks do pytest.
- Adicionar opções de linha de comando personalizadas.
- Realizar configurações iniciais antes da execução dos testes.

Para mais informações, consulte a documentação do pytest: https://docs.pytest.org/
"""

# Exemplo de fixture global
import pytest
from unittest.mock import MagicMock
from pathlib import Path
 
 

# Mock para o core da conversão 

@pytest.fixture
def conversor():
    mock = MagicMock()
    mock.converter.return_value = {
        "sucesso": True,
        "arquivo_saida": "saida.pdf"
    }
    mock.validar_arquivo.return_value = True
    mock.converter_lote.return_value = [
        {"sucesso": True, "arquivo": f"arquivo_{i}.pdf"} for i in range(3)
    ]
    mock.cancelar.return_value = {
        "cancelado": True,
        "arquivos_parciais_removidos": ["saida_parcial.pdf"]
    }
    return mock
 
 
# ------------------------------------------------------------------
# MOCK DO GERENCIADOR DE LOGS
# ------------------------------------------------------------------
@pytest.fixture
def gerenciador_logs():

    mock = MagicMock()
    mock.registrar.return_value = None
    mock.obter_logs.return_value = []
    return mock
 
 
# ------------------------------------------------------------------
# MOCK DA INTERFACE CLI
# ------------------------------------------------------------------
@pytest.fixture
def cli():
    mock = MagicMock()
    mock.executar.return_value = {
        "codigo_saida": 0,
        "mensagem": "Conversão concluída com sucesso",
        "arquivo_saida": "saida.pdf"
    }
    return mock
 
 

# Mock gui 

@pytest.fixture
def gui():
    """Mock da Interface Gráfica do Usuário."""
    mock = MagicMock()
    mock.obter_arquivo_selecionado.return_value = "documento.md"
    mock.obter_formato_saida.return_value = "pdf"
    mock.obter_diretorio_saida.return_value = "/saida"
    mock.exibir_progresso.return_value = None
    mock.exibir_mensagem.return_value = None
    return mock
 
 
# Arquiv temporários
@pytest.fixture
def arquivo_md_valido(tmp_path):
    f = tmp_path / "documento.md"
    f.write_text("# Título\n\nConteúdo markdown válido.")
    return f
 
 
@pytest.fixture
def arquivo_txt_valido(tmp_path):
    f = tmp_path / "documento.txt"
    f.write_text("Conteúdo de texto simples.")
    return f
 
 
@pytest.fixture
def arquivo_docx_valido(tmp_path):
    f = tmp_path / "documento.docx"
    f.write_bytes(b"PK\x03\x04 fake docx content")  # magic bytes de ZIP
    return f
 
 
@pytest.fixture
def arquivo_epub_valido(tmp_path):
    f = tmp_path / "documento.epub"
    f.write_bytes(b"PK\x03\x04 fake epub content")
    return f
 
 
@pytest.fixture
def arquivo_pdf_valido(tmp_path):
    f = tmp_path / "documento.pdf"
    f.write_bytes(b"%PDF-1.4 fake content")
    return f
 
 
@pytest.fixture
def arquivo_vazio(tmp_path):
    f = tmp_path / "vazio.txt"
    f.write_text("")
    return f
 
 
@pytest.fixture
def arquivo_formato_invalido(tmp_path):
    f = tmp_path / "video.avi"
    f.write_bytes(b"fake avi content")
    return f
 
 
@pytest.fixture
def lista_arquivos_validos(tmp_path):
    arquivos = []
    for i in range(3):
        f = tmp_path / f"arquivo_{i}.txt"
        f.write_text(f"Conteúdo do arquivo {i}")
        arquivos.append(str(f))
    return arquivos
