import sys  # Zaimportowanie modułu sys do obsługi argumentów wiersza poleceń i zakończenia aplikacji
from PyQt5.QtWidgets import QApplication  # Zaimportowanie klasę QApplication do utworzenia głównej aplikacji
from views.main_window import MainWindow  # Zaimportowanie klasę MainWindow z modułu views (główne okno GUI)
from utils.database import Database  # Zaimportowanie klasę Database do zarządzania danymi (wzorzec Singleton)
from models.movie import Movie  # Zaimportowanie klasę Movie do reprezentacji filmów
from models.cinema_hall import CinemaHall  # Zaimportowanie klasę CinemaHall do reprezentacji sal kinowych
from builders.screening_builder import ScreeningBuilder  # Zaimportowanie klasę ScreeningBuilder do tworzenia seansów (wzorzec Builder)
from datetime import datetime, timedelta  # Zaimportowanie klasy datetime i timedelta do obsługi dat i czasu

def load_sample_data():
    """Funkcja ładująca przykładowe dane do systemu"""
    db = Database()  # Utworzenie instancję bazy danych (pobieram istniejącą instancję dzięki wzorcowi Singleton)
    
    # Przykładowe filmy, które otrzymały Oscara (zgodnie z wymaganiami)
    movies = [
        Movie("Oppenheimer", 180, 16),  # Utworzenie filmu Oppenheimer (czas trwania 180 min, kategoria wiekowa 16+)
        Movie("Everything Everywhere All at Once", 139, 16),
        Movie("CODA", 111, 12),
        Movie("Nomadland", 107, 15),
        Movie("Parasite", 132, 16),
        Movie("Anora", 115, 16),
    ]
    
    for movie in movies:
        db.add_movie(movie)  # Dodajnie każdego filmu z listy do bazy danych
    
    # Przykładowe sale kinowe
    halls = [
        CinemaHall("Sala 1", 8, 10),  # Utworzenie sali 1 (8 rzędów, 10 miejsc w rzędzie)
        CinemaHall("Sala 2", 10, 12),
        CinemaHall("Sala VIP", 6, 8),
    ]
    
    for hall in halls:
        db.add_cinema_hall(hall)  # Dodanie każdej sali z listy do bazy danych
    
    builder = ScreeningBuilder()
    
    today = datetime.now().date()
    
    # Generowanie seansu na najbliższe 7 dni, aby system miał początkowe dane
    for day_offset in range(7):
        current_date = today + timedelta(days=day_offset)  # Obliczenie daty dla każdego dnia w zakresie
        
        # Seans poranny - przykład seansu z zastosowaniem wzorca Builder
        morning_time = datetime.combine(current_date, datetime.min.time().replace(hour=10, minute=0)) # Ustawia godzinę 10:00
        db.add_screening(
            builder.set_movie(movies[0])  # Ustawia film "Oppenheimer" dla tego seansu
                  .set_cinema_hall(halls[0])  # Ustawia salę "Sala 1" dla tego seansu
                  .set_date_time(morning_time)  # Ustawia datę i czas seansu
                  .set_base_price(20)  # Ustawia cenę bazową biletu na 20 zł
                  .build()  # Buduję obiekt seansu na podstawie ustawionych parametrów
        )
        
        # Seans popołudniowy - kolejny przykład użycia wzorca Builder
        afternoon_time = datetime.combine(current_date, datetime.min.time().replace(hour=15, minute=30)) # Ustawia godzinę 15:30
        db.add_screening(
            builder.set_movie(movies[1])
                  .set_cinema_hall(halls[1])
                  .set_date_time(afternoon_time)
                  .set_base_price(25)
                  .build() 
        )
        
        # Seans wieczorny - kolejny przykład użycia wzorca Builder
        evening_time = datetime.combine(current_date, datetime.min.time().replace(hour=20, minute=0)) # Ustawia godzinę 20:00
        db.add_screening(
            builder.set_movie(movies[2])
                  .set_cinema_hall(halls[2])
                  .set_date_time(evening_time)
                  .set_base_price(30)
                  .build()
        )

def main():
    """Główna funkcja aplikacji, punkt wejścia"""
    db = Database()

    load_sample_data()  # Załadowanie przykładowych danych (filmy, sale, seanse)
    db.reset_all_seats()
    db.load_reservations("reservations.json")  # Wczytanie rezerwacji

    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.aboutToQuit.connect(lambda: db.save_reservations("reservations.json"))
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()  # Uruchamia funkcję main() tylko gdy skrypt jest wykonywany bezpośrednio (nie jest importowany jako moduł)

for seat in seats:
    seat.reserve()