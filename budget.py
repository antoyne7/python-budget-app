from math import floor

class Category:
    print_width = 30

    def __init__(self, name: str) -> int:
        self.name = name
        self.ledger = []


    def deposit(self, amount: float, description: str = '') -> None:
        self.ledger.append({
            'amount': float(amount),
            'description': description
        })


    def withdraw(self, amount: float, description: str = '') -> bool:
        if not self.check_funds(amount): return False

        self.deposit(-amount, description)
        return True
        

    def get_balance(self) -> float:
        total = 0
        for operation in self.ledger:
            total += operation['amount']
        return total


    def check_funds(self, amount) -> bool:
        return amount <= self.get_balance()


    def transfer(self, amount: float, other_category) -> bool:
        if not self.check_funds(amount):
            return False

        self.withdraw(amount, 'Transfer to {}'.format(other_category.name))
        other_category.deposit(amount, 'Transfer from {}'.format(self.name))
        return True

    
    def __str__(self) -> str:
        title = '{:*^30}\n'.format(self.name)

        ledger_lines = ''
        for line in self.ledger:
            descr = '{:23}'.format(line['description'][:23])
            amount = '{:>7.2f}'.format(line['amount'])
            ledger_lines += '{}{}\n'.format(descr, amount)

        total = 'Total: {:.2f}'.format(self.get_balance())

        return title + ledger_lines + total



def get_withdrawals(categorie):
    withdrawals = 0
    for operation in categorie.ledger:
        if operation['amount'] < 0: withdrawals += operation['amount']
    return withdrawals

def create_spend_chart(categories):
    cat_dict = {}
    sum = 0
    for categorie in categories:
        cat_withdrawals = -get_withdrawals(categorie)
        cat_dict[categorie.name] = cat_withdrawals
        sum += cat_withdrawals

    for cat_name in cat_dict:
        cat_dict[cat_name] = floor(cat_dict[cat_name]/sum*10)*10
        
    print('Cat Dict:', cat_dict)

    title = 'Percentage spent by category\n'

    return '{}'.format(
        title
    )


g = Category('gamin')

g.deposit(10, 'Achat 1')
g.deposit(30, 'ah oui le super achatttee')
g.deposit(13, 'Achat 2')
g.deposit(40.00, 'Achat 3')
g.deposit(1000, 'Achat 4')

g.withdraw(10, 'withdraw')

c = Category('couille')

g.transfer(100, c)

print(g.ledger[-1], g.get_balance())
print(c.ledger[-1], c.get_balance())

print(g)
