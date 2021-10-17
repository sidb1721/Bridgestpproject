
class message:
    def __init__(self, root, d, sender):
        self.root = root
        self.d = d
        self.sender = sender
        
class lan:
    def __init__(self, id,bridge_list):
        self.id = id
        self.bridge_list = bridge_list
        self.bridge_list_obj = []
    
class bridge:
    def __init__(self, id, root,d,lan_list,port_status):
        self.id = id
        self.root = root
        self.d = d
        self.lan_list = lan_list        #lan_list is a list of char
        self.port_status = port_status  #port_status is a dictionary char to string
        self.lan_list_obj =[]
        self.sendbuffer=[]
        self.receivebuffer=[]
        self.RP_B_id = None
        self.bool=1
        self.count=0
        self.RPcheck=0

    def get_key(self,val,dicty):
        for key, value in dicty.items():
            if val == value:
                return key
        return 0

    def bridge_check(self):
        if 'DP' not in list(self.port_status.values()):
            self.port_status=self.port_status.fromkeys(self.port_status,'NP')

    def receive(self,tr,t):
        for j in range(26):
            #print(self.id)
            for i in range(len(self.receivebuffer)):
                pid=self.receivebuffer[i].port_id
                if (j==ord(pid)-65):
                    if tr==1:
                        print(str(t)+" r"+" B"+str(self.id)+" (B"+str(self.receivebuffer[i].root)+","+str(self.receivebuffer[i].d)+",B"+str(self.receivebuffer[i].sender)+")")

                    if ((self.receivebuffer[i].root<self.root) or (self.receivebuffer[i].root==self.root and (self.d>(self.receivebuffer[i].d +1))) or (self.receivebuffer[i].root==self.root and self.d==self.receivebuffer[i].d +1 and self.RP_B_id>self.receivebuffer[i].sender)):
                        self.bool=1
                        self.root=self.receivebuffer[i].root
                        self.port_status=self.port_status.fromkeys(self.port_status,'DP')
                        self.port_status[pid] = 'RP'
                        self.RP_B_id = self.receivebuffer[i].sender
                        self.d =self.receivebuffer[i].d +1 #remember boolean all dp #make all dp
                                                
                    elif(self.receivebuffer[i].root==self.root and self.port_status[pid] == 'DP' and (self.d>self.receivebuffer[i].d or (self.d==self.receivebuffer[i].d and self.id>self.receivebuffer[i].sender))):
                        self.port_status[pid] = 'NP'   
                        self.bool=1

                    else:
                        self.bool=0

        self.bridge_check()
        self.receivebuffer=[]

class bridgesim:
    def __init__(self,bridge_network,lan_network,tr,t):
        self.bridge_network=bridge_network
        self.lan_network=lan_network
        self.t=t
        self.tr=tr

    def forwarding(self,tr,t):
        for i in range(len(self.bridge_network)):    
            for j in range(len(self.bridge_network[i].lan_list_obj)):
                x=self.bridge_network[i].lan_list_obj[j].id
                if (self.bridge_network[i].port_status[x] == 'DP'):
                    if tr==1:
                        print(str(t)+" s"+" B"+str(self.bridge_network[i].id)+" (B"+str(self.bridge_network[i].root)+","+str(self.bridge_network[i].d)+",B"+str(self.bridge_network[i].id)+")")
                    for k in range(len(self.bridge_network[i].lan_list_obj[j].bridge_list_obj)):   
                        #if (self.bridge_network[i].lan_list_obj[j].bridge_list_obj[k].port_status[x] != 'NP'):               
                            if(self.bridge_network[i].lan_list_obj[j].bridge_list_obj[k].id!=self.bridge_network[i].id):
                                m=message(self.bridge_network[i].root,self.bridge_network[i].d,self.bridge_network[i].id)
                                m.port_id = self.bridge_network[i].lan_list_obj[j].id
                                self.bridge_network[i].lan_list_obj[j].bridge_list_obj[k].receivebuffer.append(m)

    def simulateSTP(self):    
        while 1:
            z=0
            self.forwarding(self.tr,self.t)           
            self.t=self.t+1
            for i in range(len(self.bridge_network)):
                self.bridge_network[i].receive(self.tr,self.t)         
            for j in range(len(self.bridge_network)):
                z+=self.bridge_network[j].bool    
            if(z==0):
               break
    def final_port_status(self):       
        for i in self.bridge_network:
            z=''
            keylist = list(i.port_status.keys())
            keylist=sorted(keylist)
            for j in i.lan_list_obj:
                z = z + str(j.id) + "-" + str(i.port_status[j.id]+' ')
            print('B'+str(i.id)+': '+ z )
