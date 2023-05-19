tfc-cancel-pending
=================

Script to cancel pending runs on a Terraform Cloud workspace


Caution
-------

**Footgun Warning**: This software has no safety bumpers.  It is easy to shoot
yourself in the foot.  Be careful!


Install
-------

```
poetry install
```


Usage
-----

```bash
export TFC_TOKEN=your_terraform_cloud_token
./tfc-cancel-pending.py [--dry-run] --organization ORGANIZATION WORKSPACE_ID
```
