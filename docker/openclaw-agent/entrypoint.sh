#!/bin/sh
# Entrypoint for OpenClaw Agent Container

# Ensure workspace exists
mkdir -p /workspace

# Start OpenClaw gateway
exec "$@"
