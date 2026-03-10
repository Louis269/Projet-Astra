# core/thought_engine.py

class ThoughtEngine:
    """
    ThoughtEngine simule la réflexion interne d'Astra.
    Il analyse :
      - la personnalité
      - les émotions
      - la mémoire
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

        # Récupère les souvenirs récents
        recent_memories = self.memory.get_memories(limit=3)
        memory_summary = "\n".join([m[0] for m in recent_memories]) if recent_memories else "Aucun souvenir pertinent."

        # Analyse dominante des émotions
        dom_em = self.emotions.dominant_emotion()
        dom_em_text = f"{dom_em[1]} (catégorie : {dom_em[0]})" if dom_em else "neutre"

        # Réflexion interne
        thought = f"""
Réflexion interne :
- Utilisateur a dit : {user_message}
- Mémoire pertinente : {memory_summary}
- Émotion dominante : {dom_em_text}
- Traits de personnalité : {self.personality.traits}

Je dois répondre de manière cohérente et naturelle, 
en tenant compte de ma personnalité, de mes émotions et de mes souvenirs.
"""

        return thought.strip()