class Movie:
    """Klasa reprezentująca film w kinie WSBCinema."""
    
    def __init__(self, title, duration_minutes, age_category):
        """
        Inicjalizacja obiektu filmu.
        Konstruktor klasy Movie przyjmuje trzy argumenty: tytuł filmu, czas trwania w minutach oraz wymaganą kategorię wiekową.
        """
        self.title = title  # Przypisuję podany tytuł do atrybutu 'title' obiektu.
        self.duration_minutes = duration_minutes  # Przypisuję podany czas trwania do atrybutu 'duration_minutes'.
        self.age_category = age_category  # Przypisuję podaną kategorię wiekową do atrybutu 'age_category'.
    
    def __str__(self):
        """
        Metoda zwracająca tekstową reprezentację obiektu filmu.
        Ta metoda jest wywoływana, gdy próbujemy przedstawić obiekt Movie jako string, np. podczas drukowania.
        """
        # Zwracam sformatowany string zawierający tytuł, czas trwania i kategorię wiekową filmu.
        return f"{self.title} ({self.duration_minutes} min, {self.age_category}+)"