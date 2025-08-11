tfc-cancel-pending
=================

Script to cancel pending runs on a Terraform Cloud workspace


Caution
-------

**Footgun Warning**: This software has no safety bumpers.  It is easy to shoot
yourself in the foot.  Be careful!


Install
-------

```bash
# Install dependencies using uv
uv sync
```


Usage
-----

### Using Make (recommended)

```bash
# Cancel pending runs
make cancel <organization> <workspace>

# Dry run (see what would be cancelled without actually cancelling)
make cancel-dry-run <organization> <workspace>

# Show help
make help
```

### Direct script usage

```bash
# Using uv run
uv run python tfc-cancel-pending.py <organization> <workspace> [--dry-run]

# Or make the script executable
chmod +x tfc-cancel-pending.py
./tfc-cancel-pending.py <organization> <workspace> [--dry-run]
```

If you already have the Terraform CLI authorized with Terraform
Cloud, `tfc-cancel-pending` will automatically read your TFC API token from the
Terraform CLI's credentials file.

Otherwise, you must populate environment variable `TFC_TOKEN` with your
Terraform Cloud API token.