from dataclasses import dataclass
from model.country import Country

@dataclass
class Contiguity:
    state1: Country
    state2: Country

    def __hash__(self):
        return hash((self.state1, self.state2))
        # quando ci sono due chiavi primarie si ritornano gli hash in questo modo

    def __str__(self):
        return f"Confine tra {self.state1.StateNme} e {self.state2.StateNme}"