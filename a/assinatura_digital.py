from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
import os

# Caminhos padrão
PRIVATE_KEY_FILE = "chave_privada.pem"
PUBLIC_KEY_FILE = "chave_publica.pem"
SIGNATURE_FILE = "assinatura.sig"

# Função 1: Gerar chaves
def gerar_chaves():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("✅ Par de chaves gerado com sucesso.")



# Função 2: Assinar arquivo
def assinar_arquivo():
    if not os.path.exists(PRIVATE_KEY_FILE):
        print("⚠️ Chave privada não encontrada. Gere as chaves primeiro.")
        return

    arquivo = input("📄 Nome do arquivo a ser assinado: ")
    if not os.path.exists(arquivo):
        print("❌ Arquivo não encontrado.")
        return

    with open(arquivo, "rb") as f:
        dados = f.read()

    with open(PRIVATE_KEY_FILE, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    assinatura = private_key.sign(
        dados,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    with open(SIGNATURE_FILE, "wb") as f:
        f.write(assinatura)

    print("✍️ Arquivo assinado com sucesso. Assinatura salva em 'assinatura.sig'.")



# Função 3: Verificar assinatura
def verificar_assinatura():
    if not os.path.exists(PUBLIC_KEY_FILE) or not os.path.exists(SIGNATURE_FILE):
        print("⚠️ Arquivo de chave pública ou assinatura não encontrado.")
        return

    arquivo = input("📄 Nome do arquivo original: ")
    if not os.path.exists(arquivo):
        print("❌ Arquivo não encontrado.")
        return

    with open(arquivo, "rb") as f:
        dados = f.read()

    with open(SIGNATURE_FILE, "rb") as f:
        assinatura = f.read()

    with open(PUBLIC_KEY_FILE, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    try:
        public_key.verify(
            assinatura,
            dados,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print("✅ Assinatura válida e verificada com sucesso.")
    except InvalidSignature:
        print("❌ Assinatura inválida ou arquivo alterado.")


