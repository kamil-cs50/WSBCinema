import json # Importuję moduł json do pracy z danymi w formacie JSON (serializacja i deserializacja).
import os # Importuję moduł os do obsługi ścieżek plików i sprawdzania ich istnienia.
from models.reservation import Reservation # Importuję klasę Reservation, ponieważ będę ją serializować/deserializować.
# Importuję klasy modeli, które są agregowane w obiektach Database i Screening.
from models.movie import Movie
from models.cinema_hall import CinemaHall
from models.screening import Screening
from states.seat_state import FreeSeatState

class Database:
    """
    Singleton przechowujący dane aplikacji (filmy, sale, seanse, rezerwacje).
    Wzorzec Singleton zapewnia, że w całej aplikacji istnieje tylko jedna instancja tej klasy, co gwarantuje spójność danych.
    """
    
    _instance = None  # Prywatne pole statyczne, które będzie przechowywać jedyną instancję klasy Database.
    _is_initialized = False # Flaga pomocnicza do jednokrotnej inicjalizacji danych.
    
    def __new__(cls):
        """
        Metoda tworząca nową instancję klasy lub zwracająca istniejącą (implementacja wzorca Singleton).
        Ta specjalna metoda __new__ jest wywoływana przed __init__ i kontroluje tworzenie instancji.
        """
        if cls._instance is None:  # Sprawdzam, czy instancja klasy Database jeszcze nie istnieje (czy pole _instance jest None).
            # Jeśli instancja nie istnieje, tworzę nową instancję klasy bazowej (object) i przypisuję ją do _instance.
            cls._instance = super(Database, cls).__new__(cls)
            # Oznaczam, że instancja wymaga inicjalizacji danych.
            cls._is_initialized = False
        return cls._instance  # Zwracam jedyną instancję klasy Database.
    
    def _initialize(self):
        """
        Inicjalizuje struktury danych dla bazy danych, jeśli nie zostały jeszcze zainicjalizowane.
        Ta metoda jest wywoływana tylko raz, przy pierwszym tworzeniu instancji Singletonu.
        """
        if not self._is_initialized: # Sprawdzam, czy dane nie zostały już zainicjalizowane.
            self.movies = []  # Inicjalizuję pustą listę do przechowywania obiektów Movie.
            self.cinema_halls = []  # Inicjalizuję pustą listę do przechowywania obiektów CinemaHall.
            self.screenings = []  # Inicjalizuję pustą listę do przechowywania obiektów Screening.
            self.reservations = []  # Inicjalizuję pustą listę do przechowywania obiektów Reservation.
            self._is_initialized = True # Ustawiam flagę na True, aby zapobiec ponownej inicjalizacji.
    
    def __init__(self):
         """
         Konstruktor klasy Database.
         Ten konstruktor jest wywoływany za każdym razem, gdy próbujemy utworzyć instancję (choć zawsze zwraca tę samą instancję).
         Upewnia się, że dane są zainicjalizowane.
         """
         self._initialize() # Wywołuję metodę _initialize() aby upewnić się, że struktury danych są gotowe.

    def add_movie(self, movie):
        """
        Dodaje obiekt filmu do listy filmów w bazie danych.
        Metoda przyjmuje obiekt Movie i dodaje go do wewnętrznej listy filmów.
        """
        self.movies.append(movie)  # Dodaję obiekt movie do listy self.movies.
    
    def add_cinema_hall(self, cinema_hall):
        """
        Dodaje obiekt sali kinowej do listy sal w bazie danych.
        Metoda przyjmuje obiekt CinemaHall i dodaje go do wewnętrznej listy sal.
        """
        self.cinema_halls.append(cinema_hall)  # Dodaję obiekt cinema_hall do listy self.cinema_halls.
    
    def add_screening(self, screening):
        """
        Dodaje obiekt seansu do listy seansów w bazie danych.
        Metoda przyjmuje obiekt Screening i dodaje go do wewnętrznej listy seansów.
        """
        self.screenings.append(screening)  # Dodaję obiekt screening do listy self.screenings.
    
    def add_reservation(self, reservation):
        """
        Dodaje obiekt rezerwacji do listy rezerwacji w bazie danych.
        Metoda przyjmuje obiekt Reservation i dodaje go do wewnętrznej listy rezerwacji. Po dodaniu zapisuje rezerwacje do pliku.
        """
        self.reservations.append(reservation)  # Dodaję obiekt reservation do listy self.reservations.
        self.save_reservations("reservations.json") # Automatycznie zapisuję rezerwacje do pliku po dodaniu nowej.
    
    def get_movies(self):
        """
        Zwraca listę wszystkich filmów w bazie danych.
        Metoda zwraca wewnętrzną listę obiektów Movie.
        """
        return self.movies  # Zwracam listę self.movies.
    
    def get_cinema_halls(self):
        """
        Zwraca listę wszystkich sal kinowych w bazie danych.
        Metoda zwraca wewnętrzną listę obiektów CinemaHall.
        """
        return self.cinema_halls  # Zwracam listę self.cinema_halls.
    
    def get_screenings(self):
        """
        Zwraca listę wszystkich seansów w bazie danych.
        Metoda zwraca wewnętrzną listę obiektów Screening.
        """
        return self.screenings  # Zwracam listę self.screenings.
    
    def get_reservations(self):
        """
        Zwraca listę wszystkich rezerwacji w bazie danych.
        Metoda zwraca wewnętrzną listę obiektów Reservation.
        """
        return self.reservations  # Zwracam listę self.reservations.
    
    def get_screenings_for_date(self, date):
        """
        Zwraca listę seansów zaplanowanych na podaną datę.
        Metoda filtruje listę wszystkich seansów i zwraca tylko te, których data seansu zgadza się z podaną datą.
        """
        # Używam list comprehension do stworzenia nowej listy seansów, których data seansu (ignorując czas) jest równa podanej dacie.
        return [s for s in self.screenings if s.date_time.date() == date]

    def save_reservations(self, filepath):
        """
        Zapisuje listę rezerwacji do pliku JSON.
        Ta metoda serializuje listę obiektów Reservation do formatu JSON i zapisuje ją w podanym pliku.
        """
        # Tworzę listę słowników, konwertując każdy obiekt Reservation za pomocą metody to_dict().
        reservations_data = [r.to_dict() for r in self.reservations]
        try:
            # Otwieram plik w trybie zapisu ('w') z kodowaniem UTF-8.
            with open(filepath, 'w', encoding='utf-8') as f:
                # Zapisuję listę słowników do pliku w formacie JSON z wcięciami (indent=4) dla czytelności.
                json.dump(reservations_data, f, indent=4)
            # Wyświetlam komunikat potwierdzający zapis.
            print(f"Rezerwacje zapisane do {filepath}")
        except IOError as e:
            # W przypadku błędu wejścia/wyjścia (np. brak uprawnień), wyświetlam komunikat o błędzie.
            print(f"Błąd zapisu rezerwacji do {filepath}: {e}")

    def load_reservations(self, filepath):
        """
        Wczytuje listę rezerwacji z pliku JSON.
        Ta metoda odczytuje dane rezerwacji z pliku JSON i deserializuje je z powrotem do listy obiektów Reservation.
        """
        if not os.path.exists(filepath):
            # Sprawdzam, czy plik z rezerwacjami istnieje. Jeśli nie, przerywam ładowanie.
            print(f"Plik {filepath} nie istnieje, nie wczytano rezerwacji.")
            return

        try:
            # Otwieram plik w trybie odczytu ('r') z kodowaniem UTF-8.
            with open(filepath, 'r', encoding='utf-8') as f:
                # Wczytuję dane z pliku JSON do listy słowników.
                reservations_data = json.load(f)
            
            # Tworzę nową listę rezerwacji, deserializując każdy słownik za pomocą metody from_dict().
            # Przekazuję aktualną listę seansów, aby metoda from_dict mogła odtworzyć powiązania z seansami.
            self.reservations = [Reservation.from_dict(data, self) for data in reservations_data if Reservation.from_dict(data, self) is not None]
            # Wyświetlam komunikat potwierdzający wczytanie.
            print(f"Wczytano {len(self.reservations)} rezerwacji z {filepath}")
        except json.JSONDecodeError as e:
            # W przypadku błędu dekodowania JSON, wyświetlam komunikat o błędach.
            print(f"Błąd odczytu rezerwacji z {filepath}: Błąd formatu JSON - {e}")
        except IOError as e:
            # W przypadku błędu wejścia/wyjścia, wyświetlam komunikat o błędzie.
            print(f"Błąd odczytu rezerwacji z {filepath}: {e}")

    def find_screening(self, movie_title, hall_name, date_time):
        """
        Znajduje seans na podstawie tytułu filmu, nazwy sali i daty/czasu.
        """
        for screening in self.screenings:
            if (screening.movie.title == movie_title and
                screening.cinema_hall.name == hall_name and
                screening.date_time == date_time):
                return screening
        return None

    def reset_all_seats(self):
        for screening in self.screenings:
            for seat in screening.seats:
                seat.state = FreeSeatState()