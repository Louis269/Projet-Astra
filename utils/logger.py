# core/logger.py
import datetime

class Logger:
    """
    Logger simple pour Astra.
    Enregistre les décisions et réponses dans un fichier ou affichage console.
    """

    def __init__(self, log_file="data/brain.log", console=True):
        self.log_file = log_file
        self.console = console

        # Crée le fichier si inexistant
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"\n--- Nouvelle session : {datetime.datetime.now()} ---\n")
        except Exception as e:
            print(f"Erreur création log: {e}")

    def log_decision(self, user_input, response, action_type):
        """
        Log une action ou une décision d'Astra.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Action: {action_type} | Input: {user_input} | Response: {response}\n"

        # Écriture dans le fichier
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Erreur écriture log: {e}")

        # Affichage console si activé
        if self.console:
            print(log_entry.strip())