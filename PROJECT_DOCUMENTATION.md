# GitHub Actions Integration MCP Server - Complete Project Documentation

## 🎯 Project Overview

This project is a **Model Context Protocol (MCP) Server** that integrates GitHub Actions with AI assistants like Claude. It provides tools for analyzing pull requests, managing CI/CD workflows, and generating standardized reports through webhook integration.

### Key Features
- **PR Analysis**: Analyze git changes and suggest appropriate PR templates
- **GitHub Actions Integration**: Receive and process GitHub webhook events
- **CI/CD Monitoring**: Track workflow status and provide insights
- **Standardized Prompts**: Pre-built prompts for common CI/CD tasks
- **Real-time Webhook Processing**: Live event capture via Cloudflare tunnels

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub        │    │  Cloudflare      │    │  Local Server   │
│   Webhooks      │───▶│  Tunnel          │───▶│  (Port 8080)    │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │ github_events   │
                                               │ .json           │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │ MCP Server      │
                                               │ (server.py)     │
                                               │ Port varies     │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │ Claude/AI       │
                                               │ Assistant       │
                                               └─────────────────┘
```

## 📁 Project Structure

```
hf_mod_1/
├── server.py              # Main MCP server with tools and prompts
├── webhook_server.py      # GitHub webhook receiver
├── github_events.json    # Stored webhook events
├── pyproject.toml        # Project dependencies
├── README.md             # Basic setup instructions
├── test_server.py        # Test suite
├── validate_starter.py   # Validation script
└── PROJECT_DOCUMENTATION.md  # This file
```

## 🔧 Core Components

### 1. MCP Server (`server.py`)

The main server provides two categories of functionality:

#### **Module 1 Tools (PR Analysis)**
- `analyze_file_changes()`: Git diff analysis with truncation support
- `get_pr_templates()`: Retrieve available PR templates
- `suggest_template()`: AI-powered template recommendation

#### **Module 2 Tools (GitHub Actions)**
- `get_recent_actions_events()`: Fetch recent webhook events
- `get_workflow_status()`: Get current workflow states

#### **MCP Prompts (Standardized Workflows)**
- `analyze_ci_results()`: CI/CD health analysis
- `create_deployment_summary()`: Team deployment updates
- `generate_pr_status_report()`: Comprehensive PR reports
- `troubleshoot_workflow_failure()`: Systematic failure diagnosis

### 2. Webhook Server (`webhook_server.py`)

A lightweight aiohttp server that:
- Receives GitHub webhook events on `/webhook/github`
- Stores events in `github_events.json` (last 100 events)
- Provides health check endpoint on `/`
- Runs on `localhost:8080`

### 3. Event Storage (`github_events.json`)

JSON file storing webhook events with structure:
```json
{
  "timestamp": "ISO datetime",
  "event_type": "workflow_run|check_run|etc",
  "action": "completed|started|etc",
  "workflow_run": { /* GitHub workflow data */ },
  "check_run": { /* GitHub check data */ },
  "repository": "owner/repo",
  "sender": "username"
}
```

## 🚀 Setup and Installation

### Prerequisites
- Python 3.10+
- Git repository
- GitHub repository with Actions (for webhook testing)
- Cloudflared (for webhook exposure)

### Installation Steps

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Start Webhook Server**
   ```bash
   python webhook_server.py
   ```

3. **Start MCP Server**
   ```bash
   uv run server.py
   ```

4. **Expose Webhook (for GitHub integration)**
   ```bash
   cloudflared tunnel --url http://localhost:8080
   ```

### GitHub Webhook Configuration

1. Go to your GitHub repository → Settings → Webhooks
2. Add webhook with URL: `https://your-tunnel-url.trycloudflare.com/webhook/github`
3. Select events: `Workflow runs`, `Check runs`
4. Content type: `application/json`

## 🛠️ Tool Reference

### analyze_file_changes(base_branch, include_diff, max_diff_lines, working_directory)

Analyzes git changes between branches.

**Parameters:**
- `base_branch` (str): Branch to compare against (default: "main")
- `include_diff` (bool): Include full diff content (default: true)
- `max_diff_lines` (int): Maximum diff lines to return (default: 500)
- `working_directory` (str): Git repository path (auto-detected)

**Returns:** JSON with files changed, statistics, commits, and diff content

**Example Usage:**
```python
# Get changes with limited diff output
result = await analyze_file_changes(
    base_branch="develop",
    max_diff_lines=200
)
```

### get_recent_actions_events(limit)

Retrieves recent GitHub Actions events from webhook storage.

**Parameters:**
- `limit` (int): Maximum events to return (default: 10)

**Returns:** JSON array of recent events

### get_workflow_status(workflow_name)

Gets current status of GitHub Actions workflows.

**Parameters:**
- `workflow_name` (str, optional): Filter by specific workflow

**Returns:** JSON array of workflow statuses with latest state

## 📋 Prompt Reference

### analyze_ci_results()

Provides instructions for comprehensive CI/CD analysis.

**Output Format:**
- Overall health status
- Failed/successful workflows
- Actionable recommendations
- Trend analysis

### create_deployment_summary()

Generates team-friendly deployment updates.

**Output Format:**
- Deployment status (Success/Failed/In Progress)
- Environment and version info
- Key changes and issues
- Next steps

### generate_pr_status_report()

Creates detailed PR readiness reports.

**Output Format:**
- Code change analysis
- CI/CD status summary
- Template recommendations
- Risk assessment

### troubleshoot_workflow_failure()

Systematic workflow failure diagnosis.

**Output Format:**
- Failed workflow details
- Diagnostic information
- Possible causes (prioritized)
- Suggested fixes and investigation steps

## 🔄 Workflow Integration

### Typical Usage Patterns

1. **PR Review Workflow**
   ```
   analyze_file_changes() → suggest_template() → generate_pr_status_report()
   ```

2. **CI/CD Monitoring**
   ```
   get_workflow_status() → analyze_ci_results() → troubleshoot_workflow_failure()
   ```

3. **Deployment Process**
   ```
   get_recent_actions_events() → create_deployment_summary()
   ```

### Event Flow

1. **GitHub Action triggers** → Webhook sent to GitHub
2. **Cloudflare tunnel** → Routes to local webhook server
3. **Webhook server** → Stores event in JSON file
4. **MCP tools** → Read events from JSON file
5. **AI Assistant** → Processes data using prompts

## 🧪 Testing

### Manual Testing

1. **Test Webhook Reception**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"test": "data"}' \
        http://localhost:8080/webhook/github
   ```

2. **Test MCP Tools**
   ```bash
   # Start server and use Claude Code to call tools
   uv run server.py
   ```

3. **Test Cloudflare Tunnel**
   ```bash
   curl https://your-tunnel-url.trycloudflare.com/webhook/github
   ```

### Automated Testing

Run the test suite:
```bash
uv run pytest test_server.py -v
```

## 🔧 Configuration

### Environment Variables
- No environment variables required for basic operation
- GitHub webhook secret can be added for production security

### File Paths
- `EVENTS_FILE`: `./github_events.json` (configurable in both servers)
- `TEMPLATES_DIR`: `../../../templates` (relative to server.py)

### Port Configuration
- Webhook server: `8080` (hardcoded in webhook_server.py)
- MCP server: Auto-assigned by FastMCP

## 🚨 Troubleshooting

### Common Issues

1. **404 on Cloudflare URL**
   - Expected behavior for root path
   - Webhook endpoint should work: `/webhook/github`

2. **No Events Received**
   - Check GitHub webhook configuration
   - Verify Cloudflare tunnel is running
   - Check webhook server logs

3. **MCP Server Connection Issues**
   - Ensure FastMCP is properly installed
   - Check for port conflicts
   - Verify working directory access

4. **Git Command Failures**
   - Ensure running in git repository
   - Check branch names exist
   - Verify git is installed and accessible

### Debug Commands

```bash
# Check webhook server status
curl http://localhost:8080/

# Check stored events
cat github_events.json

# Test git commands
git diff --name-status main...HEAD

# Check running processes
ps aux | grep python
```

## 🔮 Future Enhancements

### Planned Features
- **Authentication**: GitHub webhook secret validation
- **Database Storage**: Replace JSON with proper database
- **Metrics**: Performance and usage analytics
- **Templates**: Dynamic PR template management
- **Notifications**: Slack/Teams integration
- **Multi-repo**: Support for multiple repositories

### Extension Points
- Additional webhook event types
- Custom prompt templates
- Integration with other CI/CD platforms
- Advanced workflow analysis
- Custom notification channels

## 📚 Dependencies

### Core Dependencies
- `mcp[cli]>=1.0.0`: Model Context Protocol framework
- `aiohttp>=3.10.0,<4.0.0`: Async HTTP server for webhooks

### Development Dependencies
- `pytest>=8.3.0`: Testing framework
- `pytest-asyncio>=0.21.0`: Async testing support

### External Tools
- `git`: Version control operations
- `cloudflared`: Tunnel creation for webhook exposure

## 📄 License and Usage

This project is part of the HuggingFace MCP training module. Refer to the course materials for usage guidelines and licensing information.

---

*Last updated: June 28, 2025*
*Version: 1.0.0*
