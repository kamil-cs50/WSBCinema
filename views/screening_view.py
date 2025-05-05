from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QCalendarWidget, QHBoxLayout, QMessageBox # Importuję niezbędne klasy z modułu QtWidgets, dodaję QMessageBox.
from PyQt5.QtCore import QDate, Qt, pyqtSignal # Importuję klasy QDate (do obsługi daty), Qt (do wyrównania) i pyqtSignal (do definiowania sygnałów) z modułu QtCore.
from utils.database import Database # Importuję klasę Database do pobierania danych o seansach.

class ScreeningView(QWidget):
    """
    Widok do przeglądania seansów.
    Umożliwia wybór daty i wyświetlenie listy seansów dostępnych w tym dniu.
    """
    
    
    # Definiuję sygnał, który będzie emitowany po wybraniu seansu. Sygnał ten będzie przekazywał obiekt Seansu.
    screening_selected = pyqtSignal(object)
    
    def __init__(self):
        """
        Inicjalizacja widoku seansów.
        Konfiguruje układ i tworzy elementy GUI dla tej zakładki.
        """
        super().__init__() # Wywołuję konstruktor klasy nadrzędnej QWidget.
        # print("Inicjalizacja ScreeningView...") # Usunięto print do debugowania
        
        self.database = Database() # Pobieram instancję bazy danych (Singleton).
        self.selected_screening = None # Atrybut do przechowywania wybranego seansu.
        self.layout = QVBoxLayout(self) # Tworzę główny pionowy układ dla tego widoku.
        
        self.setup_date_selection() # Konfiguruję sekcję do wyboru daty.
        self.setup_screening_list() # Konfiguruję sekcję do wyświetlania listy seansów.
        self.setup_action_buttons() # Konfiguruję przyciski akcji (np. wybór seansu).

        self.load_screenings_for_date(QDate.currentDate()) # Wczytuję seanse dla dzisiejszej daty przy starcie.

    def setup_date_selection(self):
        """
        Konfiguruje sekcję GUI do wyboru daty.
        Zawiera kalendarz (QCalendarWidget).
        """
        date_layout = QHBoxLayout() # Tworzę poziomy układ dla kalendarza.
        date_label = QLabel("Wybierz datę:") # Etykieta "Wybierz datę:".
        date_layout.addWidget(date_label) # Dodaję etykietę do układu.

        self.calendar_widget = QCalendarWidget() # Tworzę widget kalendarza.
        self.calendar_widget.setGridVisible(True) # Włączam wyświetlanie siatki w kalendarzu.
        # Podpinam sygnał selectionChanged kalendarza do metody on_date_selected.
        self.calendar_widget.selectionChanged.connect(self.on_date_selected) 
        date_layout.addWidget(self.calendar_widget) # Dodaję kalendarz do układu.

        date_layout.addStretch() # Dodaję rozciągliwy element, aby kalendarz był wyrównany do lewej.

        self.layout.addLayout(date_layout) # Dodaję poziomy układ wyboru daty do głównego pionowego układu.


    def setup_screening_list(self):
        """
        Konfiguruje sekcję GUI do wyświetlania listy seansów dla wybranej daty.
        Zawiera etykietę "Dostępne seanse:" i widget listy (QListWidget).
        """
        screening_list_label = QLabel("Dostępne seanse:") # Etykieta "Dostępne seanse:".
        self.layout.addWidget(screening_list_label) # Dodaję etykietę do głównego układu.
        
        self.screening_list_widget = QListWidget() # Tworzę widget listy do wyświetlania seansów.
        # Podpinam sygnał currentItemChanged listy seansów do metody on_screening_selected.
        self.screening_list_widget.currentItemChanged.connect(self.on_screening_selected)
        self.layout.addWidget(self.screening_list_widget) # Dodaję widget listy do głównego układu.

    def setup_action_buttons(self):
        """
        Konfiguruje przyciski akcji pod listą seansów.
        """
        action_button_layout = QHBoxLayout() # Tworzę poziomy układ dla przycisków akcji.

        self.select_screening_button = QPushButton("Wybierz seans") # Tworzę przycisk "Wybierz seans".
        self.select_screening_button.setEnabled(False) # Domyślnie przycisk jest wyłączony (żaden seans nie jest wybrany).
        # Podpinam sygnał clicked przycisku do metody select_screening.
        self.select_screening_button.clicked.connect(self.select_screening)
        action_button_layout.addWidget(self.select_screening_button) # Dodaję przycisk do układu.

        action_button_layout.addStretch() # Dodaję rozciągliwy element.

        self.layout.addLayout(action_button_layout) # Dodaję poziomy układ przycisków akcji do głównego pionowego układu.

    def on_date_selected(self):
        """
        Slot wywoływany po zmianie wybranej daty w kalendarzu.
        Wczytuje seanse dla nowo wybranej daty.
        """
        selected_date = self.calendar_widget.selectedDate().toPyDate() # Pobieram wybraną datę z kalendarza jako obiekt date z Pythona.
        self.load_screenings_for_date(selected_date) # Wczytuję seanse dla wybranej daty.

    def load_screenings_for_date(self, date):
        """
        Wczytuje seanse dla podanej daty z bazy danych i wypełnia QListWidget.
        """
        self.screening_list_widget.clear() # Czyszczę istniejącą listę seansów w GUI.
        # Pobieram seanse dla podanej daty z bazy danych.
        screenings = self.database.get_screenings_for_date(date) 
        
        if not screenings: # Sprawdzam, czy lista seansów jest pusta.
            self.screening_list_widget.addItem("Brak seansów w wybranym dniu.") # Dodaję informację o braku seansów.
            self.select_screening_button.setEnabled(False) # Wyłączam przycisk wyboru seansu.
            self.selected_screening = None # Resetuję wybrany seans.
            return # Przerywam działanie metody.

        # Dodaję seanse do listy w GUI.
        for screening in screenings: # Iteruję przez każdy seans na liście.
            self.screening_list_widget.addItem(str(screening)) # Dodaję tekstową reprezentację seansu do QListWidget.
        
        # Domyślnie żaden seans nie jest wybrany po załadowaniu nowej daty
        self.selected_screening = None 
        self.select_screening_button.setEnabled(False) # Wyłączam przycisk

    def on_screening_selected(self, current, previous):
        """
        Slot wywoływany po zmianie wybranego elementu na liście seansów.
        Zapamiętuje wybrany seans.
        """
        if current: # Sprawdzam, czy jakiś element został wybrany (current nie jest None).
            # Wyszukuję wybrany seans w bazie danych na podstawie jego tekstowej reprezentacji.
            selected_text = current.text()
            # Znajduję obiekt seansu, którego tekstowa reprezentacja pasuje do wybranego elementu listy.
            self.selected_screening = next((s for s in self.database.get_screenings_for_date(self.calendar_widget.selectedDate().toPyDate()) if str(s) == selected_text), None)
            self.select_screening_button.setEnabled(self.selected_screening is not None) # Włączam przycisk, jeśli seans został znaleziony.
        else: # Jeśli żaden element nie jest wybrany (lista pusta lub zaznaczenie usunięte).
            self.selected_screening = None # Resetuję wybrany seans.
            self.select_screening_button.setEnabled(False) # Wyłączam przycisk wyboru seansu.

    def select_screening(self):
        """
        Metoda wywoływana po kliknięciu przycisku "Wybierz seans".
        Sygnalizuje główne okno o wyborze seansu.
        """
        if self.selected_screening: # Sprawdzam, czy jakiś seans został wybrany.
            print(f"Wybrano seans: {self.selected_screening}") # Tymczasowy print.
            # Emituję sygnał screening_selected, przekazując wybrany obiekt seansu.
            self.screening_selected.emit(self.selected_screening)
            # Na potrzeby demonstracji, można wyświetlić komunikat.
            # QMessageBox.information(self, "Wybrano seans", f"Wybrano seans: {self.selected_screening}") # Komunikat informacyjny usunięto, aby nie blokował aplikacji po wybraniu seansu.
            # TODO: Emitować sygnał do MainWindow z wybranym seansem, aby przełączyć widok na ReservationView.
        else:
             QMessageBox.warning(self, "Błąd", "Proszę wybrać seans z listy.") # Wyświetlam komunikat ostrzegawczy, jeśli żaden seans nie został wybrany.