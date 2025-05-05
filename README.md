# System Rezerwacji Biletów Kinowych - WSBCinema

## Opis projektu

System rezerwacji biletów kinowych WSBCinema to aplikacja desktopowa symulująca podstawowe funkcjonalności systemu rezerwacji miejsc w kinie. Projekt został zrealizowany z zastosowaniem zasad programowania obiektowego oraz wybranych wzorców projektowych w celu stworzenia elastycznego, rozszerzalnego i łatwego w utrzymaniu kodu. Aplikacja posiada graficzny interfejs użytkownika (GUI) z nowoczesnym efektem glassmorphism.

## Zaimplementowane funkcjonalności

1.  **Zarządzanie repertuarem:**
    *   Możliwość dodawania/definiowania filmów (tytuł, czas trwania, kategoria wiekowa).
    *   Możliwość definiowania sal kinowych (numer/nazwa, liczba miejsc w rzędach) - dane sal są predefiniowane w kodzie.
    *   Możliwość tworzenia seansów (przypisanie filmu do sali w określonym terminie) - seanse są generowane przykładowo przy starcie aplikacji.
2.  **Proces rezerwacji:**
    *   Możliwość wyświetlenia listy seansów w danym dniu (wybór daty z kalendarza).
    *   Możliwość wybrania konkretnego seansu i wyświetlenia planu sali z zaznaczonymi wolnymi i zajętymi miejscami.
    *   Możliwość wyboru jednego lub więcej wolnych miejsc do rezerwacji.
    *   Obliczanie ceny rezerwacji w oparciu o liczbę i typ biletów (normalny, ulgowy, VIP) z możliwością dekorowania biletów (np. opcja 3D, zestaw przekąsek).
    *   Potwierdzenie rezerwacji (zapis rezerwacji do pliku JSON).
3.  **Interfejs użytkownika:**
    *   Graficzny interfejs użytkownika (GUI) zrealizowany przy użyciu biblioteki PyQt5.
    *   Nowoczesny wygląd z efektem glassmorphism i prostymi animacjami.
    *   Podział na zakładki: "Filmy" (zarządzanie filmami), "Seanse" (przeglądanie i wybór seansów), "Rezerwacje" (dokonywanie rezerwacji).

## Zastosowane wzorce projektowe

W projekcie świadomie zastosowano następujące wzorce projektowe, aby poprawić strukturę i elastyczność kodu:

*   **Factory Method (Metoda Wytwórcza):** Zastosowany w `factories/ticket_factory.py` do tworzenia różnych typów biletów (normalny, ulgowy, VIP). Pozwala to na łatwe dodawanie nowych rodzajów biletów bez modyfikacji kodu korzystającego z fabryk.
*   **Builder (Budowniczy):** Wykorzystany w `builders/screening_builder.py` do konstruowania złożonych obiektów seansów. Umożliwia tworzenie instancji klasy `Screening` krok po kroku, co jest czytelne i ułatwia zarządzanie wieloma parametrami konstruktora.
*   **Singleton:** Zaimplementowany w `utils/database.py` do zarządzania centralnym repozytorium danych (filmów, sal, seansów, rezerwacji). Zapewnia, że w całej aplikacji istnieje tylko jedna instancja bazy danych, co gwarantuje spójność danych.
*   **Facade (Fasada):** Zastosowany w `facades/reservation_facade.py` do uproszczenia interfejsu złożonego podsystemu rezerwacji. Ukrywa szczegóły operacji takich jak sprawdzanie dostępności miejsc, obliczanie cen czy tworzenie rezerwacji, prezentując prostszy interfejs dla klienta fasady (np. widoków GUI).
*   **Decorator (Dekorator):** Wykorzystany w `decorators/ticket_decorator.py` do dynamicznego dodawania funkcjonalności i modyfikowania ceny biletów (np. opcja 3D, zestaw przekąsek). Pozwala na rozszerzanie funkcjonalności biletów w sposób elastyczny, bez modyfikacji ich podstawowych klas.
*   **Observer (Obserwator):** Zastosowany w `observers/seat_observer.py` i `models/seat.py` do powiadamiania o zmianach stanu miejsc (np. zarezerwowanie, sprzedanie). Umożliwia automatyczną aktualizację widoku sali w GUI po zmianie stanu miejsca.
*   **State (Stan):** Zaimplementowany w `states/seat_state.py` i `models/seat.py` do zarządzania stanem miejsca (wolne, zarezerwowane, sprzedane). Upraszcza logikę związaną ze zmianami stanów i zachowaniem miejsca w różnych kontekstach.
*   **Strategy (Strategia):** Zastosowany w `strategies/pricing_strategy.py` do implementacji różnych strategii cenowych (standardowa, weekendowa, poranna). Pozwala na elastyczne obliczanie cen biletów w zależności od różnych czynników, bez konieczności zmiany kodu kontekstu (np. metody obliczającej cenę w fasadzie).

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
    ├── movie_view.py
    ├── screening_view.py
    └── reservation_view.py
```

Uproszczony diagram klas znajduje się w pliku `dokumentacja/diagram.md`.

## Sposób uruchomienia aplikacji

1.  Upewnij się, że masz zainstalowany Python w wersji 3.x.
2.  Zainstaluj bibliotekę PyQt5, wykonując w terminalu komendę:
    ```bash
    pip install PyQt5
    ```
3.  Pobierz kod źródłowy projektu i zachowaj strukturę katalogów przedstawioną powyżej.
4.  Przejdź do głównego katalogu projektu w terminalu.
5.  Uruchom aplikację, wykonując komendę:
    ```bash
    python main.py
    ```
    Aplikacja GUI powinna się uruchomić, prezentując główne okno z zakładkami. Przykładowe filmy i seanse zostaną załadowane przy starcie. Rezerwacje będą zapisywane do pliku `reservations.json` w głównym katalogu projektu i wczytywane przy ponownym uruchomieniu.

## Przykładowe filmy (zdobywcy Oscarów)

W systemie WSBCinema jako przykładowy repertuar zaimplementowano filmy, które zostały nagrodzone Oscarem dla najlepszego filmu:

*   Oppenheimer (Oscar 2024)
*   Everything Everywhere All at Once (Oscar 2023)
*   CODA (Oscar 2022)
*   Nomadland (Oscar 2021)
*   Parasite (Oscar 2020)
*   Anora (Oscar 2025 - hipotetycznie)# WSBCinema
