import pandas as pd 
import numpy as np

patients=pd.read_csv(r"C:\krishnasri\deliverables_project_2_krishnasri\RCM_CA_Hospital/patients.csv")
claims_and_billing=pd.read_csv(r"C:\krishnasri\deliverables_project_2_krishnasri\RCM_CA_Hospital/claims_and_billing.csv")
encounters=pd.read_csv(r"C:\krishnasri\deliverables_project_2_krishnasri\RCM_CA_Hospital/encounters.csv")
diagnoses=pd.read_csv(r"C:\krishnasri\deliverables_project_2_krishnasri\RCM_CA_Hospital/diagnoses.csv")
procedures=pd.read_csv(r"C:\krishnasri\deliverables_project_2_krishnasri\RCM_CA_Hospital/procedures.csv")
providers=pd.read_csv(r"C:\krishnasri\deliverables_project_2_krishnasri\RCM_CA_Hospital/providers.csv")
#updating null values for few columns based on business understanding

patients['address']=patients['address'].fillna(value="not given")
patients['state']=patients['state'].fillna(value='others')
patients['zip']=patients['zip'].fillna(0)
claims_and_billing['claim_id']=claims_and_billing['claim_id'].fillna('No claim')
claims_and_billing['denial_reason']=claims_and_billing['denial_reason'].fillna('Nothing')


encounters["readmitted_flag"]=encounters["readmitted_flag"].apply(lambda x : 1 if x == 'Yes' else 0)
patients['registration_date']=pd.to_datetime(patients['registration_date'],dayfirst=True)
procedures['procedure_date']=pd.to_datetime(procedures['procedure_date'],dayfirst=True)
encounters['visit_date']=pd.to_datetime(encounters['visit_date'],dayfirst=True)
encounters['discharge_date']=pd.to_datetime(encounters['discharge_date'],dayfirst=True)
patients['age_bins']=patients['age'].apply(lambda x:'0-10' if x >0 and x <11 else "11-20" if x > 10 and x < 21 else '21-40' if x >20 and x < 41 else '41-60' if x > 40 and x < 61 else '60+').astype(str)
providers['experience_type']=providers['years_experience'].apply(lambda x : 'experienced professional' if x > 25 else 'experienced' if x > 10 else 'less experienced' if x > 2 else 'no experience' )

#patients 360 view table

patients_360=patients.merge(encounters.groupby(by='patient_id').agg(
    no_of_visits=('encounter_id','size'),
    most_frequent_visit=('visit_type',lambda x : x.mode()[0]),
    frequent_admission_type=('admission_type',lambda x : x.mode().iloc[0] if len(x.mode()) > 0 else None),
    no_of_times_readmitted=('readmitted_flag','sum')
    ).reset_index(),on='patient_id',how='left').merge(
    claims_and_billing.groupby(by='patient_id').agg(
    insurance_provider=("insurance_provider",lambda x : x.mode()),
    billed_amount=("billed_amount",'sum'),
    paid_amount=("paid_amount",'sum')
    ).reset_index(),on='patient_id',how='left')

patients_360["registered_month"]=patients_360['registration_date'].dt.month_name()

#encounters 360 view table 
encounters_360=encounters.merge(claims_and_billing,on='encounter_id',how='left').merge(
                 procedures.groupby(by='encounter_id').agg(
                 tot_procedure_cost=("procedure_cost","sum")
).reset_index(),on='encounter_id',how='left').merge(
    diagnoses,on='encounter_id',how='left')

encounters_360["visit_month"]=encounters_360['visit_date'].dt.month_name()
encounters_360['discharge_month']=encounters_360['discharge_date'].dt.month_name()

#providers 360 view
providers_360=providers.merge(encounters.groupby(by='provider_id').agg(
    no_of_patients_treated=('encounter_id','count'),
    frequent_visit_type=('visit_type',lambda x : x.mode()[0]),
).reset_index(),on='provider_id',how='left')

patients_360.to_csv(r"C:\krishnasri\project_2_ppt/patients_360.csv")
encounters_360.to_csv(r"C:\krishnasri\project_2_ppt/encounter_360.csv")
providers_360.to_csv(r"C:\krishnasri\project_2_ppt/provider_360.csv")

print(encounters['readmitted_flag'].value_counts())