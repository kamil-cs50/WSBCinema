from abc import ABC, abstractmethod  # Zaimportowanie klasy bazowej ABC i abstractmethod do tworzenia abstrakcyjnych klas i metod.
from models.ticket import Ticket # Zaimportowanie klasy bazowej Ticket, która jest komponentem dla dekoratorów.

class TicketDecorator(Ticket):
    """
    Abstrakcyjny dekorator biletu - wzorzec Decorator.
    Klasa TicketDecorator dziedziczy po Ticket i stanowi bazę dla wszystkich konkretnych dekoratorów biletów.
    Przekazuje wywołania metod do opakowanego obiektu biletu.
    """
    
    def __init__(self, ticket: Ticket):
        """
        Inicjalizacja obiektu dekoratora.
        Konstruktor przyjmuje obiekt biletu (Ticket lub inny dekorator), który będzie dekorowany.
        """
        self._ticket = ticket  # Zapisuję referencję do opakowanego obiektu biletu.
    
    @property
    def price(self):
        """
        Metoda zwracająca cenę dekorowanego biletu.
        Ta metoda deleguje wywołanie do opakowanego obiektu biletu. Konkretne dekoratory mogą nadpisać tę metodę, aby zmodyfikować cenę.
        """
        return self._ticket.price  # Zwraca cenę opakowanego biletu.
    
    @property
    def screening(self):
        """
        Metoda zwracająca seans dekorowanego biletu.
        Deleguje wywołanie do opakowanego obiektu biletu.
        """
        return self._ticket.screening
    
    @property
    def seat(self):
        """
        Metoda zwracająca miejsce dekorowanego biletu.
        Deleguje wywołanie do opakowanego obiektu biletu.
        """
        return self._ticket.seat
    
    @abstractmethod
    def __str__(self):
        """
        Abstrakcyjna metoda zwracająca tekstową reprezentację dekorowanego biletu.
        Każdy konkretny dekorator musi zaimplementować tę metodę, aby dodać swój opis do reprezentacji stringowej biletu.
        """
        pass # Metoda abstrakcyjna bez implementacji.

class ThreeDTicketDecorator(TicketDecorator):
    """
    Dekorator dodający funkcjonalność i koszt biletu 3D.
    Ta klasa dziedziczy po TicketDecorator i dodaje informację o opcji 3D oraz zwiększa cenę biletu.
    """
    
    def __init__(self, ticket: Ticket):
        """
        Inicjalizacja dekoratora 3D.
        Konstruktor przyjmuje obiekt biletu do dekorowania.
        """
        super().__init__(ticket)  # Wywołanie konstruktora klasy nadrzędnej (TicketDecorator), przekazując opakowany bilet.
    
    @property
    def price(self):
        """
        Metoda zwracająca cenę biletu 3D.
        Nadpisuję metodę price(), aby dodać dodatkowy koszt za opcję 3D do ceny opakowanego biletu.
        """
        return self._ticket.price + 5  # Zwraca cenę opakowanego biletu powiększoną o 5 zł (koszt 3D).
    
    def __str__(self):
        """
        Metoda zwracająca tekstową reprezentację biletu 3D.
        Nadpisuję metodę __str__(), aby dodać informację "[3D]" do opisu opakowanego biletu.
        """
        # Zwraca tekstową reprezentację opakowanego biletu i dodaję na końcu "[3D]".
        return f"{self._ticket.__str__()} [3D]"

class SnackComboTicketDecorator(TicketDecorator):
    """
    Dekorator dodający funkcjonalność i koszt zestawu przekąsek do biletu.
    Ta klasa dziedziczy po TicketDecorator i dodaje informację o zestawie przekąsek oraz zwiększa cenę biletu.
    """
    
    def __init__(self, ticket: Ticket):
        """
        Inicjalizacja dekoratora zestawu przekąsek.
        Konstruktor przyjmuje obiekt biletu do dekorowania.
        """
        super().__init__(ticket)  # Wywołanie konstruktora klasy nadrzędnej (TicketDecorator), przekazując opakowany bilet.
    
    @property
    def price(self):
        """
        Metoda zwracająca cenę biletu z zestawem przekąsek.
        Nadpisuję metodę price(), aby dodać dodatkowy koszt za zestaw przekąsek do ceny opakowanego biletu.
        """
        return self._ticket.price + 15  # Zwraca cenę opakowanego biletu powiększoną o 15 zł (koszt zestawu przekąsek).
    
    def __str__(self):
        """
        Metoda zwracająca tekstową reprezentację biletu z zestawem przekąsek.
        Nadpisuję metodę __str__(), aby dodać informację "[+ Zestaw Przekąsek]" do opisu opakowanego biletu.
        """
        # Zwraca tekstową reprezentację opakowanego biletu i dodaję na końcu "[+ Zestaw Przekąsek]".
        return f"{self._ticket.__str__()} [+ Zestaw Przekąsek]"