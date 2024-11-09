#!/bin/bash

pushgateway_endpoint="http://localhost:9091"
job_name="python_temperature_test"

output=$((1 + RANDOM % 100))
echo $output
# Generate a temporary file to store the metrics
temp_file=$(mktemp)

# Format the metrics output in Prometheus format
cat <<EOF > "$temp_file"
temperature_monitor_test{instance="raspberryPi"} $output
EOF

# Push the metrics to Pushgateway
curl -v -X POST -H "Content-Type: text/plain" --data-binary "@$temp_file" "$pushgateway_endpoint/metrics/job/$job_name"

# Clean up the temporary file
rm "$temp_file"