# README for viakonnect/konnect-travelopro-middleware

# Konnect TraveloPro Middleware

A middleware application that serves as an integration layer between Konnect and TraveloPro systems for flight search and booking operations.

## Project Description

This NestJS application provides a middleware solution that connects to both Konnect and TraveloPro systems. It handles flight search and booking operations, transforming data between the two systems to ensure seamless integration.

The middleware:

- Provides standardized API endpoints for client applications
- Handles data transformation between systems
- Manages error handling and response formatting
- Includes comprehensive API documentation

## Project Structure

```
src/
├── konnect/           # Konnect integration module
│   ├── konnect.controller.ts
│   └── konnect.module.ts
├── travelopro/        # TraveloPro integration module
│   ├── config/        # Configuration for TraveloPro API
│   ├── dto/           # Data Transfer Objects
│   ├── exceptions/    # Custom exceptions
│   ├── interfaces/    # TypeScript interfaces
│   ├── travelopro.controller.ts
│   ├── travelopro.module.ts
│   └── travelopro.service.ts
├── app.module.ts      # Main application module
└── main.ts            # Application entry point
```

## Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/) with automated version increments based on commit messages.

### Commit Format

We use [Conventional Commits](https://www.conventionalcommits.org/) to structure commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types include:

- `feat`: A new feature (increments minor version)
- `fix`: A bug fix (increments patch version)
- `docs`: Documentation changes
- `refactor`: Code changes that neither fix bugs nor add features

### Making Commits

Use our interactive commit tool:

```bash
git add .
yarn commit
```

For more details, see [versioning documentation](docs/versioning.md).

## Installation

```bash
$ yarn install
```

## Environment Configuration

The application uses GPG encryption for protecting sensitive environment variables. This ensures that secrets are not stored in plaintext in the repository.

For basic environment setup:

1. Initialize your GPG key:

   ```bash
   yarn env:init "Your Name" "your.email@example.com" "Optional comment"
   ```

   **IMPORTANT**: When you initialize your GPG key, a secure passphrase is generated for you. You MUST save this passphrase in a secure location (like a password manager).

2. See the [Deployment Setup Guide](docs/deployment-setup.md) for complete instructions on:
   - Environment encryption setup
   - GitHub Actions configuration
   - AWS setup
   - Initial deployment steps
   - Troubleshooting deployment issues

### Required Environment Variables

For the application to run properly, especially in production, these environment variables are required:

#### TraveloPro API Configuration

- `TRAVELOPRO_USER_ID` - Your TraveloPro API user ID
- `TRAVELOPRO_USER_PASSWORD` - Your TraveloPro API password
- `TRAVELOPRO_ACCESS_MODE` - Either "Test" or "Production"
- `TRAVELOPRO_BASE_URL` - The TraveloPro API endpoint URL

#### Database Configuration

- `DATABASE_URL` - PostgreSQL connection string for Prisma
- `DIRECT_URL` - Direct PostgreSQL connection string (often same as DATABASE_URL)

#### Supabase Configuration

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` - Supabase service role key for server-side operations

#### IP Database S3 Configuration

The application uses an IP geolocation database for location-based services. If the database file doesn't exist locally, it will automatically download from AWS S3.

- `AWS_REGION` - AWS region for S3 access (default: us-east-1)
- `AWS_ACCESS_KEY_ID` - AWS Access Key ID with S3 read permissions
- `AWS_SECRET_ACCESS_KEY` - AWS Secret Access Key
- `IP_DATABASE_S3_BUCKET` - S3 bucket name containing the IP database file
- `IP_DATABASE_S3_KEY` - S3 object key for the IP database file (default: ip-location.db)

**Note**: The IP database will be stored locally at `src/konnect/data/ip-location.db` after the first download.

For detailed instructions on setting up S3 and uploading the database file, see the [IP Database S3 Setup Guide](docs/ip-database-s3-setup.md).

### AWS SSM Parameters

When deployed to AWS, the application expects the following parameters to be available in SSM Parameter Store:

- `/{stack-name}/TRAVELOPRO_USER_ID`
- `/{stack-name}/TRAVELOPRO_USER_PASSWORD`
- `/{stack-name}/DATABASE_URL`
- `/{stack-name}/DIRECT_URL`
- `/{stack-name}/SUPABASE_URL`
- `/{stack-name}/SUPABASE_SERVICE_ROLE_KEY`
- `/{stack-name}/TRAVELOPRO_ACCESS_MODE`
- `/{stack-name}/TRAVELOPRO_BASE_URL`
- `/{stack-name}/TRAVELOPRO_REQUEST_TIMEOUT_MS`
- `/{stack-name}/TRAVELOPRO_MAX_RETRIES`
- `/{stack-name}/TRAVELOPRO_FALLBACK_IP`

You can verify the SSM parameters are set correctly by running:

```bash
./scripts/list-ssm-parameters.sh [your-stack-name] [aws-region]
```

### First-time Setup

If you are setting up the project for the first time:

1. Initialize your GPG key:

   ```bash
   yarn env:init "Your Name" "your.email@example.com" "Optional comment"
   ```

   **IMPORTANT**: When you initialize your GPG key, a secure passphrase is generated for you. You MUST save this passphrase in a secure location (like a password manager). You will need it for:

   - Decrypting environment files locally
   - Setting up CI/CD (as a GitHub secret)

2. Create your `.env` file based on the example:

   ```bash
   cp .env.example .env
   # Edit the .env file with your actual values
   ```

3. Encrypt your `.env` file:

   ```bash
   yarn env:encrypt "Your Name"
   ```

4. Export your public key to share with the team:
   ```bash
   yarn env:export-key "Your Name"
   ```

### CI/CD Setup

For the GitHub Actions workflow to successfully decrypt environment files:

1. Add your GPG passphrase as a GitHub secret:

   - Go to your repository on GitHub
   - Navigate to Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `GPG_PASSPHRASE`
   - Value: Your GPG passphrase (saved during initialization)
   - Click "Add secret"

2. Add your base64-encoded GPG private key as a GitHub secret:

   - Export your private key in base64 format:
     ```bash
     gpg --export-secret-keys --armor YOUR_KEY_ID | base64 -w0
     ```
   - Go to your repository on GitHub
   - Navigate to Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `GPG_PRIVATE_KEY`
   - Value: The base64-encoded GPG private key
   - Click "Add secret"

3. The CI/CD pipeline will use these secrets to import your private key and decrypt your environment files during deployment.

### Working with Environment Files

For team members joining the project:

1. Ask an existing team member for the encrypted `.env.asc` file and their public GPG key
2. Import their public key:

   ```bash
   yarn env:import-key "team-member-name.pub.asc"
   ```

3. Decrypt the environment file:
   ```bash
   yarn env:decrypt
   ```
   You will be prompted to enter the passphrase for the GPG key.

### Adding or Updating Environment Variables

When you need to update environment variables:

1. Decrypt the environment file (if not already done)
2. Edit the `.env` file with your changes
3. The pre-commit hook will automatically:
   - Encrypt the `.env` file
   - Add the encrypted `.env.asc` to your commit
   - Run linting and formatting on your changes

If you need to manually encrypt the file:

```bash
yarn env:encrypt "Your Name"
```

### Pre-commit Hook

The project includes a pre-commit hook that automatically:

- Runs linting and formatting on staged files
- Encrypts the `.env` file if it has been modified
- Adds the encrypted `.env.asc` to your commit

The hook is managed by Husky and will run automatically when you make a commit. If you need to bypass the hook for any reason, you can use:

```bash
git commit -m "your message" --no-verify
```

## Running the Application

```bash
# development
$ yarn run start

# watch mode
$ yarn run start:dev

# production mode
$ yarn run start:prod
```

## API Documentation

The application includes auto-generated API documentation:

1. **Swagger UI**:

   - Available at `/api/docs` when running in development mode
   - Provides interactive documentation for testing API endpoints

2. **Scalar API Reference**:
   - Available at `/api/reference` when running in development mode
   - Offers a more modern and feature-rich documentation interface

Access the documentation by running the application and navigating to:

- Swagger UI: http://localhost:3000/api/docs
- Scalar API Reference: http://localhost:3000/api/reference

## Testing

```bash
# unit tests
$ yarn run test

# e2e tests
$ yarn run test:e2e

# test coverage
$ yarn run test:cov
```

## Deployment

### Docker Deployment

The application includes a Dockerfile for containerization:

```bash
# Build the Docker image
docker build -t konnect-travelopro-middleware .

# Run the container
docker run -p 3000:3000 konnect-travelopro-middleware
```

### AWS Deployment with CloudFormation

For production deployment on AWS, use the CloudFormation template and deployment script:

```bash
# Make the deployment script executable
chmod +x infrastructure/cloudformation/deploy.sh

# Deploy to AWS
./infrastructure/cloudformation/deploy.sh [STACK_NAME] [AWS_REGION] [ECR_REPOSITORY_NAME] [IMAGE_TAG]
```

See the [AWS CloudFormation Deployment README](infrastructure/cloudformation/README.md) for detailed instructions.

## Continuous Integration/Continuous Deployment

This project uses GitHub Actions for CI/CD:

- **Automated Deployment**: Every commit to the `master` branch automatically triggers a build and deployment to AWS ECS
- **Environment Configuration**: All TraveloPro credentials and configuration are stored as GitHub Secrets

See the [CI/CD README](.github/workflows/README.md) for detailed instructions on setup and configuration.

## License

This project is licensed under the terms of the license provided by ViaKonnect.
