from matplotlib import pyplot as plt
import numpy as np
import grequests
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))
import sys
import boto3
from datetime import datetime


host = sys.argv[1]
qtd_gets = int(sys.argv[2])
distributType = sys.argv[3]
email = sys.argv[4]
testName = sys.argv[5]
pathFolder = email+"/"+testName
#log variaveis
#total_time_response = 0
req = 0
init_test = datetime.now()
text=""
error=""
histNum = 30


if distributType == "normal" :
    mu, sigma = 0, 0.2 # mean and standard deviation
    s = np.random.normal(mu, sigma,qtd_gets)
    histNum = 30
elif distributType == "logistic" :
    loc, scale = 10, 1
    s = np.random.logistic(loc, scale, qtd_gets)
    histNum = 20
else:
    mu, sigma = 0, 0.2 # mean and standard deviation
    s = np.random.normal(mu, sigma,qtd_gets)
    histNum = 30
    text +="p.s: Distribution type erro, NORMAL was use in test: \n\n"    
    
text +="the host tested was: "+host+"\n\n"
#abs(mu - np.mean(s)) < 0.01

#abs(sigma - np.std(s, ddof=1)) < 0.01



minTH = abs(min(s))
#sN=sorted(s)
s = s+minTH
#print(sN)

count, bins, ignored = plt.hist(s, histNum, normed=False)
print("subgrupos-COUNT")
print(sum(count))
print(count)

def exception_handler(request, exception):
    #print "Request failed"
    #print exception
    global error
    error+= str(exception) +" \n"
    
    

#CRIACAO URLS
for i in range(histNum):
    print('Ciclo ',i)
    n = int(count[i])
    urls = [host for x in range(n)]
    #print(urls)
    rs = (grequests.get(u) for u in urls)
    result = grequests.map(rs, exception_handler=exception_handler)
    #print(max(result))
    for j in range(len(result)):
        if result[j] != None:
            #print(result[j].elapsed.total_seconds())
            text+=str(result[j].elapsed.total_seconds()*1000)+" ms;"+str(len(result[j].content))+" bytes\n"
        else:
            text+="TimeOut_error \n"



end_test = datetime.now()
totalTimeTest = end_test-init_test
text+="\n\n===============================================\n\n"
text+="Date Init Test: "+str(init_test)+" \n"
text+="Date End Test: "+str(end_test)+" \n"
text+="total time: "+str(totalTimeTest.seconds)+" s\n"
text+="Distribution used: "+distributType+" \n"
text+="Total request used: "+str(qtd_gets)  +" \n"
text+="dis: "+",".join(str(x) for x in count)+" \n"


my_session = boto3.session.Session()
my_region = my_session.region_name

s3 = boto3.resource('s3')
object = s3.Object('scalability-logs', pathFolder+"/"+my_region+".log")
objectError = s3.Object('scalability-logs',pathFolder+"/"+my_region+"_error.log")

object.put(Body=text)
objectError.put(Body=error)


