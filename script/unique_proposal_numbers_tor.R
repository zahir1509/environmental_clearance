library(dplyr)
##Preliminary Analysis 
user_name='anust'
state_name='Haryana'
##EC Complete 1
tor_complete<-NA


for (attempt in 1:2){
  print(attempt)
  

tor_complete_temp<-read.csv(paste('C:/Users/',user_name,'/Dropbox/agnihotri_gupta/Environment_Clearance/',state_name,'/',state_name,'_tor_complete_',attempt,'.csv',sep = ''),
                      stringsAsFactors = F)
tor_complete<-rbind(tor_complete,tor_complete_temp)

print(attempt)
print(length(unique(tor_complete_temp$Proposal.No.)))

}

##Combined 

tor_complete_all_unique<-tor_complete%>%
  select(!c('ï..','Sno.'))%>%
  filter(!is.na(Proposal.No.))

tor_complete_all_unique<-distinct(tor_complete_all_unique)

##Duuplicates 
print(length(unique(tor_complete_all_unique$Proposal.No.)))


write.csv(tor_complete_all_unique,paste('C:/Users/',user_name,'/Dropbox/agnihotri_gupta/Environment_Clearance/',state_name,'/',state_name,'_tor_complete_unique','.csv',sep = ''))
