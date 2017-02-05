import requests
import json
import poker
from poker import *
_DEEP_DEBUG_=False
from remote import *	

class zhongcaiweiyou:
	_connected=False
	def __init__(self):
		self.cookies={}
		self.lastMessage=''
		

	def  heartbeat(self):
		source= self.source_url+self.source_heartbeat
		hb=self.getit(source,'')

		self._connected=True
		if _DEBUG_:
			print (hb['time'])
			print (hb['version'])


	def  disconnect(self):
		todo=2
		
			
	def  getit(self,source,pay_load):
		if _DEEP_DEBUG_:
			print('in getit')
			print (source,pay_load)
		try:
			r=requests.get(source ,params=pay_load,cookies=self.cookies)
			self.cookies=r.cookies;
			
			if (r.status_code ==200):
				self._connected=True
				return  json.loads(r.text)
		except  IOError as e:
			return {'__get__status':'000099'}




	def login(self,userid,appid):
		source=source_url+source_action_head+source_login
		
		logininfo=self.getit(source,{'fbuid':userid, 'appId':appid})
		if (logininfo['errcode']=='000000'):
			return logininfo['coin']
		else:
			return 0
		
	def deal(self,betCoins):
		source=source_url+source_action_head+source_deal
		dealinfo=self.getit(source,{"betCoins":betCoins})
		if _DEEP_DEBUG_:
			print ('in middle layer,deal')
			print (dealinfo)
			print ('parseMessageToFinancial',self.parseMessageToFinancial(dealinfo))
		return self.parseMessageToCard(dealinfo)



	def hit(self):
		source=source_url+source_action_head+source_hit

		hitinfo=self.getit(source,{})
		if _DEEP_DEBUG_:
			print ('in middle layer,hit')
			print (hitinfo)
		return self.parseMessageToCard(hitinfo)

	def double(self):
		source=source_url+source_action_head+source_double

		doubleinfo=self.getit(source,{})
		if _DEEP_DEBUG_:
			print ('in middle layer,double')
			print (doubleinfo)
		return self.parseMessageToCard(doubleinfo)
	def stand(self):
		source=source_url+source_action_head+source_stand
		dealerCard=[]

		standinfo=self.getit(source,{})
		if _DEEP_DEBUG_:
			print ('in middle layer,stand')
			print (standinfo)
		return self.parseMessageToCard(standinfo)

	def parseMessageToFinancial(self,inMessage):
		level=0
		coinblance=0
		
		if 'totalCoins' in inMessage:
			coinblance=inMessage['totalCoins']


		return coinblance,level

	def parseMessageToCard(self,inMessage):
		dealerhand=Hand()
		playerhand=Hand()
		fewCardOfPlayer=0
		fewCardOfDealer=0

		if ('player' in inMessage):
			fewCardOfPlayer=len(inMessage['player'])

		if ('dealer' in inMessage):
			fewCardOfDealer=len(inMessage['dealer'])

		if _DEEP_DEBUG_:
			print('player hand size',fewCardOfPlayer)
			print('dealer hand size',fewCardOfDealer)
		for i in range(0,fewCardOfPlayer):
			playerhand.add_card(self.readcard(inMessage['player'][i]))
		for i in range(0,fewCardOfDealer):
			dealerhand.add_card(self.readcard(inMessage['dealer'][i]))
		self.lastMessage=inMessage
		return playerhand,dealerhand

	def readcard(self,inhand):
		card=Card(SUITS[inhand['id']//13],RANKS[inhand['id']%13])
		return card
		
