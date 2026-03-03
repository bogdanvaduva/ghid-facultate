# llm_advisor_opensource.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

class OpenSourceLLMAdvisor:
    def __init__(self, specializations_data: List[Dict], model_name: str = "mistralai/Mistral-7B-Instruct-v0.1"):
        """
        Initialize with open-source LLM
        """
        self.specializations = specializations_data
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.conversation_history = []

    def generate_response(self, prompt: str, max_length: int = 500) -> str:
        """
        Generate response using the local LLM
        """
        # Format prompt based on model type
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"

        inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                do_sample=True,
                top_p=0.95
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the response part (after [/INST])
        response = response.split("[/INST]")[-1].strip()

        return response

    def get_recommendations(self, student_profile: Dict) -> str:
        """
        Get specialization recommendations
        """
        prompt = f"""
        As an academic advisor, recommend specializations for this student:
        
        Student Profile:
        - Skills: {student_profile.get('skills', [])}
        - Interests: {student_profile.get('interests', [])}
        - Personality: {student_profile.get('personality_traits', [])}
        - Career Goals: {student_profile.get('desired_careers', [])}
        
        Available specializations: {[s['name'] for s in self.specializations]}
        
        Provide:
        1. Top 3 recommendations with reasons
        2. How each matches their profile
        3. Career prospects for each
        """

        return self.generate_response(prompt, max_length=800)

    def chat(self, user_message: str) -> str:
        """
        Chat with the advisor
        """
        # Add context from specialization database
        context = f"Available specializations: {', '.join([s['name'] for s in self.specializations])}"

        prompt = f"""
        {context}
        
        Previous conversation: {self.conversation_history[-5:] if self.conversation_history else 'None'}
        
        Student: {user_message}
        
        Provide helpful, encouraging advice about academic specializations and careers.
        """

        response = self.generate_response(prompt)
        self.conversation_history.append({"user": user_message, "assistant": response})

        return response
