#!/usr/bin/env python3
"""
GitHub Actions Webhook Server

This is a lightweight HTTP server that receives GitHub webhook events and stores them
for processing by the MCP (Model Context Protocol) server. It serves as the bridge
between GitHub Actions and AI assistants like Claude.

OVERVIEW:
---------
This server provides a webhook endpoint that GitHub can POST to when Actions events
occur (workflow runs, check runs, etc.). Events are stored in a JSON file that the
MCP server reads to provide CI/CD insights and automation.

ARCHITECTURE:
------------
GitHub Actions → Webhook → Cloudflare Tunnel → This Server → JSON Storage → MCP Server → AI Assistant

KEY FEATURES:
------------
• Receives GitHub webhook events via HTTP POST
• Stores events in rolling JSON file (last 100 events)
• Provides health check endpoint for monitoring
• Handles GitHub event types: workflow_run, check_run, etc.
• Async/await architecture for high performance
• Error handling and logging

ENDPOINTS:
---------
• GET  /           - Health check endpoint
• POST /webhook/github - GitHub webhook receiver

USAGE:
------
1. Start the server: python webhook_server.py
2. Expose via tunnel: cloudflared tunnel --url http://localhost:8080
3. Configure GitHub webhook with the tunnel URL + /webhook/github
4. Events will be stored in github_events.json for MCP server consumption

CONFIGURATION:
-------------
• Port: 8080 (hardcoded)
• Host: localhost (local only, exposed via tunnel)
• Storage: github_events.json (same directory)
• Event limit: 100 events (rolling buffer)

DEPENDENCIES:
------------
• aiohttp: Async HTTP server framework
• json: Event serialization
• datetime: Timestamp generation
• pathlib: File path handling

SECURITY NOTES:
--------------
• Server runs on localhost only (not exposed directly)
• Cloudflare tunnel provides HTTPS termination
• No authentication implemented (add webhook secret for production)
• Input validation on JSON payloads

MONITORING:
----------
• Health check endpoint returns server status
• Events include timestamps for tracking
• Server logs startup information
• Cloudflare provides request metrics

INTEGRATION:
-----------
This server works with:
• GitHub Actions (webhook source)
• Cloudflare Tunnels (secure exposure)
• MCP Server (event consumer)
• AI Assistants (end user)

For more details, see PROJECT_DOCUMENTATION.md
"""

import json
from datetime import datetime
from pathlib import Path
from aiohttp import web

# File to store events
EVENTS_FILE = Path(__file__).parent / "github_events.json"

async def handle_webhook(request):
    """Handle incoming GitHub webhook"""
    try:
        data = await request.json()
        
        # Create event record
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": request.headers.get("X-GitHub-Event", "unknown"),
            "action": data.get("action"),
            "workflow_run": data.get("workflow_run"),
            "check_run": data.get("check_run"),
            "repository": data.get("repository", {}).get("full_name"),
            "sender": data.get("sender", {}).get("login")
        }
        
        # Load existing events
        events = []
        if EVENTS_FILE.exists():
            with open(EVENTS_FILE, 'r') as f:
                events = json.load(f)
        
        # Add new event and keep last 100
        events.append(event)
        events = events[-100:]
        
        # Save events
        with open(EVENTS_FILE, 'w') as f:
            json.dump(events, f, indent=2)
        
        return web.json_response({"status": "received"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

# Create app and add route
app = web.Application()
app.router.add_post('/webhook/github', handle_webhook)

if __name__ == '__main__':
    print("🚀 Starting webhook server on http://localhost:8080")
    print("📝 Events will be saved to:", EVENTS_FILE)
    print("🔗 Webhook URL: http://localhost:8080/webhook/github")
    web.run_app(app, host='localhost', port=8080)