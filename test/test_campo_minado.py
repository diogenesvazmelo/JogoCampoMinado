import sys
sys.path.insert(0, '../src')
import io
import unittest
from campo_minado import CampoMinado

import unittest.mock

class TestCampoMinado(unittest.TestCase):
    def testPreencheComBombas(self):
        qtd_linhas = 5
        qtd_colunas = 5
        mapa = CampoMinado(qtd_linhas, qtd_colunas)
        mapa.preenche_com_bombas(4)
        self.assertEqual(4, mapa.qtd_bombas)

    def testAcertouBomba(self):
        qtd_linhas = 5
        qtd_colunas = 5
        linha = 3
        coluna = 3
        mapa = CampoMinado(qtd_linhas, qtd_colunas)
        mapa._coloca_bomba_posicao(linha-1, coluna-1)
        mapa.processa_jogada(linha-1, coluna-1)
        self.assertTrue(mapa.perdeu_jogo)

    def testExibePecaSelecionada(self):
        qtd_linhas = 5
        qtd_colunas = 5
        linha = 3
        coluna = 3
        mapa = CampoMinado(qtd_linhas, qtd_colunas)
        mapa.processa_jogada(linha-1, coluna-1)
        self.assertTrue(mapa.acessa_peca_mapa(linha-1, coluna-1).esta_visivel)

    def testOcultaPecaNaoSelecionada(self):
        qtd_linhas = 5
        qtd_colunas = 5
        linha = 3
        coluna = 3
        mapa = CampoMinado(qtd_linhas, qtd_colunas)
        self.assertFalse(mapa.acessa_peca_mapa(linha-1, coluna-1).esta_visivel)

    def testGanhouJogo(self):
        qtd_linhas = 3
        qtd_colunas = 3
        linha = 3
        coluna = 1
        mapa = CampoMinado(qtd_linhas, qtd_colunas)
        mapa._coloca_bomba_posicao(linha-1, coluna-1)
        mapa.qtd_bombas += 1

        mapa.processa_jogada(1-1, 1-1)
        mapa.processa_jogada(1-1, 2-1)
        mapa.processa_jogada(1-1, 3-1)

        mapa.processa_jogada(2-1, 1-1)
        mapa.processa_jogada(2-1, 2-1)
        mapa.processa_jogada(2-1, 3-1)

        mapa.processa_jogada(3-1, 2-1)
        mapa.processa_jogada(3-1, 3-1)

        self.assertTrue(mapa.ganhou_jogo)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def testImprimeMapaOculto(self, mock_stdout):
        mapa_impresso = "      \tC1\tC2\n L1  │\t.\t.\t│ L1\n L2  │\t.\t.\t│ L2\n      \tC1\tC2\n"
        qtd_linhas = 2
        qtd_colunas = 2
        mapa = CampoMinado(qtd_linhas, qtd_colunas)
        mapa.imprime_mapa() 

        self.assertEqual(mock_stdout.getvalue(), mapa_impresso)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def testImprimeSolucao(self, mock_stdout):
        mapa_impresso = "      \tC1\tC2\n L1  │\t1\t1\t│ L1\n L2  │\t*\t1\t│ L2\n      \tC1\tC2\n"
        qtd_linhas = 2
        qtd_colunas = 2
        mapa = CampoMinado(qtd_linhas, qtd_colunas)

        linha = 2
        coluna = 1
        mapa._coloca_bomba_posicao(linha-1, coluna-1)
        mapa.imprime_mapa(True) 

        self.assertEqual(mock_stdout.getvalue(), mapa_impresso)

    def testScore2x23bGanhou(self):
        qtd_linhas = 2
        qtd_colunas = 2
        linha = 2
        coluna = 2
        mapa = CampoMinado(qtd_linhas, qtd_colunas)
        mapa._coloca_bomba_posicao(1-1, 1-1)
        mapa.qtd_bombas += 1
        mapa._coloca_bomba_posicao(1-1, 2-1)
        mapa.qtd_bombas += 1
        mapa._coloca_bomba_posicao(2-1, 1-1)
        mapa.qtd_bombas += 1

        mapa.processa_jogada(linha-1, coluna-1)

        self.assertEqual(225, mapa.score)

    def testScore2x21bGanhou(self):
        qtd_linhas = 2
        qtd_colunas = 2
        mapa = CampoMinado(qtd_linhas, qtd_colunas)
        mapa._coloca_bomba_posicao(1-1, 1-1)
        mapa.qtd_bombas += 1

        mapa.processa_jogada(1-1, 2-1)

        self.assertEqual(75, mapa.score)