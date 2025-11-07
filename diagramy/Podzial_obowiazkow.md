# Podział Obowiązków - Projekt WSBCinema

## Zespół projektowy
**Kamil Tukendorf, Bartek Jankowski, Damian Banaszek, Filip Waroch, Marcin Gałażyn, Tomek Szyluk**

## Informacje o projekcie
- **Nazwa:** WSBCinema - System Rezerwacji Biletów Kinowych
- **Technologia:** Python 3.13, PyQt5
- **Architektura:** MVC z wzorcami projektowymi
- **Czas realizacji:** 8 tygodni (październik - listopad 2024)
- **Łączny nakład pracy:** ~240 godzin (6 osób × 40 godzin)

---

## **Kamil Tukendorf**
### Zakres odpowiedzialności:
- Implementacja modeli podstawowych (`models/movie.py`, `models/cinema_hall.py`, `models/seat.py`)
- Wzorzec State (`states/seat_state.py`)
- Koordynacja projektu i integracja modułów

### Wypowiedź obrończa:
*"Odpowiadałem za fundament całego systemu - modele danych. Zaimplementowałem trzy kluczowe klasy: Movie z atrybutami title, duration_minutes i age_category, CinemaHall z metodą get_total_seats() obliczającą pojemność sali, oraz Seat dziedziczący po SeatSubject dla wsparcia wzorca Observer. W klasie Seat zastosowałem property dla atrybutu state, co umożliwia automatyczne powiadamianie obserwatorów przy każdej zmianie stanu.*

*Szczególnie skupiłem się na implementacji wzorca State. Stworzyłem abstrakcyjną klasę SeatState z metodami reserve(), cancel(), sell() i is_available(), oraz trzy konkretne stany: FreeSeatState (pozwala na rezerwację i sprzedaż), ReservedSeatState (pozwala na anulowanie i sprzedaż) oraz SoldSeatState (blokuje wszystkie operacje). Każdy stan implementuje własną logikę przejść - na przykład FreeSeatState.reserve() zmienia stan na ReservedSeatState. To rozwiązanie eliminuje skomplikowane instrukcje warunkowe i czyni kod łatwym do rozszerzenia o nowe stany.*

*Technicznie, wykorzystałem dziedziczenie (Seat extends SeatSubject), kompozycję (Seat zawiera SeatState) oraz polimorfizm (wywołania metod na obiekcie state są delegowane do konkretnej implementacji). Dodatkowo koordynowałem pracę zespołu przez code review i zapewnienie spójności nazewnictwa oraz interfejsów między modułami. "*

---

## **Bartek Jankowski**
### Zakres odpowiedzialności:
- Implementacja wzorców Builder (`builders/screening_builder.py`) i Factory (`factories/ticket_factory.py`)
- Model Screening (`models/screening.py`)
- Logika tworzenia seansów i biletów

### Wypowiedź obrończa:
*"Zajmowałem się implementacją wzorców kreacyjnych, które są fundamentem tworzenia obiektów w systemie. ScreeningBuilder implementuje wzorzec Builder z fluent interface - każda metoda set_movie(), set_cinema_hall(), set_date_time() i set_base_price() zwraca self, co pozwala na łańcuchowe wywoływanie: builder.set_movie(m).set_cinema_hall(h).build(). Metoda build() waliduje kompletność danych (sprawdza czy wszystkie wymagane pola są ustawione) i wywołuje reset() po utworzeniu obiektu, przygotowując builder do kolejnego użycia.*

*W TicketFactory zastosowałem wzorzec Factory Method z hierarchią klas: abstrakcyjna TicketFactory definiuje interfejs create_ticket(screening, seat), a trzy konkretne fabryki implementują różne logiki cenowe: RegularTicketFactory (100% ceny bazowej), DiscountedTicketFactory (70% - zniżka 30%) oraz VIPTicketFactory (150% - dopłata 50%). To oddziela logikę tworzenia od logiki biznesowej i pozwala łatwo dodawać nowe typy biletów.*

*Model Screening jest najbardziej złożony - zawiera metodę _initialize_seats() tworzącą obiekty Seat dla każdego miejsca w sali (zagnieżdżone pętle przez rzędy i miejsca), metodę get_available_seats() filtrującą miejsca przez is_available(), oraz find_seat(row, number) do wyszukiwania konkretnego miejsca. Screening agreguje Movie, CinemaHall i kompozytowo zawiera listę Seat. Technicznie wykorzystałem list comprehension, datetime do obsługi czasu oraz type hints dla lepszej czytelności. "*

---

## **Damian Banaszek**
### Zakres odpowiedzialności:
- Implementacja wzorców Singleton (`utils/database.py`) i Facade (`facades/reservation_facade.py`)
- Model Reservation (`models/reservation.py`)
- Zarządzanie danymi i uproszczenie procesu rezerwacji

### Wypowiedź obrończa:
*"Odpowiadałem za zarządzanie danymi i uproszczenie złożonych operacji. Wzorzec Singleton w Database implementuję przez nadpisanie metody __new__() - sprawdzam czy cls._instance istnieje, jeśli nie to tworzę nową instancję przez super().__new__(cls), w przeciwnym razie zwracam istniejącą. Dodatkowo używam flagi _is_initialized aby metoda _initialize() wykonała się tylko raz, inicjalizując listy movies, cinema_halls, screenings i reservations. Singleton zapewnia globalny punkt dostępu do danych i eliminuje problemy z synchronizacją.*

*Database zawiera metody CRUD: add_movie(), add_cinema_hall(), add_screening(), add_reservation() oraz gettery get_movies(), get_screenings() itd. Kluczowa jest metoda get_screenings_for_date(date) używająca list comprehension z filtrowaniem przez date_time.date(). Implementuję również persystencję - save_reservations() serializuje rezerwacje do JSON przez reservation.to_dict(), a load_reservations() deserializuje przez Reservation.from_dict(). Obsługuję błędy IOError i JSONDecodeError.*

*ReservationFacade to wzorzec Facade upraszczający interfejs. Metoda make_reservation() agreguje operacje: walidację miejsc, zmianę stanów (seat.state = ReservedSeatState()), tworzenie Reservation i zapis do bazy. Metoda calculate_price() używa fabryki biletów do obliczenia ceny, a get_available_ticket_options() zwraca słownik fabryk w zależności od sali (Sala VIP ma tylko VIPTicketFactory).*

*Model Reservation używa uuid.uuid4() dla unikalnego ID, datetime.now() dla timestamp, oraz sum() z generator expression do obliczenia total_price. Metoda to_dict() serializuje do JSON (używam isoformat() dla dat), a statyczna from_dict() deserializuje z walidacją i obsługą błędów. "*

---

## **Filip Waroch**
### Zakres odpowiedzialności:
- Implementacja wzorców Decorator (`decorators/ticket_decorator.py`) i Strategy (`strategies/pricing_strategy.py`)
- Model Ticket (`models/ticket.py`)
- System cenowy i rozszerzanie funkcjonalności biletów

### Wypowiedź obrończa:
*"Skupiłem się na elastycznym systemie cenowym i dynamicznym rozszerzaniu funkcjonalności. Wzorzec Decorator implementuję przez dziedziczenie i kompozycję jednocześnie - TicketDecorator dziedziczy po Ticket (aby zachować interfejs) i zawiera referencję _ticket do opakowywanego obiektu. Używam @property dla price, screening i seat, które delegują wywołania do _ticket. ThreeDTicketDecorator nadpisuje property price zwracając self._ticket.price + 5, a SnackComboTicketDecorator dodaje 15 zł. Metoda __str__() rozszerza opis bazowego biletu o informacje o dodatkach.*

*Kluczowe jest to, że dekoratory można łączyć: SnackComboTicketDecorator(ThreeDTicketDecorator(ticket)) doda 20 zł. To realizuje zasadę Open/Closed - klasa Ticket jest zamknięta na modyfikacje, ale otwarta na rozszerzenia. Technicznie wykorzystuję properties zamiast zwykłych metod get_price(), co jest bardziej pythoniczne.*

*Wzorzec Strategy implementuję przez abstrakcyjną klasę PricingStrategy z metodą calculate_price(base_price). RegularPricingStrategy zwraca base_price bez zmian, WeekendPricingStrategy mnoży przez 1.2 (20% drożej), a MorningPricingStrategy przez 0.8 (20% taniej). PricingContext przechowuje referencję do strategii i deleguje do niej obliczenia. Metoda set_strategy() pozwala dynamicznie zmieniać strategię w runtime.*

*Model Ticket jest prosty ale kluczowy - zawiera screening, seat i price. Hierarchia RegularTicket, DiscountedTicket, VIPTicket to puste klasy (pass) - różnice cenowe są w fabrykach. To separacja odpowiedzialności: Ticket reprezentuje bilet, Factory tworzy z odpowiednią ceną, Decorator rozszerza funkcjonalność, Strategy modyfikuje cenę. "*

---

## **Marcin Gałażyn**
### Zakres odpowiedzialności:
- Implementacja wzorca Observer (`observers/seat_observer.py`)
- Główny interfejs aplikacji (`views/main_window.py`)
- Integracja GUI z logiką biznesową

### Wypowiedź obrończa:
*"Odpowiadałem za komunikację między komponentami i główny interfejs. Wzorzec Observer implementuję przez trzy klasy: abstrakcyjną SeatObserver z metodą update(seat), konkretną SeatView implementującą update() (wyświetla print z informacją o zmianie), oraz SeatSubject z listą _observers i metodami attach(), detach() i notify(). Klasa Seat dziedziczy po SeatSubject, a setter property state wywołuje self.notify() po każdej zmianie, co automatycznie powiadamia wszystkich obserwatorów. To luźne powiązanie - Seat nie wie nic o konkretnych obserwatorach.*

*MainWindow dziedziczy po QMainWindow z PyQt5. W __init__() konfiguruję geometrię (1200x800), tworzę QVBoxLayout jako główny układ, wywołuję setup_header() tworzący QLabel z tytułem i podtytułem, oraz setup_tabs() tworzący QTabWidget z trzema zakładkami. Kluczowe jest połączenie sygnału: self.screening_tab.screening_selected.connect(self.handle_screening_selected) - gdy użytkownik wybierze seans w ScreeningView, sygnał pyqtSignal(object) emituje obiekt Screening, a slot handle_screening_selected() przekazuje go do ReservationView i przełącza zakładkę przez setCurrentWidget().*

*Metoda setup_styles() używa Qt Style Sheets (CSS-like) do stylowania - gradient tła przez qlineargradient, rgba() dla przezroczystości, border-radius dla zaokrągleń. Zastosowałem glass morphism przez BackDropWrapper z QGraphicsBlurEffect, choć w finalnej wersji jest wyłączony dla stabilności. Technicznie wykorzystuję Qt signals/slots (event-driven programming), layouts (QVBoxLayout, QHBoxLayout) dla responsywności, oraz composition (MainWindow zawiera widoki). "*

---

## **Tomek Szyluk**
### Zakres odpowiedzialności:
- Implementacja widoków specjalistycznych (`views/screening_view.py`, `views/reservation_view.py`)
- Utilities i wsparcie GUI (`utils/glass_morphism.py`)
- Testy i dokumentacja techniczna

### Wypowiedź obrończa:
*"Zajmowałem się najbardziej złożonymi widokami aplikacji. ScreeningView definiuje sygnał screening_selected = pyqtSignal(object) do komunikacji z MainWindow. W setup_date_selection() tworzę QCalendarWidget z sygnałem selectionChanged.connect(self.on_date_selected), który wywołuje load_screenings_for_date(). Ta metoda pobiera seanse przez database.get_screenings_for_date(date), iteruje przez nie i dodaje do QListWidget. Slot on_screening_selected(current, previous) używa next() z generator expression do znalezienia obiektu Screening pasującego do wybranego tekstu - to eleganckie rozwiązanie bez pętli. Przycisk "Wybierz seans" emituje sygnał screening_selected.emit(self.selected_screening).*

*ReservationView jest najbardziej skomplikowany - 450+ linii. Używam QHBoxLayout z dwiema kolumnami: lewa dla planu sali, prawa dla legendy. Metoda display_seat_layout() tworzy QGridLayout z przyciskami QPushButton dla każdego miejsca - używam setProperty("seat_obj", seat) do przechowania referencji, sprawdzam stan przez seat.state.__class__.__name__ (porównanie typu) i stylizuję kolorem (lightgreen/orange/red). Slot toggle_seat_selection() używa sender() do identyfikacji klikniętego przycisku, property("seat_obj") do pobrania obiektu Seat, i modyfikuje listę selected_seats.*

*Metoda make_reservation() pokazuje QInputDialog dla imienia, ReservationSummaryDialog (custom QDialog) z podsumowaniem, wywołuje facade.make_reservation(), i wyświetla QMessageBox z potwierdzeniem. Używam try-except do obsługi błędów. Metoda update_price() używa facade.calculate_price() z wybraną fabryką biletów z QComboBox.*

*Glass morphism w utils/glass_morphism.py używa QGraphicsBlurEffect i QGraphicsOpacityEffect dla efektu rozmycia. który ostatecznie nie został zaimplementowany"*

---


### Statystyki projektu:
- **Liczba klas:** 30 klas
- **Liczba wzorców projektowych:** 8 wzorców
- **Liczba plików źródłowych:** 19 plików
- **Średnia liczba linii na osobę:** ~375 linii

### Równy podział odpowiedzialności:

**Każdy członek zespołu:**
1. ✅ Implementował kod (modele, wzorce lub widoki)
2. ✅ Uczestniczył w code review
3. ✅ Testował integrację z innymi modułami
4. ✅ Wniósł równy wkład czasowy (~40 godzin/osoba)

**Podział według obszarów:**
- **Warstwa danych (Models):** Kamil, Bartek, Damian, Filip
- **Wzorce projektowe:** Wszyscy (po 1-2 wzorce)
- **Warstwa prezentacji (Views):** Marcin, Tomek
- **Integracja i testy:** Wszyscy wspólnie



### Współpraca zespołowa:
- **Spotkania:** 2 razy w tygodniu (planowanie i code review)
- **Narzędzia:** Git, GitHub, Discord
- **Metodyka:** Agile/Scrum z 2-tygodniowymi sprintami
- **Code review:** Każdy commit był recenzowany przez minimum 1 osobę

**Każdy członek zespołu wniósł równy i istotny wkład w projekt, implementując zarówno kod jak i dokumentację w swoim obszarze odpowiedzialności. Projekt został zrealizowany w pełni zespołowo z zachowaniem wysokiej jakości kodu i spójności architektury.**