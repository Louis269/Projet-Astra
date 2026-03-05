# main.py
import json
from core.emotion_engine import EmotionEngine
from core.personality import Personality
from core.memory import Memory
from core.reasoning import Reasoning
from core.communication import Communication
from core.evolution import Evolution
from core.brain import Brain
from utils.logger import Logger

# 🔹 Chargement de la configuration
with open("data/config.json", encoding="utf-8") as f:
    config = json.load(f)

# 🔹 Initialisation des modules
emotions = EmotionEngine(config.get("emotions", {}))
personality = Personality(config.get("traits", {}))
memory = Memory()
reasoning = Reasoning(emotions, personality, memory)
communication = Communication(model_name="stabilityai/stablelm-tuned-alpha-7b")
evolution = Evolution(personality, emotions)
logger = Logger("astra_log.txt")  # Fichier de log

# 🔹 Création du "cerveau" Astra
astra_brain = Brain(personality, emotions, memory, reasoning, communication, evolution, logger)

print("Astra est prête. Tapez 'exit' pour quitter.")

# 🔹 Boucle principale d'interaction
while True:
    user_message = input("Vous : ")
    if user_message.lower() in ["exit", "quit"]:
        print("Astra : À bientôt ! 👋")
        break

    # 🔹 Traitement du message par Astra
    response = astra_brain.process_message(user_message)

    # 🔹 Affichage de la réponse et des traits actuels
    print(f"Astra : {response}")
    print(f"Traits actuels : {personality.traits}")