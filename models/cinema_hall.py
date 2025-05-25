class CinemaHall:
    """Klasa reprezentująca salę kinową w WSBCinema."""
    
    def __init__(self, name, rows, seats_per_row):
        """
        Inicjalizacja obiektu sali kinowej.
        Konstruktor klasy CinemaHall przyjmuje nazwę sali, liczbę rzędów oraz liczbę miejsc w każdym rzędzie.
        """
        self.name = name  # Przypisywanie podanej nazwy do atrybutu 'name' obiektu.
        self.rows = rows  # Przypisywanie podanej liczby rzędów do atrybutu 'rows'.
        self.seats_per_row = seats_per_row  # Przypisywanie podanej liczby miejsc w rzędzie do atrybutu 'seats_per_row'.

    def get_total_seats(self):
        """
        Metoda obliczająca całkowitą liczbę miejsc w sali.
        Ta metoda zwraca iloczyn liczby rzędów i miejsc w rzędzie, co daje łączną liczbę miejsc.
        """
        return self.rows * self.seats_per_row  # Obliczanie i zwracanie całkowitej liczby miejsc.

    def __str__(self):
        """
        Metoda zwracająca tekstową reprezentację obiektu sali kinowej.
        Ta metoda jest wywoływana, gdy próbujemy przedstawić obiekt CinemaHall jako string.
        """
        # Zwracanie sformatowanego stringa zawierającego nazwę sali oraz jej wymiary (rzędy x miejsca).
        return f"{self.name} ({self.rows}x{self.seats_per_row})"