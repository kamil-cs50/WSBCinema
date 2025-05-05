from abc import ABC, abstractmethod  # Importuję klasy bazowe ABC i abstractmethod do tworzenia abstrakcyjnych klas i metod.

class SeatObserver(ABC):
    """
    Abstrakcyjny obserwator miejsca - wzorzec Observer.
    Ta klasa definiuje interfejs dla obiektów, które chcą być powiadamiane o zmianach stanu miejsca.
    """
    
    @abstractmethod
    def update(self, seat):
        """
        Abstrakcyjna metoda aktualizująca obserwatora o zmianie stanu miejsca.
        Jest wywoływana przez podmiot (SeatSubject) po zmianie stanu.
        Przyjmuje obiekt miejsca, którego stan się zmienił.
        """
        pass # Metoda abstrakcyjna bez implementacji.

class SeatView(SeatObserver):
    """
    Konkretny obserwator miejsca, aktualizujący widok (przykładowa implementacja).
    Ta klasa dziedziczy po SeatObserver i implementuje metodę update, symulując aktualizację interfejsu użytkownika.
    """
    
    def update(self, seat):
        """
        Aktualizuje widok po zmianie stanu miejsca.
        W rzeczywistej aplikacji zaktualizowałoby to widok GUI odzwierciedlający nowy stan miejsca.
        """
        # Na potrzeby przykładu, wyświetlam informację o zmianie stanu miejsca.
        print(f"Miejsce {seat} zmieniło stan na {seat.state}") 

class SeatSubject:
    """
    Klasa podmiotu obserwowanego - wzorzec Observer.
    Ta klasa stanowi bazę dla obiektów, które mogą być obserwowane (np. Seat).
    Umożliwia rejestrowanie, wyrejestrowywanie i powiadamianie obserwatorów.
    """
    
    def __init__(self):
        """
        Inicjalizacja obiektu podmiotu.
        Tworzy pustą listę do przechowywania zarejestrowanych obserwatorów.
        """
        self._observers = []  # Lista obiektów SeatObserver, które obserwują ten podmiot.
    
    def attach(self, observer: SeatObserver):
        """
        Dodaje obserwatora do listy.
        Obiekt obserwatora zostanie powiadomiony o przyszłych zmianach stanu.
        """
        if observer not in self._observers:  # Sprawdzam, czy obserwator nie jest już zarejestrowany.
            self._observers.append(observer)  # Dodaję obserwatora do listy.
    
    def detach(self, observer: SeatObserver):
        """
        Usuwa obserwatora z listy.
        Obiekt obserwatora przestanie być powiadamiany o zmianach stanu.
        """
        try:
            self._observers.remove(observer)  # Próbuję usunąć obserwatora z listy.
        except ValueError:
            pass  # Ignoruję błąd, jeśli obserwator nie znajduje się na liście.
    
    def notify(self):
        """
        Powiadamia wszystkich zarejestrowanych obserwatorów o zmianie stanu.
        Dla każdego obserwatora na liście wywołuje jego metodę update(), przekazując referencję do siebie (podmiotu).
        """
        for observer in self._observers:  # Iteruję przez listę obserwatorów.
            observer.update(self)  # Wywołuję metodę update() obserwatora, przekazując mu referencję do obiektu Seat (self).