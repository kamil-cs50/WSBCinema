# Raport z realizacji projektu WSBCinema – System rezerwacji biletów kinowych

## 1. Wprowadzenie

Projekt WSBCinema stanowi aplikację desktopową symulującą funkcjonalności systemu rezerwacji miejsc w kinie. Celem przedsięwzięcia było stworzenie rozwiązania informatycznego, które w sposób kompleksowy obsługuje proces zarządzania repertuarem kinowym oraz umożliwia użytkownikom dokonywanie rezerwacji biletów na wybrane seanse. Aplikacja została zaprojektowana z wykorzystaniem paradygmatu programowania obiektowego oraz klasycznych wzorców projektowych, co zapewnia jej modularność, skalowalność oraz łatwość w utrzymaniu i rozbudowie.

System oferuje podstawowe funkcjonalności niezbędne w kontekście zarządzania kinem, w tym: definiowanie filmów wraz z ich parametrami (tytuł, czas trwania, kategoria wiekowa), zarządzanie salami kinowymi o różnej konfiguracji miejsc, tworzenie seansów filmowych w określonych terminach, wizualizację dostępności miejsc w sali oraz realizację procesu rezerwacji z uwzględnieniem różnych typów biletów i opcji dodatkowych. Interfejs graficzny aplikacji został zrealizowany przy użyciu biblioteki PyQt5, co zapewnia intuicyjną obsługę oraz estetyczny wygląd zgodny ze współczesnymi standardami projektowania interfejsów użytkownika.

Aplikacja WSBCinema znajduje zastosowanie zarówno w celach edukacyjnych, jako przykład implementacji wzorców projektowych w praktycznym projekcie, jak i jako prototyp systemu, który mógłby zostać rozbudowany do pełnoprawnego systemu rezerwacji biletów kinowych. System umożliwia symulację pełnego cyklu życia rezerwacji – od przeglądania dostępnych seansów, przez wybór miejsc, aż po finalizację rezerwacji z automatycznym zapisem danych do pliku JSON, co zapewnia persystencję informacji między sesjami aplikacji.

## 2. Część I – Planowanie projektu

### 2.1. Analiza wymagań i identyfikacja przypadków użycia

Proces tworzenia aplikacji rozpoczęto od przeprowadzenia szczegółowej analizy wymagań funkcjonalnych oraz niefunkcjonalnych systemu. W ramach analizy funkcjonalnej zidentyfikowano kluczowe przypadki użycia, które system powinien obsługiwać. Do najważniejszych przypadków użycia zaliczono: przeglądanie repertuaru filmowego z możliwością wyświetlania szczegółowych informacji o filmach, przeglądanie dostępnych seansów w wybranym dniu z wykorzystaniem kalendarza, wybór konkretnego seansu i wyświetlenie planu sali z wizualizacją dostępności miejsc, wybór jednego lub wielu miejsc do rezerwacji, wybór typu biletu (normalny, ulgowy, VIP) oraz opcjonalnych dodatków, obliczanie całkowitej ceny rezerwacji oraz finalizację rezerwacji z zapisem do systemu.

W zakresie wymagań niefunkcjonalnych określono, że aplikacja powinna charakteryzować się intuicyjnym interfejsem użytkownika, responsywnością działania, możliwością persystencji danych między sesjami oraz modularną architekturą umożliwiającą łatwą rozbudowę funkcjonalności. Szczególny nacisk położono na zastosowanie wzorców projektowych, które miały stanowić fundament architektury systemu oraz demonstrować dobre praktyki inżynierii oprogramowania.

Na podstawie zebranych wymagań opracowano wstępny model koncepcyjny systemu, identyfikując główne encje domenowe oraz relacje między nimi. Zidentyfikowano następujące kluczowe encje: Film (Movie) reprezentujący informacje o filmie, Sala kinowa (CinemaHall) opisującą konfigurację sali, Seans (Screening) łączący film z salą i terminem, Miejsce (Seat) reprezentujące pojedyncze miejsce w sali, Bilet (Ticket) zawierający informacje o typie i cenie biletu oraz Rezerwacja (Reservation) agregującą wszystkie informacje o dokonanej rezerwacji.

### 2.2. Wybór wzorców projektowych i ich uzasadnienie

W kolejnym etapie planowania dokonano świadomego wyboru wzorców projektowych, które miały zostać zaimplementowane w projekcie. Zdecydowano się na zastosowanie ośmiu klasycznych wzorców: Builder, Singleton, Factory Method, Facade, Decorator, Observer, State oraz Strategy. Każdy z wybranych wzorców został przypisany do konkretnego obszaru funkcjonalnego aplikacji, gdzie jego zastosowanie przynosi wymierne korzyści.

Wzorzec Builder został wybrany do konstruowania obiektów Screening, ponieważ seans wymaga ustawienia wielu parametrów (film, sala, data, cena), a wzorzec ten umożliwia czytelne i elastyczne tworzenie obiektów z różnymi konfiguracjami. Wzorzec Singleton został zastosowany dla klasy Database, aby zapewnić globalny punkt dostępu do danych oraz zagwarantować spójność informacji w całej aplikacji. Wzorzec Factory Method został wybrany do tworzenia różnych typów biletów, co umożliwia łatwe dodawanie nowych typów biletów bez modyfikacji istniejącego kodu.

Wzorzec Facade został zastosowany w klasie ReservationFacade, aby uprościć złożony proces rezerwacji i ukryć szczegóły implementacyjne przed warstwą prezentacji. Wzorzec Decorator umożliwia dynamiczne rozszerzanie funkcjonalności biletów o dodatkowe opcje (np. 3D, przekąski) bez modyfikacji klas bazowych. Wzorzec Observer został wybrany do monitorowania zmian stanu miejsc, co pozwala na automatyczną aktualizację interfejsu użytkownika. Wzorzec State zarządza stanami miejsc (wolne, zarezerwowane, sprzedane), eliminując potrzebę stosowania złożonych instrukcji warunkowych. Wzorzec Strategy umożliwia elastyczne definiowanie różnych strategii cenowych w zależności od kontekstu (np. ceny weekendowe).

### 2.3. Projektowanie architektury i struktury projektu

Zaprojektowano strukturę katalogów projektu, która odzwierciedla podział na warstwy logiczne oraz grupuje kod według odpowiedzialności. Struktura została zaprojektowana w sposób modularny, co sprzyja przejrzystości projektu oraz ułatwia nawigację po kodzie źródłowym. Główne katalogi projektu obejmują: katalog models zawierający klasy reprezentujące encje domenowe, katalog factories z implementacjami wzorca Factory Method, katalog builders z implementacją wzorca Builder, katalog utils zawierający narzędzia pomocnicze (baza danych, efekty wizualne), katalog facades z implementacją wzorca Facade, katalog decorators z implementacją wzorca Decorator, katalog observers z implementacją wzorca Observer, katalog states z implementacją wzorca State, katalog strategies z implementacją wzorca Strategy oraz katalog views zawierający komponenty interfejsu użytkownika.

Opracowano również diagram klas przedstawiający relacje między poszczególnymi komponentami systemu. Diagram uwzględnia zarówno relacje dziedziczenia (np. różne typy biletów dziedziczące po klasie bazowej Ticket), jak i relacje agregacji (np. Screening agregujący obiekty Movie, CinemaHall i listę Seat). Szczególną uwagę poświęcono zaprojektowaniu interfejsów komunikacji między warstwami, aby zapewnić luźne powiązanie komponentów oraz ułatwić testowanie i rozbudowę systemu.

### 2.4. Planowanie interfejsu użytkownika

W fazie planowania interfejsu użytkownika opracowano koncepcję wizualną aplikacji oraz określono sposób organizacji funkcjonalności. Zdecydowano się na zastosowanie interfejsu zakładkowego, który umożliwia logiczne grupowanie funkcjonalności oraz intuicyjną nawigację między różnymi obszarami systemu. Zaplanowano trzy główne zakładki: zakładkę "Filmy" do przeglądania repertuaru, zakładkę "Seanse" do wyboru seansu z kalendarza oraz zakładkę "Rezerwacje" do realizacji procesu rezerwacji.

W zakresie estetyki interfejsu zdecydowano się na nowoczesny design z wykorzystaniem gradientów, przezroczystości oraz zaokrąglonych rogów elementów. Zaplanowano zastosowanie spójnej palety kolorów opartej na odcieniach niebieskiego i szarego, co miało nadać aplikacji profesjonalny i elegancki wygląd. Szczególną uwagę poświęcono czytelności interfejsu oraz intuicyjności obsługi, aby użytkownik mógł bez problemu poruszać się po aplikacji i realizować swoje cele.

## 3. Część II – Wykonywanie projektu (implementacja)

### 3.1. Implementacja warstwy modeli danych

Implementację rozpoczęto od stworzenia podstawowych klas reprezentujących encje domenowe systemu. Klasa Movie została zaprojektowana jako prosta struktura danych przechowująca informacje o filmie: tytuł, czas trwania w minutach oraz kategorię wiekową. Klasa CinemaHall reprezentuje salę kinową i zawiera informacje o jej nazwie oraz wymiarach (liczba rzędów i miejsc w rzędzie).

Szczególną uwagę poświęcono klasie Seat, która reprezentuje pojedyncze miejsce w sali kinowej. W tej klasie zaimplementowano wzorzec State, umożliwiający zarządzanie stanem miejsca (wolne, zarezerwowane, sprzedane). Każdy stan został zdefiniowany jako osobna klasa (FreeSeatState, ReservedSeatState, SoldSeatState), co pozwala na łatwe rozszerzenie systemu o nowe stany oraz zapewnia spójność logiki biznesowej związanej ze zmianą stanów.

Klasa Screening agreguje obiekty Movie, CinemaHall oraz listę obiektów Seat, tworząc kompletną reprezentację seansu filmowego. W konstruktorze tej klasy następuje automatyczna inicjalizacja wszystkich miejsc w sali na podstawie jej wymiarów. Klasa Reservation przechowuje informacje o dokonanej rezerwacji, w tym referencję do seansu, listę zarezerwowanych miejsc oraz całkowitą cenę.

### 3.2. Implementacja wzorców kreacyjnych

W celu zapewnienia elastycznego tworzenia obiektów zaimplementowano trzy wzorce kreacyjne. Wzorzec Builder został zastosowany w klasie ScreeningBuilder, która umożliwia krokowe konstruowanie obiektów Screening. Dzięki metodom set_movie, set_cinema_hall, set_date_time oraz set_base_price możliwe jest stopniowe definiowanie parametrów seansu, a metoda build finalizuje proces tworzenia obiektu. Takie podejście zwiększa czytelność kodu oraz umożliwia tworzenie obiektów z różnymi konfiguracjami parametrów.

Wzorzec Singleton został zaimplementowany w klasie Database, która pełni rolę centralnego repozytorium danych aplikacji. Implementacja wzorca zapewnia, że w całym systemie istnieje tylko jedna instancja bazy danych, co gwarantuje spójność danych oraz eliminuje problemy związane z synchronizacją dostępu do współdzielonych zasobów. Klasa Database zarządza kolekcjami filmów, sal kinowych, seansów oraz rezerwacji, a także odpowiada za persystencję danych w formacie JSON.

Wzorzec Factory Method został zastosowany w klasie TicketFactory, która odpowiada za tworzenie różnych typów biletów (normalny, ulgowy, VIP). Metoda statyczna create_ticket przyjmuje typ biletu jako parametr i zwraca odpowiednią instancję klasy dziedziczącej po abstrakcyjnej klasie Ticket. Takie rozwiązanie centralizuje logikę tworzenia biletów oraz ułatwia dodawanie nowych typów biletów w przyszłości.

### 3.3. Implementacja wzorców strukturalnych

W warstwie logiki biznesowej zaimplementowano dwa wzorce strukturalne. Wzorzec Facade został zastosowany w klasie ReservationFacade, która stanowi uproszczony interfejs do złożonego procesu rezerwacji miejsc. Fasada ukrywa przed klientem szczegóły implementacyjne związane z weryfikacją dostępności miejsc, obliczaniem ceny oraz zapisem rezerwacji do bazy danych. Metoda reserve_seats przyjmuje obiekt seansu, listę miejsc oraz typ biletu, a następnie koordynuje działanie różnych komponentów systemu w celu realizacji rezerwacji.

Wzorzec Decorator został zaimplementowany w klasie TicketDecorator, która umożliwia dynamiczne rozszerzanie funkcjonalności biletów o dodatkowe opcje, takie jak projekcja 3D czy zestaw przekąsek. Każdy dekorator opakowuje obiekt biletu i modyfikuje jego cenę poprzez dodanie odpowiedniej opłaty. Możliwe jest łańcuchowe stosowanie dekoratorów, co pozwala na elastyczne komponowanie różnych kombinacji opcji dodatkowych.

### 3.4. Implementacja wzorców behawioralnych

W celu zapewnienia elastyczności w zakresie logiki biznesowej zaimplementowano trzy wzorce behawioralne. Wzorzec Observer został zastosowany w klasie SeatObserver, która monitoruje zmiany stanu miejsc w sali. Gdy miejsce zmienia swój stan (np. z wolnego na zarezerwowane), obserwator zostaje powiadomiony i może wykonać odpowiednie akcje, takie jak aktualizacja interfejsu użytkownika czy logowanie zdarzenia.

Wzorzec Strategy został zaimplementowany w module pricing_strategy, gdzie zdefiniowano różne strategie kalkulacji cen biletów. Klasa StandardPricingStrategy implementuje podstawową logikę cenową, podczas gdy WeekendPricingStrategy stosuje podwyższone ceny w weekendy. Strategia cenowa jest wybierana dynamicznie w zależności od kontekstu, co umożliwia łatwe dostosowanie polityki cenowej bez modyfikacji kodu klienta.

Wzorzec State, jak wspomniano wcześniej, został zaimplementowany w kontekście zarządzania stanami miejsc. Każdy stan definiuje dozwolone przejścia do innych stanów oraz zachowanie specyficzne dla danego stanu, co zapewnia spójność logiki biznesowej oraz eliminuje potrzebę stosowania złożonych instrukcji warunkowych.

### 3.5. Implementacja interfejsu użytkownika

Warstwa prezentacji została zrealizowana przy użyciu biblioteki PyQt5. Główne okno aplikacji (MainWindow) zawiera system zakładek umożliwiający przełączanie się między różnymi widokami: zarządzaniem filmami (MovieView), przeglądaniem seansów (ScreeningView) oraz zarządzaniem rezerwacjami (ReservationView).

Widok seansów umożliwia wybór daty z kalendarza oraz wyświetla listę seansów zaplanowanych na wybrany dzień. Po wybraniu konkretnego seansu użytkownik jest przenoszony do widoku rezerwacji, gdzie prezentowany jest plan sali z wizualizacją dostępności poszczególnych miejsc. Miejsca wolne, zarezerwowane i sprzedane są oznaczone różnymi kolorami, co ułatwia orientację w dostępności miejsc.

Proces rezerwacji obejmuje wybór miejsc poprzez kliknięcie na odpowiednie przyciski reprezentujące miejsca, wybór typu biletu oraz opcjonalnie dodanie opcji dodatkowych poprzez zastosowanie dekoratorów. System automatycznie oblicza całkowitą cenę rezerwacji i prezentuje ją użytkownikowi przed potwierdzeniem. Po zatwierdzeniu rezerwacji dane są zapisywane do pliku JSON, co zapewnia persystencję danych między sesjami aplikacji.

### 3.6. Implementacja persystencji danych

W celu zapewnienia trwałości danych między sesjami aplikacji zaimplementowano mechanizm persystencji oparty na formacie JSON. Klasa Database została rozszerzona o metody save_reservations oraz load_reservations, które odpowiadają za serializację i deserializację obiektów rezerwacji. Metoda save_reservations konwertuje listę obiektów Reservation na listę słowników przy użyciu metody to_dict, a następnie zapisuje dane do pliku JSON z odpowiednim formatowaniem (wcięcia dla czytelności).

Metoda load_reservations odczytuje dane z pliku JSON i rekonstruuje obiekty Reservation przy użyciu metody from_dict. Proces deserializacji jest bardziej złożony, ponieważ wymaga odtworzenia powiązań między rezerwacją a seansem oraz miejscami. W tym celu metoda from_dict przyjmuje referencję do obiektu Database, co umożliwia wyszukanie odpowiedniego seansu na podstawie zapisanych identyfikatorów (tytuł filmu, nazwa sali, data i czas). Po znalezieniu seansu, metoda odtwarza listę zarezerwowanych miejsc poprzez wyszukanie odpowiednich obiektów Seat w liście miejsc seansu.

Zaimplementowano również mechanizm automatycznego zapisu rezerwacji po każdej operacji dodania nowej rezerwacji do bazy danych. Metoda add_reservation w klasie Database automatycznie wywołuje save_reservations, co zapewnia, że dane są zawsze aktualne w pliku JSON. Przy starcie aplikacji, w funkcji main, następuje automatyczne wczytanie rezerwacji z pliku, co przywraca stan systemu z poprzedniej sesji. Zastosowano również obsługę błędów dla operacji wejścia/wyjścia, aby aplikacja mogła gracefully obsłużyć sytuacje, gdy plik nie istnieje lub jest uszkodzony.

### 3.7. Integracja komponentów i przepływ danych

Po zaimplementowaniu poszczególnych komponentów systemu przystąpiono do ich integracji oraz zapewnienia prawidłowego przepływu danych między warstwami. Kluczowym elementem integracji było połączenie warstwy prezentacji (widoki PyQt5) z warstwą logiki biznesowej (fasada, fabryki, wzorce) oraz warstwą danych (baza danych Singleton).

W widoku seansów (ScreeningView) zaimplementowano mechanizm sygnałów i slotów PyQt5, który umożliwia komunikację między komponentami interfejsu użytkownika. Po wybraniu seansu przez użytkownika, widok emituje sygnał screening_selected, który jest przechwytywany przez główne okno aplikacji (MainWindow). Główne okno następnie przekazuje wybrany seans do widoku rezerwacji (ReservationView) poprzez wywołanie metody set_screening, a także automatycznie przełącza aktywną zakładkę na zakładkę rezerwacji.

W widoku rezerwacji zaimplementowano logikę obsługi wyboru miejsc przez użytkownika. Każde miejsce jest reprezentowane przez przycisk, którego stan wizualny (kolor, możliwość kliknięcia) jest aktualizowany w zależności od stanu miejsca (wolne, zarezerwowane, sprzedane). Po wybraniu miejsc i typu biletu, widok wykorzystuje ReservationFacade do obliczenia ceny oraz finalizacji rezerwacji. Fasada koordynuje działanie różnych komponentów: wykorzystuje odpowiednią fabrykę biletów do utworzenia obiektów Ticket, aktualizuje stany miejsc przy użyciu wzorca State oraz zapisuje rezerwację do bazy danych.

### 3.8. Testowanie i debugowanie

W fazie testowania przeprowadzono weryfikację poprawności działania wszystkich funkcjonalności systemu. Testowanie obejmowało zarówno testy manualne interfejsu użytkownika, jak i weryfikację poprawności implementacji wzorców projektowych oraz logiki biznesowej. Przetestowano proces dodawania filmów do repertuaru, tworzenia seansów przy użyciu wzorca Builder, rezerwacji miejsc z różnymi typami biletów oraz zapisywania i wczytywania danych z pliku JSON.

W trakcie testowania zidentyfikowano i naprawiono kilka błędów. Jednym z problemów była nieprawidłowa aktualizacja stanu miejsc po wczytaniu rezerwacji z pliku – miejsca zarezerwowane w poprzedniej sesji nie były prawidłowo oznaczane jako zajęte. Problem został rozwiązany poprzez dodanie logiki aktualizacji stanów miejsc w metodzie load_reservations. Innym problemem była nieprawidłowa kalkulacja ceny przy stosowaniu dekoratorów biletów – rozwiązano to poprzez poprawną implementację metody get_price w klasach dekoratorów.

Przeprowadzono również testy wydajnościowe, weryfikując czas ładowania danych oraz responsywność interfejsu użytkownika przy dużej liczbie seansów i rezerwacji. Zoptymalizowano kod w kilku miejscach, m.in. poprzez zastosowanie list comprehension zamiast pętli for w metodach filtrujących dane. Kod został również poddany refaktoryzacji w celu poprawy czytelności oraz eliminacji duplikacji.

### 3.9. Dokumentacja i finalizacja projektu

W fazie testowania przeprowadzono weryfikację poprawności działania wszystkich funkcjonalności systemu. Przetestowano proces dodawania filmów, tworzenia seansów, rezerwacji miejsc oraz zapisywania i wczytywania danych z pliku JSON. Zidentyfikowane błędy zostały naprawione, a kod został zoptymalizowany pod kątem wydajności i czytelności.

Przygotowano kompleksową dokumentację projektu, która obejmuje kilka kluczowych elementów. Plik README.md zawiera szczegółowy opis funkcjonalności systemu, listę zaimplementowanych wzorców projektowych wraz z fragmentami kodu ilustrującymi ich zastosowanie, strukturę katalogów projektu oraz instrukcję uruchomienia aplikacji. Dokumentacja została napisana w sposób przystępny zarówno dla osób technicznych, jak i nietechnicznych, co ułatwia zrozumienie celów i możliwości systemu.

W kodzie źródłowym zastosowano szczegółowe komentarze wyjaśniające działanie poszczególnych metod oraz klas. Komentarze zostały napisane w języku polskim, co ułatwia zrozumienie kodu przez polskojęzycznych programistów. Każda klasa oraz metoda została opatrzona docstringiem wyjaśniającym jej przeznaczenie oraz sposób użycia. W miejscach, gdzie zastosowano wzorce projektowe, dodano komentarze wskazujące na konkretny wzorzec oraz wyjaśniające, dlaczego został on zastosowany w danym kontekście.

Przygotowano również diagram klas w formacie Markdown, który wizualizuje strukturę systemu oraz relacje między poszczególnymi komponentami. Diagram został wyrenderowany do formatu graficznego (JPEG), co ułatwia jego przeglądanie i prezentację. W ramach finalizacji projektu przeprowadzono również przegląd kodu (code review), weryfikując zgodność implementacji z założeniami projektowymi oraz sprawdzając jakość kodu pod kątem czytelności, modularności oraz zgodności z dobrymi praktykami programowania obiektowego.

## 4. Podsumowanie i wnioski

Projekt WSBCinema został zrealizowany zgodnie z założeniami, implementując wszystkie zaplanowane funkcjonalności oraz wzorce projektowe. Proces realizacji projektu przebiegał w sposób uporządkowany, od fazy analizy i planowania, przez implementację poszczególnych warstw systemu, aż po testowanie i dokumentację. Zastosowanie paradygmatu programowania obiektowego oraz ośmiu klasycznych wzorców projektowych (Builder, Singleton, Factory Method, Facade, Decorator, Observer, State, Strategy) zaowocowało stworzeniem aplikacji o wysokiej jakości kodu, która charakteryzuje się modularnością, skalowalnością oraz łatwością w utrzymaniu.

Realizacja projektu pozwoliła na praktyczne zastosowanie wiedzy teoretycznej z zakresu inżynierii oprogramowania oraz pogłębienie umiejętności programistycznych w języku Python. Szczególnie wartościowe okazało się praktyczne zastosowanie wzorców projektowych w rzeczywistym projekcie, co pozwoliło na zrozumienie ich zalet oraz kontekstów, w których przynoszą one największe korzyści. Implementacja interfejsu użytkownika przy użyciu biblioteki PyQt5 umożliwiła poznanie technik tworzenia aplikacji desktopowych z graficznym interfejsem użytkownika.

System stanowi solidną podstawę do ewentualnego rozszerzenia o dodatkowe funkcjonalności. Modularna architektura oraz zastosowanie wzorców projektowych ułatwiają dodawanie nowych funkcji bez konieczności modyfikacji istniejącego kodu. Potencjalne kierunki rozwoju systemu obejmują: integrację z systemami płatności online, implementację systemu zarządzania użytkownikami z różnymi poziomami uprawnień, dodanie funkcjonalności generowania raportów statystycznych dotyczących sprzedaży biletów, implementację systemu powiadomień e-mail lub SMS, rozszerzenie systemu o obsługę promocji i kodów rabatowych oraz integrację z zewnętrznymi bazami danych filmowych (np. TMDB API) w celu automatycznego pobierania informacji o filmach.

Podsumowując, projekt WSBCinema stanowi udaną implementację systemu rezerwacji biletów kinowych, która łączy funkcjonalność, estetykę oraz wysoką jakość kodu. Realizacja projektu dostarczyła cennych doświadczeń w zakresie projektowania i implementacji aplikacji obiektowych oraz praktycznego zastosowania wzorców projektowych w kontekście rzeczywistego problemu biznesowego.
