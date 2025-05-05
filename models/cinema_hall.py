class CinemaHall:
    """Klasa reprezentująca salę kinową w WSBCinema."""
    
    def __init__(self, name, rows, seats_per_row):
        """
        Inicjalizacja obiektu sali kinowej.
        Konstruktor klasy CinemaHall przyjmuje nazwę sali, liczbę rzędów oraz liczbę miejsc w każdym rzędzie.
        """
        self.name = name  # Przypisuję podaną nazwę do atrybutu 'name' obiektu.
        self.rows = rows  # Przypisuję podaną liczbę rzędów do atrybutu 'rows'.
        self.seats_per_row = seats_per_row  # Przypisuję podaną liczbę miejsc w rzędzie do atrybutu 'seats_per_row'.
    
    def get_total_seats(self):
        """
        Metoda obliczająca całkowitą liczbę miejsc w sali.
        Ta metoda zwraca iloczyn liczby rzędów i miejsc w rzędzie, co daje łączną liczbę miejsc.
        """
        return self.rows * self.seats_per_row  # Obliczam i zwracam całkowitą liczbę miejsc.
    
    def __str__(self):
        """
        Metoda zwracająca tekstową reprezentację obiektu sali kinowej.
        Ta metoda jest wywoływana, gdy próbujemy przedstawić obiekt CinemaHall jako string.
        """
        # Zwracam sformatowany string zawierający nazwę sali oraz jej wymiary (rzędy x miejsca).
        return f"{self.name} ({self.rows}x{self.seats_per_row})"