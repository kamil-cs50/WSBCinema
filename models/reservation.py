import uuid  # Import modułu uuid do generowania unikalnych identyfikatorów dla każdej rezerwacji.
from datetime import datetime  # Import klasy datetime do zapisywania czasu utworzenia rezerwacji.
from models.screening import Screening # Import klasy Screening, aby określić typ seansu.
from models.seat import Seat # Import klasy Seat, aby określić typ listy miejsc.
from models.ticket import Ticket # Import klasy Ticket, aby określić typ listy biletów.

class Reservation:
    """
    Klasa reprezentująca rezerwację w systemie WSBCinema.
    Przechowywanie informacji o kliencie, seansie, zarezerwowanych miejscach, biletach oraz łącznej cenie.
    """
    
    def __init__(self, customer_name: str, screening: Screening, seats: list[Seat], tickets: list[Ticket]):
        """
        Inicjalizacja obiektu rezerwacji.
        Konstruktor przyjmuje imię i nazwisko klienta, obiekt seansu, listę zarezerwowanych obiektów miejsc oraz listę obiektów biletów.
        Dodawanie adnotacji typów dla lepszej czytelności i statycznej analizy.
        """
        self.id: str = str(uuid.uuid4())  # Generowanie unikalnego identyfikatora rezerwacji przy użyciu uuid.uuid4() i konwertowanie go na string.
        self.customer_name: str = customer_name  # Przypisywanie imienia i nazwiska klienta.
        self.screening: Screening = screening  # Przypisywanie odniesienia do obiektu seansu, na który dokonano rezerwacji.
        self.seats: list[Seat] = seats  # Przypisywanie listy obiektów Seat, które zostały zarezerwowane w ramach tej rezerwacji.
        self.tickets: list[Ticket] = tickets  # Przypisywanie listy obiektów Ticket wygenerowanych dla tej rezerwacji.
        self.timestamp: datetime = datetime.now()  # Przypisywanie aktualnego czasu utworzenia rezerwacji.
        self.total_price: float = sum(ticket.price for ticket in tickets)  # Obliczanie łącznej ceny rezerwacji sumując ceny wszystkich biletów na liście.
    
    def __str__(self) -> str:
        """
        Metoda zwracająca tekstową reprezentację obiektu rezerwacji.
        Ta metoda formatuje informacje o rezerwacji w czytelny sposób.
        """
        seats_str = ", ".join([f"R{seat.row}M{seat.number}" for seat in self.seats]) # Formatowanie miejsc
        return f"{self.customer_name} | {self.screening} | Miejsca: {seats_str} | Cena: {self.total_price:.2f} zł"
    
    def to_dict(self) -> dict:
        """
        Metoda konwertująca obiekt Reservation na słownik.
        Ta metoda jest pomocnicza do serializacji obiektu Reservation do formatu JSON.
        """
        return {
            "id": self.id,  # Dodaję identyfikator rezerwacji do słownika.
            "customer_name": self.customer_name,  # Dodaję imię i nazwisko klienta.
            # Zmieniono zapis screening na ID filmu i sali oraz datę/godzinę, aby uniknąć problemów z serializacją obiektu
            "movie_title": self.screening.movie.title,
            "hall_name": self.screening.cinema_hall.name,
            "date_time": self.screening.date_time.isoformat(), # Zapisuję datę i czas w formacie ISO
            "seats": [{"row": seat.row, "number": seat.number} for seat in self.seats],  # Zapisuję listę miejsc jako listę słowników z numerem rzędu i miejsca.
            "total_price": self.total_price, # Dodaję całkowitą cenę
            "timestamp": self.timestamp.isoformat() # Dodaję znacznik czasu utworzenia
            # Nie zapisujemy bezpośrednio obiektów biletów, ponieważ ich stan może się zmieniać (np. przez dekoratory)
            # i lepiej jest odtworzyć cenę przy wczytywaniu lub wyświetlaniu.
        }

    @staticmethod
    def from_dict(data: dict, db) -> 'Reservation | None':
        """
        Metoda statyczna tworząca obiekt Reservation ze słownika (np. z danych JSON).
        Wymaga dostępu do bazy danych (db), aby znaleźć odpowiedni seans.
        """
        try:
            screening_date_time = datetime.fromisoformat(data['date_time'])
            # Wyszukujemy seans w bazie danych na podstawie tytułu filmu, nazwy sali i daty/czasu
            screening = db.find_screening(data['movie_title'], data['hall_name'], screening_date_time)
            
            if not screening:
                print(f"Ostrzeżenie: Nie znaleziono seansu dla rezerwacji ID: {data.get('id', 'brak')}. Pomijanie.")
                return None

            # Odtwarzamy obiekty miejsc na podstawie danych ze słownika i stanu miejsc w znalezionym seansie
            seats = []
            for seat_data in data['seats']:
                seat = screening.get_seat(seat_data['row'], seat_data['number'])
                if seat:
                    seats.append(seat)
                else:
                    print(f"Ostrzeżenie: Nie znaleziono miejsca R{seat_data['row']}M{seat_data['number']} dla rezerwacji ID: {data.get('id', 'brak')}. Pomijanie miejsca.")

            if not seats:
                print(f"Ostrzeżenie: Brak prawidłowych miejsc dla rezerwacji ID: {data.get('id', 'brak')}. Pomijanie rezerwacji.")
                return None

            # Tworzymy tymczasowe obiekty biletów - cena zostanie pobrana z total_price
            # W idealnym świecie, zapisywalibyśmy typ biletu i odtwarzali go przez fabrykę,
            # ale dla uproszczenia użyjemy zapisanej ceny całkowitej.
            # Zakładamy, że cena była równo podzielona między bilety (co nie zawsze jest prawdą przy różnych typach).
            num_tickets = len(seats)
            price_per_ticket = data['total_price'] / num_tickets if num_tickets > 0 else 0
            tickets = [Ticket(screening, seat, price_per_ticket) for seat in seats]

            reservation = Reservation(data['customer_name'], screening, seats, tickets)
            reservation.id = data['id'] # Przywracamy oryginalne ID
            reservation.timestamp = datetime.fromisoformat(data['timestamp']) # Przywracamy oryginalny timestamp
            reservation.total_price = data['total_price'] # Przywracamy oryginalną cenę

            # Ważne: Aktualizujemy stan miejsc w odtworzonym seansie na "zarezerwowane"
            for seat in seats:
                seat.reserve()  # Wywołaj bez argumentów!

            return reservation
        except KeyError as e:
            print(f"Błąd wczytywania rezerwacji: Brakujący klucz {e} w danych: {data}")
            return None
        except Exception as e:
            print(f"Nieoczekiwany błąd podczas wczytywania rezerwacji {data.get('id', 'brak')}: {e}")
            return None