from dataclasses import dataclass

from model.artista import Artista


@dataclass

class Arco:
    a1: Artista
    a2: Artista
    peso: int

    def __hash__(self):
        return hash((self.a1, self.a2))

    def __eq__(self, other):
        return (self.a1, self.a2) == (other.a1, other.a2)




