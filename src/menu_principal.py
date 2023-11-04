import os
import re
from submenu import SubMenu
from jogador import Jogador

MAX_LINHAS = 5
MAX_COLUNAS = 5

MIN_LINHAS = 1
MIN_COLUNAS = 1

MAX_LEN_NICK = 8

class MenuPrincipal:
    def __init__(self, msg = ""):
        self._msg = msg

    def menu_principal(self):
        while True:
            self._exibir_menu()
            escolha = str(input(" Escolha: "))

            if escolha == "1":
                self._msg = ""
                jogador = self._inserir_nick()
                while True:
                    self._exibir_vamos_jogar(jogador)
                    texto_input = input(" Qual o tamanho do mapa? Informe a quantidade de linhas e colunas (máx.: {}x{}): ".format(MAX_LINHAS, MAX_COLUNAS))
                    qtd_linhas, qtd_colunas, erro = self._trata_string_tamanho_mapa(texto_input)

                    if (MIN_LINHAS <= qtd_linhas <= MAX_LINHAS) and (MIN_COLUNAS <= qtd_colunas <= MAX_COLUNAS):
                        self._msg = ""
                        break
                    else:
                        self._envia_msg_alerta_tamanho_mapa(qtd_linhas, qtd_colunas, erro)

                submenu1 = SubMenu(qtd_linhas, qtd_colunas, jogador)
                submenu1.submenu()
            elif escolha == "2":
                os.system('cls')
                exit(0)
            else:
                self._msg = "Entrada inválida!"

    def _exibir_menu(self):
        os.system('cls')

        print()
        print("╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗")
        print("║                                                                            ║")
        print("║  MENU                                                                      ║")
        print("║                                                                            ║")
        print("║  Opções:   1. Jogar   2. Sair                                              ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        if self._msg != "":
            print(f" MENSAGEM DE ALERTA: {self._msg}\n")

    def _exibir_vamos_jogar(self, jogador: Jogador):
        os.system('cls')

        print()
        print("╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗")
        print("║                                                                            ║")
        print(f"║  VAMOS JOGAR!                                     {jogador.nick.rjust(MAX_LEN_NICK)}                 ║")
        print("║                                                                            ║")
        print("║                                                                            ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        if self._msg != "":
            print(f" MENSAGEM DE ALERTA: {self._msg}\n")
        
    def _exibir_inserir_nick(self):
        os.system('cls')

        print()
        print("╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗")
        print("║                                                                            ║")
        print("║  VAMOS JOGAR!                                                              ║")
        print("║                                                                            ║")
        print("║  Escolha um nickname. Escreva apenas letras e números (máx. {} caracteres)  ║".format(MAX_LEN_NICK))
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        if self._msg != "":
            print(f" MENSAGEM DE ALERTA: {self._msg}\n")
    
    def _inserir_nick(self) -> Jogador:
        while True:
            self._exibir_inserir_nick()
            
            texto_input = str(input(" Informe o nickname desejado: "))
            if re.match("^[A-Za-z0-9_-]*$", texto_input) and len(texto_input) <= MAX_LEN_NICK:
                self._msg = ""
                return Jogador(texto_input)
            else:
                self._msg = "Não foi possível utilizar o nickname informado. Tente novamente."

    def _trata_string_tamanho_mapa(self, texto_input: str):
        texto_input = texto_input.lower()
        try:
            qtd_linhas = int(texto_input.split('x')[0])
            qtd_colunas = int(texto_input.split('x')[1])
        except ValueError:
            return -1, -1, "Entrada Inválida! (ValueError)"
        except IndexError:
            return -1, -1, "Entrada Inválida! (IndexError)"

        if qtd_linhas > 0 and qtd_colunas > 0:
            return qtd_linhas, qtd_colunas, ""
        else:
            return -1, -1, "Entrada Inválida!"

    def _envia_msg_alerta_tamanho_mapa(self, qtd_linhas: int, qtd_colunas: int, erro: str):
        if qtd_linhas < 0 or qtd_colunas < 0:
            self._msg = erro
        elif qtd_linhas > MAX_LINHAS and qtd_colunas > MAX_COLUNAS:
            self._msg = "Quantidade de linhas e colunas acima do permitido!"
        elif qtd_linhas < MIN_LINHAS and qtd_colunas < MIN_COLUNAS:
            self._msg = "Quantidade de linhas e colunas abaixo do permitido!"
        
        elif qtd_linhas > MAX_LINHAS and qtd_colunas < MIN_COLUNAS:
            self._msg = "Quantidade de linhas acima do permitido e colunas abaixo do permitido!"
        elif qtd_linhas < MIN_LINHAS and qtd_colunas > MAX_COLUNAS:
            self._msg = "Quantidade de linhas abaixo do permitido e colunas acima do permitido!"
        
        elif qtd_linhas > MAX_LINHAS:
            self._msg = "Quantidade de linhas acima do permitido!"
        elif qtd_colunas > MAX_COLUNAS:
            self._msg = "Quantidade de colunas acima do permitido!"

        elif qtd_linhas < MIN_LINHAS:
            self._msg = "Quantidade de linhas abaixo do permitido!"
        else:
            self._msg = "Quantidade de colunas abaixo do permitido!"