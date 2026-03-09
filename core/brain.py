# core/brain.py

from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


class Brain:

    def __init__(self, personality, emotions, memory, reasoning, communication, evolution, logger):

        self.personality = personality
        self.emotions = emotions
        self.memory = memory
        self.reasoning = reasoning
        self.communication = communication
        self.evolution = evolution
        self.logger = logger

        # historique conversation
        self.conversation_history = []

    def process_message(self, user_message: str):

        # 1️⃣ détecter la langue
        try:
            language = detect(user_message)
        except:
            language = "unknown"

        # 2️⃣ ajouter message utilisateur à l'historique
        self.conversation_history.append(f"User: {user_message}")

        # limiter historique (évite d'exploser le contexte)
        history_context = "\n".join(self.conversation_history[-6:])

        # 3️⃣ récupérer souvenirs
        recent_memories = self.memory.get_memories()

        memory_context = "\n".join([m[0] for m in recent_memories])

        # 4️⃣ raisonnement stratégique
        action = self.reasoning.decide_action(user_message)

        # 5️⃣ évolution (optionnel)
        if len(self.conversation_history) % 10 == 0:
            self.evolution.evolve()

        # 6️⃣ génération réponse via communication
        response = self.communication.generate_response(
            user_message,
            self.personality.traits,
            self.emotions.emotions,
            memory_context
        )

        # 7️⃣ ajouter réponse Astra à l'historique
        self.conversation_history.append(f"Astra: {response}")

        # 8️⃣ sauvegarde mémoire
        self.memory.add_memory(
            "conversation",
            user_message,
            self.emotions.emotions
        )

        # 9️⃣ log de décision
        self.logger.log_decision(user_message, response, action)

        return response