class Evolution:

    def __init__(self, personality, emotion_engine):
        self.personality = personality
        self.emotion_engine = emotion_engine

    def evolve(self):
        dom_cat, dominant = self.emotion_engine.dominant_emotion()

        if dominant == "curiosite":
            self.personality.adjust_trait("curiosite", 1)

        elif dominant == "fierte":
            self.personality.adjust_trait("empathie", 1)

        elif dominant == "amusement":
            self.personality.adjust_trait("creativite", 1)

        elif dominant == "frustration":
            self.personality.adjust_trait("resilience", 1)

        # Optionnel : évolution naturelle avec un petit hasard
        # Cela permet de rendre l’IA moins prévisible
        import random
        for trait in self.personality.traits:
            if random.random() < 0.05:  # 5 % de chance
                self.personality.adjust_trait(trait, random.choice([-1, 1]))