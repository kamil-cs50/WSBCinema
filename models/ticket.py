class Ticket:
    """
    Klasa reprezentująca bilet na seans filmowy.
    Przechowywanie informacji o typie biletu, cenie oraz przypisanym miejscu.
    """

    def __init__(self, ticket_type: str, price: float, seat):
        """
        Inicjalizacja obiektu biletu.
        Przypisywanie typu biletu, ceny oraz obiektu miejsca do odpowiednich atrybutów.
        """
        self.ticket_type = ticket_type  # Przypisywanie typu biletu do atrybutu ticket_type.
        self.price = price  # Przypisywanie ceny biletu do atrybutu price.
        self.seat = seat  # Przypisywanie obiektu miejsca do atrybutu seat.

    def __str__(self):
        """
        Zwracanie tekstowej reprezentacji biletu w formacie "Typ: X, Miejsce: Y, Cena: Z zł".
        """
        return f"{self.ticket_type}, {self.seat}, {self.price:.2f} zł"
class RegularTicket(Ticket):
    def __init__(self, screening, seat, price):
        super().__init__("Normalny", price, seat)

class DiscountedTicket(Ticket):
    def __init__(self, screening, seat, price):
        super().__init__("Ulgowy", price, seat)

class VIPTicket(Ticket):
    def __init__(self, screening, seat, price):
        super().__init__("VIP", price, seat)