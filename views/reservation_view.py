from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox, QDialog, QLineEdit, QComboBox, QInputDialog, QDialogButtonBox, QFrame # Importuję niezbędne klasy z modułu QtWidgets do tworzenia elementów GUI, takich jak widget bazowy (QWidget), układy (QVBoxLayout, QGridLayout), etykiety (QLabel), przyciski (QPushButton), okna dialogowe (QMessageBox, QDialog, QInputDialog), pola tekstowe (QLineEdit) i listy rozwijane (QComboBox). Dodano import QInputDialog dla okna dialogowego pobierającego dane tekstowe. Dodano QDialogButtonBox.
from PyQt5.QtCore import Qt, pyqtSignal # Importuję klasy Qt z modułu QtCore (do obsługi flag i wyrównania) oraz pyqtSignal do definiowania niestandardowych sygnałów w klasach QObject (QWidget dziedziczy po QObject).
from utils.database import Database # Importuję klasę Database z modułu utils, która służy jako repozytorium danych (Singleton).
from facades.reservation_facade import ReservationFacade # Importuję klasę ReservationFacade z modułu facades, która implementuje wzorzec Fasady i upraszcza interfejs do złożonych operacji związanych z rezerwacją.
from factories.ticket_factory import RegularTicketFactory, DiscountedTicketFactory, VIPTicketFactory # Importuję klasy fabryk biletów (Normalny, Ulgowy, VIP) z modułu factories. Są to implementacje wzorca Metody Wytwórczej.
from models.seat import Seat # Importuję klasę Seat z modułu models, która reprezentuje pojedyncze miejsce w sali kinowej.

class ReservationView(QWidget): # Deklaruję klasę ReservationView, która dziedziczy po QWidget, co oznacza, że jest to niestandardowy widget GUI reprezentujący widok rezerwacji.
    """
    Widok do procesu rezerwacji biletów. # Docstring opisujący przeznaczenie klasy ReservationView.
    Wyświetla plan sali, umożliwia wybór miejsc, obliczenie ceny i dokonanie rezerwacji. # Rozszerzenie opisu funkcjonalności widoku rezerwacji.
    """

    # Sygnał emitowany po dokonaniu rezerwacji (może być użyty do odświeżenia listy rezerwacji w innym miejscu).
    # Definiuję sygnał reservation_made, który nie przekazuje żadnych argumentów (puste nawiasy).
    reservation_made = pyqtSignal() 
    
    def __init__(self): # Definiuję metodę __init__, która jest konstruktorem klasy ReservationView. Jest wywoływana podczas tworzenia instancji tej klasy.
        """
        Inicjalizacja widoku rezerwacji. # Docstring opisujący konstruktor.
        Konfiguruje układ i tworzy elementy GUI dla tej zakładki. # Opisuje działania wykonywane w konstruktorze.
        """
        super().__init__() # Wywołuję konstruktor klasy nadrzędnej QWidget. Jest to konieczne do poprawnej inicjalizacji widgetu PyQt5.
        
        # Zmień główny layout na poziomy
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        # Lewa kolumna: dotychczasowy pionowy layout
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout, stretch=1)

        self.database = Database() # Pobieram instancję bazy danych (Singleton) poprzez wywołanie klasy Database().
        self.reservation_facade = ReservationFacade() # Tworzę instancję fasady rezerwacji (ReservationFacade). Będę jej używał do wykonywania operacji na rezerwacjach.
        self.current_screening = None # Inicjalizuję atrybut self.current_screening na None. Będzie on przechowywał obiekt seansu, który aktualnie jest wybrany do rezerwacji.
        self.selected_seats = [] # Inicjalizuję pustą listę self.selected_seats. Będzie ona przechowywać obiekty Seat wybrane przez użytkownika do rezerwacji.
        self.available_ticket_factories = {} # Słownik przechowujący dostępne fabryki biletów dla bieżącego seansu.
        
        self.screening_info_label = QLabel("Proszę wybrać seans z zakładki 'Seanse'.") # Tworzę instancję QLabel (etykieta) wyświetlającą początkowy komunikat informujący o konieczności wyboru seansu.
        self.left_layout.addWidget(self.screening_info_label) # Dodaję utworzoną etykietę do głównego pionowego układu.
        
        self.seat_layout = QGridLayout() # Tworzę układ siatki (QGridLayout) dla planu sali kinowej. Przyciski miejsc zostaną dodane do tego layoutu.
        self.left_layout.addLayout(self.seat_layout) # Dodaję utworzony układ siatki do głównego pionowego układu.
 
        self.price_label = QLabel("Łączna cena: 0.00 zł") # Tworzę etykietę wyświetlającą łączną cenę rezerwacji, początkowo ustawioną na 0.00 zł.
        self.left_layout.addWidget(self.price_label) # Dodaję etykietę ceny do głównego pionowego układu.

        self.ticket_type_combo = QComboBox()  # Tworzę instancję QComboBox (lista rozwijana) do wyboru typu biletu.
        self.ticket_type_combo.setMaximumWidth(150)  # Ustawiam maksymalną szerokość na 150 pikseli.
        self.ticket_type_combo.currentIndexChanged.connect(self.update_price)  # Podpinam sygnał 'currentIndexChanged'.
        self.left_layout.addWidget(self.ticket_type_combo)  # Dodaję listę rozwijaną do układu.

        self.reserve_button = QPushButton("Zarezerwuj")  # Tworzę przycisk "Zarezerwuj".
        self.reserve_button.setMaximumWidth(150)  # Ustawiam maksymalną szerokość na 150 pikseli.
        self.reserve_button.setEnabled(False)  # Domyślnie wyłączam przycisk.
        self.reserve_button.clicked.connect(self.make_reservation)  # Podpinam sygnał 'clicked'.
        self.left_layout.addWidget(self.reserve_button)  # Dodaję przycisk do układu.
        
        self.left_layout.addStretch() # Dodaję rozciągliwy element (stretch) na końcu głównego układu pionowego. Powoduje to, że elementy powyżej są wyrównane do góry.

        # Prawa kolumna: miejsce na legendę
        self.legend_layout = QVBoxLayout()
        self.legend_layout.addStretch()  # Legenda będzie przyklejona do góry
        self.main_layout.addLayout(self.legend_layout)

        self.legend_widget = None

    def set_screening(self, screening): # Definiuję metodę set_screening, która jest slotem wywoływanym z innego widoku (np. ScreeningView) w celu ustawienia aktualnie wybranego seansu.
        """
        Ustawia aktualnie wybrany seans i odświeża widok planu sali. # Docstring opisujący metodę.
        Wywoływana z innego widoku (np. ScreeningView) po wybraniu seansu. # Wskazuje na sposób użycia metody.
        """
        self.current_screening = screening # Przypisuję przekazany obiekt seansu do atrybutu self.current_screening.
        if self.current_screening: # Sprawdzam warunek: jeśli atrybut self.current_screening nie jest None (czyli seans został pomyślnie ustawiony).
            self.screening_info_label.setText(f"Wybrany seans: {self.current_screening.movie.title} w {self.current_screening.cinema_hall.name} o {self.current_screening.date_time.strftime('%d.%m.%Y %H:%M')}") # Aktualizuję tekst etykiety informacyjnej o seansie, wyświetlając tytuł filmu, nazwę sali oraz sformatowaną datę i godzinę seansu.
            
            # Pobieram i ustawiam dostępne typy biletów
            self.available_ticket_factories = self.reservation_facade.get_available_ticket_options(self.current_screening)
            self.ticket_type_combo.clear()
            if self.available_ticket_factories:
                for ticket_name in self.available_ticket_factories.keys():
                    self.ticket_type_combo.addItem(ticket_name)
                self.ticket_type_combo.setEnabled(True)
            else:
                self.ticket_type_combo.addItem("Brak dostępnych biletów")
                self.ticket_type_combo.setEnabled(False)

            self.display_seat_layout() # Wywołuję metodę display_seat_layout, aby wyświetlić plan sali kinowej dla wybranego seansu.
            self.update_price() # Wywołuję metodę update_price, aby zaktualizować wyświetlaną łączną cenę (powinna być 0 na początku dla nowego seansu).
            self.reserve_button.setEnabled(len(self.selected_seats) > 0 and bool(self.available_ticket_factories)) # Ustawiam stan (aktywny/nieaktywny) przycisku rezerwacji w zależności od tego, czy lista wybranych miejsc (self.selected_seats) jest pusta oraz czy są dostępne bilety.
        else: # Jeśli atrybut self.current_screening jest None (czyli seans nie został ustawiony lub został zresetowany).
            self.screening_info_label.setText("Proszę wybrać seans z zakładki 'Seanse'.") # Resetuję tekst etykiety informacyjnej do początkowego komunikatu.
            self.clear_seat_layout() # Wywołuję metodę clear_seat_layout, aby usunąć wszystkie elementy z planu sali.
            self.selected_seats = [] # Czyszczę listę wybranych miejsc.
            self.ticket_type_combo.clear()
            self.ticket_type_combo.setEnabled(False)
            self.available_ticket_factories = {}
            self.update_price() # Wywołuję metodę update_price, aby zaktualizować wyświetlaną cenę na 0.00 zł.
            self.reserve_button.setEnabled(False) # Wyłączam przycisk rezerwacji.
 

    def display_seat_layout(self): # Definiuję metodę display_seat_layout, która tworzy i wyświetla graficzną reprezentację planu sali kinowej.
        """
        Wyświetla plan sali dla aktualnie wybranego seansu. # Docstring opisujący metodę.
        Tworzy przyciski reprezentujące miejsca i dodaje je do układu siatki. # Opisuje działanie metody.
        """
        self.clear_seat_layout() # Najpierw wywołuję metodę clear_seat_layout, aby usunąć wszystkie istniejące przyciski miejsc z układu siatki przed wyświetleniem nowego planu sali.

        # --- LEGENDA KOLORÓW MIEJSC ---
        # Usuń starą legendę jeśli istnieje
        if self.legend_widget is not None:
            self.legend_layout.removeWidget(self.legend_widget)
            self.legend_widget.deleteLater()
            self.legend_widget = None

        legend_widget = QWidget()
        legend_vbox = QVBoxLayout(legend_widget)
        legend_vbox.setContentsMargins(20, 40, 20, 0)
        legend_vbox.setSpacing(20)

        # Lightgreen - wolne
        free_box = QFrame()
        free_box.setFixedSize(20, 20)
        free_box.setStyleSheet("background-color: lightgreen; border: 1px solid #888;")
        free_label = QLabel("Wolne")
        free_label.setStyleSheet("color: white;")
        row1 = QHBoxLayout()
        row1.addWidget(free_box)
        row1.addWidget(free_label)
        legend_vbox.addLayout(row1)

        # Orange - zarezerwowane
        reserved_box = QFrame()
        reserved_box.setFixedSize(20, 20)
        reserved_box.setStyleSheet("background-color: orange; border: 1px solid #888;")
        reserved_label = QLabel("Zarezerwowane")
        reserved_label.setStyleSheet("color: white;")
        row2 = QHBoxLayout()
        row2.addWidget(reserved_box)
        row2.addWidget(reserved_label)
        legend_vbox.addLayout(row2)

        # Red - sprzedane
        sold_box = QFrame()
        sold_box.setFixedSize(20, 20)
        sold_box.setStyleSheet("background-color: red; border: 1px solid #888;")
        sold_label = QLabel("Sprzedane")
        sold_label.setStyleSheet("color: white;")
        row3 = QHBoxLayout()
        row3.addWidget(sold_box)
        row3.addWidget(sold_label)
        legend_vbox.addLayout(row3)

        legend_widget.setLayout(legend_vbox)
        self.legend_layout.insertWidget(0, legend_widget)
        self.legend_widget = legend_widget

        if not self.current_screening: # Sprawdzam warunek: jeśli nie ma aktualnie wybranego seansu (self.current_screening jest None).
            return # Jeśli nie ma wybranego seansu, przerywam dalsze wykonywanie metody.

        # Tworzę przyciski dla każdego miejsca w sali i dodaję je do siatki.
        for seat in self.current_screening.seats: # Rozpoczynam pętlę, która iteruje przez każdy obiekt Seat na liście miejsc (seats) w aktualnie wybranym seansie (self.current_screening).
            seat_button = QPushButton(str(seat)) # Tworzę instancję QPushButton (przycisk) z tekstem reprezentującym miejsce, uzyskanym przez konwersję obiektu Seat na string za pomocą str(seat) (np. "R1M5").
            seat_button.setFixedSize(40, 40) # Ustawiam stały rozmiar przycisku miejsca na 40 pikseli szerokości i 40 pikseli wysokości.
            seat_button.setProperty("seat_obj", seat) # Zapisuję referencję do oryginalnego obiektu Seat jako właściwość przycisku o nazwie "seat_obj". Pozwala to na łatwy dostęp do obiektu Seat z przycisku.
            
            # Ustawiam styl przycisku w zależności od stanu miejsca.
            if seat.state.__class__.__name__ == "FreeSeatState": # Sprawdzam, czy aktualny stan miejsca jest instancją klasy FreeSeatState (wolne).
                seat_button.setStyleSheet("background-color: lightgreen;") # Jeśli miejsce jest wolne, ustawiam kolor tła przycisku na jasnozielony za pomocą stylów CSS.
                seat_button.clicked.connect(self.toggle_seat_selection) # Podpinam sygnał 'clicked' przycisku do metody self.toggle_seat_selection. Oznacza to, że kliknięcie wolnego miejsca wywoła tę metodę w celu wyboru/odznaczenia miejsca.
            elif seat.state.__class__.__name__ == "ReservedSeatState": # Sprawdzam, czy aktualny stan miejsca jest instancją klasy ReservedSeatState (zarezerwowane).
                 seat_button.setStyleSheet("background-color: orange;") # Jeśli miejsce jest zarezerwowane, ustawiam kolor tła przycisku na żółty.
                 seat_button.setEnabled(False) # Wyłączam przycisk dla zarezerwowanych miejsc, aby nie można ich było wybrać.
            elif seat.state.__class__.__name__ == "SoldSeatState": # Sprawdzam, czy aktualny stan miejsca jest instancją klasy SoldSeatState (sprzedane).
                seat_button.setStyleSheet("background-color: red;") # Jeśli miejsce jest sprzedane, ustawiam kolor tła przycisku na czerwony.
                seat_button.setEnabled(False) # Wyłączam przycisk dla sprzedanych miejsc.
            else: # Jeśli stan miejsca jest inny niż wolne, zarezerwowane lub sprzedane (np. nieznany stan).
                 seat_button.setStyleSheet("background-color: gray;") # Ustawiam kolor tła przycisku na szary.
                 seat_button.setEnabled(False) # Wyłączam przycisk dla nieznanych stanów.

            # Dodaję przycisk miejsca do układu siatki, używając numeru rzędu i miejsca jako koordynatów.
            # Używam (seat.row - 1) i (seat.number - 1), ponieważ QGridLayout używa indeksów od 0.
            # Place button in its natural column index
            col_index = seat.number - 1 # 0-based index
            self.seat_layout.addWidget(seat_button, seat.row - 1, col_index) # Add button at its original column index
 
        # Dodaję etykiety rzędów i miejsc do siatki dla lepszej czytelności.
        for row in range(self.current_screening.cinema_hall.rows):  # Iteruję przez liczbę rzędów w sali kinowej.
            row_label = QLabel(f"Rząd {row + 1}")  # Tworzę etykietę z numerem rzędu.
            row_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Wyrównuję tekst etykiety do lewej i środka w pionie.
            row_label.setContentsMargins(10, 0, 0, 0)  # Dodaję margines po lewej stronie, aby odsunąć etykietę od miejsc.
            self.seat_layout.addWidget(row_label, row, self.current_screening.cinema_hall.seats_per_row)  # Dodaję etykietę w kolumnie tuż za ostatnim miejscem w rzędzie.

        # Add a fixed minimum width for the gap column for middle
        middle = (self.current_screening.cinema_hall.seats_per_row // 2)-1 # Calculate middle column index
        self.seat_layout.setColumnMinimumWidth(middle, 60) # Set minimum width for the gap column

        # Dodaję etykiety miejsc do siatki dla lepszej czytelności.
        max_seat_num = self.current_screening.cinema_hall.seats_per_row
        for seat_num_idx in range(max_seat_num):  # Iterate using 0-based index
            seat_num = seat_num_idx + 1 # Actual seat number (1-based)
            col_label = QLabel(f"M{seat_num}")  # Create label e.g., "M 7"
            col_label.setAlignment(Qt.AlignCenter)  # Center align label text

            # Place label in its natural column index
            col_index = seat_num_idx # 0-based index
            self.seat_layout.addWidget(col_label, self.current_screening.cinema_hall.rows, col_index)  # Add label at its original column index

 
    def clear_seat_layout(self): # Definiuję metodę clear_seat_layout, która usuwa wszystkie widgety (przyciski miejsc i etykiety) z układu siatki planu sali.
        """
        Usuwa wszystkie elementy z układu siatki planu sali. # Docstring opisujący metodę.
        Używane przed wyświetleniem nowego planu sali. # Wskazuje na sposób użycia metody.
        """
        # Iteruję przez wszystkie elementy w układzie siatki.
        while self.seat_layout.count(): # Rozpoczynam pętlę, która trwa dopóki liczba elementów w układzie siatki (self.seat_layout.count()) jest większa od zera.
            item = self.seat_layout.takeAt(0) # Pobieram kolejny element (QLayoutItem) z układu siatki bez usuwania go z pamięci.
            widget = item.widget() # Pobieram widget skojarzony z pobranym elementem (jeśli element zawiera widget).
            if widget is not None: # Sprawdzam warunek: jeśli pobrany element zawiera widget (widget nie jest None).
                widget.deleteLater() # Planuję usunięcie widgetu. deleteLater() jest bezpieczniejszą metodą w PyQt, ponieważ odkłada usunięcie widgetu do momentu, gdy pętla zdarzeń Qt będzie gotowa, zapobiegając potencjalnym problemom z dostępem do usuwanego widgetu.
            # Else: Element może być tylko układem (layout), w takim przypadku nie ma widgetu do usunięcia, więc nie robimy nic więcej.
        
        # Resetuj minimalną szerokość kolumn (usuwa padding dodany dla środkowej przerwy)
        for col in range(self.seat_layout.columnCount()):
            self.seat_layout.setColumnMinimumWidth(col, 0)
            

    def toggle_seat_selection(self): # Definiuję metodę toggle_seat_selection, która jest slotem wywoływanym po kliknięciu przycisku reprezentującego wolne miejsce.
        """
        Slot wywoływany po kliknięciu przycisku miejsca. # Docstring opisujący metodę.
        Dodaje lub usuwa miejsce z listy wybranych miejsc i aktualizuje jego wygląd. # Opisuje działanie metody.
        """
        seat_button = self.sender() # Pobieram obiekt, który wysłał sygnał 'clicked', czyli przycisk miejsca, który został kliknięty.
        seat = seat_button.property("seat_obj") # Pobieram referencję do oryginalnego obiektu Seat, który został zapisany jako właściwość przycisku za pomocą setProperty.
        
        if seat in self.selected_seats: # Sprawdzam warunek: jeśli obiekt Seat jest już obecny na liście wybranych miejsc (self.selected_seats).
            self.selected_seats.remove(seat) # Jeśli miejsce jest już wybrane, usuwam je z listy wybranych miejsc.
            seat_button.setStyleSheet("background-color: lightgreen;") # Zmieniam kolor tła przycisku miejsca z powrotem na jasnozielony, symbolizujący wolne miejsce.
        else: # Jeśli obiekt Seat nie jest obecny na liście wybranych miejsc.
            self.selected_seats.append(seat) # Dodaję obiekt Seat do listy wybranych miejsc.
            seat_button.setStyleSheet("background-color: blue;") # Zmieniam kolor tła przycisku miejsca na niebieski, symbolizujący wybrane miejsce.
        
        self.update_price() # Wywołuję metodę update_price, aby przeliczyć i zaktualizować wyświetlaną łączną cenę rezerwacji na podstawie nowej listy wybranych miejsc.
        self.reserve_button.setEnabled(len(self.selected_seats) > 0) # Ustawiam stan (aktywny/nieaktywny) przycisku rezerwacji w zależności od tego, czy lista wybranych miejsc nie jest pusta.

    def update_price(self): # Definiuję metodę update_price, która oblicza łączną cenę rezerwacji na podstawie wybranych miejsc i typu biletu.
        """
        Oblicza i aktualizuje wyświetlaną łączną cenę rezerwacji na podstawie wybranych miejsc i typu biletu. # Docstring opisujący metodę.
        """
        if not self.current_screening or not self.selected_seats: # Sprawdzam warunek: jeśli nie wybrano seansu (self.current_screening jest None) LUB nie wybrano żadnych miejsc (lista self.selected_seats jest pusta).
            self.price_label.setText("Łączna cena: 0.00 zł") # Jeśli warunek jest spełniony, ustawiam tekst etykiety ceny na "Łączna cena: 0.00 zł".
            return # Przerywam dalsze wykonywanie metody update_price.

        # Pobieram wybraną fabrykę biletów na podstawie wyboru w QComboBox i dostępnych opcji.
        selected_ticket_name = self.ticket_type_combo.currentText()
        
        if not selected_ticket_name or not self.available_ticket_factories:
            self.price_label.setText("Łączna cena: 0.00 zł")
            return

        ticket_factory = self.available_ticket_factories.get(selected_ticket_name)

        if not ticket_factory:
            # Ten przypadek nie powinien wystąpić, jeśli combo box jest poprawnie wypełniony
            # i zsynchronizowany z self.available_ticket_factories.
            # Można dodać logowanie błędu lub wyświetlenie komunikatu.
            self.price_label.setText("Łączna cena: 0.00 zł")
            QMessageBox.warning(self, "Błąd", "Nie można znaleźć fabryki dla wybranego typu biletu.")
            return

        # Obliczam łączną cenę rezerwacji, używając fasady.
        # Wywołuję metodę calculate_price na instancji fasady rezerwacji (self.reservation_facade),
        # przekazując aktualny seans, listę wybranych miejsc i wybraną fabrykę biletów.
        # Metoda ta zwraca łączną cenę oraz listę utworzonych obiektów biletów.
        total_price, _ = self.reservation_facade.calculate_price(self.current_screening, self.selected_seats, ticket_factory)
        
        # Aktualizuję tekst etykiety ceny.
        self.price_label.setText(f"Łączna cena: {total_price:.2f} zł") # Ustawiam tekst etykiety ceny (self.price_label) na sformatowany string zawierający "Łączna cena:" i obliczoną łączną cenę (total_price) z dwoma miejscami po przecinku.

    def make_reservation(self): # Definiuję metodę make_reservation, która jest slotem wywoływanym po kliknięciu przycisku "Zarezerwuj".
        """
        Dokonuje rezerwacji wybranych miejsc dla klienta. # Docstring opisujący metodę.
        Wyświetla dialog do wprowadzenia imienia i nazwiska klienta, a następnie tworzy rezerwację. # Opisuje działanie metody.
        """
        if not self.current_screening or not self.selected_seats: # Sprawdzam warunek: jeśli nie wybrano seansu LUB nie wybrano żadnych miejsc.
            QMessageBox.warning(self, "Błąd", "Proszę wybrać seans i miejsca.") # Jeśli warunek jest spełniony, wyświetlam okno dialogowe z komunikatem ostrzegawczym.
            return # Przerywam dalsze wykonywanie metody make_reservation.

        # Pobieram wybraną fabrykę biletów (tak samo jak w update_price).
        selected_ticket_name = self.ticket_type_combo.currentText()

        if not selected_ticket_name or not self.available_ticket_factories:
            QMessageBox.warning(self, "Błąd", "Proszę wybrać typ biletu.")
            return

        ticket_factory = self.available_ticket_factories.get(selected_ticket_name)

        if not ticket_factory:
            QMessageBox.warning(self, "Błąd", f"Nieprawidłowy typ biletu: {selected_ticket_name}. Proszę wybrać poprawny typ biletu.")
            return
        
        # Obliczam cenę i generuję obiekty biletów.
        # Wywołuję metodę calculate_price na instancji fasady rezerwacji, aby uzyskać łączną cenę i listę obiektów biletów dla wybranych miejsc i typu biletu.
        total_price, tickets = self.reservation_facade.calculate_price(self.current_screening, self.selected_seats, ticket_factory)

        # Wyświetlam dialog do wprowadzenia imienia i nazwiska klienta.
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Potwierdzenie rezerwacji")
        dialog.setLabelText("Imię i nazwisko:")
        dialog.setTextValue("")  # Initial text can be empty or pre-filled
        dialog.setMinimumWidth(300) # Set a minimum width for the dialog
        
        # Apply stylesheet for better readability
        dialog.setStyleSheet("""
            QInputDialog {
                background-color: #f0f0f0; /* Light gray background for the dialog */
            }
            QLineEdit {
                background-color: white; /* White background for the input field */
                color: black; /* Black text color for the input field */
                border: 1px solid #cccccc;
                padding: 5px;
            }
            QLabel {
                color: black; /* Black text color for the label */
            }
            QPushButton {
                color: white;
                background-color: #007bff; /* Blue background for buttons */
                border: 1px solid #007bff;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0056b3; /* Darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #004085; /* Even darker blue when pressed */
            }
        """)

        ok = dialog.exec_()
        customer_name = dialog.textValue()

        if ok and customer_name:
            summary_dialog = ReservationSummaryDialog(
                self.current_screening,
                self.selected_seats,
                customer_name,
                total_price,
                self
            )
            
            if summary_dialog.exec_() == QDialog.Accepted:
                try:
                    reservation = self.reservation_facade.make_reservation(customer_name, self.current_screening, self.selected_seats, tickets)
                    
                    msg_box = QMessageBox(self)
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setWindowTitle("Sukces")
                    msg_box.setText("Sukces! Udało Ci się zarezerwować bilet/y.")
                    msg_box.setStyleSheet("""
                        QLabel {
                            color: black; /* Czarny kolor tekstu */
                            font-size: 12pt; /* Rozmiar czcionki */
                        }
                        QMessageBox {
                            background-color: white; /* Białe tło okna */
                        }
                        QPushButton {
                            color: white;
                            background-color: #007bff; /* Niebieskie przyciski */
                            border: 1px solid #007bff;
                            padding: 5px 10px;
                            border-radius: 3px;
                        }
                        QPushButton:hover {
                            background-color: #0056b3; /* Ciemniejszy niebieski po najechaniu */
                        }
                        QPushButton:pressed {
                            background-color: #004085; /* Jeszcze ciemniejszy niebieski po kliknięciu */
                        }
                    """)
                    msg_box.exec_()

                    self.selected_seats = []
                    self.display_seat_layout()
                    self.update_price()
                    self.reserve_button.setEnabled(False)
                    self.reservation_made.emit()

                except Exception as e:
                    QMessageBox.critical(self, "Błąd rezerwacji", f"Wystąpił błąd podczas rezerwacji: {e}")
            # else: User cancelled the summary dialog, do nothing further.

        elif ok:
             QMessageBox.warning(self, "Błąd", "Imię i nazwisko klienta nie może być puste.")


class ReservationSummaryDialog(QDialog):
    def __init__(self, screening, selected_seats, customer_name, total_price, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Podsumowanie Rezerwacji")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        details_text = f"Film: {screening.movie.title}\n"
        details_text += f"Data: {screening.date_time.strftime('%d.%m.%Y %H:%M')}\n"
        details_text += f"Sala: {screening.cinema_hall.name}\n\n"
        details_text += "Zarezerwowane miejsca:\n"
        details_text += self._format_selected_seats(selected_seats) + "\n\n"
        details_text += f"Imię i nazwisko: {customer_name}\n"
        details_text += f"Łączna cena: {total_price:.2f} zł"

        summary_label = QLabel(details_text)
        summary_label.setAlignment(Qt.AlignLeft)
        summary_label.setWordWrap(True) # Ensure text wraps if too long
        layout.addWidget(summary_label)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setText("Potwierdź")
        button_box.button(QDialogButtonBox.Cancel).setText("Anuluj")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: black;
                font-size: 10pt; /* Adjusted font size for readability */
            }
            QPushButton {
                color: white;
                background-color: #007bff;
                border: 1px solid #007bff;
                padding: 8px 15px; /* Increased padding for better clickability */
                border-radius: 3px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)

    def _format_selected_seats(self, selected_seats):
        if not selected_seats:
            return "Brak wybranych miejsc"
        
        seats_by_row = {}
        for seat in selected_seats:
            if seat.row not in seats_by_row:
                seats_by_row[seat.row] = []
            seats_by_row[seat.row].append(seat.number)
        
        summary_lines = []
        for row, numbers in sorted(seats_by_row.items()):
            numbers_str = ", ".join(map(str, sorted(numbers)))
            label = "Miejsce" if len(numbers) == 1 else "Miejsca"
            summary_lines.append(f"  Rząd {row} {label}: {numbers_str}") # Added indent for seats
        return "\n".join(summary_lines)