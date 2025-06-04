.PHONY: start stop build logs clean init all setup_docker setup_nvidia

all: start

# Setup Docker and Docker Compose (Official Method)
setup_docker:
	@echo "Installing Docker (Official Method)..."
	# Update package index
	sudo apt-get update
	# Install prerequisites
	sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
	# Add Docker's official GPG key
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	# Set up stable repository
	echo "deb [arch=$$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	# Update package index
	sudo apt-get update
	# Install Docker Engine, CLI, and containerd
	sudo apt-get install -y docker-ce docker-ce-cli containerd.io
	# Install Docker Compose Plugin (Official Method)
	@echo "Installing Docker Compose Plugin..."
	sudo apt-get install -y docker-compose-plugin
	# Add current user to docker group
	@echo "Adding current user to docker group..."
	sudo usermod -aG docker $$USER
	@echo "Docker setup complete! Please log out and log back in for docker group changes to take effect."
	@echo "After re-login, test with: docker --version && docker compose version"

# Setup NVIDIA Container Toolkit
setup_nvidia:
	@echo "Installing NVIDIA Container Toolkit..."
	curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
	curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
	sudo apt-get update
	sudo apt-get install -y nvidia-container-toolkit
	# Configure Docker daemon
	sudo nvidia-ctk runtime configure --runtime=docker
	sudo systemctl restart docker
	@echo "NVIDIA Container Toolkit setup complete!"

# Start all services
start:
	docker compose up -d
	chmod +x ./create-model.sh
	@echo "Waiting for services to start..."
	@while ! curl -s http://localhost:11434; do sleep 5; done
	./create-model.sh
	@echo "Services started. App available at http://localhost:3000 and Ollama at http://localhost:11434"
	@echo "Use 'make logs' to follow logs"

# Stop all services
stop:
	docker compose down

# Build services
build:
	docker compose build

# View logs
logs:
	docker compose logs -f

# Remove containers, volumes, and database files
clean:
	docker compose down -v
	@echo "Services stopped and volumes removed"

# Restart services
restart: stop start
