from abc import ABC, abstractmethod  # Importuję klasy bazowe ABC i abstractmethod do tworzenia abstrakcyjnych klas i metod.

class SeatState(ABC):
    """
    Abstrakcyjny stan miejsca - wzorzec State.
    Definiuje interfejs dla wszystkich konkretnych stanów miejsca (wolne, zarezerwowane, sprzedane).
    """
    
    @abstractmethod
    def reserve(self, seat):
        """
        Abstrakcyjna metoda do próby rezerwacji miejsca w danym stanie.
        Przyjmuje obiekt miejsca (Seat), na którym ma być wykonana operacja.
        """
        pass # Metoda abstrakcyjna bez implementacji.
    
    @abstractmethod
    def cancel(self, seat):
        """
        Abstrakcyjna metoda do próby anulowania rezerwacji miejsca w danym stanie.
        Przyjmuje obiekt miejsca (Seat), na którym ma być wykonana operacja.
        """
        pass # Metoda abstrakcyjna bez implementacji.
    
    @abstractmethod
    def sell(self, seat):
        """
        Abstrakcyjna metoda do próby sprzedaży miejsca w danym stanie.
        Przyjmuje obiekt miejsca (Seat), na którym ma być wykonana operacja.
        """
        pass # Metoda abstrakcyjna bez implementacji.
    
    @abstractmethod
    def is_available(self):
        """
        Abstrakcyjna metoda sprawdzająca czy miejsce w danym stanie jest dostępne do rezerwacji/sprzedaży.
        """
        pass # Metoda abstrakcyjna bez implementacji.
    
    @abstractmethod
    def __str__(self):
        """
        Abstrakcyjna metoda zwracająca tekstową reprezentację stanu.
        """
        pass # Metoda abstrakcyjna bez implementacji.

class FreeSeatState(SeatState):
    """
    Stan wolnego miejsca.
    Implementuje zachowanie dla miejsca, które jest wolne i dostępne do rezerwacji lub sprzedaży.
    """
    
    def reserve(self, seat):
        """
        Rezerwuje wolne miejsce.
        Zmienia stan miejsca na ReservedSeatState.
        """
        seat.state = ReservedSeatState()  # Ustawiam nowy stan miejsca na ReservedSeatState.
        return True  # Operacja rezerwacji zakończyła się sukcesem.
    
    def cancel(self, seat):
        """
        Próba anulowania rezerwacji wolnego miejsca.
        Anulowanie rezerwacji nie jest możliwe dla miejsca, które już jest wolne.
        """
        return False  # Operacja anulowania zakończyła się niepowodzeniem.
    
    def sell(self, seat):
        """
        Sprzedaje wolne miejsce.
        Zmienia stan miejsca na SoldSeatState.
        """
        seat.state = SoldSeatState()  # Ustawiam nowy stan miejsca na SoldSeatState.
        return True  # Operacja sprzedaży zakończyła się sukcesem.
    
    def is_available(self):
        """
        Sprawdza czy miejsce w stanie FreeSeatState jest dostępne.
        Wolne miejsce jest dostępne.
        """
        return True  # Zwracam True, ponieważ miejsce jest wolne.
    
    def __str__(self):
        """
        Zwraca tekstową reprezentację stanu "wolne".
        """
        return "wolne"  # Zwracam tekstową nazwę stanu.

class ReservedSeatState(SeatState):
    """
    Stan zarezerwowanego miejsca.
    Implementuje zachowanie dla miejsca, które zostało zarezerwowane.
    """
    
    def reserve(self, seat):
        """
        Próba rezerwacji zarezerwowanego miejsca.
        Nie można zarezerwować miejsca, które już jest zarezerwowane.
        """
        return False  # Operacja rezerwacji zakończyła się niepowodzeniem.
    
    def cancel(self, seat):
        """
        Anuluje rezerwację zarezerwowanego miejsca.
        Zmienia stan miejsca na FreeSeatState.
        """
        seat.state = FreeSeatState()  # Ustawiam nowy stan miejsca na FreeSeatState.
        return True  # Operacja anulowania zakończyła się sukcesem.
    
    def sell(self, seat):
        """
        Sprzedaje zarezerwowane miejsce.
        Zmienia stan miejsca na SoldSeatState.
        """
        seat.state = SoldSeatState()  # Ustawiam nowy stan miejsca na SoldSeatState.
        return True  # Operacja sprzedaży zakończyła się sukcesem.
    
    def is_available(self):
        """
        Sprawdza czy miejsce w stanie ReservedSeatState jest dostępne.
        Zarezerwowane miejsce nie jest dostępne do kolejnej rezerwacji/sprzedaży.
        """
        return False  # Zwracam False, ponieważ miejsce jest zarezerwowane.
    
    def __str__(self):
        """
        Zwraca tekstową reprezentację stanu "zarezerwowane".
        """
        return "zarezerwowane"  # Zwracam tekstową nazwę stanu.

class SoldSeatState(SeatState):
    """
    Stan sprzedanego miejsca.
    Implementuje zachowanie dla miejsca, które zostało sprzedane.
    """
    
    def reserve(self, seat):
        """
        Próba rezerwacji sprzedanego miejsca.
        Nie można zarezerwować miejsca, które zostało sprzedane.
        """
        return False  # Operacja rezerwacji zakończyła się niepowodzeniem.
    
    def cancel(self, seat):
        """
        Próba anulowania rezerwacji sprzedanego miejsca.
        Nie można anulować rezerwacji miejsca, które zostało sprzedane.
        """
        return False  # Operacja anulowania zakończyła się niepowodzeniem.
    
    def sell(self, seat):
        """
        Próba sprzedaży sprzedanego miejsca.
        Nie można sprzedać miejsca, które już zostało sprzedane.
        """
        return False  # Operacja sprzedaży zakończyła się niepowodzeniem.
    
    def is_available(self):
        """
        Sprawdza czy miejsce w stanie SoldSeatState jest dostępne.
        Sprzedane miejsce nie jest dostępne.
        """
        return False  # Zwracam False, ponieważ miejsce jest sprzedane.
    
    def __str__(self):
        """
        Zwraca tekstową reprezentację stanu "sprzedane".
        """
        return "sprzedane"  # Zwracam tekstową nazwę stanu.