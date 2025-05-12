# Cyber Compass

Cyber Compass is an educational platform focused on teaching cyber ethics through interactive ethical dilemmas. The platform helps users develop critical thinking skills related to digital issues, online safety, privacy, and digital citizenship.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
  - [Setting up NVIDIA Container Toolkit](#setting-up-nvidia-container-toolkit)
  - [Docker and Docker Compose Setup](#docker-and-docker-compose-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [AI Model](#ai-model)
- [Multilingual Support](#multilingual-support)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## Project Overview

Cyber Compass is a web application that presents users with ethical dilemmas related to digital issues such as cyberbullying, deepfakes, catfishing, and disinformation. Users can select responses to these dilemmas and receive educational feedback from an AI assistant that evaluates their answers and provides constructive guidance.

## Features

- User registration and authentication
- Interactive ethical dilemmas with multiple-choice responses
- AI-powered educational feedback
- Progress tracking
- Multilingual support (English and Portuguese)
- Educational resources on cyber ethics topics

## Technology Stack

- **Frontend**: Next.js 15, React 19, TailwindCSS 4
- **UI**: [Buoucoding](https://ui.buoucoding.com)
- **Backend**: Next.js API routes
- **Authentication**: NextAuth.js
- **Database**: Supabase
- **AI**: Custom Ollama model based on ALIENTELLIGENCE/psychologistv2
- **Internationalization**: next-intl
- **Containerization**: Docker and Docker Compose

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [NVIDIA GPU](https://www.nvidia.com/) (recommended for optimal AI performance)
- [NVIDIA Drivers](https://www.nvidia.com/Download/index.aspx)

## Installation and Setup

### Setting up NVIDIA Container Toolkit

If you have an NVIDIA GPU, you'll need to set up the NVIDIA Container Toolkit to enable GPU acceleration for the AI model. Run:

```bash
make setup
```

This command will:
1. Add NVIDIA's GPG key to your system
2. Add the NVIDIA Container Toolkit repository
3. Update package lists
4. Install the NVIDIA Container Toolkit

### Docker and Docker Compose Setup

1. Clone this repository:
```bash
git clone https://github.com/CodeZobac/cyber-compass.git
cd cyber-compass
```

2. Build the Docker images:
```bash
make build
```

## Running the Application

To start all services (web application and AI model):

```bash
make start
```

This will:
- Start the Docker containers in detached mode
- Make the `create-model.sh` script executable
- Wait for services to start
- Create the custom AI model
- Display URLs for the application and Ollama service

To view logs from running containers:

```bash
make logs
```

To stop all services:

```bash
make stop
```

To restart services:

```bash
make restart
```

To clean up containers, volumes, and database files:

```bash
make clean
```

### Access the application

Once started, the application will be available at:
- Web application: http://localhost:3000
- Ollama AI service: http://localhost:11434

## Project Structure

- `/app` - Next.js application
  - `/app/app` - Application components and routes
  - `/app/components` - Reusable UI components
  - `/app/lib` - Utility functions and libraries
  - `/app/messages` - Internationalization files
- `/Modelfile` - Definition for the custom AI model
- `create-model.sh` - Script to create the AI model in Ollama
- `docker-compose.yml` - Docker Compose configuration
- `Makefile` - Commands for building and running the application

## AI Model

Cyber Compass uses a custom AI model based on ALIENTELLIGENCE/psychologistv2, specialized for evaluating ethical responses to digital dilemmas. The model is configured to:

- Evaluate user responses to ethical dilemmas
- Provide constructive feedback
- Explain ethical principles relevant to digital environments
- Support both English and Portuguese languages

## Multilingual Support

The application supports both English and Portuguese languages. Language files are stored in the `/app/messages` directory.

## Development

For development purposes, the Next.js application is mounted as a volume in the Docker container, enabling hot-reloading of changes made to the codebase.

To run the application in development mode outside of Docker:

```bash
cd app
npm install
npm run dev
```

## Troubleshooting

- **GPU Not Detected**: Ensure you have the latest NVIDIA drivers installed and that the NVIDIA Container Toolkit is properly configured.
- **Services Not Starting**: Check logs with `make logs` to identify any startup issues.
- **Model Creation Failing**: Ensure your system has enough resources (RAM and GPU memory) for the AI model.

---

For more information, please refer to the user stories in the `user_stories.md` file or contact the project maintainers.