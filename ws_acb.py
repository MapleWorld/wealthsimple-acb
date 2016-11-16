
# Adjusted Cost Basis
# D1: Buy 10 of ABC @ $5/unit: 10 units at $5/unit
# D2: Buy 10 of ABC @ $10/unit: 20 units at ((10 * 5) + (10 * 10))/(10 + 10) = $7.5/unit
# D3: Sell 5 of ABC @ $8/unit: 15 units at $7.5/unit
# D4: Buy 10 of ABC @ $6/unit: 25 units at ((15 * 7.5) + (10 * 6))/(15 + 10) = $6.9/unit

activities = [
	'DATE,SYMBOL,ACTION,QUANTITY,PRICE,CURRENCY',
	'2015-01-15,DEF,BUY,200,15,CAD',
	'2015-01-15,MMM,BUY,100,31,USD',
	'2015-01-15,XYZ,BUY,100,25,USD',
	'2015-01-30,DEF,BUY,100,18,CAD',
	'2015-01-30,MMM,BUY,100,32,USD',
	'2015-02-15,MMM,SELL,150,20,USD',
	'2015-02-17,DEF,SELL,300,15,CAD',
	'2015-02-25,DEF,BUY,75,21,CAD',
	'2015-02-27,DEF,BUY,25,25,CAD',
	'2015-02-30,MMM,SELL,50,15,USD',
	'2015-03-01,DEF,SELL,50,22,CAD',
	'2015-03-01,XYZ,BUY,25,35,USD',
	'2015-03-15,DEF,SELL,25,23,CAD',
	'2015-03-25,XYZ,SELL,50,37,USD',
	'2015-04-01,DEF,BUY,100,25,CAD',
	'2015-05-22,XYZ,BUY,125,31,USD',
	'2015-06-01,XYZ,SELL,25,32,USD',
	'2015-06-10,XYZ,BUY,50,38,USD']

rates = [
	'DATE,USD_to_CAD',
	'2015-01-15,1.13',
	'2015-01-30,1.15',
	'2015-02-15,1.17',
	'2015-02-17,1.21',
	'2015-02-25,1.26',
	'2015-02-27,1.25',
	'2015-02-30,1.22',
	'2015-03-01,1.2',
	'2015-03-15,1.35',
	'2015-03-25,1.23',
	'2015-04-01,1.33',
	'2015-05-22,1.3',
	'2015-06-01,1.2',
	'2015-06-10,1.18']


#Parse rates into dict
rate = {}
for r in rates[1:]:
	r = r.split(',')
	rate[r[0]] = r[1]

#Quick lookup function to rate table returning exchange rate on day 'x'
xrate = lambda x: float(rate[x])


class Asset():
	def __init__(self, symbol, quantity, acb, currency):
		self.symbol = symbol
		self.quantity = float(quantity)
		self.acb = float(acb)
		self.currency = currency

	def buy(self, date, quantity, price):
		#Assume currency in CAD
		exrate = 1
		if self.currency == "USD":
			exrate = xrate(date)

		self.acb = ((self.acb * self.quantity) + (float(quantity) * float(price) * exrate)) / (self.quantity + float(quantity))
		self.quantity += float(quantity)

	def sell(self, quantity):
		self.quantity -= float(quantity)

	def __repr__(self):
		return "You own %i shares of asset %s at an average cost of $%s per share" % (self.quantity, self.symbol, str(self.acb))

	def info(self):
		return "You own %i shares of asset %s at an average cost of $%s per share" % (self.quantity, self.symbol, str(self.acb))


class Portfolio():
	def __init__(self):
		self.assets = {}

	def contains_asset(self, symbol):
		if symbol in self.assets.keys():
			return True
		else:
			return False

	def add_asset(self, symbol, currency):
		self.assets[symbol] = Asset(symbol, 0, 0, currency)

	def get_asset(self, symbol):
		return self.assets[symbol]

	def display(self):
		positions = []
		for symbol in self.assets.keys():
			positions.append(self.assets[symbol].info())
		print positions


portfolio = Portfolio()

for activity in activities[1:]:
	activity = activity.split(',')
	symbol = activity[1]
	if not portfolio.contains_asset(symbol):
		portfolio.add_asset(symbol, activity[5])
	if activity[2] == "BUY":
		portfolio.get_asset(symbol).buy(activity[0], activity[3], activity[4])
	elif activity[2] == "SELL":
		portfolio.get_asset(symbol).sell(activity[3])

portfolio.display()
