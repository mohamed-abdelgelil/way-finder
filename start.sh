#!/bin/bash
# Start the Egypt Travel Agent chatbot (backend + frontend)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🏛️  Way-Finder — Egypt Travel Agent"
echo "======================================"

# Activate venv
source "$SCRIPT_DIR/.venv/bin/activate"

# Start backend
echo "▶ Starting backend on http://localhost:8000 ..."
cd "$SCRIPT_DIR"
uvicorn backend.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --reload-dir backend \
  --reload-include "*.py" &
BACKEND_PID=$!

# Wait for backend to be ready
echo "  Waiting for backend..."
for i in $(seq 1 30); do
  if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "  ✅ Backend ready"
    break
  fi
  sleep 1
done

# Start frontend
echo "▶ Starting frontend on http://localhost:5173 ..."
cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "======================================"
echo "✅ App running at: http://localhost:5173"
echo "   Backend API:    http://localhost:8000"
echo "   Press Ctrl+C to stop both servers"
echo "======================================"

# Clean up on exit
trap "echo ''; echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM
wait
