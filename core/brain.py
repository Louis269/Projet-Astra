# core/brain.py
from langdetect import detect, DetectorFactory
import random

DetectorFactory.seed = 0  # pour cohérence de détection de langue

class Brain:
    def __init__(self, personality, emotions, memory, reasoning, communication,
                 evolution, initiative, thought_engine, logger):
        self.personality = personality
        self.emotions = emotions
        self.memory = memory
        self.reasoning = reasoning
        self.communication = communication
        self.evolution = evolution
        self.initiative = initiative
        self.thought_engine = thought_engine
        self.logger = logger

        # Historique des messages
        self.conversation_history = []

    # -------------------- Gestion messages --------------------
    def process_message(self, user_message: str):
        """
        Traite un message utilisateur : mise à jour émotionnelle,
        réflexion, décision, génération de réponse et log.
        """

        # 1️⃣ Mise à jour émotionnelle simple
        self.emotions.update_emotion({"joie": {"amusement": 5}})  # exemple d'événement

        # 2️⃣ Récupération du contexte mémoire
        memory_context = self.get_memory_context()

        # 3️⃣ Réflexion interne
        internal_thought = self.thought_engine.generate_thought(user_message)

        # 4️⃣ Décision stratégique
        action = self.reasoning.decide_action(user_message)

        # 5️⃣ Évolution autonome
        self.evolution.evolve()

        # 6️⃣ Déterminer style et ton
        style_instruction = self.choose_style(user_message)

        # 7️⃣ Génération réponse
        response = self.communication.generate_response(
            user_message,
            self.personality.traits,
            self.emotions.emotions,
            memory_context
        )

        # 8️⃣ Appliquer style
        response = f"{style_instruction} {response}".strip()

        # 9️⃣ Sauvegarder dans la mémoire
        self.memory.add_memory("conversation", user_message, self.emotions.emotions)
        self.conversation_history.append(user_message)

        # 🔟 Logger l’action
        self.logger.log_decision(user_message, response, action)

        return response

    # -------------------- Initiative autonome --------------------
    def try_initiative(self):
        """
        Tente une action autonome selon curiosité et cooldown.
        """
        return self.initiative.try_action()

    # -------------------- Style et ton --------------------
    def choose_style(self, user_message: str):
        """
        Détermine le style de réponse selon personnalité, émotions et langue détectée.
        """
        style = ""

        # Style selon curiosité
        if self.personality.traits.get("curiosite", 0) > 70:
            style += "Je me demande… "

        # Style selon joie
        if self.emotions.emotions.get("joie", {}).get("plaisir", 0) > 60:
            style += "😄 "

        # Détection automatique de la langue
        try:
            lang = detect(user_message)
            if lang == "en":
                style += "(In English) "
        except:
            pass

        return style.strip()

    # -------------------- Mémoire --------------------
    def get_memory_context(self, limit=5, char_limit=200):
        """
        Récupère les derniers souvenirs pour contextualiser la réponse.
        """
        recent_memories = self.memory.get_memories(limit)
        lines = [m[0][:char_limit] for m in recent_memories]
        return "\n".join(lines)

    # -------------------- Gestion des perceptions --------------------
    def perceive_input(self, user_message: str):
        """
        Méthode publique pour ajouter une perception.
        """
        if hasattr(self, "perception"):
            self.perception.perceive(user_message)
        else:
            # Cas où perception n'est pas injectée
            pass