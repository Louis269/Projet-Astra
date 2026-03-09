# core/thought_engine.py

class ThoughtEngine:
    """
    Moteur de réflexion d'Astra : analyse les messages reçus,
    le contexte mémoire et propose des idées ou pensées internes.
    """

    def __init__(self, memory, personality, emotions):
        self.memory = memory
        self.personality = personality
        self.emotions = emotions

    def generate_thought(self, user_message: str):
        """
        Crée une pensée interne à partir d'un message utilisateur.
        """
        # Récupère les derniers souvenirs
        recent_memories = self.memory.get_memories(limit=5)
        memory_context = "\n".join([m[0] for m in recent_memories])

        # Exemple simple de réflexion : concatène traits, émotions et mémoire
        thought = f"Traits: {self.personality.traits}, Emotions: {self.emotions.emotions}\n"
        thought += f"Contexte: {memory_context}\n"
        thought += f"Réaction à l'entrée: {user_message}"

        return thought

    def evaluate_thoughts(self, thoughts_list):
        """
        Évalue les pensées et renvoie la plus pertinente (simple exemple : longueur minimale)
        """
        if not thoughts_list:
            return None
        # Choix simple : pensée la plus longue
        return max(thoughts_list, key=lambda t: len(t))