# README for olivium-dev/pricing-service

# Pricing Microservice

This microservice provides a straightforward way to manage product prices in a database. It supports adding new prices, retrieving them by SKU ID or Reference ID, editing existing prices, and deactivating prices. It also logs historical changes (edits and deactivations) in a separate table.

Below, you will find:

-   [Key Features](#key-features)
-   [Tech Stack](#tech-stack)
-   [Requirements](#requirements)
-   [Installation & Running](#installation--running)
    -   [1. Run Locally (Go)](#1-run-locally-go)
    -   [2. Run with Docker](#2-run-with-docker)
-   [Testing](#testing)
-   [API Endpoints](#api-endpoints)
-   [Swagger / OpenAPI Specification](#swagger--openapi-specification)
-   [License](#license)

----------

## Key Features

-   **Add a new price** with support for _international_ or _country-specific_ prices.
-   **Retrieve prices** by:
    -   SKU ID (unique identifier for a single SKU)
    -   Reference ID (groups multiple SKUs together)
-   **Batch retrieval** of prices for multiple Reference IDs (with fallback to an _international_ price).
-   **Edit prices** while automatically logging previous price data.
-   **Deactivate prices** by moving them to a log table.

----------

## Tech Stack

-   **Language:** Go 1.20
-   **Frameworks:**
    -   [Gin Gonic](https://github.com/gin-gonic/gin) (HTTP web framework)
    -   [GORM](https://github.com/go-gorm/gorm) (ORM for Go)
-   **Database:** SQLite (for demo) — you can adapt it to any other database driver supported by GORM (MySQL, Postgres, etc.)
-   **Docker:** Alpine-based images for lightweight containerization

----------

## Requirements

-   [Go 1.20+](https://go.dev/) (if running locally)
-   [Docker](https://www.docker.com/) (if running in a container)

----------

## Installation & Running

Below are two main ways to run this microservice:

### 1. Run Locally (Go)

1.  **Clone the repository**:
    
    bash
    
    Copy code
    
    `git clone https://github.com/your-org/pricing-microservice.git
    cd pricing-microservice` 
    
2.  **Install dependencies**:
    
    bash
    
    Copy code
    
    `go mod download` 
    
3.  **Run the microservice**:
    
    bash
    
    Copy code
    
    `go run main.go` 
    
    By default, it will listen on port **8080**. You can then access the endpoints at `http://localhost:8080`.
    

----------

### 2. Run with Docker

We provide a `Dockerfile` that compiles and runs the microservice inside a lightweight Alpine container.

1.  **Build the image**:
    
    bash
    
    Copy code
    
    `docker build -t your-username/pricing-microservice:latest .` 
    
2.  **Run the container**:
    
    bash
    
    Copy code
    
    `docker run -d -p 8080:8080 --name pricing-microservice your-username/pricing-microservice:latest` 
    
    This will expose the service on port **8080** of your Docker host.

3.  **Run the container with persistent data**:
    
    To ensure your data persists between container restarts or when deploying new versions, use a volume:
    
    bash
    
    Copy code
    
    `docker run -d -p 8080:8080 -v pricing_data:/app/data --name pricing-microservice your-username/pricing-microservice:latest` 
    
    This creates a named volume `pricing_data` that will persist your database even when the container is replaced.

----------

## Testing

To test the microservice endpoints, you can use:

-   **cURL**
-   **Postman** (a Postman collection is partially demonstrated in the code snippet, or you can import your own).
-   **Any other REST client** (Insomnia, etc.)

A few example cURL commands are:

1.  **Create a new price** (international):
    
    bash
    
    Copy code
    
    `curl -X POST "http://localhost:8080/sku" \
    -H "Content-Type: application/json" \
    -d '{
          "reference_id": "dfd7f877-8b6b-4c47-bf49-9e752bb0ead8",
          "description": "Product #1 (International)",
          "price": 99.99,
          "type": "Physical",
          "tag": "Promo",
          "country_code": null,
          "currency_id": 1,
          "currency": "USD"
        }'` 
    
2.  **Get prices by SKU ID**:
    
    bash
    
    Copy code
    
    `curl -X GET "http://localhost:8080/sku/id/your-sku-id"` 
    
3.  **Get prices by Reference ID**:
    
    bash
    
    Copy code
    
    `curl -X GET "http://localhost:8080/sku/reference/your-ref-id"` 
    
4.  **Edit an existing price**:
    
    bash
    
    Copy code
    
    `curl -X POST "http://localhost:8080/sku/edit" \
    -H "Content-Type: application/json" \
    -d '{
          "id": "ec51a376-1598-4529-81ff-2b8bf8330e05",
          "new_price": 69.99
        }'` 
    
5.  **Deactivate a price**:
    
    bash
    
    Copy code
    
    `curl -X POST "http://localhost:8080/sku/deactivate" \
    -H "Content-Type: application/json" \
    -d '{"id":"5014d0ef-e310-4c5e-a47d-81118ac9bf0a"}'` 
    

----------

## API Endpoints

HTTP Method

Endpoint

Description

**GET**

`/sku/id/:id`

Get prices by SKU ID

**GET**

`/sku/reference/:reference_id`

Get prices by Reference ID

**POST**

`/sku`

Add a new price

**POST**

`/sku/batch`

Get prices for multiple Reference IDs

**POST**

`/sku/deactivate`

Deactivate a price

**POST**

`/sku/edit`

Edit a price (logs old data automatically)