class Ticket:
    """
    Klasa bazowa reprezentująca bilet na seans w WSBCinema.
    Służy jako komponent dla wzorca Dekorator.
    Klasa Ticket przechowuje podstawowe informacje o bilecie, takie jak seans, miejsce i cena.
    """
    
    def __init__(self, screening, seat, price):
        """
        Inicjalizacja obiektu biletu.
        Konstruktor przyjmuje obiekt seansu, obiekt miejsca oraz cenę biletu.
        """
        self.screening = screening  # Przypisanie obiektu seansu, na który jest bilet.
        self.seat = seat  # Przypisanie obiektu miejsca, które rezerwuje bilet.
        self.price = price  # Przypisanie ceny biletu.
    
    def __str__(self):
        """
        Metoda zwracająca tekstową reprezentację obiektu biletu.
        Ta metoda formatuje informacje o bilecie w czytelny sposób.
        """
        # Zwracanie sformatowanego stringa zawierającego tytuł filmu, czas seansu, numer miejsca i cenę.
        return f"Bilet na {self.screening.movie.title} o {self.screening.date_time.strftime('%H:%M')}, Miejsce: {self.seat}, Cena: {self.price:.2f} zł"

class RegularTicket(Ticket):
    """
    Klasa reprezentująca bilet normalny.
    RegularTicket dziedziczy po klasie bazowej Ticket i nie dodaje żadnej nowej funkcjonalności ani danych.
    """
    pass  # 'pass' oznacza, że klasa nie ma dodatkowych metod ani atrybutów poza tymi dziedziczonymi.

class DiscountedTicket(Ticket):
    """
    Klasa reprezentująca bilet ulgowy.
    DiscountedTicket również dziedziczy po klasie Ticket. Cena ulgowa jest ustalana w fabryce biletów.
    """
    pass  # Klasa pusta, funkcjonalność związana ze zniżką jest w fabryce.

class VIPTicket(Ticket):
    """
    Klasa reprezentująca bilet VIP.
    VIPTicket dziedziczy po klasie Ticket. Dodatkowa opłata za bilet VIP jest ustalana w fabryce biletów lub przez dekorator.
    """
    pass  # Klasa pusta, funkcjonalność VIP może być dodana przez dekorator.