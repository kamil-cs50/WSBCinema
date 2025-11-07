# Diagramy Projektu WSBCinema

## Zawartość

### 1. Diagram Gantta (diagram_gantta.jpeg)
Przedstawia harmonogram realizacji projektu z podziałem na etapy:
- Analiza wymagań (5 dni)
- Projektowanie architektury (7 dni)
- Implementacja modeli (10 dni)
- Implementacja wzorców projektowych (12 dni)
- Implementacja GUI (15 dni)
- Testy (8 dni)
- Dokumentacja (5 dni)

### 2. Diagram Klas (diagram_klas.jpeg)
Kompleksowy diagram przedstawiający:
- **Modele**: Movie, CinemaHall, Seat, Screening, Ticket, Reservation
- **Wzorce projektowe**:
  - Builder: ScreeningBuilder
  - Singleton: Database
  - Factory: TicketFactory i jego implementacje
  - Facade: ReservationFacade
  - Decorator: TicketDecorator (3D, przekąski)
  - Observer: SeatObserver, SeatView, SeatSubject
  - State: SeatState (Free, Reserved, Sold)
  - Strategy: PricingStrategy (Regular, Weekend, Morning)
- **Widoki**: MainWindow, MovieView, ScreeningView, ReservationView
- Relacje między klasami (dziedziczenie, kompozycja, agregacja, zależności)

### 3. Diagram Przypadków Użycia (diagram_przypadkow_uzycia.jpeg)
Przedstawia interakcje użytkownika z systemem:
- Przeglądanie filmów
- Wybór daty i przeglądanie seansów
- Wybór seansu i wyświetlenie planu sali
- Wybór miejsc i typu biletu
- Dodawanie opcji (3D, przekąski)
- Obliczanie ceny i potwierdzanie rezerwacji
- Zapisywanie rezerwacji przez system

### 4. Diagram Aktywności - Rezerwacja Biletów (diagram_aktywnosci_rezerwacja.jpeg)
Szczegółowy przepływ procesu rezerwacji:
- Wybór seansu i daty
- Wyświetlenie planu sali
- Wybór miejsc (z walidacją dostępności)
- Wybór typu biletu
- Opcjonalne dodanie dekoratorów (3D, przekąski)
- Obliczenie ceny
- Potwierdzenie i zapis rezerwacji
- Zmiana stanu miejsc

### 5. Diagram Aktywności - Przeglądanie Seansów (diagram_aktywnosci_przegladanie_seansow.jpeg)
Przepływ przeglądania dostępnych seansów:
- Otwarcie zakładki "Seanse"
- Pobranie danych z bazy
- Wybór daty z kalendarza
- Filtrowanie seansów
- Wyświetlenie szczegółów każdego seansu
- Obsługa braku dostępnych seansów
- Przejście do rezerwacji lub zmiana daty

## Formaty plików
- `.puml` - źródłowe pliki PlantUML
- `.jpeg` - wyeksportowane diagramy w formacie JPEG
- `.png` - wyeksportowane diagramy w formacie PNG (wersja pośrednia)

## Narzędzia
Diagramy zostały wygenerowane przy użyciu PlantUML.
