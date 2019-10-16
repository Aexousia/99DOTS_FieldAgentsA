#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
import queue
import copy
import matplotlib.pyplot as plt
import pylab as plt

final1=[] #to store the steady state waiting time for different patient counts
final2=[] #to store the steady state queue length for different patient counts
realqlen3=[] #the rate of entry of patients into the FO's visit queue
x4=[] #dosing implementation

for pc in range(1,400):  #number of patients=pc
    task1=[]  #stores waiting time values for different sample paths
    task2=[]   #stores average queue length values for different sample paths
    realqlen2=[] #stores the rate of entry of patients into FO's queue for diff. sample paths
    x3=[]  #dosing implementation at steady state for each sample path
    #pc=pct*100
    for pcm in range(10): #taking 10 sample paths
        x1=0
        list1=[] #keeps a track of days spent by every patient who ever enters the simulation
        value=[]  #keeps a track of average waiting time after every day
        value1=[]  #keeps a track of average queue length after every day
        x2=[]
        sum3=0
        sum4=0
        realqlen=[]
        miss_days_x1=[]                  #for counting dosing implementation
        
        total_time = 1000         #number of days for which simulation runs
        ST_rate = 1/4           #Service Rate
        num_total = pc      #number of patients in the simulation
        m= pc/100       #Little's Law
        IAT_rate=1/m    #Inter-Arrival Rate

        thresh = 3  #After 'thresh' consecutive misses, the patient enters the queue of field officers' visit target
        addh = 0.5  #average adherence of the region
        P_miss_Add = 0.78   #P(Person missing the missed call|He is adherent). Experimental Value
        P_miss_noAdd = 0.93 #P(Person missing the missed call|He is not adherent). Experimental Value
        p_th=0.847   #After this P(miss), a person is said to have missed medication that day with confirmation
        abc1=0

        qu = queue.Queue()  #Queue that stores the list of patients who need a visit
        curr= None

        wait_time = []  #list that stores how much each patient had to wait in total
        server_busy = False  #keeps a track of server's occupancy
        d=0

        P_miss = [] #a list of P(miss) of every patient who has ever been in simulation
        P_add = [] #a list of adherence of every patient who has ever been in simulation
        miss_days_1=[] #last day's record of missed days by all patients who are in simulation
        miss_days = [] #todays'  record of missed days by all patients who are in simulation (appends only if consecutive)
        Simul_me= []  #list of patients who have crossed the threshold and will be visited 
        len1=[]
    
            
      
        
        visited=[]                        #holds list1 index of people where field visit has been made
        for k in range(total_time): #Simulation starts here
            Simul_me=[] #Stores a list of people where visit must be made
            a1=np.random.poisson(1/IAT_rate) #number of people who enter the treatment today
            a2=np.random.poisson(1/ST_rate) #number of field visits that the FO can make today
            for i in range(a1): #all the people who have just entered the system will be given a place in all these lists
                list1.append(0)
                miss_days_x1.append(0)
                miss_days.append(0)
                wait_time.append(0)
                miss_days_1.append(0)
                P_add.append(0)
                P_miss.append(0)
                
            l=0
            for i in range(len(list1)):    #calculating total number of patients undergoing treatment currently
                if(list1[i]<100):
                    l=l+1
                    
            for i in range(len(list1)): #assigning P_miss
                if(list1[i]<100 and l>0):  #as long as the patient is currently going treatment
                    temp = np.random.binomial(l,addh)/l   
                    P_add[i]= temp                       #assigning P_add binomially
                    P_miss[i]=P_miss_Add*P_add[i]+ P_miss_noAdd*(1-P_add[i]) #assigning P_miss based on this relation
                for j in range(len(visited)): #if someone have been visited previously, that person becomes completely adherent
                    if(visited[j]==i and list1[i]<100):
                        P_add[i]=1
                        P_miss[i]=P_miss_Add
                        
                
                    
            for i in range(len(list1)):  #days spent in the simulation increase by 1
                list1[i]=list1[i]+1
            for i in range(len(list1)): #calculating missed days
                if(P_miss[i]> p_th):  #if they have crossed the threshold probability of missing
                    if(list1[i]<100): #if active in treatment
                        miss_days_x1[i]=miss_days_x1[i]+1 #total missed days of every patient
                        x1=x1+1 #total patient miss days
                        if(miss_days_1[i]>=1): 
                            miss_days[i]= miss_days_1[i]+1  #calculating consecutive misses
                        if(miss_days_1[i]==0):
                            miss_days[i]=1           
                else:       
                    if(list1[i]<100):
                        miss_days[i]=0
             
            fab=0
            for i in range(len(list1)): #adding everyone who has missed threshold into a list
                if(miss_days[i]>thresh and list1[i]<100):
                    Simul_me.append(i)
                    fab=fab+1
            
            
            a= len(Simul_me)
            realqlen.append(fab) #new people who area bout to enter the list of the FO
            for j in range(a):
                if Simul_me[j] not in qu.queue:
                    qu.put(Simul_me[j])    #people entering the queue
                    
            b3=0
            b=qu.qsize()
            cb=b
            b2=a2
            if b<=b2:
                b3=b
            else:
                b3=b2   #b3 are the number of patients who will get the treatment
            
            
            for j in range(a2):
                if(b>0 and b2>0): #visits will be made as long as there are people needing the visit and availablility of visit BOTH
                    curr= qu.get() #first member of the queue visited
                    visited.append(curr) #adding the index of the visited patient into the list 'visited'
                    #print(curr)
                    miss_days[curr]=0 #reinitialising it's consecutive missed days
                    P_add[curr]=1  #after the visit, the adherence becomes 1
                    b=b-1 #people needing field visit decrease by 1
                    b2=b2-1  #field visits available decrease by 1
                    d=d+1 #total visits made today
                    
            for item in list(qu.queue): #everyone who couldn't be visited has 1 day added to the waiting time
                if(list1[item]<100):
                    wait_time[item]=wait_time[item]+1
                    #miss_days_x1[item]=miss_days_x1[item]+1
                    
            for i in range(len(list1)): # shifting todays missed days to tomorrow's yesterday missed days and reinitializing
                miss_days_1[i]=miss_days[i]
                miss_days[i]=0
                
                
            abc1=abc1+b3 #total field visits made till today
            sum1=0
 
            for i in range(len(list1)):
                if(list1[i]<100):
                    sum1=sum1+wait_time[i]
            if(abc1!=0):
                value.append(sum1/abc1) #average waiting time till now
            if(abc1==0):
                value.append(0)

            value1.append(cb)  #average queue length till now
            
            sumx1=0
            c=0
            for i in range(len(list1)):  #c is the total patient days
                if(list1[i]>100):
                    c=c+100
                if(list1[i]<100):
                    c=c+list1[i]
            for i in range(len(list1)):
                sumx1=sumx1+miss_days_x1[i]
            if(c!=0):
                x2.append(1-(sumx1/c))   #dosing implementation
            if(c==0):
                x2.append(0)
            
            #print(list1)
            #print(miss_days_x1)
            #print(miss_days_1)
            #print(visited)
            #print(P_add)
            #print(' ')
            
                
        
        
    
        print(pc)

        
        
        
        ohk=0
        for i in range(len(realqlen)-200,len(realqlen)-1):  #taking steady state values in all these cases
            ohk=ohk+realqlen[i]
        realqlen2.append(ohk/200)
        sumx2=0

        for kl in range(len(x2)-200,len(x2)-1):
            sumx2=sumx2+x2[kl]
        sumx2=sumx2/200
        x3.append(sumx2)     

        
        
        for kl in range(len(value)-200,len(value)-1):
            sum3=sum3+value[kl]
        sum3=sum3/200
        task1.append(sum3)    
         
        for kl in range(len(value1)-200,len(value1)-1):
            sum4=sum4+value1[kl]
        sum4=sum4/200
        task2.append(sum4)
        

    x4.append(sum(x3)/len(x3))  #taking avg of different sample paths
    final1.append(sum(task1)/len(task1))
    final2.append(sum(task2)/len(task2))
    realqlen3.append(sum(realqlen2)/len(realqlen2))
     
        
    
    
    
    #print(pc)
    #print(' ')
    

plt.plot([i+1 for i in range(0,len(final1))], final1)   #final graphs against patient numbers of average waiting time
plt.ylabel("Avg waiting time")
plt.xlabel("No. of patients")
plt.show() 


plt.plot([i+1 for i in range(0,len(final2))], final2)   #final graphs against patient numbers of average queue length
plt.ylabel("Avg length of the queue")
plt.xlabel("No. of patients")
plt.show()                    


# In[7]:


plt.plot([i+1 for i in range(0,len(final1))], final1)   #value1 is queue length and value is avg wating time
plt.ylabel("Avg waiting time")
plt.xlabel("No. of patients")
plt.show() 


plt.plot([i+1 for i in range(0,len(final2))], final2)   #value1 is queue length and value is avg wating time
plt.ylabel("Avg length of the queue")
plt.xlabel("No. of patients")
plt.show()                    

#the output below is for one sample path only(to check trend). Advisable to take 10 sample paths


# In[ ]:




