# Система Аэропорт (Airport System)

**Сводка по проекту:**  
- Всего классов: **50**  
- Всего полей (атрибутов классов с аннотациями типов): **154**  
- Всего уникальных поведений (методов классов): **104**  
- Всего примеров ассоциаций между классами (поля/параметры/типы результата с другими классами): **33**  
- Всего персональных пользовательских исключений (наследников `AirportError`): **12**  


Проект моделирует: пассажиров, персонал, самолёты, рейсы, терминалы и гейты, билеты и бронирования, платежи и транзакции, безопасность, багаж и расписание.



## Конфигурация и точка входа

### `airport_system.config.AppConfig`

**Поля:**
- `airport_name: str` — название аэропорта.
- `timezone: str` — часовой пояс.
- `default_currency: str` — валюта по умолчанию.
- `support_email: str` — e-mail службы поддержки.
- `max_baggage_weight: float` — лимит веса багажа на пассажира.

**Методы:**
- `default() -> AppConfig` — создаёт конфигурацию по умолчанию.
- `baggage_limit_kg() -> float` — возвращает лимит багажа.

**Ассоциации:**
- Используется в `airport_system.main.main` для конфигурирования приложения.

### `airport_system.main.main`

Пример сценария: создаёт конфигурацию, инициализирует репозиторий и сервис рейсов, добавляет самолёт и рейс, обновляет статус и выводит список запланированных рейсов.

## Domain-слой: предметные модели

### Модуль `domain.enums`

### `domain.enums.BaggageStatus`
_Наследуется от_: Enum

**Поля:** — нет аннотированных полей

**Методы:** — нет методов

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.enums.BookingStatus`
_Наследуется от_: Enum

**Поля:** — нет аннотированных полей

**Методы:** — нет методов

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.enums.EmployeeRole`
_Наследуется от_: Enum

**Поля:** — нет аннотированных полей

**Методы:** — нет методов

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.enums.FlightStatus`
_Наследуется от_: Enum

**Поля:** — нет аннотированных полей

**Методы:** — нет методов

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.enums.PaymentStatus`
_Наследуется от_: Enum

**Поля:** — нет аннотированных полей

**Методы:** — нет методов

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.enums.SeatClass`
_Наследуется от_: Enum

**Поля:** — нет аннотированных полей

**Методы:** — нет методов

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.enums.SecurityLevel`
_Наследуется от_: Enum

**Поля:** — нет аннотированных полей

**Методы:** — нет методов

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### Модуль `domain.passenger`

### `domain.passenger.ContactInfo`

**Поля:**
- `email: str`
- `phone: str`
- `address: str`
- `emergency_phone: Optional`

**Методы:**
- `is_email_valid()`
- `has_emergency_contact()`
- `masked_email()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.passenger.LoyaltyAccount`

**Поля:**
- `number: str`
- `points: int`
- `tier: str`
- `status_expiry: Optional`

**Методы:**
- `add_points()`
- `redeem_points()`
- `_recalculate_tier()`
- `will_expire_within()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.passenger.Passenger`

**Поля:**
- `passenger_id: str`
- `name: str`
- `contact: ContactInfo`
- `loyalty: Optional`
- `is_vip: bool`
- `security_cleared: bool`
- `notes: List`
- `passport_number: str`
- `nationality: str`
- `date_of_birth: Optional`
- `password_hash: str`

**Методы:**
- `link_loyalty()`
- `add_note()`
- `mark_security_cleared()`
- `can_board()`
- `update_contact()`
- `set_password()`
- `verify_password()`
- `age()`

**Ассоциации с другими классами:**
- параметр `account`: `LoyaltyAccount`
- параметр `new_contact`: `ContactInfo`
- поле `contact` → `ContactInfo`

### Модуль `domain.employee`

### `domain.employee.CabinCrew`
_Наследуется от_: Employee

**Поля:**
- `languages_spoken: int`

**Методы:**
- `can_serve_language()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.employee.Employee`

**Поля:**
- `employee_id: str`
- `name: str`
- `role: EmployeeRole`
- `active: bool`
- `username: str`
- `password_hash: str`

**Методы:**
- `deactivate()`
- `activate()`
- `can_access_high_security()`
- `set_password()`
- `verify_password()`
- `is_active_staff()`

**Ассоциации с другими классами:**
- поле `role` → `EmployeeRole`

### `domain.employee.GroundStaff`
_Наследуется от_: Employee

**Поля:**
- `station: Optional`

**Методы:**
- `assign_station()`
- `is_assigned()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.employee.Pilot`
_Наследуется от_: Employee

**Поля:**
- `license_number: str`
- `flight_hours: int`

**Методы:**
- `add_flight_hours()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### Модуль `domain.aircraft`

### `domain.aircraft.Aircraft`

**Поля:**
- `registration: str`
- `model: str`
- `seats: List`
- `flight_hours: int`
- `manufacturer: str`
- `range_km: int`
- `in_service: bool`

**Методы:**
- `add_seat()`
- `available_seats()`
- `add_flight_hours()`
- `retire()`
- `is_long_haul()`

**Ассоциации с другими классами:**
- параметр `seat`: `Seat`

### `domain.aircraft.Seat`

**Поля:**
- `seat_number: str`
- `seat_class: SeatClass`
- `is_available: bool`
- `is_exit_row: bool`

**Методы:**
- `reserve()`
- `release()`
- `is_premium()`

**Ассоциации с другими классами:**
- поле `seat_class` → `SeatClass`

### Модуль `domain.terminal`

### `domain.terminal.BoardingPass`

**Поля:**
- `boarding_pass_id: str`
- `booking_id: str`
- `passenger_name: str`
- `gate_id: str`
- `seat_number: str`

**Методы:**
- `change_gate()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.terminal.Gate`

**Поля:**
- `gate_id: str`
- `terminal_code: str`
- `is_open: bool`
- `current_flight_id: Optional`
- `supports_international: bool`

**Методы:**
- `assign_flight()`
- `clear_flight()`
- `close()`
- `open()`
- `is_free()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.terminal.Terminal`

**Поля:**
- `code: str`
- `gates: List`
- `name: str`
- `security_level: SecurityLevel`

**Методы:**
- `add_gate()`
- `find_free_gate()`
- `is_international_terminal()`
- `available_gates_count()`

**Ассоциации с другими классами:**
- параметр `gate`: `Gate`
- поле `security_level` → `SecurityLevel`

### Модуль `domain.ticket`

### `domain.ticket.Ticket`

**Поля:**
- `ticket_id: str`
- `passenger_id: str`
- `flight_id: str`
- `seat_number: str`
- `seat_class: SeatClass`
- `base_price: float`
- `checked_in: bool`
- `fare_basis: str`
- `booking_class: str`
- `refundable: bool`

**Методы:**
- `mark_checked_in()`
- `calculate_price_with_tax()`
- `is_upgradeable()`
- `can_refund()`

**Ассоциации с другими классами:**
- поле `seat_class` → `SeatClass`

### Модуль `domain.flight`

### `domain.flight.Flight`

**Поля:**
- `flight_id: str`
- `origin: str`
- `destination: str`
- `departure_time: datetime`
- `arrival_time: datetime`
- `aircraft: Aircraft`
- `status: FlightStatus`
- `gate_id: Optional`
- `terminal_code: Optional`
- `distance_km: int`

**Методы:**
- `delay()`
- `depart()`
- `arrive()`
- `assign_gate()`
- `flight_duration_hours()`

**Ассоциации с другими классами:**
- поле `aircraft` → `Aircraft`
- поле `status` → `FlightStatus`

### Модуль `domain.booking`

### `domain.booking.Booking`

**Поля:**
- `booking_id: str`
- `passenger_id: str`
- `flight_id: str`
- `status: BookingStatus`
- `ticket_ids: List`
- `payment_ids: List`
- `created_at: datetime`
- `updated_at: datetime`
- `refundable: bool`

**Методы:**
- `confirm()`
- `cancel()`
- `add_ticket()`
- `add_payment()`
- `mark_checked_in()`
- `is_refundable()`
- `has_payments()`
- `touch()`

**Ассоциации с другими классами:**
- поле `status` → `BookingStatus`

### Модуль `domain.payment`

### `domain.payment.CardPayment`

**Поля:**
- `card_number: str`
- `holder_name: str`
- `expiration: str`
- `billing_address: str`

**Методы:**
- `authorize()`
- `masked_number()`

**Ассоциации с другими классами:**
- параметр `amount`: `Money`

### `domain.payment.Money`

**Поля:**
- `amount: float`
- `currency: str`
- `precision: int`

**Методы:**
- `allocate()`
- `add()`
- `subtract()`
- `percentage()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### `domain.payment.Payment`

**Поля:**
- `payment_id: str`
- `booking_id: str`
- `amount: Money`
- `status: PaymentStatus`
- `provider: str`
- `metadata: Dict`

**Методы:**
- `mark_completed()`
- `mark_declined()`
- `mark_refunded()`
- `is_successful()`
- `add_metadata()`

**Ассоциации с другими классами:**
- поле `amount` → `Money`
- поле `status` → `PaymentStatus`

### `domain.payment.PaymentMethod`
_Наследуется от_: Protocol

**Поля:** — нет аннотированных полей

**Методы:**
- `authorize()`

**Ассоциации с другими классами:**
- параметр `amount`: `Money`

### Модуль `domain.security`

### `domain.security.AccessBadge`

**Поля:**
- `badge_id: str`
- `owner_id: str`
- `level: SecurityLevel`
- `revoked: bool`

**Методы:**
- `upgrade()`
- `revoke()`
- `is_active()`

**Ассоциации с другими классами:**
- параметр `new_level`: `SecurityLevel`
- поле `level` → `SecurityLevel`

### `domain.security.SecurityCheckpoint`

**Поля:**
- `checkpoint_id: str`
- `required_level: SecurityLevel`
- `name: str`

**Методы:**
- `can_pass()`
- `describe()`

**Ассоциации с другими классами:**
- параметр `badge`: `AccessBadge`
- поле `required_level` → `SecurityLevel`

### Модуль `domain.baggage`

### `domain.baggage.BaggageItem`

**Поля:**
- `tag: BaggageTag`
- `weight_kg: float`
- `status: BaggageStatus`
- `location: Optional`
- `length_cm: int`
- `width_cm: int`
- `height_cm: int`
- `owner_id: str`

**Методы:**
- `check_in()`
- `mark_loaded()`
- `mark_lost()`
- `volume_liters()`
- `is_oversized()`

**Ассоциации с другими классами:**
- поле `status` → `BaggageStatus`
- поле `tag` → `BaggageTag`

### `domain.baggage.BaggageTag`

**Поля:**
- `tag_id: str`
- `booking_id: str`
- `priority: bool`

**Методы:** — нет методов

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### Модуль `domain.schedule`

### `domain.schedule.AirportSchedule`

**Поля:**
- `days: Dict`

**Методы:**
- `add_flight()`
- `flights_on()`
- `total_flights()`
- `remove_flight()`

**Ассоциации с другими классами:**
- параметр `flight`: `Flight`

### `domain.schedule.DailySchedule`

**Поля:**
- `day: date`
- `flights: List`
- `notes: str`

**Методы:**
- `add_flight()`
- `flights_from()`
- `flights_to()`

**Ассоциации с другими классами:**
- параметр `flight`: `Flight`

### Модуль `domain.statistics`

### `domain.statistics.AirportStatistics`

**Поля:**
- `year: int`
- `total_passengers: int`
- `total_flights: int`
- `total_cargo_tons: float`
- `avg_delay_minutes: float`
- `cancelled_flights: int`
- `diverted_flights: int`
- `on_time_flights: int`
- `international_flights: int`
- `domestic_flights: int`
- `security_incidents: int`
- `lost_baggage_items: int`
- `handled_baggage_items: int`
- `vip_passengers: int`
- `loyalty_gold: int`
- `loyalty_platinum: int`
- `checkin_counters: int`
- `security_checkpoints: int`
- `terminals: int`
- `gates: int`
- `runways: int`
- `max_daily_flights: int`
- `max_daily_passengers: int`
- `avg_load_factor: float`
- `fuel_consumption_tons: float`

**Методы:**
- `on_time_percents()`
- `baggage_loss_rate()`
- `average_passengers_per_flight()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

## Пользовательские исключения

Все пользовательские исключения наследуются от базового класса `exceptions.base.AirportError`.

### Базовый класс

- `exceptions.base.AirportError` — базовый класс для всех доменных исключений.

### Специализированные исключения (12 штук)

#### Модуль `exceptions.booking_exceptions`
- `exceptions.booking_exceptions.BookingAlreadyPaidError` — наследник `AirportError`.
- `exceptions.booking_exceptions.BookingNotFoundError` — наследник `AirportError`.
- `exceptions.booking_exceptions.SeatUnavailableError` — наследник `AirportError`.

#### Модуль `exceptions.payment_exceptions`
- `exceptions.payment_exceptions.CurrencyMismatchError` — наследник `AirportError`.
- `exceptions.payment_exceptions.InsufficientFundsError` — наследник `AirportError`.
- `exceptions.payment_exceptions.PaymentDeclinedError` — наследник `AirportError`.

#### Модуль `exceptions.security_exceptions`
- `exceptions.security_exceptions.AccessDeniedError` — наследник `AirportError`.
- `exceptions.security_exceptions.InvalidBadgeError` — наследник `AirportError`.

#### Модуль `exceptions.baggage_exceptions`
- `exceptions.baggage_exceptions.BaggageNotFoundError` — наследник `AirportError`.
- `exceptions.baggage_exceptions.OverweightBaggageError` — наследник `AirportError`.

#### Модуль `exceptions.flight_exceptions`
- `exceptions.flight_exceptions.FlightAlreadyDepartedError` — наследник `AirportError`.
- `exceptions.flight_exceptions.FlightNotFoundError` — наследник `AirportError`.

## Репозитории (слой доступа к данным)

### Модуль `repositories.base`

### `repositories.base.InMemoryRepository`

**Поля:**
- `_items: Dict`

**Методы:**
- `add()`
- `get()`
- `remove()`
- `all()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

### Модуль `repositories.booking_repository`

### `repositories.booking_repository.BookingRepository`

**Поля:** — нет аннотированных полей

**Методы:**
- `find_by_passenger()`
- `get_required()`

**Ассоциации с другими классами:**
- тип результата `Booking`

### Модуль `repositories.flight_repository`

### `repositories.flight_repository.FlightRepository`

**Поля:** — нет аннотированных полей

**Методы:**
- `find_active()`
- `find_by_route()`

**Ассоциации с другими классами:** — нет явных ассоциаций по типам

## Сервисы (бизнес-логика)

### Модуль `services.booking_service`

### `services.booking_service.BookingService`

**Поля:**
- `bookings: BookingRepository`

**Методы:**
- `create_booking()`
- `confirm_booking()`
- `mark_paid()`
- `cancel_booking()`
- `get_bookings_for_passenger()`

**Ассоциации с другими классами:**
- поле `bookings` → `BookingRepository`
- тип результата `Booking`

### Модуль `services.payment_service`

### `services.payment_service.PaymentService`

**Поля:**
- `currency: str`

**Методы:**
- `charge_card()`
- `refund_payment()`
- `split_payment()`
- `transfer_between_cards()`

**Ассоциации с другими классами:**
- параметр `amount`: `Money`
- параметр `card`: `CardPayment`
- параметр `from_card`: `CardPayment`
- параметр `payment`: `Payment`
- параметр `to_card`: `CardPayment`
- параметр `total`: `Money`
- тип результата `Payment`

### Модуль `services.baggage_service`

### `services.baggage_service.BaggageService`

**Поля:**
- `max_weight_kg: float`
- `_items: Dict`

**Методы:**
- `check_in_baggage()`
- `load_to_aircraft()`
- `mark_lost()`
- `count_by_status()`
- `total_weight()`
- `find_by_booking()`

**Ассоциации с другими классами:**
- параметр `status`: `BaggageStatus`
- тип результата `BaggageItem`

### Модуль `services.security_service`

### `services.security_service.SecurityService`

**Поля:** — нет аннотированных полей

**Методы:**
- `pass_checkpoint()`
- `upgrade_badge()`

**Ассоциации с другими классами:**
- параметр `badge`: `AccessBadge`
- параметр `checkpoint`: `SecurityCheckpoint`
- тип результата `AccessBadge`

### Модуль `services.flight_service`

### `services.flight_service.FlightService`

**Поля:**
- `flights: FlightRepository`

**Методы:**
- `schedule_flight()`
- `update_status()`
- `upcoming_flights()`
- `cancel_flight()`
- `find_by_route()`

**Ассоциации с другими классами:**
- параметр `flight`: `Flight`
- параметр `status`: `FlightStatus`
- поле `flights` → `FlightRepository`
- тип результата `Flight`

## Утилиты

### `utils.time_utils`
- `now_utc() -> datetime` — текущее время в UTC.
- `to_iso(dt: datetime) -> str` — перевод даты/времени в ISO-строку (UTC).

### `utils.validation`
- `ensure_not_empty(value: str, field_name: str) -> None` — проверка, что строка не пустая.
- `ensure_positive(number: float, field_name: str) -> None` — проверка, что число положительное.

### `utils.id_generator`
- `next_id(prefix: str) -> str` — генерация последовательных строковых ID с заданным префиксом.

## Тесты и покрытие

Тесты в папке `tests/` покрывают:
- положительные сценарии работы сервисов (создание и подтверждение бронирования, оплата, возвраты, обработка багажа, проход через безопасность, управление рейсами);
- негативные сценарии с выбросом пользовательских исключений (`BookingNotFoundError`, `PaymentDeclinedError`, `OverweightBaggageError`, `AccessDeniedError`, `FlightNotFoundError` и др.);
- базовые сценарии для доменных моделей (`Passenger`, `LoyaltyAccount`, `Aircraft`, `Seat`, `Booking`, `BaggageItem`, `Flight`, `Terminal`, `AccessBadge`, `AirportSchedule`).

### Запуск проекта

```bash
cd airport_system_project
python -m airport_system.main
```

### Запуск тестов с измерением покрытия

```bash
pip install pytest pytest-cov
pytest --cov=airport_system
```
