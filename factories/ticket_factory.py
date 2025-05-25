from abc import ABC, abstractmethod  # Import bazowych klas ABC (Abstract Base Class) i abstractmethod do tworzenia abstrakcyjnych klas i metod.
from models.ticket import RegularTicket, DiscountedTicket, VIPTicket  # Import konkretnych klas biletów: RegularTicket, DiscountedTicket, VIPTicket.

class TicketFactory(ABC):
    """
    Abstrakcyjna fabryka biletów - wzorzec Factory Method.
    Definiowanie interfejsu do tworzenia obiektów biletów, pozostawiając implementację konkretnym podklasom fabryk.
    """
    
    @abstractmethod
    def create_ticket(self, screening, seat):
        """
        Abstrakcyjna metoda do tworzenia biletów.
        Każda konkretna fabryka musi implementować tę metodę, aby tworzyć specyficzny typ biletu.
        Przyjmowanie obiektu seansu i obiektu miejsca.
        """
        pass # Metoda abstrakcyjna bez domyślnej implementacji.

class RegularTicketFactory(TicketFactory):
    """
    Konkretna fabryka biletów normalnych.
    Implementowanie TicketFactory i tworzenie obiektów RegularTicket.
    """
    
    def create_ticket(self, screening, seat):
        """
        Tworzenie biletu normalnego z pełną ceną.
        Implementacja metody create_ticket() dla biletów normalnych.
        """
        price = screening.base_price  # Ustalanie ceny biletu normalnego jako podstawowej ceny seansu.
        return RegularTicket(screening, seat, price)  # Tworzenie i zwracanie nowego obiektu RegularTicket.

class DiscountedTicketFactory(TicketFactory):
    """
    Konkretna fabryka biletów ulgowych.
    Implementowanie TicketFactory i tworzenie obiektów DiscountedTicket.
    """
    
    def create_ticket(self, screening, seat):
        """
        Tworzenie biletu ulgowego ze zniżką 30%.
        Implementacja metody create_ticket() dla biletów ulgowych.
        """
        price = screening.base_price * 0.7  # Ustalanie ceny biletu ulgowego jako 70% ceny bazowej (30% zniżki).
        return DiscountedTicket(screening, seat, price)  # Tworzenie i zwracanie nowego obiektu DiscountedTicket.

class VIPTicketFactory(TicketFactory):
    """
    Konkretna fabryka biletów VIP.
    Implementowanie TicketFactory i tworzenie obiektów VIPTicket.
    """
    
    def create_ticket(self, screening, seat):
        """
        Tworzenie biletu VIP z dopłatą 50%.
        Implementacja metody create_ticket() dla biletów VIP.
        """
        price = screening.base_price * 1.5  # Ustalanie ceny biletu VIP jako 150% ceny bazowej (dopłata 50%).
        return VIPTicket(screening, seat, price)  # Tworzenie i zwracanie nowego obiektu VIPTicket.