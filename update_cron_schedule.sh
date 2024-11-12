#!/bin/bash

CRONJOB_JSON="data/cronjob.json"
TEMPLATE_YML="sample.yml"
OUTPUT_YML=".github/workflows/run_prediction.yml"

# Extract datetime_cron value using grep and sed
CRON_SCHEDULE=$(grep '"datetime_cron"' "$CRONJOB_JSON" | sed -E 's/.*: "(.*)".*/\1/')

# Substitute the placeholder in sample.yml and create run_prediction.yml
sed "s/{{CRON_SCHEDULE}}/$CRON_SCHEDULE/" "$TEMPLATE_YML" > "$OUTPUT_YML"

echo "Updated cron schedule to: $CRON_SCHEDULE"
