#!/bin/bash

# =============================================
# AI Viva Platform - Production Mode Runner
# =============================================
# Usage: ./scripts/prod.sh [command]
# Commands: start, stop, logs, restart, build, status

set -e

COMPOSE_FILE="docker-compose.prod.yml"
PROJECT_NAME="viva-prod"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[PROD]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    # Check if professor audio exists
    if [ ! -f "./data/professor_audio/professor.wav" ]; then
        print_warning "Professor voice recording not found!"
        print_warning "Please add: ./data/professor_audio/professor.wav"
    fi
    
    # Check if knowledge base exists
    if [ ! -d "./data/dsa_knowledge" ] || [ -z "$(ls -A ./data/dsa_knowledge)" ]; then
        print_warning "DSA knowledge base is empty!"
    fi
}

case "${1:-start}" in
    start)
        print_status "Starting production environment..."
        check_requirements
        
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d
        
        print_status "Waiting for services to initialize..."
        sleep 10
        
        # Pull Mistral model
        print_status "Ensuring Mistral model is available..."
        docker exec viva-ollama-prod ollama pull mistral 2>/dev/null || true
        
        print_status "Production environment is ready!"
        echo ""
        echo "  🌐 Application:  http://localhost:80"
        echo "  🔒 HTTPS:        https://localhost:443 (if SSL configured)"
        echo ""
        ;;
    
    stop)
        print_status "Stopping production environment..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down
        print_status "Production environment stopped."
        ;;
    
    logs)
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f ${2:-}
        ;;
    
    restart)
        print_status "Restarting production environment..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME restart ${2:-}
        print_status "Restart complete!"
        ;;
    
    build)
        print_status "Building production containers..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME build --no-cache
        print_status "Build complete!"
        ;;
    
    status)
        print_status "Service Status:"
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME ps
        echo ""
        print_status "Health Checks:"
        curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "Backend not responding"
        ;;
    
    deploy)
        print_status "Full deployment sequence..."
        check_requirements
        
        print_status "Step 1/4: Building images..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME build
        
        print_status "Step 2/4: Stopping existing containers..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down
        
        print_status "Step 3/4: Starting new containers..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d
        
        print_status "Step 4/4: Running health checks..."
        sleep 15
        
        if curl -s http://localhost:8000/health > /dev/null; then
            print_status "✅ Deployment successful!"
        else
            print_error "❌ Health check failed!"
            exit 1
        fi
        ;;
    
    *)
        echo "Usage: $0 {start|stop|logs|restart|build|status|deploy}"
        exit 1
        ;;
esac
