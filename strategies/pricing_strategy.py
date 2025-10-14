from abc import ABC, abstractmethod  # Import bazowych klas ABC i abstractmethod do tworzenia abstrakcyjnych klas i metod.
from datetime import datetime  # Import klasy datetime do obsługi daty i czasu (potrzebne do strategii cenowych zależnych od czasu).

class PricingStrategy(ABC):
    """
    Abstrakcyjna strategia cenowa - wzorzec Strategy.
    Definiowanie interfejsu dla wszystkich konkretnych strategii obliczania ceny biletu.
    """
    
    @abstractmethod
    def calculate_price(self, base_price: float) -> float:
        """
        Abstrakcyjna metoda obliczająca cenę biletu.
        Przyjmowanie podstawowej ceny biletu i zwracanie ceny po zastosowaniu strategii.
        """
        pass # Metoda abstrakcyjna bez implementacji.

class RegularPricingStrategy(PricingStrategy):
    """
    Standardowa strategia cenowa.
    Cena biletu równa cenie bazowej.
    """
    
    def calculate_price(self, base_price: float) -> float:
        """
        Obliczanie standardowej ceny biletu.
        Zwracanie ceny bazowej bez żadnych modyfikacji.
        """
        return base_price  # Zwracanie ceny bazowej.

class WeekendPricingStrategy(PricingStrategy):
    """
    Strategia cenowa na weekendy.
    Cena biletu podwyższona o 20% w weekendy.
    """
    
    def calculate_price(self, base_price: float) -> float:
        """
        Obliczanie ceny biletu w weekend (20% drożej).
        Zwracanie ceny bazowej powiększonej o 20%.
        """
        return base_price * 1.2  # Zwiększanie ceny bazowej o 20%.

class MorningPricingStrategy(PricingStrategy):
    """
    Strategia cenowa na poranne seanse.
    Cena biletu obniżona o 20% na poranne seanse.
    """
    
    def calculate_price(self, base_price: float) -> float:
        """
        Obliczanie ceny biletu na poranny seans (20% taniej).
        Zwracanie ceny bazowej pomniejszonej o 20%.
        """
        return base_price * 0.8  # Zmniejszanie ceny bazowej o 20%.

class PricingContext:
    """
    Kontekst dla strategii cenowej - wzorzec Strategy.
    Przechowywanie referencji do aktualnie używanej strategii cenowej i delegowanie do niej obliczenia ceny.
    """
    
    def __init__(self, strategy: PricingStrategy):
        """
        Inicjalizacja kontekstu z podaną strategią.
        """
        self.strategy = strategy  # Zapisywanie obiektu strategii cenowej.
    
    def set_strategy(self, strategy: PricingStrategy):
        """
        Zmiana aktualnej strategii cenowej.
        """
        self.strategy = strategy  # Ustawianie nowej strategii cenowej.
    
    def calculate_price(self, base_price: float) -> float:
        """
        Obliczanie ceny biletu używając aktualnej strategii.
        Delegowanie obliczenia ceny do obiektu strategii przechowywanego w kontekście.
        """
        return self.strategy.calculate_price(base_price)  # Wywoływanie metody calculate_price na aktualnej strategii.