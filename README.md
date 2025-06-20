# 🤖 Smart Support Bot Platform

A scalable backend platform that powers a generative AI–driven customer support system with real-time chat, automated summarization, product recommendations, and human escalation.

> Built to demonstrate backend engineering, GenAI integration, distributed architecture, and ML-backed personalization.

---

## 📌 Features

- ✨ **Generative AI Chatbot** using OpenAI / Amazon Bedrock
- 🧠 **Product Review Summarization** and semantic tagging
- 🛍️ **Personalized Recommendations** (collaborative & content-based)
- ⚙️ **Microservice Architecture** with API gateway
- 📊 **Real-Time Chat Processing** via Kafka / SQS
- 🔐 **Secure Auth** with JWT, user roles, and rate limiting
- 🔍 **Observability** via OpenTelemetry and Grafana
- 🚀 **Cloud-Native Ready** (Docker, Terraform, AWS ECS/Lambda)

---

## 🏗️ Architecture Overview

```text
[Client (Web/Mobile)]
       │
    [API Gateway]
       │
 ┌─────────────┬──────────────┬──────────────┐
 │             │              │              │
User Service  Chat Service  Feedback Service  ← User messages & ratings
       │             │              │
       └────┐   ┌────┘        ┌─────┘
            │   │             │
         AI Engine        Recommendation Engine
            │                   │
         Bedrock /             Redis / FAISS / LightFM
         OpenAI API

[PostgreSQL / DynamoDB]    [Kafka / SQS]    [Grafana + OpenTelemetry]
