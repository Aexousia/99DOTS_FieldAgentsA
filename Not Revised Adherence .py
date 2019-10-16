#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import queue
import copy
import matplotlib.pyplot as plt
import pylab as plt

final1=[]  #to store the steady state waiting time for different patient counts
final2=[]  #to store the steady state queue length for different patient counts

for pc in range(1,400):  #number of patients=pc
    task1=[]            #stores waiting time values for different sample paths
    task2=[]            #stores queue length values for different sample paths
    
    for pcm in range(1):  #taking 10 sample paths
        list1=[] #keeps a track of days spent by every patient who ever enters the simulation
        value=[]  #keeps a track of average waiting time after every day
        value1=[] #keeps a track of average queue length after every day
        sum3=0
        sum4=0
        
        total_time = 4000        #number of days for which simulation runs
        ST_rate = 1/4         #Service Rate
        num_total = pc       #number of patients in the simulation 
        m= pc/100       #Little's Law
        IAT_rate=1/m       #Inter-Arrival Rate

        thresh = 3      #After 'thresh' consecutive misses, the patient enters the queue of field officers' visit target
        addh = 0.55      #average adherence of the region
        P_miss_Add = 0.78  #P(Person missing the missed call|He is adherent). Experimental Value
        P_miss_noAdd = 0.93 #P(Person missing the missed call|He is not adherent). Experimental Value
        p_th=0.847   #After this P(miss), a person is said to have missed medication that day with confirmation
        abc1=0

        qu = queue.Queue()  #Queue that stores the list of patients who need a visit
        curr= None

        wait_time = []   #list that stores how much each patient had to wait in total
        server_busy = False  #keeps a track of server's occupancy
        d=0

        P_miss = []  #a list of P(miss) of every patient who has ever been in simulation
        P_add = [] #a list of adherence of every patient who has ever been in simulation
        miss_days_1=[] #last day's record of missed days by all patients who are in simulation
        miss_days = []  #todays' record of missed days by all patients who are in simulation (appends only if consecutive)
        Simul_me= [] #list of patients who have crossed the threshold and will be visited 
        len1=[]
    
        for k in range(400000):  #just initializing
            miss_days_1.append(0)
            miss_days.append(0)
            wait_time.append(0)
            
        for k in range(total_time):  #Simulation Starts
            Simul_me=[]
            a1=np.random.poisson(1/IAT_rate) #number of patients who enter the system today
            a2=np.random.poisson(1/ST_rate)  #number of patients who will be visited today
            for i in range(a1): #Everyone who has just entered has spent zero days in simulation
                list1.append(0)
                
            for i in range(a1): #appending so that we can use the indexes later
                temp = np.random.binomial(a1,addh)/a1
                P_add.append(temp)
                P_miss.append(P_miss_Add*P_add[i]+ P_miss_noAdd*(1-P_add[i]))
                
            l=0
            for i in range(len(list1)): #calculating number of people who are still active (haven't completed 100 day treatment)
                if(list1[i]<100):
                    l=l+1
                    
            for i in range(len(list1)):  #Assigning fresh P(add) by binomial distribution and hence P(miss) to everyone undergoing treatment
                if(list1[i]<100 and l>0):
                    temp = np.random.binomial(l,addh)/l  
                    P_add[i]= temp
                    P_miss[i]=P_miss_Add*P_add[i]+ P_miss_noAdd*(1-P_add[i])
                     
            for i in range(len(list1)): #Increasing the days spent in simulation by 1
                list1[i]=list1[i]+1
            for i in range(len(list1)): #Increasing miss_days if threshold is crossed
                if(P_miss[i]> p_th):
                    if(list1[i]<100):
                        if(miss_days_1[i]>=1): #only if missed days are consecutive, it will count for entry in simulation
                            miss_days[i]= miss_days_1[i]+1
                        if(miss_days_1[i]==0):
                            miss_days[i]=1
                else:
                    if(list1[i]<100): #if today wasn't a miss day, then by consecutive policy, miss_days=0
                        miss_days[i]=0
                        
            for i in range(len(list1)): #Adding everyone who has crossed threshold today into the list Simul_me
                if(miss_days[i]>thresh and list1[i]<100):
                    Simul_me.append(i)
            a= len(Simul_me)
            for j in range(a): #Every new patient who needs attention is added to the queue of pending field visits
                if Simul_me[j] not in qu.queue:
                    qu.put(Simul_me[j])
                    
            b3=0
            b=qu.qsize()
            cb=b
            b2=a2
            if(b<b2):
                b3=b
            if(b>b2):
                b3=b2
            
            for j in range(a2):
                if(b>0 and b2>0): #as long as both, people needing help and available field visits exist, the visits are made
                    curr= qu.get() #first member in the queue is visited
                    miss_days[curr]=0  #after the visit, his miss_days become zero
                    P_add[curr]=1   #after the visit, the patients become fully adherent
                    b=b-1 #reducing needy patients by 1 after the field visit
                    b2=b2-1 #one less field visit available for today
                    d=d+1 #number of visits made
                    
            for item in list(qu.queue): #whoever couldn't be visited today and are still left in the queue
                if(list1[item]<100): #as long as they are still in treatment
                    wait_time[item]=wait_time[item]+1  #they had to wait for one more day
                    
            for i in range(len(list1)): #assigning missed days of today to tomorrow's yesterday
                miss_days_1[i]=miss_days[i]
                
            for i in range(len(list1)): #reinitializing todays'
                miss_days[i]=0
                
            abc1=abc1+b3 #total visits made till now
            sum1=0
            
            for i in range(len(list1)):
                if(list1[i]<100):
                    sum1=sum1+wait_time[i] 
            if(abc1!=0):
                value.append(sum1/abc1) #average waiting time till this day
            if(abc1==0):
                value.append(sum1)
            value1.append(cb) #average queue length
            
        
        for kl in range(len(value)-1000,len(value)-1):   #taking the steady state average for this sample path
            sum3=sum3+value[kl]
        sum3=sum3/1000
        task1.append(sum3)    
         
        for kl in range(len(value1)-1000,len(value1)-1):
            sum4=sum4+value1[kl]
        sum4=sum4/1000
        task2.append(sum4)
        
    sum5=0
    sum6=0
    for i in range(len(task1)):  #averages of all sample paths' steady states
        sum5=sum5+task1[i]
    final1.append(sum5/1)
    
    for i in range(len(task2)):
        sum6=sum6+task2[i]
    final2.append(sum6/1)
    print(pc)
    

plt.plot([i+1 for i in range(0,len(final1))], final1)   #desired graphs of waiting time
plt.ylabel("Avg waiting time")
plt.xlabel("No. of days")
plt.show() 


plt.plot([i+1 for i in range(0,len(final2))], final2)   #desired graph of queue length
plt.ylabel("Avg length of the queue")
plt.xlabel("No. of days")
plt.show()                    


# In[13]:


plt.plot([i+1 for i in range(0,len(final1))], final1)   #value1 is queue length and value is avg wating time
plt.ylabel("Avg waiting time")
plt.xlabel("No. of days")
plt.show() 


plt.plot([i+1 for i in range(0,len(final2))], final2)   #value1 is queue length and value is avg wating time
plt.ylabel("Avg length of the queue")
plt.xlabel("No. of days")
plt.show()  


# In[ ]:




