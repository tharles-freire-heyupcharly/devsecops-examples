#!/bin/bash

# Abordagem Imperativa - AWS CLI
# "COMO FAZER passo a passo"

echo "=== INICIANDO DEPLOY IMPERATIVO ==="

# Variáveis
REGION="us-east-1"
AZ="us-east-1a"
KEY_NAME="my-key-pair"
AMI_ID="ami-0c7217cdde317cfec"  # Ubuntu 22.04
INSTANCE_TYPE="t3.micro"

# PASSO 1: Criar Security Group
echo "PASSO 1: Criando Security Group..."
SG_ID=$(aws ec2 create-security-group \
    --group-name "web-server-sg-$(date +%s)" \
    --description "Security group for web server" \
    --region $REGION \
    --query 'GroupId' \
    --output text)

if [ $? -eq 0 ]; then
    echo "✅ Security Group criado: $SG_ID"
else
    echo "❌ Erro ao criar Security Group"
    exit 1
fi

# PASSO 2: Configurar regras do Security Group - HTTP
echo "PASSO 2: Adicionando regra HTTP..."
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0 \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Regra HTTP adicionada"
else
    echo "❌ Erro ao adicionar regra HTTP"
fi

# PASSO 3: Configurar regras do Security Group - SSH
echo "PASSO 3: Adicionando regra SSH..."
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0 \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Regra SSH adicionada"
else
    echo "❌ Erro ao adicionar regra SSH"
fi

# PASSO 4: Criar volume EBS
echo "PASSO 4: Criando volume EBS..."
VOLUME_ID=$(aws ec2 create-volume \
    --availability-zone $AZ \
    --size 20 \
    --volume-type gp3 \
    --iops 3000 \
    --throughput 125 \
    --encrypted \
    --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=WebServer-Storage},{Key=Environment,Value=Development}]' \
    --region $REGION \
    --query 'VolumeId' \
    --output text)

if [ $? -eq 0 ]; then
    echo "✅ Volume EBS criado: $VOLUME_ID"
else
    echo "❌ Erro ao criar volume EBS"
    exit 1
fi

# PASSO 5: Aguardar volume ficar disponível
echo "PASSO 5: Aguardando volume ficar disponível..."
aws ec2 wait volume-available \
    --volume-ids $VOLUME_ID \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Volume disponível"
else
    echo "❌ Timeout aguardando volume"
    exit 1
fi

# PASSO 6: Criar instância EC2
echo "PASSO 6: Criando instância EC2..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SG_ID \
    --placement "AvailabilityZone=$AZ" \
    --tag-specifications 'ResourceType=instance,
    Tags=[{Key=Name,Value=WebServer-Imperative},
    {Key=Environment,Value=Development}]' \
    --region $REGION \
    --query 'Instances[0].InstanceId' \
    --output text)

if [ $? -eq 0 ]; then
    echo "✅ Instância EC2 criada: $INSTANCE_ID"
else
    echo "❌ Erro ao criar instância EC2"
    exit 1
fi

# PASSO 7: Aguardar instância ficar running
echo "PASSO 7: Aguardando instância ficar running..."
aws ec2 wait instance-running \
    --instance-ids $INSTANCE_ID \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Instância running"
else
    echo "❌ Timeout aguardando instância"
    exit 1
fi

# PASSO 8: Anexar volume EBS à instância
echo "PASSO 8: Anexando volume EBS à instância..."
aws ec2 attach-volume \
    --volume-id $VOLUME_ID \
    --instance-id $INSTANCE_ID \
    --device /dev/xvdf \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Volume anexado"
else
    echo "❌ Erro ao anexar volume"
fi

# PASSO 9: Aguardar volume estar anexado
echo "PASSO 9: Aguardando volume estar anexado..."
aws ec2 wait volume-in-use \
    --volume-ids $VOLUME_ID \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Volume em uso"
else
    echo "❌ Timeout aguardando anexação"
fi

# PASSO 10: Obter IP público
echo "PASSO 10: Obtendo informações da instância..."
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

PUBLIC_DNS=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION \
    --query 'Reservations[0].Instances[0].PublicDnsName' \
    --output text)

# RESULTADOS FINAIS
echo ""
echo "=== DEPLOY IMPERATIVO CONCLUÍDO ==="
echo "🆔 Instance ID: $INSTANCE_ID"
echo "🌐 Public IP: $PUBLIC_IP"
echo "🔗 Public DNS: $PUBLIC_DNS"
echo "💾 Volume ID: $VOLUME_ID"
echo "🛡️ Security Group: $SG_ID"
echo ""
echo "📝 Para conectar: ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP"
echo ""

# Salvar IDs para cleanup posterior
echo "INSTANCE_ID=$INSTANCE_ID" > infrastructure-ids.txt
echo "VOLUME_ID=$VOLUME_ID" >> infrastructure-ids.txt
echo "SG_ID=$SG_ID" >> infrastructure-ids.txt
echo "✅ IDs salvos em infrastructure-ids.txt"