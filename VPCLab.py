#Creating VPC, Gateway, Tables and Subnets using Boto3 SDK

import boto3
import time

#Create VPC/When creating VPC's using boto3 you need to creat and ec2 resource or client. im going with client for this Hands on
ec2 = boto3.client('ec2')
vpc_name = 'Abbas-vpc'

#Line 11 - 32 Creating condition for boto3 to check if VPC name already exists so we dont make duplicates for the duration of the hands on
response = ec2.describe_vpcs(
    Filters = [{'Name':'tag:Name', 'Values': [vpc_name]}]
    )
vpcs = response.get('Vpcs', [])

if vpcs:
    vpc_id = vpcs[0]['VpcId']
    print (f"VPC '{vpc_name}' with '{vpc_id}' ID has already been created")
else:    
#Line 21 is the method which creates the VPC including the CidrBlock for your choosing
    vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    
    #line 24 is the method to get the VPC ID
    vpc_id = vpc_response['Vpc']['VpcId']
    
    #i put the 8 seconds to give us a bit of time. i got an error the first time since it takes a couple seconds for the VPC to be created
    time.sleep(8)
    
    #Line 30 will create the vpc name and add it to the tags
    ec2.create_tags(Resources=[vpc_id], Tags=[{'Key':'Name', 'Value': vpc_name}])
    
    print (f"VPC '{vpc_name}' with '{vpc_id}' ID has been created")

#create an internet gateway. Using the same conditional i used for the VPC to the IG as well.

ig_name = 'ig-abbas-vpc'
response = ec2.describe_internet_gateways(
    Filters = [{'Name':'tag:Name', 'Values': [ig_name]}]
    )
internet_gateways = response.get('InternetGateways', [])

if internet_gateways:
    ig_id = internet_gateways[0]['InternetGatewayId']
    print (f"Internet Gateway '{ig_name}' with '{ig_id}' ID has already been created")
else:    

    ig_response = ec2.create_internet_gateway()
    ig_id = ig_response['InternetGateway']['InternetGatewayId']
    ec2.create_tags(Resources=[ig_id], Tags=[{'Key':'Name', 'Value': ig_name}])
    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=ig_id)
    print (f"Internet Gateway '{ig_name}' with '{ig_id}' ID has  been created")


#Creating a routing table and public route
rt_response = ec2.create_route_table(VpcId=vpc_id)
rt_id = rt_response['RouteTable']['RouteTableId']
route = ec2.create_route(
    RouteTableId=rt_id,
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ig_id,
    )
print (f"Route Table with '{rt_id}' ID has  been created")


#create 3 Subnets
subnet_1 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24', AvailabilityZone='us-east-1a')
subnet_2 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.2.0/24', AvailabilityZone='us-east-1b')
subnet_3 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.3.0/24', AvailabilityZone='us-east-1c')

print(f"Subnet_1 ID = '{subnet_1['Subnet']['SubnetId']}', Subnet_2 ID = '{subnet_2['Subnet']['SubnetId']}',Subnet_3 ID = '{subnet_3['Subnet']['SubnetId']}' has been created.")
