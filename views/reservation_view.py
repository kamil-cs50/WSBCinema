from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox, QDialog, QLineEdit, QComboBox # Importuję niezbędne klasy z modułu QtWidgets.
from PyQt5.QtCore import Qt, pyqtSignal # Importuję klasy Qt (do wyrównania) i pyqtSignal (do definiowania sygnałów) z modułu QtCore.
from utils.database import Database # Importuję klasę Database do interakcji z danymi.
from facades.reservation_facade import ReservationFacade # Importuję fasadę rezerwacji do uproszczenia operacji.
from factories.ticket_factory import RegularTicketFactory, DiscountedTicketFactory, VIPTicketFactory # Importuję fabryki biletów.
from models.seat import Seat # Importuję klasę Seat.

class ReservationView(QWidget):
    """
    Widok do procesu rezerwacji biletów.
    Wyświetla plan sali, umożliwia wybór miejsc, obliczenie ceny i dokonanie rezerwacji.
    """

    # Sygnał emitowany po dokonaniu rezerwacji (może być użyty do odświeżenia listy rezerwacji w innym miejscu).
    reservation_made = pyqtSignal() 
    
    def __init__(self):
        """
        Inicjalizacja widoku rezerwacji.
        Konfiguruje układ i tworzy elementy GUI dla tej zakładki.
        """
        super().__init__() # Wywołuję konstruktor klasy nadrzędnej QWidget.
        
        self.database = Database() # Pobieram instancję bazy danych (Singleton).
        self.reservation_facade = ReservationFacade() # Tworzę instancję fasady rezerwacji.
        self.current_screening = None # Atrybut do przechowywania aktualnie wybranego seansu.
        self.selected_seats = [] # Lista wybranych miejsc przez użytkownika.
        
        self.layout = QVBoxLayout(self) # Tworzę główny pionowy układ dla tego widoku.
        
        self.screening_info_label = QLabel("Proszę wybrać seans z zakładki 'Seanse'.") # Etykieta wyświetlająca informacje o wybranym seansie.
        self.layout.addWidget(self.screening_info_label) # Dodaję etykietę do układu.
        
        self.seat_layout = QGridLayout() # Tworzę układ siatki dla planu sali.
        self.layout.addLayout(self.seat_layout) # Dodaję układ siatki do głównego układu.

        self.price_label = QLabel("Łączna cena: 0.00 zł") # Etykieta wyświetlająca łączną cenę rezerwacji.
        self.layout.addWidget(self.price_label) # Dodaję etykietę ceny do układu.

        self.ticket_type_combo = QComboBox() # Pole wyboru typu biletu.
        self.ticket_type_combo.addItem("Normalny") # Dodaję opcję "Normalny".
        self.ticket_type_combo.addItem("Ulgowy") # Dodaję opcję "Ulgowy".
        self.ticket_type_combo.addItem("VIP") # Dodaję opcję "VIP".
        # Podpinam sygnał currentIndexChanged do metody update_price.
        self.ticket_type_combo.currentIndexChanged.connect(self.update_price) 
        self.layout.addWidget(self.ticket_type_combo) # Dodaję pole wyboru do układu.
        
        self.reserve_button = QPushButton("Zarezerwuj") # Przycisk do dokonania rezerwacji.
        self.reserve_button.setEnabled(False) # Domyślnie przycisk jest wyłączony.
        # Podpinam sygnał clicked do metody make_reservation.
        self.reserve_button.clicked.connect(self.make_reservation) 
        self.layout.addWidget(self.reserve_button) # Dodaję przycisk do układu.

        self.layout.addStretch() # Dodaję rozciągliwy element na końcu układu.

    def set_screening(self, screening):
        """
        Ustawia aktualnie wybrany seans i odświeża widok planu sali.
        Wywoływana z innego widoku (np. ScreeningView) po wybraniu seansu.
        """
        self.current_screening = screening # Zapisuję wybrany obiekt seansu.
        if self.current_screening: # Sprawdzam, czy seans został pomyślnie ustawiony.
            self.screening_info_label.setText(f"Wybrany seans: {self.current_screening.movie.title} w {self.current_screening.cinema_hall.name} o {self.current_screening.date_time.strftime('%d.%m.%Y %H:%M')}") # Aktualizuję etykietę z informacjami o seansie.
            self.display_seat_layout() # Wyświetlam plan sali dla tego seansu.
            self.update_price() # Aktualizuję wyświetlaną cenę (powinna być 0 na początku).
            self.reserve_button.setEnabled(len(self.selected_seats) > 0) # Włączam przycisk rezerwacji tylko jeśli wybrano miejsca.
        else:
            self.screening_info_label.setText("Proszę wybrać seans z zakładki 'Seanse'.") # Resetuję tekst etykiety, jeśli seans nie został ustawiony.
            self.clear_seat_layout() # Czyszczę plan sali.
            self.selected_seats = [] # Czyszczę listę wybranych miejsc.
            self.update_price() # Aktualizuję cenę na 0.
            self.reserve_button.setEnabled(False) # Wyłączam przycisk rezerwacji.


    def display_seat_layout(self):
        """
        Wyświetla plan sali dla aktualnie wybranego seansu.
        Tworzy przyciski reprezentujące miejsca i dodaje je do układu siatki.
        """
        self.clear_seat_layout() # Najpierw czyszczę istniejący plan sali.

        if not self.current_screening: # Sprawdzam, czy seans jest wybrany.
            return # Jeśli nie, przerywam działanie metody.

        # Tworzę przyciski dla każdego miejsca w sali i dodaję je do siatki.
        for seat in self.current_screening.seats: # Iteruję przez wszystkie miejsca w seansie.
            seat_button = QPushButton(str(seat)) # Tworzę przycisk z tekstem reprezentującym miejsce (np. "R1M5").
            seat_button.setFixedSize(40, 40) # Ustawiam stały rozmiar przycisku.
            seat_button.setProperty("seat_obj", seat) # Zapisuję referencję do obiektu Seat jako właściwość przycisku.
            
            # Ustawiam styl przycisku w zależności od stanu miejsca.
            if seat.state.__class__.__name__ == "FreeSeatState":
                seat_button.setStyleSheet("background-color: lightgreen;") # Wolne miejsce - zielone tło.
                seat_button.clicked.connect(self.toggle_seat_selection) # Podpinam slot do wyboru/odznaczenia miejsca.
            elif seat.state.__class__.__name__ == "ReservedSeatState":
                 seat_button.setStyleSheet("background-color: yellow;") # Zarezerwowane miejsce - żółte tło.
                 seat_button.setEnabled(False) # Wyłączam przycisk dla zarezerwowanych miejsc.
            elif seat.state.__class__.__name__ == "SoldSeatState":
                seat_button.setStyleSheet("background-color: red;") # Sprzedane miejsce - czerwone tło.
                seat_button.setEnabled(False) # Wyłączam przycisk dla sprzedanych miejsc.
            else:
                 seat_button.setStyleSheet("background-color: gray;") # Inny stan - szare tło (stan domyślny/nieznany).
                 seat_button.setEnabled(False) # Wyłączam przycisk.

            # Dodaję przycisk miejsca do układu siatki, używając numeru rzędu i miejsca jako koordynatów.
            # Używam (seat.row - 1) i (seat.number - 1), ponieważ QGridLayout używa indeksów od 0.
            self.seat_layout.addWidget(seat_button, seat.row - 1, seat.number - 1) 

        # Dodaję etykiety rzędów i miejsc do siatki dla lepszej czytelności.
        for row in range(self.current_screening.cinema_hall.rows): # Iteruję przez rzędy.
            row_label = QLabel(f"Rząd {row + 1}") # Tworzę etykietę rzędu.
            row_label.setAlignment(Qt.AlignCenter) # Wyrównuję tekst do środka.
            self.seat_layout.addWidget(row_label, row, self.current_screening.cinema_hall.seats_per_row) # Dodaję etykietę rzędu na końcu rzędu.
        
        for col in range(self.current_screening.cinema_hall.seats_per_row): # Iteruję przez kolumny (miejsca w rzędzie).
            col_label = QLabel(f"M {col + 1}") # Tworzę etykietę miejsca.
            col_label.setAlignment(Qt.AlignCenter) # Wyrównuję tekst do środka.
            self.seat_layout.addWidget(col_label, self.current_screening.cinema_hall.rows, col) # Dodaję etykietę miejsca na końcu kolumny.


    def clear_seat_layout(self):
        """
        Usuwa wszystkie elementy z układu siatki planu sali.
        Używane przed wyświetleniem nowego planu sali.
        """
        # Iteruję przez wszystkie elementy w układzie siatki.
        while self.seat_layout.count():
            item = self.seat_layout.takeAt(0) # Pobieram kolejny element z układu.
            widget = item.widget() # Pobieram widget z elementu (jeśli istnieje).
            if widget is not None: # Jeśli element jest widgetem.
                widget.deleteLater() # Usuwam widget.
            # Else: Element może być tylko układem (layout), w takim przypadku nie ma widgetu do usunięcia.

    def toggle_seat_selection(self):
        """
        Slot wywoływany po kliknięciu przycisku miejsca.
        Dodaje lub usuwa miejsce z listy wybranych miejsc i aktualizuje jego wygląd.
        """
        seat_button = self.sender() # Pobieram przycisk, który wywołał ten slot.
        seat = seat_button.property("seat_obj") # Pobieram obiekt Seat przypisany do przycisku.
        
        if seat in self.selected_seats: # Sprawdzam, czy miejsce jest już na liście wybranych.
            self.selected_seats.remove(seat) # Jeśli tak, usuwam je z listy.
            seat_button.setStyleSheet("background-color: lightgreen;") # Zmieniam kolor tła przycisku na zielony (wolne).
        else: # Jeśli miejsce nie jest na liście wybranych.
            self.selected_seats.append(seat) # Dodaję miejsce do listy wybranych.
            seat_button.setStyleSheet("background-color: blue;") # Zmieniam kolor tła przycisku na niebieski (wybrane).
        
        self.update_price() # Aktualizuję wyświetlaną łączną cenę po zmianie wybranych miejsc.
        self.reserve_button.setEnabled(len(self.selected_seats) > 0) # Włączam/wyłączam przycisk rezerwacji w zależności od liczby wybranych miejsc.

    def update_price(self):
        """
        Oblicza i aktualizuje wyświetlaną łączną cenę rezerwacji na podstawie wybranych miejsc i typu biletu.
        """
        if not self.current_screening or not self.selected_seats: # Sprawdzam, czy wybrano seans i miejsca.
            self.price_label.setText("Łączna cena: 0.00 zł") # Jeśli nie, ustawiam cenę na 0.
            return # Przerywam działanie metody.

        # Pobieram wybraną fabrykę biletów na podstawie wyboru w QComboBox.
        selected_ticket_type = self.ticket_type_combo.currentText() # Pobieram tekst wybranego typu biletu.
        if selected_ticket_type == "Normalny":
            ticket_factory = RegularTicketFactory() # Używam fabryki biletów normalnych.
        elif selected_ticket_type == "Ulgowy":
            ticket_factory = DiscountedTicketFactory() # Używam fabryki biletów ulgowych.
        elif selected_ticket_type == "VIP":
            ticket_factory = VIPTicketFactory() # Używam fabryki biletów VIP.
        else:
            # Domyślnie używam fabryki biletów normalnych, jeśli typ jest nieznany.
            ticket_factory = RegularTicketFactory() 

        # Obliczam łączną cenę rezerwacji, używając fasady.
        total_price, _ = self.reservation_facade.calculate_price(self.current_screening, self.selected_seats, ticket_factory)
        
        # Aktualizuję tekst etykiety ceny.
        self.price_label.setText(f"Łączna cena: {total_price:.2f} zł") # Wyświetlam obliczoną cenę z dwoma miejscami po przecinku.


    def make_reservation(self):
        """
        Dokonuje rezerwacji wybranych miejsc dla klienta.
        Wyświetla dialog do wprowadzenia imienia i nazwiska klienta, a następnie tworzy rezerwację.
        """
        if not self.current_screening or not self.selected_seats: # Sprawdzam, czy wybrano seans i miejsca.
            QMessageBox.warning(self, "Błąd", "Proszę wybrać seans i miejsca.") # Wyświetlam komunikat ostrzegawczy.
            return # Przerywam działanie metody.

        # Pobieram wybraną fabrykę biletów (tak samo jak w update_price).
        selected_ticket_type = self.ticket_type_combo.currentText()
        if selected_ticket_type == "Normalny":
            ticket_factory = RegularTicketFactory()
        elif selected_ticket_type == "Ulgowy":
            ticket_factory = DiscountedTicketFactory()
        elif selected_ticket_type == "VIP":
            ticket_factory = VIPTicketFactory()
        else:
            ticket_factory = RegularTicketFactory()

        # Obliczam cenę i generuję obiekty biletów.
        total_price, tickets = self.reservation_facade.calculate_price(self.current_screening, self.selected_seats, ticket_factory)

        # Wyświetlam dialog do wprowadzenia imienia i nazwiska klienta.
        customer_name, ok = QLineEdit.getText(self, "Potwierdzenie rezerwacji", "Imię i nazwisko:")
        
        if ok and customer_name: # Jeśli użytkownik kliknął OK i wprowadził imię i nazwisko.
            try:
                # Dokonuję rezerwacji, używając fasady.
                reservation = self.reservation_facade.make_reservation(customer_name, self.current_screening, self.selected_seats, tickets)
                
                QMessageBox.information(self, "Sukces", f"Rezerwacja dokonana:\n{reservation}") # Wyświetlam komunikat o sukcesie rezerwacji.
                
                # Po dokonaniu rezerwacji, odświeżam widok (np. plan sali) i czyszczę wybrane miejsca.
                self.selected_seats = [] # Czyszczę listę wybranych miejsc.
                self.display_seat_layout() # Odświeżam plan sali, aby miejsca były zaznaczone jako zarezerwowane.
                self.update_price() # Aktualizuję cenę na 0.
                self.reserve_button.setEnabled(False) # Wyłączam przycisk rezerwacji.
                self.reservation_made.emit() # Emituję sygnał informujący o dokonaniu rezerwacji.

            except Exception as e: # Obsługa błędów podczas rezerwacji.
                 QMessageBox.critical(self, "Błąd rezerwacji", f"Wystąpił błąd podczas rezerwacji: {e}") # Wyświetlam komunikat o błędzie.
        elif ok: # Jeśli użytkownik kliknął OK, ale nie wprowadził imienia i nazwiska.
             QMessageBox.warning(self, "Błąd", "Imię i nazwisko klienta nie może być puste.") # Wyświetlam komunikat ostrzegawczy.