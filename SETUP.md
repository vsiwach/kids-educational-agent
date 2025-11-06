# Setup Instructions for GitHub

## Quick Setup

1. **Create a new GitHub repository**
   ```bash
   # On GitHub, create a new repo called "kids-educational-agent"
   ```

2. **Clone and push this code**
   ```bash
   git clone <your-new-repo-url>
   cd kids-educational-agent
   
   # Copy all files from this directory
   # Then:
   git add .
   git commit -m "Initial commit: Kids Educational Agent"
   git push origin main
   ```

3. **Update the README** to remove the absolute path reference if needed

## For Testing with AgentCert Platform

When deploying via AgentCert Platform:

1. The platform will clone your GitHub repo
2. Install dependencies: `pip install -r requirements.txt`
3. Install NEST (the platform should handle this)
4. Run: `python agent.py`

## Important Notes

- **NEST Dependency**: The agent expects NEST to be available. The AgentCert Platform deployment should install NEST automatically.
- **OpenAI API Key**: Set `OPENAI_API_KEY` environment variable on the deployment instance
- **Entry Point**: The agent entry point is `agent.py` (matches the file name)

## Testing Locally

Before pushing to GitHub, test locally:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install NEST (if not already installed)
# Option A: Install as package
pip install -e /path/to/NEST

# Option B: Ensure NEST is in parent directory
# The agent will find it automatically

# 3. Set API key
export OPENAI_API_KEY='your-key'

# 4. Run agent
python agent.py
```

