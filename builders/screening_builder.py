from datetime import datetime  # Importuję klasę datetime z modułu datetime do obsługi daty i czasu.
from models.screening import Screening  # Importuję klasę Screening, która jest obiektem budowanym przez ten budowniczy.

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
        self.reset()  # Wywołuję metodę reset(), aby ustawić wszystkie atrybuty na wartości początkowe (None).
    
    def reset(self):
        """
        Resetuje wszystkie atrybuty budowniczego do stanu początkowego.
        Ta metoda czyści stan budowniczego, przygotowując go do budowania kolejnego obiektu seansu.
        """
        self.movie = None  # Resetuję atrybut movie.
        self.cinema_hall = None  # Resetuję atrybut cinema_hall.
        self.date_time = None  # Resetuję atrybut date_time.
        self.base_price = None  # Resetuję atrybut base_price.
    
    def set_movie(self, movie):
        """
        Ustawia obiekt filmu dla seansu.
        Ta metoda pozwala ustawić, który film będzie wyświetlany na seansie.
        """
        self.movie = movie  # Przypisuję podany obiekt movie do atrybutu movie budowniczego.
        return self  # Zwracam referencję do samego siebie (self), aby umożliwić łańcuchowe wywoływanie metod (fluent interface).
    
    def set_cinema_hall(self, cinema_hall):
        """
        Ustawia obiekt sali kinowej dla seansu.
        Ta metoda pozwala ustawić, w której sali kinowej odbędzie się seans.
        """
        self.cinema_hall = cinema_hall  # Przypisuję podany obiekt cinema_hall do atrybutu cinema_hall budowniczego.
        return self  # Zwracam self dla łańcuchowania.
    
    def set_date_time(self, date_time):
        """
        Ustawia datę i czas seansu.
        Ta metoda pozwala ustawić dokładny termin seansu.
        """
        self.date_time = date_time  # Przypisuję podany obiekt date_time do atrybutu date_time budowniczego.
        return self  # Zwracam self dla łańcuchowania.
    
    def set_base_price(self, base_price):
        """
        Ustawia podstawową cenę biletu dla seansu.
        Ta metoda pozwala ustawić bazową cenę biletu dla tego seansu, która może być modyfikowana przez strategie cenowe i dekoratory.
        """
        self.base_price = base_price  # Przypisuję podaną cenę bazową do atrybutu base_price budowniczego.
        return self  # Zwracam self dla łańcuchowania.
    
    def build(self):
        """
        Tworzy i zwraca obiekt seansu na podstawie zebranych danych.
        Ta metoda finalizuje proces budowania i zwraca gotowy obiekt Screening.
        """
        # Sprawdzam, czy wszystkie wymagane atrybuty (movie, cinema_hall, date_time, base_price) zostały ustawione przed próbą zbudowania obiektu.
        if not all([self.movie, self.cinema_hall, self.date_time, self.base_price]):
            # Jeśli brakuje któregoś z wymaganych atrybutów, zgłaszam błąd ValueError z informacją o problemie.
            raise ValueError("Nie można utworzyć seansu: brakuje wymaganych atrybutów")
        
        # Tworzę nowy obiekt Screening, przekazując zebrane atrybuty z budowniczego do konstruktora klasy Screening.
        screening = Screening(self.movie, self.cinema_hall, self.date_time, self.base_price)
        self.reset()  # Resetuję budowniczego do stanu początkowego po zbudowaniu obiektu, aby był gotowy na budowanie kolejnego seansu.
        return screening  # Zwracam utworzony obiekt Screening.