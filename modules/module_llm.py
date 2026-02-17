"""
module_llm.py

LLM module for TalkMate AI.
Provides integration with OpenAI-compatible LLM backends.
"""
import requests
from modules.module_prompt import build_prompt

class LLMManager:
    """Manages LLM interactions."""
    
    def __init__(self, config, character_manager, memory_manager):
        self.config = config
        self.character_manager = character_manager
        self.memory_manager = memory_manager

    def get_completion(self, user_prompt):
        """
        Generate a completion using the configured LLM backend.
        
        Parameters:
        - user_prompt (str): The user's input prompt.
        
        Returns:
        - str: The generated completion.
        """
        prompt = build_prompt(
            user_prompt, self.character_manager, self.memory_manager, self.config
        )
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['LLM']['api_key']}"
        }
        
        llm_backend = self.config['LLM']['llm_backend']
        url, data = self._prepare_request_data(llm_backend, prompt)

        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            bot_reply = self._extract_text(response.json(), llm_backend)
            
            # Save to memory
            self.memory_manager.write_longterm_memory(user_prompt, bot_reply)
            
            return bot_reply
        
        except requests.RequestException as e:
            error_msg = f"LLM request failed: {e}"
            print(f"✗ {error_msg}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"✗ Error details: {error_detail}")
                except:
                    print(f"✗ Response text: {e.response.text}")
            return None

    def _prepare_request_data(self, llm_backend, prompt):
        """Prepare the request URL and data for the LLM backend."""
        if llm_backend == "openai":
            # Smart URL construction
            base = self.config['LLM']['base_url'].rstrip('/')
            if base.endswith('/v1'):
                # Already has /v1, just add endpoint
                url = f"{base}/chat/completions"
            else:
                # Need to add /v1/chat/completions
                url = f"{base}/v1/chat/completions"
            data = {
                "model": self.config['LLM']['openai_model'],
                "messages": [
                    {"role": "system", "content": self.config['LLM']['systemprompt']},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": self.config['LLM']['max_tokens'],
                "temperature": self.config['LLM']['temperature'],
                "top_p": self.config['LLM']['top_p']
            }
        elif llm_backend in ["ooba", "tabby"]:
            url = f"{self.config['LLM']['base_url']}/v1/completions"
            data = {
                "prompt": prompt,
                "max_tokens": self.config['LLM']['max_tokens'],
                "temperature": self.config['LLM']['temperature'],
                "top_p": self.config['LLM']['top_p']
            }
        else:
            raise ValueError(f"Unsupported LLM backend: {llm_backend}")

        return url, data

    def _extract_text(self, response_json, llm_backend):
        """Extract the generated text from the LLM response."""
        try:
            if 'choices' in response_json:
                if llm_backend == "openai":
                    return response_json['choices'][0]['message']['content'].strip()
                else:
                    return response_json['choices'][0]['text'].strip()
            else:
                raise KeyError("Invalid response format: 'choices' key not found.")
        except (KeyError, IndexError, TypeError) as error:
            return f"Text extraction failed: {str(error)}"
