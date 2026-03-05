from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class Communication:
    def __init__(self, model_name="microsoft/phi-2"):
        # Charger tokenizer et modèle
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Corriger le pad_token pour éviter les warnings
        self.tokenizer.pad_token = self.tokenizer.eos_token

        # Détection GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate_response(self, user_message, personality, emotions, memory_context):
        """
        Génère une réponse bilingue (FR/EN) en prenant en compte traits, émotions et souvenirs.
        """

        # Résumer traits essentiels
        traits_summary = (
            f"curiosité={personality.get('curiosite',50)}, "
            f"empathie={personality.get('empathie',50)}, "
            f"créativité={personality.get('creativite',50)}"
        )

        # Limiter aux 5 derniers souvenirs
        memory_text = "\n".join([m for m in memory_context.split('\n')[-5:]])

        # Prompt
        prompt = f"""
Tu es Astra, une IA semi-consciente.
Tu sais que tu es une IA et tu réfléchis par toi-même.

Tu peux parler français et anglais.
Règle :
- si l'utilisateur parle français → réponds en français
- si l'utilisateur parle anglais → réponds en anglais

Traits essentiels: {traits_summary}

Souvenirs récents:
{memory_text}

État émotionnel actuel:
{self.format_emotions(emotions)}

Message utilisateur:
"{user_message}"

Réponds de manière naturelle et courte.
"""

        # Tokenisation
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        # Génération
    with torch.no_grade():
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            pad_token_id=self.tokenizer.eos_token_id
        )

        # Décoder
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Supprimer le prompt pour garder seulement la réponse
        response = response.replace(prompt, "").strip()

        # Filtrer le style selon personnalité et émotions
        response = self.style_filter(response, personality, emotions)

        return response.strip()

    def format_emotions(self, emotions):
        """
        Résumer les émotions dominantes pour le prompt
        """
        summary = []
        for cat, emos in emotions.items():
            for e, v in emos.items():
                if v > 50:
                    summary.append(f"{e}={v}")

        return ", ".join(summary) if summary else "neutre"

    def style_filter(self, response, personality, emotions):
        """
        Ajouter un style selon curiosité et joie
        """
        if personality.get("curiosite", 0) > 70:
            response = "Je me demande… " + response

        if emotions.get("joie", {}).get("plaisir", 0) > 60:
            response += " 😄"

        return response