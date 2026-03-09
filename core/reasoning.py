class Reasoning:

    def __init__(self, emotion_engine, personality, memory):

        self.emotion_engine = emotion_engine
        self.personality = personality
        self.memory = memory

    def decide_action(self, user_message):

        # émotion dominante
        try:
            dom_cat, dom_emotion = self.emotion_engine.dominant_emotion()
        except:
            dom_cat, dom_emotion = "neutre", "neutre"

        # analyse simple du message
        question = "?" in user_message

        if question:
            return "repondre_question"

        if dom_emotion in ["curiosite", "etonement"]:
            return "poser_question"

        elif dom_emotion in ["fierte", "amusement"]:
            return "proposer_idee"

        elif dom_emotion in ["frustration", "jalousie"]:
            return "reflechir_avant_parler"

        else:
            return "repondre_normalement"