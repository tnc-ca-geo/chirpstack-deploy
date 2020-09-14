# ChirpStack deployment

This repository contains tools to deploy ChirpStack for TNC. It is somewhat
cumbersome since ChirpStack provides an Ansible playbook containing roles 
not managed by Ansible-Galaxy. For this reason, we added a fork of 
https://github.com/brocaar/chirpstack-ansible-playbook as a submodule
which is certainly not very elegant.

We copied (and modified) the original playbook referring to roles in the
sub-module. The sub-module itself should not be touched.

This repo also contains code to backup ChirpStack settings on a regular basis.

## Getting started

### Clone the repo

```
git clone --recurse-submodules https://github.com/tnc-ca-geo/chirpstack-deploy
```

### Install dependencies

Ideally create and activate a Python 3 based virtual environment. And install 
the dependencies from the requirements.txt file, like:

```
pip install -r requirements.txt
```

Also install missing Ansible modules like:

```
ansible-galaxy install -r requirements.yml
```

### Create EC2 instance using tnc-ca-geo/tnc_machines

Make sure to use the correct security group, a sensitive choice would be ...

```
aws-vault exec falk -- fab create-ec2 --ubuntu bionic --security-group "chirpstack" --instance-type "m4.large" --block-device 40 basics
```

Add a name to the new instance in order to avoid unintended termination.

### Point chirpstack.codefornature.org to the public IP address of the new instance

The domain is managed by hover.com. Be aware of the fact that the public 
IP will be lost if an EC2 instance is halted. Use Elastic IPs to persist an address.
A normal reboot will not affect the IP assignment. 

