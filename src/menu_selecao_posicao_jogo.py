import os
from campo_minado import CampoMinado
from menu_finaliza_jogo import MenuFinalizaJogo
from jogador import Jogador

MAX_LINHAS = 5
MAX_COLUNAS = 5

MAX_LEN_NICK = 8

class MenuSelecaoPosicaoJogo:
    def __init__(self, jogador: Jogador, msg = ""):
        self._jogador = jogador
        self._msg = msg

    def menu_selecao_jogo(self, mapa: CampoMinado):
        while True:
            self._exibir_cabecalho(mapa)
            mapa.imprime_mapa()
            texto_input = input("\n Escolha uma posição (linha e coluna, ex. l1c2): ")
            l, c, erro = self.trata_string_linha_coluna_escolhida(texto_input)

            if (0 < l <= mapa.qtd_linhas) and (0 < c <= mapa.qtd_colunas):
                if mapa.acessa_peca_mapa(l - 1, c - 1).esta_oculta:
                    self._msg = ""
                    mapa.processa_jogada(l - 1, c - 1)

                    if mapa.perdeu_jogo or mapa.ganhou_jogo:
                        self._finalizacao_jogo(mapa)
                        menu_finaliza = MenuFinalizaJogo(mapa, self._jogador)
                        menu_finaliza.menu_finaliza_jogo()
                        break
                else:
                    self._msg = "A posição selecionada já foi revelada. Escolha uma posição diferente."
            elif l > mapa.qtd_linhas and l > mapa.qtd_colunas:
                self._msg = "Linha e coluna acima do tamanho do mapa!"
            elif l > mapa.qtd_linhas:
                self._msg = "Linha acima do tamanho do mapa!"
            elif c > mapa.qtd_colunas:
                self._msg = "Coluna acima do tamanho do mapa!"
            else:
                self._msg = erro
            
    def trata_string_linha_coluna_escolhida(self, texto_input: str):
        if len(texto_input) <= 0:
            return -1, -1, "Houve erro na operação. A string não está no formato esperado. (vazio)"
        elif texto_input[0].lower() != 'l':
            return -1, -1, "Houve erro na operação. A string não está no formato esperado. (não iniciado com l)"

        numeros = []

        # Itera sobre os caracteres da string
        numero_atual = ''
        for i in range(len(texto_input)):
            char = texto_input[i]
            if char.isdigit():
                # Se o caractere atual é um dígito, adiciona ao número atual
                numero_atual += char
            elif (numero_atual and char.lower() == 'c'):
                try:
                    # Tenta converter o número acumulado para inteiro
                    numeros.append(int(numero_atual))
                    numero_atual = ''  # Reseta o número atual
                except ValueError:
                    return -1, -1, "Houve erro na operação ao registrar o valor da linha. A string não está no formato esperado. (ValueError)"

        # Adiciona o último número, se houver
        if numero_atual:
            try:
                numeros.append(int(numero_atual))
            except ValueError:
                return "Houve erro na operação ao registrar o valor da coluna. A string não está no formato esperado. (ValueError)"
    
        if len(numeros) == 2 and (numeros[0] > 0 or numeros[1] > 0):
            return numeros[0], numeros[1], "Houve erro na operação. O valor de linhas e colunas deve ser superior a zero."
        else:
            print(numeros)
            return -1, -1, "Entrada Inválida! (Valor nulo ou negativo)"
        
    def _exibir_cabecalho(self, mapa: CampoMinado):
        os.system('cls')

        print()
        print("╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗")
        print("║                                                                            ║")
        print(f"║  JOGANDO...                                       {self._jogador.nick.rjust(MAX_LEN_NICK)}                 ║")
        print("║                                                                            ║")
        print("║  Bombas no mapa: {}                                         Score: {}  ║".format(str(mapa.qtd_bombas).ljust(3), str(mapa.score).ljust(5)))
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        if self._msg != "":
            print(f" MENSAGEM DE ALERTA: {self._msg}")
        print()

    def _exibir_cabecalho_perdedor(self, mapa: CampoMinado):
        os.system('cls')

        print()
        print("╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗")
        print("║                                                                            ║")
        print(f"║  VOCÊ PERDEU!                                     {self._jogador.nick.rjust(MAX_LEN_NICK)}                 ║")
        print("║                                                                            ║")
        print("║  Bombas no mapa: {}                                         Score: {}  ║".format(str(mapa.qtd_bombas).ljust(3), str(mapa.score).ljust(5)))
        print("╚════════════════════════════════════════════════════════════════════════════╝")

    def _exibir_cabecalho_vencedor(self, mapa: CampoMinado):
        os.system('cls')

        print()
        print("╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗")
        print("║                                                                            ║")
        print(f"║  PARABÉNS, VOCÊ VENCEU!                           {self._jogador.nick.rjust(MAX_LEN_NICK)}                 ║")
        print("║                                                                            ║")
        print("║  Bombas no mapa: {}                                         Score: {}  ║".format(str(mapa.qtd_bombas).ljust(3), str(mapa.score).ljust(5)))
        print("╚════════════════════════════════════════════════════════════════════════════╝")

    def _finalizacao_jogo(self, mapa: CampoMinado):
        if mapa._perdeu_jogo:
            self._exibir_cabecalho_perdedor(mapa)
        else:
            self._exibir_cabecalho_vencedor(mapa)
        print("\n Veja a solução:\n")
        mapa.imprime_mapa(True)
        input("\n\n Pressione ENTER para continuar...")