# 🎨 Perchance OpenAI V1 Compatible Image API

A production-ready, OpenAI V1 compatible image generation API server powered by [Perchance AI Text-to-Image Generator](https://perchance.org/ai-text-to-image-generator).

Engineered to seamlessly integrate into any OpenAI-compatible client, web UI, discord bot, or frontend app (LibreChat, NextChat, LobeChat, etc.).

---

## ⚡ Features

- **OpenAI V1 Compatibility**: Drop-in replacement for `POST /v1/images/generations` and `GET /v1/models`.
- **100% Free & Unlimited**: Powered by Perchance AI with zero account or token limits.
- **Aspect Ratio Mapping**: Automatically maps standard OpenAI sizes (`1024x1024`, `1792x1024`, `1024x1792`) to Square, Landscape, and Portrait shapes.
- **Model Presets for Styles**: Use models like `perchance-cinematic`, `perchance-anime`, `perchance-ghibli`, `perchance-disney`, `perchance-photo`, etc.
- **FastAPI Framework**: High-performance asynchronous API with automatic interactive OpenAPI docs (`/docs`).
- **Serverless & Local Ready**: Configured for Vercel, Docker, and local development.

---

## 🚀 Quick Start (Local)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run API Server
```bash
python run_local.py
```
The server will start at `http://127.0.0.1:8000`. Interactive docs are available at `http://127.0.0.1:8000/docs`.

---

## 📡 API Reference

### 1. Generate Image (`POST /v1/images/generations`)

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic cybernetic tiger in a rainy neon city",
    "model": "perchance-cinematic",
    "size": "1792x1024",
    "response_format": "b64_json"
  }'
```

**Response:**
```json
{
  "created": 1729462800,
  "data": [
    {
      "b64_json": "iVBORw0KGgoAAAANSUhEUgAA...",
      "revised_prompt": "A futuristic cybernetic tiger in a rainy neon city"
    }
  ]
}
```

### 2. List Models (`GET /v1/models`)
```bash
curl http://127.0.0.1:8000/v1/models
```

---

## 🐍 Usage with OpenAI Python SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="none"  # Not required unless API_KEY is set in .env
)

response = client.images.generate(
    model="perchance-anime",
    prompt="A magical floating castle surrounded by sakura petals",
    size="1024x1024"
)

# Access base64 image data
image_b64 = response.data[0].b64_json
```

---

## 🌐 Deployment

### Vercel Serverless
This repository includes [`vercel.json`](file:///c:/Users/YİĞİT/Desktop/Yiğit/perchance-api/vercel.json) configured for `@vercel/python`.

> **Note on Vercel:** Perchance uses Cloudflare Turnstile anti-bot checks. While local and VPS/Docker environments bypass this smoothly, Vercel Serverless Functions have strict 10s execution limits on the Hobby plan. For production hosting, Docker/Render/Railway or self-hosted VPS is recommended.
