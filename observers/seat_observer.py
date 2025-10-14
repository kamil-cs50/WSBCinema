from abc import ABC, abstractmethod  # Import bazowych klas ABC i abstractmethod do tworzenia abstrakcyjnych klas i metod.

class SeatObserver(ABC):
    """
    Abstrakcyjny obserwator miejsca - wzorzec Observer.
    Definiowanie interfejsu dla obiektów, które chcą być powiadamiane o zmianach stanu miejsca.
    """
    
    @abstractmethod
    def update(self, seat):
        """
        Abstrakcyjna metoda aktualizująca obserwatora o zmianie stanu miejsca.
        Wywoływanie przez podmiot (SeatSubject) po zmianie stanu.
        Przyjmowanie obiektu miejsca, którego stan się zmienił.
        """
        pass # Metoda abstrakcyjna bez implementacji.

class SeatView(SeatObserver):
    """
    Konkretny obserwator miejsca, aktualizujący widok (przykładowa implementacja).
    Dziedziczenie po SeatObserver i implementowanie metody update, symulując aktualizację interfejsu użytkownika.
    """
    
    def update(self, seat):
        """
        Aktualizowanie widoku po zmianie stanu miejsca.
        W rzeczywistej aplikacji zaktualizowałoby to widok GUI odzwierciedlający nowy stan miejsca.
        """
        # Przykładowe wyświetlanie informacji o zmianie stanu miejsca.
        print(f"Miejsce {seat} zmieniło stan na {seat.state}") 

class SeatSubject:
    """
    Klasa podmiotu obserwowanego - wzorzec Observer.
    Stanowienie bazy dla obiektów, które mogą być obserwowane (np. Seat).
    Umożliwianie rejestrowania, wyrejestrowywania i powiadamiania obserwatorów.
    """
    
    def __init__(self):
        """
        Inicjalizacja obiektu podmiotu.
        Tworzenie pustej listy do przechowywania zarejestrowanych obserwatorów.
        """
        self._observers = []  # Lista obiektów SeatObserver, które obserwują ten podmiot.
    
    def attach(self, observer: SeatObserver):
        """
        Dodawanie obserwatora do listy.
        Obiekt obserwatora będzie powiadamiany o przyszłych zmianach stanu.
        """
        if observer not in self._observers:  # Sprawdzanie, czy obserwator nie jest już zarejestrowany.
            self._observers.append(observer)  # Dodawanie obserwatora do listy.
    
    def detach(self, observer: SeatObserver):
        """
        Usuwanie obserwatora z listy.
        Obiekt obserwatora przestaje być powiadamiany o zmianach stanu.
        """
        try:
            self._observers.remove(observer)  # Usuwanie obserwatora z listy.
        except ValueError:
            pass  # Ignorowanie błędu, jeśli obserwator nie znajduje się na liście.
    
    def notify(self):
        """
        Powiadamianie wszystkich zarejestrowanych obserwatorów o zmianie stanu.
        Dla każdego obserwatora na liście wywoływanie jego metody update(), przekazując referencję do siebie (podmiotu).
        """
        for observer in self._observers:  # Iterowanie przez listę obserwatorów.
            observer.update(self)  # Wywoływanie metody update() obserwatora, przekazując mu referencję do obiektu Seat (self).