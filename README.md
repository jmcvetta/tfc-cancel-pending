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

```
./tfc-cancel-pending.py [--dry-run] ORGANIZATION WORKSPACE_NAME
```

If you already have the Terraform CLI authorized with Terraform
Cloud, `tfc-cancel-pending` will automatically read your TFC API token from the
Terraform CLI's credentials file.

Otherwise, you must populate environment variable `TFC_TOKEN` with your
Terraform Cloud API token.