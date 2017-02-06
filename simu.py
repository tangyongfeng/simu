#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

__author__ = 'tangyongfeng'
import json
import datetime
import threading
import os,errno
import configfile
import zhongcaiweiyou
import strategytable
from poker import *


_DEBUG_=False
_DEEP_DEBUG_=False

class Financial:
	def __init__(self):
		self.CoinBlance=0	
		self.DiamondBlance=0
		self.startCoinBlance=0
		self.stake=0
		self.level=0
		self.round=0
		self.stage=0
		self.accountList=[]
		self.awardList=[]
	def pocketIt(self,award):
		self.CoinBlance-=self.stake
		self.CoinBlance+=award
	def nextRound(self,strategy,score,award):
		result= self.round,strategy,score,self.stake,award,self.CoinBlance
		if _DEBUG_:
			print (result)
		self.accountList.append(result)
		self.awardList.append(award)
		self.round+=1
	def getStage(self):
		#import numpy as np
		#mean=np.mean(self.awardList)
		#var=np.var(self.awardList)
		#std=np.std(self.awardList)
		#median=np.median(self.awardList)

		#stage_info='%d,%f,%f,%f,%f,%d'%(self.stage,mean,median,var,std,self.stake)
		stage_info=''
		self.accountList=[]
		self.awardList=[]
		self.stage+=1
		return stage_info
class Player:
	def  __init__(self):
		self.uid=0
		self.appid=0
		self.fristHand=Hand()
		self.dealerhand=Hand()
		self.financial=Financial()

class Loging:
	def __init__(self,userid,session_log,detail_log,break_log,stage_log):
		path='.//log//'+str(userid)
		self.makedir(path)

		self.logfilename=path+'//'+datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")

		self.sessionId=1
		self.detail_Log=detail_log
		self.session_Log=session_log
		self.break_Log=break_log
		self.stage_Log=stage_log
		if self.detail_Log:
			self.detailfile=open(self.logfilename +'.detail.txt','w')
		if self.session_Log:
			self.sessionfile=open(self.logfilename+'.session.txt','w')
		if self.break_Log:
			self.breakfile=open(self.logfilename+'.break.txt','w')
		if self.stage_Log:
			self.stagefile=open(self.logfilename+'.stage.txt','w')
			self.stagefile.write('stage,mean,median,var,std,stake')
			self.stagefile.write('\n')
			self.stagefile.flush()
	def __del__(self):
		if self.detail_Log:
			self.detailfile.close()
		if self.session_Log:
			self.sessionfile.close()
		if self.break_Log:
			self.breakfile.close()
		if self.stage_Log:
			self.stagefile.close()
	def makedir(self,path):
		os.makedirs(path,exist_ok=True)

	def detaillog(self,buf):
		self.detailfile.write(str(self.sessionId)+','+datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")+','+buf)
		self.detailfile.write('\n')
	def sessionlog(self,buf):
		self.sessionfile.write(str(self.sessionId)+','+datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")+','+buf)
		self.sessionfile.write('\n')

		self.sessionfile.flush()
		try:

			self.detailfile.write('\n')
			self.detailfile.flush()
		except:
			pass
		self.sessionId+=1

	def breaklog(self,buf,compare):
		self.breakfile.write(str(self.sessionId)+','+datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")+','+buf+','+compare)
		self.breakfile.write('\n')
		self.breakfile.write('\n')
		self.breakfile.flush()
	def stagelog(self,stagemessage):
		self.stagefile.write(stagemessage)
		self.stagefile.write('\n')
		self.stagefile.flush()

	def configDescription(self,config):
		if hasattr(config,'best_strategy'):
			result='best strategy:'+str(config.best_strategy)
		if hasattr(config,'has_double'):
			result+='has double:'+str(config.has_double)
		if hasattr(config,'native_black_return'):
			result+='native_black_return:'+str(config.native_black_return)
		if hasattr(config,'has_split'):
			result+='has_split:'+str(config.has_split)
		result+='\n'
		self._config=config

		return result
 
		
		



class Simuclient(threading.Thread):
	

	def __init__(self,userid):
		threading.Thread.__init__(self)
		
		self.starttime=datetime.datetime.now()
		self.config=configfile.ConfigFile().userconfig(userid)
		
		self.uid=userid
		self.win=0
		self.lost=0
		self.push=0

		self.net=zhongcaiweiyou.zhongcaiweiyou()
		self.player=Player()
		self.strategy=strategytable.Strategy(self.config.best_strategy)
		self.loging=Loging(userid,self.config.session_log,self.config.detail_log,self.config.break_log,self.config.stage_log)
		self.loging.sessionlog(self.config)


	def __del__(self):
		try:
			if self.net._connected:
				self.net.disconnect()
		except:
			pass
	def run(self):
		self.player_action()
		
	def deal(self,stake):
		self.player.bust=False
		if (self.player.financial.CoinBlance>100):
			self.player.fristHand,self.player.dealerhand= self.net.deal(stake)
		else:
			self.roundState='OUTOFMONEY'
			if _DEBUG_:
				print ("insufficient blance")

	def hit(self):
		a,b=self.net.hit()
		if a.get_count()>0:
			self.player.fristHand=a
		if b.get_count()>0:
			self.player.dealerhand=b

	def double(self):
		a,b=self.net.double()
		if a.get_count()>0:
			self.player.fristHand=a
		if b.get_count()>0:
			self.player.dealerhand=b

	def stand(self):
		a,b=self.net.stand()
		if a.get_count()>0:
			self.player.fristHand=a
		if b.get_count()>0:
			self.player.dealerhand=b

	def login(self,userid,appid):
		self.player.financial.CoinBlance= self.net.login(userid,appid)
		if _DEBUG_:
			print ('in simu login')
			print("player blance ",self.player.financial.CoinBlance)
		self.player.financial.startCoinBlance=self.player.financial.CoinBlance
		return self.player.financial.CoinBlance
		
		
	def getJudgment(self,playerhand,dealerhand,stake):
		self.roundState='DEAL'
		award=0
		if playerhand.get_value()>21:
			result= 'DEALER_WIN'
			if _DEEP_DEBUG_:
				print (result)
			self.lost+=1
			award=0
		elif dealerhand.get_value()>21:
			self.win+=1
			result= 'PLAYER_WIN'
			if _DEEP_DEBUG_:
				print (result)
			self.win+=1
			award=stake*2
		elif (playerhand.get_count()==2) and (playerhand.get_value()==21):
			result= 'PLAYER_BLACKJACK'
			if _DEEP_DEBUG_:
				print (result)
			self.win+=1
			award=stake*self.config.native_black_return

		elif playerhand.get_value()>dealerhand.get_value():
			result= 'PLAYER_WIN'	
			if _DEEP_DEBUG_:
				print (result)
			self.win+=1
			award=stake*2
		elif playerhand.get_value()<dealerhand.get_value():
			result= 'DEALER_WIN'	
			if _DEEP_DEBUG_:
				print (result)
			self.lost+=1
			award=0
		elif playerhand.get_value()==dealerhand.get_value():
			result= 'PUSH'	
			if _DEEP_DEBUG_:
				print (result)
			self.push+=1
			award=stake

		self.updateBlance(stake,award)
		return result,award

	def updateBlance(self,stake,award):
		self.player.financial.pocketIt(award)
	def detailMaker(self,playerhand,dealerhand,roundstate,strategy,winer):
		detailstr=str(playerhand.get_value())+':'
		detailstr+=str(dealerhand.get_value())+ ','
		detailstr+=str(playerhand)+','
		detailstr+=str(dealerhand)+','
		detailstr+=str(roundstate)+','
		detailstr+=str(strategy)+','
		detailstr+=str(winer)+','
		detailstr+=str(self.player.financial.CoinBlance)+','
		detailstr+=str(self.player.financial.stake)

		if _DEBUG_ :
			print (detailstr)
		if self.config.detail_log:
			self.loging.detaillog(detailstr)

	def  roundVerify(self,strategy,winer,award):
		result= "%s:%s,%s:%s,%s,%s,%d,%d,%d"%(self.player.fristHand.get_value(),self.player.dealerhand.get_value(),self.player.fristHand,self.player.dealerhand,strategy,winer,self.player.financial.CoinBlance,self.player.financial.stake,award)
		if self.config.session_log:
			self.loging.sessionlog (result)
		if self.config.break_log:
			blance,level =self.net.parseMessageToFinancial(self.net.lastMessage)
			if blance != self.player.financial.CoinBlance:
				self.loging.breaklog(result,str(self.net.lastMessage))
				if self.config.error_break:
					print ('error break')
					print (self.net.lastMessage)
					print (result)
					input()
				self.player.financial.CoinBlance=blance

		self.player.financial.nextRound(strategy,'%d:%d'%(self.player.fristHand.get_value(),self.player.dealerhand.get_value()),award)

		if ((self.player.financial.round % self.config.stage_size)==0) :
			result=self.player.financial.getStage()
			if self.config.stage_log:
				self.loging.stagelog(result)
			if(self.player.financial.stake < self.config.stake_end):
				self.player.financial.stake+=self.config.stake_stride
	

	def player_action(self):
		self.player.uid=self.uid
		self.player.appid=911
		result= self.login(self.player.uid,self.player.appid)
		self.roundState='DEAL'

		self.player.financial.round=0
		self.player.financial.stake=self.config.stake_start
		self.player.financial.startCoinBlance=result
		self.player.financial.CoinBlance=result
		if _DEBUG_ :
			print (self.player.financial.stake,self.player.financial.startCoinBlance,self.player.financial.CoinBlance)
		while(self.player.financial.CoinBlance>100):
			try:
				strategy=''
				winer=''
				if self.roundState=='DEAL':
					roundStake=self.player.financial.stake
					result=self.deal(self.player.financial.stake)
					self.detailMaker(self.player.fristHand,self.player.dealerhand,self.roundState,strategy,winer)

					if self.player.fristHand.get_value()!=21:
						self.roundState='HIT'
					else:
						self.roundState='SETTLE'

				if self.roundState=='HIT':
					strategy=self.strategy.getStrategy(self.player.fristHand,self.player.dealerhand)
					if (strategy=='H') or (strategy=='P'):
						result=self.hit()

						self.detailMaker(self.player.fristHand,self.player.dealerhand,self.roundState,strategy,winer)

						if self.player.fristHand.get_value()<=21:
							self.roundState='HIT'
						else:
							self.roundState='SETTLE'

					elif strategy=='D':
						self.player.financial.stake*=2
						result=self.double()
						
						self.detailMaker(self.player.fristHand,self.player.dealerhand,self.roundState,strategy,winer)
						self.roundState='SETTLE'

						
					elif strategy=='P':
						pass

					elif strategy=='S':
						result=self.stand()
						self.detailMaker(self.player.fristHand,self.player.dealerhand,self.roundState,strategy,winer)
						self.roundState='SETTLE'

				if self.roundState=='SETTLE':
					winer,award=self.getJudgment(self.player.fristHand,self.player.dealerhand,self.player.financial.stake)

					self.detailMaker(self.player.fristHand,self.player.dealerhand,self.roundState,strategy,winer)
					self.roundVerify(strategy,winer,award)
					self.player.financial.stake=roundStake

			except IOError as e:
				print (e)


					
















def main():
	config=configfile.ConfigFile()


	cli=[]
	start_uid=config.mainconfig.start_user_id
	end_uid=config.mainconfig.end_user_id

	for i in range(start_uid,end_uid+1):
		cli.insert((i-start_uid),Simuclient(i))
		cli[i-start_uid].start()
		print ('simu thread ' ,i,' Started')
	print("go go go!")



if __name__ == "__main__":
    main()
