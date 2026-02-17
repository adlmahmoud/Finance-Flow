# FinanceFlow Architecture & API Documentation

## 📐 System Architecture

### Layered Architecture

```
┌─────────────────────────────────────────┐
│         UI Layer (Flet)                 │
│  ├─ Pages (Dashboard, Transactions)    │
│  ├─ Components (Cards, Charts)         │
│  └─ Main App (Navigation, State)       │
├─────────────────────────────────────────┤
│      Controllers (Business Logic)       │
│  ├─ AppController (Main Orchestrator)  │
│  └─ Request Handling                   │
├─────────────────────────────────────────┤
│         Services Layer                  │
│  ├─ BankService (Bank Integration)    │
│  ├─ TransactionService (Mgmt)         │
│  └─ AnalyticsService (Analytics)      │
├─────────────────────────────────────────┤
│         Data Layer (SQLModel)           │
│  ├─ User Model                         │
│  ├─ BankAccount Model                  │
│  ├─ Transaction Model                  │
│  ├─ Budget Model                       │
│  └─ Analytics Model                    │
├─────────────────────────────────────────┤
│    Database Layer (SQLite)              │
│  └─ finance_flow.db                    │
└─────────────────────────────────────────┘
```

## 🔄 Data Flow

### User Authentication Flow
```
Login Page
    ↓
Username/Password Input
    ↓
AppController.authenticate_user()
    ↓
SecurityManager.verify_password()
    ↓
Database Query (User)
    ↓
Session Created
    ↓
Dashboard Loaded
```

### Transaction Sync Flow
```
Sync Button Clicked
    ↓
AppController.sync_transactions_from_bank()
    ↓
BankServiceFactory.create()
    ↓
BankService.get_transactions()
    ↓
TransactionService.import_transactions_from_bank()
    ↓
Database Insert (Transactions)
    ↓
Dashboard Refreshed with New Data
```

### Analytics Generation Flow
```
Dashboard Load
    ↓
AppController.get_dashboard_data()
    ↓
AnalyticsService Methods:
  ├─ get_total_balance()
  ├─ get_spending_by_category()
  ├─ get_budget_status()
  └─ get_insights()
    ↓
Aggregated Data
    ↓
UI Rendered
```

## 📊 Data Models

### User Model
```python
User
├── id (int, PK)
├── username (str, unique)
├── email (str, unique)
├── password_hash (str, encrypted)
├── full_name (str)
├── monthly_budget (float)
├── currency (str)
├── created_at (datetime)
├── updated_at (datetime)
└── relationships:
    ├── accounts (BankAccount[])
    └── budgets (Budget[])
```

### BankAccount Model
```python
BankAccount
├── id (int, PK)
├── user_id (int, FK)
├── account_name (str)
├── account_number (str, unique)
├── bank_name (str)
├── balance (float)
├── currency (str)
├── bank_api_id (str, optional)
├── created_at (datetime)
├── updated_at (datetime)
└── relationships:
    ├── user (User)
    └── transactions (Transaction[])
```

### Transaction Model
```python
Transaction
├── id (int, PK)
├── account_id (int, FK)
├── description (str)
├── amount (float)
├── category (TransactionCategory, enum)
├── transaction_type (TransactionType, enum)
├── merchant (str, optional)
├── external_id (str, optional)
├── date (datetime, indexed)
├── created_at (datetime)
├── updated_at (datetime)
└── relationships:
    └── account (BankAccount)
```

### Budget Model
```python
Budget
├── id (int, PK)
├── user_id (int, FK)
├── category (TransactionCategory, enum)
├── monthly_limit (float)
├── spent_this_month (float)
├── created_at (datetime)
├── updated_at (datetime)
└── relationships:
    └── user (User)
```

### Analytics Model
```python
Analytics
├── id (int, PK)
├── user_id (int, FK)
├── year (int)
├── month (int)
├── total_income (float)
├── total_expenses (float)
├── net_balance (float)
├── created_at (datetime)
├── updated_at (datetime)
```

## 🎯 Service Interfaces

### BankService Interface
```python
class BaseBankService(ABC):
    def authenticate(credentials: Dict) -> bool
    def get_accounts() -> List[Dict]
    def get_transactions(account_id: str, days_back: int) -> List[Dict]
    def get_balance(account_id: str) -> float
```

### TransactionService
```python
class TransactionService:
    def create_transaction(transaction: Transaction) -> Transaction
    def get_transaction(id: int) -> Optional[Transaction]
    def get_transactions_for_account(account_id: int) -> List[Transaction]
    def update_transaction(id: int, **kwargs) -> Optional[Transaction]
    def delete_transaction(id: int) -> bool
    def import_transactions_from_bank(account_id: int, txns: List) -> List
    def get_monthly_summary(account_id: int, year: int, month: int) -> Dict
    def get_category_spending(account_id: int, days_back: int) -> Dict
```

### AnalyticsService
```python
class AnalyticsService:
    def get_total_balance(user_id: int) -> float
    def get_account_balance(account_id: int) -> float
    def get_monthly_balance_trend(user_id: int) -> List[Dict]
    def get_spending_by_category(user_id: int, days_back: int) -> Dict
    def get_budget_status(user_id: int) -> List[Dict]
    def get_insights(user_id: int) -> Dict
    def export_monthly_report(user_id: int, year: int, month: int) -> Dict
```

### AppController
```python
class AppController:
    # User Management
    def create_user(username, email, password, full_name, monthly_budget) -> User
    def authenticate_user(username, password) -> Optional[User]
    
    # Bank Accounts
    def add_bank_account(user_id, account_name, account_number, bank_name) -> BankAccount
    def get_user_accounts(user_id: int) -> List[BankAccount]
    
    # Transactions
    def sync_transactions_from_bank(user_id: int) -> Dict
    def get_transactions(user_id, account_id, days_back) -> List[Transaction]
    
    # Budgets
    def set_category_budget(user_id, category, monthly_limit) -> Budget
    
    # Analytics
    def get_dashboard_data(user_id: int) -> Dict
    def get_monthly_report(user_id, year, month) -> Dict
    def get_category_analysis(user_id, days_back) -> Dict
```

## 🔐 Security Architecture

### Password Security
```
User Input Password
    ↓
Generate Random 32-byte Salt
    ↓
PBKDF2-HMAC-SHA256 (100,000 iterations)
    ↓
Concatenate: salt_hex + hash_hex
    ↓
Store in Database
    ↓
On Login:
    Extract salt from stored hash
    ↓
    Rehash with same salt
    ↓
    Constant-time comparison
```

### Sensitive Data Encryption
```
API Key / Token
    ↓
Fernet Encryption (AES-128)
    ↓
Encrypt with derived key from SECRET_KEY
    ↓
Store encrypted blob in database
    ↓
On Use:
    Decrypt with same key
    ↓
    Use decrypted value
    ↓
    Discard after use
```

## 🎨 UI Component Hierarchy

```
FinanceFlowApp (Main)
├── Sidebar (Navigation)
│   ├── Logo & Brand
│   ├── Navigation Items
│   │   ├── Dashboard
│   │   ├── Transactions
│   │   ├── Analytics
│   │   └── Settings
│   └── User Profile
├── Main Content Area
│   ├── DashboardPage
│   │   ├── HeaderBar
│   │   ├── StatCard (multiple)
│   │   ├── Chart Section
│   │   ├── Budgets Section
│   │   │   └── BudgetBar (multiple)
│   │   └── Transactions Section
│   │       └── TransactionItem (multiple)
│   ├── TransactionsPage
│   │   ├── HeaderBar
│   │   ├── Filters
│   │   └── TransactionItem List
│   ├── AnalyticsPage
│   │   ├── HeaderBar
│   │   └── Charts & Reports
│   └── SettingsPage
│       ├── HeaderBar
│       ├── Account Settings
│       ├── Budget Configuration
│       ├── Bank API Settings
│       └── App Settings
└── LoginPage
    ├── Logo
    ├── Login Form
    └── Signup Form
```

## 📋 Database Indexes

```sql
-- Performance Optimization
CREATE INDEX idx_transaction_account_date 
    ON transactions(account_id, date);

CREATE INDEX idx_transaction_date 
    ON transactions(date);

CREATE INDEX idx_bankaccount_user 
    ON bank_accounts(user_id);

CREATE INDEX idx_budget_user 
    ON budgets(user_id);

CREATE INDEX idx_analytics_user_month 
    ON analytics(user_id, year, month);
```

## 🔄 Event Flow

### Application Lifecycle
```
1. main.py executed
   ↓
2. init_application()
   ├─ DatabaseManager.init_db()
   ├─ Logger configured
   └─ Settings loaded
   ↓
3. Flet app started
   ↓
4. FinanceFlowApp initialized
   ├─ AppController created
   ├─ BankService created
   └─ UI built
   ↓
5. LoginPage displayed
   ↓
6. User authenticates
   ├─ Credentials validated
   ├─ User loaded from DB
   └─ Session created
   ↓
7. DashboardPage loaded
   ├─ Dashboard data fetched
   ├─ UI components rendered
   └─ User can interact
```

## 🚀 Performance Optimization

### Database Query Optimization
- Indexed columns (date, user_id, account_id)
- Batch imports for transactions
- Aggregation queries at database level
- Connection pooling via SQLAlchemy

### Memory Management
- Session management for connections
- Lazy loading for relationships
- UI pagination for long lists
- Cache invalidation on updates

### Caching Strategies
- Transaction history cached per request
- Dashboard data refreshed on user request
- Category spending aggregated monthly

## 🧪 Testing Scenarios

### Happy Path
1. User creates account
2. Adds bank account
3. Syncs transactions from bank (mock)
4. Views dashboard
5. Sets budgets
6. Views analytics
7. Logs out

### Error Cases
1. Invalid login credentials
2. Duplicate username
3. Weak password
4. Database connection failure
5. API timeout
6. Corrupt transaction data

## 📈 Scalability Considerations

### Database Scaling
- Migration to PostgreSQL for production
- Connection pooling for concurrency
- Partitioning transactions table by date
- Archival of old transactions

### Application Scaling
- Separate API backend
- Caching layer (Redis)
- Load balancing
- Asynchronous job processing

## 🔌 API Integration Points

### Mock Bank Service
- Generates realistic test data
- Perfect for development
- No external dependencies

### Plaid Integration
- Provider: Plaid (https://plaid.com)
- Models: Bank accounts, transactions, balances
- SDKs available
- Webhook support for real-time updates

### GoCardless Integration
- Provider: GoCardless (https://gocardless.com)
- Open banking API
- Multi-country support
- Payment processing included

## 📝 Code Examples

### Creating a Transaction
```python
controller = AppController()
txn = Transaction(
    account_id=1,
    description="Grocery store",
    amount=45.50,
    category=TransactionCategory.FOOD,
    transaction_type=TransactionType.EXPENSE,
    date=datetime.now(),
)
controller.controller.session.add(txn)
controller.controller.session.commit()
```

### Getting Dashboard Data
```python
controller = AppController()
data = controller.get_dashboard_data(user_id=1)

print(f"Total balance: {data['total_balance']}")
print(f"Top categories: {data['insights']['top_categories']}")
print(f"Budget alerts: {data['insights']['budget_alerts']}")
```

### Syncing From Bank
```python
results = controller.sync_transactions_from_bank(user_id=1)
# Results: {account_id: num_imported, ...}

for account_id, count in results.items():
    print(f"Account {account_id}: {count} transactions imported")
```

---

**FinanceFlow Architecture v2.0**
This architecture supports current needs and scales for future growth.
