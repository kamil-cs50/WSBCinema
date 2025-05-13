import sys  # Importuję moduł sys do obsługi argumentów wiersza poleceń i zakończenia aplikacji
from PyQt5.QtWidgets import QApplication  # Importuję klasę QApplication do utworzenia głównej aplikacji
from views.main_window import MainWindow  # Importuję klasę MainWindow z modułu views (główne okno GUI)
from utils.database import Database  # Importuję klasę Database do zarządzania danymi (wzorzec Singleton)
from models.movie import Movie  # Importuję klasę Movie do reprezentacji filmów
from models.cinema_hall import CinemaHall  # Importuję klasę CinemaHall do reprezentacji sal kinowych
from builders.screening_builder import ScreeningBuilder  # Importuję klasę ScreeningBuilder do tworzenia seansów (wzorzec Builder)
from datetime import datetime, timedelta  # Importuję klasy datetime i timedelta do obsługi dat i czasu

def load_sample_data():
    """Funkcja ładująca przykładowe dane do systemu"""
    db = Database()  # Tworzę instancję bazy danych (pobieram istniejącą instancję dzięki wzorcowi Singleton)
    
    # Przykładowe filmy, które otrzymały Oscara (zgodnie z wymaganiami)
    movies = [
        Movie("Oppenheimer", 180, 16),  # Tworzę film Oppenheimer (czas trwania 180 min, kategoria wiekowa 16+)
        Movie("Everything Everywhere All at Once", 139, 16),  # Tworzę film EEAAO (czas trwania 139 min, kategoria wiekowa 16+)
        Movie("CODA", 111, 12),  # Tworzę film CODA (czas trwania 111 min, kategoria wiekowa 12+)
        Movie("Nomadland", 107, 15),  # Tworzę film Nomadland (czas trwania 107 min, kategoria wiekowa 15+)
        Movie("Parasite", 132, 16),  # Tworzę film Parasite (czas trwania 132 min, kategoria wiekowa 16+)
        Movie("Anora", 115, 16),  # Tworzę film Anora (czas trwania 115 min, kategoria wiekowa 16+) - hipotetyczny Oscar 2025
    ]
    
    for movie in movies:
        db.add_movie(movie)  # Dodaję każdy film z listy do bazy danych
    
    # Przykładowe sale kinowe
    halls = [
        CinemaHall("Sala 1", 8, 10),  # Tworzę salę 1 (8 rzędów, 10 miejsc w rzędzie)
        CinemaHall("Sala 2", 10, 12),  # Tworzę salę 2 (10 rzędów, 12 miejsc w rzędzie)
        CinemaHall("Sala VIP", 6, 8),  # Tworzę salę VIP (5 rzędów, 8 miejsc w rzędzie, miejsca w tej sali mogą być droższe)
    ]
    
    for hall in halls:
        db.add_cinema_hall(hall)  # Dodaję każdą salę z listy do bazy danych
    
    # Tworzę budowniczego seansów (wzorzec Builder ułatwia tworzenie złożonych obiektów Screening)
    builder = ScreeningBuilder()
    
    # Bieżąca data, od której generowane będą seanse
    today = datetime.now().date()
    
    # Generuję seanse na najbliższe 7 dni, aby system miał początkowe dane
    for day_offset in range(7):
        current_date = today + timedelta(days=day_offset)  # Obliczam datę dla każdego dnia w zakresie
        
        # Seans poranny - przykład seansu z zastosowaniem wzorca Builder
        morning_time = datetime.combine(current_date, datetime.min.time().replace(hour=10, minute=0)) # Ustawiam godzinę 10:00
        db.add_screening(
            builder.set_movie(movies[0])  # Ustawiam film "Oppenheimer" dla tego seansu
                  .set_cinema_hall(halls[0])  # Ustawiam salę "Sala 1" dla tego seansu
                  .set_date_time(morning_time)  # Ustawiam datę i czas seansu
                  .set_base_price(20)  # Ustawiam cenę bazową biletu na 20 zł
                  .build()  # Buduję obiekt seansu na podstawie ustawionych parametrów
        )
        
        # Seans popołudniowy - kolejny przykład użycia wzorca Builder
        afternoon_time = datetime.combine(current_date, datetime.min.time().replace(hour=15, minute=30)) # Ustawiam godzinę 15:30
        db.add_screening(
            builder.set_movie(movies[1]) # Ustawiam film "Everything Everywhere All at Once"
                  .set_cinema_hall(halls[1]) # Ustawiam salę "Sala 2"
                  .set_date_time(afternoon_time) # Ustawiam datę i czas
                  .set_base_price(25) # Ustawiam cenę bazową na 25 zł
                  .build() # Buduję obiekt seansu
        )
        
        # Seans wieczorny - kolejny przykład użycia wzorca Builder
        evening_time = datetime.combine(current_date, datetime.min.time().replace(hour=20, minute=0)) # Ustawiam godzinę 20:00
        db.add_screening(
            builder.set_movie(movies[2]) # Ustawiam film "CODA"
                  .set_cinema_hall(halls[2]) # Ustawiam salę "Sala VIP"
                  .set_date_time(evening_time) # Ustawiam datę i czas
                  .set_base_price(30) # Ustawiam cenę bazową na 30 zł (sala VIP może mieć wyższą cenę bazową)
                  .build() # Buduję obiekt seansu
        )

def main():
    """Główna funkcja aplikacji, punkt wejścia"""
    db = Database()  # Pobieram instancję bazy danych (Singleton)

    load_sample_data()  # Najpierw ładuję przykładowe dane (filmy, sale, seanse)
    db.reset_all_seats()  # Dodaj to tutaj!
    db.load_reservations("reservations.json")  # Dopiero potem wczytuję rezerwacje

    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.aboutToQuit.connect(lambda: db.save_reservations("reservations.json"))
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()  # Uruchamiam funkcję main() tylko gdy skrypt jest wykonywany bezpośrednio (nie jest importowany jako moduł)

for seat in seats:
    seat.reserve()