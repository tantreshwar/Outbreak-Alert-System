import pymysql
connection=pymysql.connect(host="localhost",user="root",passwd="Tantra123",db='disease')
cursor=connection.cursor()

# Patient data class
class node:
    def __init__(self,name=None,ids=None):
        self.name=name
        self.id=ids
        self.next=None

#initialises database count records to NULL
def initdatabase():
    sql=("Update Disease_Record set Red=NULL")
    cursor.execute(sql)
    connection.commit()
    sql=("Update Disease_Record set Green=NULL")
    cursor.execute(sql)
    connection.commit()


# Maps area with their corresponding hashing index 
def gethindex(area):
    asigner={'Pragati Maidan':0,'New Delhi':1,'Delhi Cantt.':2}
    return asigner.get(area,-1)

# Fills red column of corresponding hashing index(corona positive counts)
def flushreddB(i,hindex):
    if i==1:
        sql=("Update Disease_Record set Red=%d where Hindex=%d"%(i,hindex))
        cursor.execute(sql)
        connection.commit()
        return
    else:
        sql=("Update Disease_Record set Red=Red+1 where Hindex=%d"%(hindex,))
        cursor.execute(sql)
        connection.commit()
        return

# Fills green column of corresponding hashing index(corona recovery counts)
def flushgreendB(hindex):
    sql=("Select Green from Disease_Record where Hindex=%d"%(hindex,))
    cursor.execute(sql)
    s=cursor.fetchall()
    temp=s[0][0]
    if temp==None:
        sql=("Update Disease_Record set Green=%d where Hindex=%d"%(1,hindex))
        cursor.execute(sql)
        connection.commit()
        return
    else:
        sql=("Update Disease_Record set Green=Green+1 where Hindex=%d"%(hindex,))
        cursor.execute(sql)
        connection.commit()
        return
    
# Finds the last element from link list
def lastele(ele):
    if ele.next==None:
        return ele
    else:
        lastele(ele.next)

# Patient input data asking function
def getdata(idp):
    area=input('Enter the area:')
    hindex=gethindex(area)
    if hindex==-1:
        print('Invalid Entry!!')
        return 0
    name=input('Enter the name:')
    ele=node(name,idp)
    if (hlist[hindex]==None):
        hlist[hindex]=ele
        flushreddB(1,hindex)
        return ele
    else:
        flushreddB(0,hindex)
        lastele(hlist[hindex]).next=ele

#search the patient particulars from the list stored by hashing index
def search(vals,bas):
    if bas==None:
        return 
    if bas.next!=None and bas.next.id==vals:
        return bas
    else:
        return(search(vals,bas.next))
    
#remove the patient particulars from the list stored by hashing index
def removedata(hindex,idp):
    if idp==hlist[hindex].id:
        temp=hlist[hindex]
        hlist[hindex]=hlist[hindex].next
        flushgreendB(hindex)
        del temp
        return
    targ=search(idp,hlist[hindex])
    if targ==None:
        return
    flushgreendB(hindex)
    temp=targ.next
    targ.next=targ.next.next
    del temp
    
#prints the list for a particular hashing index
st=" "
def prtlist(n):
    global st
    if n==None:
        return
    else:
        st=st+str(n.id)
        prtlist(n.next)
        return st

#prints all the list from each hashing index
def printdata():
    global st
    for i in range(3):
        st=" "
        print(prtlist(hlist[i]))




if __name__=="__main__":
    hlist=[]    #Stores the base pointers of all hashing index
    
    #initialises the base pointers of all hashing index to none
    for i in range(3):
        hlist.append(None)
    initdatabase()  #initialises the database count records to null
    power=1         #power is variable which when set to zero,the Hashdata file will seize
    idp=0	    #patient id
    
    while power:
        entryexch=int(input('New Admission press 1 for discharge press 2:')) #choice for admission to hospital or discharge
        if entryexch==1:
            idp=idp+1
            getdata(idp)    #input for patient admission
            print("Patient id:%d"%(idp,))
        elif entryexch==2:
            ar=input('Enter the area:')
            hindex=gethindex(ar)
            ids=int(input('Enter patient id:'))
            removedata(hindex,ids)  #data removal of particular patient record by hashing index
        power=int(input('To continue in the system press 1 else 0'))
    printdata() #whole data of hashtable
    connection.close()
