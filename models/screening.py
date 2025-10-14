from datetime import datetime  # Import klasy datetime z modułu datetime do obsługi dat i czasu seansu.
from models.seat import Seat  # Import klasy Seat, która reprezentuje pojedyncze miejsce w sali.

class Screening:
    """
    Klasa reprezentująca seans filmowy w kinie WSBCinema.
    Agregowanie obiektów Movie, CinemaHall oraz listy obiektów Seat.
    Obiekt Screening łączy film, salę kinową i określony czas, tworząc konkretne wydarzenie, na które można kupić bilety.
    """
    
    def __init__(self, movie, cinema_hall, date_time, base_price):
        """
        Inicjalizacja obiektu seansu.
        Konstruktor przyjmuje obiekt filmu, obiekt sali kinowej, datę i czas seansu oraz podstawową cenę biletu.
        """
        self.movie = movie  # Przypisywanie obiektu filmu do atrybutu 'movie'.
        self.cinema_hall = cinema_hall  # Przypisywanie obiektu sali kinowej do atrybutu 'cinema_hall'.
        self.date_time = date_time  # Przypisywanie daty i czasu seansu do atrybutu 'date_time'.
        self.base_price = base_price  # Przypisywanie podstawowej ceny biletu do atrybutu 'base_price'.
        self.seats = self._initialize_seats()  # Wywoływanie prywatnej metody _initialize_seats() do stworzenia listy miejsc w sali dla tego seansu i przypisywanie jej do atrybutu 'seats'.

    def _initialize_seats(self):
        """
        Prywatna metoda inicjalizująca wszystkie miejsca w sali kinowej dla danego seansu.
        Tworzenie obiektów Seat dla każdego miejsca w sali, na podstawie wymiarów sali (liczby rzędów i miejsc w rzędzie).
        """
        seats = []  # Tworzenie pustej listy, która będzie przechowywać obiekty Seat.
        for row in range(1, self.cinema_hall.rows + 1):  # Iterowanie przez każdy rząd w sali kinowej (od 1 do liczby rzędów).
            for seat_num in range(1, self.cinema_hall.seats_per_row + 1):  # Iterowanie przez każde miejsce w danym rzędzie (od 1 do liczby miejsc w rzędzie).
                seats.append(Seat(row, seat_num))  # Tworzenie nowego obiektu Seat z numerem rzędu i miejsca i dodawanie go do listy 'seats'.
        return seats  # Zwracanie listy wszystkich utworzonych obiektów Seat.

    def get_available_seats(self):
        """
        Metoda zwracająca listę dostępnych miejsc (niezarezerwowanych i niesprzedanych).
        """
        return [seat for seat in self.seats if seat.is_available()]  # Zwracanie listy dostępnych miejsc.

    def find_seat(self, row, number):
        """
        Metoda wyszukująca konkretne miejsce po numerze rzędu i miejsca.
        Ta metoda pozwala znaleźć konkretny obiekt Seat w liście 'self.seats' na podstawie jego numeru rzędu i miejsca.
        """
        for seat in self.seats:  # Iterowanie przez wszystkie miejsca w liście 'self.seats'.
            if seat.row == row and seat.number == number:
                return seat  # Zwracanie obiektu Seat, jeśli znaleziono pasujące miejsce.
        return None  # Zwracanie None, jeśli nie znaleziono miejsca.

    def get_seat(self, row, number):
        """
        Alias do find_seat – zwracanie obiektu Seat o podanym rzędzie i numerze.
        """
        return self.find_seat(row, number)

    def __str__(self):
        """
        Metoda zwracająca tekstową reprezentację obiektu seansu.
        Zwracanie sformatowanego stringa z informacjami o filmie, sali i czasie seansu.
        """
        return f"{self.movie} w {self.cinema_hall.name} o {self.date_time.strftime('%d.%m.%Y %H:%M')}"