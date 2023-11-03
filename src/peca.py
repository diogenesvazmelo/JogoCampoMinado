CARACTERE_OCULTO = "."
CARACTERE_REVELADO = "0"
CARACTERE_SELECAO_ATUAL = "S"

class Peca():
    def __init__(self, linha, coluna):
        self._caractere_oculto = CARACTERE_OCULTO
        self._caractere_revelado = CARACTERE_REVELADO
        self._caractere_selecao_atual = CARACTERE_SELECAO_ATUAL
        self._esta_visivel = False
        self._ativa_fim_jogo = False
        self._e_bomba = False
        self._valor = 0
        self._linha = linha
        self._coluna = coluna

    @property
    def caractere_oculto(self) -> str:
        return self._caractere_oculto

    def get_caractere_revelado(self) -> str:
        return self._caractere_revelado
    
    def set_caractere_revelado(self, value):
        self._caractere_revelado = value
    
    @property
    def caractere_selecao_atual(self) -> str:
        return self._caractere_selecao_atual
    
    def caractere_ativo(self) -> str:
        if self._esta_visivel:
            return self.get_caractere_revelado()
        elif not self._esta_visivel:
            return self._caractere_oculto
    
    @property
    def esta_visivel(self) -> bool:
        return self._esta_visivel
    def define_visivel(self):
        self._esta_visivel = True

    @property
    def esta_oculta(self) -> bool:
        if self._esta_visivel:
            return False
        return True
    def define_oculta(self):
        self._esta_visivel = False

    def get_ativa_fim_jogo(self) -> bool:
        return self._ativa_fim_jogo
    
    @property
    def e_bomba(self) -> bool:
        return self._e_bomba
    
    def get_valor(self) -> int:
        return self._valor
    def set_valor(self, value):
        self._valor = value
        self.set_caractere_revelado(str(value))
    
    @property
    def linha(self) -> int:
        return self._linha
    
    @property
    def coluna(self) -> int:
        return self._coluna