# Cyber Compass

Cyber Compass is an educational platform focused on teaching cyber ethics through interactive ethical dilemmas. The platform helps users develop critical thinking skills related to digital issues, online safety, privacy, and digital citizenship.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
  - [Installing Make](#installing-make)
  - [Setting up Docker and Docker Compose](#setting-up-docker-and-docker-compose)
  - [Setting up NVIDIA Container Toolkit](#setting-up-nvidia-container-toolkit)
- [Running the Application](#running-the-application)
  - [Port Conflict Disclaimer](#port-conflict-disclaimer)
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

- [Make](https://www.gnu.org/software/make/) (for running setup scripts)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [NVIDIA GPU](https://www.nvidia.com/) (recommended for optimal AI performance)
- [NVIDIA Drivers](https://www.nvidia.com/Download/index.aspx)

## Installation and Setup

### Installing Make

**Official Make Installation for Ubuntu/Debian:**

```bash
# Update package index
sudo apt-get update

# Install build-essential which includes make
sudo apt-get install -y build-essential

# Verify installation
make --version
```

**Alternative installation methods:**

For other Linux distributions:
- **CentOS/RHEL/Fedora**: `sudo yum install make` or `sudo dnf install make`
- **Arch Linux**: `sudo pacman -S make`
- **macOS**: Install Xcode command line tools: `xcode-select --install`
- **Windows**: Install via [Chocolatey](https://chocolatey.org/): `choco install make`

### Setting up Docker and Docker Compose

**Automated Setup (Recommended):**

Use our automated setup script that follows Docker's official installation method:

```bash
make setup_docker
```

This command will:
1. Update package index
2. Install prerequisites (apt-transport-https, ca-certificates, curl, gnupg, lsb-release)
3. Add Docker's official GPG key
4. Set up the stable Docker repository
5. Install Docker Engine, CLI, and containerd
6. Install Docker Compose Plugin (official method)
7. Add current user to docker group

**Important:** After running this command, you must log out and log back in for the docker group changes to take effect.

**Manual Installation:**

If you prefer to install manually, follow the [official Docker installation guide](https://docs.docker.com/engine/install/ubuntu/) for your operating system.

### Setting up NVIDIA Container Toolkit

If you have an NVIDIA GPU, you'll need to set up the NVIDIA Container Toolkit to enable GPU acceleration for the AI model:

```bash
make setup_nvidia
```

This command will:
1. Add NVIDIA's GPG key to your system
2. Add the NVIDIA Container Toolkit repository
3. Update package lists
4. Install the NVIDIA Container Toolkit
5. Configure Docker daemon for NVIDIA runtime
6. Restart Docker service

### Project Setup

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

### Port Conflict Disclaimer

If you encounter the following error when running `make start`:

```
Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint cybercompass-ai-service-1 (e4d0462277da1eade52e5cb85ad4404767e8f1de2f77a43a561681789c486287): Bind for 0.0.0.0:11434 failed: port is already allocated
make: *** [Makefile:43: start] Error 1
```

This error occurs when port 11434 is already in use by another Ollama instance running on your system. The port conflict can be caused by either a system-wide Ollama installation or another Docker container using the same port.

#### Diagnostic Step

First, identify what's using port 11434:

```bash
sudo lsof -i :11434
```

If you see output like this, it means Docker containers are using the port:
```
COMMAND     PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
docker-pr 61032 root    7u  IPv4 615400      0t0  TCP *:11434 (LISTEN)
docker-pr 61038 root    7u  IPv6 615401      0t0  TCP *:11434 (LISTEN)
```

#### Resolution Steps

**For System-wide Ollama Installation:**

1. **Stop the Ollama service:**
   ```bash
   sudo systemctl stop ollama
   ```

2. **Disable it from starting automatically (optional):**
   ```bash
   sudo systemctl disable ollama
   ```

3. **Or kill any Ollama processes:**
   ```bash
   pkill ollama
   ```

**For Docker Container Conflicts:**

1. **List all running containers:**
   ```bash
   docker ps
   ```

2. **Stop containers using port 11434 (replace with actual container name/ID from `docker ps`):**
   ```bash
   docker stop container_name_or_id
   ```

3. **Or stop all containers if needed:**
   ```bash
   docker stop $(docker ps -q)
   ```

4. **Remove containers if they're not needed (replace with actual container name/ID):**
   ```bash
   docker rm container_name_or_id
   ```

**For Docker Compose conflicts:**

1. **Stop any other Docker Compose projects that might be using Ollama:**
   ```bash
   docker compose down
   ```

2. **In other project directories, check for running services:**
   ```bash
   cd /path/to/other/project && docker compose ps
   ```

#### Final Verification

1. **Verify port 11434 is free:**
   ```bash
   sudo lsof -i :11434
   ```

2. **If the port is still occupied, forcefully kill the process using the PID from the lsof output:**
   ```bash
   sudo kill -9 61032
   sudo kill -9 61038
   ```
   
   Replace `61032` and `61038` with the actual PIDs shown in your `lsof` output.

3. **Start the CyberCompass application:**
   ```bash
   make start
   ```

**Note:** The containerized Ollama service in this project needs exclusive access to port 11434 to function properly. Make sure no other Ollama instances (system-wide or containerized) are running before starting this application.

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

- **Make Command Not Found**: Install make using the instructions in the [Installing Make](#installing-make) section.
- **Docker Permission Denied**: Ensure you've logged out and logged back in after running `make setup_docker` to apply docker group membership.
- **GPU Not Detected**: Ensure you have the latest NVIDIA drivers installed and that the NVIDIA Container Toolkit is properly configured with `make setup_nvidia`.
- **Services Not Starting**: Check logs with `make logs` to identify any startup issues.
- **Model Creation Failing**: Ensure your system has enough resources (RAM and GPU memory) for the AI model.

---

For more information, please refer to the user stories in the `user_stories.md` file or contact the project maintainers.
