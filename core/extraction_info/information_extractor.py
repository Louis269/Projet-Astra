# core/extraction/information_extractor.py
import re

class InformationExtractor:

    def extract(self, message):
        message = message.lower()
        infos = {}

        # prénom
        match = re.search(r"je m'appelle (\w+)", message)
        if match:
            infos["prenom"] = match.group(1).capitalize()

        # préférences
        match = re.search(r"j'aime (.+)", message)
        if match:
            infos["aime"] = match.group(1)

        return infos