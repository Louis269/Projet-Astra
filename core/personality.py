class Personality:

    def __init__(self, traits):
        self.traits = traits

    def adjust_trait(self, trait_name, value):

        if trait_name not in self.traits:
            return

        self.traits[trait_name] += value

        # clamp 0–100
        self.traits[trait_name] = max(
            0,
            min(100, self.traits[trait_name])
        )

        return self.traits[trait_name]

    def get_traits(self):
        return self.traits