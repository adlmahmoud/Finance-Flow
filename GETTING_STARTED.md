# 🚀 FinanceFlow v2.0 - Getting Started

## Installation & Running

### Option 1: Quick Start (Recommended)
```bash
cd finance-flow-v2
python main.py
```

### Option 2: With Setup Verification
```bash
cd finance-flow-v2
python quickstart.py
python main.py
```

## First Login

When the application starts, you'll see a login screen.

### Create a Test Account
1. Click **"S'inscrire"** (Sign Up) button
2. Enter credentials:
   - **Username**: `demo`
   - **Email**: Any email (e.g., demo@test.com)
   - **Password**: `Demo@1234` (or choose your own)
3. Click **Sign Up**

**Important**: Passwords must be strong:
- At least 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter  
- At least 1 number
- At least 1 special character (!@#$%^&*)

### Example Strong Password
- ✅ `FinanceFlow@2024`
- ✅ `MyExpense!!123`
- ✅ `Budget$Manager99`

## Features to Try

### 1. Dashboard
- **Location**: Main page after login
- **Features**:
  - View total balance (mock data)
  - See monthly expenses
  - Check remaining budget
  - View recent transactions
  - See budget status by category

### 2. Transactions
- **Location**: Click "💳 Transactions" in sidebar
- **Features**:
  - View all transactions
  - Filter by date range (7, 30, 90, 365 days)
  - Click refresh button to sync from bank (mock data)
  - See transaction details

### 3. Settings
- **Location**: Click "⚙️ Paramètres" in sidebar
- **Features**:
  - View account information
  - Configure category budgets
  - Bank API settings
  - App preferences

## Sample Data

The application comes with realistic mock bank data:

### Accounts
- **Compte Courant** - 2500.50 EUR
- **Compte Épargne** - 5000.00 EUR

### Transactions Include
- Grocery purchases
- Transport costs
- Utility bills
- Entertainment subscriptions
- Shopping purchases
- Healthcare expenses
- Random monthly salary

## Configuration

### Environment Variables (.env file)
```env
DEBUG=False
THEME=dark
BANK_API_PROVIDER=mock
DEFAULT_MONTHLY_BUDGET=3000.0
```

Default settings are fine for exploration. Create a `.env` file in the project root to customize.

## Project Structure

```
finance-flow-v2/
├── main.py                    # Entry point - run this!
├── config/                    # Configuration
├── models/                    # Database models
├── services/                  # Business logic
├── controllers/               # Application controller
├── ui/                        # User interface
│   ├── pages/                # Dashboard, Transactions, Settings
│   └── components/           # Reusable UI components
├── utils/                     # Security utilities
├── data/                      # Database (created on first run)
├── logs/                      # Application logs
├── requirements.txt           # Python dependencies
├── README.md                  # Full documentation
└── ARCHITECTURE.md           # Technical architecture
```

## Database

### Automatic Setup
- Database automatically created on first run
- Location: `data/finance_flow.db`
- SQLite format

### Reset Database
To start fresh with a clean database:
```bash
rm data/finance_flow.db
python main.py
```

## Troubleshooting

### Common Issues

**Issue**: "Module not found errors"
```bash
pip install -r requirements.txt
```

**Issue**: "Database locked"
- Close the application
- Delete `data/finance_flow.db`
- Restart application

**Issue**: "Port already in use"
- Flet automatically uses available ports
- Should resolve itself

### Logs
Check application logs for detailed errors:
```bash
cat logs/financeflow.log
```

## Next Steps

### Explore Features
1. Create multiple test accounts
2. Try different password strengths
3. Explore all menu items
4. Check dashboard calculations
5. View different time ranges

### Customize
Edit `config/settings.py` to change:
- Default monthly budget
- Currency and date format
- Window size
- Theme colors

### Bank Integration
When ready for real bank data:
1. Get API credentials from Plaid or GoCardless
2. Set environment variables with API keys
3. Change `BANK_API_PROVIDER` in `.env`
4. Implement API calls in respective service classes

## Documentation

- **README.md** - Complete feature documentation
- **ARCHITECTURE.md** - System design and architecture
- **IMPLEMENTATION_SUMMARY.md** - What's been delivered
- Code comments - Detailed inline documentation

## Support

### Check These First
1. Review README.md for feature documentation
2. Check logs in `logs/financeflow.log`
3. Verify database isn't corrupted
4. Ensure all dependencies installed

### For Development
- Code is well-commented
- Architecture.md explains design
- Each module has docstrings
- Examples in docstrings

## System Requirements

- **Python**: 3.11 or higher
- **OS**: Windows, macOS, Linux
- **RAM**: 512 MB minimum
- **Disk**: 100 MB for dependencies

## Performance

The application is optimized for:
- Fast startup (< 5 seconds)
- Smooth UI interactions
- Quick database queries
- Low memory usage (< 200 MB)

## Security

Your data is secure:
- Passwords hashed with PBKDF2 (100k iterations)
- API keys encrypted with Fernet
- No sensitive data in logs
- Local SQLite database

## Tips & Tricks

### Keyboard Shortcuts
- Alt+Tab: Switch between windows (OS-level)
- Tab: Navigate between fields
- Enter: Submit forms

### Budget Tips
- Set category budgets in Settings
- Dashboard shows budget status
- Red color = over budget
- Green color = within budget

### Transaction Tips
- Use filter to see specific date ranges
- Sync button fetches latest bank data
- Recent transactions shown on dashboard

## Keyboard Navigation

All UI elements are keyboard accessible:
- Tab: Move between fields
- Enter: Click buttons
- Arrows: Scroll lists

---

**Happy using FinanceFlow! 💰**

For questions or issues, check the full README.md and ARCHITECTURE.md files.
