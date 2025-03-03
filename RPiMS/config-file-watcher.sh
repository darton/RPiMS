#!/bin/bash

# Check if at least two arguments are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <path-to-file1> [<path-to-file2> ... <path-to-filen>] <service-name>"
    exit 1
fi

# Assign the last argument to the service_name variable
service_name="${@: -1}"

# Delay in seconds
delay=1  # Adjust this value as needed

# Loop through all arguments except the last one
for file in "$@"; do
    # Skip the service name argument
    if [ "$file" == "$service_name" ]; then
        continue
    fi

    # Define checksum file names
    checksum_file="$file.sha256"
    old_checksum_file="$file.old.sha256"

    # Wait for the checksum file to be created
    sleep "$delay"

    # Check if both checksum files exist
    if [ ! -f "$checksum_file" ] || [ ! -f "$old_checksum_file" ]; then
        echo "Checksum file(s) do not exist for $file."
        exit 1
    fi

    # Read the current and previous checksums
    current_checksum=$(cat "$checksum_file")
    previous_checksum=$(cat "$old_checksum_file")

    # Compare checksums
    if [ "$current_checksum" != "$previous_checksum" ]; then
        # Restart the service
        systemctl restart "$service_name"
        exit 0
    fi
done
