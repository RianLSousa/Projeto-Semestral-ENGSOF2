import pytest
from unittest.mock import MagicMock


# Bloco de  Conversão arquivo único 

class TestAceitacaoConverterArquivoUnico:

    def test_fluxo_completo_usuario_converte_arquivo_unico_gui(
        self, conversor, gui
    ):
      
        # Simula as ações do usuário na GUI
        arquivo   = gui.obter_arquivo_selecionado()   # clica em "Selecionar arquivo"
        formato   = gui.obter_formato_saida()          # escolhe "pdf"
        diretorio = gui.obter_diretorio_saida()        # escolhe pasta de destino

        # O Core processa
        resultado = conversor.converter(
            arquivo_entrada=arquivo,
            formato_saida=formato,
            diretorio_saida=diretorio
        )

        # GUI exibe resultado
        gui.exibir_mensagem("Conversão concluída!")

        # Critérios de aceitação
        assert resultado["sucesso"] is True
        gui.obter_arquivo_selecionado.assert_called_once()
        gui.exibir_mensagem.assert_called_once_with("Conversão concluída!")

    def test_fluxo_completo_usuario_converte_via_cli(self, cli):
      
        cli.executar.return_value = {
            "codigo_saida": 0,
            "mensagem": "Conversão concluída com sucesso",
            "arquivo_saida": "saida.pdf"
        }

        resultado = cli.executar(
            args=["converter", "documento.md", "--saida", "pdf", "--dir", "/saida"]
        )

        assert resultado["codigo_saida"] == 0
        assert resultado["arquivo_saida"].endswith(".pdf")

    def test_ct15_conversao_via_gui_retorna_resultado_correto(
        self, conversor, gui
    ):
        
        resultado = conversor.converter(
            arquivo_entrada=gui.obter_arquivo_selecionado(),
            formato_saida=gui.obter_formato_saida(),
            diretorio_saida=gui.obter_diretorio_saida()
        )

        assert resultado["sucesso"] is True


# Bloco de cancelamento de conversão 

class TestAceitacaoCancelarConversao:
 
    def test_usuario_cancela_e_recebe_confirmacao(self, conversor, gui):
     
        conversor.cancelar.return_value = {
            "cancelado": True,
            "arquivos_parciais_removidos": ["saida_parcial.pdf"]
        }

        resultado = conversor.cancelar()
        gui.exibir_mensagem("Conversão cancelada pelo usuário")

        assert resultado["cancelado"] is True
        assert len(resultado["arquivos_parciais_removidos"]) > 0
        gui.exibir_mensagem.assert_called_with("Conversão cancelada pelo usuário")


# Bloco BATCH

class TestAceitacaoBatch:
    

    def test_usuario_converte_multiplos_arquivos_com_progresso(
        self, conversor, gui, lista_arquivos_validos
    ):
      
        progresso_exibido = []

        def lote_com_progresso(arquivos, formato_saida, callback_progresso=None):
            for i, arq in enumerate(arquivos):
                pct = int(((i + 1) / len(arquivos)) * 100)
                if callback_progresso:
                    callback_progresso(pct)
            return [{"sucesso": True, "arquivo": arq} for arq in arquivos]

        conversor.converter_lote.side_effect = lote_com_progresso
        callback = lambda p: progresso_exibido.append(p)

        resultados = conversor.converter_lote(
            arquivos=lista_arquivos_validos,
            formato_saida="pdf",
            callback_progresso=callback
        )

        assert len(resultados) == 3
        assert all(r["sucesso"] for r in resultados)
        assert 100 in progresso_exibido  # progresso chegou a 100%


# Bloco validação de arquivos

class TestAceitacaoValidacao:
    def test_arquivo_invalido_exibe_mensagem_amigavel(self, conversor, gui):
     
        conversor.validar_arquivo.return_value = False

        valido = conversor.validar_arquivo("corrompido.pdf")

        if not valido:
            gui.exibir_mensagem("Erro: o arquivo selecionado está corrompido ou inválido.")

        gui.exibir_mensagem.assert_called_with(
            "Erro: o arquivo selecionado está corrompido ou inválido."
        )

    def test_arquivo_valido_prossegue_para_conversao(
        self, conversor, arquivo_md_valido
    ):
  
        conversor.validar_arquivo.return_value = True

        if conversor.validar_arquivo(str(arquivo_md_valido)):
            conversor.converter(
                arquivo_entrada=str(arquivo_md_valido),
                formato_saida="pdf",
                diretorio_saida="/saida"
            )

        conversor.converter.assert_called_once()

# bloco relacionado a sobrescrita 


class TestAceitacaoSobrescrita:


    def test_arquivo_existente_recebe_nome_alternativo(self, conversor, tmp_path):
      
        from pathlib import Path

        existente = tmp_path / "saida.pdf"
        existente.write_bytes(b"arquivo antigo")

        def converter(arquivo_entrada, formato_saida, diretorio_saida, force_overwrite=False):
            saida = Path(diretorio_saida) / "saida.pdf"
            if saida.exists() and not force_overwrite:
                saida = Path(diretorio_saida) / "saida(1).pdf"
            saida.write_bytes(b"arquivo novo")
            return {"sucesso": True, "arquivo_saida": str(saida)}

        conversor.converter.side_effect = converter

        resultado = conversor.converter(
            arquivo_entrada="doc.md",
            formato_saida="pdf",
            diretorio_saida=str(tmp_path)
        )

        assert "saida(1).pdf" in resultado["arquivo_saida"]
        assert existente.read_bytes() == b"arquivo antigo"  # intacto!


# bloco ci/cd


class TestAceitacaoParidadeCLIeGUI:
  

    def test_cli_e_gui_produzem_mesmo_resultado(self, conversor, cli, gui):
      
        # Via GUI
        resultado_gui = conversor.converter(
            arquivo_entrada=gui.obter_arquivo_selecionado(),
            formato_saida=gui.obter_formato_saida(),
            diretorio_saida=gui.obter_diretorio_saida()
        )

        # Via CLI
        resultado_cli = cli.executar(
            args=["converter", "documento.md", "--saida", "pdf", "--dir", "/saida"]
        )

        assert resultado_gui["sucesso"] is True
        assert resultado_cli["codigo_saida"] == 0

    def test_ct14_cli_argumento_invalido_retorna_codigo_erro(self, cli):
      
        cli.executar.return_value = {
            "codigo_saida": 1,
            "mensagem": "Erro: argumento '--formato-errado' não reconhecido"
        }

        resultado = cli.executar(args=["--formato-errado", "arquivo.md"])

        assert resultado["codigo_saida"] == 1
        assert "não reconhecido" in resultado["mensagem"]




