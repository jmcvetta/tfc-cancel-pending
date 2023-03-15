#!/bin/env python3
import logging
import sys

import environs
import click
from terrasnek.api import TFC
import structlog


@click.command()
@click.argument("workspace_id")
@click.option("--organization", "-o", default="core-strengths-sandbox")
@click.option("--dry-run", default=False, is_flag=True)
def clear(workspace_id: str, organization: str, dry_run: bool):
    log = structlog.stdlib.get_logger()
    log = log.bind(dry_run=dry_run)
    # NOTE: Structlog renderer processors can be useful during development when
    #  logging large JSON or dict objects.
    # processors = [structlog.processors.JSONRenderer(indent=2, sort_keys=True)]
    # structlog.configure(processors=processors)

    env = environs.Env()
    try:
        tfc_token = env.str("TFC_TOKEN")
    except environs.EnvError:
        log.fatal("Environment variable TFC_TOKEN must be set")
        sys.exit(1)
    api = TFC(tfc_token)
    api.set_org(organization)
    log = log.bind(workspace_id=workspace_id, organization=organization)

    log.debug("Deleting all pending runs...")
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

    if not dry_run:
        for run_id in runs_to_discard:
            log.debug(f"Discard pending run", run_id=run_id)
            api.runs.cancel(run_id=run_id, payload={
                "comment": "Discarded by script tfc-clear-pending.py"
            })

    log.info("Deleted all pending runs", deleted_count=len(runs_to_discard))


if __name__ == "__main__":
    clear()
