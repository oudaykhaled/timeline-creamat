# README for olivium-dev/wallet-service


# Wallet Microservices README

## Introduction

This document provides an extensive overview of the Wallet Microservices, a system designed to handle various financial transactions including currency conversions, fee calculations, and complex transaction scenarios.

## Services Overview

### Transaction Service

Handles all operations related to transactions between wallets, including:

- **Expected Fees Calculation:** Predicts fees for transactions based on currency and amounts.
- **Transaction Validation:** Ensures that wallets have sufficient funds before proceeding with the transaction.
- **Transaction Initiation and Execution:** Processes transactions ensuring all business rules and validations are adhered to before completing the transaction.

### Wallet Service

Manages wallet operations such as:

- **Creating Wallet Holders:** Registers new wallet holders in the system.
- **Wallet Management:** Allows adding new wallets, deactivating wallets, and updating wallet information for existing holders.

### Fees Service

Responsible for managing transaction fees configurations:

- **Fees Configuration:** Add, update, or delete fee configurations that are used to calculate transaction costs between different currencies.

## Complex Use Cases

### Multi-Currency Transactions

This service supports transactions across wallets with different currencies. It involves converting currencies based on current exchange rates and calculating transaction fees accordingly.

### Fee Calculations

Fees are calculated both as a fixed amount and as a percentage of the transaction amount. The service handles:

- **Dynamic Fee Calculation:** Based on the transaction amount and the currencies involved, dynamically calculate the fees ensuring accuracy and compliance with international transaction regulations.

### Transaction Validation

Before initiating any transaction, the system validates:

- **Sufficient Funds:** Ensures the source wallet has enough funds after accounting for the transaction amount and associated fees.
- **Legitimate Transaction Paths:** Validates that the transaction path (from source to destination) is allowed under the system's rules.

## API Endpoints

Outlined below are key API endpoints provided by the Wallet Microservices, which include operations for managing fees, transactions, and wallets.

### Fees API

- `GET /Fees`: Fetches all fees configurations.
- `POST /Fees`: Adds a new fee configuration.
- `PUT /Fees/{id}`: Updates an existing fee configuration.
- `DELETE /Fees/{id}`: Removes a fee configuration.

### Transaction API

- `POST /Transaction/predict`: Predicts the fees and the final amount for a given transaction.
- `POST /Transaction/validate`: Validates if a transaction can be processed.
- `POST /Transaction/initiate`: Initiates a new transaction.
- `POST /Transaction/{transactionHeaderId}/execute`: Executes a previously validated and initiated transaction.
- `POST /Transaction/{transactionHeaderId}/abort`: Aborts an ongoing transaction.

### Wallet API

- `POST /Wallet/holder/add`: Adds a new wallet holder along with their wallets.
- `GET /Wallet/{holderId}/wallets`: Retrieves all wallets for a given holder.
- `POST /Wallet/{holderId}/{walletId}/deactivate`: Deactivates a specific wallet.

## Conclusion

The Wallet Microservices are designed to provide robust and flexible financial transaction capabilities tailored for modern financial ecosystems. This service ensures high performance, security, and reliability in handling complex, multi-currency financial transactions.
