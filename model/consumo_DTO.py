import datetime
from dataclasses import dataclass

'''
    DTO (Data Transfer Object) dell'entità Consumo
'''


@dataclass()
class Consumo:
    data: datetime.date
    kwh: int
    id_impianto: int

    def __eq__(self, other):
        return isinstance(other, Consumo) and self.data == other.data and self.id_impianto == other.id_impianto

    def __str__(self):
        return f"{self.data} | Consumo: {self.kwh} kWh | Impianto: {self.id_impianto}"

    def __repr__(self):
        return f"{self.data} | Consumo: {self.kwh} kWh | Impianto: {self.id_impianto}"
