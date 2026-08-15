import os
import subprocess
import time
import socket
import sys

# Caminhos dos arquivos
IMG_HD = "himd_950mb.img"
PASTA_DOS = "/home/astral/Downloads/MSDOS/Microsoft MS-DOS 6.22 [Brazilian-Portuguese] (3.5)"
SOCK_PATH = "/tmp/qemu_monitor.sock"

print("\n" + "="*60)
print(" INSTALADOR DO MS-DOS 6.22 - IMAGEM DE 950MB (Hi-MD)")
print("="*60)

# Cria a imagem de 950MB para simular o disco Hi-MD
if not os.path.exists(IMG_HD):
    print(f"\nCriando imagem de disco '{IMG_HD}' com 950MB...")
    # Usa qemu-img para criar a imagem RAW
    os.system(f"qemu-img create -f raw {IMG_HD} 950M")
    print("Imagem criada com sucesso!")
else:
    confirmar = input(f"\nA imagem '{IMG_HD}' já existe. Deseja apagá-la e recriar uma nova? (s/n): ").strip().lower()
    if confirmar == 's':
        os.remove(IMG_HD)
        os.system(f"qemu-img create -f raw {IMG_HD} 950M")
        print("Imagem recriada com sucesso!")
    else:
        print("Usando a imagem existente...")

if os.path.exists(SOCK_PATH):
    os.remove(SOCK_PATH)

print("\nIniciando o QEMU...")

# Inicia o QEMU com o socket de monitoramento
# Apontando para a imagem local em vez do /dev/sda físico
qemu_cmd = [
    "/usr/bin/qemu-system-i386",
    "-drive", f"file={IMG_HD},format=raw,if=ide",
    "-fda", f"{PASTA_DOS}/disk1.img",
    "-boot", "a",
    "-vga", "cirrus",
    "-m", "64",
    "-monitor", f"unix:{SOCK_PATH},server,nowait"
]

proc = subprocess.Popen(qemu_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2) # Aguarda o QEMU abrir

def enviar_comando_qemu(comando):
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(SOCK_PATH)
        s.recv(1024) # Ignora o texto de boas-vindas do QEMU
        s.sendall((comando + "\n").encode())
        s.close()
    except Exception as e:
        print(f"Erro ao comunicar com o QEMU: {e}")

print("\n" + "="*50)
print(" O QEMU foi aberto em outra janela.")
print(" Volte para o terminal quando a tela azul pedir o próximo disquete!")
print("="*50)

while True:
    if proc.poll() is not None:
        print("\nO QEMU foi fechado. Encerrando o script...")
        break

    print("\n[1] Inserir Disquete 1")
    print("[2] Inserir Disquete 2")
    print("[3] Inserir Disquete 3")
    print("[4] Ejetar disquete (Use isso quando pedir para remover no final)")
    print("[0] Fechar Tudo")
    
    opcao = input("\nEscolha uma opção e aperte ENTER: ").strip()

    if opcao == '1':
        enviar_comando_qemu(f'change floppy0 "{PASTA_DOS}/disk1.img"')
        print("=> Disquete 1 inserido! Pode apertar ENTER na tela azul do QEMU.")
    elif opcao == '2':
        enviar_comando_qemu(f'change floppy0 "{PASTA_DOS}/disk2.img"')
        print("=> Disquete 2 inserido! Pode apertar ENTER na tela azul do QEMU.")
    elif opcao == '3':
        enviar_comando_qemu(f'change floppy0 "{PASTA_DOS}/disk3.img"')
        print("=> Disquete 3 inserido! Pode apertar ENTER na tela azul do QEMU.")
    elif opcao == '4':
        enviar_comando_qemu('eject floppy0')
        print("=> Disquete ejetado! Pode apertar ENTER na tela azul para reiniciar.")
    elif opcao == '0':
        proc.terminate()
        break
    else:
        print("Opção inválida!")
