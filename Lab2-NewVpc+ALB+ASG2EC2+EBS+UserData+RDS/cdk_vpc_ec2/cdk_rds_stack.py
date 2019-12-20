from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds

db_master_username = "admin"
db_master_user_password = "password"


class CdkRdsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, asg_security_groups, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creat DB Low Level API - MySQL M-AZs
        db_security_group = ec2.CfnSecurityGroup(self, "dbSG",
                                                 group_description="All EC2 access DB",
                                                 group_name="DB_SG",
                                                 vpc_id=vpc.vpc_id
                                                 )

        for asg_sg in asg_security_groups:
            ec2.CfnSecurityGroupIngress(self, "SG_ingress",
                                        ip_protocol="tcp",
                                        description="ASG EC2 access DB",
                                        to_port=3306,
                                        from_port=3306,
                                        group_id=db_security_group.attr_group_id,
                                        source_security_group_id=asg_sg.security_group_id
                                        )

        subnet_ids = []
        for i in vpc.isolated_subnets:
            subnet_ids.append(i.subnet_id)

        db_subnet_group = rds.CfnDBSubnetGroup(self, "db_subnet",
                                               db_subnet_group_description="DB_subnet",
                                               db_subnet_group_name="db_subnet",
                                               subnet_ids=subnet_ids)
        db_mysql = rds.CfnDBInstance(self, "MyDB",
                                     db_name="mysqldb",
                                     db_instance_class="db.t2.small",
                                     allocated_storage="100",
                                     storage_type="gp2",
                                     engine="MySQL",
                                     engine_version="5.7.22",
                                     master_username=db_master_username,
                                     master_user_password=db_master_user_password,
                                     multi_az=True,
                                     vpc_security_groups=[
                                         db_security_group.attr_group_id],
                                     db_subnet_group_name=db_subnet_group.db_subnet_group_name,
                                     backup_retention_period=7,
                                     allow_major_version_upgrade=False,
                                     enable_cloudwatch_logs_exports=[
                                         "audit", "error", "general", "slowquery"],
                                     delete_automated_backups=False
                                     )
        db_mysql.add_depends_on(db_subnet_group)
        db_mysql.add_depends_on(db_security_group)

        # Create Aurora/RDS with High Level API, but it doesn't support China region's SecretManager yet
        # db = rds.DatabaseCluster(self, "MyAurora",
        #                          default_database_name="MyAurora",
        #                          engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
        #                          master_user=rds.Login(username="admin"),
        #                          instance_props=rds.InstanceProps(
        #                              vpc=vpc,
        #                              vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
        #                              instance_type=ec2.InstanceType(instance_type_identifier="t2.small")
        #                          )
        #                          )
        # db.connections.allow_default_port_from(asg, "EC2 Autoscaling Group access DB")

        # Create AuroraDB doestn't work in China Region
        # db_aurora_cluster = rds.CfnDBCluster(self, "AuroraDB",
        #                                      engine="aurora-mysql",
        #                                      engine_version="5.7.12",
        #                                      engine_mode="provisioned",
        #                                      database_name="myDBAurora",
        #                                      master_username=db_master_username,
        #                                      master_user_password=db_master_user_password,
        #                                      vpc_security_group_ids=[db_security_group.attr_group_id],
        #                                      db_subnet_group_name=db_subnet_group.db_subnet_group_name,
        #                                      db_cluster_parameter_group_name="default.aurora-mysql5.7",
        #                                      backup_retention_period=7
        #                                      )
        # db_aurora_cluster.add_depends_on(db_subnet_group)
        # db_aurora_cluster.add_depends_on(db_security_group)
        # Check all engine_version with aws cli command:
        # aws rds describe-db-engine-versions --engine aurora-mysql --query "DBEngineVersions[].EngineVersion"
        # engine_mode = provisioned, serverless, parallelquery, global, or multimaster
        # engine = aurora (MySQL5.6), aurora-mysql (MySQL5.7), aurora-postgresql
        # db_security_groups is old and should use vpc_security_groups

        # db_aurora_instance1 = rds.CfnDBInstance(self, "AuroraInstance1",
        #                                         db_cluster_identifier=db_aurora_cluster.db_cluster_identifier,
        #                                         db_instance_class="db.t2.small",
        #                                         engine="aurora-mysql",
        #                                         engine_version="5.7.12",
        #                                         db_parameter_group_name="default.aurora-mysql5.7",
        #                                         db_subnet_group_name=db_subnet_group.db_subnet_group_name,
        #                                         allow_major_version_upgrade=False,
        #                                         # allocated_storage="10",  # ??? why ???
        #                                         # storage_type="io1",  # ??? why ???
        #                                         # master_username=db_master_username,  # ??? why ???
        #                                         # master_user_password=db_master_user_password,  # ??? why ???
        #                                         delete_automated_backups=False
        #                                         )
        # db_aurora_instance1.add_depends_on(db_aurora_cluster)
        #
