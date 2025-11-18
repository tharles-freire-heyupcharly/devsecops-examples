#!/bin/bash

# Abordagem Imperativa - CLEANUP
# "COMO DESTRUIR passo a passo"

echo "=== INICIANDO CLEANUP IMPERATIVO ==="

REGION="us-east-1"

# Verificar se arquivo de IDs existe
if [ ! -f "infrastructure-ids.txt" ]; then
    echo "❌ Arquivo infrastructure-ids.txt não encontrado!"
    echo "Por favor, forneça os IDs manualmente ou execute o deploy primeiro."
    exit 1
fi

# Carregar IDs
source infrastructure-ids.txt

echo "🔍 IDs encontrados:"
echo "   Instance: $INSTANCE_ID"
echo "   Volume: $VOLUME_ID"
echo "   Security Group: $SG_ID"
echo ""

# PASSO 1: Parar instância
echo "PASSO 1: Parando instância EC2..."
aws ec2 stop-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION

# PASSO 2: Aguardar instância parar
echo "PASSO 2: Aguardando instância parar..."
aws ec2 wait instance-stopped \
    --instance-ids $INSTANCE_ID \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Instância parada"
else
    echo "❌ Timeout aguardando parada"
fi

# PASSO 3: Desanexar volume EBS
echo "PASSO 3: Desanexando volume EBS..."
aws ec2 detach-volume \
    --volume-id $VOLUME_ID \
    --region $REGION

# PASSO 4: Aguardar volume ser desanexado
echo "PASSO 4: Aguardando volume ser desanexado..."
aws ec2 wait volume-available \
    --volume-ids $VOLUME_ID \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Volume desanexado"
else
    echo "❌ Timeout aguardando desanexação"
fi

# PASSO 5: Terminar instância
echo "PASSO 5: Terminando instância EC2..."
aws ec2 terminate-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION

# PASSO 6: Aguardar instância ser terminada
echo "PASSO 6: Aguardando instância ser terminada..."
aws ec2 wait instance-terminated \
    --instance-ids $INSTANCE_ID \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Instância terminada"
else
    echo "❌ Timeout aguardando terminação"
fi

# PASSO 7: Deletar volume EBS
echo "PASSO 7: Deletando volume EBS..."
aws ec2 delete-volume \
    --volume-id $VOLUME_ID \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Volume deletado"
else
    echo "❌ Erro ao deletar volume"
fi

# PASSO 8: Deletar Security Group
echo "PASSO 8: Deletando Security Group..."
# Aguardar um pouco para garantir que a instância foi completamente removida
sleep 30

aws ec2 delete-security-group \
    --group-id $SG_ID \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Security Group deletado"
else
    echo "❌ Erro ao deletar Security Group (pode estar em uso)"
fi

# PASSO 9: Limpar arquivo de IDs
echo "PASSO 9: Limpando arquivos temporários..."
rm -f infrastructure-ids.txt

echo ""
echo "=== CLEANUP IMPERATIVO CONCLUÍDO ==="
echo "🗑️ Todos os recursos foram removidos"