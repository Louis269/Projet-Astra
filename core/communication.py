# core/communication.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Communication:
    def __init__(self, model_name="Qwen/Qwen2-1.5B-Instruct"):
        """
        Initialise le tokenizer et le modèle Qwen.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Charger tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Charger modèle
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.model.to(self.device)

    def generate_response(self, user_message, personality, emotions, memory_context):
        """
        Génère une réponse basée sur le message utilisateur, la personnalité,
        les émotions et les souvenirs récents.
        """
        # Résumer traits essentiels
        traits_summary = (
            f"curiosité={personality.get('curiosite',50)}, "
            f"empathie={personality.get('empathie',50)}, "
            f"créativité={personality.get('creativite',50)}"
        )

        # Limiter aux 5 derniers souvenirs
        memory_text = "\n".join([m for m in memory_context.split('\n')[-5:]])

        # Prompt formaté pour Qwen (chat)
        prompt = f"""
<|system|>
You are Astra, an experimental AI assistant.
Traits: {traits_summary}
Recent memories: {memory_text}

<|user|>
{user_message}

<|assistant|>
"""

        # Tokenisation et génération
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            pad_token_id=self.tokenizer.eos_token_id
        )

        # Décoder la réponse
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Retourner texte nettoyé
        return response.strip()