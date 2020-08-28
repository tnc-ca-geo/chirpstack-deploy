# ChirpStack deployment

This repository contains tools to deploy ChirpStack for TNC. It is somewhat
cumbersome since ChirpStack provides an Ansible playbook containing roles 
not managed by Ansible-Galaxy. For this reason, we added
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

###
