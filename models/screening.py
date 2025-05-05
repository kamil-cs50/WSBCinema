from datetime import datetime  # Importuję klasę datetime z modułu datetime do obsługi dat i czasu seansu.
from models.seat import Seat  # Importuję klasę Seat, która reprezentuje pojedyncze miejsce w sali.

class Screening:
    """
    Klasa reprezentująca seans filmowy w kinie WSBCinema.
    Agreguje obiekty Movie, CinemaHall oraz listę obiektów Seat.
    Obiekt Screening łączy film, salę kinową i określony czas, tworząc konkretne wydarzenie, na które można kupić bilety.
    """
    
    def __init__(self, movie, cinema_hall, date_time, base_price):
        """
        Inicjalizacja obiektu seansu.
        Konstruktor przyjmuje obiekt filmu, obiekt sali kinowej, datę i czas seansu oraz podstawową cenę biletu.
        """
        self.movie = movie  # Przypisuję obiekt filmu do atrybutu 'movie'.
        self.cinema_hall = cinema_hall  # Przypisuję obiekt sali kinowej do atrybutu 'cinema_hall'.
        self.date_time = date_time  # Przypisuję datę i czas seansu do atrybutu 'date_time'.
        self.base_price = base_price  # Przypisuję podstawową cenę biletu do atrybutu 'base_price'.
        self.seats = self._initialize_seats()  # Wywołuję prywatną metodę _initialize_seats() do stworzenia listy miejsc w sali dla tego seansu i przypisuję ją do atrybutu 'seats'.
    
    def _initialize_seats(self):
        """
        Prywatna metoda inicjalizująca wszystkie miejsca w sali kinowej dla danego seansu.
        Ta metoda tworzy obiekty Seat dla każdego miejsca w sali, na podstawie wymiarów sali (liczby rzędów i miejsc w rzędzie).
        """
        seats = []  # Tworzę pustą listę, która będzie przechowywać obiekty Seat.
        for row in range(1, self.cinema_hall.rows + 1):  # Iteruję przez każdy rząd w sali kinowej (od 1 do liczby rzędów).
            for seat_num in range(1, self.cinema_hall.seats_per_row + 1):  # Iteruję przez każde miejsce w danym rzędzie (od 1 do liczby miejsc w rzędzie).
                seats.append(Seat(row, seat_num))  # Tworzę nowy obiekt Seat z numerem rzędu i miejsca i dodaję go do listy 'seats'.
        return seats  # Zwracam listę wszystkich utworzonych obiektów Seat.
    
    def get_available_seats(self):
        """
        Metoda zwracająca listę dostępnych miejsc dla danego seansu.
        Dostępne miejsca to te, których aktualny stan wskazuje na dostępność (np. FreeSeatState).
        """
        # Używam list comprehension do stworzenia nowej listy zawierającej tylko te obiekty Seat z listy 'self.seats', dla których metoda is_available() zwraca True.
        return [seat for seat in self.seats if seat.is_available()]
    
    def find_seat(self, row, number):
        """
        Metoda wyszukująca konkretne miejsce po numerze rzędu i miejsca.
        Ta metoda pozwala znaleźć konkretny obiekt Seat w liście 'self.seats' na podstawie jego numeru rzędu i miejsca.
        """
        # Iteruję przez wszystkie miejsca w liście 'self.seats'.
        for seat in self.seats:
            # Sprawdzam, czy numer rzędu i numer miejsca aktualnego obiektu Seat zgadzają się z podanymi argumentami.
            if seat.row == row and seat.number == number:
                return seat  # Jeśli znajdę pasujące miejsce, zwracam ten obiekt Seat.
        return None  # Jeśli żadne miejsce nie pasuje, zwracam None.
    
    def __str__(self):
        """
        Metoda zwracająca tekstową reprezentację obiektu seansu.
        Zwraca sformatowany string z informacjami o filmie, sali i czasie seansu.
        """
        # Zwracam sformatowany tekst, używając metod __str__ obiektów Movie i CinemaHall oraz formatując datę i czas.
        return f"{self.movie} w {self.cinema_hall.name} o {self.date_time.strftime('%d.%m.%Y %H:%M')}"