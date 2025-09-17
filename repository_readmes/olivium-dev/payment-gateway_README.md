# README for olivium-dev/payment-gateway

# Payment Gateway Microservice

A flexible and extendable payment gateway microservice built with **ASP.NET Core**, designed to handle multiple payment providers such as Stripe, PayPal, and more. This service supports features like session creation, webhook handling, and environment switching between test and live modes.

## Features
- **Dynamic Gateway Support:** Easily add and configure new payment gateways.
- **Environment Switching:** Seamless transition between test and live environments.
- **Webhook Handling:** Secure and scalable webhook endpoint for payment notifications.
- **Modular Architecture:** Extensible design using repositories and factories for different gateways.

---

## Getting Started

### Prerequisites
- **.NET 8 SDK** or later
- **Stripe CLI** (for testing Stripe webhooks)
- A supported payment gateway account (e.g., Stripe, PayPal)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/olivium-dev/payment-gateway.git
   cd payment-gateway
   ```

2. Restore dependencies:
   ```bash
   dotnet restore
   ```

3. Update the `appsettings.json` file:
   - Configure your gateway keys and environment details.

---

## Configuration

### AppSettings Structure
The `appsettings.json` file should include configurations for payment gateways, mode switching, and keys:

```json
{
  "PaymentGatewaySettings": {
    "Mode": "Test", // Can be "Test" or "Live"
    "Gateways": {
      "Stripe": {
        "Test": {
          "SecretKey": "sk_test_1234567890",
          "PublishableKey": "pk_test_1234567890"
        },
        "Live": {
          "SecretKey": "sk_live_0987654321",
          "PublishableKey": "pk_live_0987654321"
        }
      },
      "PayPal": {
        "Test": {
          "ClientId": "test_client_id",
          "ClientSecret": "test_client_secret"
        },
        "Live": {
          "ClientId": "live_client_id",
          "ClientSecret": "live_client_secret"
        }
      }
    }
  }
}
```

### Dependency Injection
Ensure repositories and the factory are registered in `Program.cs`:

```csharp
builder.Services.AddSingleton(paymentGatewaySettings);
builder.Services.AddScoped<IBaseRepository, StripePaymentRepository>();
builder.Services.AddScoped<IBaseRepository, PayPalPaymentRepository>();
builder.Services.AddSingleton<PaymentGatewayFactory>();
```

---

## Endpoints

### 1. Create Payment Session
**URL:** `POST /api/Payment/create-session`

**Payload:**
```json
{
  "Gateway": "stripe",
  "Amount": 1000,
  "Currency": "usd",
  "ProductName": "Test Product",
  "SuccessUrl": "https://example.com/success",
  "CancelUrl": "https://example.com/cancel"
}
```

**Response:**
- `200 OK`: Session created successfully.
- `400 Bad Request`: Invalid request.
- `404 Not Found`: Unsupported gateway.

---

### 2. Webhook Endpoint
**URL:** `POST /api/payment/webhook/{gateway}`

**Description:** Processes events from the payment provider. For example, Stripe webhooks such as `payment_intent.succeeded`.

**Headers:**
- `Stripe-Signature`: (for Stripe)

**Payload:** Depends on the gateway (e.g., Stripe event payloads).

**Response:**
- `200 OK`: Webhook processed successfully.
- `400 Bad Request`: Invalid payload or signature.
