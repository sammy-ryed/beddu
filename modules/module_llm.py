"""
module_llm.py

LLM module for TalkMate AI.
Provides integration with OpenAI-compatible LLM backends.
Enhanced with stress detection, financial analysis, and resource recommendation.
"""
import requests
from modules.module_prompt import build_prompt
from modules.module_stress_detector import SimpleStressDetector
from modules.module_financial import FinancialStressDetector
from modules.module_resources import ResourceManager

class LLMManager:
    """Manages LLM interactions with stress detection and financial analysis support."""
    
    def __init__(self, config, character_manager, memory_manager):
        self.config = config
        self.character_manager = character_manager
        self.memory_manager = memory_manager
        
        # Initialize stress detection and financial analysis
        self.stress_detector = SimpleStressDetector()
        self.financial_detector = FinancialStressDetector()
        self.resource_manager = ResourceManager()
        print("✓ Stress detection, financial analysis, and resources initialized")

    def get_completion(self, user_prompt):
        """
        Generate a completion using the configured LLM backend.
        Now includes stress detection, financial analysis, and resource recommendations.
        
        Parameters:
        - user_prompt (str): The user's input prompt.
        
        Returns:
        - str: The generated completion.
        """
        # Step 1: Detect stress in user's message
        stress_data = self.stress_detector.detect(user_prompt)
        
        # Step 2: Check for financial stress specifically
        financial_data = self.financial_detector.detect(user_prompt)
        
        # Step 3: Get appropriate resources if stress or crisis detected
        resources = None
        if stress_data.get('stress_detected') and stress_data.get('stress_level', 0) > 3:
            # Pass both stress and financial data to resource manager
            resources = self.resource_manager.get_resources(stress_data, financial_data)
        elif financial_data.get('has_financial_stress'):
            # Financial stress detected even if general stress wasn't
            resources = self.resource_manager.get_resources(
                {'stress_detected': True, 'stress_level': financial_data.get('stress_level', 5)},
                financial_data
            )
        
        # For crisis, we'll still let AI respond empathetically, but flag it
        is_crisis = stress_data.get('is_crisis', False)
        
        # Step 4: Build prompt with stress context (includes financial if detected)
        combined_context = stress_data.copy()
        if financial_data and financial_data.get('has_financial_stress'):
            combined_context['financial_stress'] = financial_data
        
        prompt = build_prompt(
            user_prompt, self.character_manager, self.memory_manager, self.config,
            stress_context=combined_context
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
            
            # Step 5: Append resources to response if available
            if resources:
                resource_text = self.resource_manager.format_resources_for_display(resources)
                if resource_text:
                    bot_reply += f"\n\n{resource_text}"
            
            # Step 5b: For crisis, always add urgent resources at the top
            if is_crisis:
                crisis_header = self.resource_manager.get_crisis_header()
                bot_reply = f"{crisis_header}\n\n{bot_reply}"
            
            # Step 6: Save to memory with stress tracking
            memory_context = stress_data.copy()
            if financial_data and financial_data.get('has_financial_stress'):
                memory_context['financial_stress'] = financial_data
            
            self.memory_manager.write_longterm_memory(user_prompt, bot_reply, memory_context)
            
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
