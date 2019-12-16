
# 在现有 VPC 上新建 EC2 (AWS CDK Python)

打开 app.py 修改 Account ID 为你的AWS Account ID, 要部署的 Region。这里因为是在现有 VPC 中部署，需要读取 VPC 信息，所以需要手工设置 Account 和 Region。  
```
env_cn = core.Environment(account="11111111", region="cn-northwest-1")
```
打开 cdk_vpc_ec2_stack.py 修改以下变量：  
```
vpc_id = "vpc-111111111"
ec2_type = "m5.xlarge"
key_name = "id_rsa"
linux_ami = ec2.GenericLinuxImage({
    "cn-northwest-1": "ami-0f62e91915e16cfc2",
    "eu-west-1": "ami-12345678"
})
```



To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk init`        Init cdk project
 * `cdk bootstrap`   Init cdk bootstrap
 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
