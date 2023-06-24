from Crypto.PublicKey import RSA;
from Crypto.Cipher import PKCS1_OAEP;
from Crypto.Cipher import AES;
from Crypto.Random import get_random_bytes;
from Crypto.Random.random import getrandbits;
import os


def generateRSAKey():
    flag = 0
    while(flag == 0):
        entrada = input("Digite o tamanho da chave desejada: ")

        if(entrada not in ["512", "1024", "2048", "4096"]):
            print("Valor de chave não válido. Necessário ser 512, 1024, 2048 ou 4096!")
            flag = 0
        else:
            tamanho_chave = int(entrada)
            flag = 1
    
    chave_pr = RSA.generate(tamanho_chave)
    chave_pu = chave_pr.public_key()

    private_file = open(nome + ".pr", 'w')
    public_file = open(nome + '.pu', 'w')

    private_file.write(chave_pr.export_key().decode("utf-8"))
    public_file.write(chave_pu.export_key().decode("utf-8"))

    private_file.close()
    public_file.close()

    print("Chave pública criada no {}.pu e chave privada no {}.pr".format(nome,nome))

    return 

def encryptFile():
    if(input("Para este modo, as chaves já devem estar geradas e o arquivo para criptografar precisa existir na pasta do projeto.\nAperte enter para continuar, ou digite 1 para voltar.") == '1'):
        return
    encrypt_file = input("Digite o nome do arquivo com extensão que você deseja criptografar: \n")
    
    flag = 0
    while flag == 0:
        try:
            file = open(encrypt_file, 'rb')
            flag=1
        except:
            print("Arquivo não encontrado")
            encrypt_file = input("Digite o nome do arquivo com extensão que você deseja criptografar ou digite ### para voltar ao menu: \n")
            if(encrypt_file == '###'):
                flag=2

    if(flag==2):
        print("Voltando para o menu.")
        return
    
    pub_rsa = input("Digite o nome do arquivo que contenha a chave pública do destinatário: \n")
    
    flag = 0
    while flag == 0:
        try:
            pub_rsa_file = open(pub_rsa, 'rb')
            flag=1
        except:
            print("Arquivo não encontrado")
            pub_rsa = input("Digite o nome do arquivo que contenha a chave pública do destinatário ou digite ### para voltar ao menu: \n")
            if(encrypt_file == '###'):
                flag=2

    if(flag==2):
        print("Voltando para o menu.")
        return

    key_size = input("Digite o tamanho da chave para que o arquivo seja criptografado:\n")

    flag = 0
    while flag == 0:
        if(key_size in ['128', '256']):
            flag=1
        else:
            print("Tamanho inválido!")
            key_size = input("Digite o tamanho da chave para que o arquivo seja criptografado ou ### para voltar ao menu: \n")
            if(key_size == '###'):
                flag=2
    
    if(flag==2):
        print("Voltando para o menu")
        return
    
    key = get_random_bytes(int(int(key_size)/8))
    nonce = getrandbits(4)
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce.to_bytes())


    teste = cipher.encrypt(file.read())
    file.close()

    encrypted_file = open(encrypt_file+".enc", "wb")

    encrypted_file.write(teste)

    encrypted_file.close()

    print("O arquivo {}.enc foi gerado e está encriptado".format(encrypt_file))

    rsa_key = RSA.importKey(pub_rsa_file.read())
    cipher = PKCS1_OAEP.new(rsa_key)
    
    keys_enc = open("keys.enc", "wb")
    keys_enc.write(cipher.encrypt(bytes("{},{}".format(key.hex(), nonce), "utf-8")))
    keys_enc.close()
    print("O arquivo keys.enc foi gerado contendo as chaves encriptadas")


def decryptFile():
    if(input("Para este modo, as chaves já devem estar geradas e o arquivo keys.enc precisa existir na pasta do projeto .\nAperte enter para continuar, ou digite 1 para voltar.") == '1'):
        return
    
    encrypted_file_name = input("Digite o nome do arquivo com extensão que você deseja descriptografar: \n")
    
    flag = 0
    while flag == 0:
        try:
            encrypted_file = open(encrypted_file_name, 'rb')
            flag=1
        except:
            print("Arquivo não encontrado")
            encrypted_file_name = input("Digite o nome do arquivo com extensão que você deseja descriptografar ou digite ### para voltar ao menu: \n")
            if(encrypted_file_name == '###'):
                flag=2

    if(flag==2):
        print("Voltando para o menu.")
        return


    key_size = input("Digite o tamanho da chave para que o arquivo seja criptografado:\n")

    flag = 0
    while flag == 0:
        if(key_size in ['128', '256']):
            flag=1
        else:
            print("Tamanho inválido! Deve ser 128 ou 256")
            key_size = input("Digite o tamanho da chave para que o arquivo seja criptografado ou ### para voltar ao menu: \n")
            if(key_size == '###'):
                flag=2
    
    if(flag==2):
        print("Voltando para o menu")
        return

    private_key = PKCS1_OAEP.new(RSA.importKey(open("{}.pr".format(nome)).read()))

    aes_keys = private_key.decrypt(open("keys.enc", "rb").read())

    keys = aes_keys.decode().split(',')

    aes_cipher = AES.new(bytes.fromhex(keys[0]), AES.MODE_CTR, nonce=int(keys[1]).to_bytes())

    ptext = open("original_file.txt", "wb")
    ptext.write(aes_cipher.decrypt(encrypted_file.read()))



print("                                   _   \n\
                                  | |  \n\
 _ __  _   _  ___ _ __ _   _ _ __ | |_ \n\
| '_ \| | | |/ __| '__| | | | '_ \| __|\n\
| |_) | |_| | (__| |  | |_| | |_) | |_ \n\
| .__/ \__, |\___|_|   \__, | .__/ \__|\n\
| |     __/ |           __/ | |        \n\
|_|    |___/           |___/|_|        \n")
      
nome = input("Digite seu nome: ")

control_flag=0
while control_flag == 0:
    print("========================================\n\
                Menu\n\
========================================\n\
Escolha uma das opções abaixo:\n\
1. Gerar chave RSA\n\
2. Criptografar um arquivo\n\
3. Descriptografar\n\
0. Sair do PyCrypt\n")

    entrada = input("Digite a opção: ")
    match(entrada):
        case '1':
            generateRSAKey()
        case '2':
            encryptFile()
        case '3':
            decryptFile()
        case '0':
            control_flag = 1
            print("Saindo do pycrypt!")