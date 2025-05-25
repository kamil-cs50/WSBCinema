from datetime import datetime  # Zaimportowanie klasy datetime z modułu datetime do obsługi daty i czasu.
from models.screening import Screening  # Zaimportowanie klasy Screening, która jest obiektem budowanym przez ten budowniczy.

class ScreeningBuilder:
    """
    Budowniczy seansów - wzorzec Builder.
    Ta klasa umożliwia konstruowanie złożonych obiektów Screening krok po kroku, co jest przydatne przy wielu opcjonalnych parametrach.
    """
    
    def __init__(self):
        """
        Inicjalizacja obiektu budowniczego.
        Konstruktor wywołuje metodę reset(), aby przygotować budowniczego do nowego procesu budowania.
        """
        self.reset()  # Wywołanie metody reset(), aby ustawić wszystkie atrybuty na wartości początkowe (None).
    
    def reset(self):
        """
        Resetuje wszystkie atrybuty budowniczego do stanu początkowego.
        Ta metoda czyści stan budowniczego, przygotowując go do budowania kolejnego obiektu seansu.
        """
        self.movie = None  # Reset atrybutu movie.
        self.cinema_hall = None 
        self.date_time = None  
        self.base_price = None  
    
    def set_movie(self, movie):
        """
        Ustawia obiekt filmu dla seansu.
        Ta metoda pozwala ustawić, który film będzie wyświetlany na seansie.
        """
        self.movie = movie  # Przypisanie podanego obiektu movie do atrybutu movie budowniczego.
        return self  # Zwraca referencję do samego siebie (self), aby umożliwić łańcuchowe wywoływanie metod (fluent interface).
    
    def set_cinema_hall(self, cinema_hall):
        """
        Ustawia obiekt sali kinowej dla seansu.
        Ta metoda pozwala ustawić, w której sali kinowej odbędzie się seans.
        """
        self.cinema_hall = cinema_hall  # Przypisanie podanego obiektu cinema_hall do atrybutu cinema_hall budowniczego.
        return self  # Zwraca self dla łańcuchowania.
    
    def set_date_time(self, date_time):
        """
        Ustawia datę i czas seansu.
        Ta metoda pozwala ustawić dokładny termin seansu.
        """
        self.date_time = date_time  # Przypisanie podanego obiektu date_time do atrybutu date_time budowniczego.
        return self
    
    def set_base_price(self, base_price):
        """
        Ustawia podstawową cenę biletu dla seansu.
        Ta metoda pozwala ustawić bazową cenę biletu dla tego seansu, która może być modyfikowana przez strategie cenowe i dekoratory.
        """
        self.base_price = base_price  # Przypisanie podanej ceny bazowej do atrybutu base_price budowniczego.
        return self 
    
    def build(self):
        """
        Tworzy i zwraca obiekt seansu na podstawie zebranych danych.
        Ta metoda finalizuje proces budowania i zwraca gotowy obiekt Screening.
        """
        # Sprawdzenie, czy wszystkie wymagane atrybuty (movie, cinema_hall, date_time, base_price) zostały ustawione przed próbą zbudowania obiektu.
        if not all([self.movie, self.cinema_hall, self.date_time, self.base_price]):
            # Jeśli brakuje któregoś z wymaganych atrybutów, zgłasza błąd ValueError z informacją o problemie.
            raise ValueError("Nie można utworzyć seansu: brakuje wymaganych atrybutów")
        
        # Tworzy nowy obiekt Screening, przekazując zebrane atrybuty z budowniczego do konstruktora klasy Screening.
        screening = Screening(self.movie, self.cinema_hall, self.date_time, self.base_price)
        self.reset()  # Reset budowniczego do stanu początkowego po zbudowaniu obiektu, aby był gotowy na budowanie kolejnego seansu.
        return screening  # Zwrócenie utworzonego obiektu Screening.