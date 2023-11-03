import os
from datetime import datetime
from aws_handler import AWSHandler
from campo_minado import CampoMinado
from jogador import Jogador

MAX_LEN_NICK = 8

class MenuFinalizaJogo:
    def __init__(self, mapa: CampoMinado, jogador: Jogador, msg = ""):
        self._mapa = mapa
        self._jogador = jogador
        self._msg = msg

    def menu_finaliza_jogo(self):
        while True:
            self._exibir_menu_finalizacao(self._mapa)
            escolha = str(input(" Escolha: "))

            if escolha == "1":
                self._msg = ""

                aws_handler = AWSHandler(self._mapa, self._jogador)

                # Caso precise apagar o registro de placar, descomentar a linha abaixo:
                # aws_handler.zerar_placar()

                # Salvando os dados no S3
                data = aws_handler.salvar_no_s3()

                if aws_handler.status_score_salvo:
                    self._exibir_menu_salvo_sucesso(self._mapa)
                    self._exibir_ranking(aws_handler.ler_do_s3(), data)
                else:
                    self._exibir_menu_salvo_falha(self._mapa)

                input("\n\n Pressione ENTER para continuar...")
                break

            elif escolha == "2":
                break
            else:
                self._msg = "Entrada inválida!"

    def _exibir_menu_finalizacao(self, mapa: CampoMinado):
        os.system('cls')

        print()
        print("╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗")
        print("║                                                                            ║")
        print(f"║  SALVAR SCORE                                     {self._jogador.nick.rjust(MAX_LEN_NICK)}   Score: {str(mapa.score).ljust(5)}  ║")
        print("║                                                                            ║")
        print("║  Opções:   1. Salvar   2. Voltar ao Menu Principal                         ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        if self._msg != "":
            print(f" MENSAGEM DE ALERTA: {self._msg}\n")

    def _exibir_menu_salvo_sucesso(self, mapa: CampoMinado):
        os.system('cls')

        print()
        print("╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗")
        print("║                                                                            ║")
        print(f"║  SALVAR SCORE                                     {self._jogador.nick.rjust(MAX_LEN_NICK)}   Score: {str(mapa.score).ljust(5)}  ║")
        print("║                                                                            ║")
        print("║  Score salvo com sucesso!                                                  ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        if self._msg != "":
            print(f" MENSAGEM DE ALERTA: {self._msg}\n")

    def _exibir_menu_salvo_falha(self, mapa: CampoMinado):
        os.system('cls')

        print()
        print("╔═══════════════════════════════ CAMPO MINADO ═══════════════════════════════╗")
        print("║                                                                            ║")
        print(f"║  SALVAR SCORE                                     {self._jogador.nick.rjust(MAX_LEN_NICK)}   Score: {str(mapa.score).ljust(5)}  ║")
        print("║                                                                            ║")
        print("║  Infelizmente não foi possível salvar seu Score no momento                 ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        if self._msg != "":
            print(f" MENSAGEM DE ALERTA: {self._msg}\n")

    def _exibir_ranking(self, json_com_registro: dict, data_procurada: datetime):
        # Ordenar os registros pelo "valor" (decrescente) e pela data (decrescente)
        registros_ordenados = sorted(json_com_registro["Registros"], key=lambda x: (x["score"], datetime.strptime(x["data"], "%Y-%m-%dT%H:%M:%S.%f")), reverse=True)
        posicao_registro = next((index for index, registro in enumerate(registros_ordenados) if registro["score"] == self._mapa.score and registro["nick"] == self._jogador.nick and registro["data"] == data_procurada), None)
        posicao_registro += 1

        print(" Você ficou na posição \t-- {} --".format(posicao_registro))
        print(" Veja o Ranking com os 5 maiores Scores:\n")

        # Exibir os 5 primeiros registros em uma tabela no terminal
        print(" {:<15} {:<10} {:<25}".format("Nickname", "Score", "Data"))
        print("=" * 78)
        for registro in registros_ordenados[:5]:
            data_formatada = datetime.strptime(registro["data"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y %H:%M")
            print(" {:<15} {:<10} {:<25}".format(registro["nick"], registro["score"], data_formatada))