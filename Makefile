# Simple usage: make cancel my-org my-workspace
.PHONY: cancel
cancel:
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ] || [ -z "$(word 3,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make cancel <organization> <workspace>"; \
		echo ""; \
		echo "Example:"; \
		echo "  make cancel my-org my-workspace"; \
		exit 1; \
	fi
	@uv run python tfc_cancel_pending.py $(word 2,$(MAKECMDGOALS)) $(word 3,$(MAKECMDGOALS))

.PHONY: cancel-dry-run
cancel-dry-run:
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ] || [ -z "$(word 3,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make cancel-dry-run <organization> <workspace>"; \
		echo ""; \
		echo "Example:"; \
		echo "  make cancel-dry-run my-org my-workspace"; \
		exit 1; \
	fi
	@uv run python tfc_cancel_pending.py $(word 2,$(MAKECMDGOALS)) $(word 3,$(MAKECMDGOALS)) --dry-run

# Catch-all target to prevent "No rule to make target" errors
%:
	@:

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  cancel           - Cancel pending runs"
	@echo "  cancel-dry-run   - Dry run for canceling pending runs"
	@echo ""
	@echo "Usage:"
	@echo "  make cancel <organization> <workspace>"
	@echo "  make cancel-dry-run <organization> <workspace>"
	@echo ""
	@echo "Examples:"
	@echo "  make cancel my-org my-workspace"
	@echo "  make cancel-dry-run my-org my-workspace"

.DEFAULT_GOAL := help