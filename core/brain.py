# core/brain.py
from core.perception import Perception
from core.memory import Memory
from core.emotion_engine import EmotionEngine
from core.reasoning import Reasoning
from core.personality import Personality
from core.evolution import Evolution
from autonomy.initiative import Initiative
from core.thought_engine import ThoughtEngine
from core.communication import Communication
from utils.logger import Logger

class Brain:
    def __init__(self, model_name="Qwen/Qwen2-3B-Instruct"):
        # Modules internes
        self.personality = Personality({"curiosite": 50, "empathie": 50, "fierte": 40})
        self.emotions = EmotionEngine({
            "positives": {"curiosite": 50, "fierte": 40, "amusement": 30},
            "negatives": {"frustration": 10, "jalousie": 0}
        })
        self.memory = Memory()
        self.perception = Perception()
        self.reasoning = Reasoning(self.emotions, self.personality, self.memory)
        self.evolution = Evolution(self.personality, self.emotions)
        self.communication = Communication(model_name)
        self.thought_engine = ThoughtEngine(self.personality, self.emotions, self.memory)
        self.initiative = Initiative(self)
        self.logger = Logger()

    def choose_style(self, user_message):
        """
        Retourne un style de réponse selon le message utilisateur.
        Pour l’instant, on fait simple : neutre, amical, ou humoristique.
        """
        # Exemple simple basé sur ponctuation et mots
        if "?" in user_message:
            return "Répond de manière amicale et curieuse :"
        if "!" in user_message:
            return "Répond de manière enthousiaste :"
        return "Répond de manière naturelle :"

    def _shorten_memory(self, text, max_chars=500):
        """Retourne une version condensée d'un texte de mémoire pour le prompt"""
        return text[-max_chars:] if len(text) > max_chars else text

    def receive_input(self, user_message):
        """Enregistre la perception"""
        self.perception.perceive(user_message)

    def get_memory_context(self, limit=5):
        """Retourne un résumé des souvenirs récents pour le contexte du modèle."""
        memories = self.memory.get_memories(limit=limit)
        if not memories:
            return ""
        context = ""
        for mem in memories:
            context += mem[0] + "\n"
        return context.strip()

    def generate_reply(self, user_message):
        """Pipeline complet de génération de réponse"""

        # 1️⃣ Enregistrer la perception
        self.receive_input(user_message)

        # 2️⃣ Réflexion interne
        internal_thought = self.thought_engine.think(user_message)

        # 3️⃣ Récupérer contexte mémoire
        memory_context = self.get_memory_context()

        # 4️⃣ Génération de la réponse
        response = self.communication.generate_response(
            user_message=user_message,
            traits=self.personality.traits,
            emotions=self.emotions.emotions,
            memory_context=memory_context,
            thoughts=internal_thought
        )

        # 5️⃣ Ajouter la réponse à la mémoire
        self.memory.add_memory("conversation", f"Utilisateur: {user_message}", self.emotions.emotions)
        self.memory.add_memory("conversation", f"Astra: {response}", self.emotions.emotions)

        # 6️⃣ Log de la décision
        self.logger.log_decision("réponse", response, "user_input")

        # 7️⃣ Vérifier initiative autonome
        autonomous = self.initiative.try_action()

        return response, autonomous