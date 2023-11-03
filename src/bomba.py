import peca

class Bomba(peca.Peca):
    def __init__(self, linha, coluna):
        super().__init__(linha, coluna)
        self._caractere_revelado = "*"
        self._ativa_fim_jogo = True
        self._e_bomba = True