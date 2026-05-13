"""
Arquivos de teste precisam ser nomeados com o prefixo `test_` ou sufixo `_test`.

O pytest só reconhece automaticamente arquivos com esses nomes.

Este arquivo contém exemplos de testes utilizando pytest, incluindo:
- Um teste simples para validar uma função.
- Um teste que utiliza o recurso de monkeypatching do pytest para modificar 
comportamentos durante o teste.

O objetivo é demonstrar como usar o pytest e seus recursos para criar testes eficazes.
"""

import pytest
from unittest.mock import MagicMock
from pathlib import Path



class TestValidacaoDeArquivos:

    def test_arquivo_valido_passa_na_validacao(self, conversor, arquivo_md_valido):
       
        conversor.validar_arquivo.return_value = True

        valido = conversor.validar_arquivo(str(arquivo_md_valido))

        assert valido is True
        conversor.validar_arquivo.assert_called_once_with(str(arquivo_md_valido))

    def test_ct11_arquivo_vazio_lanca_value_error(self, conversor, arquivo_vazio):
      
        conversor.converter.side_effect = ValueError(
            "Arquivo está vazio e não pode ser convertido"
        )

        with pytest.raises(ValueError, match="Arquivo está vazio"):
            conversor.converter(
                arquivo_entrada=str(arquivo_vazio),
                formato_saida="pdf",
                diretorio_saida="/saida"
            )

    def test_arquivo_corrompido_nao_inicia_conversao(self, conversor, tmp_path):
      
        arquivo_corrompido = tmp_path / "corrompido.pdf"
        arquivo_corrompido.write_bytes(b"\x00\xFF\xFE dados invalidos")

        conversor.validar_arquivo.return_value = False
        conversor.converter.side_effect = ValueError("Arquivo corrompido ou inválido")

        valido = conversor.validar_arquivo(str(arquivo_corrompido))
        assert valido is False

        with pytest.raises(ValueError, match="corrompido"):
            conversor.converter(
                arquivo_entrada=str(arquivo_corrompido),
                formato_saida="pdf",
                diretorio_saida="/saida"
            )

    def test_arquivo_inexistente_lanca_file_not_found(self, conversor):
      
        conversor.converter.side_effect = FileNotFoundError(
            "Arquivo não encontrado: /caminho/que/nao/existe.md"
        )

        with pytest.raises(FileNotFoundError):
            conversor.converter(
                arquivo_entrada="/caminho/que/nao/existe.md",
                formato_saida="pdf",
                diretorio_saida="/saida"
            )



class TestFormatosNaoSuportados:
 

    def test_ct12_formato_avi_nao_suportado(self, conversor, arquivo_formato_invalido):
        
        conversor.converter.side_effect = ValueError(
            "Formato .avi não é suportado pelo Convert+"
        )

        with pytest.raises(ValueError, match="não é suportado"):
            conversor.converter(
                arquivo_entrada=str(arquivo_formato_invalido),
                formato_saida="pdf",
                diretorio_saida="/saida"
            )

    def test_ct04_formato_odt_nao_suportado(self, conversor, tmp_path):
     
        arquivo_odt = tmp_path / "documento.odt"
        arquivo_odt.write_bytes(b"fake odt content")

        conversor.converter.side_effect = ValueError(
            "Formato .odt não é suportado pelo Convert+"
        )

        with pytest.raises(ValueError, match=".odt"):
            conversor.converter(
                arquivo_entrada=str(arquivo_odt),
                formato_saida="md",
                diretorio_saida="/saida"
            )

    @pytest.mark.parametrize("extensao", [".mp3", ".mp4", ".png", ".jpg", ".xlsx", ".csv"])
    def test_extensoes_fora_do_escopo_sao_rejeitadas(self, conversor, tmp_path, extensao):
       
        arquivo = tmp_path / f"arquivo{extensao}"
        arquivo.write_bytes(b"fake content")

        conversor.converter.side_effect = ValueError(
            f"Formato {extensao} não é suportado"
        )

        with pytest.raises(ValueError):
            conversor.converter(
                arquivo_entrada=str(arquivo),
                formato_saida="pdf",
                diretorio_saida="/saida"
            )

    def test_formato_saida_invalido_e_rejeitado(self, conversor, arquivo_txt_valido):
       
        conversor.converter.side_effect = ValueError(
            "Formato de saída .xyz não é suportado"
        )

        with pytest.raises(ValueError, match="saída"):
            conversor.converter(
                arquivo_entrada=str(arquivo_txt_valido),
                formato_saida="xyz",
                diretorio_saida="/saida"
            )



class TestErrosSistemaArquivos:
 

    def test_ct09_diretorio_inexistente_criado_automaticamente(
        self, conversor, tmp_path
    ):
       
        dir_novo = tmp_path / "novo" / "subpasta"
        assert not dir_novo.exists()

        def converter_cria_dir(arquivo_entrada, formato_saida, diretorio_saida):
            Path(diretorio_saida).mkdir(parents=True, exist_ok=True)
            saida = Path(diretorio_saida) / "saida.pdf"
            saida.write_bytes(b"conteudo convertido")
            return {"sucesso": True, "arquivo_saida": str(saida)}

        conversor.converter.side_effect = converter_cria_dir

        resultado = conversor.converter(
            arquivo_entrada="arquivo.md",
            formato_saida="pdf",
            diretorio_saida=str(dir_novo)
        )

        assert resultado["sucesso"] is True
        assert dir_novo.exists()

    def test_ct13_permissao_negada_lanca_os_error(self, conversor):
     
        conversor.converter.side_effect = OSError(
            "Permissão negada: /root/protegido"
        )

        with pytest.raises(OSError, match="Permissão negada"):
            conversor.converter(
                arquivo_entrada="arquivo.md",
                formato_saida="pdf",
                diretorio_saida="/root/protegido"
            )

    def test_erro_durante_conversao_nao_encerra_app(self, conversor):
       
        conversor.converter.side_effect = RuntimeError(
            "Erro interno durante conversão"
        )

        # O teste verifica que o erro é lançado de forma controlada
        # (não um segfault ou crash silencioso)
        with pytest.raises(RuntimeError, match="Erro interno"):
            conversor.converter(
                arquivo_entrada="arquivo.md",
                formato_saida="pdf",
                diretorio_saida="/saida"
            )

        # O conversor continua existindo após o erro — não crashou
        assert conversor is not None



class TestTratamentoErrosEmLote:
 

    def test_erro_em_um_arquivo_nao_para_lote(self, conversor):
       
        conversor.converter_lote.return_value = [
            {"sucesso": True,  "arquivo": "a.txt"},
            {"sucesso": False, "arquivo": "b.txt", "erro": "corrompido"},
            {"sucesso": True,  "arquivo": "c.txt"},
        ]

        resultados = conversor.converter_lote(
            arquivos=["a.txt", "b.txt", "c.txt"],
            formato_saida="pdf"
        )

        assert len(resultados) == 3
        # 2 sucessos, 1 falha — mas todos foram processados
        assert sum(1 for r in resultados if r["sucesso"]) == 2
        assert sum(1 for r in resultados if not r["sucesso"]) == 1

    def test_log_registra_erro_de_conversao(self, conversor, gerenciador_logs):
    
        def converter_com_log_de_erro(
            arquivo_entrada, formato_saida, diretorio_saida, logger=None
        ):
            erro = ValueError("Arquivo corrompido")
            if logger:
                logger.registrar(
                    evento="ERRO_CONVERSAO",
                    arquivo=arquivo_entrada,
                    mensagem=str(erro)
                )
            raise erro

        conversor.converter.side_effect = converter_com_log_de_erro

        with pytest.raises(ValueError):
            conversor.converter(
                arquivo_entrada="corrompido.md",
                formato_saida="pdf",
                diretorio_saida="/saida",
                logger=gerenciador_logs
            )

        gerenciador_logs.registrar.assert_called_once()
        chamada = gerenciador_logs.registrar.call_args
        assert chamada.kwargs["evento"] == "ERRO_CONVERSAO"
