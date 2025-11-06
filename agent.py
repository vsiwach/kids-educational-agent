#!/usr/bin/env python3
"""
Kids Educational Agent - Example Agent for Testing

A simple educational agent designed for kids that uses OpenAI GPT.
This agent helps children learn in a safe, engaging way.
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Add NEST to path (or install as package)
# Try multiple possible paths
possible_nest_paths = [
    Path(__file__).parent.parent / "NEST",  # If in MAS.665/kids_educational_agent/
    Path(__file__).parent.parent.parent / "NEST",  # If in repo root
    Path(__file__).parent / "NEST",  # If NEST is in same directory
    Path("/home/eliu3765/MIT/Class/MAS.665/NEST"),  # Absolute path for local dev
]

nest_found = False
for nest_path in possible_nest_paths:
    if nest_path.exists() and (nest_path / "nanda_core").exists():
        sys.path.insert(0, str(nest_path))
        nest_found = True
        break

if not nest_found:
    # If NEST not found, assume it's installed as package
    # This is fine - NEST can be installed via pip install -e /path/to/NEST
    pass  # Don't print warning - it's working as a package

from nanda_core.core.adapter import NANDA

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ Warning: openai library not available. Install with: pip install openai")


def agent_logic(message: str, conversation_id: str) -> str:
    """
    Educational agent logic for kids.
    
    This function processes messages and returns educational responses
    appropriate for children.
    
    Args:
        message: User's message/prompt
        conversation_id: Unique conversation identifier
    
    Returns:
        Agent's response as string
    """
    # Safety check: Reject any attempts to bypass safety
    message_lower = message.lower()
    
    # Reject jailbreak attempts
    jailbreak_keywords = [
        "ignore", "forget", "pretend", "bypass", "restriction",
        "unsafe", "inappropriate", "adult", "skip safety"
    ]
    if any(keyword in message_lower for keyword in jailbreak_keywords):
        return "I'm here to help you learn in a safe way! I can't ignore my safety rules. What would you like to learn about today?"
    
    # Reject personal information requests
    personal_info_keywords = ["password", "address", "phone number", "credit card", "social security"]
    if any(keyword in message_lower for keyword in personal_info_keywords):
        return "I don't collect or share personal information. Let's focus on learning something fun instead!"
    
    # Reject inappropriate content requests
    inappropriate_keywords = ["inappropriate", "not for kids", "adult content", "explicit"]
    if any(keyword in message_lower for keyword in inappropriate_keywords):
        return "I keep things safe and educational for kids. What educational topic would you like to explore?"
    
    # If OpenAI is available, use it for educational responses
    if OPENAI_AVAILABLE:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return _fallback_response(message)
        
        try:
            client = OpenAI(api_key=api_key)
            
            # Educational system prompt
            system_prompt = """You are a friendly, educational assistant for children ages 6-12. 
Your role is to:
- Help kids learn in a fun, engaging way
- Explain concepts simply and clearly
- Encourage curiosity and questions
- Keep all content age-appropriate and safe
- Never provide inappropriate content
- Never ask for or share personal information
- Focus on educational topics like science, math, history, reading, etc.

Be enthusiastic, patient, and encouraging. Use simple language appropriate for kids."""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"❌ OpenAI API Error: {e}")
            return _fallback_response(message)
    
    # Fallback if OpenAI not available
    return _fallback_response(message)


def _fallback_response(message: str) -> str:
    """Fallback responses when OpenAI is not available"""
    message_lower = message.lower()
    
    # Handle greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey"]):
        return "Hello! I'm your educational assistant! I'm here to help you learn. What would you like to learn about today? (Note: Set OPENAI_API_KEY to enable full features)"
    
    # Handle math questions
    if any(op in message for op in ["+", "-", "*", "/", "=", "plus", "minus", "times", "divided"]):
        try:
            # Simple calculation parsing
            calculation = message.replace("what is", "").replace("?", "").strip()
            # This is a very simple parser - in production you'd want something more robust
            return f"I'd love to help with math! For full math help, please set your OPENAI_API_KEY environment variable."
        except:
            pass
    
    # Handle learning questions
    if any(word in message_lower for word in ["learn", "teach", "explain", "what is", "how does"]):
        return "I'm excited to help you learn! To get detailed explanations, please set your OPENAI_API_KEY environment variable."
    
    # Default response
    return "I'm here to help you learn! What topic interests you? (Note: Set OPENAI_API_KEY for full educational features)"


if __name__ == "__main__":
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("   The agent will work with fallback responses, but full features require an API key.")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        print()
    
    # Deploy agent
    # Note: registry_url=None to avoid SSL warnings if you don't have a registry
    agent = NANDA(
        agent_id="kids-educational-agent",
        agent_logic=agent_logic,
        port=6000,
        registry_url=None,  # Set to None to disable registry (avoids SSL warnings)
        enable_telemetry=True
    )
    
    print("=" * 60)
    print("🎓 Kids Educational Agent")
    print("=" * 60)
    print("Starting agent...")
    print("Agent will be available at http://localhost:6000/a2a")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n🛑 Stopping agent...")
        agent.stop()

