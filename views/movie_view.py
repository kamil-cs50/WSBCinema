from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QMessageBox, QSpinBox # Importuję niezbędne klasy z modułu QtWidgets do tworzenia elementów GUI, takich jak widget bazowy (QWidget), układy (QVBoxLayout, QHBoxLayout), etykiety (QLabel), pola tekstowe (QLineEdit), przyciski (QPushButton), listy (QListWidget), okna dialogowe (QMessageBox) i pola numeryczne (QSpinBox).
from utils.database import Database # Importuję klasę Database z modułu utils, która służy jako repozytorium danych dla aplikacji (filmy, seanse, rezerwacje). Jest to implementacja wzorca Singleton.
from models.movie import Movie # Importuję klasę Movie z modułu models, która reprezentuje obiekt filmu w systemie.

class MovieView(QWidget): # Deklaruję klasę MovieView, która dziedziczy po QWidget, co oznacza, że jest to niestandardowy widget GUI.
    """
    Widok do zarządzania filmami. # Docstring opisujący przeznaczenie klasy MovieView.
    Umożliwia wyświetlanie listy filmów i dodawanie nowych filmów do systemu. # Rozszerzenie opisu funkcjonalności widoku filmów.
    """
    
    def __init__(self): # Definiuję metodę __init__, która jest konstruktorem klasy MovieView. Jest wywoływana podczas tworzenia instancji tej klasy.
        """
        Inicjalizacja widoku filmów. # Docstring opisujący konstruktor.
        Konfiguruje układ i tworzy elementy GUI dla tej zakładki. # Opisuje działania wykonywane w konstruktorze.
        """
        super().__init__() # Wywołuję konstruktor klasy nadrzędnej QWidget. Jest to konieczne do poprawnej inicjalizacji widgetu PyQt5.
        
        self.database = Database() # Pobieram instancję bazy danych (Singleton) poprzez wywołanie klasy Database(). Dzięki wzorcowi Singleton, zawsze otrzymuję tę samą instancję bazy danych.
        self.layout = QVBoxLayout(self) # Tworzę główny pionowy układ (QVBoxLayout) dla tego widoku i ustawiam go jako layout dla bieżącego widgetu (self), czyli MovieView. Elementy dodane do tego layoutu będą układane pionowo.
        
        self.setup_add_movie_section() # Wywołuję metodę setup_add_movie_section, odpowiedzialną za konfigurację sekcji GUI do dodawania nowych filmów.
        self.setup_movie_list_section() # Wywołuję metodę setup_movie_list_section, odpowiedzialną za konfigurację sekcji GUI do wyświetlania listy filmów.
        
        self.load_movies() # Wywołuję metodę load_movies, która wczytuje filmy z bazy danych i wyświetla je na liście w GUI przy starcie widoku.

    def setup_add_movie_section(self): # Definiuję metodę setup_add_movie_section, która konfiguruje część interfejsu użytkownika służącą do dodawania nowych filmów.
        """
        Konfiguruje sekcję GUI do dodawania nowego filmu. # Docstring opisujący metodę.
        Zawiera pola tekstowe na tytuł, czas trwania, kategorię wiekową i przycisk "Dodaj film". # Opisuje elementy GUI tworzone w tej sekcji.
        """
        add_movie_layout = QHBoxLayout() # Tworzę poziomy układ (QHBoxLayout) dla elementów sekcji dodawania filmu. Elementy dodane do tego layoutu będą układane poziomo.
        
        self.title_input = QLineEdit() # Tworzę instancję QLineEdit (pole tekstowe) do wprowadzania tytułu filmu i przypisuję ją do atrybutu self.title_input.
        self.title_input.setPlaceholderText("Tytuł filmu") # Ustawiam tekst placeholder w polu tytułu, który znika po rozpoczęciu wprowadzania tekstu.
        add_movie_layout.addWidget(self.title_input) # Dodaję utworzone pole tekstowe na tytuł do poziomego układu sekcji dodawania filmu.
        
        self.duration_input = QSpinBox() # Tworzę instancję QSpinBox (pole do wprowadzania liczby) do wprowadzania czasu trwania filmu i przypisuję ją do atrybutu self.duration_input.
        self.duration_input.setMinimum(1) # Ustawiam minimalną akceptowalną wartość w polu czasu trwania na 1.
        self.duration_input.setMaximum(500) # Ustawiam maksymalną akceptowalną wartość w polu czasu trwania na 500 (minut).
        self.duration_input.setSuffix(" min") # Dodaję sufiks " min" do wartości wyświetlanej w polu czasu trwania.
        add_movie_layout.addWidget(self.duration_input) # Dodaję utworzone pole numeryczne na czas trwania do poziomego układu sekcji dodawania filmu.
        
        self.age_category_input = QSpinBox() # Tworzę instancję QSpinBox do wprowadzania kategorii wiekowej i przypisuję ją do atrybutu self.age_category_input.
        self.age_category_input.setMinimum(0) # Ustawiam minimalną akceptowalną wartość kategorii wiekowej na 0 (brak ograniczeń).
        self.age_category_input.setMaximum(21) # Ustawiam maksymalną akceptowalną wartość kategorii wiekowej na 21.
        self.age_category_input.setPrefix("+") # Dodaję prefiks "+" do wartości wyświetlanej w polu kategorii wiekowej.
        add_movie_layout.addWidget(self.age_category_input) # Dodaję utworzone pole numeryczne na kategorię wiekową do poziomego układu sekcji dodawania filmu.
        
        add_movie_button = QPushButton("Dodaj film") # Tworzę instancję QPushButton (przycisk) z tekstem "Dodaj film".
        add_movie_button.clicked.connect(self.add_movie) # Podpinam sygnał 'clicked' (kliknięcie przycisku) do metody self.add_movie. Oznacza to, że metoda add_movie zostanie wywołana, gdy przycisk zostanie kliknięty.
        add_movie_layout.addWidget(add_movie_button) # Dodaję utworzony przycisk do poziomego układu sekcji dodawania filmu.
        
        self.layout.addLayout(add_movie_layout) # Dodaję poziomy układ sekcji dodawania filmu (add_movie_layout) do głównego pionowego układu widoku (self.layout).

    def setup_movie_list_section(self): # Definiuję metodę setup_movie_list_section, która konfiguruje część interfejsu użytkownika służącą do wyświetlania listy filmów.
        """
        Konfiguruje sekcję GUI do wyświetlania listy filmów. # Docstring opisujący metodę.
        Zawiera etykietę "Lista filmów" i widget listy (QListWidget). # Opisuje elementy GUI tworzone w tej sekcji.
        """
        movie_list_label = QLabel("Lista filmów:") # Tworzę instancję QLabel (etykieta) z tekstem "Lista filmów:".
        self.layout.addWidget(movie_list_label) # Dodaję utworzoną etykietę do głównego pionowego układu widoku.
        
        self.movie_list_widget = QListWidget() # Tworzę instancję QListWidget (widget listy) do wyświetlania filmów i przypisuję ją do atrybutu self.movie_list_widget.
        self.layout.addWidget(self.movie_list_widget) # Dodaję utworzony widget listy do głównego pionowego układu widoku.

    def load_movies(self): # Definiuję metodę load_movies, która wczytuje filmy z bazy danych i wyświetla je w QListWidget.
        """
        Wczytuje filmy z bazy danych i wypełnia QListWidget. # Docstring opisujący metodę.
        """
        self.movie_list_widget.clear() # Czyszczę zawartość QListWidget (self.movie_list_widget), usuwając wszystkie istniejące elementy listy.
        movies = self.database.get_movies() # Pobieram listę wszystkich filmów z bazy danych (instancji Singleton Database) i przypisuję ją do zmiennej movies.
        for movie in movies: # Rozpoczynam pętlę, która iteruje przez każdy obiekt filmu na liście movies.
            self.movie_list_widget.addItem(str(movie)) # Dla każdego obiektu filmu, konwertuję go na string za pomocą str(movie) i dodaję jako nowy element do QListWidget.

    def add_movie(self): # Definiuję metodę add_movie, która jest wywoływana po kliknięciu przycisku "Dodaj film".
        """
        Dodaje nowy film do bazy danych na podstawie danych wprowadzonych w polach tekstowych. # Docstring opisujący metodę.
        """
        title = self.title_input.text() # Pobieram aktualny tekst z pola tekstowego tytułu (self.title_input) i przypisuję go do zmiennej title.
        duration = self.duration_input.value() # Pobieram aktualną wartość liczbową z pola numerycznego czasu trwania (self.duration_input) i przypisuję ją do zmiennej duration.
        age_category = self.age_category_input.value() # Pobieram aktualną wartość liczbową z pola numerycznego kategorii wiekowej (self.age_category_input) i przypisuję ją do zmiennej age_category.
        
        if not title: # Sprawdzam warunek: jeśli zmienna title jest pusta (czyli użytkownik nie wpisał tytułu filmu).
            QMessageBox.warning(self, "Błąd", "Tytuł filmu nie może być pusty.") # Wyświetlam okno dialogowe z komunikatem ostrzegawczym (QMessageBox.warning). Pierwszy argument (self) ustawia okno główne jako rodzica, drugi to tytuł okna dialogowego ("Błąd"), a trzeci to treść komunikatu.
            return # Przerywam wykonywanie metody add_movie, jeśli tytuł jest pusty.
        
        new_movie = Movie(title, duration, age_category) # Tworzę nową instancję klasy Movie, przekazując zebrane dane jako argumenty konstruktora, i przypisuję ją do zmiennej new_movie.
        self.database.add_movie(new_movie) # Dodaję nowo utworzony obiekt filmu (new_movie) do bazy danych (instancji Singleton Database).
        
        QMessageBox.information(self, "Sukces", f"Dodano film: {new_movie}") # Wyświetlam okno dialogowe z komunikatem informacyjnym (QMessageBox.information), potwierdzając dodanie filmu i wyświetlając jego tekstową reprezentację.
        
        self.load_movies() # Wywołuję metodę load_movies, aby odświeżyć listę filmów wyświetlaną w QListWidget po dodaniu nowego filmu.
        
        # Czyszczę pola wprowadzania danych po dodaniu filmu.
        self.title_input.clear() # Czyści zawartość pola tekstowego tytułu.
        self.duration_input.setValue(1) # Ustawia wartość w polu numerycznym czasu trwania z powrotem na 1.
        self.age_category_input.setValue(0) # Ustawia wartość w polu numerycznym kategorii wiekowej z powrotem na 0.