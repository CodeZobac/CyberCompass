build:
	docker build -t ai-compass .

run:
	docker run -p 11434:11434 ai-compass

dev:
	cd app && npm run dev

start: build run dev
	@echo "Starting AI Compass..."
	@echo "Access the application at http://localhost:3000"
	@echo "Press Ctrl+C to stop the application."