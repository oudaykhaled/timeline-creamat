# README for olivium-dev/rahmah-gateway

# Rahmah Gateway

## Overview

Rahmah Gateway is a .NET-based web application designed to provide a robust and scalable gateway service. This project leverages ASP.NET Core for building modern, cloud-based, and internet-connected applications.

## Project Structure

- **Program.cs**: The main entry point of the application where the web host is configured and run.
- **appsettings.json**: Configuration file for application settings, including logging and allowed hosts.
- **appsettings.Development.json**: Configuration file for development-specific settings.
- **Dockerfile**: Instructions for building and running the application in a Docker container.
- **Controllers/**: Contains API endpoints controllers
- **Services/**: Contains business logic services and validators

## Features

### Chat Packages

The gateway manages chat slot licenses, allowing users to purchase packages for multiple simultaneous chats.

### Digital Assets

The gateway supports various digital assets that users can purchase with credits:

- **Careem Assets**: Vouchers for Careem rides
- **Careem+ Assets**: Vouchers for Careem+ services (food, groceries)
- **Compliments**: One-time assets for sending special compliments to users
- **Profile Unlock**: One-time licenses to unlock profile information
- **Profile Boost**: Time-limited licenses to boost profile visibility

Digital assets are configured in `appsettings.json` and initialized on application startup. Each asset has a name, description, price, license type, and active status. Asset IDs are automatically generated from the asset names.

For more information on the Digital Assets API, see [DigitalAssetsAPI.md](DigitalAssetsAPI.md).

## Chat Message Validation

The gateway includes a simple payload validator for chat messages, which performs basic validation:

- **Text Messages**: Checks if the message has a value
- **Image, Video, and Audio**: Validates if the path has a file extension or is a valid URL
- **Link Messages**: Checks if a URL is provided and in correct format
- **Location Messages**: Verifies the payload can be parsed as a location object

Error handling is simplified, with basic validation messages returned directly to the client.

### Example Payloads

```json
// Text Message
{
  "type": "text",
  "value": "This is a simple message"
}

// Image Message
{
  "type": "image",
  "value": "image.jpg" 
}

// Video Message
{
  "type": "video",
  "value": "https://example.com/video.mp4"
}
```

## Getting Started

### Prerequisites

- .NET 8.0 SDK
- Docker

### Building and Running the Application

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-repo/rahmah-gateway.git
    cd rahmah-gateway
    ```

2. **Build and run the application**:
    ```sh
    dotnet build
    dotnet run
    ```

3. **Using Docker**:
    ```sh
    docker build -t rahmah-gateway .
    docker run -d -p 1122:8080 rahmah-gateway
    ```

## Configuration

### appsettings.json

This file contains configuration settings for the application, such as logging levels, allowed hosts, and digital asset definitions.

Example Digital Assets configuration:
```json
"DigitalAssets": {
  "CareemAssets": [
    {
      "name": "Careem Ride Voucher - Basic",
      "description": "Voucher for a basic Careem ride",
      "price": 50,
      "licenseType": "standard",
      "active": true
    }
  ]
}
```

### appsettings.Development.json

This file contains development-specific configuration settings, which override the settings in `appsettings.json` when the application is run in the Development environment.

### Dockerfile

The Dockerfile contains instructions for building and running the application in a Docker container. It uses multi-stage builds to create a lightweight and efficient Docker image.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
