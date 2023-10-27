##Preliminary Analysis 

##EC Complete 1
ec_complete<-read.csv('C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/Odisha_ec_complete.csv',
                      stringsAsFactors = F)

table(duplicated(ec_complete$Sno.))
table(duplicated(ec_complete$Proposal.No.))

length(unique(ec_complete$Proposal.No.))

##EC Complete 2
ec_complete_2<-read.csv('C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/Odisha_ec_complete_2.csv',
                      stringsAsFactors = F)

table(duplicated(ec_complete_2$Sno.))
table(duplicated(ec_complete_2$Proposal.No.))

length(unique(ec_complete_2$Proposal.No.))

##EC Complete 3
ec_complete_3<-read.csv('C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/Odisha_ec_complete_3.csv',
                        stringsAsFactors = F)

table(duplicated(ec_complete_3$Sno.))
table(duplicated(ec_complete_3$Proposal.No.))

length(unique(ec_complete_3$Proposal.No.))

##Combined 
ec_complete_all<-rbind(ec_complete_3,ec_complete_2,ec_complete)

length(unique(ec_complete_all$Proposal.No.))

ec_complete_all_unique<-ec_complete_all%>%
  select(!c('Sno.','ï..'))

ec_complete_all_unique<-distinct(ec_complete_all_unique)
  



###More Information (A more detailed crawler that clicks on each link)
ec_complete_addtional_data<-read.csv('C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/Odisha_ec_complete_data.csv',
                      stringsAsFactors = F)

table(duplicated(ec_complete_addtional_data$Proposal))
table(ec_complete$Proposal.No.%in%ec_complete_addtional_data$Proposal)

ec_complete_links_data<-read.csv('C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/Odisha_ec_complete_links_pid.csv',
                                     stringsAsFactors = F)
table(duplicated(ec_complete_links_data$X0))

##TOR submitted 

tor_submitted<-read.csv('C:/Users/anust/Dropbox/agnihotri_gupta/Environment_Clearance/Odisha/Odisha_tor_complete.csv',
                      stringsAsFactors = F)


## Common Proposal Numbers

table(tor_submitted$Proposal.No.%in%ec_complete$Proposal.No.)
table(ec_complete$Proposal.No.%in%tor_submitted$Proposal.No.)


## Any Duplicated Serial Numbers

table(duplicated(ec_complete$Sno.))
table(duplicated(tor_submitted$Sno.))

## Proposal Status
library(dplyr)

ec_complete%>%
  group_by(Proposal.Status)%>%
  summarise(N=n())%>%
  arrange(desc(N))


tor_submitted%>%
  group_by(Proposal.Status)%>%
  summarise(N=n())%>%
  arrange(desc(N))


