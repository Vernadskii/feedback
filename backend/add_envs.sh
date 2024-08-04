#!/bin/bash

# Load environment variables from .env_local file
if [ -f .env_local ]; then
  export $(grep -v '^#' .env_local | xargs)
else
  echo ".env_local file not found."
  exit 1
fi

echo "Environment variables loaded. You can now run your django command."

# Keep the script running to allow user to run commands interactively
exec "$SHELL"