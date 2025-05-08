.PHONY: start stop build logs clean init all setup

all: start

# Setup NVIDIA Container Toolkit
setup:
	curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
	curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
	sudo apt-get update
	sudo apt-get install -y nvidia-container-toolkit

# Start all services
start:
	docker compose up -d
	chmod +x ./create-model.sh
	@echo "Waiting for services to start..."
	@while ! curl -s http://localhost:11434; do sleep 5; done
	./create-model.sh
	@echo "Services started. Backend available at http://localhost:3000 and Ollama at http://localhost:11434"
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