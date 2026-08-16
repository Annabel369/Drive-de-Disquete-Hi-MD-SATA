# Drive de Disquete Hi-MD SATA


<img width="1749" height="955" alt="Captura de tela de 2026-08-14 02-33-22" src="https://github.com/user-attachments/assets/9d62f8ea-1522-4f01-aa1c-c2866247f87c" />


Este repositório documenta o projeto para a criação de um "Drive de Disquete Hi-MD SATA", uma central multimídia baseada em MS-DOS que utiliza mídia Hi-MD, executada em hardware de PC antigo com suporte a SATA e reprodução headless (sem monitor/teclado) com integração a um display LCD frontal.

## 1. O "Drive de Disquete Hi-MD SATA"

Como o drive mecânico original da Sony conversa exclusivamente via USB/ATAPI proprietário e depende do controlador Hi-MD para ler a mídia óptica, você precisa de uma ponte interna:

- **Mídia e Leitor:** Utilize a mecânica e a placa controladora de um drive Hi-MD de gaveta/módulo (como o de um deck ONKYO MD-133 ou drive de PC Sony Hi-MD).
- **Conversão USB para SATA:** Placas-mãe de PC não leem mídias Hi-MD nativamente via SATA. Você precisará usar uma placa conversora de protocolo (USB-to-SATA ou ponte de barramento) acoplada internamente ao gabinete.
- **Formatação FAT16 de 900MB:** O MS-DOS 6.22 suporta partições FAT16 de até 2GB (desde que use clusters de 32KB). Formate o disco Hi-MD de 1GB diretamente em FAT16 usando utilitários como o MKFS.FAT no Linux ou Diskpart no Windows, mantendo o tamanho útil em ~900MB.

## 2. A Central Multimídia DOS (Hardware & Boot)

https://drive.google.com/file/d/1Jm0dEdqjywIgEgmnEKEcz_yJKzEWrn5k/view?usp=sharing

### 1. Gravador de Imagem de Disco (GNOME Disks) - Mais fácil no Linux

  Como você está usando Linux, é muito provável que você já tenha esse
  programa instalado (padrão no Ubuntu, Mint e outras distribuições).

  • Por que recomendo: É nativo, seguro e não precisa instalar nada.
  • Como usar: Basta abrir o seu gerenciador de arquivos, clicar com o
  botão direito do mouse no arquivo himd_dos.img, escolher "Abrir com
  Gravador de Imagem de Disco" (ou Disk Image Writer), selecionar o seu
  drive Hi-MD na lista e clicar em Restaurar/Gravar.

  ### 2. Balena Etcher - A melhor opção visual

  Se você preferir um programa dedicado com uma interface muito bonita e à
  prova de erros.

  • Por que recomendo: Ele esconde os HDs principais do seu sistema para
  evitar que você grave no lugar errado por acidente. É excelente para
  pendrives, cartões SD e adaptadores USB/SATA.
  • Como usar: Você baixa no site oficial (tem para Linux, Windows e Mac),
  seleciona o arquivo himd_dos.img, seleciona o drive Hi-MD e clica em
  "Flash!".

  ### 3. Comando dd - Para os fortes no Terminal

  Se você quiser gravar direto pelo terminal Linux sem instalar nada.

  • Por que recomendo: É a ferramenta mais pura e direta que existe no
  Linux.
  • Como usar:
  Primeiro, descubra a letra do seu drive Hi-MD rodando lsblk (digamos que
  seja /dev/sdb ou /dev/sdc).
  Depois, rode o comando:
  sudo dd if=/home/astral/ama/himd_dos.img of=/dev/sdX bs=4M
  status=progress
  (Cuidado: troque o sdX pela letra correta do drive Hi-MD. Se colocar o HD
  errado, ele apaga seu sistema!)

  ### 4. Rufus - Se for fazer pelo Windows

  Caso você decida plugar o disco em um PC com Windows.

  • Por que recomendo: É leve, não precisa instalar (versão portátil) e
  grava imagens RAW perfeitamente.

  Minha sugestão final: Tente primeiro a opção 1 (GNOME Disks) clicando com
  o botão direito no arquivo. Se não tiver no seu sistema, baixe o Balena
  Etcher. São as formas mais seguras de garantir que você não vai apagar o
  HD do seu computador sem querer!


<img width="1376" height="768" alt="Storyboard_grid_for_product_prop…_202608141812" src="https://github.com/user-attachments/assets/35350d26-5e15-4145-9ee9-09395937a33d" />


Para dar boot em DOS via conexão SATA mantendo suporte a teclado, mouse e saída de vídeo moderna/antiga:

| Componente | Opção Recomendada | Função no Projeto |
| :--- | :--- | :--- |
| **Placa-Mãe / Processador** | SBC Thin Mini-ITX (ex: Intel Atom / Celeron antigo) ou placa industrial com IDE/SATA | Suporte nativo a BIOS Legacy (necessário para dar boot no MS-DOS/FreeDOS em SATA). |
| **Vídeo & Áudio** | Placa de som compatível com Sound Blaster (ex: chip ES1371 / Ensoniq) e saída VGA/HDMI | Garantir execução de som em jogos DOS sem drivers complexos. |
| **Controles** | Portas PS/2 para Teclado/Mouse (ou USB com suporte a Legacy Emulation na BIOS) | Entrada de comandos nativa em ambiente MS-DOS. |

## 3. Execução Sem Teclado/Monitor (Headless Player)

Para que o PC ligue, toque as músicas automaticamente e mostre as informações no painel frontal (como o ONKYO MD-133) sem precisar de monitor ou teclado conectados:

<img width="960" height="1101" alt="Gemini_Generated_Image_gtxrzhgtxrzhgtxr" src="https://github.com/user-attachments/assets/e4bd92b7-62b8-487a-bfc3-2be599907215" />


### Reprodutor de Áudio (MPXPLAY)
O MPXPLAY é a escolha ideal para DOS. Ele suporta MP3, WAV, FLAC, navegação por diretórios e possui suporte a telas LCD seriais/paralelas.
Configure o arquivo `AUTOEXEC.BAT` do DOS para iniciar o MPXPLAY em modo automático apontando para a pasta de músicas da mídia Hi-MD:

```bat
@ECHO OFF
C:\MPXPLAY\MPXPLAY.EXE D:\MUSICAS\*.* -control
```

### Display Frontal (VFD / LCD Display)
Para exibir o nome da música e tempo decorrido sem monitor, instale um display de caractere (ex: LCD 16x2 ou VFD HD44780) no painel frontal ligado à porta serial (COM) ou paralela (LPT).
O MPXPLAY possui suporte nativo para enviar o ID3 Tag e nome do arquivo diretamente para displays LCD via plugin/configuração no `MPXPLAY.INI`.

### Reprodutor de Vídeo (QVPro / QuickView)
O QVPro gerencia a reprodução de vídeo (AVI, MPG) em DOS diretamente pelo frame buffer da placa de vídeo. Pode ser chamado via linha de comando ou integrado a um menu em lote (`MENU.BAT`).

---

## 4. Configurações de Software e Hardware

### 4.1. Configuração do Display no MPXPLAY.INI
O MPXPLAY inclui módulos internos de saída para controladores de display LCD/VFD clássicos (como o HD44780 ligado na porta paralela LPT1, ou displays seriais RS-232 em COM1/COM2).
Abra o arquivo `MPXPLAY.INI` na pasta do programa e edite/descomente a seção de LCD:

```ini
[LCD]
LCDtype=1            ; 1 = HD44780 (Porta Paralela), 2 = Display Serial (COM)
LCDport=0x378        ; Endereço da porta LPT1 (ou 0x3F8 para COM1)
LCDsize=2x16         ; Formato do display: 2 linhas por 16 caracteres (ou 4x20)
LCDdelay=5           ; Velocidade de rolagem (scroll) do texto em tela

; Definição das linhas do display:
LCDline1=%ARTIST% - %TITLE%   ; Exibe Artista e Nome da Música na Linha 1
LCDline2=%TIME% / %LENGTH%    ; Exibe Tempo decorrido / Duração total na Linha 2
```

### 4.2. Script de Boot Automático (AUTOEXEC.BAT)
Configure o `AUTOEXEC.BAT` na raiz do seu disco de boot (C:) para carregar o suporte à porta e disparar a execução do MPXPLAY assim que o MS-DOS inicializar.

```bat
@ECHO OFF
PROMPT $P$G
PATH C:\DOS;C:\MPXPLAY

REM Carrega o driver da placa de som (exemplo para Sound Blaster)
SET BLASTER=A220 I5 D1 T4

REM Executa o MPXPLAY apontando para a pasta de musicas na midia Hi-MD (D:)
REM -bl: Executa em loop continuo
REM -f0: Oculta a interface de tela cheia para otimizar processamento no DOS
MPXPLAY.EXE D:\MUSICAS\*.* -bl -f0
```

### 4.3. Esquema de Ligação Hardware (Painel Frontal)

Para conectar um display LCD alfanumérico padrão HD44780 (16x2 ou 20x4) diretamente à porta paralela DB25 (LPT1) do PC e fazê-lo funcionar com o MPXPLAY em modo de 8 bits, utilize a tabela e o esquema de soldagem abaixo.

*(Conexão da porta paralela ao LCD HD44780)*

**Tabela de Pinagem e Soldagem (DB25 para HD44780)**

<img width="312" height="320" alt="serialmsdos" src="https://github.com/user-attachments/assets/78b12625-cffb-4956-8dae-de2ea4f83318" />

exemple: https://www.bristolwatch.com/pport2/hd44780.htm


**How does a USB keyboard work?**

https://www.youtube.com/watch?v=wdgULBpRoXk


| Pino LCD HD44780 | Nome do Pino | Função | Conectar em (Origem) |
| :--- | :--- | :--- | :--- |
| 1 | VSS | Ground (0V) | GND da Fonte (Fio Preto) / Pino 18 do DB25 |
| 2 | VDD | Alimentação (+5V) | +5V da Fonte Molex (Fio Vermelho) |
| 3 | V0 / VE | Ajuste de Contraste | Pino Central (Wiper) de um Potenciômetro de 10kΩ |
| 4 | RS | Register Select | Pino 16 do conector DB25 (Init) |
| 5 | R/W | Read / Write | GND (Fio Preto - fixa o LCD em modo de escrita) |
| 6 | E / Enable | Enable Signal | Pino 17 do conector DB25 (Select Input) |
| 7 | D0 | Dado Bit 0 | Pino 2 do DB25 (Data 0) |
| 8 | D1 | Dado Bit 1 | Pino 3 do DB25 (Data 1) |
| 9 | D2 | Dado Bit 2 | Pino 4 do DB25 (Data 2) |
| 10 | D3 | Dado Bit 3 | Pino 5 do DB25 (Data 3) |
| 11 | D4 | Dado Bit 4 | Pino 6 do DB25 (Data 4) |
| 12 | D5 | Dado Bit 5 | Pino 7 do DB25 (Data 5) |
| 13 | D6 | Dado Bit 6 | Pino 8 do DB25 (Data 6) |
| 14 | D7 | Dado Bit 7 | Pino 9 do DB25 (Data 7) |
| 15 | BLA / LED+ | Anodo do Backlight (+5V) | +5V da Fonte (recomenda-se resistor de 100Ω em série) |
| 16 | BLK / LED- | Catodo do Backlight (GND) | GND da Fonte (Fio Preto) |

**Componentes Adicionais Necessários**
- **Potenciômetro de 10kΩ:** Conecte o pino esquerdo ao +5V, o pino direito ao GND, e o pino do meio ao Pino 3 (V0) do LCD. Sem ele, a tela ficará apagada ou cheia de blocos pretos.
- **Resistor de 100Ω (opcional, para Backlight):** Colocado em série no Pino 15 para evitar a queima dos LEDs de iluminação de fundo.
- **Terra Comum:** Certifique-se de soldar uma ponte entre os pinos 18 até 25 do DB25 e interligá-los com o GND da fonte de alimentação do PC e os pinos 1 e 5 do LCD.

**Ajuste Final no BIOS**
Na inicialização da placa-mãe (BIOS/Setup), configure o modo de operação da Porta Paralela (*Parallel Port Mode*) como **Standard**, **SPP** ou **Normal**. Evite os modos ECP ou EPP, pois eles podem causar interferência ou falhas de sincronismo na escrita contínua do MPXPLAY.

### 4.4. Chamada de Vídeo via QVPro
Caso você queira criar um menu simples para alternar entre música e vídeo (quando conectar um monitor via VGA/HDMI), crie um arquivo em lote `MENU.BAT`:

```bat
@ECHO OFF
CLS
ECHO =========================================
ECHO   CENTRAL MULTIMIDIA HI-MD MS-DOS
ECHO =========================================
ECHO 1. Tocar Musicas (MPXPLAY)
ECHO 2. Reproduzir Videos (QVPro)
ECHO 3. Sair para o DOS
ECHO =========================================
CHOICE /C:123 /N Escolha uma opcao: 

IF ERRORLEVEL 3 GOTO END
IF ERRORLEVEL 2 GOTO VIDEO
IF ERRORLEVEL 1 GOTO MUSIC

:MUSIC
C:\MPXPLAY\MPXPLAY.EXE D:\MUSICAS\*.* -bl
GOTO END

:VIDEO
C:\QVPRO\QV.EXE D:\VIDEOS\*.AVI
GOTO END

:END
```
