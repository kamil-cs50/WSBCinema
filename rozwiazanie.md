# System Rezerwacji Biletów Kinowych - WSBCinema

System rezerwacji biletów kinowych WSBCinema to aplikacja umożliwiająca zarządzanie repertuarem kinowym oraz dokonywanie rezerwacji miejsc na seanse. Aplikacja posiada nowoczesny interfejs graficzny z efektem glassmorphism, zapewniający estetyczne i funkcjonalne doświadczenie użytkownika.

## Struktura projektu i użyte wzorce projektowe

System został zaprojektowany z wykorzystaniem wielu wzorców projektowych, które zapewniają elastyczność, rozszerzalność i łatwość utrzymania kodu. Poniżej przedstawiam implementację tych wzorców wraz z opisem ich zastosowania.

### Metoda Wytwórcza (Factory Method)

Wzorzec Factory Method zastosowano do tworzenia różnych typów biletów (normalny, ulgowy), co pozwala na łatwe rozszerzanie systemu o nowe rodzaje biletów w przyszłości[^1_10][^1_12].

### Budowniczy (Builder)

Wzorzec Builder wykorzystano do konstrukcji złożonych obiektów seansu (film, sala, czas, cennik), co upraszcza proces tworzenia seansów i zapewnia spójność danych[^1_14].

### Singleton

Wzorzec Singleton zaimplementowano w module bazy danych, aby zapewnić tylko jedną instancję repozytorium danych w całej aplikacji[^1_10].

### Fasada (Facade)

Wzorzec Facade zastosowano do uproszczenia interfejsu podsystemu rezerwacji, ukrywając złożoność operacji takich jak sprawdzanie dostępności miejsc czy obliczanie cen[^1_10].

### Dekorator (Decorator)

Wzorzec Decorator umożliwia dynamiczne dodawanie funkcjonalności do biletów, np. dodatkowe opłaty za miejsca VIP czy okulary 3D[^1_10].

### Obserwator (Observer)

Wzorzec Observer zastosowano do powiadamiania o zmianach stanu miejsc na sali, co pozwala na automatyczną aktualizację interfejsu użytkownika[^1_10].

### Stan (State)

Wzorzec State wykorzystano do zarządzania stanem miejsc (wolne, zarezerwowane, sprzedane), co upraszcza logikę związaną ze zmianami stanów[^1_10].

### Strategia (Strategy)

Wzorzec Strategy zaimplementowano dla różnych strategii cenowych, umożliwiając elastyczne obliczanie cen biletów w zależności od różnych czynników (np. dzień tygodnia, pora dnia)[^1_10].

## Implementacja kodu

Poniżej przedstawiam kod źródłowy projektu wraz z dokładnymi komentarzami wyjaśniającymi działanie poszczególnych elementów.

### main.py

```python
import sys  # Importuję moduł sys do obsługi argumentów wiersza poleceń i zakończenia aplikacji
from PyQt5.QtWidgets import QApplication  # Importuję klasę QApplication do utworzenia głównej aplikacji
from views.main_window import MainWindow  # Importuję klasę MainWindow z modułu views
from utils.database import Database  # Importuję klasę Database do zarządzania danymi
from models.movie import Movie  # Importuję klasę Movie do reprezentacji filmów
from models.cinema_hall import CinemaHall  # Importuję klasę CinemaHall do reprezentacji sal kinowych
from builders.screening_builder import ScreeningBuilder  # Importuję klasę ScreeningBuilder do tworzenia seansów
from datetime import datetime, timedelta  # Importuję klasy datetime i timedelta do obsługi dat i czasu

def load_sample_data():
    """Funkcja ładująca przykładowe dane do systemu"""
    db = Database()  # Tworzę instancję bazy danych (singleton)
    
    # Przykładowe filmy, które otrzymały Oscara
    movies = [
        Movie("Oppenheimer", 180, 16),  # Tworzę film Oppenheimer (czas trwania 180 min, kategoria wiekowa 16+)
        Movie("Everything Everywhere All at Once", 139, 16),  # Tworzę film EEAAO (czas trwania 139 min, kategoria wiekowa 16+)
        Movie("CODA", 111, 12),  # Tworzę film CODA (czas trwania 111 min, kategoria wiekowa 12+)
        Movie("Nomadland", 107, 15),  # Tworzę film Nomadland (czas trwania 107 min, kategoria wiekowa 15+)
        Movie("Parasite", 132, 16),  # Tworzę film Parasite (czas trwania 132 min, kategoria wiekowa 16+)
        Movie("Anora", 115, 16),  # Tworzę film Anora (czas trwania 115 min, kategoria wiekowa 16+)
    ]
    
    for movie in movies:
        db.add_movie(movie)  # Dodaję każdy film do bazy danych
    
    # Przykładowe sale kinowe
    halls = [
        CinemaHall("Sala 1", 8, 10),  # Tworzę salę 1 (8 rzędów, 10 miejsc w rzędzie)
        CinemaHall("Sala 2", 10, 12),  # Tworzę salę 2 (10 rzędów, 12 miejsc w rzędzie)
        CinemaHall("Sala VIP", 5, 8),  # Tworzę salę VIP (5 rzędów, 8 miejsc w rzędzie)
    ]
    
    for hall in halls:
        db.add_cinema_hall(hall)  # Dodaję każdą salę do bazy danych
    
    # Tworzę budowniczego seansów (wzorzec Builder)
    builder = ScreeningBuilder()
    
    # Bieżąca data
    today = datetime.now().date()
    
    # Generuję seanse na najbliższe 7 dni
    for day_offset in range(7):
        current_date = today + timedelta(days=day_offset)  # Obliczam datę dla każdego dnia
        
        # Seans poranny
        morning_time = datetime.combine(current_date, datetime.min.time().replace(hour=10, minute=0))
        db.add_screening(
            builder.set_movie(movies[^1_0])  # Ustawiam film dla seansu
                  .set_cinema_hall(halls[^1_0])  # Ustawiam salę dla seansu
                  .set_date_time(morning_time)  # Ustawiam datę i czas seansu
                  .set_base_price(20)  # Ustawiam cenę bazową biletu
                  .build()  # Buduję obiekt seansu
        )
        
        # Seans popołudniowy
        afternoon_time = datetime.combine(current_date, datetime.min.time().replace(hour=15, minute=30))
        db.add_screening(
            builder.set_movie(movies[^1_1])
                  .set_cinema_hall(halls[^1_1])
                  .set_date_time(afternoon_time)
                  .set_base_price(25)
                  .build()
        )
        
        # Seans wieczorny
        evening_time = datetime.combine(current_date, datetime.min.time().replace(hour=20, minute=0))
        db.add_screening(
            builder.set_movie(movies[^1_2])
                  .set_cinema_hall(halls[^1_2])
                  .set_date_time(evening_time)
                  .set_base_price(30)
                  .build()
        )

def main():
    """Główna funkcja aplikacji"""
    load_sample_data()  # Ładuję przykładowe dane
    
    app = QApplication(sys.argv)  # Tworzę instancję aplikacji Qt
    window = MainWindow()  # Tworzę główne okno aplikacji
    window.show()  # Wyświetlam główne okno
    sys.exit(app.exec_())  # Uruchamiam pętlę zdarzeń aplikacji

if __name__ == "__main__":
    main()  # Uruchamiam funkcję main gdy skrypt jest wykonywany bezpośrednio
```


### models/movie.py

```python
class Movie:
    """Klasa reprezentująca film w kinie"""
    
    def __init__(self, title, duration_minutes, age_category):
        """Inicjalizacja filmu z tytułem, czasem trwania i kategorią wiekową"""
        self.title = title  # Zapisuję tytuł filmu
        self.duration_minutes = duration_minutes  # Zapisuję czas trwania filmu w minutach
        self.age_category = age_category  # Zapisuję kategorię wiekową filmu
    
    def __str__(self):
        """Metoda zwracająca tekstową reprezentację filmu"""
        return f"{self.title} ({self.duration_minutes} min, {self.age_category}+)"  # Zwracam sformatowany tekst z informacjami o filmie
```


### models/cinema_hall.py

```python
class CinemaHall:
    """Klasa reprezentująca salę kinową"""
    
    def __init__(self, name, rows, seats_per_row):
        """Inicjalizacja sali kinowej z nazwą, liczbą rzędów i liczbą miejsc w rzędzie"""
        self.name = name  # Zapisuję nazwę sali
        self.rows = rows  # Zapisuję liczbę rzędów
        self.seats_per_row = seats_per_row  # Zapisuję liczbę miejsc w każdym rzędzie
    
    def get_total_seats(self):
        """Metoda zwracająca całkowitą liczbę miejsc w sali"""
        return self.rows * self.seats_per_row  # Obliczam i zwracam liczbę miejsc jako iloczyn rzędów i miejsc w rzędzie
```


### models/seat.py

```python
from states.seat_state import FreeSeatState  # Importuję stan wolnego miejsca
from observers.seat_observer import SeatSubject  # Importuję klasę bazową dla wzorca Observer

class Seat(SeatSubject):
    """Klasa reprezentująca miejsce w sali kinowej, implementująca wzorzec Observer i State"""
    
    def __init__(self, row, number):
        """Inicjalizacja miejsca z numerem rzędu i numerem miejsca"""
        super().__init__()  # Wywołuję konstruktor klasy nadrzędnej
        self.row = row  # Zapisuję numer rzędu
        self.number = number  # Zapisuję numer miejsca
        self._state = FreeSeatState()  # Ustawiam początkowy stan miejsca jako wolne
    
    @property
    def state(self):
        """Getter dla stanu miejsca"""
        return self._state  # Zwracam aktualny stan miejsca
    
    @state.setter
    def state(self, state):
        """Setter dla stanu miejsca, powiadamiający obserwatorów o zmianie"""
        self._state = state  # Ustawiam nowy stan miejsca
        self.notify()  # Powiadamiam wszystkich obserwatorów o zmianie stanu
    
    def reserve(self):
        """Metoda do rezerwacji miejsca"""
        return self._state.reserve(self)  # Delegowanie operacji do aktualnego stanu
    
    def cancel(self):
        """Metoda do anulowania rezerwacji miejsca"""
        return self._state.cancel(self)  # Delegowanie operacji do aktualnego stanu
    
    def sell(self):
        """Metoda do sprzedaży miejsca"""
        return self._state.sell(self)  # Delegowanie operacji do aktualnego stanu
    
    def is_available(self):
        """Metoda sprawdzająca czy miejsce jest dostępne"""
        return self._state.is_available()  # Delegowanie operacji do aktualnego stanu
    
    def __str__(self):
        """Metoda zwracająca tekstową reprezentację miejsca"""
        return f"{self.row}{self.number}"  # Zwracam sformatowany tekst z informacjami o miejscu
```


### models/screening.py

```python
from datetime import datetime  # Importuję klasę datetime do obsługi dat
from models.seat import Seat  # Importuję klasę Seat do reprezentacji miejsc

class Screening:
    """Klasa reprezentująca seans filmowy"""
    
    def __init__(self, movie, cinema_hall, date_time, base_price):
        """Inicjalizacja seansu z filmem, salą, datą/czasem i podstawową ceną"""
        self.movie = movie  # Zapisuję odniesienie do filmu
        self.cinema_hall = cinema_hall  # Zapisuję odniesienie do sali kinowej
        self.date_time = date_time  # Zapisuję datę i czas seansu
        self.base_price = base_price  # Zapisuję podstawową cenę biletu
        self.seats = self._initialize_seats()  # Inicjalizuję miejsca w sali dla tego seansu
    
    def _initialize_seats(self):
        """Prywatna metoda inicjalizująca wszystkie miejsca w sali"""
        seats = []  # Tworzę pustą listę na miejsca
        for row in range(1, self.cinema_hall.rows + 1):  # Dla każdego rzędu w sali
            for seat_num in range(1, self.cinema_hall.seats_per_row + 1):  # Dla każdego miejsca w rzędzie
                seats.append(Seat(row, seat_num))  # Dodaję nowe miejsce do listy
        return seats  # Zwracam listę wszystkich miejsc
    
    def get_available_seats(self):
        """Metoda zwracająca listę dostępnych miejsc"""
        return [seat for seat in self.seats if seat.is_available()]  # Zwracam listę miejsc, które są dostępne
```


### models/ticket.py

```python
class Ticket:
    """Klasa bazowa reprezentująca bilet na seans"""
    
    def __init__(self, screening, seat, price):
        """Inicjalizacja biletu z seansem, miejscem i ceną"""
        self.screening = screening  # Zapisuję odniesienie do seansu
        self.seat = seat  # Zapisuję odniesienie do miejsca
        self.price = price  # Zapisuję cenę biletu
    
    def __str__(self):
        """Metoda zwracająca tekstową reprezentację biletu"""
        return f"Bilet na {self.screening.movie.title} o {self.screening.date_time.strftime('%H:%M')}, Miejsce: {self.seat}, Cena: {self.price} zł"

class RegularTicket(Ticket):
    """Klasa reprezentująca bilet normalny"""
    pass  # Nie dodaję dodatkowej funkcjonalności, dziedziczę wszystko z klasy Ticket

class DiscountedTicket(Ticket):
    """Klasa reprezentująca bilet ulgowy"""
    pass  # Nie dodaję dodatkowej funkcjonalności, dziedziczę wszystko z klasy Ticket

class VIPTicket(Ticket):
    """Klasa reprezentująca bilet VIP"""
    pass  # Nie dodaję dodatkowej funkcjonalności, dziedziczę wszystko z klasy Ticket
```


### models/reservation.py

```python
import uuid  # Importuję moduł uuid do generowania unikalnych identyfikatorów
from datetime import datetime  # Importuję klasę datetime do obsługi czasu

class Reservation:
    """Klasa reprezentująca rezerwację biletów"""
    
    def __init__(self, customer_name, screening, seats, tickets):
        """Inicjalizacja rezerwacji z danymi klienta, seansem, miejscami i biletami"""
        self.id = str(uuid.uuid4())  # Generuję unikalny identyfikator rezerwacji
        self.customer_name = customer_name  # Zapisuję imię i nazwisko klienta
        self.screening = screening  # Zapisuję odniesienie do seansu
        self.seats = seats  # Zapisuję listę zarezerwowanych miejsc
        self.tickets = tickets  # Zapisuję listę biletów
        self.timestamp = datetime.now()  # Zapisuję czas utworzenia rezerwacji
        self.total_price = sum(ticket.price for ticket in tickets)  # Obliczam łączną cenę wszystkich biletów
    
    def __str__(self):
        """Metoda zwracająca tekstową reprezentację rezerwacji"""
        seats_str = ", ".join([f"{seat.row}{seat.number}" for seat in self.seats])  # Tworzę string z listą miejsc
        return f"{self.customer_name}: {self.screening.movie.title} ({self.screening.date_time.strftime('%d.%m.%Y %H:%M')}), Miejsca: {seats_str}, Cena: {self.total_price} zł"
```


### factories/ticket_factory.py

```python
from abc import ABC, abstractmethod  # Importuję klasy do tworzenia abstrakcyjnych klas i metod
from models.ticket import RegularTicket, DiscountedTicket, VIPTicket  # Importuję klasy biletów

class TicketFactory(ABC):
    """Abstrakcyjna fabryka biletów - wzorzec Factory Method"""
    
    @abstractmethod
    def create_ticket(self, screening, seat):
        """Abstrakcyjna metoda do tworzenia biletów"""
        pass

class RegularTicketFactory(TicketFactory):
    """Konkretna fabryka biletów normalnych"""
    
    def create_ticket(self, screening, seat):
        """Tworzy bilet normalny z pełną ceną"""
        price = screening.base_price  # Ustawiam cenę biletu jako cenę bazową seansu
        return RegularTicket(screening, seat, price)  # Tworzę i zwracam bilet normalny

class DiscountedTicketFactory(TicketFactory):
    """Konkretna fabryka biletów ulgowych"""
    
    def create_ticket(self, screening, seat):
        """Tworzy bilet ulgowy ze zniżką 30%"""
        price = screening.base_price * 0.7  # Ustawiam cenę biletu jako 70% ceny bazowej
        return DiscountedTicket(screening, seat, price)  # Tworzę i zwracam bilet ulgowy

class VIPTicketFactory(TicketFactory):
    """Konkretna fabryka biletów VIP"""
    
    def create_ticket(self, screening, seat):
        """Tworzy bilet VIP z dopłatą 50%"""
        price = screening.base_price * 1.5  # Ustawiam cenę biletu jako 150% ceny bazowej
        return VIPTicket(screening, seat, price)  # Tworzę i zwracam bilet VIP
```


### builders/screening_builder.py

```python
from datetime import datetime  # Importuję klasę datetime do obsługi dat
from models.screening import Screening  # Importuję klasę Screening

class ScreeningBuilder:
    """Budowniczy seansów - wzorzec Builder"""
    
    def __init__(self):
        """Inicjalizacja budowniczego"""
        self.reset()  # Resetuję budowniczego do stanu początkowego
    
    def reset(self):
        """Resetuje wszystkie atrybuty budowniczego"""
        self.movie = None  # Resetuję film
        self.cinema_hall = None  # Resetuję salę
        self.date_time = None  # Resetuję datę i czas
        self.base_price = None  # Resetuję cenę bazową
    
    def set_movie(self, movie):
        """Ustawia film dla seansu"""
        self.movie = movie  # Zapisuję film
        return self  # Zwracam self aby umożliwić łańcuchowanie metod
    
    def set_cinema_hall(self, cinema_hall):
        """Ustawia salę dla seansu"""
        self.cinema_hall = cinema_hall  # Zapisuję salę
        return self  # Zwracam self aby umożliwić łańcuchowanie metod
    
    def set_date_time(self, date_time):
        """Ustawia datę i czas seansu"""
        self.date_time = date_time  # Zapisuję datę i czas
        return self  # Zwracam self aby umożliwić łańcuchowanie metod
    
    def set_base_price(self, base_price):
        """Ustawia podstawową cenę biletu"""
        self.base_price = base_price  # Zapisuję cenę
        return self  # Zwracam self aby umożliwić łańcuchowanie metod
    
    def build(self):
        """Tworzy i zwraca obiekt seansu na podstawie zebranych danych"""
        if not all([self.movie, self.cinema_hall, self.date_time, self.base_price]):
            # Sprawdzam czy wszystkie wymagane atrybuty zostały ustawione
            raise ValueError("Nie można utworzyć seansu: brakuje wymaganych atrybutów")
        
        screening = Screening(self.movie, self.cinema_hall, self.date_time, self.base_price)  # Tworzę seans
        self.reset()  # Resetuję budowniczego do stanu początkowego
        return screening  # Zwracam utworzony seans
```


### utils/database.py

```python
class Database:
    """Singleton przechowujący dane aplikacji"""
    
    _instance = None  # Prywatne pole statyczne przechowujące jedyną instancję
    
    def __new__(cls):
        """Metoda tworząca nową instancję lub zwracająca istniejącą (wzorzec Singleton)"""
        if cls._instance is None:  # Jeśli instancja jeszcze nie istnieje
            cls._instance = super(Database, cls).__new__(cls)  # Tworzę nową instancję
            cls._instance._initialize()  # Inicjalizuję instancję
        return cls._instance  # Zwracam jedyną instancję
    
    def _initialize(self):
        """Inicjalizuje struktury danych dla bazy danych"""
        self.movies = []  # Inicjalizuję pustą listę filmów
        self.cinema_halls = []  # Inicjalizuję pustą listę sal
        self.screenings = []  # Inicjalizuję pustą listę seansów
        self.reservations = []  # Inicjalizuję pustą listę rezerwacji
    
    def add_movie(self, movie):
        """Dodaje film do bazy danych"""
        self.movies.append(movie)  # Dodaję film do listy filmów
    
    def add_cinema_hall(self, cinema_hall):
        """Dodaje salę do bazy danych"""
        self.cinema_halls.append(cinema_hall)  # Dodaję salę do listy sal
    
    def add_screening(self, screening):
        """Dodaje seans do bazy danych"""
        self.screenings.append(screening)  # Dodaję seans do listy seansów
    
    def add_reservation(self, reservation):
        """Dodaje rezerwację do bazy danych"""
        self.reservations.append(reservation)  # Dodaję rezerwację do listy rezerwacji
    
    def get_movies(self):
        """Zwraca wszystkie filmy"""
        return self.movies  # Zwracam listę filmów
    
    def get_cinema_halls(self):
        """Zwraca wszystkie sale"""
        return self.cinema_halls  # Zwracam listę sal
    
    def get_screenings(self):
        """Zwraca wszystkie seanse"""
        return self.screenings  # Zwracam listę seansów
    
    def get_reservations(self):
        """Zwraca wszystkie rezerwacje"""
        return self.reservations  # Zwracam listę rezerwacji
    
    def get_screenings_for_date(self, date):
        """Zwraca seanse dla podanej daty"""
        return [s for s in self.screenings if s.date_time.date() == date]  # Zwracam przefiltrowaną listę seansów
```


### utils/glass_morphism.py

```python
from PyQt5 import QtWidgets, QtGui, QtCore  # Importuję moduły Qt do tworzenia GUI

class BackDrop(QtWidgets.QGraphicsEffect):
    """Efekt graficzny glassmorphism - implementacja efektu szkła"""
    
    def __init__(self, blur=0, radius=0, backgrounds=None):
        """Inicjalizacja efektu z rozmyciem, zaokrągleniem rogów i tłem"""
        super().__init__()  # Wywołuję konstruktor klasy nadrzędnej
        self.blur = blur  # Zapisuję wartość rozmycia
        self.radius = radius  # Zapisuję promień zaokrąglenia rogów
        self.backgrounds = backgrounds or []  # Zapisuję tła lub pustą listę jeśli brak
    
    def draw(self, painter):
        """Metoda rysująca efekt szkła"""
        # Pobieram źródłową mapę pikseli (oryginalną zawartość widgetu)
        source_pixmap = self.sourcePixmap()
        painter.save()  # Zapisuję stan malarza
        # Ustawiam renderowanie z antyaliasingiem dla lepszej jakości
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        
        # Rysuję tła
        for bg in self.backgrounds:
            # Ustawiam przezroczystość jeśli została określona
            if "opacity" in bg:
                painter.setOpacity(bg["opacity"])
            
            # Tworzę ścieżkę z zaokrąglonymi rogami
            path = QtGui.QPainterPath()
            path.addRoundedRect(
                QtCore.QRectF(0, 0, source_pixmap.width(), source_pixmap.height()),
                self.radius, self.radius
            )
            
            # Ustawiam kolor tła jeśli został określony
            if "background-color" in bg:
                painter.fillPath(path, bg["background-color"])
            
            # Rysuję obramowanie jeśli zostało określone
            if "border" in bg and "border-width" in bg:
                pen = QtGui.QPen(bg["border"])
                pen.setWidth(bg["border-width"])
                painter.setPen(pen)
                painter.drawPath(path)
        
        # Aplikuję efekt rozmycia jeśli został określony
        if self.blur &gt; 0:
            blur_effect = QtWidgets.QGraphicsBlurEffect()
            blur_effect.setBlurRadius(self.blur)
            blur_pixmap = QtGui.QPixmap(source_pixmap)
            blur_painter = QtGui.QPainter(blur_pixmap)
            blur_effect.draw(blur_painter)
            blur_painter.end()
            painter.drawPixmap(0, 0, blur_pixmap)
        else:
            painter.drawPixmap(0, 0, source_pixmap)
        
        painter.restore()  # Przywracam zapisany stan malarza

class BackDropWrapper(QtWidgets.QWidget):
    """Wrapper dla widgetów do łatwego stosowania efektu glassmorphism"""
    
    def __init__(self, widget, blur=0, radius=0, backgrounds=None, shine_animation=None, move_animation=None):
        """Inicjalizacja wrappera z widgetem, efektem i animacjami"""
        super().__init__()  # Wywołuję konstruktor klasy nadrzędnej
        self.widget = widget  # Zapisuję widget do opakowania
        
        # Ustawiam układ
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        
        # Ustawiam efekt tła
        self.backdrop = BackDrop(blur, radius, backgrounds)
        self.widget.setGraphicsEffect(self.backdrop)
        
        # Ustawiam animacje
        self.shine_animation = None
        self.move_animation = None
        
        # Dodaję animację błysku jeśli została podana
        if shine_animation:
            self.enable_shine_animation(*shine_animation)
        
        # Dodaję animację ruchu jeśli została podana
        if move_animation:
            self.enable_move_animation(*move_animation)
    
    def enable_shine_animation(self, duration=500, forward=True, angle=45, width=150, color=None):
        """Włącza animację błysku przy najechaniu myszą"""
        if color is None:
            color = QtGui.QColor(255, 255, 255, 90)  # Domyślny kolor to półprzezroczysty biały
        
        # Zapisuję parametry animacji
        self.shine_animation = {
            'duration': duration,
            'forward': forward,
            'angle': angle,
            'width': width,
            'color': color
        }
        
        # Podpinam zdarzenia myszy do animacji
        self.widget.enterEvent = lambda event: self._start_shine_animation()
        self.widget.leaveEvent = lambda event: self._stop_shine_animation()
    
    def enable_move_animation(self, duration=300, offset=(0, -10), forward=True):
        """Włącza animację ruchu przy najechaniu myszą"""
        # Zapisuję parametry animacji
        self.move_animation = {
            'duration': duration,
            'offset': offset,
            'forward': forward
        }
        
        # Podpinam zdarzenia myszy do animacji
        self.widget.enterEvent = lambda event: self._start_move_animation()
        self.widget.leaveEvent = lambda event: self._stop_move_animation()
    
    def _start_shine_animation(self):
        """Rozpoczyna animację błysku"""
        # Pełną implementację animacji błysku należy dodać tutaj
        pass
    
    def _stop_shine_animation(self):
        """Zatrzymuje animację błysku"""
        # Pełną implementację zatrzymania animacji błysku należy dodać tutaj
        pass
    
    def _start_move_animation(self):
        """Rozpoczyna animację ruchu"""
        # Pełną implementację animacji ruchu należy dodać tutaj
        pass
    
    def _stop_move_animation(self):
        """Zatrzymuje animację ruchu"""
        # Pełną implementację zatrzymania animacji ruchu należy dodać tutaj
        pass
```


### facades/reservation_facade.py

```python
from utils.database import Database  # Importuję klasę Database do zarządzania danymi
from models.reservation import Reservation  # Importuję klasę Reservation

class ReservationFacade:
    """Fasada dla systemu rezerwacji - wzorzec Facade"""
    
    def __init__(self):
        """Inicjalizacja fasady z instancją bazy danych"""
        self.database = Database()  # Pobieram instancję bazy danych (singleton)
    
    def get_available_screenings(self, date):
        """Zwraca dostępne seanse na podaną datę"""
        return self.database.get_screenings_for_date(date)  # Deleguje żądanie do bazy danych
    
    def get_available_seats(self, screening):
        """Zwraca dostępne miejsca dla podanego seansu"""
        return screening.get_available_seats()  # Deleguje żądanie do seansu
    
    def calculate_price(self, screening, seats, ticket_factory):
        """Oblicza cenę rezerwacji na podstawie miejsc i fabryki biletów"""
        total_price = 0  # Inicjalizuję cenę całkowitą
        tickets = []  # Inicjalizuję listę biletów
        
        for seat in seats:  # Dla każdego wybranego miejsca
            ticket = ticket_factory.create_ticket(screening, seat)  # Tworzę bilet używając fabryki
            tickets.append(ticket)  # Dodaję bilet do listy
            total_price += ticket.price  # Dodaję cenę biletu do ceny całkowitej
        
        return total_price, tickets  # Zwracam cenę całkowitą i listę biletów
    
    def make_reservation(self, customer_name, screening, seats, tickets):
        """Tworzy rezerwację dla klienta"""
        reservation = Reservation(customer_name, screening, seats, tickets)  # Tworzę obiekt rezerwacji
        
        # Aktualizuję stan miejsc na zarezerwowane
        for seat in seats:
            seat.state = seat.state.__class__.__name__ == "FreeSeatState" and "reserved" or seat.state
        
        self.database.add_reservation(reservation)  # Dodaję rezerwację do bazy danych
        return reservation  # Zwracam utworzoną rezerwację
```


### decorators/ticket_decorator.py

```python
from abc import ABC, abstractmethod  # Importuję klasy do tworzenia abstrakcyjnych klas i metod

class TicketDecorator(ABC):
    """Abstrakcyjny dekorator biletu - wzorzec Decorator"""
    
    def __init__(self, ticket):
        """Inicjalizacja dekoratora z bilet do dekorowania"""
        self.ticket = ticket  # Zapisuję bilet do dekorowania
    
    @property
    def price(self):
        """Metoda zwracająca cenę dekorowanego biletu"""
        return self.ticket.price  # Domyślnie zwracam cenę oryginalnego biletu
    
    @property
    def screening(self):
        """Metoda zwracająca seans dekorowanego biletu"""
        return self.ticket.screening  # Zwracam seans oryginalnego biletu
    
    @property
    def seat(self):
        """Metoda zwracająca miejsce dekorowanego biletu"""
        return self.ticket.seat  # Zwracam miejsce oryginalnego biletu
    
    @abstractmethod
    def __str__(self):
        """Abstrakcyjna metoda zwracająca tekstową reprezentację biletu"""
        pass

class ThreeDTicketDecorator(TicketDecorator):
    """Dekorator dodający funkcjonalność biletu 3D"""
    
    def __init__(self, ticket):
        """Inicjalizacja dekoratora 3D"""
        super().__init__(ticket)  # Wywołuję konstruktor klasy nadrzędnej
    
    @property
    def price(self):
        """Metoda zwracająca cenę biletu 3D"""
        return self.ticket.price + 5  # Dodaję 5 zł do ceny biletu za 3D
    
    def __str__(self):
        """Metoda zwracająca tekstową reprezentację biletu 3D"""
        return f"{self.ticket} [3D]"  # Dodaję oznaczenie 3D do opisu biletu

class SnackComboTicketDecorator(TicketDecorator):
    """Dekorator dodający funkcjonalność biletu z zestawem przekąsek"""
    
    def __init__(self, ticket):
        """Inicjalizacja dekoratora zestawu przekąsek"""
        super().__init__(ticket)  # Wywołuję konstruktor klasy nadrzędnej
    
    @property
    def price(self):
        """Metoda zwracająca cenę biletu z zestawem przekąsek"""
        return self.ticket.price + 15  # Dodaję 15 zł do ceny biletu za zestaw przekąsek
    
    def __str__(self):
        """Metoda zwracająca tekstową reprezentację biletu z zestawem przekąsek"""
        return f"{self.ticket} [+ Zestaw Przekąsek]"  # Dodaję oznaczenie zestawu do opisu biletu
```


### observers/seat_observer.py

```python
from abc import ABC, abstractmethod  # Importuję klasy do tworzenia abstrakcyjnych klas i metod

class SeatObserver(ABC):
    """Abstrakcyjny obserwator miejsca - wzorzec Observer"""
    
    @abstractmethod
    def update(self, seat):
        """Abstrakcyjna metoda aktualizująca obserwatora o zmianie stanu miejsca"""
        pass

class SeatView(SeatObserver):
    """Konkretny obserwator miejsca, aktualizujący widok"""
    
    def update(self, seat):
        """Aktualizuje widok po zmianie stanu miejsca"""
        # W rzeczywistej aplikacji zaktualizowałoby to widok GUI
        print(f"Miejsce {seat} zmieniło stan na {seat.state}")  # Wyświetlam informację o zmianie stanu

class SeatSubject:
    """Klasa podmiotu obserwowanego - wzorzec Observer"""
    
    def __init__(self):
        """Inicjalizacja podmiotu z pustą listą obserwatorów"""
        self._observers = []  # Inicjalizuję pustą listę obserwatorów
    
    def attach(self, observer):
        """Dodaje obserwatora do listy"""
        if observer not in self._observers:  # Jeśli obserwator nie jest już na liście
            self._observers.append(observer)  # Dodaję obserwatora do listy
    
    def detach(self, observer):
        """Usuwa obserwatora z listy"""
        try:
            self._observers.remove(observer)  # Próbuję usunąć obserwatora z listy
        except ValueError:
            pass  # Ignoruję błąd jeśli obserwator nie jest na liście
    
    def notify(self):
        """Powiadamia wszystkich obserwatorów o zmianie"""
        for observer in self._observers:  # Dla każdego obserwatora na liście
            observer.update(self)  # Wywołuję metodę update z referencją do siebie
```


### states/seat_state.py

```python
from abc import ABC, abstractmethod  # Importuję klasy do tworzenia abstrakcyjnych klas i metod

class SeatState(ABC):
    """Abstrakcyjny stan miejsca - wzorzec State"""
    
    @abstractmethod
    def reserve(self, seat):
        """Abstrakcyjna metoda do rezerwacji miejsca"""
        pass
    
    @abstractmethod
    def cancel(self, seat):
        """Abstrakcyjna metoda do anulowania rezerwacji miejsca"""
        pass
    
    @abstractmethod
    def sell(self, seat):
        """Abstrakcyjna metoda do sprzedaży miejsca"""
        pass
    
    @abstractmethod
    def is_available(self):
        """Abstrakcyjna metoda sprawdzająca czy miejsce jest dostępne"""
        pass

class FreeSeatState(SeatState):
    """Stan wolnego miejsca"""
    
    def reserve(self, seat):
        """Rezerwuje wolne miejsce"""
        seat.state = ReservedSeatState()  # Zmieniam stan miejsca na zarezerwowane
        return True  # Zwracam sukces operacji
    
    def cancel(self, seat):
        """Próba anulowania rezerwacji wolnego miejsca"""
        return False  # Nie można anulować rezerwacji miejsca, które nie jest zarezerwowane
    
    def sell(self, seat):
        """Sprzedaje wolne miejsce"""
        seat.state = SoldSeatState()  # Zmieniam stan miejsca na sprzedane
        return True  # Zwracam sukces operacji
    
    def is_available(self):
        """Sprawdza czy miejsce jest dostępne"""
        return True  # Wolne miejsce jest dostępne
    
    def __str__(self):
        """Zwraca tekstową reprezentację stanu"""
        return "free"  # Zwracam "free" jako reprezentację tekstową stanu

class ReservedSeatState(SeatState):
    """Stan zarezerwowanego miejsca"""
    
    def reserve(self, seat):
        """Próba rezerwacji zarezerwowanego miejsca"""
        return False  # Nie można zarezerwować już zarezerwowanego miejsca
    
    def cancel(self, seat):
        """Anuluje rezerwację miejsca"""
        seat.state = FreeSeatState()  # Zmieniam stan miejsca na wolne
        return True  # Zwracam sukces operacji
    
    def sell(self, seat):
        """Sprzedaje zarezerwowane miejsce"""
        seat.state = SoldSeatState()  # Zmieniam stan miejsca na sprzedane
        return True  # Zwracam sukces operacji
    
    def is_available(self):
        """Sprawdza czy miejsce jest dostępne"""
        return False  # Zarezerwowane miejsce nie jest dostępne
    
    def __str__(self):
        """Zwraca tekstową reprezentację stanu"""
        return "reserved"  # Zwracam "reserved" jako reprezentację tekstową stanu

class SoldSeatState(SeatState):
    """Stan sprzedanego miejsca"""
    
    def reserve(self, seat):
        """Próba rezerwacji sprzedanego miejsca"""
        return False  # Nie można zarezerwować sprzedanego miejsca
    
    def cancel(self, seat):
        """Próba anulowania rezerwacji sprzedanego miejsca"""
        return False  # Nie można anulować rezerwacji sprzedanego miejsca
    
    def sell(self, seat):
        """Próba sprzedaży sprzedanego miejsca"""
        return False  # Nie można sprzedać już sprzedanego miejsca
    
    def is_available(self):
        """Sprawdza czy miejsce jest dostępne"""
        return False  # Sprzedane miejsce nie jest dostępne
    
    def __str__(self):
        """Zwraca tekstową reprezentację stanu"""
        return "sold"  # Zwracam "sold" jako reprezentację tekstową stanu
```


### strategies/pricing_strategy.py

```python
from abc import ABC, abstractmethod  # Importuję klasy do tworzenia abstrakcyjnych klas i metod
from datetime import datetime  # Importuję klasę datetime do obsługi dat

class PricingStrategy(ABC):
    """Abstrakcyjna strategia cenowa - wzorzec Strategy"""
    
    @abstractmethod
    def calculate_price(self, base_price):
        """Abstrakcyjna metoda obliczająca cenę biletu"""
        pass

class RegularPricingStrategy(PricingStrategy):
    """Standardowa strategia cenowa"""
    
    def calculate_price(self, base_price):
        """Oblicza standardową cenę biletu"""
        return base_price  # Zwracam cenę bazową bez modyfikacji

class WeekendPricingStrategy(PricingStrategy):
    """Strategia cenowa na weekendy"""
    
    def calculate_price(self, base_price):
        """Oblicza cenę biletu w weekend (20% drożej)"""
        return base_price * 1.2  # Zwiększam cenę bazową o 20%

class MorningPricingStrategy(PricingStrategy):
    """Strategia cenowa na poranne seanse"""
    
    def calculate_price(self, base_price):
        """Oblicza cenę biletu na poranny seans (20% taniej)"""
        return base_price * 0.8  # Zmniejszam cenę bazową o 20%

class PricingContext:
    """Kontekst dla strategii cenowej - wzorzec Strategy"""
    
    def __init__(self, strategy):
        """Inicjalizacja kontekstu z podaną strategią"""
        self.strategy = strategy  # Zapisuję strategię cenową
    
    def set_strategy(self, strategy):
        """Zmienia strategię cenową"""
        self.strategy = strategy  # Aktualizuję strategię cenową
    
    def calculate_price(self, base_price):
        """Oblicza cenę biletu używając aktualnej strategii"""
        return self.strategy.calculate_price(base_price)  # Deleguje obliczenie ceny do strategii
```


### views/main_window.py

```python
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QLinearGradient

from utils.glass_morphism import BackDropWrapper  # Importuję klasę do efektu glass morphism
from views.movie_view import MovieView  # Importuję widok filmów
from views.screening_view import ScreeningView  # Importuję widok seansów
from views.reservation_view import ReservationView  # Importuję widok rezerwacji

class MainWindow(QMainWindow):
    """Główne okno aplikacji"""
    
    def __init__(self):
        """Inicjalizacja głównego okna"""
        super().__init__()  # Wywołuję konstruktor klasy nadrzędnej
        
        # Ustawiam właściwości okna
        self.setWindowTitle("WSBCinema - System Rezerwacji Biletów")  # Ustawiam tytuł okna
        self.setGeometry(100, 100, 1200, 800)  # Ustawiam pozycję i rozmiar okna
        
        # Tworzę główny widget
        self.central_widget = QWidget()  # Tworzę centralny widget
        self.setCentralWidget(self.central_widget)  # Ustawiam centralny widget
        
        # Tworzę układ
        self.layout = QVBoxLayout(self.central_widget)  # Tworzę pionowy układ dla głównego widgetu
        
        # Tworzę nagłówek
        self.setup_header()  # Wywołuję metodę tworzącą nagłówek
        
        # Tworzę zakładki
        self.setup_tabs()  # Wywołuję metodę tworzącą zakładki
        
        # Ustawiam style
        self.setup_styles()  # Wywołuję metodę ustawiającą style
    
    def setup_header(self):
        """Tworzy nagłówek aplikacji"""
        # Tworzę kontener nagłówka
        header_container = QWidget()  # Tworzę widget dla nagłówka
        header_layout = QVBoxLayout(header_container)  # Tworzę pionowy układ dla nagłówka
        
        # Tworzę tytuł
        title = QLabel("WSBCinema")  # Tworzę etykietę z tytułem
        title.setAlignment(Qt.AlignCenter)  # Wyrównuję tekst do środka
        title.setFont(QFont("Arial", 24, QFont.Bold))  # Ustawiam czcionkę tytułu
        
        # Tworzę podtytuł
        subtitle = QLabel("System Rezerwacji Biletów")  # Tworzę etykietę z podtytułem
        subtitle.setAlignment(Qt.AlignCenter)  # Wyrównuję tekst do środka
        subtitle.setFont(QFont("Arial", 16))  # Ustawiam czcionkę podtytułu
        
        # Dodaję do układu
        header_layout.addWidget(title)  # Dodaję tytuł do układu
        header_layout.addWidget(subtitle)  # Dodaję podtytuł do układu
        
        # Aplikuję efekt glass morphism
        grad = QLinearGradient(0, 0, 1, 1)  # Tworzę gradient liniowy
        grad.setCoordinateMode(QLinearGradient.ObjectMode)  # Ustawiam tryb koordynatów
        grad.setStops([  # Ustawiam punkty zatrzymania gradientu
            (0, QColor(255, 255, 255, 255)), 
            (0.35, QColor(255, 255, 255, 125)), 
            (0.65, QColor(255, 255, 255, 125)), 
            (1, QColor(255, 255, 255, 255))
        ])
        
        backgrounds = [{  # Definiuję tło dla efektu glass morphism
            "background-color": grad, 
            "border": QColor("#FFFFFF"),
            "border-width": 2, 
            "opacity": .4
        }]
        
        header_wrapper = BackDropWrapper(  # Tworzę wrapper z efektem glass morphism
            header_container, 
            blur=10, 
            radius=25, 
            backgrounds=backgrounds
        )
        
        # Dodaję do głównego układu
        self.layout.addWidget(header_wrapper)  # Dodaję nagłówek do głównego układu
    
    def setup_tabs(self):
        """Tworzy zakładki aplikacji"""
        # Tworzę widget zakładek
        self.tabs = QTabWidget()  # Tworzę widget zakładek
        
        # Tworzę zakładki
        self.movie_tab = MovieView()  # Tworzę widok filmów
        self.screening_tab = ScreeningView()  # Tworzę widok seansów
        self.reservation_tab = ReservationView()  # Tworzę widok rezerwacji
        
        # Dodaję zakładki
        self.tabs.addTab(self.movie_tab, "Filmy")  # Dodaję zakładkę filmów
        self.tabs.addTab(self.screening_tab, "Seanse")  # Dodaję zakładkę seansów
        self.tabs.addTab(self.reservation_tab, "Rezerwacje")  # Dodaję zakładkę rezerwacji
        
        # Aplikuję efekt glass morphism
        grad = QLinearGradient(0, 0, 1, 1)  # Tworzę gradient liniowy
        grad.setCoordinateMode(QLinearGradient.ObjectMode)  # Ustawiam tryb koordynatów
        grad.setStops([  # Ustawiam punkty zatrzymania gradientu
            (0, QColor(200, 200, 255, 200)), 
            (1, QColor(150, 150, 255, 150))
        ])
        
        backgrounds = [{  # Definiuję tło dla efektu glass morphism
            "background-color": grad, 
            "border": QColor("#BBBBFF"),
            "border-width": 1, 
            "opacity": .3
        }]
        
        tabs_wrapper = BackDropWrapper(  # Tworzę wrapper z efektem glass morphism
            self.tabs, 
            blur=5, 
            radius=15, 
            backgrounds=backgrounds
        )
        
        # Dodaję do głównego układu
        self.layout.addWidget(tabs_wrapper)  # Dodaję zakładki do głównego układu
    
    def setup_styles(self):
        """Ustawia style dla elementów aplikacji"""
        # Ustawiam styl aplikacji
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                           stop:0 #2c3e50, stop:1 #3498db);
            }
            
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            
            QTabBar::tab {
                background: rgba(255, 255, 255, 100);
                color: white;
                padding: 10px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background: rgba(255, 255, 255, 150);
                font-weight: bold;
            }
            
            QPushButton {
                background-color: rgba(52, 152, 219, 180);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: rgba(41, 128, 185, 200);
            }
            
            QLabel {
                color: white;
            }
        """)  # Ustawiam styl dla różnych elementów interfejsu
```


## Sposób uruchomienia aplikacji

Aby uruchomić aplikację, należy wykonać następujące kroki:

1. Zainstalować wymagane biblioteki:
```
pip install PyQt5
```

2. Stworzyć strukturę katalogów zgodnie z powyższym kodem.
3. Zapisać wszystkie pliki w odpowiednich katalogach zgodnie z podaną strukturą.
4. Uruchomić aplikację:
```
python main.py
```


## Zastosowane wzorce projektowe

W projekcie świadomie zastosowano następujące wzorce projektowe:

1. **Factory Method (Metoda Wytwórcza)** - do tworzenia różnych typów biletów (normalny, ulgowy, VIP) bez konieczności określania ich konkretnych klas. Pozwala łatwo rozszerzać system o nowe rodzaje biletów.
2. **Builder (Budowniczy)** - do konstruowania złożonych obiektów seansów. Umożliwia tworzenie instancji krok po kroku, co jest przydatne przy obiektach z wieloma parametrami.
3. **Singleton** - do zapewnienia tylko jednej instancji bazy danych w całej aplikacji. Gwarantuje, że wszystkie komponenty pracują na tych samych danych.
4. **Facade (Fasada)** - do uproszczenia złożonych operacji związanych z rezerwacją. Ukrywa szczegóły implementacji i zapewnia prosty interfejs.
5. **Decorator (Dekorator)** - do dynamicznego dodawania funkcjonalności do biletów, jak opcja 3D czy zestawy przekąsek, bez modyfikacji istniejących klas.
6. **Observer (Obserwator)** - do powiadamiania o zmianach stanu miejsc. Umożliwia automatyczne aktualizacje interfejsu użytkownika.
7. **State (Stan)** - do zarządzania stanem miejsc (wolne, zarezerwowane, sprzedane). Upraszcza logikę związaną ze zmianami stanów.
8. **Strategy (Strategia)** - do implementacji różnych strategii cenowych. Pozwala na elastyczne obliczanie cen biletów w zależności od różnych czynników.

## Filmy w WSBCinema

W systemie WSBCinema zaimplementowano filmy, które zostały nagrodzone Oscarem dla najlepszego filmu[^1_8]:

1. Oppenheimer (Oscar 2024)
2. Everything Everywhere All at Once (Oscar 2023)
3. CODA (Oscar 2022)
4. Nomadland (Oscar 2021)
5. Parasite (Oscar 2020)
6. Anora (Oscar 2025 - hipotetycznie)

## Funkcjonalności aplikacji

System WSBCinema oferuje następujące funkcjonalności:

1. Zarządzanie repertuarem:
    - Dodawanie i wyświetlanie filmów
    - Definiowanie sal kinowych
    - Tworzenie seansów
2. Proces rezerwacji:
    - Wyświetlanie listy seansów w danym dniu
    - Wybór konkretnego seansu i wyświetlenie planu sali
    - Wybór miejsc do rezerwacji
    - Obliczanie ceny rezerwacji
    - Potwierdzanie rezerwacji
3. Interfejs użytkownika:
    - Nowoczesny interfejs graficzny z efektem glassmorphism
    - Podział na zakładki (Filmy, Seanse, Rezerwacje)
    - Interaktywny plan sali z zaznaczaniem miejsc
