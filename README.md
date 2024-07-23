# Social Media Post Automation

![GitHub stars](https://img.shields.io/github/stars/ridhotamma/Project-Roy?style=social)
![GitHub forks](https://img.shields.io/github/forks/ridhotamma/Project-Roy?style=social)
![GitHub issues](https://img.shields.io/github/issues/ridhotamma/Project-Roy)
![GitHub license](https://img.shields.io/github/license/ridhotamma/Project-Roy)

## 🚀 Overview

Welcome to the **Social Media Post Automation** project! This tool is designed to automate Instagram posts, stories, and much more. Whether you're looking to upload in bulk, schedule content, or streamline your social media management, this project has you covered.

## ✨ Features

- **Bulk Post Upload**: Upload multiple posts at once with ease.
- **Bulk Story Upload**: Share multiple stories in a single go.
- **Content Scheduling**: Plan and schedule your posts and stories for future dates and times.
- **Automatic Posting**: Automate your posts to go live at the optimal times.
- **Detailed Analytics**: Get insights and analytics on your posts and stories.
- **User-Friendly Interface**: Simple and intuitive interface for seamless navigation.
- **Multi-Account Management**: Manage multiple Instagram accounts effortlessly.

## 🛠️ Technologies Used

- **FastAPI**: For building the backend API.
- **React**: For building the frontend interface.
- **Celery**: For handling asynchronous tasks.
- **MongoDB**: For storing data.
- **Redis**: For task queuing.

## 📸 Screenshots

![Dashboard Screenshot](https://via.placeholder.com/800x400.png?text=Dashboard+Screenshot)
![Bulk Upload Screenshot](https://via.placeholder.com/800x400.png?text=Bulk+Upload+Screenshot)

## 📚 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 14+
- MongoDB
- Redis

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ridhotamma/Project-Roy.git
   cd ./Project-Roy
   ```

2. **Project Setup**

   Create a virtual environment for the backend FastAPI:

   If on macOS/Linux:
   ```bash
   python3 -m venv venv
   ```

   If on Windows:
   ```bash
   python -m venv venv
   ```

   Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Install frontend dependencies:
   ```bash
   cd ./frontend
   npm install
   ```

3. **How to run the project**

   Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

   Run the frontend:
   ```bash
   cd ./frontend && npm run dev
   ```

   If you are using macOS, just run using the Makefile:
   ```bash
   make start-dev
   ```

4. **Running with Docker**

   Using Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
```