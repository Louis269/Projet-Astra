# core/communication.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class Communication:

    def __init__(self, model_name="microsoft/Phi-3-mini-4k-instruct"):
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
        """
        Génère une réponse d'Astra à partir du message utilisateur,
        de la mémoire pertinente et éventuellement de la pensée interne.
        """

        # --- Prompt optimisé ---
        prompt = f"""
Tu es Astra, une intelligence artificielle amicale, curieuse et naturelle.

Règles importantes :
- Réponds toujours en français
- Réponse courte (1 ou 2 phrases)
- Reste cohérente avec le message de l'utilisateur
- Ne parle jamais de toi comme d'un modèle IA

Mémoire pertinente :
{memory_context}

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
            max_new_tokens=60,
            temperature=0.5,
            top_p=0.85,
            repetition_penalty=1.2,
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id
        )

        # Décodage
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # --- Nettoyage post-génération ---
        def clean_response(self, text):
            """
            Nettoie la réponse générée par le modèle pour éviter :
            - répétitions
            - texte hors dialogue
            - réponses trop longues
            """

            # Supprimer les balises dialogue
            if "Astra :" in text:
                text = text.split("Astra :")[-1]

            if "Utilisateur :" in text:
                text = text.split("Utilisateur :")[0]

            if user_message.lower() in text.lower():
                text = "Peux-tu préciser ta question ?"

            # Nettoyer les espaces
            text = text.strip()

            # Séparer les phrases
            sentences = [s.strip() for s in text.split(".") if s.strip()]

            # Supprimer les phrases trop courtes
            sentences = [s for s in sentences if len(s.split()) >= 3]

            # Garder seulement 2 phrases maximum
            sentences = sentences[:2]

            # Reconstruction
            if sentences:
                text = ". ".join(sentences) + "."
            else:
                text = "Je ne suis pas sûr d'avoir bien compris."

            return text

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        response = self.clean_response(response)

        return response