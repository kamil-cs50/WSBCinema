from utils.database import Database  # Importowanie klasy Database, która jest Singletonem przechowującym dane (fasada będzie z niej korzystać).
from models.reservation import Reservation  # Importowanie klasy Reservation, ponieważ fasada będzie tworzyć obiekty tego typu.
from models.seat import Seat  # Importowanie klasy Seat, ponieważ fasada będzie operować na miejscach.
from factories.ticket_factory import TicketFactory, RegularTicketFactory, DiscountedTicketFactory, VIPTicketFactory # Importowanie konkretnych fabryk biletów.

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
        self.database = Database()  # Pobieranie jedynej instancji bazy danych (Singleton).
    
    def get_available_screenings(self, date):
        """
        Zwraca dostępne seanse na podaną datę.
        Metoda fasady, która deleguje zapytanie o seanse do bazy danych.
        """
        # Wywoływanie metody get_screenings_for_date() na obiekcie bazy danych i zwracanie jej wyniku.
        return self.database.get_screenings_for_date(date)
    
    def get_available_seats(self, screening):
        """
        Zwraca listę dostępnych miejsc dla podanego seansu.
        Metoda fasady, która deleguje zapytanie o dostępne miejsca do obiektu seansu.
        """
        # Wywoływanie metody get_available_seats() na obiekcie screening i zwracanie jej wyniku.
        return screening.get_available_seats()
    
    def calculate_price(self, screening, seats, ticket_factory: TicketFactory):
        """
        Oblicza łączną cenę rezerwacji na podstawie wybranych miejsc i typu biletu (fabryki).
        Metoda fasady, która oblicza cenę rezerwacji, używając fabryki biletów do stworzenia tymczasowych obiektów biletów.
        Przyjmowanie obiektu seansu, listy wybranych miejsc oraz obiektu fabryki biletów (np. RegularTicketFactory).
        """
        total_price = 0  # Inicjalizowanie zmiennej do przechowywania łącznej ceny na 0.
        tickets = []  # Inicjalizowanie pustej listy do przechowywania obiektów biletów.
        
        for seat in seats:  # Iterowanie przez każde miejsce na liście wybranych miejsc.
            # Używanie podanej fabryki biletów do stworzenia obiektu biletu dla danego seansu i miejsca.
            ticket = ticket_factory.create_ticket(screening, seat)
            tickets.append(ticket)  
            total_price += ticket.price  # Dodawanie ceny utworzonego biletu do łącznej ceny.
        # Zwracanie łącznej ceny rezerwacji oraz listy utworzonych obiektów biletów.
        return total_price, tickets
    def make_reservation(self, customer_name, screening, seats, tickets):
        """
        Tworzy nową rezerwację dla klienta.
        Metoda fasady, która tworzy obiekt rezerwacji, aktualizuje stan miejsc i dodaje rezerwację do bazy danych.
        Przyjmowanie imienia i nazwiska klienta, obiektu seansu, listy zarezerwowanych miejsc oraz listy utworzonych biletów.
        """
        # Tworzenie nowego obiektu Reservation z podanymi danymi.
        reservation = Reservation(customer_name, screening, seats, tickets)
         
        # Sprawdzanie, czy aktualny stan miejsca to FreeSeatState przed zmianą na ReservedState.
        from states.seat_state import ReservedSeatState, FreeSeatState # Importowanie tutaj, aby uniknąć zależności cyklicznych na poziomie modułów
        for seat in seats:
            if isinstance(seat.state, FreeSeatState): # Sprawdzanie, czy aktualny stan to FreeSeatState.
                 seat.state = ReservedSeatState() 
        
        # Dodawanie utworzonej rezerwacji do bazy danych (co automatycznie zapisuje rezerwacje do pliku JSON).
        self.database.add_reservation(reservation)
        # Zwracanie utworzonego obiektu rezerwacji.
        return reservation

    def get_all_reservations(self):
        """
        Zwraca listę wszystkich rezerwacji.
        Metoda fasady, która deleguje zapytanie o wszystkie rezerwacje do bazy danych.
        """
        return self.database.get_reservations() # Wywoływanie metody get_reservations() na obiekcie bazy danych i zwracanie jej wyniku.

    def get_available_ticket_options(self, screening):
        """
        Zwraca słownik dostępnych opcji biletów (nazwa typu biletu jako klucz, fabryka jako wartość)
        dla danego seansu, w zależności od sali kinowej.
        """
        hall_name = screening.cinema_hall.name
        options = {}

        if hall_name == "Sala 1" or hall_name == "Sala 2":
            options["Normalny"] = RegularTicketFactory()
            options["Ulgowy"] = DiscountedTicketFactory()
        elif hall_name == "Sala VIP":
            options["VIP"] = VIPTicketFactory()
        # Można dodać domyślną obsługę lub zgłaszanie błędu, jeśli nazwa sali nie pasuje
        
        return options



