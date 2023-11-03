from campo_minado import CampoMinado
from menu_selecao_posicao_jogo import MenuSelecaoPosicaoJogo
from jogador import Jogador

class SubMenu:
    def __init__(self, qtd_linhas: int, qtd_colunas: int, jogador: Jogador):
        self._qtd_linhas = qtd_linhas
        self._qtd_colunas = qtd_colunas
        self._jogador = jogador

    def submenu(self):
        mapa = CampoMinado(self._qtd_linhas, self._qtd_colunas)

        qtd_bombas = 0
        while True:
            try:
                qtd_bombas = int(input("\n Quantas bombas deseja colocar no mapa? (máx. {}): ".format((self._qtd_linhas * self._qtd_colunas) - 1)))
                if qtd_bombas > (self._qtd_linhas * self._qtd_colunas) - 1:
                    print("\n Entrada Inválida! Quantidade de bombas acima do permitido.")
                elif qtd_bombas <= 0:
                    print("\n Entrada Inválida! A menor quantidade permitida de bombas é 1 (uma).")
                else:
                    break
            except ValueError:
                print("\n Entrada Inválida! Informe um valor numérico.")

        mapa.preenche_com_bombas(qtd_bombas)
        menu_selecao_jogo_1 = MenuSelecaoPosicaoJogo(self._jogador)
        menu_selecao_jogo_1.menu_selecao_jogo(mapa)