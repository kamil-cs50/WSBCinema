# Plan działania - System Rezerwacji Biletów Kinowych WSBCinema

Poniżej przedstawiam szczegółowy plan działania dotyczący stworzenia systemu rezerwacji biletów kinowych WSBCinema, bazując na dostarczonym pliku `rozwiazanie.md` oraz dodatkowych wytycznych.

**Cel:** Stworzenie kompletnego systemu rezerwacji biletów kinowych z GUI, zgodnego z zasadami programowania obiektowego i wykorzystującego wskazane wzorce projektowe.

**Kroki do wykonania:**

1.  **Stworzenie struktury katalogów:** Utworzenie niezbędnych katalogów (`models`, `factories`, `builders`, `utils`, `facades`, `decorators`, `observers`, `states`, `strategies`, `views`, `dokumentacja`) w głównym katalogu projektu.
2.  **Utworzenie i uzupełnienie plików kodu:**
    *   Utworzenie wszystkich plików `.py` wymienionych w `rozwiazanie.md`:
        *   `main.py`
        *   `models/movie.py`
        *   `models/cinema_hall.py`
        *   `models/seat.py`
        *   `models/screening.py`
        *   `models/ticket.py`
        *   `models/reservation.py`
        *   `factories/ticket_factory.py`
        *   `builders/screening_builder.py`
        *   `utils/database.py`
        *   `utils/glass_morphism.py`
        *   `facades/reservation_facade.py`
        *   `decorators/ticket_decorator.py`
        *   `observers/seat_observer.py`
        *   `states/seat_state.py`
        *   `strategies/pricing_strategy.py`
        *   `views/main_window.py`
    *   Uzupełnienie tych plików kodem z `rozwiazanie.md`, dodając do każdej linii komentarze w języku polskim, w stylu opisanym w zadaniu (tłumaczenie dla wykładowcy, zwięzłe).
    *   **Implementacja widoków GUI:** Stworzenie brakujących plików widoków w katalogu `views`:
        *   `views/movie_view.py` - Implementacja GUI do zarządzania filmami (wyświetlanie listy, dodawanie).
        *   `views/screening_view.py` - Implementacja GUI do zarządzania seansami (wyświetlanie listy, dodawanie, wybór seansu).
        *   `views/reservation_view.py` - Implementacja GUI do procesu rezerwacji (wyświetlanie planu sali, wybór miejsc, potwierdzenie rezerwacji, wyświetlanie rezerwacji).
    *   **Implementacja animacji Glassmorphism:** Uzupełnienie metod `_start_shine_animation`, `_stop_shine_animation`, `_start_move_animation`, `_stop_move_animation` w pliku `utils/glass_morphism.py` w celu dodania dynamicznych animacji.
    *   **Zapis i odczyt rezerwacji:** Modyfikacja klasy `Database` lub dodanie osobnej logiki do zapisywania listy rezerwacji do pliku w formacie JSON oraz wczytywania ich przy starcie aplikacji.
3.  **Wzorce projektowe:** Potwierdzenie zastosowania i opis wzorców: Factory Method, Builder, Singleton, Facade, Decorator, Observer, State, Strategy. Uzasadnienie ich wyboru zostanie zawarte w dokumentacji.
4.  **Przykładowe dane:** Dodanie filmów nagrodzonych Oscarem jako przykładowego repertuaru w funkcji ładowania danych.
5.  **Interfejs graficzny:** Dopracowanie stylów i układu GUI z efektem glassmorphism przy użyciu biblioteki PyQt5.
6.  **Dokumentacja (README.md):** Utworzenie pliku `README.md` w głównym katalogu projektu zawierającego:
    *   Opis projektu "System Rezerwacji Biletów Kinowych - WSBCinema".
    *   Listę zaimplementowanych funkcjonalności.
    *   Opis zastosowanych wzorców projektowych wraz z uzasadnieniem.
    *   Uproszczony diagram klas (odwołanie do pliku `dokumentacja/diagram.md`).
    *   Instrukcję uruchomienia aplikacji.
7.  **Diagram klas:** Zapisanie diagramu klas w formacie Mermaid do pliku `dokumentacja/diagram.md`.

**Diagram Klas (Mermaid):**

[Diagram zostanie zapisany w oddzielnym pliku zgodnie z prośbą użytkownika.]

Po pomyślnym wykonaniu tych kroków, system rezerwacji biletów kinowych WSBCinema będzie gotowy, spełniając wszystkie określone wymagania.