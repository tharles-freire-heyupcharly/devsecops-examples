#!/bin/bash
# Script para converter SVG para PNG de alta qualidade usando ImageMagick

SVG_FILE="compliance-lifecycle-graphviz.svg"
OUTPUT_PNG="compliance-lifecycle-graphviz-hd.png"

echo "🔄 Convertendo SVG para PNG de alta qualidade..."

# Converter SVG para PNG com 300 DPI e largura de 4000px
magick -density 300 -background white -alpha remove -alpha off "$SVG_FILE" -resize 4000x "$OUTPUT_PNG"

if [ $? -eq 0 ]; then
    echo "✅ PNG de alta qualidade gerado: $OUTPUT_PNG"
    ls -lh "$OUTPUT_PNG"
    sips -g pixelWidth -g pixelHeight "$OUTPUT_PNG"
else
    echo "❌ Erro: ImageMagick não está instalado"
    echo "💡 Instale com: brew install imagemagick"
    echo ""
    echo "Alternativa: Use o arquivo SVG diretamente no PowerPoint"
    echo "   O SVG tem qualidade vetorial infinita!"
fi
