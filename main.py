from Crypto.PublicKey import RSA;
from Crypto.Cipher import AES;
import os


def generateRSAKey():
    flag = 0
    while(flag == 0):
        entrada = input("Digite o tamanho da chave desejada: ")

        print(entrada)

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
    encrypt_file = input("Digite o nome do arquivo com extensão que você deseja criptografar: ")
    flag = 0
    while flag == 0:
        try:
            open(encrypt_file, 'r')
            flag=1
        except:
            print("Arquivo não encontrado")
            encrypt_file = input("Digite o nome do arquivo com extensão que você deseja criptografar ou digite ### para voltar ao menu: ")
            if(encrypt_file == '###'):
                flag=2

    if(flag==2):
        print("Voltando para o menu.")
        return

    key_size = input("Digite o tamanho da chave para que o arquivo seja criptografado.")

    flag = 0
    while flag == 0:
        if(key_size in ['128', '256']):
            flag=1
        else:
            print("Tamanho inválido!")
            key_size = input("Digite o tamanho da chave para que o arquivo seja criptografado ou ### para voltar ao menu.")
            if(key_size == '###'):
                flag=2
    
    if(flag==2):
        print("Voltando para o menu")
        return
    
    key = os.urandom(int(int(key_size)/8))
    vi = os.urandom(int(int(key_size)/8))
    AES.new(key, AES.MODE_CTR)


    

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
0. Sair do PyCrypt\n")

    entrada = input("Digite a opção: ")
    match(entrada):
        case '1':
            generateRSAKey()
        case '2':
            encryptFile()
        case '0':
            control_flag = 1
            print("Saindo do pycrypt!")