#!/bin/bash
# Converte imagens modernas para BMP compatível com MS-DOS (640x480, 256 cores)
# Uso: ./converter_img_dos.sh "foto.jpg" "foto_dos"

if [ $# -lt 2 ]; then
    echo "Uso: $0 \"<imagem de entrada>\" <nome de saida sem extensao>"
    echo "Exemplo: $0 \"capa.jpg\" CAPA"
    exit 1
fi

INPUT="$1"
OUTPUT_NAME="$2"
OUTPUT="${OUTPUT_NAME}.BMP"

if [ ! -f "$INPUT" ]; then
    echo "Erro: arquivo '$INPUT' não encontrado."
    exit 1
fi

if [ -f "$OUTPUT" ]; then
    echo "Aviso: '$OUTPUT' já existe. Nada foi feito."
    exit 0
fi

echo "Convertendo '$INPUT' -> '$OUTPUT' ..."

convert "$INPUT" \
    -resize 640x480! \
    -dither FloydSteinberg \
    -colors 256 \
    -type Palette \
    -compress None \
    BMP3:"$OUTPUT"

if [ $? -eq 0 ]; then
    echo "✅ Pronto! Arquivo criado: $OUTPUT"
else
    echo "❌ Erro na conversão."
    exit 1
fi
