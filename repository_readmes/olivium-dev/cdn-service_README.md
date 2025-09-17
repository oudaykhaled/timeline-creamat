# README for olivium-dev/cdn-service

# CDN Service - S3 Image Upload API

A .NET Core-based API service for uploading, retrieving, and managing media files in AWS S3 with advanced features like LQIP (Low Quality Image Placeholders).

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [LQIP (Low Quality Image Placeholders)](#lqip-low-quality-image-placeholders)
- [Validation](#validation)

## Overview

This service provides a robust API layer for media file management, using AWS S3 as the storage backend. It supports various media types with specialized validation rules and offers automatic generation of low-quality image placeholders (LQIP) for supported image types.

## Features

- Upload media files to AWS S3
- Configurable media type validation (sizes, dimensions, file types)
- Automatic LQIP generation for faster page loads
- Range request support for media streaming
- Delete operations for file management

## Getting Started

### Prerequisites

- .NET 6.0 or later
- AWS account with S3 bucket access
- AWS credentials (AccessKey and SecretKey)

### Installation

1. Clone the repository
2. Configure the `appsettings.json` file with your AWS credentials and media types
3. Run the application:

```bash
dotnet run
```

## Configuration

The service is configured via the `appsettings.json` file:

```json
{
  "AWS": {
    "AccessKey": "YOUR_ACCESS_KEY",
    "SecretKey": "YOUR_SECRET_KEY",
    "BucketName": "your-bucket-name",
    "Region": "us-east-2"
  },
  "MediaTypes": [
    {
      "name": "profile-picture",
      "extensions": [ ".jpg", ".png", ".jpeg" ],
      "maxFileSize": "75MB",
      "img-lqip": ["res-100", "res-200", "res-300"]
    },
    {
      "name": "thumbnail-channel",
      "aspectRatio": "1:1",
      "extensions": [ ".jpg", ".png", ".jpeg" ],
      "maxFileSize": "100kb"
    }
  ]
}
```

## API Endpoints

### Upload a File

```http
POST /api/ImageUpload/upload?mediaTypeName={mediaTypeName}
```

### Fetch a File

```http
GET /api/ImageUpload/fetch/{fileName}
```

### Delete a File

```http
DELETE /api/ImageUpload/delete/{fileName}
```

### Get Media Types Configuration

```http
GET /api/ImageUpload/mediaTypes
```

### Diagnostic Configuration Check

```http
GET /api/ImageUpload/diagnose-config
```

### Manually Generate LQIP

```http
GET /api/ImageUpload/generate-lqip/{id}
```

## LQIP (Low Quality Image Placeholders)

### What is LQIP?

LQIP (Low Quality Image Placeholders) is a technique that improves the perceived loading speed of web pages. It involves:

1. Generating smaller, lower resolution versions of images
2. Loading these smaller versions first as placeholders
3. Replacing them with the full-quality images once loaded

This approach gives users immediate visual feedback while the larger, higher-quality images load in the background.

### How to Configure LQIP

LQIP is configured in the `MediaTypes` section of the `appsettings.json` file:

```json
{
  "name": "profile-picture",
  "extensions": [ ".jpg", ".png", ".jpeg" ],
  "maxFileSize": "75MB",
  "img-lqip": ["res-100", "res-200", "res-300"]
}
```

The `img-lqip` array specifies the resolutions to generate. Each entry follows the format `res-{width}`, where `{width}` is the width in pixels for the generated image. The height is proportionally scaled.

### How LQIP Works

When an image is uploaded with a media type that has LQIP configured:

1. The original image is stored at `{mediaTypeName}/{fileName}`
2. For each resolution specified in `img-lqip`, a resized version is generated and stored at `{mediaTypeName}/{resolution}/{fileName}`

Example:
- Original: `profile-picture/abc123.png`
- LQIP versions:
  - `profile-picture/res-100/abc123.png`
  - `profile-picture/res-200/abc123.png`
  - `profile-picture/res-300/abc123.png`

### Usage Example

1. **Configuration**:
   ```json
   "img-lqip": ["res-100", "res-200", "res-300"]
   ```

2. **Upload an Image**:
   ```bash
   # Upload a profile picture
   curl -X POST "http://localhost:5221/api/ImageUpload/upload?mediaTypeName=profile-picture" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.png"
   ```
   
   Response:
   ```json
   {"fileName":"e74fc7a4-e70e-44b8-8b41-eeb75b59825a.png"}
   ```

3. **Fetch the Images**:
   ```bash
   # Fetch the original
   curl "http://localhost:5221/api/ImageUpload/fetch/profile-picture%2Fe74fc7a4-e70e-44b8-8b41-eeb75b59825a.png" -o original.png
   
   # Fetch the LQIP versions
   curl "http://localhost:5221/api/ImageUpload/fetch/profile-picture%2Fres-100%2Fe74fc7a4-e70e-44b8-8b41-eeb75b59825a.png" -o lqip-100.png
   curl "http://localhost:5221/api/ImageUpload/fetch/profile-picture%2Fres-200%2Fe74fc7a4-e70e-44b8-8b41-eeb75b59825a.png" -o lqip-200.png
   curl "http://localhost:5221/api/ImageUpload/fetch/profile-picture%2Fres-300%2Fe74fc7a4-e70e-44b8-8b41-eeb75b59825a.png" -o lqip-300.png
   ```

4. **Client-side Implementation**:
   ```javascript
   // Example using a progressive image loading pattern
   function loadImage(imageId, filename) {
     const img = document.getElementById(imageId);
     
     // First load the smallest LQIP
     img.src = `/api/ImageUpload/fetch/profile-picture%2Fres-100%2F${filename}`;
     
     // Then load the full resolution version
     const fullImg = new Image();
     fullImg.onload = function() {
       img.src = this.src;
     };
     fullImg.src = `/api/ImageUpload/fetch/profile-picture%2F${filename}`;
   }
   ```

### Manual LQIP Generation

For existing images that were uploaded without LQIP generation, use the manual endpoint:

```bash
curl "http://localhost:5221/api/ImageUpload/generate-lqip/e74fc7a4-e70e-44b8-8b41-eeb75b59825a"
```

Response:
```json
{
  "message": "LQIP generation completed",
  "results": [
    "Created LQIP: profile-picture/res-100/e74fc7a4-e70e-44b8-8b41-eeb75b59825a.png",
    "Created LQIP: profile-picture/res-200/e74fc7a4-e70e-44b8-8b41-eeb75b59825a.png",
    "Created LQIP: profile-picture/res-300/e74fc7a4-e70e-44b8-8b41-eeb75b59825a.png"
  ]
}
```

## Validation

Use the included validation script to verify successful upload and LQIP generation:

```bash
./validate-cdn-upload.sh path/to/image.png
```

This script will:
1. Upload the image
2. Check that the original file was created in S3
3. Verify that all LQIP versions were created correctly 