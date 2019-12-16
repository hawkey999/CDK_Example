from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

vpc_id = "vpc-111111"
ec2_type = "m5.xlarge"
key_name = "id_rsa"
linux_ami = ec2.GenericLinuxImage({
    "cn-northwest-1": "ami-0f62e91915e16cfc2",
    "eu-west-1": "ami-12345678"
})


class CdkVpcEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        vpc = ec2.Vpc.from_lookup(self, "VPC",
                                  vpc_id=vpc_id,
                                  )

        my_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                              vpc=vpc,
                                              description="Allow ssh access to ec2 instances",
                                              allow_all_outbound=True
                                              )
        my_security_group.add_ingress_rule(ec2.Peer.any_ipv4(),
                                           ec2.Port.tcp(22),
                                           "allow ssh access from internet")

        host = ec2.Instance(self, "myEC2",
                            instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                            machine_image=linux_ami,
                            vpc=vpc,
                            key_name=key_name,
                            security_group=my_security_group,
                            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
                            )
