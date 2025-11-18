import pulumi
import pulumi_aws as aws

# Pulumi - Mais próximo do imperativo (mas ainda declarativo)
# Usando Python com lógica imperativa

def create_infrastructure():
    # Lógica imperativa dentro do código
    regions = ["us-east-1", "us-west-2"]
    instance_sizes = {"dev": "t3.micro", "prod": "t3.large"}
    
    instances = []
    
    # Loop imperativo para criar múltiplas instâncias
    for i, region in enumerate(regions):
        # Condição imperativa
        if region == "us-east-1":
            env = "dev"
        else:
            env = "prod"
            
        # Security Group
        sg = aws.ec2.SecurityGroup(f"web-sg-{i}",
            description=f"Security group for {env}",
            ingress=[
                {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]},
                {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]}
            ],
            opts=pulumi.ResourceOptions(provider=aws.Provider(f"aws-{region}", region=region))
        )
        
        # Lógica imperativa para escolher AMI
        if region == "us-east-1":
            ami = "ami-0c7217cdde317cfec"
        else:
            ami = "ami-0abcdef1234567890"
            
        # EC2 Instance
        instance = aws.ec2.Instance(f"web-{i}",
            ami=ami,
            instance_type=instance_sizes[env],
            vpc_security_group_ids=[sg.id],
            tags={"Name": f"WebServer-{env}-{i}"},
            opts=pulumi.ResourceOptions(provider=aws.Provider(f"aws-{region}", region=region))
        )
        
        instances.append(instance)
    
    return instances

# Chamada imperativa
infrastructure = create_infrastructure()

# Exports
pulumi.export("instance_ips", [instance.public_ip for instance in infrastructure])