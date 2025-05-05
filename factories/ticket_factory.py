from abc import ABC, abstractmethod  # Importuję klasy bazowe ABC (Abstract Base Class) i abstractmethod do tworzenia abstrakcyjnych klas i metod.
from models.ticket import RegularTicket, DiscountedTicket, VIPTicket  # Importuję konkretne klasy biletów: RegularTicket, DiscountedTicket, VIPTicket.

class TicketFactory(ABC):
    """
    Abstrakcyjna fabryka biletów - wzorzec Factory Method.
    Ta klasa definiuje interfejs do tworzenia obiektów biletów, ale pozostawia implementację konkretnym podklasom fabryk.
    """
    
    @abstractmethod
    def create_ticket(self, screening, seat):
        """
        Abstrakcyjna metoda do tworzenia biletów.
        Każda konkretna fabryka musi zaimplementować tę metodę, aby tworzyć specyficzny typ biletu.
        Przyjmuje obiekt seansu i obiekt miejsca.
        """
        pass # 'pass' oznacza, że jest to metoda abstrakcyjna bez domyślnej implementacji.

class RegularTicketFactory(TicketFactory):
    """
    Konkretna fabryka biletów normalnych.
    Ta klasa jest konkretną implementacją TicketFactory i tworzy obiekty RegularTicket.
    """
    
    def create_ticket(self, screening, seat):
        """
        Tworzy bilet normalny z pełną ceną.
        Implementacja metody create_ticket() dla biletów normalnych.
        """
        price = screening.base_price  # Cena biletu normalnego to podstawowa cena seansu.
        # Tworzę i zwracam nowy obiekt RegularTicket z podanymi danymi i obliczoną ceną.
        return RegularTicket(screening, seat, price)

class DiscountedTicketFactory(TicketFactory):
    """
    Konkretna fabryka biletów ulgowych.
    Ta klasa jest konkretną implementacją TicketFactory i tworzy obiekty DiscountedTicket.
    """
    
    def create_ticket(self, screening, seat):
        """
        Tworzy bilet ulgowy ze zniżką 30%.
        Implementacja metody create_ticket() dla biletów ulgowych.
        """
        price = screening.base_price * 0.7  # Cena biletu ulgowego to 70% ceny bazowej (30% zniżki).
        # Tworzę i zwracam nowy obiekt DiscountedTicket z podanymi danymi i obliczoną ceną ulgową.
        return DiscountedTicket(screening, seat, price)

class VIPTicketFactory(TicketFactory):
    """
    Konkretna fabryka biletów VIP.
    Ta klasa jest konkretną implementacją TicketFactory i tworzy obiekty VIPTicket.
    """
    
    def create_ticket(self, screening, seat):
        """
        Tworzy bilet VIP z dopłatą 50%.
        Implementacja metody create_ticket() dla biletów VIP.
        """
        price = screening.base_price * 1.5  # Cena biletu VIP to 150% ceny bazowej (dopłata 50%).
        # Tworzę i zwracam nowy obiekt VIPTicket z podanymi danymi i obliczoną ceną VIP.
        return VIPTicket(screening, seat, price)