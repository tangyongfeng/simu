class Strategy:
	def __init__(self,bestStrategy):	
		self.loadStrategyTable()
		self.startOfStrategyTable=4
		self.endOfStrategyTable=27
		self.beststrategy=bestStrategy
		self.strategyData=[
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','S','S','S','S','S'],
['S','S','S','S','S','H','H','H','H','H'],
['S','S','S','S','S','H','H','H','H','H'],
['S','S','S','S','S','H','H','H','H','H'],
['S','S','S','S','S','H','H','H','H','H'],
['H','H','S','S','S','H','H','H','H','H'],
['D','D','D','D','D','D','D','D','D','D'],
['D','D','D','D','D','D','D','D','H','H'],
['H','D','D','D','D','D','H','H','H','H'],
['H','H','H','H','H','H','H','H','H','H'],
['H','H','H','H','H','H','H','H','H','H'],
['H','H','H','H','H','H','H','H','H','H'],
['H','H','H','H','H','H','H','H','H','H'],
['H','H','H','H','H','H','H','H','H','H']]

	def loadStrategyTable(self):	
		try:
			fp=open('strategytable.txt','r')
			self.strategyData.clear()
			while True:
				line = fp.readline()
				if not line:
					break
				line=line[:-1]
				x=line.split(' ')
				self.strategyData.append(x)
			self.hasStrategyTable=True
			self.startOfStrategyTable=4
			self.endOfStrategyTable=27
		except:
			self.hasStrategyTable=False
		
	def getStrategy(self,playerhand,dealerhand):

		if self.beststrategy:
			x=playerhand.get_value()
			y=dealerhand.get_value()
			if x<self.startOfStrategyTable:
				x=self.startOfStrategyTable
			else:
				x=self.endOfStrategyTable-x
			y-=2
			result=self.strategyData[x][y]
			if result=='D':
				if (playerhand.get_count()!=2):
					result='H'
		else:

			if playerhand.get_value()<17 :
				if (playerhand.get_value()==11) and (playerhand.get_count()==2):
					result='D'
				else:
					result='H'
			else:
				result='S'
		return result





