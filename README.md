# AI Compass (Production)

This is the production repository for **the-ai-compass.de**. This repository contains the optimized, live version of the AI Compass platform, automatically synchronized from the [Development Repository](https://github.com/AI-Compass-SME/ai-compass).

## 🚀 Live Environment
- **Platform Domain:** [the-ai-compass.de](https://the-ai-compass.de)
- **Frontend:** Hosted on **Vercel** (Vite + React)
- **Backend:** Hosted on **Render** (FastAPI)
- **Database:** PostgreSQL (Render Managed)

## 📁 Repository Structure
This repository uses a streamlined structure optimized for PaaS deployment:
- `/backend`: FastAPI application and ML inference engine.
- `/frontend`: Vite-based React frontend.

## 🛠 Maintenance
This repository is managed by **GitHub Actions**. Manual edits to this repository are discouraged as they will be overwritten by the next automated sync from the development repository.

To update the application:
1. Make changes in the `ai-compass` (Development) repository.
2. Merge changes into the `main` branch.
3. The automation will restructure and push changes here, triggering a live deployment.

---
© 2024-2025 AI Compass SME
