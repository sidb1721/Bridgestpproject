
from bridge import *

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
                        if(self.bridge_network[i].lan_list_obj[j].bridge_list_obj[k].id!=self.bridge_network[i].id):
                            m=message(self.bridge_network[i].root,self.bridge_network[i].d,self.bridge_network[i].id)
                            m.port_id = self.bridge_network[i].lan_list_obj[j].id
                            if(self.bridge_network[i].lan_list_obj[j].bridge_list_obj[k].port_status[x] != 'NP'):            
                                self.bridge_network[i].lan_list_obj[j].bridge_list_obj[k].receivebuffer.append(m)
                                

    def simulateSTP(self):    
        while 1:
            z=0
            self.forwarding(self.tr,self.t)           
            self.t=self.t+1
            for i in range(len(self.bridge_network)):
                z=z+self.bridge_network[i].receive(self.tr,self.t,0)       
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


tr = int(input())
n = int(input())
bridge_network=[]
lan_network=[]
ul=[]

for i in range(n):
    port_st={}
    lan_l=[]
    string = input()
    for j in range(4,len(string),2):
        lan_l.append(string[j])
        port_st[string[j]] = 'DP'
    bridge1 = bridge(string[1],string[1],0,sorted(lan_l),port_st)
    bridge_network.append(bridge1)    

for i in range (n):
    ul = list(set(bridge_network[i].lan_list)|set(ul))
ul=list(set(ul))
ul=sorted(ul)

for x in ul:
    empty=[]
    for i in range(n):
        if x in bridge_network[i].lan_list:
            empty.append(i)
    lan_network.append(lan(x,empty))
        
for x in ul:
    for i in range(n):
        if x in bridge_network[i].lan_list:
            bridge_network[i].lan_list_obj.append(lan_network[ord(x)-65])

        if i in lan_network[ord(x)-65].bridge_list:
            lan_network[ord(x)-65].bridge_list_obj.append(bridge_network[i])

bsim=bridgesim(bridge_network,lan_network,tr,0)
bsim.simulateSTP()
bsim.final_port_status()

#combine sendbuffer and transmit packet into forwarding using 3 for loops