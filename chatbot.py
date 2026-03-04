# chatbot_app.py
# A complete chatbot application using the Ollama API
# Features: conversation history, streaming, system prompts, and model switching

import requests
import json
from typing import List, Dict, Optional, Generator

class OllamaChatbot:
    """
    A full-featured chatbot using the Ollama API.

    Supports conversation history, streaming responses, custom system prompts,
    and model switching.
    """

    def __init__(
            self,
            model: str = "llama3.2",
            system_prompt: Optional[str] = None,
            base_url: str = "http://localhost:11434",
    ):
        """
        Initialize the chatbot.

        Args:
            model: The default model to use
            system_prompt: Optional system prompt to set context
            base_url: The Ollama server URL
        """
        self.model = model
        self.base_url = base_url
        self.conversation: List[Dict] = []

        if system_prompt:
            self.conversation.append({
                "role": "system",
                "content": system_prompt
            })

    def set_model(self, model: str) -> None:
        """Switch to a different model."""
        self.model = model

    def clear_history(self) -> None:
        """Clear conversation history, keeping system prompt if present."""
        if self.conversation and self.conversation[0]["role"] == "system":
            self.conversation = [self.conversation[0]]
        else:
            self.conversation = []

    def chat(self, message: str, stream: bool = True) -> Generator[str, None, None]:
        """
        Send a message and yield response chunks.

        Args:
            message: The user's message
            stream: Whether to stream the response

        Yields:
            Response text chunks as they arrive
        """
        # Add user message to history
        self.conversation.append({
            "role": "user",
            "content": message
        })

        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": self.conversation,
            "stream": stream
        }

        if stream:
            # Stream the response
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()

            full_response = []

            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    content = chunk.get("message", {}).get("content", "")
                    full_response.append(content)
                    yield content

                    if chunk.get("done"):
                        break

            # Add assistant response to history
            self.conversation.append({
                "role": "assistant",
                "content": "".join(full_response)
            })
        else:
            # Get complete response
            response = requests.post(url, json=payload)
            response.raise_for_status()

            data = response.json()
            assistant_message = data["message"]["content"]

            self.conversation.append({
                "role": "assistant",
                "content": assistant_message
            })

            yield assistant_message

    def get_history(self) -> List[Dict]:
        """Get the full conversation history."""
        return self.conversation.copy()

    def save_history(self, filepath: str) -> None:
        """Save conversation history to a JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.conversation, f, indent=2)

    def load_history(self, filepath: str) -> None:
        """Load conversation history from a JSON file."""
        with open(filepath, "r") as f:
            self.conversation = json.load(f)


def main():
    """Interactive chatbot demo."""
    print("Ollama Chatbot")
    print("Commands: /clear, /model <name>, /save <file>, /load <file>, /quit")
    print("-" * 50)

    # Initialize chatbot with a system prompt
    bot = OllamaChatbot(
        model="llama3.2",
        system_prompt="You are a helpful assistant. Be concise but thorough."
    )

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else None

                if command == "/quit":
                    print("Goodbye!")
                    break
                elif command == "/clear":
                    bot.clear_history()
                    print("Conversation cleared.")
                elif command == "/model" and arg:
                    bot.set_model(arg)
                    print(f"Switched to model: {arg}")
                elif command == "/save" and arg:
                    bot.save_history(arg)
                    print(f"History saved to: {arg}")
                elif command == "/load" and arg:
                    bot.load_history(arg)
                    print(f"History loaded from: {arg}")
                else:
                    print("Unknown command")
                continue

            # Send message and stream response
            print("\nAssistant: ", end="", flush=True)
            for chunk in bot.chat(user_input):
                print(chunk, end="", flush=True)
            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")



