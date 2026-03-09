import random

class Initiative:
    def __init__(self, brain, cooldown=5):
        self.brain = brain
        self.cooldown = cooldown
        self.cycles_since_last_action = cooldown  # init pour permettre action immédiate

    def try_action(self):
        """
        L’IA décide de parler spontanément selon sa curiosité et cooldown.
        """
        self.cycles_since_last_action += 1

        curiosite = self.brain.personality.traits.get("curiosite", 50)
        chance = random.randint(0, 100)

        # Vérifie si la curiosité déclenche l'action et cooldown
        if chance < curiosite and self.cycles_since_last_action >= self.cooldown:
            self.cycles_since_last_action = 0

            # Générer un message autonome aléatoire
            prompts = [
                "Je me demande quelque chose...",
                "Tiens, une idée me vient !",
                "Je veux dire quelque chose de spontané.",
                "Curieux de savoir..."
            ]
            user_message = random.choice(prompts)

            # Récupère le contexte mémoire via méthode publique
            memory_context = self.brain.get_memory_context()

            # Génération réponse
            response = self.brain.communication.generate_response(
                user_message,
                self.brain.personality.traits,
                self.brain.emotions.emotions,
                memory_context
            )

            # Style et log
            style_instruction = self.brain.choose_style(user_message)
            response = f"{style_instruction} {response}".strip()

            self.brain.memory.add_memory("autonome", response, self.brain.emotions.emotions)
            self.brain.logger.log_decision("Autonome", response, "autonomous_action")

            return response

        return None