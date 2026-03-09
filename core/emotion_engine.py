class EmotionEngine:

    def __init__(self, emotions):
        self.emotions = emotions

    def update_emotion(self, event):
        """Met à jour les émotions selon un événement"""

        for category, changes in event.items():

            if category not in self.emotions:
                continue

            for emotion, value in changes.items():

                if emotion not in self.emotions[category]:
                    continue

                self.emotions[category][emotion] += value

                # clamp 0-100
                self.emotions[category][emotion] = max(
                    0,
                    min(100, self.emotions[category][emotion])
                )

    def decay_emotions(self, rate=1):
        """Les émotions redescendent lentement"""

        for category in self.emotions:
            for emotion in self.emotions[category]:

                value = self.emotions[category][emotion]

                if value > 0:
                    self.emotions[category][emotion] = max(0, value - rate)

    def dominant_emotion(self):
        """Retourne l’émotion dominante"""

        max_val = -1
        dom_cat = "neutre"
        dom_emotion = "neutre"

        for cat, emos in self.emotions.items():
            for e, v in emos.items():

                if v > max_val:
                    max_val = v
                    dom_cat = cat
                    dom_emotion = e

        return dom_cat, dom_emotion