from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox, QDialog, QLineEdit, QComboBox, QInputDialog, QDialogButtonBox, QFrame  # Używane klasy z QtWidgets do budowy GUI.
from PyQt5.QtCore import Qt, pyqtSignal  # Qt do flag, wyrównania i sygnałów.
from utils.database import Database  # Klasa Database jako repozytorium danych (Singleton).
from facades.reservation_facade import ReservationFacade  # Fasada do operacji rezerwacji.
from factories.ticket_factory import RegularTicketFactory, DiscountedTicketFactory, VIPTicketFactory  # Fabryki biletów (Normalny, Ulgowy, VIP).
from models.seat import Seat  # Klasa Seat reprezentuje pojedyncze miejsce w sali kinowej.

class ReservationView(QWidget):  # Główny widok rezerwacji biletów.
    """
    Widok do procesu rezerwacji biletów.
    Wyświetla plan sali, umożliwia wybór miejsc, obliczenie ceny i dokonanie rezerwacji.
    """

    reservation_made = pyqtSignal()  # Sygnał emitowany po dokonaniu rezerwacji.
    
    def __init__(self):
        """
        Inicjalizacja widoku rezerwacji.
        Konfiguruje układ i tworzy elementy GUI dla tej zakładki.
        """
        super().__init__()
        
        # Główny layout poziomy
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        # Lewa kolumna: pionowy layout
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout, stretch=1)

        self.database = Database()  # Instancja bazy danych (Singleton).
        self.reservation_facade = ReservationFacade()  # Fasada rezerwacji.
        self.current_screening = None  # Aktualnie wybrany seans.
        self.selected_seats = []  # Wybrane miejsca do rezerwacji.
        self.available_ticket_factories = {}  # Dostępne fabryki biletów dla seansu.
        
        self.screening_info_label = QLabel("Proszę wybrać seans z zakładki 'Seanse'.")  # Informacja o wyborze seansu.
        self.left_layout.addWidget(self.screening_info_label)
        
        self.seat_layout = QGridLayout()  # Siatka miejsc na sali.
        self.left_layout.addLayout(self.seat_layout)
 
        self.price_label = QLabel("Łączna cena: 0.00 zł")  # Wyświetlanie łącznej ceny.
        self.left_layout.addWidget(self.price_label)

        self.ticket_type_combo = QComboBox()  # Wybór typu biletu.
        self.ticket_type_combo.setMaximumWidth(150)
        self.ticket_type_combo.currentIndexChanged.connect(self.update_price)
        self.left_layout.addWidget(self.ticket_type_combo)

        self.reserve_button = QPushButton("Zarezerwuj")  # Przycisk rezerwacji.
        self.reserve_button.setMaximumWidth(150)
        self.reserve_button.setEnabled(False)
        self.reserve_button.clicked.connect(self.make_reservation)
        self.left_layout.addWidget(self.reserve_button)
        
        self.left_layout.addStretch()  # Rozciągliwy element na dole.

        # Prawa kolumna: legenda
        self.legend_layout = QVBoxLayout()
        self.legend_layout.addStretch()
        self.main_layout.addLayout(self.legend_layout)

        self.legend_widget = None

    def set_screening(self, screening):
        """
        Ustawia aktualnie wybrany seans i odświeża widok planu sali.
        """
        self.current_screening = screening
        if self.current_screening:
            self.screening_info_label.setText(
                f"Wybrany seans: {self.current_screening.movie.title} w {self.current_screening.cinema_hall.name} o {self.current_screening.date_time.strftime('%d.%m.%Y %H:%M')}"
            )
            # Ustawianie dostępnych typów biletów
            self.available_ticket_factories = self.reservation_facade.get_available_ticket_options(self.current_screening)
            self.ticket_type_combo.clear()
            if self.available_ticket_factories:
                for ticket_name in self.available_ticket_factories.keys():
                    self.ticket_type_combo.addItem(ticket_name)
                self.ticket_type_combo.setEnabled(True)
            else:
                self.ticket_type_combo.addItem("Brak dostępnych biletów")
                self.ticket_type_combo.setEnabled(False)

            self.display_seat_layout()
            self.update_price()
            self.reserve_button.setEnabled(len(self.selected_seats) > 0 and bool(self.available_ticket_factories))
        else:
            self.screening_info_label.setText("Proszę wybrać seans z zakładki 'Seanse'.")
            self.clear_seat_layout()
            self.selected_seats = []
            self.ticket_type_combo.clear()
            self.ticket_type_combo.setEnabled(False)
            self.available_ticket_factories = {}
            self.update_price()
            self.reserve_button.setEnabled(False)
 
    def display_seat_layout(self):
        """
        Wyświetla plan sali dla aktualnie wybranego seansu.
        Tworzy przyciski reprezentujące miejsca i dodaje je do układu siatki.
        """
        self.clear_seat_layout()

        # Legenda kolorów miejsc
        if self.legend_widget is not None:
            self.legend_layout.removeWidget(self.legend_widget)
            self.legend_widget.deleteLater()
            self.legend_widget = None

        legend_widget = QWidget()
        legend_vbox = QVBoxLayout(legend_widget)
        legend_vbox.setContentsMargins(20, 40, 20, 0)
        legend_vbox.setSpacing(20)

        # Wolne miejsce
        free_box = QFrame()
        free_box.setFixedSize(20, 20)
        free_box.setStyleSheet("background-color: lightgreen; border: 1px solid #888;")
        free_label = QLabel("Wolne")
        free_label.setStyleSheet("color: white;")
        row1 = QHBoxLayout()
        row1.addWidget(free_box)
        row1.addWidget(free_label)
        legend_vbox.addLayout(row1)

        # Zarezerwowane miejsce
        reserved_box = QFrame()
        reserved_box.setFixedSize(20, 20)
        reserved_box.setStyleSheet("background-color: orange; border: 1px solid #888;")
        reserved_label = QLabel("Zarezerwowane")
        reserved_label.setStyleSheet("color: white;")
        row2 = QHBoxLayout()
        row2.addWidget(reserved_box)
        row2.addWidget(reserved_label)
        legend_vbox.addLayout(row2)

        # Sprzedane miejsce
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

        if not self.current_screening:
            return

        # Tworzenie przycisków dla każdego miejsca
        for seat in self.current_screening.seats:
            seat_button = QPushButton(str(seat))
            seat_button.setFixedSize(40, 40)
            seat_button.setProperty("seat_obj", seat)
            
            # Stylowanie przycisku w zależności od stanu miejsca
            if seat.state.__class__.__name__ == "FreeSeatState":
                seat_button.setStyleSheet("background-color: lightgreen;")
                seat_button.clicked.connect(self.toggle_seat_selection)
            elif seat.state.__class__.__name__ == "ReservedSeatState":
                seat_button.setStyleSheet("background-color: orange;")
                seat_button.setEnabled(False)
            elif seat.state.__class__.__name__ == "SoldSeatState":
                seat_button.setStyleSheet("background-color: red;")
                seat_button.setEnabled(False)
            else:
                seat_button.setStyleSheet("background-color: gray;")
                seat_button.setEnabled(False)

            # Dodanie przycisku do siatki
            col_index = seat.number - 1
            self.seat_layout.addWidget(seat_button, seat.row - 1, col_index)
 
        # Etykiety rzędów
        for row in range(self.current_screening.cinema_hall.rows):
            row_label = QLabel(f"Rząd {row + 1}")
            row_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            row_label.setContentsMargins(10, 0, 0, 0)
            self.seat_layout.addWidget(row_label, row, self.current_screening.cinema_hall.seats_per_row)

        # Szerokość przerwy na środku
        middle = (self.current_screening.cinema_hall.seats_per_row // 2)-1
        self.seat_layout.setColumnMinimumWidth(middle, 60)

        # Etykiety miejsc
        max_seat_num = self.current_screening.cinema_hall.seats_per_row
        for seat_num_idx in range(max_seat_num):
            seat_num = seat_num_idx + 1
            col_label = QLabel(f"M{seat_num}")
            col_label.setAlignment(Qt.AlignCenter)
            col_index = seat_num_idx
            self.seat_layout.addWidget(col_label, self.current_screening.cinema_hall.rows, col_index)

    def clear_seat_layout(self):
        """
        Usuwa wszystkie elementy z układu siatki planu sali.
        """
        while self.seat_layout.count():
            item = self.seat_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        # Resetowanie szerokości kolumn
        for col in range(self.seat_layout.columnCount()):
            self.seat_layout.setColumnMinimumWidth(col, 0)
            
    def toggle_seat_selection(self):
        """
        Obsługa kliknięcia przycisku miejsca.
        Dodaje lub usuwa miejsce z listy wybranych i aktualizuje jego wygląd.
        """
        seat_button = self.sender()
        seat = seat_button.property("seat_obj")
        
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
            seat_button.setStyleSheet("background-color: lightgreen;")
        else:
            self.selected_seats.append(seat)
            seat_button.setStyleSheet("background-color: blue;")
        
        self.update_price()
        self.reserve_button.setEnabled(len(self.selected_seats) > 0)

    def update_price(self):
        """
        Oblicza i aktualizuje wyświetlaną łączną cenę rezerwacji na podstawie wybranych miejsc i typu biletu.
        """
        if not self.current_screening or not self.selected_seats:
            self.price_label.setText("Łączna cena: 0.00 zł")
            return

        selected_ticket_name = self.ticket_type_combo.currentText()
        
        if not selected_ticket_name or not self.available_ticket_factories:
            self.price_label.setText("Łączna cena: 0.00 zł")
            return

        ticket_factory = self.available_ticket_factories.get(selected_ticket_name)

        if not ticket_factory:
            self.price_label.setText("Łączna cena: 0.00 zł")
            QMessageBox.warning(self, "Błąd", "Nie można znaleźć fabryki dla wybranego typu biletu.")
            return

        total_price, _ = self.reservation_facade.calculate_price(self.current_screening, self.selected_seats, ticket_factory)
        self.price_label.setText(f"Łączna cena: {total_price:.2f} zł")

    def make_reservation(self):
        """
        Dokonuje rezerwacji wybranych miejsc dla klienta.
        Wyświetla dialog do wprowadzenia imienia i nazwiska klienta, a następnie tworzy rezerwację.
        """
        if not self.current_screening or not self.selected_seats:
            QMessageBox.warning(self, "Błąd", "Proszę wybrać seans i miejsca.")
            return

        selected_ticket_name = self.ticket_type_combo.currentText()

        if not selected_ticket_name or not self.available_ticket_factories:
            QMessageBox.warning(self, "Błąd", "Proszę wybrać typ biletu.")
            return

        ticket_factory = self.available_ticket_factories.get(selected_ticket_name)

        if not ticket_factory:
            QMessageBox.warning(self, "Błąd", f"Nieprawidłowy typ biletu: {selected_ticket_name}. Proszę wybrać poprawny typ biletu.")
            return
        
        total_price, tickets = self.reservation_facade.calculate_price(self.current_screening, self.selected_seats, ticket_factory)

        # Dialog do wprowadzenia imienia i nazwiska klienta
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Potwierdzenie rezerwacji")
        dialog.setLabelText("Imię i nazwisko:")
        dialog.setTextValue("")
        dialog.setMinimumWidth(300)
        dialog.setStyleSheet("""
            QInputDialog {
                background-color: #f0f0f0;
            }
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #cccccc;
                padding: 5px;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                color: white;
                background-color: #007bff;
                border: 1px solid #007bff;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
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
                            color: black;
                            font-size: 12pt;
                        }
                        QMessageBox {
                            background-color: white;
                        }
                        QPushButton {
                            color: white;
                            background-color: #007bff;
                            border: 1px solid #007bff;
                            padding: 5px 10px;
                            border-radius: 3px;
                        }
                        QPushButton:hover {
                            background-color: #0056b3;
                        }
                        QPushButton:pressed {
                            background-color: #004085;
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
            # Jeśli użytkownik anulował podsumowanie, nie robimy nic dalej.

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
        summary_label.setWordWrap(True)
        layout.addWidget(summary_label)

        # Przyciski potwierdzenia/anulowania
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
                font-size: 10pt;
            }
            QPushButton {
                color: white;
                background-color: #007bff;
                border: 1px solid #007bff;
                padding: 8px 15px;
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
            summary_lines.append(f"  Rząd {row} {label}: {numbers_str}")
        return "\n".join(summary_lines)