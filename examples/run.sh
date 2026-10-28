#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_impact_check info
PYTHONPATH=src python -m gbt_impact_check check --payload '{"target": "<在此填写>"}'
PYTHONPATH=src python -m gbt_impact_check run   --payload '{"target": "<在此填写>"}'
