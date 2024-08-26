import os
from typing import List
import boto3
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da AWS a partir do .env
AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION: str = os.getenv('AWS_REGION')
BUCKET_NAME: str = os.getenv('BUCKET_NAME')

# Print para verificar se as variáveis de ambiente foram carregadas corretamente
print(f"AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID}")
print(f"AWS_SECRET_ACCESS_KEY: {AWS_SECRET_ACCESS_KEY}")
print(f"AWS_REGION: {AWS_REGION}")
print(f"BUCKET_NAME: {BUCKET_NAME}")

# Configura o cliente S3
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    print("Cliente S3 configurado com sucesso.")
except Exception as e:
    print(f"Erro ao configurar o cliente S3: {e}")
    raise

def deletar_todos_arquivos_s3(bucket_name: str) -> None:
    """Deleta todos os arquivos de um bucket S3."""
    try:
        # Listar todos os objetos no bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        # Verificar se o bucket contém objetos
        if 'Contents' in response:
            for objeto in response['Contents']:
                # Deletar cada objeto
                s3_client.delete_object(Bucket=bucket_name, Key=objeto['Key'])
                print(f"'{objeto['Key']}' foi deletado do bucket '{bucket_name}'.")
        else:
            print(f"O bucket '{bucket_name}' não contém nenhum arquivo.")
    except Exception as e:
        print(f"Erro ao deletar arquivos do bucket '{bucket_name}': {e}")
        raise

# Exemplo de uso
if __name__ == "__main__":
    BUCKET_NAME = 'backup-jornadadedados'
    deletar_todos_arquivos_s3(BUCKET_NAME)