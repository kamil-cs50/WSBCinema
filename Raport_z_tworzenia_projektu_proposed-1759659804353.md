# Raport z realizacji projektu WSBCinema – System rezerwacji biletów kinowych

## 1. Wprowadzenie

Projekt WSBCinema stanowi aplikację desktopową symulującą funkcjonalności systemu rezerwacji miejsc w kinie. Celem przedsięwzięcia było stworzenie rozwiązania informatycznego, które w sposób kompleksowy obsługuje proces zarządzania repertuarem kinowym oraz umożliwia użytkownikom dokonywanie rezerwacji biletów na wybrane seanse. Aplikacja została zaprojektowana z wykorzystaniem paradygmatu programowania obiektowego oraz klasycznych wzorców projektowych, co zapewnia jej modularność, skalowalność oraz łatwość w utrzymaniu i rozbudowie.

System oferuje podstawowe funkcjonalności niezbędne w kontekście zarządzania kinem, w tym: definiowanie filmów wraz z ich parametrami (tytuł, czas trwania, kategoria wiekowa), zarządzanie salami kinowymi o różnej konfiguracji miejsc, tworzenie seansów filmowych w określonych terminach, wizualizację dostępności miejsc w sali oraz realizację procesu rezerwacji z uwzględnieniem różnych typów biletów i opcji dodatkowych. Interfejs graficzny aplikacji został zrealizowany przy użyciu biblioteki PyQt5, co zapewnia intuicyjną obsługę oraz estetyczny wygląd zgodny ze współczesnymi standardami projektowania interfejsów użytkownika.

## 2. Etapy realizacji projektu

### 2.1. Faza analizy i projektowania

Proces tworzenia aplikacji rozpoczęto od przeprowadzenia analizy wymagań funkcjonalnych oraz niefunkcjonalnych systemu. Zidentyfikowano kluczowe przypadki użycia, takie jak przeglądanie repertuaru, wybór seansu, rezerwacja miejsc oraz zarządzanie danymi o filmach i salach kinowych. Na podstawie zebranych wymagań opracowano wstępny model koncepcyjny systemu, identyfikując główne encje domenowe: Film (Movie), Sala kinowa (CinemaHall), Seans (Screening), Miejsce (Seat), Bilet (Ticket) oraz Rezerwacja (Reservation).

W kolejnym kroku dokonano wyboru wzorców projektowych, które miały zostać zaimplementowane w projekcie. Zdecydowano się na zastosowanie ośmiu klasycznych wzorców: Builder, Singleton, Factory Method, Facade, Decorator, Observer, State oraz Strategy. Każdy z wybranych wzorców został przypisany do konkretnego obszaru funkcjonalnego aplikacji, gdzie jego zastosowanie przynosi wymierne korzyści w zakresie elastyczności, rozszerzalności lub uproszczenia kodu.

Zaprojektowano również strukturę katalogów projektu, która odzwierciedla podział na warstwy logiczne: modele danych (models), fabryki (factories), budowniczych (builders), narzędzia pomocnicze (utils), fasady (facades), dekoratory (decorators), obserwatorzy (observers), stany (states), strategie (strategies) oraz widoki interfejsu użytkownika (views). Taka organizacja kodu sprzyja przejrzystości projektu oraz ułatwia nawigację po kodzie źródłowym.

### 2.2. Implementacja warstwy modeli danych

Implementację rozpoczęto od stworzenia podstawowych klas reprezentujących encje domenowe systemu. Klasa Movie została zaprojektowana jako prosta struktura danych przechowująca informacje o filmie: tytuł, czas trwania w minutach oraz kategorię wiekową. Klasa CinemaHall reprezentuje salę kinową i zawiera informacje o jej nazwie oraz wymiarach (liczba rzędów i miejsc w rzędzie).

Szczególną uwagę poświęcono klasie Seat, która reprezentuje pojedyncze miejsce w sali kinowej. W tej klasie zaimplementowano wzorzec State, umożliwiający zarządzanie stanem miejsca (wolne, zarezerwowane, sprzedane). Każdy stan został zdefiniowany jako osobna klasa (FreeSeatState, ReservedSeatState, SoldSeatState), co pozwala na łatwe rozszerzenie systemu o nowe stany oraz zapewnia spójność logiki biznesowej związanej ze zmianą stanów.

Klasa Screening agreguje obiekty Movie, CinemaHall oraz listę obiektów Seat, tworząc kompletną reprezentację seansu filmowego. W konstruktorze tej klasy następuje automatyczna inicjalizacja wszystkich miejsc w sali na podstawie jej wymiarów. Klasa Reservation przechowuje informacje o dokonanej rezerwacji, w tym referencję do seansu, listę zarezerwowanych miejsc oraz całkowitą cenę.

### 2.3. Implementacja wzorców kreacyjnych

W celu zapewnienia elastycznego tworzenia obiektów zaimplementowano trzy wzorce kreacyjne. Wzorzec Builder został zastosowany w klasie ScreeningBuilder, która umożliwia krokowe konstruowanie obiektów Screening. Dzięki metodom set_movie, set_cinema_hall, set_date_time oraz set_base_price możliwe jest stopniowe definiowanie parametrów seansu, a metoda build finalizuje proces tworzenia obiektu. Takie podejście zwiększa czytelność kodu oraz umożliwia tworzenie obiektów z różnymi konfiguracjami parametrów.

Wzorzec Singleton został zaimplementowany w klasie Database, która pełni rolę centralnego repozytorium danych aplikacji. Implementacja wzorca zapewnia, że w całym systemie istnieje tylko jedna instancja bazy danych, co gwarantuje spójność danych oraz eliminuje problemy związane z synchronizacją dostępu do współdzielonych zasobów. Klasa Database zarządza kolekcjami filmów, sal kinowych, seansów oraz rezerwacji, a także odpowiada za persystencję danych w formacie JSON.

Wzorzec Factory Method został zastosowany w klasie TicketFactory, która odpowiada za tworzenie różnych typów biletów (normalny, ulgowy, VIP). Metoda statyczna create_ticket przyjmuje typ biletu jako parametr i zwraca odpowiednią instancję klasy dziedziczącej po abstrakcyjnej klasie Ticket. Takie rozwiązanie centralizuje logikę tworzenia biletów oraz ułatwia dodawanie nowych typów biletów w przyszłości.

### 2.4. Implementacja wzorców strukturalnych

W warstwie logiki biznesowej zaimplementowano dwa wzorce strukturalne. Wzorzec Facade został zastosowany w klasie ReservationFacade, która stanowi uproszczony interfejs do złożonego procesu rezerwacji miejsc. Fasada ukrywa przed klientem szczegóły implementacyjne związane z weryfikacją dostępności miejsc, obliczaniem ceny oraz zapisem rezerwacji do bazy danych. Metoda reserve_seats przyjmuje obiekt seansu, listę miejsc oraz typ biletu, a następnie koordynuje działanie różnych komponentów systemu w celu realizacji rezerwacji.

Wzorzec Decorator został zaimplementowany w klasie TicketDecorator, która umożliwia dynamiczne rozszerzanie funkcjonalności biletów o dodatkowe opcje, takie jak projekcja 3D czy zestaw przekąsek. Każdy dekorator opakowuje obiekt biletu i modyfikuje jego cenę poprzez dodanie odpowiedniej opłaty. Możliwe jest łańcuchowe stosowanie dekoratorów, co pozwala na elastyczne komponowanie różnych kombinacji opcji dodatkowych.

### 2.5. Implementacja wzorców behawioralnych

W celu zapewnienia elastyczności w zakresie logiki biznesowej zaimplementowano trzy wzorce behawioralne. Wzorzec Observer został zastosowany w klasie SeatObserver, która monitoruje zmiany stanu miejsc w sali. Gdy miejsce zmienia swój stan (np. z wolnego na zarezerwowane), obserwator zostaje powiadomiony i może wykonać odpowiednie akcje, takie jak aktualizacja interfejsu użytkownika czy logowanie zdarzenia.

Wzorzec Strategy został zaimplementowany w module pricing_strategy, gdzie zdefiniowano różne strategie kalkulacji cen biletów. Klasa StandardPricingStrategy implementuje podstawową logikę cenową, podczas gdy WeekendPricingStrategy stosuje podwyższone ceny w weekendy. Strategia cenowa jest wybierana dynamicznie w zależności od kontekstu, co umożliwia łatwe dostosowanie polityki cenowej bez modyfikacji kodu klienta.

Wzorzec State, jak wspomniano wcześniej, został zaimplementowany w kontekście zarządzania stanami miejsc. Każdy stan definiuje dozwolone przejścia do innych stanów oraz zachowanie specyficzne dla danego stanu, co zapewnia spójność logiki biznesowej oraz eliminuje potrzebę stosowania złożonych instrukcji warunkowych.

### 2.6. Implementacja interfejsu użytkownika

Warstwa prezentacji została zrealizowana przy użyciu biblioteki PyQt5. Główne okno aplikacji (MainWindow) zawiera system zakładek umożliwiający przełączanie się między różnymi widokami: zarządzaniem filmami (MovieView), przeglądaniem seansów (ScreeningView) oraz zarządzaniem rezerwacjami (ReservationView).

Widok seansów umożliwia wybór daty z kalendarza oraz wyświetla listę seansów zaplanowanych na wybrany dzień. Po wybraniu konkretnego seansu użytkownik jest przenoszony do widoku rezerwacji, gdzie prezentowany jest plan sali z wizualizacją dostępności poszczególnych miejsc. Miejsca wolne, zarezerwowane i sprzedane są oznaczone różnymi kolorami, co ułatwia orientację w dostępności miejsc.

Proces rezerwacji obejmuje wybór miejsc poprzez kliknięcie na odpowiednie przyciski reprezentujące miejsca, wybór typu biletu oraz opcjonalnie dodanie opcji dodatkowych poprzez zastosowanie dekoratorów. System automatycznie oblicza całkowitą cenę rezerwacji i prezentuje ją użytkownikowi przed potwierdzeniem. Po zatwierdzeniu rezerwacji dane są zapisywane do pliku JSON, co zapewnia persystencję danych między sesjami aplikacji.

### 2.7. Testowanie i finalizacja

W fazie testowania przeprowadzono weryfikację poprawności działania wszystkich funkcjonalności systemu. Przetestowano proces dodawania filmów, tworzenia seansów, rezerwacji miejsc oraz zapisywania i wczytywania danych z pliku JSON. Zidentyfikowane błędy zostały naprawione, a kod został zoptymalizowany pod kątem wydajności i czytelności.

Przygotowano również dokumentację projektu, w tym plik README.md zawierający opis funkcjonalności, struktury projektu oraz instrukcję uruchomienia aplikacji. Dokumentacja zawiera również fragmenty kodu ilustrujące implementację poszczególnych wzorców projektowych, co ułatwia zrozumienie architektury systemu.

## 3. Podsumowanie

Projekt WSBCinema został zrealizowany zgodnie z założeniami, implementując wszystkie zaplanowane funkcjonalności oraz wzorce projektowe. Zastosowanie paradygmatu programowania obiektowego oraz klasycznych wzorców projektowych zaowocowało stworzeniem aplikacji o wysokiej jakości kodu, która jest łatwa w utrzymaniu oraz gotowa do dalszej rozbudowy. System stanowi solidną podstawę do ewentualnego rozszerzenia o dodatkowe funkcjonalności, takie jak integracja z systemami płatności online, zarządzanie użytkownikami czy generowanie raportów statystycznych. Realizacja projektu pozwoliła na praktyczne zastosowanie wiedzy teoretycznej z zakresu inżynierii oprogramowania oraz pogłębienie umiejętności programistycznych w języku Python.
