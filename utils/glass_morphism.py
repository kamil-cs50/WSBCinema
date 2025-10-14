from PyQt5 import QtWidgets, QtGui, QtCore  # Importuję niezbędne moduły z biblioteki PyQt5 do tworzenia elementów graficznego interfejsu użytkownika.

class BackDrop(QtWidgets.QGraphicsEffect):
    """
    Efekt graficzny glassmorphism - implementacja efektu szkła.
    Klasa BackDrop dziedziczy po QGraphicsEffect i pozwala na zastosowanie efektów graficznych, takich jak rozmycie i przezroczystość, do widgetów.
    """
    
    def __init__(self, blur=0, radius=0, backgrounds=None):
        """
        Inicjalizacja obiektu efektu.
        Konstruktor przyjmuje parametry konfiguracyjne efektu glassmorphism: blur (rozmycie), radius (promień zaokrąglenia rogów) oraz listę słowników backgrounds definiujących tła.
        """
        super().__init__()  # Wywołuję konstruktor klasy nadrzędnej QGraphicsEffect.
        self.blur = blur  # Zapisuję wartość rozmycia. Większa wartość oznacza mocniejsze rozmycie.
        self.radius = radius  # Zapisuję promień zaokrąglenia rogów. Pozwala na zaokrąglenie krawędzi widgetu.
        self.backgrounds = backgrounds or []  # Zapisuję listę konfiguracji tła lub pustą listę, jeśli backgrounds nie zostało podane.
    
    def draw(self, painter):
        """
        Metoda rysująca efekt szkła na widgetcie.
        Ta metoda jest wywoływana przez system graficzny Qt, gdy widget z tym efektem wymaga odświeżenia.
        """
        # Pobieram źródłową mapę pikseli (pixmap) widgetu, na który aplikowany jest efekt. To jest oryginalna zawartość widgetu.
        source_pixmap = self.sourcePixmap()
        
        # Dodaję sprawdzenie typu source_pixmap. Jeśli nie jest QPixmap, nie aplikuję efektu.
        if not isinstance(source_pixmap, QtGui.QPixmap) or source_pixmap.isNull():
             # Jeśli source_pixmap nie jest QPixmap lub jest nullem, nie rysujemy niczego w tej metodzie,
             # ponieważ efekt nie może być zastosowany. Zwracamy kontrolę.
             # Usunięto: painter.drawPixmap(0, 0, self.sourcePixmap()) - powodowało TypeError.
             return # Kończę działanie metody draw.

        # Kontynuujemy tylko jeśli source_pixmap jest prawidłowym QPixmap.
        painter.save() # Zapisuję bieżący stan malarza (painter), aby móc go później przywrócić.
        # Ustawiam podpowiedzi renderowania dla malarza: Antialiasing (wygładzanie krawędzi) i SmoothPixmapTransform (lepsze skalowanie pixmap).
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        
        # Rysuję tła zdefiniowane w liście backgrounds. Każdy element na liście to słownik z konfiguracją tła.
        for bg in self.backgrounds:
            # Ustawiam przezroczystość malarza, jeśli w konfiguracji tła podano wartość 'opacity'.
            if "opacity" in bg:
                painter.setOpacity(bg["opacity"])
            
            # Tworzę ścieżkę rysowania (QPainterPath) w kształcie zaokrąglonego prostokąta.
            path = QtGui.QPainterPath()
            path.addRoundedRect(
                QtCore.QRectF(0, 0, source_pixmap.width(), source_pixmap.height()), # Używam szerokości i wysokości QPixmap
                self.radius, self.radius
            )
            
            # Ustawiam kolor tła i wypełniam ścieżkę, jeśli w konfiguracji podano 'background-color'.
            if "background-color" in bg:
                painter.fillPath(path, bg["background-color"])
            
            # Rysuję obramowanie, jeśli w konfiguracji podano 'border' i 'border-width'.
            if "border" in bg and "border-width" in bg:
                pen = QtGui.QPen(bg["border"])  # Tworzę obiekt pióra (QPen) z kolorem obramowania.
                pen.setWidth(bg["border-width"])  # Ustawiam szerokość pióra (grubość obramowania).
                painter.setPen(pen)  # Ustawiam pióro dla malarza.
                painter.drawPath(path)  # Rysuję ścieżkę (obramowanie).
        
        # Aplikuję efekt rozmycia do źródłowej pixmapy, jeśli wartość blur jest większa od 0.
        if self.blur > 0:
            blur_effect = QtWidgets.QGraphicsBlurEffect()  # Tworzę obiekt efektu rozmycia (QGraphicsBlurEffect).
            blur_effect.setBlurRadius(self.blur)  # Ustawiam promień rozmycia efektu.
            blur_pixmap = QtGui.QPixmap(source_pixmap)  # Tworzę nową pixmapę na podstawie źródłowej.
            blur_painter = QtGui.QPainter(blur_pixmap)  # Tworzę malarza do rysowania na nowej pixmapie.
            # Rysuję efekt rozmycia na nowej pixmapie.
            blur_effect.draw(blur_painter)
            blur_painter.end()  # Kończę rysowanie na pixmapie.
            painter.drawPixmap(0, 0, blur_pixmap)  # Rysuję rozmytą pixmapę na docelowym malarzu.
        else:
            # Jeśli blur wynosi 0, rysuję oryginalną pixmapę bez rozmycia.
            painter.drawPixmap(0, 0, source_pixmap)
        
        painter.restore()  # Przywracam poprzedni stan malarza.
    
    def setBlurRadius(self, radius):
        """Setter dla promienia rozmycia."""
        self.blur = radius
        self.update() # Aktualizuje efekt graficzny

    def setBorderRadius(self, radius):
        """Setter dla promienia zaokrąglenia rogów."""
        self.radius = radius
        self.update() # Aktualizuje efekt graficzny

class BackDropWrapper(QtWidgets.QWidget):
    """
    Wrapper dla widgetów do łatwego stosowania efektu glassmorphism z animacjami.
    Ta klasa opakowuje inny widget i dodaje do niego efekt glassmorphism oraz opcjonalne animacje przy najechaniu myszą.
    """
    
    def __init__(self, widget, blur=0, radius=0, backgrounds=None, shine_animation=None, move_animation=None):
        """
        Inicjalizacja obiektu wrappera.
        Konstruktor przyjmuje widget do opakowania oraz parametry konfiguracyjne efektu glassmorphism i animacji.
        """
        super().__init__()  # Wywołuję konstruktor klasy nadrzędnej QWidget.
        self.widget = widget  # Zapisuję referencję do widgetu, który będzie opakowany.
        
        # Ustawiam układ dla wrappera. QVBoxLayout umieści opakowany widget.
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0) # Ustawiam marginesy układu na 0.
        layout.addWidget(widget) # Dodaję opakowany widget do układu.
        
        # Ustawiam efekt tła glassmorphism na opakowanym widgetcie.
        self.backdrop = BackDrop(blur, radius, backgrounds) # Tworzę instancję efektu BackDrop z podanymi parametrami.
        self.widget.setGraphicsEffect(self.backdrop) # Aplikuję efekt graficzny do opakowanego widgetu.
        
        # Inicjalizuję atrybuty związane z animacjami.
        self.shine_animation = None # Atrybut dla animacji błysku.
        self.move_animation = None # Atrybut dla animacji ruchu.
        self.original_pos = self.widget.pos() # Zapisuję oryginalną pozycję widgetu.

        # Włączam animację błysku, jeśli parametry shine_animation zostały podane.
        if shine_animation:
            self.enable_shine_animation(*shine_animation) # Wywołuję metodę enable_shine_animation z rozpakowanymi argumentami.
        
        # Włączam animację ruchu, jeśli parametry move_animation zostały podane.
        if move_animation:
            self.enable_move_animation(*move_animation) # Wywołuję metodę enable_move_animation z rozpakowanymi argumentami.


    def enable_shine_animation(self, duration=500, forward=True, angle=45, width=150, color=None):
        """
        Włącza animację błysku przy najechaniu myszą (uproszczona implementacja).
        Ta metoda konfiguruje i aktywuje animację błysku, która powinna pojawić się, gdy kursor myszy wejdzie na widget.
        """
        if color is None:
            # Ustawiam domyślny kolor błysku na półprzezroczysty biały, jeśli kolor nie został podany.
            color = QtGui.QColor(255, 255, 255, 90)
        
        # Zapisuję parametry konfiguracji animacji błysku.
        self.shine_animation = {
            'duration': duration, # Czas trwania animacji w milisekundach.
            'forward': forward, # Kierunek animacji (True dla przód, False dla tył).
            'angle': angle, # Kąt błysku.
            'width': width, # Szerokość błysku.
            'color': color # Kolor błysku.
        }
        
        # Podpinam niestandardowe metody do zdarzeń wejścia i wyjścia myszy na widget.
        # Używam setattr, aby uniknąć potencjalnego nadpisywania innych event handlerów,
        # chociaż w prostej aplikacji lambda jest wystarczająca.
        original_enter_event = getattr(self.widget, 'enterEvent', None)
        original_leave_event = getattr(self.widget, 'leaveEvent', None)

        def enterEvent(event):
            if original_enter_event:
                original_enter_event(event)
            self._start_shine_animation()
            if self.move_animation: # Uruchamiamy animację ruchu tylko jeśli jest włączona
                self._start_move_animation()

        def leaveEvent(event):
            if original_leave_event:
                original_leave_event(event)
            self._stop_shine_animation()
            if self.move_animation: # Zatrzymujemy animację ruchu tylko jeśli jest włączona
                 self._stop_move_animation()

        self.widget.enterEvent = enterEvent
        self.widget.leaveEvent = leaveEvent
    
    def enable_move_animation(self, duration=300, offset=(0, -10), forward=True):
        """
        Włącza animację ruchu przy najechaniu myszą.
        Ta metoda konfiguruje i aktywuje animację ruchu, która powinna pojawić się, gdy kursor myszy wejdzie na widget.
        """
        # Zapisuję parametry konfiguracji animacji ruchu.
        self.move_animation = {
            'duration': duration, # Czas trwania animacji w milisekundach.
            'offset': offset, # Przesunięcie widgetu w pikselach (x, y).
            'forward': forward # Kierunek animacji (True dla przód, False dla tył).
        }
        
        # Podpinam niestandardowe metody do zdarzeń wejścia i wyjścia myszy na widget,
        # upewniając się, że nie nadpisujemy handlerów błysku.
        original_enter_event = getattr(self.widget, 'enterEvent', None)
        original_leave_event = getattr(self.widget, 'leaveEvent', None)

        def enterEvent(event):
            if original_enter_event:
                 original_enter_event(event)
            self._start_move_animation()
            if self.shine_animation: # Uruchamiamy animację błysku tylko jeśli jest włączona
                self._start_shine_animation()


        def leaveEvent(event):
            if original_leave_event:
                original_leave_event(event)
            self._stop_move_animation()
            if self.shine_animation: # Zatrzymujemy animację błysku tylko jeśli jest włączona
                self._stop_shine_animation()

        self.widget.enterEvent = enterEvent
        self.widget.leaveEvent = leaveEvent
    
    def _start_shine_animation(self):
        """
        Rozpoczyna animację błysku (uproszczona implementacja).
        Ta metoda uruchamia prostą animację zmieniającą przezroczystość tła przy najechaniu myszą.
        """
        if not self.shine_animation: # Sprawdzam czy animacja błysku jest włączona.
            return # Jeśli nie, kończę działanie metody.

        # Tworzę animację właściwości 'opacity' efektu graficznego.
        # Zatrzymuję poprzednią animację, jeśli istnieje.
        if hasattr(self, 'shine_property_animation_reverse') and self.shine_property_animation_reverse.state() == QtCore.QPropertyAnimation.Running:
            self.shine_property_animation_reverse.stop()
        if hasattr(self, 'shine_property_animation') and self.shine_property_animation.state() == QtCore.QPropertyAnimation.Running:
            self.shine_property_animation.stop() # Zatrzymuję istniejącą animację do przodu

        self.shine_property_animation = QtCore.QPropertyAnimation(self.backdrop, b'opacity', self)
        self.shine_property_animation.setDuration(self.shine_animation['duration']) # Ustawiam czas trwania animacji.
        self.shine_property_animation.setStartValue(self.backdrop.opacity()) # Ustawiam wartość początkową na aktualną przezroczystość.
        self.shine_property_animation.setEndValue(self.shine_animation['color'].alphaF()) # Ustawiam wartość końcową na przezroczystość z koloru błysku.
        self.shine_property_animation.start() # Uruchamiam animację.

    def _stop_shine_animation(self):
        """
        Zatrzymuje animację błysku (uproszczona implementacja).
        Ta metoda zatrzymuje animację błysku i przywraca oryginalną przezroczystość.
        """
        if not self.shine_animation: # Sprawdzam czy animacja błysku jest włączona.
            return # Jeśli nie, kończę działanie metody.

        # Zatrzymuję poprzednią animację, jeśli istnieje.
        if hasattr(self, 'shine_property_animation') and self.shine_property_animation.state() == QtCore.QPropertyAnimation.Running:
             self.shine_property_animation.stop()
        if hasattr(self, 'shine_property_animation_reverse') and self.shine_property_animation_reverse.state() == QtCore.QPropertyAnimation.Running:
            self.shine_property_animation_reverse.stop() # Zatrzymuję istniejącą animację powrotną

        # Tworzę animację powrotu przezzroczystości do wartości początkowej.
        self.shine_property_animation_reverse = QtCore.QPropertyAnimation(self.backdrop, b'opacity', self)
        self.shine_property_animation_reverse.setDuration(self.shine_animation['duration']) # Ustawiam czas trwania.
        self.shine_property_animation_reverse.setStartValue(self.backdrop.opacity()) # Ustawiam wartość początkową na aktualną przezroczystość.
        # Ustawiam wartość końcową na przezroczystość tła z listy backgrounds (jeśli istnieje, w przeciwnym razie domyślnie 1.0).
        original_opacity = self.backdrop.backgrounds[0].get("opacity", 1.0) if self.backdrop.backgrounds else 1.0
        self.shine_property_animation_reverse.setEndValue(original_opacity)
        self.shine_property_animation_reverse.start() # Uruchamiam animację powrotną.

    def _start_move_animation(self):
        """
        Rozpoczyna animację ruchu.
        Ta metoda uruchamia animację przesunięcia widgetu przy najechaniu myszą.
        """
        if not self.move_animation: # Sprawdzam czy animacja ruchu jest włączona.
            return # Jeśli nie, kończę działanie metody.

        # Zatrzymuję poprzednią animację, jeśli istnieje.
        if hasattr(self, 'move_property_animation_reverse') and self.move_property_animation_reverse.state() == QtCore.QPropertyAnimation.Running:
            self.move_property_animation_reverse.stop()
        if hasattr(self, 'move_property_animation') and self.move_property_animation.state() == QtCore.QPropertyAnimation.Running:
            self.move_property_animation.stop() # Zatrzymuję istniejącą animację do przodu

        # Tworzę animację właściwości 'pos' (pozycja) widgetu.
        self.move_property_animation = QtCore.QPropertyAnimation(self.widget, b'pos', self)
        self.move_property_animation.setDuration(self.move_animation['duration']) # Ustawiam czas trwania animacji.
        self.move_property_animation.setStartValue(self.widget.pos()) # Ustawiam wartość początkową na aktualną pozycję widgetu.
        # Obliczam wartość końcową dodając offset ruchu do oryginalnej pozycji.
        end_pos = self.original_pos + QtCore.QPoint(self.move_animation['offset'][0], self.move_animation['offset'][1])
        self.move_property_animation.setEndValue(end_pos) # Ustawiam wartość końcową.
        self.move_property_animation.start() # Uruchamiam animację.


    def _stop_move_animation(self):
        """
        Zatrzymuje animację ruchu.
        Ta metoda zatrzymuje animację ruchu i przywraca oryginalną pozycję widgetu.
        """
        if not self.move_animation: # Sprawdzam czy animacja ruchu jest włączona.
            return # Jeśli nie, kończę działanie metody.

        # Zatrzymuję poprzednią animację, jeśli istnieje.
        if hasattr(self, 'move_property_animation') and self.move_property_animation.state() == QtCore.QPropertyAnimation.Running:
            self.move_property_animation.stop()
        if hasattr(self, 'move_property_animation_reverse') and self.move_property_animation_reverse.state() == QtCore.QPropertyAnimation.Running:
             self.move_property_animation_reverse.stop() # Zatrzymuję istniejącą animację powrotną

        # Tworzę animację powrotu do oryginalnej pozycji.
        self.move_property_animation_reverse = QtCore.QPropertyAnimation(self.widget, b'pos', self)
        self.move_property_animation_reverse.setDuration(self.move_animation['duration']) # Ustawiam czas trwania.
        self.move_property_animation_reverse.setStartValue(self.widget.pos()) # Ustawiam wartość początkową na aktualną pozycję.
        self.move_property_animation_reverse.setEndValue(self.original_pos) # Ustawiam wartość końcową na oryginalną pozycję zapisaną przy inicjalizacji.
        self.move_property_animation_reverse.start() # Uruchamiam animację powrotną.
