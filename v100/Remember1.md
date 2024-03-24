Options
-----------------------------------------------------------------------------------------------------------------------------------------
📊 Financial Overview:

Monthly Transactions
Member Payments
Contributions Summary
Financial Status
👤 Executive Members:

Add Executive Member
View Executive Members
View Executive Member Profile
Edit Executive Member
Remove Executive Member
👥 Club Members:

View All Members
View Member Profile
Edit Member Profile
Remove Member
💰 Financial Management:

View Financial Status
Generate Financial Reports
Manage Club Expenses
Manage Bank Transactions
🔒 Logout


Database
-----------------------------------------------------------------------------------------------------------------------------------------
-- Members Table
CREATE TABLE Members (
    member_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    name TEXT,
    email TEXT,
    phone TEXT,
    is_executive INTEGER DEFAULT 0, -- 0 for regular member, 1 for executive member
    account_balance REAL DEFAULT 0
);

-- Transactions Table
CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY,
    member_id INTEGER,
    amount REAL,
    purpose TEXT,
    date DATE,
    transaction_type TEXT CHECK (transaction_type IN ('Payment', 'Contribution', 'Reimbursement')),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

-- Club Expenses Table
CREATE TABLE ClubExpenses (
    expense_id INTEGER PRIMARY KEY,
    description TEXT,
    amount REAL,
    category TEXT,
    date DATE
);

-- Bank Transactions Table
CREATE TABLE BankTransactions (
    transaction_id INTEGER PRIMARY KEY,
    member_id INTEGER,
    debit_amount REAL,
    credit_amount REAL,
    date DATE,
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

-- Indexes
CREATE INDEX idx_member_id ON Transactions(member_id);

-- Constraints
ALTER TABLE Members
ADD CHECK (is_executive IN (0, 1));

-- Hashing Function (e.g., bcrypt) should be used when storing passwords.
-- This depends on the specific database system you're using.
