# FinanceFlow v2.0 - Modern Expense Management

**A modern, secure, and automated expense management application with bank API integration.**

## 🎯 Features

### ✨ Core Features
- **Modern UI** - Built with Flet (Flutter for Python) - responsive and beautiful dark theme
- **Secure Database** - SQLite with SQLAlchemy ORM for efficient data management
- **Bank Integration** - Ready for Plaid/GoCardless API integration
- **Auto Transaction Sync** - Fetch transactions directly from your bank
- **Smart Dashboard** - Real-time financial overview with key metrics
- **Budget Management** - Set category budgets and track spending
- **Analytics** - Detailed financial insights and spending analysis
- **Security** - Password hashing, encrypted sensitive data, secure token management

### 🏦 Banking Features
- Mock bank service for development and testing
- Modular architecture ready for Plaid integration
- Modular architecture ready for GoCardless integration
- Automatic transaction categorization
- Multiple account support

### 📊 Dashboard & Analytics
- **Balance Overview** - Total balance across all accounts
- **Monthly Spending** - Track spending vs budget
- **Category Breakdown** - Pie charts and detailed breakdowns
- **Budget Status** - Progress bars for each category
- **Financial Trends** - Historical charts and trends
- **Monthly Reports** - Comprehensive financial reports

### 🔒 Security
- Passwords hashed with PBKDF2 (100,000 iterations)
- API keys encrypted with Fernet
- No plain-text sensitive data storage
- Input validation and sanitization
- CORS protection ready

## 📁 Project Structure

```
finance-flow-v2/
├── config/
│   ├── __init__.py
│   └── settings.py              # Centralized configuration
├── models/
│   ├── __init__.py
│   ├── database.py              # SQLModel database models
│   └── database_init.py         # Database initialization
├── services/
│   ├── __init__.py
│   ├── bank_service.py          # Bank API integration (Mock, Plaid, GoCardless)
│   ├── transaction_service.py   # Transaction management
│   └── analytics_service.py     # Financial analytics
├── controllers/
│   ├── __init__.py
│   └── app_controller.py        # Business logic orchestration
├── ui/
│   ├── __init__.py
│   ├── main_app.py              # Flet application entry point
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── dashboard.py         # Dashboard page
│   │   ├── transactions.py      # Transactions list page
│   │   └── settings.py          # Settings page
│   └── components/
│       ├── __init__.py
│       └── widgets.py           # Reusable UI components
├── utils/
│   ├── __init__.py
│   └── security.py              # Security utilities
├── data/                        # Database storage
├── logs/                        # Application logs
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

1. **Clone or navigate to project:**
```bash
cd finance-flow-v2
```

2. **Create virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

The application will start with:
- Welcome/Login screen
- Demo credentials can be created on first run
- Full dashboard with mock bank data

### Demo Credentials
After starting the app:
1. Click "S'inscrire" (Sign Up)
2. Create test account:
   - Username: `demo`
   - Password: `Demo@1234`

## 📚 Usage Guide

### Dashboard
Main view showing:
- Total balance across accounts
- Monthly expenses vs budget
- Category breakdown pie chart
- Recent transactions
- Budget status

### Transactions
- View all transactions with filtering
- Filter by date range (7, 30, 90, 365 days)
- Sync transactions from bank (mock data by default)
- See transaction details

### Budgets
- Set monthly budget limits for each category
- Real-time tracking with progress bars
- Budget alerts when exceeded
- Category-based spending breakdown

### Settings
- Account management
- Budget configuration
- Bank API configuration
- Theme preferences
- Logout

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Application
DEBUG=False
APP_NAME=FinanceFlow
THEME=dark

# Database
DATABASE_URL=sqlite:///./data/finance_flow.db

# Bank API
BANK_API_PROVIDER=mock
BANK_API_KEY=your_api_key_here
BANK_API_SECRET=your_api_secret_here

# Security
SECRET_KEY=your-secret-key-change-in-production
```

### Settings
Edit `config/settings.py` to customize:
- Window size
- Default currency
- Monthly budget
- Theme
- Bank provider
- etc.

## 🏗️ Architecture

### Design Patterns Used
- **MVC** - Model-View-Controller separation
- **Service Layer** - Business logic encapsulation
- **Factory Pattern** - Bank service creation
- **Singleton Pattern** - Database connection management
- **Dependency Injection** - Service initialization

### Database Schema
- **Users** - User accounts with encrypted passwords
- **BankAccounts** - Multiple bank accounts per user
- **Transactions** - Full transaction history with categorization
- **Budgets** - Category-based budget limits
- **Analytics** - Monthly aggregates for performance

## 🔌 Bank API Integration

### Mock Service (Current)
Built-in mock service generates realistic test transactions:
- Random categories and merchants
- Realistic amounts
- Monthly salary deposits
- Perfect for development

### Plaid Integration (Ready)
To enable Plaid integration:
1. Get Plaid API keys from https://plaid.com
2. Add to `.env`: `BANK_API_KEY=your_plaid_key`
3. Change provider: `BANK_API_PROVIDER=plaid`
4. Implement Plaid SDK calls in `PlaidBankService`

### GoCardless Integration (Ready)
To enable GoCardless integration:
1. Get GoCardless API keys from https://gocardless.com
2. Add to `.env`: `BANK_API_KEY=your_gocardless_key`
3. Change provider: `BANK_API_PROVIDER=gocardless`
4. Implement GoCardless SDK calls in `GoCardlessService`

## 🧪 Testing

### Test User Flow
1. Create account: username=`test`, password=`Test@1234`
2. Dashboard shows mock accounts and transactions
3. Sync transactions from bank (mock data)
4. Set budgets in settings
5. View analytics and reports

### Mock Data
- 2 mock bank accounts
- 15-30 transactions per account
- Realistic categories and amounts
- Monthly salary deposits

## 📊 Features Detailed

### Dashboard Analytics
- Current balance calculation
- Monthly spending aggregation
- Average monthly expenses
- Category spending breakdown
- Budget status for all categories
- Financial recommendations

### Transaction Sync
- Automatic deduplication by external_id
- Bulk import for efficiency
- Transaction categorization
- Date parsing from bank format
- Error handling and logging

### Budget Management
- Per-category monthly budgets
- Real-time spent tracking
- Budget alerts
- Percentage and amount display
- Exceeded indicators

### Security Features
- PBKDF2 password hashing (100k iterations)
- Fernet encryption for API keys
- Secure token generation
- Password strength validation
- Email validation
- No sensitive data in logs

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database (caution - deletes all data)
rm -rf data/finance_flow.db
python main.py
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use
The application uses Flet's built-in server. If port issues occur:
```bash
# Use different port
export FLET_SERVER_PORT=8501
python main.py
```

## 📝 Development

### Adding New Pages
1. Create page class in `ui/pages/`:
```python
class NewPage(ft.UserControl):
    def __init__(self, controller, user_id):
        super().__init__()
        self.controller = controller
        self.user_id = user_id
    
    def build(self):
        return ft.Column([...])
```

2. Add navigation in `ui/main_app.py`

### Adding New Services
1. Create service class in `services/`
2. Add to controller
3. Use in pages

### Database Migrations
SQLModel with SQLAlchemy handles schema updates:
1. Modify models in `models/database.py`
2. Restart application
3. Tables automatically created/updated

## 🚀 Deployment

### Build Standalone Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Production Checklist
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Use production database URL
- [ ] Configure bank API credentials
- [ ] Set up logging to files
- [ ] Configure HTTPS if needed
- [ ] Test all user flows
- [ ] Backup database regularly

## 📦 Dependencies

### Core
- **flet** (v0.21.0) - Modern UI framework
- **sqlalchemy** (v2.0.23) - ORM
- **sqlmodel** (v0.0.14) - SQLAlchemy + Pydantic models
- **pydantic** (v2.5.0) - Data validation

### Data & Analytics
- **pandas** (v2.1.3) - Data analysis
- **plotly** (v5.18.0) - Interactive charts (future)

### Security
- **cryptography** (v41.0.7) - Encryption
- **python-dotenv** (v1.0.0) - Environment variables

### Bank APIs (Optional)
- **plaid-python** - For Plaid integration
- **gocardless-pro** - For GoCardless integration

## 📄 License

This project is provided as-is for learning and development purposes.

## 👨‍💻 Author

Architected and built as a modern Python application using best practices in:
- Clean Architecture
- SOLID Principles
- Security-First Design
- Scalable Backend
- Beautiful Modern UI

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- [ ] Plaid/GoCardless real API implementation
- [ ] Export to CSV/PDF
- [ ] Transaction search and filtering
- [ ] Recurring transaction detection
- [ ] Mobile app version
- [ ] Cloud sync
- [ ] User collaboration features
- [ ] Advanced charting with Plotly

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review application logs in `logs/financeflow.log`
3. Check database integrity: `sqlite3 data/finance_flow.db`

---

**Happy expense tracking! 💰✨**
# Finance-Flow
