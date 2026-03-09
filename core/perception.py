class Perception:

    def __init__(self, max_inputs=10):
        """
        Initialise le buffer de perceptions.
        max_inputs : nombre maximum de messages à garder en mémoire.
        """
        self.inputs = []
        self.max_inputs = max_inputs

    def perceive(self, user_message):
        """
        Ajouter un stimulus perçu par Astra.
        """
        self.inputs.append(user_message)

        # limiter la taille du buffer
        if len(self.inputs) > self.max_inputs:
            self.inputs.pop(0)

    def get_latest_input(self):
        """
        Retourner la perception la plus récente.
        """
        return self.inputs[-1] if self.inputs else None

    def get_all_inputs(self):
        """
        Retourner toutes les perceptions récentes.
        """
        return self.inputs

    def clear_inputs(self):
        """
        Réinitialiser les perceptions.
        """
        self.inputs = []