#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Author: Will Dibb
#Data wrangling, cleaning, formatting (pandas, numpy, csv, time, os)
#Statistical analysis of primary and secondary endpoints (scipy, statsmodels)
#Data visualization (matplotlib, lifelines)
#Support Vector Machine with manufactured dataset (scikit-learn)

#Raw data not provided, active clinical research 

import pandas as pd
import numpy as np
import scipy as scp
import statsmodels as sm
import time 
import csv
import os
import matplotlib.pyplot as plt
import sklearn as skl

import sys
#If not installed - use pip install for lifelines:
get_ipython().system('{sys.executable} -m pip install lifelines')

#Commercial  Exploratory Analysis + Proof of Concept Support Vector Machine Model

#Real Data for EA primary and secondary endpoint comparison to published literature
#Supplemental dummy data created for SVM modeling

#Deliverables: 

#A. Clean reference data frames from REDCap raw CSV query

#B. Exploratory Analysis of commercial treatment Efficacy + Safety vs Clinical Trial Outcomes

    
#i. Summary Statistics Table
#ii. Primary Endpoints: Commercial vs Clinical Trial ORR (Overall Response Rate) at 30d s/p treatment
#iii.  Overall Survival + Progression Free Survival Curve (y = survival/event, x = days)
#iv. Secondary Endpoints: Commercial vs Clinical Trial Serum Biomarker SAE Association 
  
#Statistical Models: Exact Binomial, Wilson Rank-Sum/Mann-Whitney U

#Statistical methods:

#i. Hx rate of response comparator = 20%
#ii. Power >= 90% to distinguish 40% true response
#iii. one-sided alpha level = 0.025
#iv. Holm's procedure adjustment of p-values 
#v. CI calculations by Clopper-Pearson method


#C. Support Vector Machine (SVM) classification of responders vs. non-responders to 
#commercial therapy 

#i. Manufacture cohort data to build model
#ii. Derive best feature subset, find best SVC kernel fit, k-fold cross-validation




# In[2]:


#Read in REDCap raw CSV file 
#tx_core_df = pd.read_csv('', skiprows = 1)
#tx_core_df.head()


# In[3]:


#Reference Dataframes:

#1. Demographics
#2. Clinical Disease
#3. Clinical Bridging Therapy
#4. Clinical Treatment
#5. Clinical Adverse Events
#6. Clinical Infections
#7. Clinical Outcomes (Clin Outcomes + Other Outcomes)
#8. Clinical Concomitant Medications
#9. Clinical (Master)
#10. Labs (Master)
#11. CRS/NT (CRS/NT AEs + Meds)
#12. Bone Marrow Biopsy
#13. Imaging
#14. ECHO
#17. Master 1:1 Dataframe


# In[4]:


#1. Patient Demographics 

#create separate dataframe
dems_df = tx_core_df.copy(deep = True)
#filter by Lab CRF ID on columns axis
dems_df = dems_df.filter(like = 'dems_', axis = 1)
dems_df = dems_df.sort_index(ascending = True)
#drop rows with no pt DOB
dems_df = dems_df.dropna(subset = ['dems_pt_DOB'])

#dems_df.head()

#2. Clinical Disease 

clin_dz_df = tx_core_df.copy(deep = True)
clin_dz_df = clin_dz_df.filter(like = 'clin_dz_', axis = 1)
clin_dz_df = clin_dz_df.sort_index(ascending = True)
#drop rows with no clinical disease listing
clin_dz_df = clin_dz_df.dropna(subset = ['clin_dz_type'])

#clin_dz_df.head()

#3. Clinical - Bridging Therapy

clin_bridge_df = tx_core_df.copy(deep = True)
clin_bridge_df = clin_bridge_df.filter(like = 'clin_bridge_', axis = 1)
clin_bridge_df = clin_bridge_df.sort_index(ascending = True)
clin_bridge_df = clin_bridge_df.dropna(subset = ['clin_bridge_therapy'])

#clin_bridge_df.head()

#4. Clinical Treatment Infusion

clin_tx_df = tx_core_df.copy(deep = True)
clin_tx_df = clin_tx_df.filter(like = 'clin_tx_', axis = 1)
clin_tx_df = clin_tx_df.sort_index(ascending = True)
clin_tx_df = clin_tx_df.dropna(subset = ['clin_tx_inf'])

#clin_tx_df.head()

#5. Clinical Adverse Events

clin_AE_df = tx_core_df.copy(deep = True)
clin_AE_df = clin_AE_df.filter(like = 'clin_AE_', axis = 1)
clin_AE_df = clin_AE_df.sort_index(ascending = True)
clin_AE_df = clin_AE_df.dropna(subset = ['clin_AE_CRS'])

#clin_AE_df.head()

#6. Clinical Infections

clin_infx_df = tx_core_df.copy(deep = True)
clin_infx_df = clin_infx_df.filter(like = 'clin_infx_', axis = 1)
clin_infx_df = clin_infx_df.sort_index(ascending = True)
clin_infx_df = clin_infx_df.dropna(subset = ['clin_infx_bacterial_29_365'])

#clin_infx_df.head()

#7. Clinical Outcomes (Clin Outcomes + Other Outcomes)


clin_out_df = tx_core_df.copy(deep = True)
clin_out_df = clin_out_df.filter(like = 'clin_outcome', axis = 1)

clin_oth_out_df = tx_core_df.copy(deep = True)
clin_oth_out_df = clin_oth_out_df.filter(like = 'oth_outcome', axis = 1)
clin_out_df = clin_out_df.join(clin_oth_out_df, on = 'tx_biobank_id')


clin_out_df = clin_out_df.sort_index(ascending = True)
clin_out_df = clin_out_df.dropna(subset = ['clin_outcomes_prog', 'oth_outcome_low_ANC'])

#clin_out_df.head()

#8. Clinical Concomitant Medications

clin_meds_df = tx_core_df.copy(deep = True)
clin_meds_df = clin_meds_df.filter(like = 'clin_post_', axis = 1)
clin_meds_df = clin_meds_df.sort_index(ascending = True)
clin_meds_df = clin_meds_df.dropna(subset = ['clin_post_conmeds'])

#clin_meds_df.head()

#9. Clinical (Master)

clin_df = tx_core_df.copy(deep = True)
clin_df = clin_df.filter(like = 'clin_', axis = 1)
clin_df = clin_df.sort_index(ascending = True)
clin_df = clin_df.dropna(subset = ['clin_dz_type'])

#clin_df.head()

#10. Labs (Master)

labs_df = tx_core_df.copy(deep = True)
labs_df = labs_df.filter(like = 'lab_', axis = 1)
labs_df = labs_df.join(biobank_id)

#Dual index with biobank ID and lab event date:
labs_df = labs_df.set_index([biobank_id, 'lab_event_dt'])
labs_df = labs_df.sort_index(ascending = True)

#Alternative - to move biobank ID to beginning of dataframe while keeping default index:
#labs_cols_list = list(tx_labs_df)
#labs_cols_list.insert(0, labs_cols_list.pop(labs_cols_list.index('tx_biobank_id')))
#tx_labs_df = tx_labs_df.loc[:,labs_cols_list]

labs_df.dropna(subset = ['lab_event_type'], inplace = True)
labs_df = labs_df.drop(labels = 'tx_biobank_id', axis = 1)

#labs_df.head()


#11. CRS/NT (CRS/NT AEs + Meds)

clin_crsnt_df = tx_core_df.copy(deep = True)
clin_crsnt_df = clin_crsnt_df.filter(like = 'crsnt_', axis = 1)
clin_crsnt_df = clin_crsnt_df.join(clin_AE_df, on = 'tx_biobank_id')
clin_crsnt_df = clin_crsnt_df.sort_index(ascending = True)

clin_crsnt_df = clin_crsnt_df.dropna(subset = ['crsnt_toci'])
#clin_crsnt_df.head()


#12. Bone Marrow Biopsy

bmbx_df = tx_core_df.copy(deep = True)
bmbx_df = bmbx_df.filter(like = 'bmbx_', axis = 1)
bmbx_df = bmbx_df.sort_index(ascending = True)
bmbx_df = bmbx_df.dropna(subset = ['bmbx_dt'])

#bmbx_df

#13. Imaging

imag_df = tx_core_df.copy(deep = True)
imag_df = imag_df.filter(like = 'imag_', axis = 1)

#create column for Boolean overall response with respect to imag_resp
imag_df['overall_resp'] = imag_df.imag_resp.map({'CR': True, 
                                                 'PR': True,
                                                 'SD': False, 
                                                 'PD': False})
imag_df = imag_df.sort_index(ascending = True)
imag_df = imag_df.dropna(subset = ['imag_dt'])

#imag_df


#14. ECHO

echo_df = tx_core_df.copy(deep = True)
echo_df = echo_df.filter(like = 'echo_', axis = 1)
echo_df = echo_df.sort_index(ascending = True)
echo_df = echo_df.dropna(subset = ['echo_baseline'])

#echo_df.head()


#17. Master Dataframe for all single-input patient values
tx_mstr_df = tx_core_df.copy(deep = True)
tx_mstr_df = tx_mstr_df.where(tx_mstr_df['crf_name'] != 'Lab Event')
tx_mstr_df = tx_mstr_df.where(tx_mstr_df['crf_name'] != 'Imaging')
#drop duplicate entries on biobank ID column, keeping first value
tx_mstr_df = tx_mstr_df.drop_duplicates(subset = ['tx_biobank_id'], 
                                            keep = 'first', 
                                            inplace = False)  
tx_mstr_df = tx_mstr_df.dropna(subset = ['dems_pt_DOB'])
tx_mstr_df = tx_mstr_df.set_index('tx_biobank_id')
tx_mstr_df = tx_mstr_df.sort_index()
                                  
#tx_mstr_df.head()



# In[ ]:


#ORR Dataframe

#PR or CR (30d) ~ IPI + Age + Dz Stage + Dz Histology + Baseline CRP + Prior Tx + G3 CRS + G3 ICANS 

#1. Create new tx_ORR_df
tx_ORR_df = tx_core_df.copy(deep = True)

#2a.Create new ORR Boolean Column
#tx_ORR_OR_df = tx_ORR_df.copy(deep = True)
#tx_ORR_OR_df['overall_resp'] = tx_ORR_OR_df.imag_resp.map({'CR': True, 'PR': True,'SD': False, 'PD': False})

#tx_ORR_OR_df = tx_ORR_OR_df.filter(['overall_resp'])
#tx_ORR_OR_df['overall_resp'].astype('category')

#2b. Set clinical disease response type to category
tx_ORR_df['imag_resp'].astype('category')


#3. Set IPI type to category
tx_ORR_df['clin_dz_IPI_score_apher'].astype('category')

#4. Create new calculated column for patient age (years)
tx_ORR_df['dems_pt_age'] = tx_ORR_df['clin_dz_apher_dt'] - tx_ORR_df['dems_pt_DOB']
tx_ORR_df['dems_pt_age'] = tx_ORR_df['dems_pt_age']/np.timedelta64(1,'Y')
#To create new column for age groups (18-64, 65+)
#tx_ORR_df['dems_pt_age_grp'] = pd.cut(tx_ORR_df['dems_pt_age'], range(0, 130, 64)).astype('category')

#5. Set Dz Stage type to category 
tx_ORR_df['clin_dz_status_tx'].astype('category')

#6. Set disease histology type to category
tx_ORR_df['clin_dz_type'].astype('category')


#7. Create data frame to isolate baseline CRP
base_CRP_df = tx_ORR_df.copy(deep = True)
base_CRP_df = base_CRP_df[(base_CRP_df['lab_monitor_type'] == 'Day 0 (infusion)')]
base_CRP_df = base_CRP_df.filter(['lab_monitor_type',
                                  'lab_cmp_CRP'])

base_CRP_df['base_CRP_inflam'] = base_CRP_df['lab_cmp_CRP'].apply(lambda x: 'False' if x <= 100 else 'True')
            

#8. Set prior therapies count to category
tx_ORR_df['clin_dz_prior_ther_ct'].astype('category')

#9. Set CRS Max Grade to category
tx_ORR_df['clin_AE_CRS_maxgrade'] = tx_ORR_df['clin_AE_CRS_maxgrade'].fillna(value = 0)
tx_ORR_df['clin_AE_CRS_maxgrade'].astype('category')

#10. Set ICANS Max Grade to category
tx_ORR_df['clin_AE_ICANS_maxgrade'] = tx_ORR_df['clin_AE_ICANS_maxgrade'].fillna(value = 0)
tx_ORR_df['clin_AE_ICANS_maxgrade'].astype('category')


#11. Create new G3+ CRS and ICANS Boolean columns

tx_ORR_df['SAE_CRS_G3_grp'] = tx_ORR_df.clin_AE_CRS_maxgrade.map({0.0: False, 1.0: False, 2.0: False, 3.0: True, 4.0: True, 5.0: True})
tx_ORR_df['SAE_ICANS_G3_grp'] = tx_ORR_df.clin_AE_ICANS_maxgrade.map({0.0: False, 1.0: False, 2.0: False, 3.0: True, 4.0: True, 5.0: True})

#12. Format mortality event into Boolean

tx_ORR_df['pt_death_event'] = tx_ORR_df['clin_outcomes_pt_mortality'].map({'No': True,
                                                                               'Yes': False})

#13. Filter, join, drop empty and irrelevant columns
tx_ORR_df = tx_ORR_df.filter(['tx_biobank_id',
                                  'dems_pt_age',
                                  'dems_pt_age_grp',
                                  'clin_dz_type',
                                  'clin_dz_status_tx',
                                  'clin_dz_IPI_score_apher',
                                  'clin_tx_inf_dt',
                                  'clin_dz_prior_ther_ct',
                                  'clin_dz_prior_auto_HSCT',
                                  'clin_dz_prior_allo_HSCT',
                                  'clin_AE_CRS_maxgrade',
                                  'SAE_CRS_G3_grp',
                                  'clin_AE_ICANS_maxgrade',
                                  'SAE_ICANS_G3_grp',
                                  'clin_dz_stage_apher',
                                  'clin_dz_cell_orig_Hans',
                                  'clin_tx_inf_ECOG_KPS',
                                  'pt_death_event',
                                  'clin_outcomes_pt_DOD',
                                  'clin_outcomes_pt_DOLC'])



#14. Join baseline inflammation data
tx_ORR_df = tx_ORR_df.join([base_CRP_df])
tx_ORR_df = tx_ORR_df.dropna(subset = ['clin_dz_type'])

#15. Join imaging outcomes data
tx_ORR_df = tx_ORR_df.join([imag_df])
tx_ORR_df = tx_ORR_df.drop(columns = ['imag_pet_ct',
                                              'imag_ct',
                                              'imag_crf_complete'])


#16. Set Dz Stage, ECOG to category type or summary stats
tx_ORR_df['clin_dz_stage_apher'].astype('category')

#17. Map ECOG inputs to integer values
tx_ORR_df['base_ECOG'] = tx_ORR_df['clin_tx_inf_ECOG_KPS'].map({'0 (100-90)': 0,
                                                                      '1 (80-70)': 1,
                                                                      '2 (60-50)': 2})

#18. Map overall response to binary
tx_ORR_df['overall_resp_bin'] = tx_ORR_df['overall_resp'].map({True: 1,
                                                                         False: 0})

tx_ORR_df.head()


# In[ ]:


#ORR 30d s/p tx infusion dataframe

tx_ORR30_df = tx_ORR_df.copy(deep = True)
tx_ORR30_df = tx_ORR30_df.where(tx_ORR30_df['imag_timept'] == 'Day 30 (+/- 7 days)')
tx_ORR30_df = tx_ORR30_df.dropna(subset = ['dems_pt_age'])

#tx_ORR30_df.dtypes
tx_ORR30_df
#write ORR30 data to new CSV file
tx_ORR30_df.to_csv('tx_core_ORR30_yesc.csv')

#tx_ORR30_df.head()
#Descriptive statistics for numerical value columns of 30d ORR cohort
#tx_ORR30_df.describe()


# In[ ]:


#SUMMARY STATISTICS FOR SUBJECTS WITH DAY 30 OUTCOMES DATA 
print('SUMMARY STATISTICS - SUBJECTS WITH DAY 30 OUTCOMES DATA: \n')


#Patients
tx_ORR30_subject_ct = tx_ORR30_df['dems_pt_age'].count()

#Patients by DLBCL or HGBL/tFL
tx_ORR30_DLBCL_ct = tx_ORR30_df['clin_dz_type'].where(tx_ORR30_df['clin_dz_type'] == 'DLBCL').count()
tx_ORR30_HGBL_ct = tx_ORR30_df['clin_dz_type'].where(tx_ORR30_df['clin_dz_type'] == 'HGBL').count()
tx_ORR30_tFL_ct = tx_ORR30_df['clin_dz_type'].where(tx_ORR30_df['clin_dz_type'] == 'tFL').count()

print('DLBCL (Count, %): ',
      tx_ORR30_DLBCL_ct,
      ' ({0:.1f})'.format((tx_ORR30_DLBCL_ct/tx_ORR30_subject_ct)*100), sep = '')

print('HGBL/tFL (Count, %): ',
      (tx_ORR30_HGBL_ct + tx_ORR30_tFL_ct),
      ' ({0:.1f})'.format(((tx_ORR30_HGBL_ct + tx_ORR30_tFL_ct)/tx_ORR30_subject_ct)*100), sep = '')


#Age Median/SD
tx_ORR30_age_median = tx_ORR30_df['dems_pt_age'].median() 
tx_ORR30_age_SD = tx_ORR30_df['dems_pt_age'].std() 

print('\nAge (Median, SD): ', 
      '{0:.1f}'.format(tx_ORR30_age_median), 
      '({0:.1f} - {1:.1f})'.format((tx_ORR30_age_median - tx_ORR30_age_SD),(tx_ORR30_age_median + tx_ORR30_age_SD)))


#Age Group (>=65)
tx_ORR30_age_o65 = tx_ORR30_df['dems_pt_age'].where(tx_ORR30_df['dems_pt_age'] >= 65).count()
tx_ORR30_age_u65 = tx_ORR30_df['dems_pt_age'].where(tx_ORR30_df['dems_pt_age'] < 65).count()

print('Age Group (Count, %):')
print('>= 65: ', tx_ORR30_age_o65, ' ({0:.1f})'.format((tx_ORR30_age_o65/tx_ORR30_subject_ct)*100), sep = '')
print('< 65: ', tx_ORR30_age_u65, ' ({0:.1f})'.format((tx_ORR30_age_u65/tx_ORR30_subject_ct)*100), sep = '')


#Overall Response
tx_ORR30_CR = tx_ORR30_df['imag_resp'].where(tx_ORR30_df['imag_resp'] == 'CR').count()
tx_ORR30_PR = tx_ORR30_df['imag_resp'].where(tx_ORR30_df['imag_resp'] == 'PR').count()
tx_ORR30_SD = tx_ORR30_df['imag_resp'].where(tx_ORR30_df['imag_resp'] == 'SD').count()
tx_ORR30_PD = tx_ORR30_df['imag_resp'].where(tx_ORR30_df['imag_resp'] == 'PD').count()
tx_ORR30_oth = tx_ORR30_df['imag_resp'].where(tx_ORR30_df['imag_resp'] == 'Other').count()
tx_ORR30_tot = (tx_ORR30_CR + tx_ORR30_PR + tx_ORR30_SD + tx_ORR30_PD)

print('\nD30 Outcomes (Count, %):')
print('CR: ', tx_ORR30_CR, ' ({0:.1f})'.format((tx_ORR30_CR/tx_ORR30_tot)*100) ,sep = '')
print('PR: ', tx_ORR30_PR, ' ({0:.1f})'.format((tx_ORR30_PR/tx_ORR30_tot)*100) ,sep = '')
print('SD: ', tx_ORR30_SD, ' ({0:.1f})'.format((tx_ORR30_SD/tx_ORR30_tot)*100) ,sep = '')
print('PD: ', tx_ORR30_PD, ' ({0:.1f})'.format((tx_ORR30_PD/tx_ORR30_tot)*100) ,sep = '')
print('Other: ', tx_ORR30_oth, ' ({0:.1f})'.format((tx_ORR30_oth/tx_ORR30_tot)*100) ,sep = '')
print('Overall Response: ', (tx_ORR30_PR + tx_ORR30_CR), ' ({0:.1f})'.format(((tx_ORR30_PR + tx_ORR30_CR)/tx_ORR30_tot)*100) ,sep = '')

#ECOG
tx_ORR30_ECOG_0 = tx_ORR30_df['clin_tx_inf_ECOG_KPS'].where(tx_ORR30_df['clin_tx_inf_ECOG_KPS'] == '0 (100-90)').count()
tx_ORR30_ECOG_1 = tx_ORR30_df['clin_tx_inf_ECOG_KPS'].where(tx_ORR30_df['clin_tx_inf_ECOG_KPS'] == '1 (80-70)').count()
tx_ORR30_ECOG_2 = tx_ORR30_df['clin_tx_inf_ECOG_KPS'].where(tx_ORR30_df['clin_tx_inf_ECOG_KPS'] == '2 (60-50)').count()
tx_ORR30_ECOG_3 = tx_ORR30_df['clin_tx_inf_ECOG_KPS'].where(tx_ORR30_df['clin_tx_inf_ECOG_KPS'] == '3 (40-30)').count()
tx_ORR30_ECOG_4 = tx_ORR30_df['clin_tx_inf_ECOG_KPS'].where(tx_ORR30_df['clin_tx_inf_ECOG_KPS'] == '4 (20-10)').count()

print('\nECOG (KPS) (Count, %):')
print('0 (100-90): ', tx_ORR30_ECOG_0, ' ({0:.1f})'.format((tx_ORR30_ECOG_0/tx_ORR30_subject_ct)*100), 
      '\n1 (80-70): ', tx_ORR30_ECOG_1, ' ({0:.1f})'.format((tx_ORR30_ECOG_1/tx_ORR30_subject_ct)*100), 
      '\n2 (60-50): ', tx_ORR30_ECOG_2, ' ({0:.1f})'.format((tx_ORR30_ECOG_2/tx_ORR30_subject_ct)*100), 
      #'  \n3 (50-40): ', tx_ORR30_ECOG_3, ' ({0:.1f})'.format((tx_ORR30_ECOG_3/tx_ORR30_subject_ct)*100), 
      sep = '')


#Disease Stage
tx_ORR30_dzstage_0 = tx_ORR30_df['clin_dz_stage_apher'].where(tx_ORR30_df['clin_dz_stage_apher'] == 0).count()
tx_ORR30_dzstage_1 = tx_ORR30_df['clin_dz_stage_apher'].where(tx_ORR30_df['clin_dz_stage_apher'] == 1).count()
tx_ORR30_dzstage_2 = tx_ORR30_df['clin_dz_stage_apher'].where(tx_ORR30_df['clin_dz_stage_apher'] == 2).count()
tx_ORR30_dzstage_3 = tx_ORR30_df['clin_dz_stage_apher'].where(tx_ORR30_df['clin_dz_stage_apher'] == 3).count()
tx_ORR30_dzstage_4 = tx_ORR30_df['clin_dz_stage_apher'].where(tx_ORR30_df['clin_dz_stage_apher'] == 4).count()

print('\nDisease Stage (Count, %):')
print('Stage 1-2: ', (tx_ORR30_dzstage_1 + tx_ORR30_dzstage_2), ' ({0:.1f})'.format(((tx_ORR30_dzstage_1 + tx_ORR30_dzstage_2)/tx_ORR30_subject_ct)*100),
      '\nStage 3-4: ', (tx_ORR30_dzstage_3 + tx_ORR30_dzstage_4), ' ({0:.1f})'.format(((tx_ORR30_dzstage_3 + tx_ORR30_dzstage_4)/tx_ORR30_subject_ct)*100), 
      #'S1: ', tx_ORR30_dzstage_1, ' ({0:.1f})'.format((tx_ORR30_dzstage_1/tx_ORR30_subject_ct)*100), 
      #'  \nS2: ', tx_ORR30_dzstage_2, ' ({0:.1f})'.format((tx_ORR30_dzstage_2/tx_ORR30_subject_ct)*100), 
      #'  \nS3: ', tx_ORR30_dzstage_3, ' ({0:.1f})'.format((tx_ORR30_dzstage_3/tx_ORR30_subject_ct)*100), 
      #'  \nS4: ', tx_ORR30_dzstage_4, ' ({0:.1f})'.format((tx_ORR30_dzstage_4/tx_ORR30_subject_ct)*100), 
      sep = '')


#International Prognostic Index Score
tx_ORR30_IPI_0 = tx_ORR30_df['clin_dz_IPI_score_apher'].where(tx_ORR30_df['clin_dz_IPI_score_apher'] == 0).count()
tx_ORR30_IPI_1 = tx_ORR30_df['clin_dz_IPI_score_apher'].where(tx_ORR30_df['clin_dz_IPI_score_apher'] == 1).count()
tx_ORR30_IPI_2 = tx_ORR30_df['clin_dz_IPI_score_apher'].where(tx_ORR30_df['clin_dz_IPI_score_apher'] == 2).count()
tx_ORR30_IPI_3 = tx_ORR30_df['clin_dz_IPI_score_apher'].where(tx_ORR30_df['clin_dz_IPI_score_apher'] == 3).count()
tx_ORR30_IPI_4 = tx_ORR30_df['clin_dz_IPI_score_apher'].where(tx_ORR30_df['clin_dz_IPI_score_apher'] == 4).count()

print('\nIPI Score (Count, %):')
print('0-2: ', (tx_ORR30_IPI_0 + tx_ORR30_IPI_1 + tx_ORR30_IPI_2), ' ({0:.1f})'.format(((tx_ORR30_IPI_0 + tx_ORR30_IPI_1 + tx_ORR30_IPI_2)/tx_ORR30_subject_ct)*100),
      '\n3-4: ', (tx_ORR30_IPI_3 + tx_ORR30_IPI_4), ' ({0:.1f})'.format(((tx_ORR30_IPI_3 + tx_ORR30_IPI_4)/tx_ORR30_subject_ct)*100),
      #'IPI 0: ', tx_ORR30_IPI_0, ' ({0:.1f})'.format((tx_ORR30_IPI_0/tx_ORR30_subject_ct)*100),
      #'  \nIPI 1: ', tx_ORR30_IPI_1, ' ({0:.1f})'.format((tx_ORR30_IPI_1/tx_ORR30_subject_ct)*100), 
      #'  \nIPI 2: ', tx_ORR30_IPI_2, ' ({0:.1f})'.format((tx_ORR30_IPI_2/tx_ORR30_subject_ct)*100), 
      #'  \nIPI 3: ', tx_ORR30_IPI_3, ' ({0:.1f})'.format((tx_ORR30_IPI_3/tx_ORR30_subject_ct)*100), 
      #'  \nIPI 4: ', tx_ORR30_IPI_4, ' ({0:.1f})'.format((tx_ORR30_IPI_4/tx_ORR30_subject_ct)*100), 
      sep = '')


#Prior Therapies
tx_ORR30_priorther_2 = tx_ORR30_df['clin_dz_prior_ther_ct'].where(tx_ORR30_df['clin_dz_prior_ther_ct'] <= 2).count()
tx_ORR30_priorther_3 = tx_ORR30_df['clin_dz_prior_ther_ct'].where(tx_ORR30_df['clin_dz_prior_ther_ct'] >= 3).count()

print('\nPrior Therapies (Count, %):')
print('1-2: ', tx_ORR30_priorther_2, ' ({0:.1f})'.format((tx_ORR30_priorther_2/tx_ORR30_subject_ct)*100), 
      '\n3+: ', tx_ORR30_priorther_3, ' ({0:.1f})'.format((tx_ORR30_priorther_3/tx_ORR30_subject_ct)*100),
      sep = '')


#Disease Status 
tx_ORR30_dzstat_rel = tx_ORR30_df['clin_dz_status_tx'].where(tx_ORR30_df['clin_dz_status_tx'] == 'relapsed').count()
tx_ORR30_dzstat_pref = tx_ORR30_df['clin_dz_status_tx'].where(tx_ORR30_df['clin_dz_status_tx'] == 'primary refractory').count()
tx_ORR30_dzstat_ref = tx_ORR30_df['clin_dz_status_tx'].where(tx_ORR30_df['clin_dz_status_tx'] == 'refractory').count()

print('\nDisease Status (Count, %):')
print('Relapsed: ', tx_ORR30_dzstat_rel, ' ({0:.1f})'.format((tx_ORR30_dzstat_rel/tx_ORR30_subject_ct)*100), 
      '\nPrimary Refractory: ', tx_ORR30_dzstat_pref, ' ({0:.1f})'.format((tx_ORR30_dzstat_pref/tx_ORR30_subject_ct)*100),
      '\nRefractory: ', tx_ORR30_dzstat_ref, ' ({0:.1f})'.format((tx_ORR30_dzstat_ref/tx_ORR30_subject_ct)*100),
      sep = '')


#CRS Incidence
tx_ORR30_CRS_G1 = tx_ORR30_df['clin_AE_CRS_maxgrade'].where(tx_ORR30_df['clin_AE_CRS_maxgrade'] == 1).count()
tx_ORR30_CRS_G2 = tx_ORR30_df['clin_AE_CRS_maxgrade'].where(tx_ORR30_df['clin_AE_CRS_maxgrade'] == 2).count()
tx_ORR30_CRS_G3 = tx_ORR30_df['clin_AE_CRS_maxgrade'].where(tx_ORR30_df['clin_AE_CRS_maxgrade'] == 3).count()

print('\nCRS AE Incidence (Count, %):')
print('G1: ', tx_ORR30_CRS_G1, ' ({0:.1f})'.format((tx_ORR30_CRS_G1/tx_ORR30_subject_ct)*100), 
      '  \nG2: ', tx_ORR30_CRS_G2, ' ({0:.1f})'.format((tx_ORR30_CRS_G2/tx_ORR30_subject_ct)*100), 
      '  \nG3: ', tx_ORR30_CRS_G3, ' ({0:.1f})'.format((tx_ORR30_CRS_G3/tx_ORR30_subject_ct)*100), 
      sep = '')


#ICANS Incidence
tx_ORR30_ICANS_G1 = tx_ORR30_df['clin_AE_ICANS_maxgrade'].where(tx_ORR30_df['clin_AE_ICANS_maxgrade'] == 1).count()
tx_ORR30_ICANS_G2 = tx_ORR30_df['clin_AE_ICANS_maxgrade'].where(tx_ORR30_df['clin_AE_ICANS_maxgrade'] == 2).count()
tx_ORR30_ICANS_G3 = tx_ORR30_df['clin_AE_ICANS_maxgrade'].where(tx_ORR30_df['clin_AE_ICANS_maxgrade'] == 3).count()
tx_ORR30_ICANS_G4 = tx_ORR30_df['clin_AE_ICANS_maxgrade'].where(tx_ORR30_df['clin_AE_ICANS_maxgrade'] == 4).count()

print('\nICANS AE Incidence (Count, %):')
print('G1: ', tx_ORR30_ICANS_G1, ' ({0:.1f})'.format((tx_ORR30_ICANS_G1/tx_ORR30_subject_ct)*100), 
      '  \nG2: ', tx_ORR30_ICANS_G2, ' ({0:.1f})'.format((tx_ORR30_ICANS_G2/tx_ORR30_subject_ct)*100), 
      '  \nG3: ', tx_ORR30_ICANS_G3, ' ({0:.1f})'.format((tx_ORR30_ICANS_G3/tx_ORR30_subject_ct)*100),
      '  \nG4: ', tx_ORR30_ICANS_G4, ' ({0:.1f})'.format((tx_ORR30_ICANS_G4/tx_ORR30_subject_ct)*100), 
      sep = '')


# In[ ]:


#Exact Binomial Tests: 
#1. Commercial Outcomes > SOC Alternative Outcomes ORR = 20% at 30d s/p Treatment
#2. Commercial Outcomes > or < Clinical Trial Outcomes ORR = 82% at 30d s/p Treatment


from scipy import stats
import statsmodels

#Binomial test for commercial Treatment outcomes greater than SOC alternative outcomes
ebinom_tx_ORR30_SOC_pval = scp.stats.binom_test(10, n = 17, p = 0.2, alternative = 'greater')

#Binomial test for commercial Treatment outcomes greater or less than clinical trial Treatment outcomes
ebinom_tx_ORR30_study_pval = scp.stats.binom_test(10, n = 17, p = 0.82, alternative = 'two-sided')

#Response rates
tx_ORR30_ORR = (tx_ORR30_CR + tx_ORR30_PR)/tx_ORR30_tot
tx_ORR30_CRR = tx_ORR30_CR/tx_ORR30_tot
tx_ORR30_PRR = tx_ORR30_PR/tx_ORR30_tot

#Calculate confidence interval for a binomial proportion
from statsmodels.stats import proportion

#Clopper-Pearson interval based on cumulative probabilities of binomial distribution
tx_ORR30_binom_CI = statsmodels.stats.proportion.proportion_confint(10, 
                                                                      17, 
                                                                      alpha=0.05, 
                                                                      method='beta') #Clopper-Pearson method

print('Exact Binomial Test: Commercial Axicabtagene Ciloleucel D30 ORR')
print('CI calculated with Clopper-Pearson method')

print('\nOverall Response Rate (95% CI): {:.3f} ({:.3f}-{:.3f}) \nCR Rate: {:.3f} \nPR Rate: {:.3f}'.format(tx_ORR30_ORR,
                                                                                                           tx_ORR30_binom_CI[0],
                                                                                                           tx_ORR30_binom_CI[1],                                                                                              tx_ORR30_CRR,
                                                                                                           tx_ORR30_PRR))
print('\nCommercial Treatment vs SOC Alternative Outcomes')
print('n = {0:d} \t p(success) = 0.2'.format(tx_ORR30_tot))
print('p-value = {0:.5f}'.format(ebinom_tx_ORR30_SOC_pval))

print('\nCommercial Treatment vs Clinical Trial Treatment Outcomes')
print('n = {0:d} \t p(success) = 0.82'.format(tx_ORR30_tot))
print('p-value = {0:.5f}'.format(ebinom_tx_ORR30_study_pval))


# In[ ]:


#Secondary endpoints data frame
#Association between peak serum ferritin, CRP biomarkers vs SAE ICANS, SAE CRS
wilson_cmp_SAE_df = tx_ORR30_df.copy(deep = True)

#select columns of interest to calculate overall survival (date of infusion - dod)
#and SAE group comparison with serum biomarkers
wilson_cmp_SAE_df = wilson_cmp_SAE_df.filter(['SAE_CRS_G3_grp',
                                              'SAE_ICANS_G3_grp'])

#drop empty rows
wilson_cmp_SAE_df = wilson_cmp_SAE_df.reset_index()
wilson_cmp_SAE_df = wilson_cmp_SAE_df.drop_duplicates(subset = ['tx_biobank_id'], 
                                                      keep = 'first', 
                                                      inplace = False) 

#isolate peak CRP and peak Ferritin values from labs dataframe
wilson_cmp_CRP_df = labs_df.groupby(['tx_biobank_id'], sort=False)['lab_cmp_CRP'].max()
wilson_cmp_ferr_df = labs_df.groupby(['tx_biobank_id'], sort=False)['lab_cmp_ferritin'].max()


#join peak serum biomarker values to main wilson df
wilson_cmp_SAE_df = wilson_cmp_SAE_df.join(wilson_cmp_CRP_df, on = 'tx_biobank_id')
wilson_cmp_SAE_df = wilson_cmp_SAE_df.join(wilson_cmp_ferr_df, on = 'tx_biobank_id')

#set index back to repository ID
wilson_cmp_SAE_df = wilson_cmp_SAE_df.set_index(['tx_biobank_id'])

wilson_cmp_SAE_df


# In[ ]:


#Wilcoxon rank-sum/Mann-Whitney U test: 

#Wilcoxon rank-sum is used to determine whether two data samples have different
#distributions where data does not have Gaussian distribution. This
#non-parametric test transforms data into rank data before testing

#p > alpha (0.05): it is the same distribution between groups
#p <= alpha (0.05): reject null hypothesis

#Parameters:
    #i. Holm's procedure adjustment of p-values 
    #ii. CI calculations by Clopper-Pearson method

#i. Holm-Bonferroni method mitigates family-wise error rate. More hypotheses generate
#a higher probability of a Type I (false positive) error. Holm-Bonferroni adjusts the
#rejection criteria of each of the individual hypotheses

#ii. Clopper-Pearson is exact method of determining CI as above
#NOTE: Wilcoxon rank-sum = Mann-Whitney U test, which tests independent
#samples. Wilcoxon signed-rank tests dependent samples. 

#MWU is a non-parametric test of H0:
#H0: it is equally likely that a random value from one sample will be less or greater than 
#a randomly selected value from a second sample. It does not assume normal distributions

#U statistic is min(U for x, U for y)
#p is p-value

#set variables by aggregating serum biomarker values by respective SAE incidence
peak_CRP_ICANS_y = wilson_cmp_SAE_df.loc[wilson_cmp_SAE_df['SAE_ICANS_G3_grp'] > 0, 'lab_cmp_CRP']
peak_CRP_ICANS_n = wilson_cmp_SAE_df.loc[wilson_cmp_SAE_df['SAE_ICANS_G3_grp'] == 0, 'lab_cmp_CRP']

peak_CRP_CRS_y = wilson_cmp_SAE_df.loc[wilson_cmp_SAE_df['SAE_CRS_G3_grp'] > 0, 'lab_cmp_CRP']
peak_CRP_CRS_n = wilson_cmp_SAE_df.loc[wilson_cmp_SAE_df['SAE_CRS_G3_grp'] == 0, 'lab_cmp_CRP']

peak_ferr_ICANS_y = wilson_cmp_SAE_df.loc[wilson_cmp_SAE_df['SAE_ICANS_G3_grp'] > 0, 'lab_cmp_ferritin']
peak_ferr_ICANS_n = wilson_cmp_SAE_df.loc[wilson_cmp_SAE_df['SAE_ICANS_G3_grp'] == 0, 'lab_cmp_ferritin']

peak_ferr_CRS_y = wilson_cmp_SAE_df.loc[wilson_cmp_SAE_df['SAE_CRS_G3_grp'] > 0, 'lab_cmp_ferritin']
peak_ferr_CRS_n = wilson_cmp_SAE_df.loc[wilson_cmp_SAE_df['SAE_CRS_G3_grp'] == 0, 'lab_cmp_ferritin']

#function for two-sided MWU test
def mwu_SAE_biomarkers(SAE_grp, biomarker):
    stat, p = scp.stats.mannwhitneyu(SAE_grp, 
                   y = biomarker, 
                   use_continuity = True,
                   alternative = 'two-sided')
    if p < 0.001:
        return print('U-Statistic: ', stat, '\np-value: <0.001', sep = '')
    else:
        return print('U-Statistic: ', stat, '\np-value: {:.3f}'.format(p), sep = '')
                     #', stat, '\np-value: ', p, sep = '')

#1. Peak ferritin ~ ICANS (G0-2/G3+)
print('\nICANS SAE Association with Peak Serum Ferritin:')
mwu_SAE_biomarkers(peak_ferr_ICANS_y, peak_ferr_ICANS_n)

#2. Peak ferritin ~ CRS (G0-2/G3+)
print('\nCRS SAE Association with Peak Serum Ferritin:')
mwu_SAE_biomarkers(peak_ferr_CRS_y, peak_ferr_CRS_n)

#3. Peak CRP ~ ICANS (G0-2/G3+)
print('\nICANS SAE Association with Peak Serum CRP:')
mwu_SAE_biomarkers(peak_CRP_ICANS_y, peak_CRP_ICANS_n)

#4. Peak CRP ~ CRS (G0-2/G3+)
print('\nCRS SAE Association with Peak Serum CRP:')
mwu_SAE_biomarkers(peak_CRP_CRS_y, peak_CRP_CRS_n)


# In[ ]:


#Data Frames for MWU Boxplots

#omit outlier ferritin value(s)
wilson_cmp_SAE_df = wilson_cmp_SAE_df.where(wilson_cmp_SAE_df['lab_cmp_ferritin'] < 15000)

#1. MWU Boxplot DF - G3+ ICANS 
wilson_g3_ICANS_df = wilson_cmp_SAE_df.where(wilson_cmp_SAE_df['SAE_ICANS_G3_grp'] == 1)
wilson_g3_ICANS_df = wilson_g3_ICANS_df.dropna(subset = ['SAE_ICANS_G3_grp'])
#wilson_g3_ICANS_df

#2. MWU Boxplot DF - G0-2 ICANS 
wilson_g12_ICANS_df = wilson_cmp_SAE_df.where(wilson_cmp_SAE_df['SAE_ICANS_G3_grp'] == 0)
wilson_g12_ICANS_df = wilson_g12_ICANS_df.dropna(subset = ['SAE_ICANS_G3_grp'])
#wilson_g12_ICANS_df

#3. MWU Boxplot DF - G3+ CRS
wilson_g3_CRS_df = wilson_cmp_SAE_df.where(wilson_cmp_SAE_df['SAE_CRS_G3_grp'] == 1)
wilson_g3_CRS_df = wilson_g3_CRS_df.dropna(subset = ['SAE_CRS_G3_grp'])
#wilson_g3_CRS_df

#4. MWU Boxplot DF - G0-2 CRS
wilson_g12_CRS_df = wilson_cmp_SAE_df.where(wilson_cmp_SAE_df['SAE_CRS_G3_grp'] == 0)
wilson_g12_CRS_df = wilson_g12_CRS_df.dropna(subset = ['SAE_CRS_G3_grp'])
#wilson_g12_CRS_df.head()


# In[ ]:


#1. ICANS CRP Boxplot

ICANS_boxplot_CRP_data = [wilson_g12_ICANS_df['lab_cmp_CRP'], wilson_g3_ICANS_df['lab_cmp_CRP']]
fig1, ax1 = plt.subplots()
ax1.set_title('ICANS SAE Incidence vs Serum Biomarker CRP')
ax1.set_xlabel('ICANS SAE Groups')
ax1.set_ylabel('Serum C-Reactive Protein (mg/L)')

labels = ['Grade 0-2', 'Grade 3+']
bp1 = ax1.boxplot(ICANS_boxplot_CRP_data, notch=0, vert=1, patch_artist=False, whis=1.5, labels = labels)
plt.setp(bp1['boxes'], color='black')
plt.setp(bp1['whiskers'], color='black')
plt.setp(bp1['fliers'], color='red', marker='.')
plt.show()

mean_g12_ICANS_CRP = wilson_g12_ICANS_df['lab_cmp_CRP'].mean()
std_g12_ICANS_CRP = wilson_g12_ICANS_df['lab_cmp_CRP'].std()
print('\nG0-2 ICANS Group CRP: \nMean (SD): {:.2f} (+/-{:.2f}) ng/mL'.format(mean_g12_ICANS_CRP, std_g12_ICANS_CRP))
mean_g3_ICANS_CRP = wilson_g3_ICANS_df['lab_cmp_CRP'].mean()
std_g3_ICANS_CRP = wilson_g3_ICANS_df['lab_cmp_CRP'].std()
print('\nG3+ ICANS Group CRP: \nMean (SD): {:.2f} (+/-{:.2f}) ng/mL'.format(mean_g3_ICANS_CRP, std_g3_ICANS_CRP))


# In[ ]:


#2. ICANS Ferritin Boxplot

ICANS_boxplot_ferr_data = [wilson_g12_ICANS_df['lab_cmp_ferritin'], wilson_g3_ICANS_df['lab_cmp_ferritin']]
fig2, ax2 = plt.subplots()
ax2.set_title('ICANS SAE Incidence vs Serum Biomarker Ferritin')
ax2.set_xlabel('ICANS Adverse Event Groups')
ax2.set_ylabel('Serum Ferritin (ng/mL)')

labels = ['Grade 0-2', 'Grade 3+']
bp2 = ax2.boxplot(ICANS_boxplot_ferr_data, notch=0, vert=1, patch_artist=False, whis=1.5, labels = labels)
plt.setp(bp2['boxes'], color='black')
plt.setp(bp2['whiskers'], color='black')
plt.setp(bp2['fliers'], color='red', marker='.')
plt.show()
plt.show()

mean_g12_ICANS_ferr = wilson_g12_ICANS_df['lab_cmp_ferritin'].mean()
std_g12_ICANS_ferr = wilson_g12_ICANS_df['lab_cmp_ferritin'].std()
print('\nG0-2 ICANS Group Ferritin: \nMean (SD): {:.2f} (+/-{:.2f}) mg/L'.format(mean_g12_ICANS_ferr, std_g12_ICANS_ferr), sep = '')
mean_g3_ICANS_ferr = wilson_g3_ICANS_df['lab_cmp_ferritin'].mean()
std_g3_ICANS_ferr = wilson_g3_ICANS_df['lab_cmp_ferritin'].std()
print('\nG3+ ICANS Group Ferritin: \nMean (SD): {:.2f} (+/-{:.2f}) mg/L'.format(mean_g3_ICANS_ferr, std_g3_ICANS_ferr), sep = '')


# In[ ]:


#3. CRS CRP Boxplot

CRS_boxplot_CRP_data = [wilson_g12_CRS_df['lab_cmp_CRP'], wilson_g3_CRS_df['lab_cmp_CRP']]
fig3, ax3 = plt.subplots()
ax3.set_title('CRS SAE Incidence vs Serum Biomarker CRP')
ax3.set_xlabel('CRS Adverse Event Groups')
ax3.set_ylabel('Serum C-Reactive Protein (mg/L)')

labels = ['Grade 0-2', 'Grade 3+']
bp3 = ax3.boxplot(CRS_boxplot_CRP_data, notch=0, vert=1, patch_artist=False, whis=1.5, labels = labels)
plt.setp(bp3['boxes'], color='black')
plt.setp(bp3['whiskers'], color='black')
plt.setp(bp3['fliers'], color='red', marker='.')
plt.show()


mean_g12_CRS_CRP = wilson_g12_CRS_df['lab_cmp_CRP'].mean()
std_g12_CRS_CRP = wilson_g12_CRS_df['lab_cmp_CRP'].std()
print('\nG0-2 CRS Group CRP: \nMean (SD): {:.2f} (+/-{:.2f}) ng/mL'.format(mean_g12_CRS_CRP, std_g12_CRS_CRP), sep = '')
mean_g3_CRS_CRP = wilson_g3_CRS_df['lab_cmp_CRP'].mean()
std_g3_CRS_CRP = wilson_g3_CRS_df['lab_cmp_CRP'].std()
print('\nG3+ CRS Group CRP: \nMean (SD): {:.2f} (+/-{:.2f}) ng/mL'.format(mean_g3_CRS_CRP, std_g3_CRS_CRP))


# In[ ]:


#4. CRS CRP Boxplot

CRS_boxplot_ferr_data = [wilson_g12_CRS_df['lab_cmp_ferritin'], wilson_g3_CRS_df['lab_cmp_ferritin']]
fig4, ax4 = plt.subplots()
ax4.set_title('CRS SAE Incidence vs Serum Biomarker Ferritin')
ax4.set_xlabel('CRS Adverse Event Groups')
ax4.set_ylabel('Serum Ferritin (ng/mL)')

labels = ['Grade 0-2', 'Grade 3+']
bp4 = ax4.boxplot(CRS_boxplot_ferr_data, notch=0, vert=1, patch_artist=False, whis=1.5, labels = labels)
plt.setp(bp4['boxes'], color='black')
plt.setp(bp4['whiskers'], color='black')
plt.setp(bp4['fliers'], color='red', marker='.')
plt.show()


mean_g12_CRS_ferr = wilson_g12_CRS_df['lab_cmp_ferritin'].mean()
std_g12_CRS_ferr = wilson_g12_CRS_df['lab_cmp_ferritin'].std()
print('\nG0-2 CRS Group Ferritin: \nMean (SD): {:.2f} (+/-{:.2f}) ng/mL'.format(mean_g12_CRS_ferr, std_g12_CRS_ferr), sep = '')
mean_g3_CRS_ferr = wilson_g3_CRS_df['lab_cmp_ferritin'].mean()
std_g3_CRS_ferr = wilson_g3_CRS_df['lab_cmp_ferritin'].std()
print('\nG3+ CRS Group Ferritin: \nMean (SD): {:.2f} (+/-{:.2f}) ng/mL'.format(mean_g3_CRS_ferr, std_g3_CRS_ferr))


# In[ ]:


#Kaplan-Meier Survival Data Frame


tx_kaplan_df = tx_ORR_df.copy(deep = True)

#select dates to calculate timedelta and responses
tx_kaplan_df = tx_kaplan_df.filter(['imag_resp',
                                        'overall_resp',
                                        'imag_dt',
                                        'clin_tx_inf_dt',
                                        'pt_death_event',
                                        'clin_outcomes_pt_DOLC'])


#drop empty rows
tx_kaplan_df = tx_kaplan_df.dropna(subset = ['overall_resp'])

#calculate PFS interval and convert to int type
tx_kaplan_df['imag_resp_interval'] = tx_kaplan_df['imag_dt'] - tx_kaplan_df['clin_tx_inf_dt']
tx_kaplan_df['imag_resp_interval'] = (tx_kaplan_df['imag_resp_interval'] /  np.timedelta64(1, 'D')).astype(int)

#calculate OS interval and convert to int type
tx_kaplan_df['DODOLC_interval'] = tx_kaplan_df['clin_outcomes_pt_DOLC'] - tx_kaplan_df['clin_tx_inf_dt']
tx_kaplan_df['DODOLC_interval'] = (tx_kaplan_df['DODOLC_interval'] /  np.timedelta64(1, 'D')).astype(int)

#Map overall response to binaries, response = 1
tx_kaplan_df['overall_resp_bin'] = tx_kaplan_df['overall_resp'].map({True: 1,
                                                                         False: 0})
#Map death event to binaries, alive = 1
tx_kaplan_df['death_bin'] = tx_kaplan_df['pt_death_event'].map({True: 0,
                                                               False: 1})

#sort dataframe by index then by interval days to response
tx_kaplan_df['col_index'] = tx_kaplan_df.index
tx_kaplan_df = tx_kaplan_df.sort_values(['col_index','imag_resp_interval'])
#tx_kaplan_df = tx_kaplan_df.sort_values(by = 'imag_resp_interval', ascending = True)

tx_kaplan_df.head()


# In[ ]:


#Kaplan Meier Survival curve function from lifelines module
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter()

#variables for PFS/OS intervals and events
pfs_days = tx_kaplan_df['imag_resp_interval']
pfs_event = tx_kaplan_df['overall_resp_bin']

os_days = tx_kaplan_df['DODOLC_interval']
os_event = tx_kaplan_df['death_bin']

#tx_kaplan_df
print('Kaplan-Meier Estimates: OS/PFS \ny = OS/PFS (%) \nx = Days')
kmf.fit(os_days, event_observed = os_event, timeline = range(20, 180, 2), label = 'OS')
ax = kmf.plot()

#fit PFS to overlay on OS graph
kmf.fit(pfs_days, event_observed = pfs_event, timeline = range(20, 180, 2), label = 'PFS')
ax = kmf.plot(ax = ax)


# In[ ]:


#Clinical trial vs commercial cohort:

#Baseline CRP inflammation, ALC at apheresis not reported in publication

#Example T-test for one-group mean: comparing commercial cohort to clinical 
#trial population baseline CRP at apheresis:

#baseline_CRP = tx_ORR_df['lab_cmp_CRP']
#baseline_CRP = baseline_CRP.dropna()
#scp.stats.ttest_1samp(baseline_CRP,popmean = 1, axis = 0) #popmean = comparator population mean

#function for 1-sided sample comparison of means between commercial and trial data
def ttest_1samp_func(test_array, ref_mean):
    stat, p = scp.stats.ttest_1samp(test_array, 
                                    popmean = ref_mean, 
                                    axis = 0)
    mean = test_array.mean()
    return print('Commercial Mean: {:.3f} \tStudy Mean: {:.3f} \nT-statistic: {:.3f} \tp-value: {:.3f}'.format(mean, 
                                                                                                         ref_mean, 
                                                                                                         stat, 
                                                                                                         p), sep = '')
    
print('1-Sample T-tests vs. Clinical Trial Population Mean:')

#1. Baseline ECOGs
ECOG_comp_df = tx_ORR_df.copy(deep = True)
ECOG_comp_df = ECOG_comp_df.drop_duplicates(subset = ['tx_biobank_id'], keep = 'first', inplace = False)
ECOG_comp_df = ECOG_comp_df.dropna(subset = ['base_ECOG'])
ECOG_comp_df['base_ECOG'] = (ECOG_comp_df['base_ECOG']).astype(int)
ECOG_base = ECOG_comp_df['base_ECOG']

#59 subjects with ECOG = 1 of 101 evaluable in literature, mean ECOG = 0.525
print('\nECOG:')
ttest_1samp_func(ECOG_base, 0.525)

#2. Bulky dz
bulkdz_comp_df = tx_core_df.copy(deep = True)
bulkdz_comp_df = bulkdz_comp_df.drop_duplicates(subset = ['tx_biobank_id'], keep = 'first', inplace = False)
bulkdz_comp_df = bulkdz_comp_df.dropna(subset = ['clin_dz_bulky'])
bulkdz_comp_df['base_bulkdz'] = bulkdz_comp_df['clin_dz_bulky'].map({'No': 0, 'Yes': 1})
bulkdz_base = bulkdz_comp_df['base_bulkdz']

#17 subjects with bulky disease of 101 evaluable in literature, mean bulky dz = 0.168
print('\nBulky Disease:')
ttest_1samp_func(bulkdz_base, 0.168)




# In[ ]:


#Data Reconstruction: Produce 1000 dummy patients for SVM analysis

#SVM Classification of responders vs non-responders:

#FEATURES
#y-var: [Boolean, calculated] Overall Response
#xvars: 
    #1. [Categorical] International Prognostic Index (IPI),
    #2. [Boolean] Patient age (years), group by 18-64, 65+
    #3. [Categorical] Primary disease stage (Lugano 2014 classification),
    #4. [Categorical] Primary disease histology (large B-cell lymphoma subclassification),
    #5. [Boolean] Baseline inflammation state (C-Reactive Protein > 100),
    #6. [Categorical] Previous lines of chemotherapy (count),
    #7. [Boolean] Incidence of G3+ cytokine release syndrome (CRS) serious adverse event (SAE),
    #8. [Boolean] Incidence of G3+ immune-effector cell-associated neurotoxicity syndrom (ICANS) SAE,
    #9. [Categorical] Primary disease molecular subtype
    #10. [Boolean] Prior autologous hematopoietic stem cell transplant (HSCT)
    #11. [Boolean] Prior allogeneic HSCT
    #12. [Categorical] Baseline disease status 'clin_dz_status_tx'

#create column for overall response with randomized binary integers
#1= Yes, 0 = No
svm_df = pd.DataFrame(np.random.randint(0, 2, size = (1000, 1)), columns = ['overall_resp_bin'])

#create column for consecutive dummy biobank IDs starting at 10000
svm_df['tx_biobank_id'] = pd.Series(range(10000,11000,1))

#1. create column for International Prognostic Index values
#IPI range is 0-4
svm_df['clin_dz_IPI_score_apher'] = np.random.randint(0, 5, size = (1000, 1))

#2. create column for age group with randomized binary integers
#1 = 65+, 0 = 18-64
svm_df['dems_pt_age_grp'] = np.random.randint(0, 2, size = (1000, 1))
#tx_ORR_df['dems_pt_age_grp'] = pd.cut(tx_ORR_df['dems_pt_age'], range(0, 130, 64))

#3. create column for disease stage at apheresis, 
#Range: 0-4
svm_df['clin_dz_stage_apher'] = np.random.randint(1, 5, size = (1000, 1))

#4. create column for disease type
#DLBCL = 0, tFL = 1, HGBL = 2
svm_df['clin_dz_type'] = np.random.randint(0, 3, size = (1000, 1))

#5. create column for baseline inflammation status
#Baseline CRP > 100: 1, CRP <= 100: 0
svm_df['base_CRP_inflamm'] = np.random.randint(0, 2, size = (1000, 1))

#6. create column for previous lines of chemotherapy
#Count range 0-8
svm_df['clin_dz_prior_ther_ct'] = np.random.randint(0, 9, size = (1000,1))

#7. create column for incidence of SAE CRS
#1 = Yes, 0 = No
svm_df['SAE_CRS_G3_grp'] = np.random.randint(0, 2, size = (1000,1))

#8. create column for incidence of SAE ICANS
#1 = Yes, 0 = No
svm_df['SAE_ICANS_G3_grp'] = np.random.randint(0, 2, size = (1000,1))

#9. create column for primary disease molecular subtype
#1 = GBC, 0 = ABC/non-GBC
svm_df['clin_dz_cell_orig_Hans'] = np.random.randint(0, 2, size = (1000,1))

#10. create column for prior autologous HSCT
#1 = Yes, 0 = No
svm_df['clin_dz_prior_auto_HSCT'] = np.random.randint(0, 2, size = (1000,1))

#11. create column for prior allo HSCT
#1 = Yes, 0 = No
svm_df['clin_dz_prior_allo_HSCT'] = np.random.randint(0, 2, size = (1000,1))

#12. create column for baseline disease status 
#0 = relapsed, 1 = primary refractory, 2 = refractory
svm_df['clin_dz_status_tx'] = np.random.randint(0, 3, size = (1000,1))


svm_df.head()


# In[ ]:


#summary stats outputs for target columns
def set_dist_target(target):
    target_min = min(target)
    target_max = max(target)
    target_mean = (target).mean()
    target_std = (target).std()
    return [target_min, target_max, target_mean, target_std]

#Normal distribution function to set random values to mean/SD parameters
from scipy.stats import norm
import random 
def norm_dist_set(min_x, max_x, mean, std, n):
    data_series = norm.rvs(loc = mean, scale = std, size = n)
    data_series = np.clip(data_series, min_x, max_x)
    random.shuffle(data_series)
    return data_series

#Verify summary stats function
age_test = set_dist_target(tx_ORR30_df['dems_pt_age']) 
print(age_test)
print(min(tx_ORR30_df['dems_pt_age']), 
      max(tx_ORR30_df['dems_pt_age']),
      tx_ORR30_df['dems_pt_age'].mean(),
      tx_ORR30_df['dems_pt_age'].std())


# In[ ]:


#Create dataframe with distributions using mean/std real data

#set array size to 1000
n = 1000


#Create dataframe for overall response with randomized binary integers
#1= Yes, 0 = No
svm_dist_df = pd.DataFrame(np.random.randint(0, 2, size = (1000, 1)), columns = ['overall_resp_bin'])
#Collect min/max, mean, std stats from column of real values
col_target = set_dist_target(tx_ORR30_df['overall_resp'])
#Set column values using normal dist function on real dataframe column
or_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['overall_resp'] = or_randset
#set integer for boolean status of response
#1 = CR or PR (Yes), 0 = SD or PD (No)
svm_dist_df['overall_resp_bin'] = svm_dist_df['overall_resp'].apply(lambda x: 0 if x <= 0.5 else 1)
#drop non-binary column
svm_dist_df = svm_dist_df.drop(labels = 'overall_resp', axis = 1)

#Create column for consecutive dummy biobank IDs starting at 10000
svm_dist_df['tx_biobank_id'] = pd.Series(range(10000,11000,1))
svm_dist_df['tx_biobank_id'] = svm_dist_df['tx_biobank_id'].astype(str) 


#1. create column for International Prognostic Index values
#IPI range is 0-4
col_target = set_dist_target(tx_ORR30_df['clin_dz_IPI_score_apher'])
IPI_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['clin_dz_IPI_score_apher'] = IPI_randset
#round to nearest integer values
svm_dist_df['clin_dz_IPI_score_apher'] = svm_dist_df['clin_dz_IPI_score_apher'].astype(int)


#2. create column for age groups
#0 = 18-64, 1 = 65+
col_target = set_dist_target(tx_ORR30_df['dems_pt_age'])
#use n = 1000 and col_randset vars to create subsequent arrays using new targets
age_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['dems_pt_age'] = age_randset
#convert to age group 0/1 values
svm_dist_df['dems_pt_age_grp'] = svm_dist_df['dems_pt_age'].apply(lambda x: 0 if x <= 64 else 1)


#3. create column for disease stage at apheresis
#Range: 0-4
col_target = set_dist_target(tx_ORR30_df['clin_dz_stage_apher'])
dzstage_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['clin_dz_stage_apher'] = dzstage_randset
svm_dist_df['clin_dz_stage_apher'] = svm_dist_df['clin_dz_stage_apher'].astype(int)


#4. create column for disease type
#DLBCL = 0, tFL = 1, HGBL = 2
col_target = (tx_ORR30_df['clin_dz_type']).map({'DLBCL': 0,
                                                  'tFL': 1,
                                                  'HGBL': 2})
col_target = set_dist_target(col_target)

dztype_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['clin_dz_type'] = dztype_randset
svm_dist_df['clin_dz_type'] = svm_dist_df['clin_dz_type'].astype(int)


#5. create column for baseline inflammation status
#Baseline CRP > 100: 1, CRP <= 100: 0
col_target = set_dist_target(tx_ORR30_df['lab_cmp_CRP'])
crp_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['lab_cmp_CRP'] = crp_randset
svm_dist_df['base_CRP_inflam'] = svm_dist_df['lab_cmp_CRP'].apply(lambda x: 0 if x <= 100 else 1)



#6. create column for previous lines of chemotherapy
#Count range 0-8
col_target = set_dist_target(tx_ORR30_df['clin_dz_prior_ther_ct'])
chemo_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['clin_dz_prior_ther_ct'] = chemo_randset
svm_dist_df['clin_dz_prior_ther_ct'] = svm_dist_df['clin_dz_prior_ther_ct'].astype(int)

#Categorize into prior therapy groups
#0 = 0-2 lines therapy, 1 = 3+ lines therapy




#7. create column for incidence of SAE CRS
#1 = Yes, 0 = No
col_target = set_dist_target(tx_ORR30_df['SAE_CRS_G3_grp'])
CRS_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['SAE_CRS_G3_grp'] = CRS_randset
svm_dist_df['SAE_CRS_G3_grp'] = svm_dist_df['SAE_CRS_G3_grp'].apply(lambda x: 0 if x < 0.5 else 1)


#8. create column for incidence of SAE ICANS
#1 = Yes, 0 = No
col_target = set_dist_target(tx_ORR30_df['SAE_ICANS_G3_grp'])
ICANS_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['SAE_ICANS_G3_grp'] = ICANS_randset
svm_dist_df['SAE_ICANS_G3_grp'] = svm_dist_df['SAE_ICANS_G3_grp'].apply(lambda x: 0 if x < 0.5 else 1)

#9. create column for primary disease molecular subtype
#1 = GBC, 0 = ABC/non-GBC
#col_target = (tx_ORR30_df['clin_dz_cell_orig_Hans']).map({'GBC': 0,
#                                                            'ABC/Non-GCB': 1}) #database typo - should be Non-GBC
#col_target = col_target.dropna()
#subtype_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
#svm_dist_df['clin_dz_cell_orig_Hans'] = subtype_randset
#svm_dist_df['clin_dz_cell_orig_Hans'] = svm_dist_df['clin_dz_cell_orig_Hans'].apply(lambda x: 0 if x < 0.5 else 1)


#10. create column for prior autologous HSCT
#1 = Yes, 0 = No

col_target = (tx_ORR30_df['clin_dz_prior_auto_HSCT']).map({'No': 0,
                                                             'Yes': 1})
col_target = set_dist_target(col_target)
autoHSCT_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['clin_dz_prior_auto_HSCT'] = autoHSCT_randset
svm_dist_df['clin_dz_prior_auto_HSCT'] = svm_dist_df['clin_dz_prior_auto_HSCT'].apply(lambda x: 0 if x < 0.5 else 1)

#11. create column for prior allo HSCT
#1 = Yes, 0 = No
col_target = (tx_ORR30_df['clin_dz_prior_allo_HSCT']).map({'No': 0,
                                                             'Yes': 1})
col_target = set_dist_target(col_target)
alloHSCT_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['clin_dz_prior_allo_HSCT'] = alloHSCT_randset
svm_dist_df['clin_dz_prior_allo_HSCT'] = svm_dist_df['clin_dz_prior_allo_HSCT'].apply(lambda x: 0 if x < 0.5 else 1)

#12. create column for baseline disease status 
#0 = relapsed, 1 = primary refractory, 2 = refractory
col_target = (tx_ORR30_df['clin_dz_status_tx']).map({'relapsed': 0,
                                                         'primary refractory': 1,
                                                         'refractory:': 2})
col_target = set_dist_target(col_target)
dzstat_randset = norm_dist_set(col_target[0], col_target[1], col_target[2], col_target[3], n)
svm_dist_df['clin_dz_status_tx'] = dzstat_randset
svm_dist_df['clin_dz_status_tx'] = svm_dist_df['clin_dz_status_tx'].astype(int)

svm_dist_df = svm_dist_df.set_index(['tx_biobank_id'])

#omit columns not used
svm_dist_df = svm_dist_df.drop(['dems_pt_age',
                                'lab_cmp_CRP'],
                                axis = 1)
svm_dist_df.tail()


# In[ ]:


#Support Vector Machine - Classification model of responders and non-responders

#create an optimal hyperplane for linearly separable patterns
#extend to non-linear patterns separable by transformations of data using kernel function
#the 'support vectors' are the data points that lie closest to the decision surface

#SVM tries to maximize the margin around the separating hyperplane
#decision function is specified by a subset of training samples (the support vectors)

#similar to neural net - input sample features x1, x2... and output result y
#output gives a set of weights w1, w2... for each feature whose linear combination predicts
#value of y

#DIFFERENCE - optimization of maximizing the margin to reduce the number of weights that
#are nonzero to just a few that correspond to the features important for deciding the 
#hyperplane separation line. These remaining nonzero weights correspond to the support vectors
#that 'support' the separating hyperplane

#kernel functions - efficient separation of non-linear regions with new kinds of similarity
#measures based on dot products
#quadratic optimization to avoid 'local minimum' issues as with neural nets

#Best accuracy = 'RBF' or radial-basis function Gaussian kernel
#Select K = 5 best features, use K-fold cross validation to try to improve accuracy


# In[ ]:


#Using Gaussian radial basis function (RBF):
#1. set y-var of overall response binary 
y = svm_dist_df['overall_resp_bin']

#set x-vars to all other selected columns
x = svm_dist_df.drop('overall_resp_bin', axis = 1)

#2. create train-test split in sklearn model selection with 80:20 train:test split
from sklearn.model_selection import train_test_split  

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.20)  

#3. train algorithm on training data that's passed as a parameter to fit method. 
#use SVC for classification task (taking linearly separable data as linear kernel)
from sklearn.svm import SVC  

tx_svclassifier = SVC(kernel='rbf')  
tx_svclassifier.fit(x_train, y_train)  

#4. Use predict method of SVC class created 
tx_OR_pred = tx_svclassifier.predict(x_test)  

from sklearn.metrics import classification_report, confusion_matrix  

#5. Use #K-fold = 5 cross-validation for mean accuracy
from sklearn.model_selection import cross_val_score
scores = cross_val_score(tx_svclassifier, x, y, cv = 5)
kfold_acc = scores.mean()
kfold_CI = (scores.std() * 2)
print('K-fold Cross-Validation Accuracy: ', kfold_acc, ' +/- ', kfold_CI, sep = '')

print('Precision (PPV) = TP / (TP + FP)')
print('Recall (Sensitivity) = TP / (TP + FN) \n')

print(classification_report(y_test, tx_OR_pred)) 


# In[ ]:


#Select best subset of 5 features using chi-square categorical model
#Chi-square statistical test of independence between target variable (overall response)
#and feature variables for categorical data. 
from sklearn.feature_selection import SelectKBest, chi2


kfeat_select = SelectKBest(chi2, k = 5)
#set y-var to overall response
yft = svm_dist_df['overall_resp_bin']
#omit y-var and post-infusion SAE columns
xft = svm_dist_df.drop(['overall_resp_bin',
                     'SAE_CRS_G3_grp',
                     'SAE_ICANS_G3_grp'],
                     axis = 1)


kfeat_select.fit(xft, yft)

vector_names = list(xft.columns[kfeat_select.get_support(indices = True)])
def kfeat_vectors(vectors):
    feat_list = []
    for row in vectors:
        feat_list.append(row)
    return feat_list
#print(vector_names)
print('OR Best Features by Chi-Sq (K = 5):')
feat_list = kfeat_vectors(vector_names)
feat_list


# In[ ]:


#Run Gaussian radial basis function (RBF) using K = 5 best features selected:
#1. set y-var of overall response binary 
y = svm_dist_df['overall_resp_bin']

#set x-vars to all other selected columns
x = svm_dist_df.filter(['dems_pt_age_grp',
                        'clin_dz_stage_apher',
                        'clin_dz_type',
                        'clin_dz_prior_ther_ct',
                        'clin_dz_status_tx'], 
                        axis = 1)

#2. create train-test split in sklearn model selection with 80:20 train:test split
from sklearn.model_selection import train_test_split  

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.20)  

#3. train algorithm on training data that's passed as a parameter to fit method. 
#use SVC for classification task (taking linearly separable data as linear kernel)
from sklearn.svm import SVC  

tx_svclassifier = SVC(kernel='rbf')  
tx_svc_fit = tx_svclassifier.fit(x_train, y_train)  

#4. Use predict method of SVC class created 
tx_OR_pred = tx_svclassifier.predict(x_test)  

from sklearn.metrics import classification_report, confusion_matrix  

#5. Use #K-fold = 5 cross-validation for mean accuracy
from sklearn.model_selection import cross_val_score
scores = cross_val_score(tx_svc_fit, x, y, cv = 10)
kfold_acc = scores.mean()
kfold_CI = (scores.std() * 2).astype(float)

print('POC Support Vector Machine Classification Model:')
print('>Commercial Treatment Overall Response')
print('\nParameters:')
print('Radial Basis Function (RBF) Gaussian Kernel')
print('K-fold Cross-Validation Accuracy: {:.3f} +/- {:.4f}'.format(kfold_acc, kfold_CI), sep = '')

print('\nPrecision (PPV) = TP / (TP + FP)')
print('Recall (Sensitivity) = TP / (TP + FN) \n')
#F1 score is harmonic mean of precision and recall
print(classification_report(y_test, tx_OR_pred)) 


# In[ ]:


#Using real data and bootstrapping

#Run Gaussian radial basis function (RBF) using K = 5 best features selected:
#1. set y-var of overall response binary 
y = tx_ORR30_df['overall_resp_bin']

#set x-vars to all other selected columns
x = tx_ORR30_df.filter(['dems_pt_age_grp',
                        'clin_dz_stage_apher',
                        'clin_dz_type',
                        'clin_dz_prior_ther_ct',
                        'clin_dz_status_tx'], 
                        axis = 1)

#format x-vars
x['clin_dz_status_tx'] = x['clin_dz_status_tx'].map({'relapsed': 0,
                                                         'primary refractory': 1,
                                                         'refractory:': 2})


#2. create train-test split in sklearn model selection with 80:20 train:test split
from sklearn.model_selection import train_test_split  

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.20)  

#3. train algorithm on training data that's passed as a parameter to fit method. 
#use SVC for classification task (taking linearly separable data as linear kernel)
from sklearn.svm import SVC  

tx_svclassifier = SVC(kernel='rbf')  
tx_svc_fit = tx_svclassifier.fit(x_train, y_train)  

#4. Use predict method of SVC class created 
tx_OR_pred = tx_svclassifier.predict(x_test)  

from sklearn.metrics import classification_report, confusion_matrix  

#5. Use #K-fold = 5 cross-validation for mean accuracy
from sklearn.model_selection import cross_val_score
scores = cross_val_score(tx_svc_fit, x, y, cv = 10)
kfold_acc = scores.mean()
kfold_CI = (scores.std() * 2).astype(float)

print('POC Support Vector Machine Classification Model:')
print('>Commercial Treatment Overall Response')
print('\nParameters:')
print('Radial Basis Function (RBF) Gaussian Kernel')
print('K-fold Cross-Validation Accuracy: {:.3f} +/- {:.4f}'.format(kfold_acc, kfold_CI), sep = '')

print('\nPrecision (PPV) = TP / (TP + FP)')
print('Recall (Sensitivity) = TP / (TP + FN) \n')
#F1 score is harmonic mean of precision and recall
print(classification_report(y_test, tx_OR_pred)) 


# In[ ]:




