import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';

export class InfrastructureStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // CDK - Sintaxe imperativa (mas resultado declarativo)
    
    // Lógica imperativa para criar recursos
    const environments = ['dev', 'staging', 'prod'];
    const instanceTypes = {
      dev: 't3.micro',
      staging: 't3.small', 
      prod: 't3.large'
    };
    
    // Loop imperativo
    environments.forEach((env, index) => {
      // Condições imperativas
      if (env === 'prod') {
        this.createProductionInfrastructure(env, instanceTypes[env]);
      } else {
        this.createDevelopmentInfrastructure(env, instanceTypes[env]);
      }
    });
  }
  
  // Método imperativo para produção
  private createProductionInfrastructure(env: string, instanceType: string) {
    // VPC
    const vpc = new ec2.Vpc(this, `${env}-vpc`, {
      maxAzs: 3,
      natGateways: 2, // Produção precisa de redundância
    });
    
    // Security Group com regras específicas para prod
    const sg = new ec2.SecurityGroup(this, `${env}-sg`, {
      vpc,
      description: `Security group for ${env}`,
      allowAllOutbound: true
    });
    
    // Regras imperativas baseadas no ambiente
    sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(443), 'HTTPS');
    sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'HTTP');
    
    // Instância com configuração de produção
    const instance = new ec2.Instance(this, `${env}-instance`, {
      vpc,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE),
      machineImage: ec2.MachineImage.latestAmazonLinux(),
      securityGroup: sg,
      keyName: 'prod-key'
    });
    
    // EBS Volume para produção
    const volume = new ec2.Volume(this, `${env}-volume`, {
      availabilityZone: instance.instanceAvailabilityZone,
      size: cdk.Size.gibibytes(100), // Produção precisa mais espaço
      volumeType: ec2.EbsDeviceVolumeType.GP3,
      encrypted: true
    });
    
    // Anexar volume
    new ec2.CfnVolumeAttachment(this, `${env}-attachment`, {
      instanceId: instance.instanceId,
      volumeId: volume.volumeId,
      device: '/dev/xvdf'
    });
  }
  
  // Método imperativo para desenvolvimento
  private createDevelopmentInfrastructure(env: string, instanceType: string) {
    // VPC mais simples para dev
    const vpc = new ec2.Vpc(this, `${env}-vpc`, {
      maxAzs: 1,
      natGateways: 0, // Dev não precisa de NAT Gateway
    });
    
    // Security Group mais permissivo para dev
    const sg = new ec2.SecurityGroup(this, `${env}-sg`, {
      vpc,
      description: `Security group for ${env}`,
      allowAllOutbound: true
    });
    
    sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), 'SSH');
    sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'HTTP');
    
    // Instância menor para dev
    const instance = new ec2.Instance(this, `${env}-instance`, {
      vpc,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      machineImage: ec2.MachineImage.latestAmazonLinux(),
      securityGroup: sg,
      keyName: 'dev-key'
    });
    
    // Volume menor para dev
    const volume = new ec2.Volume(this, `${env}-volume`, {
      availabilityZone: instance.instanceAvailabilityZone,
      size: cdk.Size.gibibytes(20),
      volumeType: ec2.EbsDeviceVolumeType.GP3
    });
  }
}