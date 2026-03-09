# main.py
# Exemple complet pour lancer Astra

from core.personality import Personality
from core.memory import Memory
from core.reasoning import Reasoning
from core.emotion_engine import EmotionEngine
from core.perception import Perception
from core.evolution import Evolution
from core.autonomy.initiative import Initiative
from core.thought_engine import ThoughtEngine
from core.logger import Logger
from core.communication import Communication  # ton module pour le modèle

# -------------------- Initialisation des modules --------------------

# Traits de personnalité initiaux
traits = {
    "curiosite": 80,
    "empathie": 50,
    "fierte": 40
}
personality = Personality(traits)

# Émotions initiales
emotions_dict = {
    "joie": {"plaisir": 50, "amusement": 30},
    "tristesse": {"deception": 20},
    "colere": {"frustration": 10}
}
emotions = EmotionEngine(emotions_dict)

# Mémoire
memory = Memory(db_path="data/memory.db")

# Logger
logger = Logger(console=True)

# Communication (à adapter selon ton modèle HF)
communication = Communication(model_name="Qwen/Qwen2-1.5B-Instruct")  # exemple

# Reasoning
reasoning = Reasoning(emotions, personality, memory)

# Perception
perception = Perception(max_inputs=10)

# Evolution
evolution = Evolution(personality, emotions)

# ThoughtEngine
thought_engine = ThoughtEngine(memory, personality, emotions)

# Initiative
initiative = Initiative(None, cooldown=5)  # on l'initialisera avec Brain après

# -------------------- Initialisation de Brain --------------------
from core.brain import Brain

brain = Brain(
    personality=personality,
    emotions=emotions,
    memory=memory,
    reasoning=reasoning,
    communication=communication,
    evolution=evolution,
    initiative=initiative,
    thought_engine=thought_engine,
    logger=logger
)

# Injection de brain dans Initiative
initiative.brain = brain

# Injection de perception si besoin
brain.perception = perception

# -------------------- Boucle interactive simple --------------------
print("=== Astra est prête ! (tape 'quit' pour quitter) ===")

while True:
    user_input = input("Vous: ")
    if user_input.lower() in ["quit", "exit"]:
        print("Astra: À bientôt ! 👋")
        break

    # Ajouter la perception
    brain.perceive_input(user_input)

    # Réponse principale
    response = brain.process_message(user_input)
    print("Astra:", response)

    # Action autonome (facultative)
    auto_response = brain.try_initiative()
    if auto_response:
        print("Astra (autonome):", auto_response)