# Kremati Mobile App - Core Components

## Essential Mobile Components (9 Components)

| # | Component Name | Description | Key Features | Platform |
|---|---|---|---|---|
| 1 | **Login & Onboarding Screen** | User authentication and app introduction | • Social login (Google/Facebook)<br>• OTP verification<br>• Terms acceptance<br>• Profile setup form | Android (Kotlin)<br>iOS (SwiftUI) |
| 2 | **App Walkthrough/Tutorial** | Interactive introduction to app features | • Welcome slides carousel<br>• Feature highlights<br>• Skip/Next navigation<br>• Getting started guide | Android (Kotlin)<br>iOS (SwiftUI) |
| 3 | **Home Screen** | Main landing page with product discovery | • Hero banner carousel<br>• Category grid<br>• Featured products<br>• Search bar<br>• Bottom navigation | Android (Kotlin)<br>iOS (SwiftUI) |
| 4 | **Product Catalog & Details** | Browse and view cosmetic products | • Product grid/list view<br>• Filter & sort options<br>• Product detail screen<br>• Image gallery<br>• Add to cart/wishlist | Android (Kotlin)<br>iOS (SwiftUI) |
| 5 | **Shopping Cart & Checkout** | Manage cart and complete purchases | • Cart item management<br>• Quantity adjustment<br>• Shipping address form<br>• Payment method selection<br>• Order confirmation | Android (Kotlin)<br>iOS (SwiftUI) |
| 6 | **User Profile & Orders** | Account management and order tracking | • Profile information<br>• Address management<br>• Order history<br>• Loyalty points display<br>• Settings menu | Android (Kotlin)<br>iOS (SwiftUI) |
| 7 | **Product Reviews & Ratings** | User-generated content for products | • Write review form<br>• Star rating system<br>• Review list display<br>• Photo upload<br>• Helpfulness voting | Android (Kotlin)<br>iOS (SwiftUI) |
| 8 | **Customer Support Chat** | In-app help and support system | • Live chat interface<br>• Bot integration<br>• FAQ section<br>• Contact support<br>• Help center | Android (Kotlin)<br>iOS (SwiftUI) |
| 9 | **AI Face Scanner** | AI-powered cosmetics matching | • Camera integration<br>• Face detection & analysis<br>• Skin tone recognition<br>• Product recommendations<br>• AR makeup preview | Android (Kotlin)<br>iOS (SwiftUI) |

## Component Integration Flow

```
Login Screen → Walkthrough → Home Screen → Product Catalog → Shopping Cart → User Profile
                                ↓              ↓              ↓              ↓
                     AI Face Scanner → Reviews & Ratings ← Checkout ← Customer Support
```

## Development Priority

1. **Login & Onboarding** - Essential for user access
2. **App Walkthrough** - User education and retention
3. **Home Screen** - Core navigation and discovery
4. **Product Catalog** - Main business functionality
5. **Shopping Cart** - E-commerce core feature
6. **User Profile** - Account management
7. **Reviews & Ratings** - Social proof and engagement
8. **Customer Support** - User assistance and retention
9. **AI Face Scanner** - Advanced cosmetics matching and AR experience
