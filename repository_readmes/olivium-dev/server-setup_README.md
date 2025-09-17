# README for olivium-dev/server-setup

# Server Setup with ngrok

This repository contains scripts to set up and configure ngrok tunneling for a server, enabling both SSH access and HTTP forwarding through ngrok's secure tunnels.

## Overview

The `setup_ngrok.sh` script automates the process of:
1. Connecting to a server via SSH
2. Installing and configuring ngrok
3. Setting up tunnels for both SSH and HTTP services
4. Validating the connections

## Prerequisites

- A server with SSH access
- `.env` file with proper configuration (see below)
- Local machine with `sshpass` (will be installed by the script if missing)

## Configuration

Create a `.env` file with the following parameters:

```
IP_ADDRESS=<server-ip-address>
SSH_USER=<ssh-username>
SSH_PASSWORD=<ssh-password>

# Optional database credentials
POSTGRES_USERNAME=<db-username>
POSTGRES_PASSWORD=<db-password>

# ngrok settings
NGROK_TOKEN=<your-ngrok-auth-token>
NGROK_DOMAIN=<your-custom-ngrok-domain> # if available
NGROK_ID=<your-ngrok-id> # optional
```

## Usage

1. Make sure the script is executable:
   ```
   chmod +x setup_ngrok.sh
   ```

2. Run the script:
   ```
   ./setup_ngrok.sh
   ```

3. The script will:
   - Connect to your server
   - Install ngrok if not already present
   - Configure ngrok with your auth token
   - Set up tunnels for SSH and HTTP
   - Test the connections
   - Provide connection details

## Validation Results

When the script runs successfully, you should see output similar to this:

```
=== Connection Information ===
Server IP: 192.168.2.41
SSH User: ec2-user
Ngrok Domain: poodle-darling-scarcely.ngrok-free.app

=== Connecting to server and setting up ngrok ===
Checking if ngrok is installed...
[Installation details...]

=== Getting ngrok public URLs ===
[ngrok status details...]

=== Testing connections ===
SSH URL: tcp://0.tcp.eu.ngrok.io:17948
To connect via SSH, use: ssh -p 17948 ec2-user@0.tcp.eu.ngrok.io
Testing SSH connection through ngrok...
SSH connection through ngrok successful!

HTTP URL: https://6e540997b37e.ngrok.app
Testing HTTP connection through ngrok...
HTTP Response Code: 200

=== Summary ===
Ngrok setup completed on server 192.168.2.41
Domain: poodle-darling-scarcely.ngrok-free.app
SSH Forwarding: tcp://0.tcp.eu.ngrok.io:17948
HTTP Forwarding: https://6e540997b37e.ngrok.app

You can now connect to your server via SSH using:
  ssh -p 17948 ec2-user@0.tcp.eu.ngrok.io

You can make API calls to your server using:
  https://6e540997b37e.ngrok.app

To monitor ngrok status on the server, use:
  ssh ec2-user@192.168.2.41 'cat ~/ngrok.log'
```

## Using the ngrok Tunnels

### SSH Access

You can connect to your server from anywhere using:
```
ssh -p <port> <username>@<ngrok-host>
```

Example:
```
ssh -p 17948 ec2-user@0.tcp.eu.ngrok.io
```

### HTTP Access

You can access your server's web services or make API calls using the provided HTTPS URL:
```
https://<random-id>.ngrok.app
```

Example:
```
https://6e540997b37e.ngrok.app
```

## Monitoring and Troubleshooting

### Check ngrok logs

```
ssh <username>@<server-ip> 'cat ~/ngrok.log'
```

Example:
```
ssh ec2-user@192.168.2.41 'cat ~/ngrok.log'
```

### View ngrok status

You can access the ngrok web interface on your server at:
```
http://localhost:4040
```

To view it remotely, set up a separate SSH tunnel:
```
ssh -L 4040:localhost:4040 <username>@<server-ip>
```

Then open `http://localhost:4040` in your browser.

## Notes

- The ngrok free tier has limitations on the number of tunnels and connection duration
- Custom domains require a paid ngrok plan
- The tunnels will terminate if the ngrok process is stopped on the server
- To make the tunnel persistent across server reboots, consider setting up ngrok as a service

## Security Considerations

- The `.env` file contains sensitive information and should be properly secured
- Consider using SSH keys instead of passwords for more secure authentication
- Review your ngrok settings to ensure they meet your security requirements 