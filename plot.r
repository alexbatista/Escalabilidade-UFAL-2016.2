library(readr)
library(boot)
library(gplots)
#caminho para o arquivo de log
us_west_2 <- read.csv("~/Documents/escalabilidade/us-west-2-02.log", skip = 0,sep=";",header = FALSE)

i = which(us_west_2=="=====")
iFinal = dim(us_west_2)[1]
subArray = matrix(us_west_2[i:iFinal,1])
iSubFinal = dim(subArray)[1]
dist = as.numeric(unlist(strsplit(subArray[iSubFinal],',') ) )

matResult = as.numeric(matrix(us_west_2[1:i-1,1]))



inter_conf <- function(i){ 
  boot_value <- boot(i, function(x,j) mean(x[j]), R=1000)
  if(apply(boot_value$t, 2, sd) == 0) {
    return(c(boot_value$t0,boot_value$t0))
  }else {
    return((boot.ci(
      boot_value,
      type=c("perc")
    )
    )$percent[4:5])
  }
}


inter_conf_array <- function(list,count){ 
  retArray = cbind(0,0,0,1:length(count))
  
  LimInf = 1
  LimSup = 1
  for(x in 1:length(count)){
    if(x == 1){
      LimInf = 1
      LimSup = count[x]
    }else{
      LimInf = LimInf + count[x-1]
      LimSup = LimSup + count[x]
    }
    if(count[x] == 0){
      auxArray = NA
    }else{
      auxArray = list[LimInf:LimSup]
      #print(auxArray)
      a = inter_conf(auxArray)
      #print(a)
      retArray[x,1] = mean(a)
      retArray[x,2] = a[1]
      retArray[x,3] = a[2]
    }
    #print(auxArray)
  }
  return(retArray)
}
#inter_conf_array(matResult,dist)
resPlot = inter_conf_array(matResult,dist)
#https://github.com/cloudyr/aws.s3

media = c(resPlot[,1])
lower <- c(resPlot[,2])
upper <- c(resPlot[,3])
x = c(1:length(dist))

#require(plotrix)
require(gplots)
plotCI(x,media, ui = upper, li=lower)

