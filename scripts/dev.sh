#!/bin/bash

# =============================================
# AI Viva Platform - Development Mode Runner
# =============================================
# Usage: ./scripts/dev.sh [command]
# Commands: start, stop, logs, restart, build

set -e

COMPOSE_FILE="docker-compose.dev.yml"
PROJECT_NAME="viva-dev"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[DEV]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

case "${1:-start}" in
    start)
        print_status "Starting development environment..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d
        
        print_status "Waiting for services to be ready..."
        sleep 5
        
        # Pull Mistral model if not already present
        print_status "Ensuring Mistral model is available..."
        docker exec viva-ollama ollama pull mistral 2>/dev/null || true
        
        print_status "Development environment is ready!"
        echo ""
        echo "  🚀 Backend API:  http://localhost:8000"
        echo "  📚 API Docs:     http://localhost:8000/docs"
        echo "  🧠 Ollama:       http://localhost:11434"
        echo "  📊 ChromaDB:     http://localhost:8001"
        echo ""
        print_status "Hot reload is enabled - edit files and see changes instantly!"
        ;;
    
    stop)
        print_status "Stopping development environment..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down
        print_status "Development environment stopped."
        ;;
    
    logs)
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f ${2:-}
        ;;
    
    restart)
        print_status "Restarting development environment..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME restart ${2:-}
        print_status "Restart complete!"
        ;;
    
    build)
        print_status "Rebuilding development containers..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME build --no-cache
        print_status "Build complete!"
        ;;
    
    shell)
        print_status "Opening shell in backend container..."
        docker exec -it viva-backend-dev /bin/bash
        ;;
    
    *)
        echo "Usage: $0 {start|stop|logs|restart|build|shell}"
        exit 1
        ;;
esac
