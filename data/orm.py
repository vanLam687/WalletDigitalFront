import sqlobject as SO

database = 'mysql://Vanina:ilolay687@localhost/basededatos' 
__connection__ = SO.connectionForURI(database)

class User(SO.SQLObject):
    _connection = __connection__
    username = SO.StringCol(length=100, unique=True)
    pwd = SO.StringCol(length=255)
    accounts = SO.MultipleJoin("Account")

class Account(SO.SQLObject):
    _connection = __connection__
    currency = SO.StringCol(length=10)
    balance = SO.DecimalCol(size=10, precision=2, default=0.00)

    user = SO.ForeignKey("User", cascade=True)

if __name__ == "__main__":
    User.createTable(ifNotExists=True)
    Account.createTable(ifNotExists=True)