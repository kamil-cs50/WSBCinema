from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget # Importuję niezbędne klasy z modułu QtWidgets do tworzenia elementów GUI.
from PyQt5.QtCore import Qt # Importuję moduł QtCore do obsługi podstawowych typów danych i sygnałów/slotów.
from PyQt5.QtGui import QFont, QColor, QLinearGradient # Importuję moduł QtGui do obsługi czcionek, kolorów i gradientów.

# Zachowuję import BackDropWrapper na później, ale nie używam go w layoucie
from utils.glass_morphism import BackDropWrapper

# Importuję widoki dla poszczególnych zakładek
from views.movie_view import MovieView  # Widok do zarządzania filmami.
from views.screening_view import ScreeningView  # Widok do zarządzania seansami.
from views.reservation_view import ReservationView  # Widok do procesu rezerwacji.

class MainWindow(QMainWindow):
    """
    Główne okno aplikacji WSBCinema.
    Zawiera nagłówek oraz zakładki dla różnych części systemu (Filmy, Seanse, Rezerwacje),
    bez efektu glassmorphism na tym etapie debugowania.
    """
    
    def __init__(self):
        """
        Inicjalizacja głównego okna aplikacji.
        Konfiguruje podstawowe właściwości okna i tworzy jego główne komponenty.
        """
        super().__init__()  # Wywołuję konstruktor klasy nadrzędnej QMainWindow.
        # print("Inicjalizacja MainWindow...") # Usunięto log debugowania
        
        # Ustawiam podstawowe właściwości okna.
        self.setWindowTitle("WSBCinema - System Rezerwacji Biletów")  # Ustawiam tytuł paska okna.
        self.setGeometry(100, 100, 1200, 800)  # Ustawiam pozycję (x, y) i rozmiar (szerokość, wysokość) okna.
        
        # Tworzę główny widget centralny, który będzie zawierał wszystkie pozostałe elementy.
        self.central_widget = QWidget()  # Tworzę instancję QWidget.
        self.setCentralWidget(self.central_widget)  # Ustawiam utworzony widget jako centralny widget okna głównego.
        
        # Tworzę główny układ pionowy dla centralnego widgetu.
        self.layout = QVBoxLayout(self.central_widget)  # Tworzę instancję QVBoxLayout i ustawiam central_widget jako jego rodzica.
        self.layout.setContentsMargins(0, 0, 0, 0) # Usuwam domyślne marginesy wokół zawartości.
        self.layout.setSpacing(0) # Ustawiam odstęp między elementami layoutu na 0.
        
        # Tworzę nagłówek aplikacji.
        self.setup_header()  # Wywołuję metodę odpowiedzialną za tworzenie i konfigurację nagłówka.
        
        # Tworzę zakładki aplikacji.
        self.setup_tabs()  # Wywołuję metodę odpowiedzialną za tworzenie i konfigurację zakładek.
        
        # Ustawiam style wizualne dla elementów okna.
        self.setup_styles()  # Wywołuję metodę odpowiedzialną za stosowanie stylów CSS (Qt Style Sheets).

    def setup_header(self):
        # print("Konfiguracja nagłówka...") # Usunięto log debugowania
        """
        Tworzy nagłówek aplikacji z tytułem i podtytułem, dodany bezpośrednio do głównego layoutu.
        """
        # Tworzę kontener (QWidget) dla elementów nagłówka.
        header_container = QWidget()  # Tworzę widget kontenera.
        # Usunięto tymczasowe style i minimalną wysokość
        header_layout = QVBoxLayout(header_container)  # Tworzę pionowy układ dla kontenera nagłówka.
        header_layout.setAlignment(Qt.AlignCenter) # Wyrównuję zawartość nagłówka do środka.
        header_layout.setContentsMargins(20, 10, 20, 10) # Dodaję wewnętrzne marginesy.

        # Tworzę etykietę dla tytułu kina.
        title = QLabel("WSBCinema")  # Tworzę etykietę z tekstem "WSBCinema".
        title.setAlignment(Qt.AlignCenter)  # Wyrównuję tekst tytułu do środka.
        title.setFont(QFont("Arial", 24, QFont.Bold))  # Ustawiam czcionkę: Arial, rozmiar 24, pogrubiona.
        
        # Tworzę etykietę dla podtytułu systemu.
        subtitle = QLabel("System Rezerwacji Biletów")  # Tworzę etykietę z tekstem podtytułu.
        subtitle.setAlignment(Qt.AlignCenter)  # Wyrównuję tekst podtytułu do środka.
        subtitle.setFont(QFont("Arial", 16))  # Ustawiam czcionkę: Arial, rozmiar 16.
        
        # Dodaję tytuł i podtytuł do układu nagłówka.
        header_layout.addWidget(title)  # Dodaję etykietę tytułu do układu nagłówka.
        header_layout.addWidget(subtitle)  # Dodaję etykietę podtytułu do układu nagłówka.
        
        # Dodaję kontener nagłówka bezpośrednio do głównego układu
        self.layout.addWidget(header_container) 

    def setup_tabs(self):
        """
        Tworzy zakładki dla różnych widoków aplikacji (Filmy, Seanse, Rezerwacje),
        dodane bezpośrednio do głównego layoutu (bez BackDropWrapper).
        """
        # Tworzę widget zakładek (QTabWidget).
        self.tabs = QTabWidget()  # Tworzę instancję QTabWidget.
        # Usunięto tymczasowe style i minimalną wysokość

        # Tworzę instancje widoków dla każdej zakładki
        self.movie_tab = MovieView()  # Tworzę widok filmów.
        self.screening_tab = ScreeningView()  # Tworzę widok seansów.
        self.reservation_tab = ReservationView()  # Tworzę widok rezerwacji.
        
        # Dodaję poszczególne widoki jako zakładki do QTabWidget.
        self.tabs.addTab(self.movie_tab, "Filmy")  # Dodaję widok filmów jako zakładkę o nazwie "Filmy".
        self.tabs.addTab(self.screening_tab, "Seanse")  # Dodaję widok seansów jako zakładkę o nazwie "Seanse".
        self.tabs.addTab(self.reservation_tab, "Rezerwacje")  # Dodaję widok rezerwacji jako zakładkę o nazwie "Rezerwacje".
        
        # Dodaję widget zakładek bezpośrednio do głównego układu
        self.layout.addWidget(self.tabs) 

    def setup_styles(self):
        """
        Ustawia style wizualne dla elementów aplikacji przy użyciu Qt Style Sheets.
        """
        # Ustawiam globalny styl dla głównego okna i jego elementów podrzędnych.
        self.setStyleSheet("""
            QMainWindow {
                /* Styl dla głównego okna (tło gradientowe). */
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                           stop:0 #2c3e50, stop:1 #3498db); /* Gradient od ciemnoszarego do niebieskiego. */
            }
            
            QTabWidget::pane {
                /* Styl dla obszaru zawartości zakładek. */
                border: none; /* Brak obramowania. */
                background: transparent; /* Przezroczyste tło, aby efekt glassmorphism był widoczny. */
            }
            
            QTabBar::tab {
                /* Styl dla poszczególnych przycisków zakładek na pasku zakładek. */
                background: rgba(255, 255, 255, 100); /* Białe tło z 100/255 (ok. 40%) przezroczystości. */
                color: white; /* Kolor tekstu na biały. */
                padding: 10px 20px; /* Wewnętrzne odstępy (padding) w przyciskach zakładek. */
                border-top-left-radius: 8px; /* Zaokrąglenie lewego górnego rogu. */
                border-top-right-radius: 8px; /* Zaokrąglenie prawego górnego rogu. */
                margin-right: 2px; /* Odstęp między przyciskami zakładek. */
            }
            
            QTabBar::tab:selected {
                /* Styl dla aktywnej (wybranej) zakładki. */
                background: rgba(255, 255, 255, 150); /* Jaśniejsze białe tło z 150/255 (ok. 60%) przezroczystości. */
                font-weight: bold; /* Tekst pogrubiony. */
            }
            
            QPushButton {
                /* Styl dla wszystkich przycisków (QPushButton). */
                background-color: rgba(52, 152, 219, 180); /* Niebieskie tło z częściową przezroczystością. */
                color: white; /* Kolor tekstu na biały. */
                border: none; /* Brak obramowania. */
                border-radius: 5px; /* Zaokrąglenie rogów na 5 pikseli. */
                padding: 10px 20px; /* Wewnętrzne odstęsy. */
                font-weight: bold; /* Tekst pogrubiony. */
            }
            
            QPushButton:hover {
                /* Styl dla przycisków po najechaniu myszą. */
                background-color: rgba(41, 128, 185, 200); /* Ciemniejszy niebieski kolor tła z większą przezroczystością. */
            }
            
            QLabel {
                /* Styl dla wszystkich etykiet (QLabel). */
                color: white; /* Kolor tekstu na biały. */
            }
        """)  # Stosuję zdefiniowany arkusz stylów do głównego okna i jego elementów.
