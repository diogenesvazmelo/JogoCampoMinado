import boto3
from datetime import datetime
import json
from campo_minado import CampoMinado
from jogador import Jogador

import importlib.util
arq_aws_credentials_spec = importlib.util.find_spec("aws_credentials")
if arq_aws_credentials_spec is not None:
    from aws_credentials import ARQ_AWS_CREDENTIALS

class AWSHandler:
    def __init__(self, mapa: CampoMinado, jogador: Jogador):
        self._status_score_salvo = False
        self._dados = self._prepara_dados(mapa, jogador)

        self._s3 = None
        self._sucesso_autentica = self._autentica()

        self._arquivo_aws_credentials_disponivel = False
        if arq_aws_credentials_spec is not None:
            self._arquivo_aws_credentials_disponivel = True
    
    def _autentica(self) -> bool:
        try:
            self._s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
            return True
        except:
            return False


    def salvar_no_s3(self) -> datetime:
        lista_hist = self.ler_do_s3()["Registros"]
        lista_hist.append(self._dados)

        json_combinado = {}
        json_combinado["Registros"] = lista_hist
        
        # Salvando os dados atualizados no S3
        try:
            self._s3.put_object(Body=json.dumps(json_combinado), Bucket=self.bucket_name, Key=self.file_name)
            self._status_score_salvo = True
            return self._dados['data']
        except:
            return None

    def zerar_placar(self):
        json_base = {}
        json_base["Registros"] = []
        self._s3.put_object(Body=json.dumps(json_base), Bucket=self.bucket_name, Key=self.file_name)

    def ler_do_s3(self) -> dict:
        try:
            response = self._s3.get_object(Bucket=self.bucket_name, Key=self.file_name)
            dados_lidos = json.loads(response['Body'].read().decode('utf-8'))
            self._s3.close()
        except:
            # Se o arquivo não existir, retorna um dicionario vazio
            json_base = {}
            json_base["Registros"] = []
            dados_lidos = json_base

        return dados_lidos
    
    def _ler_aws_credentials(self):
        arq = ARQ_AWS_CREDENTIALS

        # Extrai as credenciais
        aws_access_key_id = arq['aws_credentials']['access_key']
        aws_secret_access_key = arq['aws_credentials']['secret_key']
        region = arq['aws_credentials']['region']
        aws_bucket = arq['aws_credentials']['bucket']
        aws_file = arq['aws_credentials']['file']

        return aws_access_key_id, aws_secret_access_key, region, aws_bucket, aws_file
    
    def _prepara_dados(self, mapa: CampoMinado, jogador: Jogador) -> dict:
        dados = {
            'nick': jogador.nick,
            'score': mapa.score,
            'data': datetime.now().isoformat()  # Formato ISO 8601 para a data e hora
        }
        return dados
    
    @property
    def aws_access_key_id(self) -> str:
        return self._ler_aws_credentials()[0]

    @property
    def aws_secret_access_key(self) -> str:
        return self._ler_aws_credentials()[1]
    
    @property
    def aws_region(self) -> str:
        return self._ler_aws_credentials()[2]
    
    @property
    def bucket_name(self) -> str:
        return self._ler_aws_credentials()[3]
    
    @property
    def file_name(self) -> str:
        return self._ler_aws_credentials()[4]
    
    @property
    def status_score_salvo(self) -> bool:
        return self._status_score_salvo

    @property
    def arquivo_aws_credentials_disponivel(self) -> bool:
        return self._arquivo_aws_credentials_disponivel
    
    @property
    def sucesso_autentica(self) -> bool:
        return self._sucesso_autentica
    
    @property
    def dados(self) -> dict:
        return self._dados
    
