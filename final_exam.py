from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []

    def __init__(self, name, accountNumber, password, type):
        self.name = name
        self.accountNo = accountNumber
        self.passW = password
        self.balance = 0
        self.type = type
        Account.accounts.append(self)


class User(ABC):
    accounts = []

    def __init__(self, name, accountNumber, password, account_type):
        self.name = name
        self.accountNumber = accountNumber
        self.password = password
        self.account_type = account_type
        self.balance = 0
        self.account_history = []
        User.accounts.append(self)

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.account_history.append(f'Deposit: +${amount}')
            print(f'Deposited ${amount}. New balance: ${self.balance}')
        else:
            print('Invalid deposit amount.')

    def withdraw(self, amount):
        if amount >= 0:
            if self.balance >= amount:
                self.balance -= amount
                self.account_history.append(f'Withdraw: -${amount}')
                print(f'Withdrew ${amount}. New balance: ${self.balance}')
            else:
                print('Withdrawal amount exceeded.')
        else:
            print('Invalid withdrawal amount.')

    def check_balance(self):
        return self.balance

    def check_transaction_history(self):
        return self.account_history

    def show_info(self):
        return f'Name: {self.name}, Account Number: {self.accountNumber}, Account Type: {self.account_type}, Balance: ${self.balance}'

    @abstractmethod
    def transfer(self, target_account, amount):
        pass

class SavingsUser(User):
    def __init__(self, name, accountNumber, password):
        super().__init__(name, accountNumber, password, 'Savings')
        self.loan_taken = 0
        self.transfer_limit = 2

    def take_loan(self, amount):
        if self.loan_taken < 2:
            self.loan_taken += 1
            self.balance += amount
            self.account_history.append(f'Loan: +${amount}')
            print(f'Loan approved: +${amount} added to your account.')
        else:
            print('You have already taken the maximum number of loans (2).')

    def transfer(self, target_account, amount):
        if target_account in User.accounts:
            if amount >= 0:
                if self.balance >= amount:
                    self.balance -= amount
                    target_account.deposit(amount)
                    self.account_history.append(f'Transfer: -${amount}')
                    print(f'Transferred ${amount} to {target_account.name}.')
                else:
                    print('Transfer amount exceeded.')
            else:
                print('Invalid transfer amount.')
        else:
            print('Account does not exist.')

class CurrentUser(User):
    def __init__(self, name, accountNumber, password):
        super().__init__(name, accountNumber, password, 'Current')

    def transfer(self, target_account, amount):
        if target_account in User.accounts:
            if amount >= 0:
                if self.balance >= amount:
                    self.balance -= amount
                    target_account.deposit(amount)
                    self.account_history.append(f'Transfer: -${amount}')
                    print(f'Transferred ${amount} to {target_account.name}.')
                else:
                    print('Transfer amount exceeded.')
            else:
                print('Invalid transfer amount.')
        else:
            print('Account does not exist.')

class Admin:
    def __init__(self):
        self.users = []

    def create_account(self, name, accountNumber, password, account_type):
        if account_type.lower() == 'savings':
            user = SavingsUser(name, accountNumber, password)
        elif account_type.lower() == 'current':
            user = CurrentUser(name, accountNumber, password)
        self.users.append(user)

    def delete_account(self, accountNumber):
        for user in self.users:
            if user.accountNumber == accountNumber:
                self.users.remove(user)
                print(f'Account {accountNumber} deleted.')

    def see_all_user_accounts(self):
        return [user.show_info() for user in self.users]

    def check_total_balance(self):
        total_balance = sum([user.balance for user in self.users])
        return f'Total bank balance: ${total_balance}'

   



admin = Admin()
admin.create_account("Alice", "12345", "password1", "Savings")
admin.create_account("Bob", "67890", "password2", "Current")

currentUser = None

while True:
    if currentUser is None:
       
        ch = input("\n--> Register/Login (R/L) : ")
        if ch == "R":
            name = input("Name: ")
            account_number = input("Account Number: ")
            password = input("Password: ")
            account = input("Savings Account or current Account (sv/cu): ")
            if account == "sv":
                ir = int(input("Interest rate: "))
                currentUser = SavingsUser(name, account_number, password, ir)
            else:
                lm = int(input("Overdraft Limit: "))
                currentUser = CurrentUser(name, account_number, password)
        else:
            account_number = input("Account Number: ")
            for account in Account.accounts:
                if account.accountNo == account_number:
                    currentUser = account
                    break
    if currentUser is not None:
     print(f"\nWelcome {currentUser.name}!\n")
    
    if currentUser.account_type == "Savings":
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Show Info")
        print("4. Apply Interest")
        print("5. Take Loan")
        print("6. Transfer Money")
        print("7. Logout\n")

        option = int(input("Choose Option: "))

        if option == 1:
            amount = int(input("Enter withdrawal amount: "))
            currentUser.withdraw(amount)
        elif option == 2:
            amount = int(input("Enter deposit amount: "))
            currentUser.deposit(amount)
        elif option == 3:
            print(currentUser.show_info())
        elif option == 4:
            currentUser.apply_interest()
        elif option == 5:
            amount = int(input("Enter loan amount: "))
            currentUser.take_loan(amount)
        elif option == 6:
            target_account_number = input("Enter target account number: ")
            target_account = None
            for account in User.accounts:
                if account.accountNumber == target_account_number:
                    target_account = account
                    break
            if target_account is not None:
                amount = int(input("Enter transfer amount: "))
                currentUser.transfer(target_account, amount)
            else:
                print("Account does not exist.")
        elif option == 7:
            currentUser = None
        else:
            print("Invalid Option")
    elif currentUser.account_type == "Current":
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Show Info")
        print("4. Transfer Money")
        print("5. Logout\n")

        option = int(input("Choose Option: "))

        if option == 1:
            amount = int(input("Enter withdrawal amount: "))
            currentUser.withdraw(amount)
        elif option == 2:
            amount = int(input("Enter deposit amount: "))
            currentUser.deposit(amount)
        elif option == 3:
            print(currentUser.show_info())
        elif option == 4:
            target_account_number = input("Enter target account number: ")
            target_account = None
            for account in User.accounts:
                if account.accountNumber == target_account_number:
                    target_account = account
                    break
            if target_account is not None:
                amount = int(input("Enter transfer amount: "))
                currentUser.transfer(target_account, amount)
            else:
                print("Account does not exist.")
        elif option == 5:
            currentUser = None
        else:
            print("Invalid Option")
    else:
       print("\n--> No user logged in!")
