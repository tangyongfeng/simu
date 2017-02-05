import json


class ConfigFile:
	def __init__(self):
		with open('simu.json','r') as f:
			self._config = json.load(f)
		f.close()
		self._mainconfig=self._config['main']
		self._defconfig=self._config['default']
		self._sessionconfig=[]
		for i in range(self._mainconfig["start_user_id"],self._mainconfig["end_user_id"]+1):
			self._sessionconfig.insert(i-self._mainconfig["start_user_id"],self._defconfig.copy())
			if '%d'%i in self._config:
				for v in self._config['%d'%i]:
					self._sessionconfig[i-self._mainconfig["start_user_id"]][v]=self._config['%d'%i]['%s'%v]
			self._sessionconfig[i-self._mainconfig["start_user_id"]]['user_id']=i
		self.mainconfig=self.obj_dict(self._mainconfig)
		self.defconfig=self.obj_dict(self._defconfig)
	def userconfig(self,user_id):
		if (user_id>=self.mainconfig.start_user_id) and (user_id <=self.mainconfig.end_user_id):
			return self.obj_dict(self._sessionconfig[user_id-self.mainconfig.start_user_id])
		
	def saveConfig(self):
		with open('simu.json','w') as f:
			json.dump(self._config,f,indent=4)
		f.close()

	def obj_dict(self,d):
		top=type('new',(object,),d)
		seqs = tuple,list,set,frozenset
		for i,j in d.items():
			if isinstance(j,dict):
				setattr(top,i,obj_dict(j))
			elif isinstance(j,seqs):
				setattr(top,i,type(j)(obj_dict(sj) if isinstance(sj, dict) else sj for sj in j))		
			else:
				setattr(top,i,j)
		return top


