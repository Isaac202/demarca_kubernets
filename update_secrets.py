#!/usr/bin/env python3
import base64
import yaml
import os
from pathlib import Path

def encode_base64(value):
    """Encode string to base64."""
    return base64.b64encode(str(value).encode()).decode()

def read_env_file(env_path):
    """Read .env file and return dict of key-value pairs."""
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def update_secrets_yaml(env_vars, output_path):
    """Create or update Kubernetes secrets YAML file."""
    # Create the secret structure
    secret = {
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {
            'name': 'demarca-secrets'
        },
        'type': 'Opaque',
        'data': {}
    }
    
    # Add all environment variables as base64 encoded values
    for key, value in env_vars.items():
        secret['data'][key] = encode_base64(value)
    
    # Write to YAML file
    with open(output_path, 'w') as f:
        yaml.dump(secret, f, default_flow_style=False)

def main():
    # Get the directory of the script
    script_dir = Path(__file__).parent
    
    # Define paths
    env_path = script_dir / '.env'
    secrets_path = script_dir / 'demarca-secrets.yaml'
    
    # Check if .env file exists
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        return
    
    # Read environment variables
    env_vars = read_env_file(env_path)
    
    # Update secrets YAML
    update_secrets_yaml(env_vars, secrets_path)
    print(f"Successfully updated {secrets_path}")

if __name__ == '__main__':
    main() 