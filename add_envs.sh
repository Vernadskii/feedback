#!/bin/bash
# Load environment variables from .env file
if [ -f .env ]; then
  # Use while-read to correctly handle spaces and special characters
  while IFS='=' read -r key value; do
    # Skip comments and empty lines
    if [[ ! "$key" =~ ^# && -n "$key" ]]; then
      # Remove any trailing comments after the value using parameter expansion
      value="${value%%#*}"  # Strip everything after the first '#'
      value="${value%"${value##*[![:space:]]}"}"  # Trim trailing spaces
      export "$key=$value"
    fi
  done < .env
else
  echo ".env file not found."
  exit 1
fi

echo "Environment variables are loaded."

# Keep the script running to allow user to run commands interactively
exec "$SHELL"