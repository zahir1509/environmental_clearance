rm(list=ls())
library(dplyr)

##Preliminary Analysis 
user_name='anust'
state_name='Tamil_Nadu'
##EC Complete 1
ec_complete<-NA


for (attempt in 1:4){
  print(attempt)
  

ec_complete_temp<-read.csv(paste('C:/Users/',user_name,'/Dropbox/agnihotri_gupta/Environment_Clearance/',state_name,'/',state_name,'_ec_complete_',attempt,'.csv',sep = ''),
                      stringsAsFactors = F)
ec_complete<-rbind(ec_complete,ec_complete_temp)

print(attempt)
print(length(unique(ec_complete_temp$Proposal.No.)))

}


print(length(unique(ec_complete_temp$Proposal.No.)))

##Combined 

ec_complete_all_unique<-ec_complete%>%
  select(!c('Sno.','ï..'))%>%
  filter(!is.na(Proposal.No.))

ec_complete_all_unique<-distinct(ec_complete_all_unique)

##Duuplicates 
print(length(unique(ec_complete_all_unique$Proposal.No.)))


write.csv(ec_complete_all_unique,paste('C:/Users/',user_name,'/Dropbox/agnihotri_gupta/Environment_Clearance/',state_name,'/',state_name,'_ec_complete_unique','.csv',sep = ''))
