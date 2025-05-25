from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QMessageBox, QSpinBox # Import niezbędnych klas z modułu QtWidgets do tworzenia elementów GUI, takich jak widget bazowy (QWidget), układy (QVBoxLayout, QHBoxLayout), etykiety (QLabel), pola tekstowe (QLineEdit), przyciski (QPushButton), listy (QListWidget), okna dialogowe (QMessageBox) i pola numeryczne (QSpinBox).
from utils.database import Database # Import klasy Database z modułu utils, która służy jako repozytorium danych dla aplikacji (filmy, seanse, rezerwacje). Implementacja wzorca Singleton.
from models.movie import Movie # Import klasy Movie z modułu models, która reprezentuje obiekt filmu w systemie.

class MovieView(QWidget): # Deklaracja klasy MovieView, dziedziczącej po QWidget, co oznacza, że jest to niestandardowy widget GUI.
    """
    Widok do zarządzania filmami.
    Umożliwia wyświetlanie listy filmów i dodawanie nowych filmów do systemu.
    """
    
    def __init__(self): # Konstruktor klasy MovieView.
        """
        Inicjalizacja widoku filmów.
        Konfigurowanie układu i tworzenie elementów GUI dla tej zakładki.
        """
        super().__init__() # Wywołanie konstruktora klasy nadrzędnej QWidget.
        
        self.database = Database() # Pobieranie instancji bazy danych (Singleton).
        self.layout = QVBoxLayout(self) # Tworzenie głównego pionowego układu (QVBoxLayout) dla tego widoku i ustawianie go jako layout dla bieżącego widgetu (self).
        
        self.setup_add_movie_section() # Konfigurowanie sekcji GUI do dodawania nowych filmów.
        self.setup_movie_list_section() # Konfigurowanie sekcji GUI do wyświetlania listy filmów.
        
        self.load_movies() # Wczytywanie filmów z bazy danych i wyświetlanie ich na liście w GUI przy starcie widoku.

    def setup_add_movie_section(self): # Metoda konfiguruje część interfejsu użytkownika służącą do dodawania nowych filmów.
        """
        Konfigurowanie sekcji GUI do dodawania nowego filmu.
        Zawiera pola tekstowe na tytuł, czas trwania, kategorię wiekową i przycisk "Dodaj film".
        """
        add_movie_layout = QHBoxLayout() # Tworzenie poziomego układu (QHBoxLayout) dla elementów sekcji dodawania filmu.
        
        self.title_input = QLineEdit() # Tworzenie pola tekstowego do wprowadzania tytułu filmu.
        self.title_input.setPlaceholderText("Tytuł filmu")
        add_movie_layout.addWidget(self.title_input)
        
        self.duration_input = QSpinBox() # Tworzenie pola numerycznego do wprowadzania czasu trwania filmu.
        self.duration_input.setMinimum(1)
        self.duration_input.setMaximum(500)
        self.duration_input.setSuffix(" min")
        add_movie_layout.addWidget(self.duration_input) # Dodawanie pola numerycznego na czas trwania do poziomego układu sekcji dodawania filmu.
        
        self.age_category_input = QSpinBox() # Tworzenie pola numerycznego do wprowadzania kategorii wiekowej.
        self.age_category_input.setMinimum(0)
        self.age_category_input.setMaximum(21)
        self.age_category_input.setPrefix("+")
        add_movie_layout.addWidget(self.age_category_input) # Dodawanie pola numerycznego na kategorię wiekową do poziomego układu sekcji dodawania filmu.
        
        add_movie_button = QPushButton("Dodaj film") # Tworzenie przycisku "Dodaj film".
        add_movie_button.clicked.connect(self.add_movie) # Podpinanie sygnału 'clicked' do metody self.add_movie.
        add_movie_layout.addWidget(add_movie_button)
        
        self.layout.addLayout(add_movie_layout) # Dodawanie poziomego układu sekcji dodawania filmu do głównego pionowego układu widoku.

    def setup_movie_list_section(self): # Metoda konfiguruje część interfejsu użytkownika służącą do wyświetlania listy filmów.
        """
        Konfigurowanie sekcji GUI do wyświetlania listy filmów.
        Zawiera etykietę "Lista filmów" i widget listy (QListWidget).
        """
        movie_list_label = QLabel("Lista filmów:") # Tworzenie etykiety z tekstem "Lista filmów:".
        self.layout.addWidget(movie_list_label)
        
        self.movie_list_widget = QListWidget() # Tworzenie widgetu listy do wyświetlania filmów.
        self.layout.addWidget(self.movie_list_widget)

    def load_movies(self): # Metoda wczytuje filmy z bazy danych i wyświetla je w QListWidget.
        """
        Wczytywanie filmów z bazy danych i wypełnianie QListWidget.
        """
        self.movie_list_widget.clear() # Czyszczenie zawartości QListWidget.
        movies = self.database.get_movies() # Pobieranie listy wszystkich filmów z bazy danych.
        for movie in movies:
            self.movie_list_widget.addItem(str(movie)) # Dodawanie tekstowej reprezentacji filmu do QListWidget.

    def add_movie(self): # Metoda wywoływana po kliknięciu przycisku "Dodaj film".
        """
        Dodawanie nowego filmu do bazy danych na podstawie danych wprowadzonych w polach tekstowych.
        """
        title = self.title_input.text() # Pobieranie aktualnego tekstu z pola tekstowego tytułu.
        duration = self.duration_input.value()
        age_category = self.age_category_input.value()
        
        if not title:
            QMessageBox.warning(self, "Błąd", "Tytuł filmu nie może być pusty.") # Wyświetlanie okna dialogowego z komunikatem ostrzegawczym.
            return
        
        new_movie = Movie(title, duration, age_category) # Tworzenie nowej instancji klasy Movie na podstawie wprowadzonych danych.
        self.database.add_movie(new_movie)
        
        QMessageBox.information(self, "Sukces", f"Dodano film: {new_movie}") # Wyświetlanie okna dialogowego z komunikatem informacyjnym o dodaniu filmu.
        
        self.load_movies() # Odświeżanie listy filmów po dodaniu nowego filmu.
        
        # Czyszczenie pól wprowadzania danych po dodaniu filmu.
        self.title_input.clear() # Czyszczenie zawartości pola tekstowego tytułu.
        self.duration_input.setValue(1)
        self.age_category_input.setValue(0)