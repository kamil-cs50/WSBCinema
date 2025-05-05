from abc import ABC, abstractmethod  # Importuję klasy bazowe ABC i abstractmethod do tworzenia abstrakcyjnych klas i metod.
from datetime import datetime  # Importuję klasę datetime do obsługi daty i czasu (potrzebne do strategii cenowych zależnych od czasu).

class PricingStrategy(ABC):
    """
    Abstrakcyjna strategia cenowa - wzorzec Strategy.
    Definiuje interfejs dla wszystkich konkretnych strategii obliczania ceny biletu.
    """
    
    @abstractmethod
    def calculate_price(self, base_price: float) -> float:
        """
        Abstrakcyjna metoda obliczająca cenę biletu.
        Przyjmuje podstawową cenę biletu i zwraca cenę po zastosowaniu strategii.
        """
        pass # Metoda abstrakcyjna bez implementacji.

class RegularPricingStrategy(PricingStrategy):
    """
    Standardowa strategia cenowa.
    Cena biletu jest równa cenie bazowej.
    """
    
    def calculate_price(self, base_price: float) -> float:
        """
        Oblicza standardową cenę biletu.
        Zwraca cenę bazową bez żadnych modyfikacji.
        """
        return base_price  # Zwracam cenę bazową.

class WeekendPricingStrategy(PricingStrategy):
    """
    Strategia cenowa na weekendy.
    Cena biletu jest podwyższona o 20% w weekendy.
    """
    
    def calculate_price(self, base_price: float) -> float:
        """
        Oblicza cenę biletu w weekend (20% drożej).
        Zwraca cenę bazową powiększoną o 20%.
        """
        return base_price * 1.2  # Zwiększam cenę bazową o 20%.

class MorningPricingStrategy(PricingStrategy):
    """
    Strategia cenowa na poranne seanse.
    Cena biletu jest obniżona o 20% na poranne seanse.
    """
    
    def calculate_price(self, base_price: float) -> float:
        """
        Oblicza cenę biletu na poranny seans (20% taniej).
        Zwraca cenę bazową pomniejszoną o 20%.
        """
        return base_price * 0.8  # Zmniejszam cenę bazową o 20%.

class PricingContext:
    """
    Kontekst dla strategii cenowej - wzorzec Strategy.
    Ta klasa przechowuje referencję do aktualnie używanej strategii cenowej i deleguje do niej obliczenie ceny.
    """
    
    def __init__(self, strategy: PricingStrategy):
        """
        Inicjalizacja kontekstu z podaną strategią.
        """
        self.strategy = strategy  # Zapisuję obiekt strategii cenowej.
    
    def set_strategy(self, strategy: PricingStrategy):
        """
        Zmienia aktualną strategię cenową.
        """
        self.strategy = strategy  # Ustawiam nową strategię cenową.
    
    def calculate_price(self, base_price: float) -> float:
        """
        Oblicza cenę biletu używając aktualnej strategii.
        Deleguje obliczenie ceny do obiektu strategii przechowywanego w kontekście.
        """
        return self.strategy.calculate_price(base_price)  # Wywołuję metodę calculate_price na aktualnej strategii.