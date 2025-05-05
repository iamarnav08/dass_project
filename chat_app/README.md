# Olive Orange (Educational AI Chat Assistant)

A full-stack AI-powered educational chatbot application with content based on academic curriculum for grades 10-12.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Data Security](#data-security)
- [Deployment](#deployment)
- [Team](#team)

## Overview

This Educational AI Chat Assistant is designed to provide academic support for students in grades 10-12. The application leverages large language models combined with a RAG (Retrieval-Augmented Generation) system to deliver accurate curriculum-aligned responses to student queries. It features a clean, responsive UI, secure authentication, and activity tracking to boost student engagement.

## Features

- **Personalized Academic Support**: Provides curriculum-aligned assistance for grades 10-12
- **Subject-Specific Knowledge**: Specialized knowledge for various academic subjects
- **Secure Authentication**: JWT-based authentication system
- **Engagement Tracking**: Activity streaks and engagement metrics
- **Chat History**: Persistent conversation history
- **Data Encryption**: End-to-end encryption of chat data
- **Responsive UI**: Mobile and desktop friendly interface
- **User Profile Management**: Customizable user settings
- **Clear Activity Option**: Allows users to reset their data and chat history

## System Architecture

The application follows a client-server architecture with the following components:

1. **Frontend**: Next.js 14-based React application with Tailwind CSS for styling
2. **Backend**: Flask API server with multiple endpoints for authentication, chat, and user management
3. **Database**: MongoDB for data storage
4. **LLM Service**: Integration with local Ollama models
5. **Retrieval System**: Vector database for retrieving relevant curriculum content

```yaml
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │ <──> │   Backend   │ <──> │  Database   │
│  (Next.js)  │      │   (Flask)   │      │  (MongoDB)  │
└─────────────┘      └──────┬──────┘      └─────────────┘
                            │
                    ┌───────┴───────┐
                    │  LLM Service  │
                    │   (Ollama)    │
                    └───────────────┘
```

## Technologies Used

### Frontend

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- React Icons
- JWT Authentication

### Backend

- Python 3.10+
- Flask
- JWT Authentication
- MongoDB (PyMongo)
- Ollama Integration
- Custom Encryption System

### Database

- MongoDB

## Prerequisites

- Node.js 18.0+
- Python 3.10+
- MongoDB
- Ollama with required models

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/educational-ai-chat.git
cd educational-ai-chat
```

### Backend Setup

1. Navigate to the backend directory:

```bash
cd code/chat_app/backend
```

2. Create and activate a virtual environment:

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables (see [Environment Variables](#environment-variables) section)

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd ../frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create environment variables file (`.env.local`) with required configuration

## Environment Variables

### Backend (.env)

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/app_info
JWT_SECRET_KEY=your_very_secure_secret_key
FLASK_ENV=development
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Database Setup

1. Create a MongoDB database named `app_info`
2. Create the following collections:
   - `users`
   - `chats`

## Running the Application

### Backend

From the backend directory:

```bash
python index.py
```

The backend server will start at <http://localhost:5000>

### Frontend

From the frontend directory:

```bash
npm run dev
```

The frontend will start at <http://localhost:3000>

## API Documentation

### Authentication Endpoints

- `POST /register` - Register a new user
- `POST /login` - Authenticate user and get token
- `POST /logout` - Invalidate token
- `GET /user` - Get user profile

### Chat Endpoints

- `POST /generate` - Generate AI responses (streaming)
- `GET /api/chats` - Get all user chats
- `GET /api/chats/:chat_id` - Get a specific chat
- `POST /api/chats` - Create a new chat
- `DELETE /api/chats/:chat_id` - Delete a chat
- `PATCH /api/chats/:chat_id/rename` - Rename a chat

### User Management Endpoints

- `PUT /user` - Update user profile
- `DELETE /user` - Delete user account
- `PUT /api/user/username` - Update username
- `PUT /api/user/password` - Update password
- `PUT /api/user/grade` - Update grade
- `POST /api/user/activity` - Update user activity
- `POST /api/user/clear-activity` - Clear user activity data

## Testing

Run backend tests:

```bash
cd code/chat_app/backend
pytest
```

Run frontend tests:

```bash
cd code/chat_app/frontend
npm test
```

## Project Structure

```
code/
├── chat_app/
│   ├── backend/           # Flask API server
│   │   ├── encryption.py  # Encryption utilities
│   │   ├── index.py       # Main application file
│   │   └── retrieval.py   # Vector database retrieval
│   └── frontend/          # Next.js frontend
│       ├── app/           # Next.js pages/routes
│       │   ├── chat/      # Chat interface
│       │   ├── login/     # Login page
│       │   ├── profile/   # User profile page
│       │   └── register/  # Registration page
│       ├── components/    # Reusable React components
│       ├── lib/           # Utility functions
│       └── styles/        # CSS styles
├── extracted_text/        # Curriculum content for vector DB
└── vectorizing_text/      # Scripts for vector embedding
```

## Data Security

1. **Chat data encryption**: All chat messages are encrypted in the database
2. **Password hashing**: User passwords are hashed using bcrypt
3. **JWT authentication**: Secure token-based authentication
4. **Token expiration**: Access tokens expire after 24 hours
5. **Token blacklisting**: Tokens are invalidated on logout

## Deployment

### Production Environment Variables

For a production deployment, set these additional environment variables:

```
NODE_ENV=production
FLASK_ENV=production
JWT_SECRET_KEY=<strong_random_key>
MONGO_URI=<production_mongodb_uri>
```

### Deploying with Docker

1. Build Docker images:

```bash
# Build backend
cd code/chat_app/backend
docker build -t edu-chat-backend .

# Build frontend
cd ../frontend
docker build -t edu-chat-frontend .
```

2. Run with Docker Compose:

Create a `docker-compose.yml` file in the root directory:

```yaml
version: '3'
services:
  backend:
    image: edu-chat-backend
    ports:
      - "5000:5000"
    environment:
      - MONGO_URI=mongodb://mongo:27017/app_info
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      - mongo

  frontend:
    image: edu-chat-frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:5000

  mongo:
    image: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

3. Start the services:

```bash
docker-compose up -d
```

### Alternative Deployment Options

- **Frontend**: Vercel, Netlify, AWS Amplify
- **Backend**: AWS Elastic Beanstalk, Heroku, Google Cloud Run
- **Database**: MongoDB Atlas

## Team

- Adithya Kishhor
- Anirudh Sankar
- Arnav Sharma
- Hardik Chadha
- Jatin Agrawal
