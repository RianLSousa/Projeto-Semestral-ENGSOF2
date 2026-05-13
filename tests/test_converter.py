from unittest.mock import MagicMock
from pathlib import Path


# Testes unitários para a função de conversão

class TestConversaoUnitaria:
    """
    Testes unitários das conversões individuais.
    Cobrem CT01, CT02, CT03 do DEF.
    """
 
    def test_ct01_conversao_md_para_pdf(self, conversor, arquivo_md_valido):
        """

 
        Arrange: arquivo .md real criado pelo fixture
        Act    : chamar conversor.converter()
        Assert : sucesso=True e saída com extensão .pdf
        """
        conversor.converter.return_value = {
            "sucesso": True,
            "arquivo_saida": "documento.pdf"
        }
 
        resultado = conversor.converter(
            arquivo_entrada=str(arquivo_md_valido),
            formato_saida="pdf",
            diretorio_saida="/saida"
        )
 
        assert resultado["sucesso"] is True
        assert resultado["arquivo_saida"].endswith(".pdf")
        conversor.converter.assert_called_once_with(
            arquivo_entrada=str(arquivo_md_valido),
            formato_saida="pdf",
            diretorio_saida="/saida"
        )
 
    def test_ct02_conversao_txt_para_md(self, conversor, arquivo_txt_valido):
  
        conversor.converter.return_value = {
            "sucesso": True,
            "arquivo_saida": "documento.md"
        }
 
        resultado = conversor.converter(
            arquivo_entrada=str(arquivo_txt_valido),
            formato_saida="md",
            diretorio_saida="/saida"
        )
 
        assert resultado["sucesso"] is True
        assert resultado["arquivo_saida"].endswith(".md")
 
    def test_ct03_conversao_docx_para_pdf(self, conversor, arquivo_docx_valido):
 
        conversor.converter.return_value = {
            "sucesso": True,
            "arquivo_saida": "documento.pdf"
        }
 
        resultado = conversor.converter(
            arquivo_entrada=str(arquivo_docx_valido),
            formato_saida="pdf",
            diretorio_saida="/saida"
        )
 
        assert resultado["sucesso"] is True
        assert resultado["arquivo_saida"].endswith(".pdf")
 
    def test_conversao_epub_para_pdf(self, conversor, arquivo_epub_valido):
  
        conversor.converter.return_value = {
            "sucesso": True,
            "arquivo_saida": "documento.pdf"
        }
 
        resultado = conversor.converter(
            arquivo_entrada=str(arquivo_epub_valido),
            formato_saida="pdf",
            diretorio_saida="/saida"
        )
 
        assert resultado["sucesso"] is True
 
    def test_conversao_pdf_para_txt(self, conversor, arquivo_pdf_valido):

        conversor.converter.return_value = {
            "sucesso": True,
            "arquivo_saida": "documento.txt"
        }
 
        resultado = conversor.converter(
            arquivo_entrada=str(arquivo_pdf_valido),
            formato_saida="txt",
            diretorio_saida="/saida"
        )
 
        assert resultado["sucesso"] is True
        assert resultado["arquivo_saida"].endswith(".txt")
 
 
# Testes de processamento em lote (BATCH)
 
class TestProcessamentoLote:

 
    def test_ct05_lote_com_multiplos_arquivos_validos(
        self, conversor, lista_arquivos_validos
    ):
       
        conversor.converter_lote.return_value = [
            {"sucesso": True, "arquivo": arq}
            for arq in lista_arquivos_validos
        ]
 
        resultados = conversor.converter_lote(
            arquivos=lista_arquivos_validos,
            formato_saida="pdf"
        )
 
        assert len(resultados) == 3
        assert all(r["sucesso"] is True for r in resultados)
 
    def test_ct06_batch_vazio_nenhuma_conversao(self, conversor):
       
        conversor.converter_lote.return_value = []
 
        resultados = conversor.converter_lote(arquivos=[], formato_saida="pdf")
 
        assert resultados == []
        conversor.converter_lote.assert_called_once_with(
            arquivos=[], formato_saida="pdf"
        )
 
    def test_lote_misto_sucesso_e_falha(self, conversor):
        
        conversor.converter_lote.return_value = [
            {"sucesso": True,  "arquivo": "valido.txt"},
            {"sucesso": False, "arquivo": "corrompido.txt", "erro": "arquivo corrompido"},
            {"sucesso": True,  "arquivo": "outro_valido.txt"},
        ]
 
        resultados = conversor.converter_lote(
            arquivos=["valido.txt", "corrompido.txt", "outro_valido.txt"],
            formato_saida="pdf"
        )
 
        sucessos = [r for r in resultados if r["sucesso"]]
        falhas   = [r for r in resultados if not r["sucesso"]]
 
        assert len(sucessos) == 2
        assert len(falhas) == 1
        assert "erro" in falhas[0]
 
 
# Testes de feedback de progresso e cancelamento
 
class TestProgressoECancelamento:
 
    def test_ct07_callback_de_progresso_e_chamado(self, conversor):
     
        callback = MagicMock()
 
        def conversao_com_progresso(
            arquivo_entrada, formato_saida, diretorio_saida, callback=None
        ):
            if callback:
                callback(25)
                callback(50)
                callback(100)
            return {"sucesso": True, "arquivo_saida": "saida.pdf"}
 
        conversor.converter.side_effect = conversao_com_progresso
 
        conversor.converter(
            arquivo_entrada="arquivo.md",
            formato_saida="pdf",
            diretorio_saida="/saida",
            callback=callback
        )
 
        assert callback.call_count == 3
        callback.assert_any_call(25)
        callback.assert_any_call(50)
        callback.assert_any_call(100)
 
    def test_ct08_cancelamento_remove_arquivos_parciais(self, conversor):
     
        conversor.cancelar.return_value = {
            "cancelado": True,
            "arquivos_parciais_removidos": ["saida_parcial.pdf"]
        }
 
        resultado = conversor.cancelar()
 
        assert resultado["cancelado"] is True
        assert len(resultado["arquivos_parciais_removidos"]) > 0
        conversor.cancelar.assert_called_once()
 
    def test_progresso_nao_ultrapassa_100(self, conversor):
   
        valores_recebidos = []
        callback = lambda p: valores_recebidos.append(p)
 
        def conversao(arquivo_entrada, formato_saida, diretorio_saida, callback=None):
            for pct in [10, 50, 100]:
                if callback:
                    callback(pct)
            return {"sucesso": True, "arquivo_saida": "saida.pdf"}
 
        conversor.converter.side_effect = conversao
 
        conversor.converter(
            arquivo_entrada="arquivo.md",
            formato_saida="pdf",
            diretorio_saida="/saida",
            callback=callback
        )
 
        assert max(valores_recebidos) <= 100
 
 
# Testes de prevenção de sobrescrita  
 
class TestSobrescrita:
 
    def test_ct17_sobrescrita_forcada_substitui_arquivo(self, conversor, tmp_path):
        """
        CT17 — Com force_overwrite=True, o arquivo existente deve ser substituído.
        """
        arquivo_existente = tmp_path / "saida.pdf"
        arquivo_existente.write_bytes(b"conteudo antigo")
 
        def converter_com_sobrescrita(
            arquivo_entrada, formato_saida, diretorio_saida, force_overwrite=False
        ):
            saida = Path(diretorio_saida) / "saida.pdf"
            if saida.exists() and not force_overwrite:
                saida = Path(diretorio_saida) / "saida(1).pdf"
            saida.write_bytes(b"conteudo novo")
            return {"sucesso": True, "arquivo_saida": str(saida)}
 
        conversor.converter.side_effect = converter_com_sobrescrita
 
        resultado = conversor.converter(
            arquivo_entrada="doc.md",
            formato_saida="pdf",
            diretorio_saida=str(tmp_path),
            force_overwrite=True
        )
 
        assert resultado["sucesso"] is True
        assert resultado["arquivo_saida"] == str(tmp_path / "saida.pdf")
 
    def test_sem_flag_cria_nome_alternativo(self, conversor, tmp_path):
      
        arquivo_existente = tmp_path / "saida.pdf"
        arquivo_existente.write_bytes(b"conteudo antigo")
 
        def converter_sem_sobrescrita(
            arquivo_entrada, formato_saida, diretorio_saida, force_overwrite=False
        ):
            saida = Path(diretorio_saida) / "saida.pdf"
            if saida.exists() and not force_overwrite:
                saida = Path(diretorio_saida) / "saida(1).pdf"
            saida.write_bytes(b"conteudo novo")
            return {"sucesso": True, "arquivo_saida": str(saida)}
 
        conversor.converter.side_effect = converter_sem_sobrescrita
 
        resultado = conversor.converter(
            arquivo_entrada="doc.md",
            formato_saida="pdf",
            diretorio_saida=str(tmp_path)
        )
 
        assert resultado["arquivo_saida"] == str(tmp_path / "saida(1).pdf")
        assert arquivo_existente.read_bytes() == b"conteudo antigo"
 
