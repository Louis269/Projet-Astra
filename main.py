# main.py

from core.brain import Brain

def main():
    # Initialisation de l’IA
    brain = Brain(model_name="Qwen/Qwen2-1.5B-Instruct")
    print("Astra est prête ! Tapez 'quit' pour arrêter.\n")

    while True:
        # Entrée utilisateur
        user_input = input("Vous: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Astra: À bientôt !")
            break

        # Génération de réponse
        response, autonomous = brain.generate_reply(user_input)

        # Affichage
        print("Astra:", response)
        if autonomous:
            print("Astra (autonome):", autonomous)


if __name__ == "__main__":
    main()