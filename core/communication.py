# core/communication.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Communication:

    def __init__(self, model_name="Qwen/Qwen2-3B-Instruct"):
        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Si pas de pad token, on le définit comme eos token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Modèle
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float32  # plus stable pour CPU
        )

    def generate_response(self, user_message, traits=None, emotions=None, memory_context="", thoughts=""):

        # Prompt renforcé
        prompt = f"""
        Tu es Astra, une intelligence artificielle amicale, curieuse et naturelle.

        Règles importantes :
        - réponds toujours en français
        - fais des phrases complètes
        - réponse courte (1 à 2 phrases maximum)
        - ne parle jamais de toi comme d'un modèle IA

        Mémoire récente :
        {memory_context}

        Pensée interne :
        {thoughts}

        Utilisateur : {user_message}
        Astra :
        """

        # Tokenization avec padding et attention mask
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        )

        # Génération
        outputs = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=120,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.15,
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id
        )

        # Décodage
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Nettoyage de la réponse
        if "Astra :" in response:
            response = response.split("Astra :")[-1]
        response = response.split("Astra :")[-1].strip()
        if "Utilisateur :" in response:
            response = response.split("Utilisateur :")[0]

        return response