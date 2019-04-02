import json
BSLog={
        "h1":{},
        "h2":{},
        "h3":{}
        # "h4":{},
        # "h5":{},
        # "h6":{}
}
BSLog["h1"]["flag"]=False
BSLog["h2"]["flag"]=False
BSLog["h3"]["flag"]=False
filename = "/home/shlled/mininet-wifi/Log/BSLog.json"
with open(filename,'r') as f:
        buffer=f.readlines()
        lenth=len(buffer)
        while lenth>0:
            temp=buffer[lenth-1]
            temp=json.loads(temp)
            #print(temp[0]["UEIP"])
            if temp[0]["UEIP"] == "10.0.0.1":
                BSLog["h1"]["flag"] = True
                BSLog["h1"]["IP"] = temp[0]["UEIP"]
                BSLog["h1"]["POWER"] = temp[0]["UEPOWER"]
                BSLog["h1"]["PRICE"] = temp[0]["UEPRICE"]
                BSLog["h1"]["LOSS"] = temp[0]["UELOSS"]
                BSLog["h1"]["MAX"] = temp[0]["UEMAX"]
            elif temp[0]["UEIP"] == "10.0.0.2":
                BSLog["h2"]["flag"] = True
                BSLog["h2"]["IP"] = temp[0]["UEIP"]
                BSLog["h2"]["POWER"] = temp[0]["UEPOWER"]
                BSLog["h2"]["PRICE"] = temp[0]["UEPRICE"]
                BSLog["h2"]["LOSS"] = temp[0]["UELOSS"]
                BSLog["h2"]["MAX"] = temp[0]["UEMAX"]
            elif temp[0]["UEIP"] == "10.0.0.3":
                BSLog["h3"]["flag"] = True
                BSLog["h3"]["IP"] = temp[0]["UEIP"]
                BSLog["h3"]["POWER"] = temp[0]["UEPOWER"]
                BSLog["h3"]["PRICE"] = temp[0]["UEPRICE"]
                BSLog["h3"]["LOSS"] = temp[0]["UELOSS"]
                BSLog["h3"]["MAX"] = temp[0]["UEMAX"]

            lenth-=1
            if BSLog["h1"]["flag"] == True and BSLog["h2"]["flag"] == True and BSLog["h3"]["flag"]==True:
                break
print (BSLog)