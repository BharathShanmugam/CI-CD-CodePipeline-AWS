#!/bin/bash
echo "Restarting FastAPI server..."
pkill -f "uvicorn"
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &
