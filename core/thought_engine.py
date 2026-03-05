class ThoughtEngine:

    def __init__(self, emotions, personality, memory):
        self.emotions = emotions
        self.personality = personality
        self.memory = memory

    def think(self, user_message):
        thoughts = []

        # Observation du message
        thoughts.append(f"L'utilisateur a dit : {user_message}")

        # Influence de la curiosité
        if self.personality.traits.get("curiosite", 0) > 70:
            thoughts.append("Je suis curieuse, je pourrais poser une question.")

        # Influence des émotions
        if self.emotions.emotions.get("joie", {}).get("plaisir", 0) > 60:
            thoughts.append("Je me sens plutôt positive.")

        # Souvenir récent
        memories = self.memory.get_memories()
        if memories:
            thoughts.append("Cela me rappelle quelque chose que j'ai déjà vécu.")

        return " ".join(thoughts)