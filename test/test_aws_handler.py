import sys
sys.path.insert(0, '../src')
import unittest
import requests
from datetime import datetime

from aws_handler import AWSHandler
from campo_minado import CampoMinado
from jogador import Jogador

class TestAwsHandler(unittest.TestCase):
    def setUp(self):
        qtd_linhas = 5
        qtd_colunas = 5
        self.mapa = CampoMinado(qtd_linhas, qtd_colunas)
        self.mapa.score = -1
        
        nickname = 'teste'
        self.jogador = Jogador(nickname)

        self.data_salvamento = datetime.now().isoformat()

        self.aws = AWSHandler(self.mapa, self.jogador)

    def testInternetConnectionGoogle(self):
        try:
            requests.get("http://www.google.com")
            conexao = True
        except requests.ConnectionError:
            conexao = False

        # error message in case if test case got failed 
        message = """
            Não foi possível acessar http://www.google.com. Verifique sua conexão com a internet.
        """

        self.assertTrue(conexao, message)

    def testInternetConnectionBing(self):
        try:
            requests.get("http://www.bing.com")
            conexao = True
        except requests.ConnectionError:
            conexao = False

        # error message in case if test case got failed 
        message = """
            Não foi possível acessar http://www.bing.com. Verifique sua conexão com a internet.
        """

        self.assertTrue(conexao, message)

    def testCredenciaisAcessoAWS(self):
        # error message in case if test case got failed 
        message = """
            Credenciais de acesso ao seriço AWS não localizadas.
        """

        # assert to check if first parameter is greater than second param 
        self.assertTrue(self.aws.arquivo_aws_credentials_disponivel, message)

    def testLerDoS3(self):
        # error message in case if test case got failed 
        message = """
            Não foi possível recuperar as informações de placar a partir do serviço AWS.
        """

        # assert to check if first parameter is greater than second param 
        self.assertGreater(len(self.aws.ler_do_s3()), 0, message) 

    def testSalvarNoS3(self):
        # error message in case if test case got failed 
        message = """
            Não foi possível salvar as informações de placar no serviço AWS.
        """

        # assert to check if first parameter is greater than second param 
        self.assertGreaterEqual(self.aws.salvar_no_s3(), self.data_salvamento, message) 
