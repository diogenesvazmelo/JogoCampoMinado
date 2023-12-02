import sys
sys.path.insert(0, '../src')
import io
import unittest
from menu_selecao_posicao_jogo import MenuSelecaoPosicaoJogo
from campo_minado import CampoMinado
from jogador import Jogador

import unittest.mock

class TestMenuSelecaoPosicaoJogo(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def testImprimeMenuVenceu(self, mock_stdout):        
        result_impresso = """
╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗
║                                                                            ║
║  PARABÉNS, VOCÊ VENCEU!                              teste                 ║
║                                                                            ║
║  Bombas no mapa: 1                                           Score: 75     ║
╚════════════════════════════════════════════════════════════════════════════╝

 Veja a solução:

      	C1	C2
 L1  │	1	1	│ L1
 L2  │	*	1	│ L2
      	C1	C2
"""
        qtd_linhas = 2
        qtd_colunas = 2
        mapa = CampoMinado(qtd_linhas, qtd_colunas)

        linha = 2
        coluna = 1
        mapa._coloca_bomba_posicao(linha-1, coluna-1)
        mapa.qtd_bombas += 1

        mapa.processa_jogada(1-1, 1-1)

        nickname = 'teste'
        jogador = Jogador(nickname)

        menu = MenuSelecaoPosicaoJogo(jogador)

        with unittest.mock.patch('builtins.input', return_value=''):
            menu._finalizacao_jogo(mapa)
            r = mock_stdout.getvalue()

            self.assertEqual(r, result_impresso)
