from collections import defaultdict
import json
def tree(): return defaultdict(tree)
session_config =tree()

session_config['main']['start_user_id']=911
session_config['main']['end_user_id']=911

session_config['default']['session_log']=True
session_config['default']['detail_log']=False
session_config['default']['break_log']=True
session_config['default']['error_break']=False
session_config['default']['stake_start']=10
session_config['default']['stake_end']=1000000
session_config['default']['stake_steps']=2000         
session_config['default']['stake_stride']=1000
session_config['default']['best_strategy']=True
session_config['default']['has_double']=True
session_config['default']['native_black_return']=2.5
session_config['default']['has_split']=False
session_config['default']['verify_coin_blance']=True
session_config['default']['verify_level']=False





session_config['911']['detail_log']=False

session_config['500']['detail_log']=False

def saveconfig():
    with open('simu.json', 'w') as f:
        json.dump(session_config, f, indent=4)
    f.close()
if __name__=='__main__':
    saveconfig()
