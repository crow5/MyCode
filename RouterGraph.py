from fastapi import FastAPI
from pydantic import BaseModel
from collections import defaultdict

description = """
CA304 - Router Graph by Egor

## Functionality


-The Router function reads in a router name.\n 
    It then adds it to our known routers database.

-The Connection function reads in two router names and the distance between them.\n
    Once given it will begin to add relations to the graph.

-The Removing function will simply remove a given node from the graph.

-The RemovingCon function will remove the realtion of two given routers from our graph.


## Inputs Description


**All inputs are in JSON form.**

**addrouter** - {'name': 'A' or 'name': B'}\n
**connect** - {'from_': 'A' , 'to': 'B' , 'weight': 5}\n
**removerouter** -  {'name': 'A'}
**removeconnection** -  {'from_': 'A', 'to': 'B'}


## Outputs Description


**All Outputs are in JSON form.**

**addrouter** - This function will output the consequences of our inputs.\n
**connect** - This function will tell us if the connection fo two routers was successful or not, or if the routers even exist.\n
**removerouter** -  This function will tell us that it succeeded removing a known node in the graph.\n
**removeconnection** -  This function will tell us that it succeeded removing a edge in the graph, getting rid of the routers and their relations.


## Input - Output


### Router\n
**Input** =\n
    { 'name': 'A' }

**Output** =\n 
    {"status": "success"}

### Connection\n
**Input** =\n 
    { 'from_': 'A'\n
    'to': 'B'\n
    'weight': 5 }

**Output** =\n
    {'status': 'success'}

### Removing\n
**Input** =\n 
    { 'name': 'B' }

**Output** =\n 
    {'status': 'success'}

### RemovingCon\n
**Input** =\n 
    { 'from_': 'A'\n
    'to': 'B' }

**Output** =\n 
    {'status': 'success'}
"""

app = FastAPI(
    title="Router Graph",
    description=description,
    version="0.1.0"
)

graph = defaultdict(list)
class Router(BaseModel):
    name: str

#FIRST ENDPOINT FOR ADDING ROUTERS
@app.post("/addrouter")
def addrouter(info: Router):
    router_name = info.name
    return addmyrouter(router_name)

#ADDING NAMED ROUTERS TO AN ARRAY
router_list = []
def addmyrouter(router_name):
    if router_name not in router_list:
        router_list.append(router_name)
        return {
            "status": "success"
        }
    else:
        return {
            "status": "Error, node already exists"
        }

class Connection(BaseModel):
    from_: str
    to: str
    weight: int

database = {}
edges = []

#SECOND ENDPOINT FOR ROUTER CONNECTION
@app.post("/connect")
def connect(info2: Connection):
    first_router = info2.from_
    second_router = info2.to
    distance = info2.weight
    return makegraph(first_router, second_router, distance)

#CREATES DATA TO BE USED FOR GRAPH
def makegraph(first_router, second_router, distance):
    if (first_router not in router_list) or (second_router not in router_list):
        return {
            "status": "Error, router does not exist"
        }
    else:
        two_routers = []
        two_routers.append(first_router)
        two_routers.append(second_router)

        #CREATING A GRAPH USING OUR DATA
        if two_routers not in edges:
            edges.append(two_routers)
            database[distance] = two_routers
            edge = edges[-1]
            a, b = edge[0], edge[1]
            graph[a].append(b)
            graph[b].append(a)
            return {
                "status": "success"
            }

        #CHECKING DICTIONARY TO COMPARE WEIGHT OF ROUTERS TO GIVE RESULT
        elif two_routers in edges:
            x = distance
            for key, value in database.items():
                if value == two_routers:
                    if key == x:
                        return {
                            "status": "No changes were made."
                        }
                    else:
                        database[x] = database.pop(key)
                        return {
                            "status": "updated"
                        }

class Removing(BaseModel):
    name: str

#THIRD ENDPOINT
@app.post("/removerouter")
def removerouter(info3: Removing):
    router_name = info3.name
    return remover(router_name)

#REMOVES OUTER NODE
def remover(router_name):
    graph.pop(router_name)
    for i in graph:
        x = graph[i]
        for j in x:
            if router_name == j[0]:
                x.remove(j)
                return {
                    "status": "success"
                }

class RemovingCon(BaseModel):
    from_: str
    to: str

#FOURTH ENDPOINT
@app.post("/removeconnection")
def removeconnection(info4: RemovingCon):
    first = info4.from_
    last = info4.to
    return connectionremover(first, last)

#REMOVES ALL CONNECTION DATA FROM GRAPH
def connectionremover(first, last):
    if last in graph[first]:
        graph[first].remove(last)
        graph[last].remove(first)
        return {
            "status": "success"
        }