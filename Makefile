.PHONY: cancel
cancel:
	@if [ -z "$(ORG)" ] || [ -z "$(WORKSPACE)" ]; then \
		echo "Usage: make cancel ORG=<organization> WORKSPACE=<workspace>"; \
		echo ""; \
		echo "Example:"; \
		echo "  make cancel ORG=my-org WORKSPACE=my-workspace"; \
		exit 1; \
	fi
	uv run python tfc-cancel-pending.py $(ORG) $(WORKSPACE)

.PHONY: cancel-dry-run
cancel-dry-run:
	@if [ -z "$(ORG)" ] || [ -z "$(WORKSPACE)" ]; then \
		echo "Usage: make cancel-dry-run ORG=<organization> WORKSPACE=<workspace>"; \
		echo ""; \
		echo "Example:"; \
		echo "  make cancel-dry-run ORG=my-org WORKSPACE=my-workspace"; \
		exit 1; \
	fi
	uv run python tfc-cancel-pending.py $(ORG) $(WORKSPACE) --dry-run

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  cancel           - Cancel pending runs (requires ORG and WORKSPACE)"
	@echo "  cancel-dry-run   - Dry run for canceling pending runs (requires ORG and WORKSPACE)"
	@echo ""
	@echo "Usage examples:"
	@echo "  make cancel ORG=my-org WORKSPACE=my-workspace"
	@echo "  make cancel-dry-run ORG=my-org WORKSPACE=my-workspace"

.DEFAULT_GOAL := help