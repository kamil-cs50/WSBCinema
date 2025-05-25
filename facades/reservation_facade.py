from utils.database import Database  # Importuję klasę Database, która jest Singletonem przechowującym dane (fasada będzie z niej korzystać).
from models.reservation import Reservation  # Import klasy Reservation do tworzenia nowych rezerwacji.
from models.ticket import Ticket  # Import klasy Ticket do obsługi biletów.
from strategies.pricing_strategy import PricingContext, RegularPricingStrategy, WeekendPricingStrategy, MorningPricingStrategy  # Import strategii cenowych i kontekstu strategii.

class ReservationFacade:
    """
    Fasada dla systemu rezerwacji - wzorzec Facade.
    Ta klasa zapewnia uproszczony interfejs do złożonego podsystemu rezerwacji, ukrywając jego wewnętrzną logikę.
    """
    
    def __init__(self):
        """
        Inicjalizacja fasady rezerwacji.
        Konstruktor pobiera instancję bazy danych (Singleton), aby fasada miała dostęp do danych.
        """
        self.database = Database()  # Pobieram jedyną instancję bazy danych (Singleton).
    
    def get_available_screenings(self, date):
        """
        Zwraca dostępne seanse na podaną datę.
        Metoda fasady, która deleguje zapytanie o seanse do bazy danych.
        """
        # Wywołuję metodę get_screenings_for_date() na obiekcie bazy danych i zwracam jej wynik.
        return self.database.get_screenings_for_date(date)
    
    def get_available_seats(self, screening):
        """
        Zwraca listę dostępnych miejsc dla podanego seansu.
        Metoda fasady, która deleguje zapytanie o dostępne miejsca do obiektu seansu.
        """
        # Wywołuję metodę get_available_seats() na obiekcie screening i zwracam jej wynik.
        return screening.get_available_seats()
    
    def get_all_reservations(self):
        """
        Zwraca listę wszystkich rezerwacji.
        Metoda fasady, która deleguje zapytanie o wszystkie rezerwacje do bazy danych.
        """
        return self.database.get_reservations() # Wywołuję metodę get_reservations() na obiekcie bazy danych i zwracam jej wynik.

    def get_available_ticket_options(self, screening):
        """
        Zwraca słownik dostępnych opcji biletów (nazwa typu biletu jako klucz, fabryka jako wartość)
        dla danego seansu, w zależności od sali kinowej.
        """
        from factories.ticket_factory import RegularTicketFactory, DiscountedTicketFactory, VIPTicketFactory  # Importowanie fabryk biletów wewnątrz metody, aby uniknąć cyklicznych zależności.
        return {
            "Normalny": RegularTicketFactory(),
            "Ulgowy": DiscountedTicketFactory(),
            "VIP": VIPTicketFactory()
        }

    def calculate_price(self, screening, selected_seats, ticket_factory):
        """
        Oblicza łączną cenę rezerwacji na podstawie wybranych miejsc i typu biletu (fabryki).
        Metoda fasady, która oblicza cenę rezerwacji, używając fabryki biletów do stworzenia tymczasowych obiektów biletów.
        Przyjmuje obiekt seansu, listę wybranych miejsc oraz obiekt fabryki biletów (np. RegularTicketFactory).
        """
        tickets = []  # Tworzenie pustej listy na bilety.
        total_price = 0.0  # Inicjalizowanie sumy cen.
        for seat in selected_seats:  # Iterowanie przez każde wybrane miejsce.
            ticket = ticket_factory.create_ticket(screening, seat)  # Tworzenie biletu dla danego miejsca.
            tickets.append(ticket)  # Dodawanie biletu do listy.
            total_price += ticket.price  # Dodawanie ceny biletu do sumy.
        # Zwracam łączną cenę rezerwacji oraz listę utworzonych obiektów biletów.
        return total_price, tickets
    
    def make_reservation(self, customer_name, screening, selected_seats, tickets):
        """
        Tworzy nową rezerwację dla klienta.
        Metoda fasady, która tworzy obiekt rezerwacji, aktualizuje stan miejsc i dodaje rezerwację do bazy danych.
        Przyjmuje imię i nazwisko klienta, obiekt seansu, listę zarezerwowanych miejsc oraz listę utworzonych biletów.
        """
        # Tworzę nowy obiekt Reservation z podanymi danymi.
        reservation = Reservation(customer_name, screening, selected_seats, tickets)
        
        # Aktualizuję stan każdego zarezerwowanego miejsca na 'reserved'.
        # Sprawdzam, czy aktualny stan miejsca to FreeSeatState przed zmianą na ReservedState.
        from states.seat_state import ReservedSeatState, FreeSeatState # Importuję tutaj, aby uniknąć zależności cyklicznych na poziomie modułów
        for seat in selected_seats:
            if isinstance(seat.state, FreeSeatState): # Sprawdzam, czy aktualny stan to FreeSeatState.
                 seat.state = ReservedSeatState() # Zmieniam stan miejsca na ReservedSeatState.
        
        # Dodaję utworzoną rezerwację do bazy danych (co automatycznie zapisze rezerwacje do pliku JSON).
        self.database.add_reservation(reservation)
        # Zwracam utworzony obiekt rezerwacji.
        return reservation