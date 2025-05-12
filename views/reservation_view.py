from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox, QDialog, QLineEdit, QComboBox, QInputDialog # Importuję niezbędne klasy z modułu QtWidgets do tworzenia elementów GUI, takich jak widget bazowy (QWidget), układy (QVBoxLayout, QGridLayout), etykiety (QLabel), przyciski (QPushButton), okna dialogowe (QMessageBox, QDialog, QInputDialog), pola tekstowe (QLineEdit) i listy rozwijane (QComboBox). Dodano import QInputDialog dla okna dialogowego pobierającego dane tekstowe.
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
        
        self.database = Database() # Pobieram instancję bazy danych (Singleton) poprzez wywołanie klasy Database().
        self.reservation_facade = ReservationFacade() # Tworzę instancję fasady rezerwacji (ReservationFacade). Będę jej używał do wykonywania operacji na rezerwacjach.
        self.current_screening = None # Inicjalizuję atrybut self.current_screening na None. Będzie on przechowywał obiekt seansu, który aktualnie jest wybrany do rezerwacji.
        self.selected_seats = [] # Inicjalizuję pustą listę self.selected_seats. Będzie ona przechowywać obiekty Seat wybrane przez użytkownika do rezerwacji.
        
        self.layout = QVBoxLayout(self) # Tworzę główny pionowy układ (QVBoxLayout) dla tego widoku i ustawiam go jako layout dla bieżącego widgetu (self).
        
        self.screening_info_label = QLabel("Proszę wybrać seans z zakładki 'Seanse'.") # Tworzę instancję QLabel (etykieta) wyświetlającą początkowy komunikat informujący o konieczności wyboru seansu.
        self.layout.addWidget(self.screening_info_label) # Dodaję utworzoną etykietę do głównego pionowego układu.
        
        self.seat_layout = QGridLayout() # Tworzę układ siatki (QGridLayout) dla planu sali kinowej. Przyciski miejsc zostaną dodane do tego layoutu.
        self.layout.addLayout(self.seat_layout) # Dodaję utworzony układ siatki do głównego pionowego układu.
 
        self.price_label = QLabel("Łączna cena: 0.00 zł") # Tworzę etykietę wyświetlającą łączną cenę rezerwacji, początkowo ustawioną na 0.00 zł.
        self.layout.addWidget(self.price_label) # Dodaję etykietę ceny do głównego pionowego układu.

        self.ticket_type_combo = QComboBox() # Tworzę instancję QComboBox (lista rozwijana) do wyboru typu biletu.
        self.ticket_type_combo.addItem("Normalny") # Dodaję opcję "Normalny" do listy rozwijanej.
        self.ticket_type_combo.addItem("Ulgowy") # Dodaję opcję "Ulgowy" do listy rozwijanej.
        self.ticket_type_combo.addItem("VIP") # Dodaję opcję "VIP" do listy rozwijanej.
        self.ticket_type_combo.currentIndexChanged.connect(self.update_price) # Podpinam sygnał 'currentIndexChanged' (zmiana wybranego elementu w liście rozwijanej) do metody self.update_price. Oznacza to, że metoda update_price zostanie wywołana za każdym razem, gdy użytkownik zmieni typ biletu.
        self.layout.addWidget(self.ticket_type_combo) # Dodaję utworzoną listę rozwijaną do głównego pionowego układu.
        
        self.reserve_button = QPushButton("Zarezerwuj") # Tworzę instancję QPushButton (przycisk) z tekstem "Zarezerwuj".
        self.reserve_button.setEnabled(False) # Domyślnie wyłączam przycisk rezerwacji. Będzie aktywny tylko wtedy, gdy wybrano seans i miejsca.
        self.reserve_button.clicked.connect(self.make_reservation) # Podpinam sygnał 'clicked' przycisku do metody self.make_reservation. Oznacza to, że metoda make_reservation zostanie wywołana, gdy przycisk zostanie kliknięty.
        self.layout.addWidget(self.reserve_button) # Dodaję utworzony przycisk do głównego pionowego układu.
        
        self.layout.addStretch() # Dodaję rozciągliwy element (stretch) na końcu głównego układu pionowego. Powoduje to, że elementy powyżej są wyrównane do góry.

    def set_screening(self, screening): # Definiuję metodę set_screening, która jest slotem wywoływanym z innego widoku (np. ScreeningView) w celu ustawienia aktualnie wybranego seansu.
        """
        Ustawia aktualnie wybrany seans i odświeża widok planu sali. # Docstring opisujący metodę.
        Wywoływana z innego widoku (np. ScreeningView) po wybraniu seansu. # Wskazuje na sposób użycia metody.
        """
        self.current_screening = screening # Przypisuję przekazany obiekt seansu do atrybutu self.current_screening.
        if self.current_screening: # Sprawdzam warunek: jeśli atrybut self.current_screening nie jest None (czyli seans został pomyślnie ustawiony).
            self.screening_info_label.setText(f"Wybrany seans: {self.current_screening.movie.title} w {self.current_screening.cinema_hall.name} o {self.current_screening.date_time.strftime('%d.%m.%Y %H:%M')}") # Aktualizuję tekst etykiety informacyjnej o seansie, wyświetlając tytuł filmu, nazwę sali oraz sformatowaną datę i godzinę seansu.
            self.display_seat_layout() # Wywołuję metodę display_seat_layout, aby wyświetlić plan sali kinowej dla wybranego seansu.
            self.update_price() # Wywołuję metodę update_price, aby zaktualizować wyświetlaną łączną cenę (powinna być 0 na początku dla nowego seansu).
            self.reserve_button.setEnabled(len(self.selected_seats) > 0) # Ustawiam stan (aktywny/nieaktywny) przycisku rezerwacji w zależności od tego, czy lista wybranych miejsc (self.selected_seats) jest pusta.
        else: # Jeśli atrybut self.current_screening jest None (czyli seans nie został ustawiony lub został zresetowany).
            self.screening_info_label.setText("Proszę wybrać seans z zakładki 'Seanse'.") # Resetuję tekst etykiety informacyjnej do początkowego komunikatu.
            self.clear_seat_layout() # Wywołuję metodę clear_seat_layout, aby usunąć wszystkie elementy z planu sali.
            self.selected_seats = [] # Czyszczę listę wybranych miejsc.
            self.update_price() # Wywołuję metodę update_price, aby zaktualizować wyświetlaną cenę na 0.00 zł.
            self.reserve_button.setEnabled(False) # Wyłączam przycisk rezerwacji.
 

    def display_seat_layout(self): # Definiuję metodę display_seat_layout, która tworzy i wyświetla graficzną reprezentację planu sali kinowej.
        """
        Wyświetla plan sali dla aktualnie wybranego seansu. # Docstring opisujący metodę.
        Tworzy przyciski reprezentujące miejsca i dodaje je do układu siatki. # Opisuje działanie metody.
        """
        self.clear_seat_layout() # Najpierw wywołuję metodę clear_seat_layout, aby usunąć wszystkie istniejące przyciski miejsc z układu siatki przed wyświetleniem nowego planu sali.

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
                 seat_button.setStyleSheet("background-color: yellow;") # Jeśli miejsce jest zarezerwowane, ustawiam kolor tła przycisku na żółty.
                 seat_button.setEnabled(False) # Wyłączam przycisk dla zarezerwowanych miejsc, aby nie można ich było wybrać.
            elif seat.state.__class__.__name__ == "SoldSeatState": # Sprawdzam, czy aktualny stan miejsca jest instancją klasy SoldSeatState (sprzedane).
                seat_button.setStyleSheet("background-color: red;") # Jeśli miejsce jest sprzedane, ustawiam kolor tła przycisku na czerwony.
                seat_button.setEnabled(False) # Wyłączam przycisk dla sprzedanych miejsc.
            else: # Jeśli stan miejsca jest inny niż wolne, zarezerwowane lub sprzedane (np. nieznany stan).
                 seat_button.setStyleSheet("background-color: gray;") # Ustawiam kolor tła przycisku na szary.
                 seat_button.setEnabled(False) # Wyłączam przycisk dla nieznanych stanów.

            # Dodaję przycisk miejsca do układu siatki, używając numeru rzędu i miejsca jako koordynatów.
            # Używam (seat.row - 1) i (seat.number - 1), ponieważ QGridLayout używa indeksów od 0.
<<<<<<< HEAD
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
        middle = self.current_screening.cinema_hall.rows // 2 # Calculate middle column index
        self.seat_layout.setColumnMinimumWidth(int(middle), 60) # Set minimum width for the gap column

        # Dodaję etykiety miejsc do siatki dla lepszej czytelności.
        max_seat_num = self.current_screening.cinema_hall.seats_per_row
        for seat_num_idx in range(max_seat_num):  # Iterate using 0-based index
            seat_num = seat_num_idx + 1 # Actual seat number (1-based)
            col_label = QLabel(f"M {seat_num}")  # Create label e.g., "M 7"
            col_label.setAlignment(Qt.AlignCenter)  # Center align label text

            # Place label in its natural column index
            col_index = seat_num_idx # 0-based index
            self.seat_layout.addWidget(col_label, self.current_screening.cinema_hall.rows, col_index)  # Add label at its original column index
=======
            self.seat_layout.addWidget(seat_button, seat.row - 1, seat.number - 1) # Dodaję utworzony przycisk miejsca (seat_button) do układu siatki (self.seat_layout) w pozycji określonej przez numer rzędu i numer miejsca (z uwzględnieniem indeksowania od 0).
 
        # Dodaję etykiety rzędów i miejsc do siatki dla lepszej czytelności.
        for row in range(self.current_screening.cinema_hall.rows): # Rozpoczynam pętlę, która iteruje przez liczbę rzędów w sali kinowej aktualnie wybranego seansu.
            row_label = QLabel(f"Rząd {row + 1}") # Tworzę instancję QLabel (etykieta) z tekstem "Rząd X", gdzie X to numer rzędu (row + 1, ponieważ rzędy są numerowane od 1).
            row_label.setAlignment(Qt.AlignCenter) # Wyrównuję tekst etykiety rzędu do środka.
            self.seat_layout.addWidget(row_label, row, self.current_screening.cinema_hall.seats_per_row) # Dodaję utworzoną etykietę rzędu do układu siatki w odpowiednim rzędzie (row) i kolumnie poza ostatnim miejscem w rzędzie (self.current_screening.cinema_hall.seats_per_row).
        
        for col in range(self.current_screening.cinema_hall.seats_per_row): # Rozpoczynam pętlę, która iteruje przez liczbę miejsc w rzędzie w sali kinowej aktualnie wybranego seansu.
            col_label = QLabel(f"M {col + 1}") # Tworzę instancję QLabel (etykieta) z tekstem "M X", gdzie X to numer miejsca w rzędzie (col + 1, ponieważ miejsca są numerowane od 1).
            col_label.setAlignment(Qt.AlignCenter) # Wyrównuję tekst etykiety miejsca do środka.
            self.seat_layout.addWidget(col_label, self.current_screening.cinema_hall.rows, col) # Dodaję utworzoną etykietę miejsca do układu siatki w rzędzie poniżej ostatniego rzędu (self.current_screening.cinema_hall.rows) i odpowiedniej kolumnie (col).
>>>>>>> 9a55c3f4adcd73157f37c8ec4be29a59581bd2f8

 
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
<<<<<<< HEAD
        
        # Resetuj minimalną szerokość kolumn (usuwa padding dodany dla środkowej przerwy)
        for col in range(self.seat_layout.columnCount()):
            self.seat_layout.setColumnMinimumWidth(col, 0)
            
=======
>>>>>>> 9a55c3f4adcd73157f37c8ec4be29a59581bd2f8

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

        # Pobieram wybraną fabrykę biletów na podstawie wyboru w QComboBox.
        selected_ticket_type = self.ticket_type_combo.currentText() # Pobieram aktualnie wybrany tekst z listy rozwijanej typu biletu (self.ticket_type_combo).
        if selected_ticket_type == "Normalny": # Sprawdzam, czy wybrany typ biletu to "Normalny".
            ticket_factory = RegularTicketFactory() # Jeśli tak, tworzę instancję fabryki biletów normalnych.
        elif selected_ticket_type == "Ulgowy": # Sprawdzam, czy wybrany typ biletu to "Ulgowy".
            ticket_factory = DiscountedTicketFactory() # Jeśli tak, tworzę instancję fabryki biletów ulgowych.
        elif selected_ticket_type == "VIP": # Sprawdzam, czy wybrany typ biletu to "VIP".
            ticket_factory = VIPTicketFactory() # Jeśli tak, tworzę instancję fabryki biletów VIP.
        else: # Jeśli wybrany typ biletu jest inny niż "Normalny", "Ulgowy" lub "VIP" (przypadek awaryjny).
            # Domyślnie używam fabryki biletów normalnych, jeśli typ jest nieznany.
            ticket_factory = RegularTicketFactory() # Domyślnie tworzę instancję fabryki biletów normalnych.

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
        selected_ticket_type = self.ticket_type_combo.currentText() # Pobieram aktualnie wybrany tekst z listy rozwijanej typu biletu.
        if selected_ticket_type == "Normalny": # Sprawdzam typ biletu.
            ticket_factory = RegularTicketFactory() # Tworzę odpowiednią fabrykę.
        elif selected_ticket_type == "Ulgowy": # Sprawdzam typ biletu.
            ticket_factory = DiscountedTicketFactory() # Tworzę odpowiednią fabrykę.
        elif selected_ticket_type == "VIP": # Sprawdzam typ biletu.
            ticket_factory = VIPTicketFactory() # Tworzę odpowiednią fabrykę.
        else: # Przypadek awaryjny.
            ticket_factory = RegularTicketFactory() # Domyślna fabryka.

        # Obliczam cenę i generuję obiekty biletów.
        # Wywołuję metodę calculate_price na instancji fasady rezerwacji, aby uzyskać łączną cenę i listę obiektów biletów dla wybranych miejsc i typu biletu.
        total_price, tickets = self.reservation_facade.calculate_price(self.current_screening, self.selected_seats, ticket_factory)

        # Wyświetlam dialog do wprowadzenia imienia i nazwiska klienta.
        # Używam statycznej metody getText z QInputDialog, aby wyświetlić proste okno dialogowe z polem tekstowym. Poprawiono z QLineEdit na QInputDialog.
        customer_name, ok = QInputDialog.getText(self, "Potwierdzenie rezerwacji", "Imię i nazwisko:")
        
        if ok and customer_name: # Sprawdzam warunek: jeśli użytkownik kliknął przycisk OK (ok jest True) ORAZ wprowadził tekst w polu imienia i nazwiska (customer_name nie jest pusty).
            try: # Rozpoczynam blok try-except do obsługi potencjalnych błędów podczas dokonywania rezerwacji.
                # Dokonuję rezerwacji, używając fasady.
                # Wywołuję metodę make_reservation na instancji fasady rezerwacji, przekazując imię klienta, wybrany seans, listę wybranych miejsc i listę obiektów biletów.
                # Metoda ta tworzy i zapisuje obiekt rezerwacji.
                reservation = self.reservation_facade.make_reservation(customer_name, self.current_screening, self.selected_seats, tickets)
                
                QMessageBox.information(self, "Sukces", f"Rezerwacja dokonana:\n{reservation}") # Wyświetlam okno dialogowe z komunikatem informacyjnym o sukcesie rezerwacji, wyświetlając tekstową reprezentację utworzonej rezerwacji.
                
                # Po dokonaniu rezerwacji, odświeżam widok (np. plan sali) i czyszczę wybrane miejsca.
                self.selected_seats = [] # Czyszczę listę wybranych miejsc.
                self.display_seat_layout() # Wywołuję metodę display_seat_layout, aby odświeżyć widok planu sali. Miejsca, które zostały właśnie zarezerwowane, powinny teraz być wyświetlane jako zarezerwowane (np. na żółto, w zależności od implementacji stanu miejsca i jego reprezentacji graficznej).
                self.update_price() # Wywołuję metodę update_price, aby zaktualizować wyświetlaną cenę na 0.00 zł.
                self.reserve_button.setEnabled(False) # Wyłączam przycisk rezerwacji, ponieważ lista wybranych miejsc jest teraz pusta.
                self.reservation_made.emit() # Emituję sygnał reservation_made, informując inne części aplikacji (jeśli są podłączone) o dokonaniu rezerwacji.
 
            except Exception as e: # Blok except: jeśli wystąpił jakikolwiek błąd (Exception) podczas wykonywania kodu w bloku try.
                 QMessageBox.critical(self, "Błąd rezerwacji", f"Wystąpił błąd podczas rezerwacji: {e}") # Wyświetlam okno dialogowe z krytycznym komunikatem o błędzie, zawierającym opis błędu (e).
        elif ok: # Sprawdzam warunek: jeśli użytkownik kliknął przycisk OK (ok jest True), ale pole imienia i nazwiska było puste.
             QMessageBox.warning(self, "Błąd", "Imię i nazwisko klienta nie może być puste.") # Wyświetlam okno dialogowe z komunikatem ostrzegawczym, informującym, że imię i nazwisko klienta nie może być puste.