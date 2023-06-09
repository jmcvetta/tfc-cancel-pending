#!/bin/env python3
import json
import os.path
import sys
from typing import Optional

import click
import environs
import structlog
from structlog.stdlib import BoundLogger
from terrasnek.api import TFC


def read_token_from_credentials(log: BoundLogger) -> Optional[str]:
    """
    Read TFC token from TFC credentials file

    :return: Terraform Cloud API token
    """
    file_path: str = os.path.expanduser("~/.terraform.d/credentials.tfrc.json")

    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
            token: str = data['credentials']['app.terraform.io']['token']
            log.debug("Successfully read token from TFC credentials file")
            return token
    except FileNotFoundError:
        log.debug("Could not find TFC credentials file", file_path=file_path)
    except (KeyError, json.JSONDecodeError):
        log.warn("TFC credentials file was found, but does not contain expected format")
    except Exception as e:
        log.fatal(f"Unexpected error: {str(e)}")
        sys.exit(-1)


@click.command(help="Cancel pending runs on a Terraform Cloud workspace")
@click.argument("organization_name")
@click.argument("workspace_name")
@click.option("--dry-run", default=False, is_flag=True)
def main(workspace_name: str, organization_name: str, dry_run: bool) -> None:
    log = structlog.stdlib.get_logger()
    log = log.bind(dry_run=dry_run)
    # NOTE: Structlog renderer processors can be useful during development when
    #  logging large JSON or dict objects.
    # processors = [structlog.processors.JSONRenderer(indent=2, sort_keys=True)]
    # structlog.configure(processors=processors)

    tfc_token = read_token_from_credentials(log)
    if not tfc_token:
        env = environs.Env()
        try:
            tfc_token = env.str("TFC_TOKEN")
        except environs.EnvError:
            log.fatal("TFC credentials file not found and environment variable TFC_TOKEN not set")
            sys.exit(1)

    api = TFC(tfc_token)
    api.set_org(organization_name)
    log = log.bind(workspace_name=workspace_name, organization=organization_name)

    log.debug("Looking up workspace name...")
    result_data = api.workspaces.list(search={"name": workspace_name})['data']
    workspace_id = None
    for ws in result_data:
        if ws['attributes']['name'] == workspace_name:
            workspace_id = ws['id']
            break
    if not workspace_id:
        log.fatal("Workspace not found")
        sys.exit(1)
    log = log.bind(workspace_id=workspace_id)
    log.debug("Found workspace")

    log.debug("Querying pending runs...")
    filter_pending = {
        "keys": ["status"],
        "value": "pending",
    }
    result = api.runs.list(workspace_id=workspace_id, filters=[filter_pending])

    runs_to_discard = []
    page = 1
    while True:
        result = api.runs.list(
            workspace_id=workspace_id, filters=[filter_pending], page=page
        )
        run_list = result["data"]
        if len(run_list) == 0:
            break
        for run in run_list:
            run_id = run["id"]
            run_status = run["attributes"]["status"]
            assert run_status == "pending" # Sanity check
            runs_to_discard.append(run_id)
        page += 1

    log.debug("Deleting all pending runs...", count=len(runs_to_discard))
    if not dry_run:
        for run_id in runs_to_discard:
            log.debug(f"Discard pending run", run_id=run_id)
            api.runs.cancel(run_id=run_id, payload={
                "comment": "Discarded by script tfc-cancel-pending.py"
            })

    log.info("Deleted all pending runs", count=len(runs_to_discard))


if __name__ == "__main__":
    main()
