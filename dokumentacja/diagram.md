classDiagram
    direction BT

    class Movie {
        +String title
        +int duration_minutes
        +int age_category
    }

    class CinemaHall {
        +String name
        +int rows
        +int seats_per_row
        +int get_total_seats()
    }

    class Seat {
        +int row
        +int number
        +SeatState state
        +void reserve()
        +void cancel()
        +void sell()
        +bool is_available()
    }

    class SeatState {
        <<abstract>>
        +void reserve(seat)
        +void cancel(seat)
        +void sell(seat)
        +bool is_available()
    }

    class FreeSeatState
    class ReservedSeatState
    class SoldSeatState

    Seat --|> SeatSubject
    SeatState <|-- FreeSeatState
    SeatState <|-- ReservedSeatState
    SeatState <|-- SoldSeatState
    Seat "1" *-- "1" SeatState : aggregates

    class Screening {
        +Movie movie
        +CinemaHall cinema_hall
        +DateTime date_time
        +float base_price
        +List~Seat~ seats
        +List~Seat~ get_available_seats()
    }

    Screening "1" *-- "1" Movie : aggregates
    Screening "1" *-- "1" CinemaHall : aggregates
    Screening "1" *-- "*" Seat : aggregates

    class Ticket {
        +Screening screening
        +Seat seat
        +float price
    }

    class RegularTicket
    class DiscountedTicket
    class VIPTicket

    Ticket <|-- RegularTicket
    Ticket <|-- DiscountedTicket
    Ticket <|-- VIPTicket

    TicketDecorator --|> Ticket
    TicketDecorator "1" *-- "1" Ticket : decorates

    class ThreeDTicketDecorator
    class SnackComboTicketDecorator

    TicketDecorator <|-- ThreeDTicketDecorator
    TicketDecorator <|-- SnackComboTicketDecorator


    class Reservation {
        +String id
        +String customer_name
        +Screening screening
        +List~Seat~ seats
        +List~Ticket~ tickets
        +DateTime timestamp
        +float total_price
    }

    Reservation "1" *-- "1" Screening : aggregates
    Reservation "1" *-- "*" Seat : aggregates
    Reservation "1" *-- "*" Ticket : aggregates


    class Database {
        <<Singleton>>
        +List~Movie~ movies
        +List~CinemaHall~ cinema_halls
        +List~Screening~ screenings
        +List~Reservation~ reservations
        +void add_movie(movie)
        +void add_cinema_hall(hall)
        +void add_screening(screening)
        +void add_reservation(reservation)
        +List~Movie~ get_movies()
        +List~CinemaHall~ get_cinema_halls()
        +List~Screening~ get_screenings()
        +List~Reservation~ get_reservations()
        +List~Screening~ get_screenings_for_date(date)
        +void save_reservations(filepath)
        +void load_reservations(filepath)
    }

    Database -- ReservationFacade : uses >


    class TicketFactory {
        <<abstract>>
        +create_ticket(screening, seat) Ticket
    }

    class RegularTicketFactory
    class DiscountedTicketFactory
    class VIPTicketFactory

    TicketFactory <|-- RegularTicketFactory
    TicketFactory <|-- DiscountedTicketFactory
    TicketFactory <|-- VIPTicketFactory

    ReservationFacade -- TicketFactory : uses >


    class ScreeningBuilder {
        +Screening build()
    }

    ScreeningBuilder -- Screening : creates >


    class ReservationFacade {
        +get_available_screenings(date)
        +get_available_seats(screening)
        +calculate_price(screening, seats, factory) float
        +make_reservation(name, screening, seats, tickets) Reservation
    }


    class SeatObserver {
        <<abstract>>
        +update(seat)
    }

    class SeatView

    SeatObserver <|-- SeatView

    class SeatSubject {
        +attach(observer)
        +detach(observer)
        +notify()
    }

    SeatSubject "1" -- "*" SeatObserver : notifies >


    class PricingStrategy {
        <<abstract>>
        +calculate_price(base_price) float
    }

    class RegularPricingStrategy
    class WeekendPricingStrategy
    class MorningPricingStrategy

    PricingStrategy <|-- RegularPricingStrategy
    PricingStrategy <|-- WeekendPricingStrategy
    PricingStrategy <|-- MorningPricingStrategy

    class PricingContext {
        +set_strategy(strategy)
        +calculate_price(base_price) float
    }

    PricingContext "1" *-- "1" PricingStrategy : aggregates

    Screening -- PricingContext : uses >


    class BackDrop {
        +draw(painter)
    }

    class BackDropWrapper {
        +enable_shine_animation(...)
        +enable_move_animation(...)
    }

    BackDropWrapper "1" *-- "1" BackDrop : aggregates


    class MovieView
    class ScreeningView
    class ReservationView

    MainWindow -- BackDropWrapper : uses >
    MainWindow -- MovieView : uses >
    MainWindow -- ScreeningView : uses >
    MainWindow -- ReservationView : uses >