import * as cdk from 'aws-cdk-lib';
import type { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecr from 'aws-cdk-lib/aws-ecr';

export class WakarunRepositoryStack extends cdk.Stack {
	public readonly frontendAppRepository: ecr.IRepository;
	public readonly backendAppRepository: ecr.IRepository;
	public readonly backendWebRepository: ecr.IRepository;
	constructor(scope: Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		this.frontendAppRepository = new ecr.Repository(
			this,
			'WakarunFrontendAppRepository',
			{
				repositoryName: 'wakarun/frontend_app',
			},
		);

		this.backendAppRepository = new ecr.Repository(
			this,
			'WakarunBackendAppRepository',
			{
				repositoryName: 'wakarun/backend_app',
			},
		);

		this.backendWebRepository = new ecr.Repository(
			this,
			'WakarunBackendWebRepository',
			{
				repositoryName: 'wakarun/backend_web',
			},
		);
	}
}
