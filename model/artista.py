from dataclasses import dataclass


@dataclass

class Artista():
    ArtistId: int
    Name: str
    pop: int
    # Usa questa scrittura per delle variabili che incrementi successivamente e che inizializzi a 0
    # quando crei l'oggetto
    pesoArchiEntranti: int = 0
    pesoArchiUscenti: int = 0

    def __hash__(self):
        return hash(self.ArtistId)

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId

    def __str__(self):
        return f"{self.Name} - ({self.ArtistId})"