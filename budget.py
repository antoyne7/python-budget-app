from math import e, floor

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
        
    graph_lines = 'Percentage spent by category\n'
    for n in range(10, -1, -1):
        graph_lines += '{:>3}|'.format(str(n*10))
        for cat in cat_dict.values():
            graph_lines += '{:^3}'.format('o' if cat >= n*10 else '')
        graph_lines += ' \n'

    names = '{}{}'.format(' '*4, 
                          '-'*(3*len(cat_dict)+1))

    is_writing_names = True
    index = 0
    while is_writing_names:
        is_writing_names = False
        chars = []
        for cat_name in cat_dict.keys():
            c = ''
            if index < len(cat_name):
                c = cat_name[index]
                is_writing_names = True
            chars.append(c)
        index += 1
        if is_writing_names:
            names += '\n    {:^3}{:^3}{:^3} '.format(chars[0], chars[1], chars[2])

    return '{}{}'.format(graph_lines,
                         names)
