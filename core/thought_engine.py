# core/thought_engine.py

class ThoughtEngine:
    """
    ThoughtEngine simule la réflexion interne d'Astra.
    Il analyse :
      - la personnalité
      - les émotions
      - la mémoire
      - le message utilisateur
    pour guider la réponse finale.
    """

    def __init__(self, personality, emotions, memory):
        self.personality = personality
        self.emotions = emotions
        self.memory = memory

    def think(self, user_message):
        """
        Retourne une réflexion interne sous forme de texte,
        utilisée ensuite pour générer la réponse finale.
        """

        # 1️⃣ Récupération des souvenirs récents
        recent_memories = self.memory.get_memories(limit=3)

        if recent_memories:
            memory_summary = "\n".join([m[0] for m in recent_memories])
        else:
            memory_summary = "Aucun souvenir pertinent."

        # 2️⃣ Analyse de l'émotion dominante
        dom_em = self.emotions.dominant_emotion()

        if dom_em:
            dom_em_text = f"{dom_em[1]} (catégorie : {dom_em[0]})"
        else:
            dom_em_text = "neutre"

        # 3️⃣ Analyse simple du message utilisateur
        message_analysis = []

        if "?" in user_message:
            message_analysis.append("L'utilisateur pose une question.")

        if len(user_message) > 80:
            message_analysis.append("Le message est assez long.")

        if not message_analysis:
            message_analysis.append("Conversation simple.")

        message_analysis_text = " ".join(message_analysis)

        # 4️⃣ Influence de la personnalité
        traits = self.personality.traits

        personality_influence = []

        if traits.get("curiosite", 50) > 60:
            personality_influence.append("Je pourrais poser une question en retour.")

        if traits.get("empathie", 50) > 60:
            personality_influence.append("Je dois être attentive à l'utilisateur.")

        if traits.get("fierte", 40) > 60:
            personality_influence.append("Je veux donner une réponse claire et sûre.")

        personality_text = " ".join(personality_influence) if personality_influence else "Répondre naturellement."

        # 5️⃣ Construction de la réflexion interne
        thought = f"""
Réflexion interne d'Astra :

Message utilisateur :
{user_message}

Analyse du message :
{message_analysis_text}

Souvenirs récents :
{memory_summary}

Émotion dominante :
{dom_em_text}

Influence de ma personnalité :
{personality_text}

Stratégie :
Répondre de manière naturelle et cohérente en tenant compte du contexte.
"""

        return thought.strip()