# Document Flow Management System

## Статистика проекта

- **Всего классов:** 78 (включая 11 протоколов/базовых классов, 54 бизнес-класса, 13 исключений)
- **Всего полей:** 174
- **Всего методов (уникальных поведений):** 149
- **Классов-исключений:** 13
- **Ассоциаций между классами:** 91+

## Описание

Система управления документооборотом с поддержкой:
- Управление пользователями и ролями (включая ролевые классы: Admin, Manager, Accountant, RegularUser, Guest)
- Работа с документами и их версионирование
- Маршруты согласования документов
- Система безопасности и аутентификации
- Платежные операции
- Хранение и архивирование документов

## Ролевая система пользователей

Система включает специализированные классы пользователей с предопределёнными правами:

### Admin (Администратор)
Полный доступ к системе:
- Создание, редактирование, удаление документов
- Согласование документов
- Управление пользователями и ролями
- Просмотр аудит-логов
- Управление системными настройками

### Manager (Менеджер)
Управление документами и командой:
- Создание и редактирование документов
- Согласование документов
- Просмотр документов команды
- Управление бюджетом команды

### Accountant (Бухгалтер)
Работа с финансовыми документами:
- Создание счетов
- Просмотр платежей
- Обработка платежей
- Просмотр финансовых документов
- Аудит транзакций

### RegularUser (Обычный пользователь)
Базовые операции с документами:
- Создание документов
- Редактирование своих документов
- Просмотр документов

### Guest (Гость)
Только чтение:
- Просмотр документов

---

## Модули системы

### Модуль: `cli.py`

#### `DemoContext`

**Поля:**

- `repo: InMemoryDocumentRepository`
- `storage: DocumentStorage`
- `doc_service: DocumentService`
- `appr_service: ApprovalService`
- `pay_service: PaymentService`
- `auth: AuthService`

---

### Модуль: `core.py`

#### `BaseEntity`

**Поля:**

- `created_at: datetime`
- `updated_at: datetime`

**Методы:**

- `touch()`

---

#### `IdentifiableMixin`

**Поля:**

- `id: str`

**Методы:**

- `identity()`

---

#### `TimestampMixin`

**Поля:**

- `created_at: datetime`
- `updated_at: datetime`

---

#### `Validatable`

**Методы:**

- `validate()`

---

#### `Approvable`

**Методы:**

- `approve()`

---

#### `Signable`

**Методы:**

- `sign(user_id)`

---

#### `Storable`

**Методы:**

- `store()`

---

#### `NotifierProtocol`

**Методы:**

- `notify(message)`

---

#### `PaymentProcessorProtocol`

**Методы:**

- `transfer(src_account, dst_account, amount)`

---

#### `DocumentLike`

**Поля:**

- `number: str`
- `title: str`

**Методы:**

- `validate()`

---

#### `DocumentRepositoryProtocol`

**Методы:**

- `save(doc)`
- `get(number)`
- `exists(number)`
- `search(query)`

---

### Модуль: `documents.py`

#### `DocumentMetadata`

**Поля:**

- `tags: List[str]`
- `attributes: Dict[str, str]`

**Методы:**

- `add_tag(tag)`: Add a tag to metadata
- `remove_tag(tag)`: Remove a tag from metadata
- `has_tag(tag)`: Check if metadata has a specific tag

---

#### `DocumentAttachment`

**Поля:**

- `filename: str`
- `content_type: str`
- `size: int`
- `checksum: str`

**Методы:**

- `is_image()`: Check if attachment is an image
- `is_pdf()`: Check if attachment is a PDF
- `get_extension()`: Get file extension

---

#### `DocumentVersion`

**Поля:**

- `number: int`
- `content: str`
- `created_at: datetime`
- `author_id: str`
- `comment: str`

**Методы:**

- `get_content_length()`: Get content length
- `is_latest(total_versions)`: Check if this is the latest version

---

#### `Signature`

**Поля:**

- `user_id: str`
- `certificate_id: str`
- `signed_at: datetime`

**Методы:**

- `is_valid_for(user_id)`: Check if signature belongs to user

---

#### `DigitalCertificate`

**Поля:**

- `id: str`
- `subject: str`
- `valid_from: datetime`
- `valid_to: datetime`
- `issuer: str`

**Методы:**

- `is_valid(moment)`
- `days_until_expiry()`: Get days until certificate expires
- `is_expiring_soon(days)`: Check if certificate is expiring within specified days

---

#### `DocumentHistoryRecord`

**Поля:**

- `event: str`
- `actor_id: str`
- `occurred_at: datetime`
- `details: str`

**Методы:**

- `get_event_type()`: Get event type

---

#### `DocumentLock`

**Поля:**

- `owner_id: str`
- `acquired_at: datetime`

**Методы:**

- `get_lock_duration()`: Get lock duration in seconds

---

#### `Document`

**Поля:**

- `id: str`
- `number: str`
- `title: str`
- `author: User`
- `organization: Organization | None`
- `department: Department | None`
- `status: str`
- `versions: List[DocumentVersion]`
- `attachments: List[DocumentAttachment]`
- `approval_route: ApprovalRoute | None`
- `metadata: DocumentMetadata`
- `signatures: List[Signature]`

**Методы:**

- `validate()`
- `add_version(content, author_id)`
- `add_attachment(attachment)`
- `lock(user_id)`
- `unlock(user_id)`
- `approve()`
- `sign(user_id)`
- `archive()`
- `restore()`

---

#### `IncomingDocument`

**Поля:**

- `sender: str`

**Методы:**

- `approve()`

---

#### `OutgoingDocument`

**Поля:**

- `recipient: str`

**Методы:**

- `approve()`

---

#### `ContractDocument`

**Поля:**

- `effective_from: datetime | None`
- `effective_to: datetime | None`
- `total_amount: int`

**Методы:**

- `validate()`

---

#### `InvoiceDocument`

**Поля:**

- `amount_due: int`
- `due_date: datetime | None`
- `paid: bool`

**Методы:**

- `mark_paid()`

---

#### `OrderDocument`

**Поля:**

- `items: List[str]`

---

#### `DocumentRegistry`

**Поля:**

- `numbers: set[str]`

**Методы:**

- `register(number)`
- `contains(number)`
- `unregister(number)`: Unregister a document number
- `count()`: Count registered numbers

---

### Модуль: `exceptions.py`

#### `DocumentFlowError` (Базовое исключение)

Базовое исключение для всех ошибок системы документооборота.

---

#### `DocumentNotFoundError` (Исключение)

Возникает когда документ не найден в системе. Содержит ID документа в сообщении об ошибке.

---

#### `InvalidDocumentStatusError` (Исключение)

Возникает при попытке выполнить операцию с документом в неверном статусе.

---

#### `AccessDeniedError` (Исключение)

Возникает когда у пользователя нет прав на выполнение операции.

---

#### `ApprovalStepError` (Исключение)

Возникает при ошибке в процессе согласования документа.

---

#### `InvalidSignatureError` (Исключение)

Возникает когда цифровая подпись документа невалидна или отсутствует.

---

#### `UserBlockedError` (Исключение)

Возникает при попытке выполнить операции заблокированным пользователем. Содержит ID пользователя.

---

#### `VersionConflictError` (Исключение)

Возникает при конфликте версий документа (например, при попытке редактирования заблокированного документа).

---

#### `RouteNotFoundError` (Исключение)

Возникает когда маршрут согласования не найден. Содержит ID маршрута.

---

#### `PaymentOperationError` (Исключение)

Возникает при ошибке платежной операции (недостаточно средств, заморожен счет и т.д.).

---

#### `AuthFailedError` (Исключение)

Возникает при неудачной попытке аутентификации пользователя.

---

#### `DuplicateDocumentError` (Исключение)

Возникает при попытке зарегистрировать документ с дублирующимся номером.

---

#### `StorageLimitExceededError` (Исключение)

Возникает когда превышена квота хранилища.

---

### Модуль: `payments.py`

#### `Currency`

---

#### `Account`

**Поля:**

- `number: str`
- `currency: str`
- `balance: int`
- `is_frozen: bool`
- `overdraft_limit: int`

**Методы:**

- `debit(amount)`
- `credit(amount)`
- `freeze()`: Freeze account operations
- `unfreeze()`: Unfreeze account operations
- `set_overdraft_limit(limit)`: Set overdraft limit for the account
- `get_available_balance()`: Get available balance including overdraft

---

#### `Transaction`

**Поля:**

- `id: str`
- `src: str`
- `dst: str`
- `amount: int`
- `created_at: datetime`
- `status: str`
- `description: str`

**Методы:**

- `cancel()`: Mark transaction as cancelled
- `is_completed()`: Check if transaction is completed

---

#### `PaymentOrder`

**Поля:**

- `invoice_number: str`
- `src_account: str`
- `dst_account: str`
- `amount: int`
- `currency: str`
- `priority: int`
- `scheduled_date: datetime | None`

**Методы:**

- `is_high_priority()`: Check if this is a high priority payment
- `is_scheduled()`: Check if payment is scheduled for future

---

#### `BalanceChecker`

**Поля:**

- `min_balance: int`

**Методы:**

- `ensure_same_currency(a, b)`
- `check_sufficient_funds(account, amount)`: Check if account has sufficient funds
- `check_min_balance(account)`: Check if account meets minimum balance requirement

---

#### `InMemoryPaymentProcessor`

**Поля:**

- `accounts: Dict[str, Account]`
- `balance_checker: BalanceChecker`
- `transactions: List[Transaction]`
- `daily_limit: int`

**Методы:**

- `transfer(src_account, dst_account, amount)`
- `get_account_balance(account_number)`: Get account balance
- `get_transaction_history(account_number)`: Get transaction history for account
- `check_daily_limit(amount)`: Check if amount is within daily limit

---

### Модуль: `security.py`

#### `PasswordPolicy`

**Поля:**

- `min_length: int`
- `require_digit: bool`
- `require_uppercase: bool`
- `require_special: bool`

**Методы:**

- `validate(password)`
- `get_strength_score(password)`: Calculate password strength score (0-100)

---

#### `Session`

**Поля:**

- `user_id: str`
- `token: str`
- `created_at: datetime`
- `expires_at: datetime`
- `ip_address: str`
- `is_terminated: bool`

**Методы:**

- `is_active(moment)`
- `terminate()`: Terminate this session
- `extend(hours)`: Extend session expiration time

---

#### `Token`

**Поля:**

- `value: str`
- `issued_at: datetime`
- `expires_at: datetime | None`

**Методы:**

- `generate()`
- `is_expired(moment)`: Check if token is expired
- `revoke()`: Revoke token by setting expiration to now

---

#### `QuotaManager`

**Поля:**

- `max_bytes: int`
- `used_bytes: int`
- `warning_threshold: int`

**Методы:**

- `can_allocate(size)`
- `allocate(size)`
- `deallocate(size)`: Free up quota space
- `get_usage_percentage()`: Get quota usage as percentage
- `is_near_limit()`: Check if usage is near warning threshold

---

### Модуль: `services.py`

#### `InMemoryDocumentRepository`

**Поля:**

- `storage: DocumentStorage`

**Методы:**

- `save(doc)`
- `get(number)`
- `exists(number)`
- `search(query)`

---

#### `ConsoleNotifier`

**Методы:**

- `notify(message)`

---

#### `SearchService`

**Поля:**

- `repo: DocumentRepositoryProtocol`

**Методы:**

- `find(query)`

---

#### `ValidationService`

**Методы:**

- `validate(doc)`

---

#### `NotificationService`

**Поля:**

- `notifier: NotifierProtocol`

**Методы:**

- `send(message)`

---

#### `DocumentService`

**Поля:**

- `repo: DocumentRepositoryProtocol`
- `registry: DocumentRegistry`
- `validator: ValidationService`
- `notifier: NotificationService`

**Методы:**

- `register(doc)`
- `add_attachment(number, att)`
- `send_for_approval(number, route)`
- `sign(number, user)`
- `archive(number)`
- `require(number)`

---

#### `ApprovalService`

**Поля:**

- `notifier: NotificationService`

**Методы:**

- `route_for_role(role_name)`
- `approve(doc)`

---

#### `PaymentService`

**Поля:**

- `processor: PaymentProcessorProtocol`
- `notifier: NotificationService`

**Методы:**

- `pay_invoice(invoice, src, dst, amount)`

---

#### `AuthService`

**Поля:**

- `users: Dict[str, str]`
- `policy: PasswordPolicy`

**Методы:**

- `login(login, password)`

---

### Модуль: `storage.py`

#### `StorageLocation`

**Поля:**

- `name: str`
- `base_path: str`
- `is_active: bool`
- `capacity: int`

**Методы:**

- `validate_path()`: Validate that path is not empty
- `get_full_path(filename)`: Get full path to file

---

#### `DocumentStorage`

**Поля:**

- `location: StorageLocation`
- `quota: QuotaManager`

**Методы:**

- `save(doc)`
- `get(number)`
- `exists(number)`
- `store_attachment(doc, att)`
- `archive(doc)`
- `delete(number)`: Delete document from storage
- `count_documents()`: Count total documents in storage
- `get_all_numbers()`: Get all document numbers
- `clear()`: Clear all documents from storage

---

#### `ArchiveService`

**Поля:**

- `storage: DocumentStorage`
- `archive_retention_days: int`

**Методы:**

- `archive_document(number)`
- `restore_document(number)`
- `get_archived_documents()`: Get all archived documents
- `can_delete_archived(doc)`: Check if archived document can be permanently deleted

---

### Модуль: `users.py`

#### `Permission`

**Поля:**

- `code: str`
- `description: str`
- `priority: int`

**Методы:**

- `is_higher_priority_than(other)`: Check if this permission has higher priority than another

---

#### `Role`

**Поля:**

- `name: str`
- `permissions: Set[Permission]`
- `is_active: bool`

**Методы:**

- `allows(code)`
- `add_permission(permission)`: Add a permission to this role
- `remove_permission(permission)`: Remove a permission from this role
- `deactivate()`: Deactivate this role
- `activate()`: Activate this role

---

#### `Department`

**Поля:**

- `name: str`
- `cost_center: str`
- `budget: int`
- `head_id: str`

**Методы:**

- `allocate_budget(amount)`: Allocate budget to department
- `spend_budget(amount)`: Spend budget from department. Returns True if successful
- `get_remaining_budget()`: Get remaining budget

---

#### `AccessPolicy`

**Поля:**

- `allowed_roles: Set[str]`
- `denied_roles: Set[str]`

**Методы:**

- `can_access(roles)`
- `allow_role(role_name)`: Allow a role in this policy
- `deny_role(role_name)`: Deny a role in this policy

---

#### `Organization`

**Поля:**

- `name: str`
- `inn: str`
- `address: str`
- `phone: str`
- `email: str`

**Методы:**

- `update_contact_info(phone, email)`: Update organization contact information
- `validate_inn()`: Validate INN (Tax Identification Number)

---

#### `User`

**Поля:**

- `id: str`
- `login: str`
- `display_name: str`
- `is_blocked: bool`
- `roles: List[Role]`
- `department: Department | None`
- `org: Organization | None`
- `email: str`
- `phone: str`

**Методы:**

- `has_permission(code)`
- `assign_role(role)`
- `remove_role(role)`: Remove a role from user
- `block()`: Block user access
- `unblock()`: Unblock user access
- `change_department(department)`: Change user's department
- `get_active_roles()`: Get list of active roles

---

#### `Admin`

Наследует `User`. Администратор с полным доступом к системе.

**Дополнительные методы:**

- `manage_user(user, action)`: Управление пользователями (блокировка, разблокировка)

**Предустановленные права:**
- CREATE_DOCUMENT, EDIT_DOCUMENT, DELETE_DOCUMENT
- APPROVE_DOCUMENT
- MANAGE_USERS, MANAGE_ROLES
- VIEW_AUDIT_LOG, MANAGE_SYSTEM

---

#### `Manager`

Наследует `User`. Менеджер с правами согласования документов и управления командой.

**Дополнительные методы:**

- `approve_document(doc)`: Согласование документа
- `allocate_team_budget(amount)`: Выделение бюджета команде

**Предустановленные права:**
- CREATE_DOCUMENT, EDIT_DOCUMENT
- APPROVE_DOCUMENT
- VIEW_TEAM_DOCS, MANAGE_TEAM_BUDGET

---

#### `Accountant`

Наследует `User`. Бухгалтер с правами работы с финансовыми документами и платежами.

**Дополнительные методы:**

- `process_invoice(invoice)`: Обработка счета
- `audit_account(account)`: Аудит счёта

**Предустановленные права:**
- CREATE_INVOICE, VIEW_PAYMENTS
- PROCESS_PAYMENT
- VIEW_FINANCIAL_DOCS, AUDIT_TRANSACTIONS

---

#### `RegularUser`

Наследует `User`. Обычный пользователь с базовыми правами.

**Дополнительные методы:**

- `can_edit_document(doc)`: Проверка возможности редактирования документа

**Предустановленные права:**
- CREATE_DOCUMENT
- EDIT_OWN_DOCUMENT, VIEW_DOCUMENT

---

#### `Guest`

Наследует `User`. Гость с правами только на чтение.

**Дополнительные методы:**

- `can_only_view()`: Возвращает True (гость может только просматривать)

**Предустановленные права:**
- VIEW_DOCUMENT

---

### Модуль: `workflow.py`

#### `WorkflowState`

---

#### `ApprovalStep`

**Поля:**

- `name: str`
- `role_name: str`
- `required: bool`
- `deadline_hours: int`
- `order: int`

**Методы:**

- `deadline(start)`
- `is_overdue(start)`: Check if step is overdue
- `extend_deadline(additional_hours)`: Extend deadline by additional hours

---

#### `ApprovalTask`

**Поля:**

- `step: ApprovalStep`
- `assignee_id: str`
- `created_at: datetime`
- `completed: bool`
- `comment: str`
- `completed_at: datetime | None`

**Методы:**

- `complete(comment)`
- `reassign(new_assignee_id)`: Reassign task to another user
- `is_overdue()`: Check if task is overdue

---

#### `ApprovalRoute`

**Поля:**

- `name: str`
- `steps: List[ApprovalStep]`
- `is_active: bool`

**Методы:**

- `first_step()`
- `next_step(current)`
- `add_step(step)`: Add a step to the route
- `remove_step(step)`: Remove a step from the route
- `get_step_count()`: Get total number of steps

---

#### `WorkflowTransition`

**Поля:**

- `src: str`
- `dst: str`
- `reason: str`
- `actor_id: str`
- `timestamp: datetime`

**Методы:**

- `is_valid_transition()`: Check if this is a valid state transition

---

#### `Notification`

**Поля:**

- `message: str`
- `recipient_id: str`
- `created_at: datetime`
- `is_read: bool`
- `priority: int`

**Методы:**

- `mark_read()`: Mark notification as read
- `is_high_priority()`: Check if notification is high priority

---

## Исключения

Система использует следующие пользовательские исключения:

1. `AccessDeniedError`
2. `ApprovalStepError`
3. `AuthFailedError`
4. `DocumentNotFoundError`
5. `DuplicateDocumentError`
6. `InvalidDocumentStatusError`
7. `InvalidSignatureError`
8. `PaymentOperationError`
9. `RouteNotFoundError`
10. `StorageLimitExceededError`
11. `UserBlockedError`
12. `VersionConflictError`

## Ассоциации между классами

Система включает следующие ассоциации (связи между классами):

1. AccessPolicy → List[Role] (method parameter)
2. ApprovalRoute → ApprovalStep (field steps)
3. ApprovalRoute → ApprovalStep (method parameter)
4. ApprovalService → Document (method parameter)
5. ArchiveService → Document (method parameter)
6. ArchiveService → DocumentStorage (field storage)
7. BalanceChecker → Account (method parameter)
8. DemoContext → DocumentStorage (field storage)
9. Document → Document (field attachments)
10. Document → Document (field versions)
11. Document → DocumentAttachment (field attachments)
12. Document → DocumentAttachment (method parameter)
13. Document → Signature (field signatures)
14. Document → User (field author)
15. DocumentService → ApprovalRoute (method parameter)
16. DocumentService → Document (method parameter)
17. DocumentService → DocumentAttachment (method parameter)
18. DocumentService → User (method parameter)
19. DocumentStorage → Document (method parameter)
20. DocumentStorage → DocumentAttachment (method parameter)
21. DocumentStorage → QuotaManager (field quota)
22. InMemoryDocumentRepository → Document (method parameter)
23. InMemoryDocumentRepository → DocumentStorage (field storage)
24. InMemoryPaymentProcessor → Account (field accounts)
25. InMemoryPaymentProcessor → BalanceChecker (field balance_checker)
26. InMemoryPaymentProcessor → Transaction (field transactions)
27. PaymentService → InvoiceDocument (method parameter)
28. Role → Permission (field permissions)
29. Role → Permission (method parameter)
30. User → Department (method parameter)

**Всего уникальных ассоциаций:** 30

## Ключевые возможности

### Управление пользователями
- Создание и управление пользователями
- Система ролей и разрешений
- Блокировка/разблокировка пользователей
- Управление департаментами и организациями

### Документооборот
- Создание и редактирование документов
- Версионирование документов
- Вложения к документам
- Цифровые подписи
- Блокировка документов для редактирования
- Архивирование и восстановление

### Согласование
- Создание маршрутов согласования
- Назначение задач на согласование
- Отслеживание статусов
- Уведомления о событиях

### Безопасность
- Аутентификация пользователей
- Политики паролей
- Управление сессиями и токенами
- Контроль квот хранилища

### Платежи
- Переводы между счетами
- Проверка баланса и валюты
- История транзакций
- Контроль лимитов
- Заморозка/разморозка счетов



## Структура проекта

### Новая структура (обновлено)

Проект был реорганизован в соответствии с принципами многоуровневой архитектуры:

```
lab2/
├── documentflow/                # Основной пакет
│   ├── core/                   # Слой абстракций
│   │   ├── base.py            # Базовые классы (BaseEntity, Mixins)
│   │   └── protocols.py       # Протоколы и интерфейсы
│   ├── domain/                 # Слой бизнес-логики
│   │   ├── documents.py       # Доменные модели документов
│   │   ├── users.py           # Доменные модели пользователей
│   │   ├── workflow.py        # Доменные модели workflow
│   │   ├── payments.py        # Доменные модели платежей
│   │   └── security.py        # Доменные модели безопасности
│   ├── services/              # Слой сервисов приложения
│   │   ├── document_service.py    # Сервис управления документами
│   │   ├── notification_service.py # Сервис уведомлений
│   │   ├── approval_service.py    # Сервис согласований
│   │   ├── payment_service.py     # Сервис платежей
│   │   ├── auth_service.py        # Сервис аутентификации
│   │   └── search_service.py      # Сервис поиска
│   ├── infrastructure/        # Слой инфраструктуры
│   │   ├── storage.py         # Хранилище документов
│   │   ├── repository.py      # Репозитории
│   │   └── payment_processor.py # Процессор платежей
│   ├── exceptions.py          # Пользовательские исключения
│   ├── cli.py                 # CLI интерфейс
│   └── [backward compat]      # Модули обратной совместимости
├── tests/                     # Тесты
└── main.py                   # Точка входа
```

### Принципы организации

1. **Core (Ядро)** - содержит базовые абстракции, протоколы и интерфейсы, которые не зависят от конкретных реализаций

2. **Domain (Доменный слой)** - содержит бизнес-логику и доменные модели. Не зависит от инфраструктуры

3. **Services (Слой сервисов)** - содержит бизнес-сервисы, которые оркеструют работу доменных объектов

4. **Infrastructure (Инфраструктурный слой)** - содержит реализации хранилищ, репозиториев и внешних интеграций

### Обратная совместимость

Для поддержки существующего кода созданы модули обратной совместимости:
- `core.py`, `documents.py`, `users.py`, `workflow.py`, `payments.py`, `security.py`, `storage.py`, `services.py`

Эти модули импортируют и реэкспортируют классы из новой структуры, что позволяет существующему коду работать без изменений.
