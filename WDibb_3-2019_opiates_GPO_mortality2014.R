
#Libraries ####
library(plyr)
library(dplyr)
library(lubridate)
library(ggplot2)

#MAKING PHARMSPENDING (COMBINED)
#Loading in the huge propublica database that has doctors, zip codes, and money given to them by pharmaceutical companies
propublica_pharmspending = read.csv("~/Downloads/OP_DTL_GNRL_PGYR2014_P01182019.csv")

#Dataset above doesn't have county names so we use another dataset to match zip codes to counties
ziptocounty <- read.csv("~/Downloads/IDA project/ZIP-COUNTY-FIPS_2014-12.csv")
propublica_pharmspending$zip <- gsub(propublica_pharmspending$Recipient_Zip_Code, pattern="-.*", replacement = "")

pharmspending <- merge(payment, ziptocounty, by.x= "Recipient_Zip_Code", by.y= "ZIP")
combined <- combined %>% 
  select(Recipient_Zip_Code,Submitting_Applicable_Manufacturer_or_Applicable_GPO_Name, Total_Amount_of_Payment_USDollars, Name_of_Associated_Covered_Drug_or_Biological1, Physician_Profile_ID, COUNTYNAME, STATE)

pharmspending= pharmspending %>% 
  unite(CoState,COUNTYNAME,STATE, remove = FALSE, sep=', ')

#write.csv(edited.propublica, file = combined)
write.csv(pharmspending, file = "edited.propublica.csv")

#MAKING COUNTY_RXNUMBERS (LANTA)
npizip <- read.csv("npi-to-zip.csv")

names(npizip)[1]<-"NPI"

prescriber_info=read.csv("prescriber-info_kaggle.csv")

county_RXnumbers=merge(npizip,pinfo, by="NPI") 

Provider_zip=substr(county_RXnumbers$nppes_provider_zip, 1, 5)

county_RXnumbers=cbind(Provider_zip,county_RXnumbers)

##MAKING COUNTY_DEATHRATE (NEWS)

##WHAT IS OHGOD? 




#Prescriber Info csv 
county_RXnumbers=read.csv("lanta.csv")

#Deathrate and RXrate CDC csv
county_deathrate=read.csv("news.csv")
county_deathrate$Crude.Rate <- gsub(county_deathrate$Crude.Rate, pattern=" .*", replacement = "")
county_deathrate$Crude.Rate <- as.numeric(county_deathrate$Crude.Rate)


#pharm spending propub csv
pharmspending=read.csv("edited.propublica.csv")


#County Population in 2014

county_population= read.csv("County_Population.csv")

county_population = na.omit(county_population)

county_population$state <- sub('.*,\\s*', '', county_population$areaname)

county_population$state = state.abb[match(county_population$state,state.name)]

county_population$new= gsub("(.*),.*", "\\1", county_population$areaname)

county_population$CoState <- paste(county_population$new, county_population$state, sep=", ")


county_population = county_population %>% 
  select(CoState, pop2014) %>% 
  mutate(totpop = pop2014) %>% 
  select(-pop2014)




### 

rural = read.csv("County_Rural_Lookup.csv")

rural = rural %>% select(GEOID_form, Percent_Rural_Pop)

pop_dataset=pop_dataset[!duplicated(pop_dataset$GEO.id2), ] 

pop_dataset=pop_dataset %>% select(GEO.display.label, GEO.id2)

pop_dataset$state <- sub('.*,\\s*', '', pop_dataset$GEO.display.label)

pop_dataset$state = state.abb[match(pop_dataset$state,state.name)]

pop_dataset$new= gsub("(.*),.*", "\\1", pop_dataset$GEO.display.label)

pop_dataset$CoState <- paste(pop_dataset$new, pop_dataset$state, sep=", ")

pop_dataset = pop_dataset %>% select(CoState,GEO.id2)


each_county_RX_spending= merge(each_county_RX_spending, county_population, by ="CoState" )  
each_county_RX_spending = each_county_RX_spending %>% select(-totpop.x) %>% mutate(totpop = totpop.y) %>% select(-totpop.y)

each_county_RX_spending= merge(each_county_RX_spending, rural, by.x ="GEO.id2", by.y = "GEOID_form") 

#number of physicans in each county####  
county_RXnumbers$CoState = paste(county_RXnumbers$county_name, county_RXnumbers$state, sep=", ")

county_npicount= county_RXnumbers %>% 
  select(CoState, npi) %>% 
  group_by(CoState) %>% 
  count()

##### numbe of phys in each county 
county_PIDcount= pharmspending %>%
  select(Physician_Profile_ID,CoState) %>%
  group_by(CoState) %>%
  mutate(unique_types = n_distinct(Physician_Profile_ID))


county_PIDcount= county_PIDcount %>% 
  select(CoState,unique_types) %>%
  group_by(CoState) %>% 
  summarise_each(funs(mean))



## summing pharm spending by county#### 
each_county_pharmspending = pharmspending %>%
  select(CoState, Total_Amount_of_Payment_USDollars) %>% 
  group_by(CoState) %>% 
  summarise_each(funs(sum)) 



# summing RXs by coutny####
each_county_RXnumbers= county_RXnumbers %>% 
  select(county_name,state,fentanyl, hydrocodone,hydromorphone,methadone,morphine,oxycodone,scriptsum) %>% 
  group_by(county_name, state) %>% 
  summarise_each(funs(sum))



each_county_RXnumbers$CoState = paste(each_county_RXnumbers$county_name, each_county_RXnumbers$state, sep=", ")



### Mergring spending and RXnumbers into each_county_RX_spending#### 
each_county_RX_spending=merge(each_county_pharmspending,each_county_RXnumbers, by="CoState")

## Merging county population with each_county_RX_spending#### 
each_county_RX_spending=merge(each_county_RX_spending,county_pop, by="CoState")

#merging number of phys per county with each_county_RX_spending #### 
each_county_RX_spending = merge(each_county_RX_spending,county_PIDcount, by="CoState")




#gather per capita information #### 
#needs work 
each_county_RX_spending = each_county_RX_spending %>% 
  mutate(oxycodone_per_person = oxycodone/totpop) %>% 
  mutate(oxycodone_per_tenk_people = oxycodone_per_person * 10000) %>% 
  select(-oxycodone_per_person)

each_county_RX_spending = each_county_RX_spending %>% 
  mutate(RX_per_person= scriptsum/totpop) %>% 
  mutate(RX_per_tenk_people = RX_per_person * 10000) %>% 
  select(-RX_per_person)

#needs work 
each_county_RX_spending = each_county_RX_spending %>% 
  mutate(dollars_per_physician= Total_Amount_of_Payment_USDollars/unique_types)

each_county_RX_spending = each_county_RX_spending %>% 
  mutate(dollars_per_capita= Total_Amount_of_Payment_USDollars/totpop) %>% 
  mutate(dollars_per_tenk_people = dollars_per_capita * 10000) %>% 
  select(-dollars_per_capita)


each_county_RX_spending = each_county_RX_spending %>% select(-scriptRate, -spend_Rate) 

#finding IQR to make  categories#### 
summary(each_county_RX_spending$Total_Amount_of_Payment_USDollars)
summary(each_county_RX_spending$dollars_per_tenk_people)
## make pharm $ into 4 categories 
each_county_RX_spending$cat_dollars_per_tenk_people <- cut(each_county_RX_spending$dollars_per_tenk_people,
                     breaks=c(-Inf,4013, 12298 , 31633, Inf),
                     labels=c("cat1","cat2","cat3","cat4")) 

each_county_RX_spending$cat_dollars_per_tenk_people = as.factor(each_county_RX_spending$cat_dollars_per_tenk_people)


each_county_RX_spending$cat_total_dollars <- cut(each_county_RX_spending$Total_Amount_of_Payment_USDollars,
                            breaks=c(-Inf,13938, 84861, 410700, Inf),
                            labels=c("cat1","cat2","cat3","cat4"))

data.frame(table(each_county_RX_spending$cat_dollars_per_tenk_people)) # making sure cats are even 

plot(density(each_county_RX_spending$Total_Amount_of_Payment_USDollars))






#scripts by spending cats####

cat_totaldollars_oxy = each_county_RX_spending %>%
  select(cat_total_dollars, oxycodone) %>% 
  group_by(cat_total_dollars) %>% 
  summarise_each(funs(sum))

summary(lm(oxycodone ~ cat_dollars_per_tenk_people, data=each_county_RX_spending))

plot(each_county_RX_spending$dollars_per_tenk_people,each_county_RX_spending$oxycodone, ylim=c(0,2500)) 



boxplot()

summary(lm(each_county_RX_spending$Total_Amount_of_Payment_USDollars ~ each_county_RX_spending$totpop))
        
        
cat_totaldollars_RXpertenk = each_county_RX_spending %>%
  select(cat_total_dollars, RX_per_tenk_people) %>% 
  group_by(cat_total_dollars) %>% 
  summarise_each(funs(median)) 



cat5 = each_county_RX_spending_death %>% 
  select(RXRate, spend_cat) %>% 
  group_by(spend_cat) %>% 
  summarise_each(funs(median))

plot(each_county_RX_spending_death$spend_Rate,each_county_RX_spending_death$RXRate)



summary(lm(scriptRate ~ spend_cat + totpop + state, data=mother)) 

lm <- lm(Crude.Rate ~  RXRate + State ,data = news )
summary(lm)

##########################

each_county_RX_spending_death= merge(each_county_RX_spending,county_deathrate, by.x = "CoState", by.y = "County.State")

each_county_RX_spending_death= each_county_RX_spending_death %>% 
  mutate(death_per_tenk= (Deaths / totpop)*10000) %>% 
  mutate(RXRate_per_tenk = RXRate *100) %>%
  mutate(deaths_per_pop = Deaths/totpop) %>%
  mutate(deaths_per_pop_timestenk = deaths_per_pop *10000) %>%
  mutate(RX_per_pop = (RXRate *100)/totpop) %>%
  mutate(RX_per_pop_timestenk = RX_per_pop * 10000) %>%
  mutate(oxy_per_pop = oxycodone/totpop) %>%
  mutate(hydrocodone_per_pop = hydrocodone/totpop,
         morphine_per_pop = morphine/totpop, methadone_per_pop = methadone/Population, 
         fentanyl_per_pop = fentanyl/Population, hydromorphone_per_pop = hydromorphone/Population )


summary(lm(RX_per_tenk_people ~ dollars_per_tenk_people, data = each_county_RX_spending))

plot(each_county_RX_spending$dollars_per_tenk_people,each_county_RX_spending$dollars_per_tenk_people, xlim = c(0,1000))


summary(lm(death_per_tenk ~ RXRate + dollars_per_tenk_people + state,  data=each_county_RX_spending_death))  







### COOK COUNTY IL ANALYSIS #### 


SC = mother %>% 
  filter(state == 'SC') 


summary(lm(scriptRate ~ spend_Rate, data = SC))

TX = mother %>% 
  filter(state == 'TX') 

summary(lm(scriptRate ~ spend_Rate, data = TX))

ID = mother %>% 
  filter(state == 'ID') 

summary(lm(scriptRate ~ spend_Rate, data = ID))

UT = mother %>% 
  filter(state == 'UT') 

summary(lm(scriptRate ~ spend_Rate, data = UT)) 


SCpharm= pharm %>% 
  filter(STATE=="SC") %>% 
  select(Submitting_Applicable_Manufacturer_or_Applicable_GPO_Name, Total_Amount_of_Payment_USDollars) %>% 
  group_by(Submitting_Applicable_Manufacturer_or_Applicable_GPO_Name) %>% 
  summarise_each(funs(sum))


SCnew= SC %>% 
  
  
ggplot(SC, aes(scriptRate, spend_Rate)) + 
  geom_point()

ggplot(SC, aes(x=area, y=poptotal)) + geom_point()

names(dollarRXrate)

summary(lm(RXRate ~ spend_cat + spend_Rate + Total_Amount_of_Payment_USDollars, data = dollarRXrate))


##########hashtag#################################hashtag#################################hashtag#################################hashtag#######################

#1)lm of opioids against money / boxplots /anovas

summary(lm(scriptsum ~ cat_dollars_per_tenk_people, data = each_county_RX_spending)) 
confint(lm(scriptsum ~ cat_dollars_per_tenk_people, data = each_county_RX_spending))

summary(lm(fentanyl~ cat_dollars_per_tenk_people, data = each_county_RX_spending)) 
confint(lm(fentanyl ~ cat_dollars_per_tenk_people, data = each_county_RX_spending))

summary(lm(hydrocodone~ cat_dollars_per_tenk_people, data = each_county_RX_spending))
confint(lm(hydrocodone ~ cat_dollars_per_tenk_people, data = each_county_RX_spending))

summary(lm(hydromorphone~ cat_dollars_per_tenk_people, data = each_county_RX_spending))
confint(lm(hydromorphone ~ cat_dollars_per_tenk_people, data = each_county_RX_spending))

summary(lm(methadone~ cat_dollars_per_tenk_people, data = each_county_RX_spending)) 
confint(lm(methadone ~ cat_dollars_per_tenk_people, data = each_county_RX_spending))

summary(lm(morphine~ cat_dollars_per_tenk_people, data = each_county_RX_spending))
confint(lm(morphine ~ cat_dollars_per_tenk_people, data = each_county_RX_spending))

summary(lm(oxycodone~ cat_dollars_per_tenk_people, data = each_county_RX_spending))
confint(lm(oxycodone~ cat_dollars_per_tenk_people, data = each_county_RX_spending))


library(ggplot2)


#SCRIPTSUM BOXPLOT AND ANOVA
GPO_rate_boxplot <- ggplot(each_county_RX_spending, aes(x = cat_dollars_per_tenk_people, y = scriptsum, fill = each_county_RX_spending$cat_dollars_per_tenk_people)) + 
  geom_boxplot() + labs(y = "# Total RX", x = "GPO Funding/10,000 people") 

#plot(GPO_rate_boxplot + ylim(0,1000) + ggtitle("Total Oxycodone Prescriptions by GPO Funding Rate Quartiles"))
GPO_rate_boxplot + scale_fill_discrete(name= "GPO Funding Quartiles", breaks= c("cat1", "cat2", "cat3", "cat4"),
                                       labels = c("cat1 = $0 - 4,013", "cat2 = $4,014 - 12,298", "cat3 = $12,299 - 31,633", "cat4 = $31,634 - ∞")) +  ylim(0,7500) + ggtitle("Total Prescriptions by GPO Funding Rate Quartiles")
scriptsum_lm <- lm(each_county_RX_spending$scriptsum ~ each_county_RX_spending$cat_dollars_per_tenk_people)
summary(scriptsum_lm)
scriptsum_anova <- aov(scriptsum_lm)
summary(scriptsum_anova) 
TukeyHSD(scriptsum_anova)

summary(each_county_RX_spending$dollars_per_tenk_people)


#OXYCODONE BOXPLOT AND ANOVA
GPO_rate_boxplot <- ggplot(each_county_RX_spending, aes(x = cat_dollars_per_tenk_people, y = oxycodone, fill = each_county_RX_spending$cat_dollars_per_tenk_people)) + 
  geom_boxplot() + labs(y = "# Oxycodone RX", x = "GPO Funding Rate (per capita)") 

#plot(GPO_rate_boxplot + ylim(0,1000) + ggtitle("Total Oxycodone Prescriptions by GPO Funding Rate Quartiles"))
GPO_rate_boxplot + scale_fill_discrete(name= "GPO Funding Quartiles", breaks= c("cat1", "cat2", "cat3", "cat4"),
                                       labels = c("cat1 = $0 - 144", "cat2 = $144 - 441", "cat3 = $441 - 1155", "cat4 = $1155 - ∞")) +  ylim(0,1000) + ggtitle("Total Oxycodone Prescriptions by GPO Funding Rate Quartiles")
oxy_lm <- lm(each_county_RX_spending$oxycodone ~ each_county_RX_spending$cat_dollars_per_tenk_people)
summary(oxy_lm)
oxy_anova <- aov(oxy_lm)
summary(oxy_anova) 
TukeyHSD(oxy_anova)


#MORPHINE BOXPlOT AND ANOVA
GPO_rate_boxplot <- ggplot(each_county_RX_spending, aes(x = cat_dollars_per_tenk_people, y = morphine, fill = each_county_RX_spending$cat_dollars_per_tenk_people)) + 
  geom_boxplot() + labs(y = "# Morphine RX", x = "GPO Funding Rate (per capita)") 

#plot(GPO_rate_boxplot + ylim(0,1000) + ggtitle("Total Oxycodone Prescriptions by GPO Funding Rate Quartiles"))
GPO_rate_boxplot + scale_fill_discrete(name= "GPO Funding Quartiles", breaks= c("cat1", "cat2", "cat3", "cat4"),
                                       labels = c("cat1 = $0 - 144", "cat2 = $144 - 441", "cat3 = $441 - 1155", "cat4 = $1155 - ∞")) +  ylim(0,500)+ ggtitle("Total Morphine Prescriptions by GPO Funding Rate Quartiles")
morphine_lm <- lm(each_county_RX_spending$morphine ~ each_county_RX_spending$cat_dollars_per_tenk_people)
summary(morphine_lm)
morphine_anova <- aov(morphine_lm)
summary(morphine_anova) 
TukeyHSD(morphine_anova)


#HYDROCODONE BOXPlOT AND ANOVA
GPO_rate_boxplot <- ggplot(each_county_RX_spending, aes(x = cat_dollars_per_tenk_people, y = hydrocodone, fill = each_county_RX_spending$cat_dollars_per_tenk_people)) + 
  geom_boxplot() + labs(y = "# Hydrocodone RX", x = "GPO Funding Rate (per capita)") 

#plot(GPO_rate_boxplot + ylim(0,1000) + ggtitle("Total Oxycodone Prescriptions by GPO Funding Rate Quartiles"))
GPO_rate_boxplot + scale_fill_discrete(name= "GPO Funding Quartiles", breaks= c("cat1", "cat2", "cat3", "cat4"),
                                       labels = c("cat1 = $0 - 144", "cat2 = $144 - 441", "cat3 = $441 - 1155", "cat4 = $1155 - ∞")) +  ylim(0,2500)+  ggtitle("Total Hydrocodone Prescriptions by GPO Funding Rate Quartiles")
hydrocodone_lm <- lm(each_county_RX_spending$hydrocodone ~ each_county_RX_spending$cat_dollars_per_tenk_people)
summary(hydrocodone_lm)
hydrocodone_anova <- aov(hydrocodone_lm)
summary(hydrocodone_anova) 
TukeyHSD(hydrocodone_anova)

#FENTANYL BOXPlOT AND ANOVA
GPO_rate_boxplot <- ggplot(each_county_RX_spending, aes(x = cat_dollars_per_tenk_people, y = fentanyl, fill = each_county_RX_spending$cat_dollars_per_tenk_people)) + 
  geom_boxplot() + labs(y = "# Fentanyl RX", x = "GPO Funding Rate (per capita)") 

#plot(GPO_rate_boxplot + ylim(0,1000) + ggtitle("Total Fentanyl Prescriptions by GPO Funding Rate Quartiles"))
GPO_rate_boxplot + scale_fill_discrete(name= "GPO Funding Quartiles", breaks= c("cat1", "cat2", "cat3", "cat4"),
                                       labels = c("cat1 = $0 - 144", "cat2 = $144 - 441", "cat3 = $441 - 1155", "cat4 = $1155 - ∞")) +  ylim(0,500)+  ggtitle("Total Fentanyl Prescriptions by GPO Funding Rate Quartiles")
fentanyl_lm <- lm(each_county_RX_spending$fentanyl ~ each_county_RX_spending$cat_dollars_per_tenk_people)
summary(fentanyl_lm)
fentanyl_anova <- aov(fentanyl_lm)
summary(fentanyl_anova) 
TukeyHSD(fentanyl_anova)




#METHADONE BOXPlOT AND ANOVA
GPO_rate_boxplot <- ggplot(each_county_RX_spending, aes(x = cat_dollars_per_tenk_people, y = methadone, fill = each_county_RX_spending$cat_dollars_per_tenk_people)) + 
  geom_boxplot() + labs(y = "# Methadone RX", x = "GPO Funding Rate (per capita)") 

#plot(GPO_rate_boxplot + ylim(0,1000) + ggtitle("Total Fentanyl Prescriptions by GPO Funding Rate Quartiles"))
GPO_rate_boxplot + scale_fill_discrete(name= "GPO Funding Quartiles", breaks= c("cat1", "cat2", "cat3", "cat4"),
                                       labels = c("cat1 = $0 - 144", "cat2 = $144 - 441", "cat3 = $441 - 1155", "cat4 = $1155 - ∞")) +  ylim(0,400)+  ggtitle("Total Methadone Prescriptions by GPO Funding Rate Quartiles")
methadone_lm <- lm(each_county_RX_spending$methadone ~ each_county_RX_spending$cat_dollars_per_tenk_people)
summary(methadone_lm)
methadone_anova <- aov(methadone_lm)
summary(methadone_anova) 
TukeyHSD(methadone_anova)


#HYDROMORPHONE BOXPlOT AND ANOVA
GPO_rate_boxplot <- ggplot(each_county_RX_spending, aes(x = cat_dollars_per_tenk_people, y = hydromorphone, fill = each_county_RX_spending$cat_dollars_per_tenk_people)) + 
  geom_boxplot() + labs(y = "# Hydromorphone RX", x = "GPO Funding Rate (per capita)") 

#plot(GPO_rate_boxplot + ylim(0,1000) + ggtitle("Total Fentanyl Prescriptions by GPO Funding Rate Quartiles"))
GPO_rate_boxplot + scale_fill_discrete(name= "GPO Funding Quartiles", breaks= c("cat1", "cat2", "cat3", "cat4"),
                                       labels = c("cat1 = $0 - 144", "cat2 = $144 - 441", "cat3 = $441 - 1155", "cat4 = $1155 - ∞")) +  ylim(0,400)+  ggtitle("Total Hydromorphone Prescriptions by GPO Funding Rate Quartiles")
hydromorphone_lm <- lm(each_county_RX_spending$hydromorphone ~ each_county_RX_spending$cat_dollars_per_tenk_people)
summary(hydromorphone_lm)
hydromorphone_anova <- aov(hydromorphone_lm)
summary(hydromorphone_anova) 
TukeyHSD(hydromorphone_anova)


#5) crudemortality ~ RX of each drug
summary(lm(death_per_tenk ~ oxycodone_per_tenk_people, data= each_county_RX_spending_death))

summary(lm(death_per_tenk ~ oxycodone, data= each_county_RX_spending_death))

summary(lm(deaths_per_pop ~ RX_per_pop, data= each_county_RX_spending_death))

par(mfrow=c(1,2))

p1 = ggplot(data = each_county_RX_spending_death, aes(x= RX_per_pop_timestenk, y=deaths_per_pop_timestenk)) + geom_point() + labs(y="Deaths/10,000 people ", x="RX/10,000 people") + geom_smooth(method = "lm") + ggtitle("Prescription Rate by Opioid Mortality Rate")


p2= ggplot(data = each_county_RX_spending_death, aes(x= RX_per_pop_timestenk, y=deaths_per_pop_timestenk)) + geom_point() + labs(y="Deaths/10,000 people ", x="RX/10,000 people") + xlim(0,10) + ylim(0,0.05) + geom_smooth(method= "lm") + ggtitle("Prescription Rate by Opioid Mortality Rate")



grid.arrange(p1,p2 , ncol=2)

#TRASH:
summary(lm(deaths_per_pop ~ oxy_per_pop, data= each_county_RX_spending_death))
summary(lm(deaths_per_pop ~ morphine_per_pop, data= each_county_RX_spending_death))
summary(lm(deaths_per_pop ~ hydrocodone_per_pop, data= each_county_RX_spending_death))
summary(lm(deaths_per_pop ~ methadone_per_pop, data= each_county_RX_spending_death))
summary(lm(deaths_per_pop ~ fentanyl_per_pop, data= each_county_RX_spending_death))
summary(lm(deaths_per_pop ~ hydromorphone_per_pop, data= each_county_RX_spending_death))

##########


hist(each_county_RX_spending$Percent_Rural_Pop)

colors = c(rep("blue",10), rep("white", 10), rep("green",10))

county_classification <- ggplot(data=each_county_RX_spending, aes(Percent_Rural_Pop)) + geom_histogram(color="black", fill=colors) + ggtitle("County Classification") + xlab("Rural Percentage of County Population")  + ylab("Number of Counties")
county_classification + scale_fill_discrete(breaks= colors, labels = c("Urban", "Mixed", "Rural"))



urban = each_county_RX_spending %>% 
  filter(Percent_Rural_Pop >= 0  &   Percent_Rural_Pop <= 33 )

Rural = each_county_RX_spending %>% 
  filter(Percent_Rural_Pop >= 66  &   Percent_Rural_Pop <= 100 )

nonurban= each_county_RX_spending %>% 
  filter(Percent_Rural_Pop > 33) 

nonurban = merge(nonurban, deathrate, by.x="CoState",by.y = "County.State")



options(scipen = 999)

boxplot(urban$Total_Amount_of_Payment_USDollars, Rural$Total_Amount_of_Payment_USDollars, 
        ylim=c(0,4000000), names=c("Urban", "Rural"), col=c("Blue","Green"), 
        ylab="GPO Funding in Dollars", main = "General Purchasing Organization Funding for Urban and Rural Counties" )




text(1.8,500000, labels = "n = 265")
text(.8, 1800000, labels= "n = 527")
text(1.2,1800000, labels = "median = $448,221")
text(2.2,500000, labels = " median = $8,674")

median(Rural$Total_Amount_of_Payment_USDollars)

median(urban$Total_Amount_of_Payment_USDollars)

wilcox.test(urban$Total_Amount_of_Payment_USDollars, Rural$Total_Amount_of_Payment_USDollars)

county_deathrate = county_deathrate %>% 
  mutate(deathRate = Deaths/Population) %>% 
  mutate(deathrate= deathRate * 10000) %>% 
  select(-deathRate)


deathrate = county_deathrate %>% select(County.State,deathrate)

Rural_death= merge(deathrate, Rural, by.x="County.State", by.y= "CoState")

Urban_death= merge(deathrate, urban, by.x="County.State", by.y= "CoState")



boxplot(deathrate$deathrate, xlab="Urban", ylab="Deaths per 10,000 people", main = "CDC Opioid Related Mortality in Urban Counties", col=c("Blue"))


text(.9,.035, 'n = 80')
text(1.1,.035, "Median = 0.014")


############## 



death_co_pop=merge(deathrate,county_population, by.x="County.State", by.y = "CoState")

sum(death_co_pop$totpop)







       