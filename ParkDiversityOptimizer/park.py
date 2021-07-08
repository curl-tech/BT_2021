import numpy as np
import hjson

#Instance of a Tree/Plant that will take a place in Park.
class Plant:
    def __init__(self):
        # initialize instance variables:
        self.name = ""  #this is the plant/tree name (apple, pear, etc)
        self.yieldperacre = 0  #this is in lbs or kgs of average expected yield from this plant
        self.bioscore = 0 #this is a relative score(0 to 1 range) on how good it is for the nature (oxg production, save soil erosion,etc)
        self.beautyscore = 0  #how good looking is this ? (0 to 1 range)
        self.newcostfirstyear = 0  #Cost to buy the plant and run for first year.  (currency units)
        self.maintaincostoneyear = 0  #Cost to maintain the plant. (currency units)
        self.lastMarketPrice=0  #this is in same units of yieldperacre and the last known market price. (currency units)
        self.isplanted=False

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    #Trigger this when planting a tree is done.
    # Once planting is done, no more unrooting possible at this time.
    def plantit(self):
        self.isplanted=True

    def getexpectedvalue(self):
        #The most  easily interpretable "Value" function.
        # (yield*marketprice)^ (bioscore+beautyscore)
        basevalue = (self.yieldperacre*self.lastMarketPrice)
        powerfactor = self.bioscore + self.beautyscore
        expectedvalue = pow(basevalue, powerfactor)
        return round(expectedvalue,2)
    
    def getexpectedcost(self, includingSetupCost=True):
        # We will look at it from 1 year perspective.
        if(includingSetupCost==False):
            return round( (self.maintaincostoneyear),2)
        return round( (self.newcostfirstyear+ (self.maintaincostoneyear)),2)

#
# The concept of self optimizing park.
# This makes "child" parks each time you optimize it and plants the tree inside child.
# The child park goes thru actual journey of self mgmt, incurring maintanence and earing the yield.
# The child park is instance of Park, so it has capacity to create new children from its own plantations.
#
class Park:
    def __init__(self, configFile):
        # initialize instance variables:
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.totalacre= 0
        self.pathwaydesignstrategy= "forest"  #Forest means no designed pathway, its just a forest of trees/plants.
        self.plantlist=[]
        self.maxcostforsetup= 0  #This is the max cost todo inital setup
        self.configfile = configFile
        if(configFile!=""):
            self.load(configFile)

    def __len__(self):
        return len(self.plantlist)

    def getexpectedvalue(self, onlyPlanted=False):
        targetlist=self.plantlist
        if(onlyPlanted):
            targetlist = self.get_planted_list()
        totalvalue =[plant.getexpectedvalue() for plant in targetlist]
        return round(sum(totalvalue),0)

    def getexpectedcost(self, onlyPlanted=False, includeSetupCost=True):
        targetlist=self.plantlist
        if(onlyPlanted):
            targetlist = self.get_planted_list()
        totalcost =[plant.getexpectedcost(includeSetupCost) for plant in targetlist]
        return round(sum(totalcost),0)

    def load(self, configfile):
        with open(configfile) as deserializeFile:
            mainConfig = hjson.loads(deserializeFile.read())
        parkConfig = mainConfig["Park"]
        self.x1 = parkConfig["x1"]
        self.x2 = parkConfig["x2"]
        self.y1 = parkConfig["y1"]
        self.y2 = parkConfig["y2"]
        self.totalacre = parkConfig["totalacres"]
        self.pathwaydesignstrategy = parkConfig["pathwaydesignstrategy"]
        self.maxcostforsetup = parkConfig["maxcostforsetup"]

        for currentplant in mainConfig["Plants"]:
            tmp1 = Plant()
            tmp1.name = currentplant["name"]
            tmp1.beautyscore = float(currentplant["beautyscore"])
            tmp1.bioscore = float(currentplant["bioscore"])
            tmp1.maintaincostoneyear = int(currentplant["maintaincostyearly"])
            tmp1.newcostfirstyear = int(currentplant["newcost1year"])
            tmp1.yieldperacre = int(currentplant["yieldperacreinkg"])
            tmp1.lastMarketPrice = float(currentplant["marketprice"])
            self.plantlist.append(tmp1)

    def print_config_file(self,configfile):
        with open(configfile) as deserializeFile:
            mainConfig = hjson.loads(deserializeFile.read())

        for attr in mainConfig["Park"]:
            print(attr,end=" ")
            tmp1 = mainConfig["Park"][attr]
            print("=", tmp1,end=" ")

        print("\n -- Plants --")
        for plant in mainConfig["Plants"]:
            for attribute in plant:
                print (plant[attribute],end=" " )
            print("")

    def getvalue_for_chosen(self, zeroOneList):
        totalcost = totalValue = 0
        for i in range(len(zeroOneList)):
            curplant = self.plantlist[i]
            cost = curplant.getexpectedcost() 
            value = curplant.getexpectedvalue()            
            if totalcost + cost <= self.maxcostforsetup:
                totalcost += zeroOneList[i] * cost
                totalValue += zeroOneList[i] * value
        return totalValue

    def make_child(self, zeroOneList):
        newBabyPark = Park(self.configfile)
        for i in range(len(zeroOneList)):
            curplant = newBabyPark.plantlist[i]
            if zeroOneList[i] > 0:
                curplant.plantit() #If it was chosen from last optimization, just plant it.
        return (newBabyPark)

    def get_planted_list(self):
        #Getting wierd error on 1 line pythonic way, writing this the dumb way for later update.
        #plantedlist = [curplant for curplant in self.plantlist if curplant.isplanted()==True]
        plantedlist=[]
        for curplant in self.plantlist:
            if(curplant.isplanted):
                plantedlist.append(curplant)
        return plantedlist

    def print(self):       
        myplantedlist  = self.get_planted_list()
        plantedcount=len(myplantedlist)
        maintanencecost= self.getexpectedcost(onlyPlanted=True,includeSetupCost=False)
        setupcost = self.getexpectedcost(onlyPlanted=True) - maintanencecost
        
        print("++ Currently having #",plantedcount, "trees/plants out of #", len(self.plantlist) , "possible trees/plants.")
        print("++ Yield Market Value is :", self.getexpectedvalue(onlyPlanted=True))
        print("++ Total Initial Setup Cost :", setupcost)
        print("++ Total Yearly Maintanence Cost:", maintanencecost)
        print(" -- Plantations --")
        print((myplantedlist))
        print(" -- --")
    