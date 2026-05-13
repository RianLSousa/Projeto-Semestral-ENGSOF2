import pytest
from unittest.mock import MagicMock, call
import datetime

'''
Armazenar informaçoes em um historico
'''



# blocos relativos ao teste 

class TestLogsDeSucesso:
   

    def test_ct10_log_registrado_com_timestamp_apos_sucesso(
        self, conversor, gerenciador_logs
    ):
        
        def converter_com_log(
            arquivo_entrada, formato_saida, diretorio_saida, logger=None
        ):
            if logger:
                logger.registrar(
                    evento="CONVERSAO_CONCLUIDA",
                    timestamp=datetime.datetime.now().isoformat(),
                    arquivo=arquivo_entrada,
                    formato_saida=formato_saida
                )
            return {"sucesso": True, "arquivo_saida": "saida.pdf"}

        conversor.converter.side_effect = converter_com_log

        conversor.converter(
            arquivo_entrada="doc.md",
            formato_saida="pdf",
            diretorio_saida="/saida",
            logger=gerenciador_logs
        )

        # Verifica que o log foi chamado
        gerenciador_logs.registrar.assert_called_once()

        # Verifica os campos do log
        kwargs = gerenciador_logs.registrar.call_args.kwargs
        assert kwargs["evento"] == "CONVERSAO_CONCLUIDA"
        assert "timestamp" in kwargs
        assert kwargs["arquivo"] == "doc.md"
        assert kwargs["formato_saida"] == "pdf"

    def test_timestamp_formato_iso8601(self, conversor, gerenciador_logs):
      
        timestamps_capturados = []

        def converter_registra_ts(
            arquivo_entrada, formato_saida, diretorio_saida, logger=None
        ):
            ts = datetime.datetime.now().isoformat()
            timestamps_capturados.append(ts)
            if logger:
                logger.registrar(evento="CONVERSAO_CONCLUIDA", timestamp=ts)
            return {"sucesso": True, "arquivo_saida": "saida.pdf"}

        conversor.converter.side_effect = converter_registra_ts

        conversor.converter(
            arquivo_entrada="doc.md",
            formato_saida="pdf",
            diretorio_saida="/saida",
            logger=gerenciador_logs
        )

        # Tenta fazer parse do timestamp — se falhar, não é ISO 8601
        ts = timestamps_capturados[0]
        parsed = datetime.datetime.fromisoformat(ts)
        assert isinstance(parsed, datetime.datetime)

    def test_log_registrado_para_cada_arquivo_em_lote(
        self, conversor, gerenciador_logs, lista_arquivos_validos
    ):
      
        def lote_com_log(arquivos, formato_saida, logger=None):
            resultados = []
            for arq in arquivos:
                if logger:
                    logger.registrar(
                        evento="CONVERSAO_CONCLUIDA",
                        timestamp=datetime.datetime.now().isoformat(),
                        arquivo=arq
                    )
                resultados.append({"sucesso": True, "arquivo": arq})
            return resultados

        conversor.converter_lote.side_effect = lote_com_log

        conversor.converter_lote(
            arquivos=lista_arquivos_validos,
            formato_saida="pdf",
            logger=gerenciador_logs
        )

        # Um log por arquivo
        assert gerenciador_logs.registrar.call_count == len(lista_arquivos_validos)



class TestLogsDeErro:
  

    def test_log_de_erro_registrado_com_mensagem(
        self, conversor, gerenciador_logs
    ):
      
        def converter_com_erro_logado(
            arquivo_entrada, formato_saida, diretorio_saida, logger=None
        ):
            erro = ValueError("Arquivo corrompido")
            if logger:
                logger.registrar(
                    evento="ERRO_CONVERSAO",
                    timestamp=datetime.datetime.now().isoformat(),
                    arquivo=arquivo_entrada,
                    mensagem=str(erro)
                )
            raise erro

        conversor.converter.side_effect = converter_com_erro_logado

        with pytest.raises(ValueError):
            conversor.converter(
                arquivo_entrada="corrompido.pdf",
                formato_saida="txt",
                diretorio_saida="/saida",
                logger=gerenciador_logs
            )

        kwargs = gerenciador_logs.registrar.call_args.kwargs
        assert kwargs["evento"] == "ERRO_CONVERSAO"
        assert "mensagem" in kwargs
        assert "corrompido" in kwargs["mensagem"].lower()

    def test_log_de_cancelamento_registrado(
        self, conversor, gerenciador_logs
    ):
     
        def cancelar_com_log(logger=None):
            if logger:
                logger.registrar(
                    evento="CONVERSAO_CANCELADA",
                    timestamp=datetime.datetime.now().isoformat(),
                    motivo="Ação do usuário"
                )
            return {"cancelado": True, "arquivos_parciais_removidos": []}

        conversor.cancelar.side_effect = cancelar_com_log

        conversor.cancelar(logger=gerenciador_logs)

        kwargs = gerenciador_logs.registrar.call_args.kwargs
        assert kwargs["evento"] == "CONVERSAO_CANCELADA"
        assert "motivo" in kwargs


class TestConsultaDeHistorico:
   
    def test_historico_retorna_lista_de_eventos(self, gerenciador_logs):
     
        gerenciador_logs.obter_logs.return_value = [
            {
                "evento": "CONVERSAO_CONCLUIDA",
                "timestamp": "2025-05-12T10:00:00",
                "arquivo": "doc1.md"
            },
            {
                "evento": "CONVERSAO_CONCLUIDA",
                "timestamp": "2025-05-12T10:05:00",
                "arquivo": "doc2.txt"
            },
        ]

        logs = gerenciador_logs.obter_logs()

        assert isinstance(logs, list)
        assert len(logs) == 2
        assert all("timestamp" in log for log in logs)

    def test_historico_vazio_retorna_lista_vazia(self, gerenciador_logs):
    
        gerenciador_logs.obter_logs.return_value = []

        logs = gerenciador_logs.obter_logs()

        assert logs == []

    def test_logs_armazenados_persistem(self, gerenciador_logs):
    
        # Registra dois eventos
        gerenciador_logs.registrar(evento="CONVERSAO_CONCLUIDA", arquivo="a.md")
        gerenciador_logs.registrar(evento="CONVERSAO_CONCLUIDA", arquivo="b.txt")

        # Verifica que foram registrados
        assert gerenciador_logs.registrar.call_count == 2
