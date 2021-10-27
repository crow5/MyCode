from fastapi import FastAPI
from pydantic import BaseModel

description = """
CA304 - API Calculator by Egor

## Functionality


-The IpCalc function reads in an IP Address and identifies what class it belongs to by testing the ranges.\n 
    If it finds the relateable range to the IP, it can access the information for that class.

-The Subnet function reads in a Mask and an IP address.\n
    Once given it will begin to evaluate to return the data in response to it.

-The Supernet function will ask for a list of addresses which it will proceed to supernet.


## Inputs Description


**All inputs are in JSON form.**

**firstread** - {'address': '136.206.18.7' or 'address': 192.211.1.1'}\n
**secondread** - {'address': '136.206.18.7' and 'mask': 255.255.192.0'}\n
**thirdread** -  {'addresses': ['205.100.0.0','205.100.1.0','205.100.2.0','205.100.3.0']}


## Outputs Description


**All Outputs are in JSON form.**

**firstread** - This function will output the class of the IP, it's networks, hosts, first address and it's last address.\n
**secondread** - This function will output the address CIDR, number of subnets, the hosts, valid subnets, broadcast addresses and first and last addresses.\n
**thirdread** -  This function will output the supernet address with CIDR in string form and it's mask in string form.


## Input - Output


### IpCalc\n
**Input** =\n
    { 'address': '136.206.18.7' }

**Output** =\n 
    'class': 'B',\n
    'num_networks': '16384',\n
    'num_hosts': '65536',\n
    'first_address': '128.0.0.0',\n
    'last_address': '191.255.255.255'

### Subnet\n
**Input** =\n 
    { 'address': '192.168.10.0'\n
    'mask': '255.255.255.192' }

**Output** =\n
    'address_cidr': '192.168.10.0/26',\n
    'num_subnets': '4',\n
    'addressable_hosts_per_subnet': '62',\n
    'valid_subnets': ['192.168.10.0', '192.168.10.64', '192.168.10.128', '192.168.10.192'],\n
    'broadcast_addresses': ['192.168.10.63', '192.168.10.127', '192.168.10.191', '192.168.10.255'],\n
    'first_addresses': ['192.168.10.1', '192.168.10.65', '192.168.10.129', '192.168.10.193'],\n
    'last_addresses':'['192.168.10.62', '192.168.10.126', '192.168.10.190', '192.168.10.254']

### Supernet\n
**Input** =\n 
    { 'addresses': ['205.100.0.0','205.100.1.0','205.100.2.0','205.100.3.0'] }

**Output** =\n 
    'address': '205.100.0.0/22',\n
    'mask': '255.255.252.0'
"""

app = FastAPI(
    title="APICalculator",
    description=description,
    version="0.1.0"
)

#IPCALCULATOR
class IpCalc(BaseModel):
    address: str 

    #Using BaseModel function from pydantic to recognise json.

@app.post("/ipcalc")
def firstrequest(info: IpCalc):
    result = info.address.split(".")
    return lastandfirst(result)

    #Setting up the first post request which will allow for a response.

def lastandfirst(result):
    if (int(result[0]) >= 0 and int(result[0]) <= 127):
        return{
	"class": "A",
	"num_networks": 127,
	"num_hosts": 16777214,
	"first_address": "1.0.0.0",
	"last_address": "127.255.255.255"
}
    elif (int(result[0]) >= 128 and int(result[0]) <= 191):
        return{
	"class": "B",
	"num_networks": 16384,
	"num_hosts": 65536,
	"first_address": "128.0.0.0",
	"last_address": "191.255.255.255"
}
    elif (int(result[0]) >= 192 and int(result[0]) <= 223):
        return{
	"class": "C",
	"num_networks": 2097152,
	"num_hosts": 254,
	"first_address": "192.0.0.0",
	"last_address": "223.255.255.255"
}
    elif (int(result[0]) >= 224 and int(result[0]) <= 239):
        return{
	"class": "D",
	"num_networks": "N/A",
	"num_hosts": "N/A",
	"first_address": "224.0.0.0",
	"last_address": "239.255.255.255"
}
    else:
        return{
	"class": "E",
	"num_networks": "N/A",
	"num_hosts": "N/A",
	"first_address": "240.0.0.0",
	"last_address": "255.255.255.254"
}

    #Checking the ranges of the IP to match the data type, then returns it.

#SUBNETTING
class Subnet(BaseModel):
    address: str
    mask: str

    #Identifying json.

@app.post("/subnet")
def secondread(name: Subnet):
    result = name.address.split(".")
    sub = name.mask.split(".")
    return subnet(sub, result)

    #Reading in inputs into post request.

def getbinary(sub):
    decimal_list = []
    binary_list = []
    for num in sub:
        decimal_list.append(bin(int(num)))
    for digit in decimal_list:
        s ="00000000"
        word = digit[2:]
        s = s[:-abs(len(word))]
        s = s + word
        binary_list.append(s)
    return ".".join(binary_list)

    #Takes a list of string decimals where max number is 255 and returns an IP string in binary. 
    # My mind works in many ways. XD

def subnet(sub, result):
    mask = getbinary(sub)
    ipstring = ".".join(result)
    hosts = (2 ** (mask.count("0")) - 2)
    if hosts == -1:
        hosts = 0
    cidr = mask.count("1")
    binarymask = mask.split(".")
    numsubnets = 0

    #Creating variables that will be useful or have an answer already.

    for digit in binarymask:
        if digit.count("1") == 8:
            pass
        elif int(digit) > 0:
            numsubnets = digit.count("1")
            numsubnets = (2 ** numsubnets)
        elif int(digit) == 0:
            pass

    #Using the 2^n formula to calculate number of subnetworks through host bits.
    
    intiplist = []
    for number in result:
        intiplist.append(int(number))

    #Creating variables that will be useful or have an answer already.


#Class C subnetting
    if ((intiplist[0]) >= 192 and intiplist[0] <= 223):
        x = 0
        limiter = 256 - int(sub[3])
        subnetcounter = []

        if numsubnets == 0:
            allsublist = []
            broadcast = []
            firstaddress = []
            lastaddress = []

    #Making lists that will be joined after the result. Returns empty list if we have no subnets.
        
        else:  
            i = 0
            while i < numsubnets:
                subnetcounter.append(x)
                x += limiter
                i += 1
            allsublist = []
            broadcast = []
            firstaddress = []
            lastaddress = []

            i = 0
            while i < len(subnetcounter):
                allsubs = ""
                broadc = ""
                lastbroad = ""
                firsta = ""
                lasta = ""
                lasta2 = ""
                allsubs = allsubs + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str(subnetcounter[i])
                broadc = broadc + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str((subnetcounter[i]) - 1)
                lastbroad = lastbroad + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str(255)
                firsta = firsta + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str((subnetcounter[i]) + 1)
                lasta = lasta + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str((subnetcounter[i]) - 2)
                lasta2 = lasta2 + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str(254)
                lastaddress.append(lasta)
                firstaddress.append(firsta)
                allsublist.append(allsubs)
                broadcast.append(broadc)
                i += 1

            lastaddress.append(lasta2)
            lastaddress.pop(0)
            broadcast.append(lastbroad)
            broadcast.pop(0)

    #Joining and appending lists to make the subnets.

#Class B subnetting
    elif ((intiplist[0]) >= 128 and intiplist[0] <= 191):
        if sub[3] != "0":
            x = 0
            limiter = 256 - int(sub[3])
            subnetcounter = []

            if numsubnets == 0:
                allsublist = []
                broadcast = []
                firstaddress = []
                lastaddress = []

            else:
                i = 0
                while i < numsubnets:
                    subnetcounter.append(x)
                    x += limiter
                    i += 1
                allsublist = []
                broadcast = []
                firstaddress = []
                lastaddress = []

                i = 0
                while i < len(subnetcounter):
                    allsubs = ""
                    broadc = ""
                    lastbroad = ""
                    firsta = ""
                    lasta = ""
                    lasta2 = ""
                    allsubs = allsubs + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str(subnetcounter[i])
                    broadc = broadc + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str((subnetcounter[i]) - 1)
                    lastbroad = lastbroad + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str(255)
                    firsta = firsta + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str((subnetcounter[i]) + 1)
                    lasta = lasta + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str((subnetcounter[i]) - 2)
                    lasta2 = lasta2 + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(intiplist[2]) + "." +  str(254)
                    lastaddress.append(lasta)
                    firstaddress.append(firsta)
                    allsublist.append(allsubs)
                    broadcast.append(broadc)
                    i += 1

                lastaddress.append(lasta2)
                lastaddress.pop(0)
                broadcast.append(lastbroad)
                broadcast.pop(0)

    #Joining and appending to make the subnets.

        else:
            x = 0
            limiter = 256 - int(sub[2])
            subnetcounter = []
            if numsubnets == 0:
                allsublist = []
                broadcast = []
                firstaddress = []
                lastaddress = []

     #Return empty list if we have no subnets.

            else:
                i = 0
                while i < numsubnets:
                    subnetcounter.append(x)
                    x += limiter
                    i += 1
                allsublist = []
                broadcast = []
                firstaddress = []
                lastaddress = []

                i = 0
                while i < len(subnetcounter):
                    allsubs = ""
                    broadc = ""
                    lastbroad = ""
                    firsta = ""
                    lasta = ""
                    lasta2 = ""
                    allsubs = allsubs + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(subnetcounter[i]) + "." +  "0"
                    broadc = broadc + str((intiplist[0])) + "." + str(intiplist[1]) + "." + str((subnetcounter[i]) - 1) + "." +  "255"
                    lastbroad = lastbroad + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(255) + "." + "255"
                    firsta = firsta + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str((subnetcounter[i]) + 1) + "." +  "0"
                    lasta = lasta + str((intiplist[0])) + "." + str(intiplist[1]) + "." + str((subnetcounter[i]) - 2) + "." +  "0"
                    lasta2 = lasta2 + str(intiplist[0]) + "." + str(intiplist[1]) + "." + str(254) + "." + "0"
                    lastaddress.append(lasta)
                    firstaddress.append(firsta)
                    allsublist.append(allsubs)
                    broadcast.append(broadc)
                    i += 1

                lastaddress.append(lasta2)
                lastaddress.pop(0)
                broadcast.append(lastbroad)
                broadcast.pop(0)

    #Joining and appending lists to make the subnets.

    return {
        "address_cidr": ipstring + "/" + str(cidr),
        "num_subnets": numsubnets,
        "addressable_hosts_per_subnet": hosts,
        "valid_subnets": allsublist,
        "broadcast_addresses": broadcast,
        "first_addresses": firstaddress,
        "last_addresses": lastaddress

    }

    #Our return data or the response body.

#SUPERNETTING
class Supernet(BaseModel):
    addresses: list

    #Identifying Json.

@app.post("/supernet")
def thirdread(value: Supernet):
    sup = value.addresses
    return getsuper(sup)

    #The third post request, taking inputs.

def getsuper(sup):
    y = getbinary(sup[0].split("."))
    b = y.split(".")

    #Making the first element a list.

    i = 1
    while i < len(sup):
        z = getbinary(sup[i].split("."))
        a = z.split(".")

        j = 0
        while j < len(b):
            if b[j] != a[j]:
                answer = j
                break
            j += 1
        i += 1

    #Getting a rough position of where the pattern in binary changes by comparing the first element with the last by digit.
    #Using small variables here as they're only used once.

    pointer = 0
    i = 0
    while i < len(sup):
        temp = sup[i].split(".")
        if int(temp[answer]) > pointer:
            pointer = int(temp[answer])
            tracker = i
        i += 1

    pointer2 = 256
    i = 0
    while i < len(sup):
        temp2 = sup[i].split(".")
        if int(temp2[answer]) < pointer2:
            pointer2 = int(temp2[answer])
            tracker2 = i
        i += 1

    largestbinary = getbinary(sup[tracker].split("."))
    mainframe = largestbinary.split(".")
    smallestbinary = getbinary(sup[tracker2].split("."))
    mainframe2 = smallestbinary.split(".")
    mainframe3 = mainframe2[answer]

    supernetresult = []
    maskresult = []
    i = 0
    while i < answer:
        supernetresult.append(mainframe[i])
        maskresult.append("11111111")
        i += 1

    i = 0
    for digit in mainframe[answer]:
        if digit != mainframe3[i]:
            calculator = i
            break
        i += 1
    
    #Identifying the mask and creating variables that will be useful for our calcualtions.

    s = "00000000"
    t = "11111111"
    c = s[calculator:]
    d = t[:calculator]
    resultip = mainframe3[:calculator] + c
    resultmask = d + c

    #Creating the mask.

    if len(supernetresult) == 1:
        maskresult.append(resultmask)
        maskresult.append("00000000")
        maskresult.append("00000000")
        supernetresult.append(resultip)
        supernetresult.append("00000000")
        supernetresult.append("00000000")

    elif len(supernetresult) == 2:
        maskresult.append(resultmask)
        maskresult.append("00000000")
        supernetresult.append(resultip)
        supernetresult.append("00000000")

    elif len(supernetresult) == 3:
        maskresult.append("00000000")
        supernetresult.append(resultip)
    
    finished_mask = ".".join(maskresult)
    cidr = str(finished_mask.count("1"))

    #Appending and joining what we need

    worker = []
    for number in supernetresult:
        i = 0
        while i < len(number):
            if i == len(number) - 1:
                worker.append("0")

            elif number[i] != "0":
                decimalnum = int(number[i:], 2)
                worker.append(str(decimalnum))
                break
            i += 1

    endres = ".".join(worker)

    worker2 = []
    for number in maskresult:
        i = 0
        while i < len(number):
            if i == len(number) - 1:
                worker2.append("0")

            elif number[i] != "0":
                decimalnum = int(number[i:], 2)
                worker2.append(str(decimalnum))
                break
            i += 1

    endres2 = ".".join(worker2)

    #Converting both answers from binary to decimal.

    return {
        "address": endres + "/" + cidr,
        "mask": endres2
    }
            
#Returning our end result









