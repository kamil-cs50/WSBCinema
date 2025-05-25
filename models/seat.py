from states.seat_state import FreeSeatState  # Importuję klasę FreeSeatState, która reprezentuje stan wolnego miejsca (część wzorca State).
from observers.seat_observer import SeatSubject  # Importuję klasę SeatSubject, która jest bazą dla obiektów obserwowanych (część wzorca Observer).

class Seat(SeatSubject):
    """
    Klasa reprezentująca pojedyncze miejsce w sali kinowej.
    Przechowywanie informacji o numerze rzędu, numerze miejsca oraz stanie miejsca.
    """
    
    def __init__(self, row: int, number: int):
        """
        Inicjalizacja obiektu miejsca.
        Przypisywanie numeru rzędu i numeru miejsca do odpowiednich atrybutów.
        Ustawianie początkowego stanu miejsca na wolne.
        """
        super().__init__()  # Wywołuję konstruktor klasy nadrzędnej (SeatSubject) do inicjalizacji mechanizmu obserwatorów.
        self.row = row  # Przypisywanie numeru rzędu do atrybutu row.
        self.number = number  # Przypisywanie numeru miejsca do atrybutu number.
        self._state = FreeSeatState()  # Ustawiam początkowy stan miejsca na FreeSeatState, czyli wolne (inicjalizacja wzorca State).
    
    @property
    def state(self):
        """
        Getter dla stanu miejsca.
        Ta właściwość pozwala na bezpieczny odczyt aktualnego stanu miejsca.
        """
        return self._state  # Zwracam aktualny obiekt stanu miejsca.
    
    @state.setter
    def state(self, state):
        """
        Setter dla stanu miejsca.
        Ta właściwość pozwala na ustawienie nowego stanu miejsca. Po zmianie stanu, powiadamiani są wszyscy obserwatorzy.
        """
        self._state = state  # Ustawiam nowy obiekt stanu miejsca.
        self.notify()  # Wywołuję metodę notify() z klasy nadrzędnej (SeatSubject), aby powiadomić wszystkich zarejestrowanych obserwatorów o tej zmianie stanu (mechanizm wzorca Observer).
    
    def reserve(self):
        """
        Metoda do próby rezerwacji miejsca.
        Ta metoda deleguje operację rezerwacji do aktualnego obiektu stanu miejsca.
        """
        return self._state.reserve(self)  # Wywołuję metodę reserve() na aktualnym obiekcie stanu, przekazując referencję do siebie (self).
    
    def cancel(self):
        """
        Metoda do próby anulowania rezerwacji miejsca.
        Ta metoda deleguje operację anulowania do aktualnego obiektu stanu miejsca.
        """
        return self._state.cancel(self)  # Wywołuję metodę cancel() na aktualnym obiekcie stanu, przekazując referencję do siebie.
    
    def sell(self):
        """
        Metoda do próby sprzedaży miejsca.
        Ta metoda deleguje operację sprzedaży do aktualnego obiektu stanu miejsca.
        """
        return self._state.sell(self)  # Wywołuję metodę sell() na aktualnym obiekcie stanu, przekazując referencję do siebie.
    
    def is_available(self):
        """
        Metoda sprawdzająca czy miejsce jest dostępne do rezerwacji/sprzedaży.
        Ta metoda deleguje sprawdzenie dostępności do aktualnego obiektu stanu miejsca.
        """
        return self._state.is_available()  # Wywołuję metodę is_available() na aktualnym obiekcie stanu.
    
    def __str__(self):
        """
        Metoda zwracająca tekstową reprezentację obiektu miejsca.
        Zwraca sformatowany string, np. "R1M5" dla miejsca w rzędzie 1, miejsce 5.
        """
        return f"Rząd {self.row} Miejsce {self.number}"  # Zwracam sformatowany tekst z numerem rzędu i miejsca.