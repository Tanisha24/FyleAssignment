import psycopg2
hostname = '127.0.0.1'
username = 'tanisha'
password = 'root'
database = 'bankdb'

# Simple routine to run a query on a database and print the results:
# Fetch Bank details on the basis of IFSC
def doQueryOnIfsc( conn , ifsc) :
    cur = conn.cursor()
    cur2=conn.cursor()
    cur.execute( "SELECT * FROM branches WHERE ifsc=\'"+ifsc+"\'" )
    for ifsc, bankid, branch, address, city, district, state in cur.fetchall() :
        cur2.execute( "SELECT * FROM banks WHERE id="+str(bankid ))
        for name,id in cur2.fetchall():
            bank=name
        jsonData={
        'ifsc':ifsc,
        'bank':bank,
        'id' : id,
        'branch':branch,
        'address':address,
        'city':city,
        'district':district,
        'state' : state
        }
        print( id, name)
    return jsonData

def doQuery2( conn ) :
    cur = conn.cursor()
    cur.execute( "SELECT * FROM branches" )
    c=0
    jsonData={}
    for ifsc, bankid, branch, address, city, district, state in cur.fetchall() :
        print (ifsc, bankid, branch, address, city, district, state)
        c=c+1
        dict={
        'ifsc':ifsc,
        'bankid':bankid,
        'branch':branch,
        'address':address,
        'city':city,
        'district':district,
        'state' : state
        }
        jsonData[c]=dict
    return jsonData

def doQuery( conn ) :
    cur = conn.cursor()
    cur.execute( "SELECT * FROM banks" )
    c=0
    jsonData={}
    for name,id in cur.fetchall() :
        c=c+1
        print (name,id)
        dict={
        'name':name,
        'id':id
        }
        jsonData[c]=dict
    return jsonData

# Fetch Bank details on the basis of IFSC
def getBankFromIfsc(ifsc):
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    jsonData=doQueryOnIfsc( myConnection, ifsc )
    doQuery2( myConnection )
    myConnection.close()
    return jsonData

# Fetch Bank details on the basis of Bank and City
def getDetailsFromBankAndCity(bank,city):
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    jsonData=doQueryOnBankAndCity( myConnection, bank,city )
    myConnection.close()
    return jsonData

def doQueryOnBankAndCity( conn,bank,city ) :
    cur = conn.cursor()
    cur2=conn.cursor()
    cur.execute( "SELECT * FROM banks WHERE name=\'"+bank+"\'" )
    jsonData={}
    c=0
    for name,id in cur.fetchall() :
        cur2.execute("SELECT * from branches WHERE bank_id="+str(id) +" AND city=\'"+city+"\'")
        for ifsc, bankid, branch, address, city, district, state in cur2.fetchall() :
            c=c+1
            # print (ifsc, bankid, branch, address, city, district, state)
            dict={
            'ifsc':ifsc,
            'bank':bank,
            'branch':branch,
            'address':address,
            'city':city,
            'district':district,
            'state' : state
            }
            print(dict)
            print(".............................................................................")

            jsonData[c]=dict
            print(jsonData)
        print (id,name)
    print(jsonData)
    return jsonData


def getAllBanks():
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    jsonData=doQuery( myConnection )
    myConnection.close()
    return jsonData

def getAllBranches():
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    jsonData=doQuery2( myConnection )
    myConnection.close()
    return jsonData
