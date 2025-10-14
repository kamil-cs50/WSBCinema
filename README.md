# WSBCinema

## Opis projektu

System rezerwacji biletów kinowych WSBCinema to aplikacja desktopowa symulująca podstawowe funkcjonalności systemu rezerwacji miejsc w kinie. Projekt został zrealizowany z zastosowaniem zasad programowania obiektowego oraz wybranych wzorców projektowych, aby stworzyć elastyczny, rozszerzalny i łatwy w utrzymaniu kod.

## Zaimplementowane funkcjonalności

1. **Zarządzanie repertuarem:**
   - Możliwość dodawania/definiowania filmów (tytuł, czas trwania, kategoria wiekowa).
   - Możliwość definiowania sal kinowych (numer/nazwa, liczba miejsc w rzędach) – dane sal są predefiniowane w kodzie.
   - Możliwość tworzenia seansów (przypisanie filmu do sali w określonym terminie) – seanse są generowane przykładowo przy starcie aplikacji.

2. **Proces rezerwacji:**
   - Możliwość wyświetlenia listy seansów w danym dniu (wybór daty z kalendarza).
   - Możliwość wybrania konkretnego seansu i wyświetlenia planu sali z zaznaczonymi wolnymi i zajętymi miejscami.
   - Możliwość wyboru jednego lub więcej wolnych miejsc do rezerwacji.
   - Obliczanie ceny rezerwacji w oparciu o liczbę i typ biletów (normalny, ulgowy, VIP) z możliwością dekorowania biletów (np. opcja 3D, zestaw przekąsek).
   - Potwierdzenie rezerwacji (zapis rezerwacji do pliku JSON).

3. **Interfejs użytkownika:**
   - Graficzny interfejs użytkownika (GUI) przy użyciu biblioteki PyQt5.
   - Podział na zakładki: "Filmy", "Seanse" oraz "Rezerwacje".

## Zastosowane wzorce projektowe

W projekcie świadomie zastosowano następujące wzorce projektowe. Poniżej zamieszczono fragmenty kodu, które potwierdzają ich zastosowanie zgodnie z opisem w tym pliku.

### Builder (Budowniczy)

Wzorzec Builder jest wykorzystywany do krokowego konstruowania obiektu seansu. Implementacja znajduje się w pliku `builders/screening_builder.py`:

```python
class ScreeningBuilder:
    def __init__(self):
        self.movie = None
        self.cinema_hall = None
        self.date_time = None
        self.base_price = 0

    def set_movie(self, movie):
        self.movie = movie
        return self

    def set_cinema_hall(self, hall):
        self.cinema_hall = hall
        return self

    def set_date_time(self, date_time):
        self.date_time = date_time
        return self

    def set_base_price(self, price):
        self.base_price = price
        return self

    def build(self):
        return Screening(self.movie, self.cinema_hall, self.date_time, self.base_price)
```

### Singleton

Wzorzec Singleton został zastosowany dla zarządzania centralnym repozytorium danych w pliku `utils/database.py`:

```python
class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
            # Inicjalizacja stanu bazy danych
        return cls._instance
```

### Factory Method

Wzorzec fabryki (Factory Method) do tworzenia różnych typów biletów znajduje się w pliku `factories/ticket_factory.py`:

```python
class TicketFactory:
    @staticmethod
    def create_ticket(ticket_type, **kwargs):
        if ticket_type == "normal":
            return NormalTicket(**kwargs)
        elif ticket_type == "ulgowy":
            return DiscountTicket(**kwargs)
        elif ticket_type == "VIP":
            return VIPTicket(**kwargs)
        else:
            raise ValueError("Nieznany typ biletu")
```

### Facade (Fasada)

Fasada upraszczająca obsługę rezerwacji została zaimplementowana w pliku `facades/reservation_facade.py`:

```python
class ReservationFacade:
    def __init__(self):
        self.database = Database()
        self.pricing_strategy = PricingStrategyFactory.get_strategy()

    def reserve_seats(self, screening, seats, ticket_type):
        available = screening.get_available_seats()
        if not all(seat in available for seat in seats):
            raise Exception("Wybrane miejsca nie są dostępne")
        price = self.pricing_strategy.calculate(screening.base_price, len(seats), ticket_type)
        reservation = Reservation(screening, seats, price)
        self.database.save_reservation(reservation)
        return reservation
```

### Decorator (Dekorator)

Wzorzec Dekoratora umożliwia dynamiczne rozszerzanie funkcjonalności biletu. Implementacja znajduje się w pliku `decorators/ticket_decorator.py`:

```python
class TicketDecorator:
    def __init__(self, ticket):
        self.ticket = ticket

    def get_price(self):
        base_price = self.ticket.get_price()
        return base_price + 5  # Dodana dodatkowa opłata, np. za opcję 3D
```

### Observer (Obserwator)

Observer jest używany do monitorowania zmian stanu miejsc w sali. Jego przykładowa implementacja znajduje się w pliku `observers/seat_observer.py`:

```python
class SeatObserver:
    def update(self, seat):
        print(f"Zmiana stanu miejsca: {seat.row}-{seat.number} na {seat.state}")
```

### State (Stan)

Wzorzec State, zarządzający stanem miejsc (wolne, zarezerwowane, sprzedane), został zaimplementowany w pliku `states/seat_state.py`:

```python
class FreeSeatState:
    def __str__(self):
        return "Wolne"

class ReservedSeatState:
    def __str__(self):
        return "Zarezerwowane"

class SoldSeatState:
    def __str__(self):
        return "Sprzedane"
```

### Strategy (Strategia)

Wzorzec Strategii umożliwia elastyczną kalkulację cen biletów. Implementacja znajduje się w pliku `strategies/pricing_strategy.py`:

```python
class StandardPricingStrategy:
    def calculate(self, base_price, quantity, ticket_type):
        return base_price * quantity

class WeekendPricingStrategy:
    def calculate(self, base_price, quantity, ticket_type):
        return base_price * quantity * 1.2  # Przykładowa logika dla weekendu
```

## Struktura projektu

```
.
├── README.md
├── main.py
├── dokumentacja
│   ├── diagram.md
│   └── plan.md
├── models
│   ├── __init__.py
│   ├── movie.py
│   ├── cinema_hall.py
│   ├── seat.py
│   ├── screening.py
│   ├── ticket.py
│   └── reservation.py
├── factories
│   ├── __init__.py
│   └── ticket_factory.py
├── builders
│   ├── __init__.py
│   └── screening_builder.py
├── utils
│   ├── __init__.py
│   ├── database.py
│   └── glass_morphism.py
├── facades
│   ├── __init__.py
│   └── reservation_facade.py
├── decorators
│   ├── __init__.py
│   └── ticket_decorator.py
├── observers
│   ├── __init__.py
│   └── seat_observer.py
├── states
│   ├── __init__.py
│   └── seat_state.py
├── strategies
│   ├── __init__.py
│   └── pricing_strategy.py
└── views
    ├── __init__.py
    ├── main_window.py
    ├── reservation_view.py
    └── screening_view.py
```

## Uruchomienie aplikacji

Aby uruchomić aplikację, wykonaj następujące kroki:

1. Sklonuj repozytorium:
   ```bash
   git clone <adres_repozytorium>
   cd WSBCinema
   ```
2. Utwórz i aktywuj wirtualne środowisko:
   - Na macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Na Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
3. Zainstaluj wymagane biblioteki:
   ```bash
   pip install PyQt5
   ```
4. Uruchom aplikację:
   ```bash
   python main.py
   ```