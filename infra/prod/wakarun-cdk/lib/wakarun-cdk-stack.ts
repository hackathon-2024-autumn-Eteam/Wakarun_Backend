import * as cdk from 'aws-cdk-lib';
import type { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as rds from 'aws-cdk-lib/aws-rds';
import type * as ecr from 'aws-cdk-lib/aws-ecr';
import * as ecsPatterns from 'aws-cdk-lib/aws-ecs-patterns';
import { PolicyStatement } from 'aws-cdk-lib/aws-iam';

interface WakarunCdkProps extends cdk.StackProps {
	webRepo: ecr.IRepository;
	appRepo: ecr.IRepository;
	frontRepo: ecr.IRepository;
}

export class WakarunCdkStack extends cdk.Stack {
	constructor(scope: Construct, id: string, props: WakarunCdkProps) {
		super(scope, id, props);

		// VPC
		const vpc = new ec2.Vpc(this, 'Vpc', {
			ipAddresses: ec2.IpAddresses.cidr('172.17.0.0/16'),
			availabilityZones: ['ap-northeast-1a', 'ap-northeast-1c'],
			enableDnsHostnames: true,
			enableDnsSupport: true,
			natGateways: 0,
			natGatewaySubnets: {
				availabilityZones: ['ap-northeast-1a'],
				subnetType: ec2.SubnetType.PUBLIC,
			},
			subnetConfiguration: [
				{
					cidrMask: 24,
					name: 'ingress',
					subnetType: ec2.SubnetType.PUBLIC,
				},
				{
					cidrMask: 24,
					name: 'front',
					subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
				},
				{
					cidrMask: 24,
					name: 'application',
					subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
				},
				{
					cidrMask: 28,
					name: 'rds',
					subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
				},
				{
					cidrMask: 24,
					name: 'interfaceEndPoint',
					subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
				},
			],
			vpnGateway: false,
		});

		// VPC endpoint
		const interfaceEndPointSubnets: ec2.SubnetSelection = {
			subnetGroupName: 'interfaceEndPoint',
		};
		vpc.addInterfaceEndpoint('ecr_dkr_endpoint', {
			service: ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
			subnets: interfaceEndPointSubnets,
		});

		vpc.addInterfaceEndpoint('ecr_api_endpoint', {
			service: ec2.InterfaceVpcEndpointAwsService.ECR,
			subnets: interfaceEndPointSubnets,
		});
		vpc.addInterfaceEndpoint('ssm_message', {
			service: ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES,
			subnets: interfaceEndPointSubnets,
		});

		vpc.addInterfaceEndpoint('secrets_manager', {
			service: ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
			subnets: interfaceEndPointSubnets,
		});

		vpc.addGatewayEndpoint('s3_endpoint', {
			service: ec2.GatewayVpcEndpointAwsService.S3,
		});

		const ecsSG = new ec2.SecurityGroup(this, 'ecsSg', {
			vpc,
		});
		const rdsSG = new ec2.SecurityGroup(this, 'rdsSg', {
			vpc,
			allowAllOutbound: true,
		});

		rdsSG.connections.allowFrom(ecsSG, ec2.Port.tcp(3306), 'Ingress from ECS');

		//rds
		const wakarunDbSubnets: ec2.SubnetSelection = {
			subnetGroupName: 'rds',
		};

		const wakarunDbsubnetGroup = new rds.SubnetGroup(
			this,
			'wakarunDbSubnetGroup',
			{
				description: 'subnet group for wakarun db',
				vpc: vpc,
				vpcSubnets: wakarunDbSubnets,
			},
		);

		const rdsUser = 'wakarun';
		const rdsCredentials: rds.Credentials =
			rds.Credentials.fromGeneratedSecret(rdsUser);

		const wakarunDbInstance = new rds.DatabaseInstance(
			this,
			'wakarunInstance',
			{
				databaseName: 'wakarunDB',
				credentials: rdsCredentials,
				engine: rds.DatabaseInstanceEngine.mysql({
					version: rds.MysqlEngineVersion.VER_8_0_39,
				}),
				vpc,
				storageType: rds.StorageType.GP2,
				subnetGroup: wakarunDbsubnetGroup,
				securityGroups: [rdsSG],
			},
		);

		// biome-ignore lint/style/noNonNullAssertion: <explanation>
		const secretManager = wakarunDbInstance.secret!;

		// ECS task definition for backend
		const backendTaskDefinition = new ecs.FargateTaskDefinition(
			this,
			'BackendTaskDef',
			{
				cpu: 512,
				memoryLimitMiB: 1024,
				family: 'WakarunBackTaskDefinition',
				runtimePlatform: {
					cpuArchitecture: ecs.CpuArchitecture.ARM64,
					operatingSystemFamily: ecs.OperatingSystemFamily.LINUX,
				},
			},
		);

		backendTaskDefinition.addContainer('web', {
			image: ecs.ContainerImage.fromEcrRepository(props.webRepo, 'v0.0.1'),
			portMappings: [
				{
					containerPort: 80,
					hostPort: 80,
				},
			],
			environment: {
				ACCESS_LOG_LOCATION: '/dev/stdout',
				PROXY_PASS_HTTP: 'http://localhost:8000',
			},
		});

		backendTaskDefinition.addContainer('app', {
			image: ecs.ContainerImage.fromEcrRepository(props.appRepo, 'v0.0.6'),
			portMappings: [
				{
					containerPort: 8000,
					hostPort: 8000,
				},
			],
			environment: {
				ALLOWED_HOST: '*',
				DB_PORT: wakarunDbInstance.dbInstanceEndpointPort,
			},
			secrets: {
				DB_NAME: ecs.Secret.fromSecretsManager(secretManager, 'dbname'),
				DB_USER: ecs.Secret.fromSecretsManager(secretManager, 'username'),
				DB_PASSWORD: ecs.Secret.fromSecretsManager(secretManager, 'password'),
				DB_HOST: ecs.Secret.fromSecretsManager(secretManager, 'host'),
			},
		});

		backendTaskDefinition.addToExecutionRolePolicy(
			new PolicyStatement({
				actions: ['secretsmanager:GetSecretValue', 'kms:Decrypt'],
				resources: ['*'],
			}),
		);

		backendTaskDefinition.addToTaskRolePolicy(
			new PolicyStatement({
				actions: ['secretsmanager:GetSecretValue', 'kms:Decrypt'],
				resources: ['*'],
			}),
		);

		// ECS Serice for backend
		const taskSubnets: ec2.SubnetSelection = {
			subnetGroupName: 'application',
		};

		const loadBarancedFargateService =
			new ecsPatterns.ApplicationLoadBalancedFargateService(
				this,
				'LBFargateService',
				{
					assignPublicIp: true,
					cpu: 512,
					loadBalancerName: 'wakarunEcsLB',
					enableExecuteCommand: true,
					memoryLimitMiB: 1024,
					runtimePlatform: {
						cpuArchitecture: ecs.CpuArchitecture.ARM64,
						operatingSystemFamily: ecs.OperatingSystemFamily.LINUX,
					},
					serviceName: 'wakarunEcsService',
					taskDefinition: backendTaskDefinition,
					taskSubnets: taskSubnets,
					securityGroups: [ecsSG],
					vpc: vpc,
				},
			);
		loadBarancedFargateService.node.addDependency(wakarunDbInstance);

		// TaskDefinition for front app
		const frontendTaskDefinition = new ecs.FargateTaskDefinition(
			this,
			'FrontTaskDef',
			{
				cpu: 512,
				memoryLimitMiB: 1024,
				family: 'WakarunFrontTaskDefinition',
				runtimePlatform: {
					cpuArchitecture: ecs.CpuArchitecture.ARM64,
					operatingSystemFamily: ecs.OperatingSystemFamily.LINUX,
				},
			},
		);

		frontendTaskDefinition.addContainer('front', {
			image: ecs.ContainerImage.fromEcrRepository(props.frontRepo, 'v0.0.1'),
			portMappings: [
				{
					containerPort: 3000,
					hostPort: 3000,
				},
			],
		});

		// ECS Serice for frontend
		const frontTaskSubnets: ec2.SubnetSelection = {
			subnetGroupName: 'front',
		};

		const frontLoadBarancedFargateService =
			new ecsPatterns.ApplicationLoadBalancedFargateService(
				this,
				'FrontLBFargateService',
				{
					assignPublicIp: true,
					cpu: 512,
					enableExecuteCommand: true,
					loadBalancerName: 'frontWakarunEcsLB',
					memoryLimitMiB: 1024,
					runtimePlatform: {
						cpuArchitecture: ecs.CpuArchitecture.ARM64,
						operatingSystemFamily: ecs.OperatingSystemFamily.LINUX,
					},

					taskDefinition: frontendTaskDefinition,
					taskSubnets: frontTaskSubnets,
					vpc: vpc,
				},
			);
	}
}
