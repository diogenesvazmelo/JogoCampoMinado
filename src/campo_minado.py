import random
from peca import Peca
from bomba import Bomba

class CampoMinado:
    def __init__(self, qtd_linhas, qtd_colunas, qtd_bombas = 0):
        self._qtd_linhas = qtd_linhas
        self._qtd_colunas = qtd_colunas
        self._qtd_bombas = qtd_bombas

        self._qtd_visivel = 0
        self._score = 0

        self._mapa = [[Peca(l, c) for c in range(qtd_colunas)] for l in range(qtd_linhas)]
        self.preenche_com_bombas(self._qtd_bombas)
        
        self._perdeu_jogo = False
        self._ganhou_jogo = False

    def preenche_com_bombas(self, qtd_bombas):
        self._qtd_bombas = qtd_bombas
        bombas_colocadas = 0
        while bombas_colocadas < qtd_bombas:
            linha = random.randint(0, self._qtd_linhas - 1)
            coluna = random.randint(0, self._qtd_colunas - 1)

            if isinstance(self._mapa[linha][coluna], Peca) and not isinstance(self._mapa[linha][coluna], Bomba):
                # Se a célula contém uma instância de Peca, adicione a bomba
                self._mapa[linha][coluna] = Bomba(linha, coluna)  # Substitui Peca() pela classe real das bombas
                bombas_colocadas += 1

        self._atualiza_pecas_proximas_de_bomba()
        
    def _atualiza_pecas_proximas_de_bomba(self):
        for l in range(self._qtd_linhas):
            for c in range(self._qtd_colunas):
                if isinstance(self._mapa[l][c], Peca) and not isinstance(self._mapa[l][c], Bomba):
                    soma = 0

                    if c - 1 >= 0 and isinstance(self._mapa[l][c - 1], Bomba):
                        soma += 1

                    if c + 1 < self._qtd_colunas and isinstance(self._mapa[l][c + 1], Bomba):
                        soma += 1

                    if l - 1 >= 0 and isinstance(self._mapa[l - 1][c], Bomba):
                        soma += 1

                    if l + 1 < self._qtd_linhas and isinstance(self._mapa[l + 1][c], Bomba):
                        soma += 1

                    if l - 1 >= 0 and c - 1 >= 0 and isinstance(self._mapa[l - 1][c - 1], Bomba):
                        soma += 1

                    if l - 1 >= 0 and c + 1 < self._qtd_colunas and isinstance(self._mapa[l - 1][c + 1], Bomba):
                        soma += 1

                    if c - 1 >= 0 and l + 1 < self._qtd_linhas and isinstance(self._mapa[l + 1][c - 1], Bomba):
                        soma += 1

                    if l + 1 < self._qtd_linhas and c + 1 < self._qtd_colunas and isinstance(self._mapa[l + 1][c + 1], Bomba):
                        soma += 1

                    if soma > 0:
                        self._mapa[l][c].set_valor(soma)

    def imprime_mapa(self, imprime_solucao = False):
        if imprime_solucao:
            for l in range(self._qtd_linhas):
                for c in range(self._qtd_colunas):
                    self._mapa[l][c].define_visivel()

        for l in range(-1, self._qtd_linhas + 1):
            if l == -1 or l == self._qtd_linhas:
                print("      ", end="")
            elif l < self._qtd_linhas:
                print(" L{}  │".format(l + 1) if l <= 8 else " L{} │".format(l + 1), end="")

            for c in range(self._qtd_colunas):
                if l == -1 or l == self._qtd_linhas:
                    print("\tC{}".format(c + 1), end="")
                else:
                    print("\t{}".format(self._mapa[l][c].caractere_ativo()), end="")

            if l != -1 and l < self._qtd_linhas:
                print("\t│ L{}".format(l + 1))
            else:
                print()

    def processa_jogada(self, linha, coluna):
        if isinstance(self._mapa[linha][coluna], Bomba):
            self._perdeu_jogo = True
        else:
            self._processa_acertou_peca(self._mapa[linha][coluna])

    def _processa_acertou_peca(self, peca: Peca):
        for l in range(peca.linha - 1,  peca.linha + 1):
            for c in range(peca.coluna - 1,  peca.coluna + 1):
                if 0 <= l < self._qtd_linhas and 0 <= c < self._qtd_colunas:
                    if isinstance(self._mapa[l][c], Peca) and not isinstance(self._mapa[l][c], Bomba):
                         self._mapa[l][c].define_visivel()

        self._atualiza_qtd_visivel()
        self._atualiza_score()
        self._verifica_ganhou_jogo()

    def _atualiza_qtd_visivel(self):
        qtd_visivel = 0
        for l in range(self._qtd_linhas):
            for c in range(self._qtd_colunas):
                if not isinstance(self._mapa[l][c], Bomba) and (self._mapa[l][c].esta_visivel):
                    qtd_visivel += 1
        self._qtd_visivel = qtd_visivel

    def _verifica_ganhou_jogo(self):
        if self._qtd_visivel == ((self._qtd_linhas * self._qtd_colunas) - self._qtd_bombas):
            self._ganhou_jogo = True

    def acessa_peca_mapa(self, linha: int, coluna: int) -> Peca:
        return self._mapa[linha][coluna]
    
    def _atualiza_score(self):
        score = 0
        for l in range(self._qtd_linhas):
            for c in range(self._qtd_colunas):
                if not isinstance(self._mapa[l][c], Bomba) and (self._mapa[l][c].esta_visivel):
                    score += self._mapa[l][c].get_valor()
        self._score = round(score * (self._qtd_bombas / (self._qtd_linhas * self._qtd_colunas)) * 100)

    @property
    def perdeu_jogo(self) -> bool:
        return self._perdeu_jogo
    
    @property
    def ganhou_jogo(self) -> bool:
        return self._ganhou_jogo
    
    @property
    def qtd_bombas(self) -> int:
        return self._qtd_bombas
    
    @property
    def score(self) -> int:
        return self._score
    
    @property
    def qtd_linhas(self) -> int:
        return self._qtd_linhas
    
    @property
    def qtd_colunas(self) -> int:
        return self._qtd_colunas