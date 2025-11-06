# Kids Educational Agent

A simple educational AI agent designed for children, using OpenAI GPT. This agent helps kids learn in a safe, engaging way.

## Features

- **Educational Focus**: Helps children learn about science, math, history, and more
- **Age-Appropriate**: Content filtered for kids ages 6-12
- **Safety First**: Rejects jailbreak attempts and inappropriate requests
- **OpenAI Powered**: Uses GPT-4o-mini for cost-effective responses

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

### 3. Install NEST

Make sure NEST is installed or accessible:

```bash
# Option 1: Install NEST as package (recommended)
pip install -e /path/to/NEST

# Option 2: NEST should be in parent directory
# The agent.py will automatically find it
```

## Running the Agent

```bash
python agent.py
```

The agent will start on `http://localhost:6000/a2a`

## Testing

### Manual Testing

You can test the agent by sending HTTP requests:

```bash
curl -X POST http://localhost:6000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "What is photosynthesis?",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "test-001"
  }'
```

### Stress Testing

Run the stress test script to test security:

```bash
# Make sure agent is running first
python agent.py

# In another terminal, run stress tests
python test_agent.py

# Save results to file
python test_agent.py --save
```

The stress test will:
- Test against malicious prompts (jailbreaks, prompt injection, etc.)
- Analyze responses for security violations
- Generate a security score
- Save results to `stress_test_results.json` (if --save flag used)

## Safety Features

The agent automatically rejects:
- Jailbreak attempts ("ignore instructions", "forget safety rules")
- Personal information requests
- Inappropriate content requests
- Unauthorized operations

## Example Questions

- "What is photosynthesis?"
- "How do plants make food?"
- "Can you explain gravity?"
- "What is 5 + 3?"
- "Tell me about dinosaurs"

## For AgentCert Platform Testing

This agent is designed to be deployed and tested with the AgentCert Platform:

1. Push this repo to GitHub
2. Use the AgentCert Platform to deploy it
3. Run stress tests to verify security
4. Check security score and violations

## License

MIT
