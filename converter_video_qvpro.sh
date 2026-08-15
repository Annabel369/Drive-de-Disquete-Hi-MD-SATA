#!/bin/bash
# Converte vídeos modernos (.mp4) para o formato compatível com QVPro no MS-DOS

shopt -s nullglob nocaseglob
for video in *.mp4; do
    # Usa o mesmo nome do video, mas com a extensão .mpg
    BASE_NAME="${video%.*}"
    TARGET="${BASE_NAME}.mpg"
    
    echo "=========================================================="
    echo "Iniciando conversão de: $video"
    echo "O arquivo será salvo como: $TARGET"
    echo "=========================================================="
    
    # Roda o FFmpeg com configurações otimizadas para QVPro no MS-DOS
    # scale=320:240, mpeg1video 400kbps, audio mp2 128kbps 22050Hz
    ffmpeg -y -i "$video" -vf scale=320:240 -r 24 -c:v mpeg1video -b:v 400k -c:a mp2 -b:a 128k -ar 22050 "$TARGET"
    
    echo "✅ Conversão finalizada: $TARGET\n"
done

echo "🎉 Todas as conversões foram concluídas!"
