import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(page_title="Hospital Dashboard",layout="wide")
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("❌ please login first")
    if st.button("switch to login"):
        st.switch_page("app.py")
    st.stop()


col1,col2=st.columns([4,1])
with col2 :
    if st.button("Logout"):
        st.session_state.authenticated=False
        st.switch_page("app.py")
        
st.markdown(
        "<h2 style='text-align: center;'>🏥 Hospital data analysis Dahboard 📊</h2>",
        unsafe_allow_html=True
)

#loading the datasets
patients=pd.read_csv(r"data/patients.csv")
claims_and_billing=pd.read_csv(r"data/claims_and_billing.csv")
encounters=pd.read_csv(r"data/encounters.csv")
diagnoses=pd.read_csv(r"data/diagnoses.csv")
procedures=pd.read_csv(r"data/procedures.csv")
providers=pd.read_csv(r"data/providers.csv")
#created these 360 tables in another file (tables_360_views.py and loaded them directly to reduce the time for loading website)
patients_360=pd.read_csv(r"data/patients_360.csv")
encounters_360=pd.read_csv(r"data/encounter_360.csv")
providers_360=pd.read_csv(r"data/provider_360.csv")


#choosing the dashboard
option=st.sidebar.selectbox("choose the dashboard",['patients overview','encounters overview','providers overview'])

#patients overview
if option =='patients overview':
   st.sidebar.header("choose filters")
   fil_pat_360=patients_360.copy()
   Registered_month=st.sidebar.multiselect("Registerd_month",fil_pat_360['registered_month'].unique())
   if Registered_month:
      fil_pat_360=fil_pat_360[fil_pat_360['registered_month'].isin(Registered_month)]

   Gender=st.sidebar.multiselect("Gender",fil_pat_360['gender'].unique())
   if Gender:
      fil_pat_360=fil_pat_360[fil_pat_360['gender'].isin(Gender)]

   insurance_provider=st.sidebar.multiselect("insurance provider",fil_pat_360['insurance_provider'].unique())
   if insurance_provider:
      fil_pat_360=fil_pat_360[fil_pat_360['insurance_provider'].isin(insurance_provider)]

    #  metrics to patients overview
   total_patients=fil_pat_360['patient_id'].nunique()
   avg_billed_amount=fil_pat_360['billed_amount'].mean()
   avg_paid_amount=fil_pat_360['paid_amount'].mean()
   avg_num_visits=fil_pat_360['no_of_visits'].mean()


   #adding them to website
   
   col1,col2,col3,col4=st.columns(4)
   col1.metric("Total number of patients",total_patients)
   col2.metric("Average billed amount per patient",f"{avg_billed_amount:,.1f}")
   col3.metric("Average paid amount per patient",f"{avg_paid_amount:,.1f}")
   col4.metric("Average number of visits per patient",f"{avg_num_visits:,.0f}")
   tab1,tab2,tab3=st.tabs(['patients count 👩👨','Revenue_patient_level💸🤑','patients age level👶🧒🧓'])
   #creating graphs 
   patients_by_readmission=fil_pat_360.groupby(by='no_of_times_readmitted').agg(
                                patients_count=("patient_id","count")
   ).reset_index()

   patients_marital_status=fil_pat_360.groupby(by="marital_status")['patient_id'].count()
   
   
   with tab1:
    col1,col2=st.columns(2)
    with col1:
     fig,ax=plt.subplots(figsize=(4,4))
     ax.bar(patients_by_readmission['no_of_times_readmitted'],patients_by_readmission['patients_count'])
     ax.set_xlabel("Number of times readmitted")
     ax.set_ylabel("patients count")
     ax.set_title("patients by readmission count")
     st.pyplot(fig)

    with col2:
     fig,ax=plt.subplots(figsize=(5,5))
     ax.pie(patients_marital_status,labels=patients_marital_status.index,autopct="%1.0f%%")
     ax.set_title("Number of patients by marital status")
     st.pyplot(fig)
    
   with tab2 :
    col1,col2=st.columns(2)
    top_by_revenue=fil_pat_360.sort_values(by='paid_amount',ascending=False).head()
    rev_by_ethnicity=fil_pat_360.groupby(by='ethnicity')['paid_amount'].sum().reset_index()
    with col1:
        fig,ax=plt.subplots(figsize=(4,4))
        ax.barh(top_by_revenue['patient_id'],top_by_revenue['paid_amount'])
        ax.set_xlabel("paid amount")
        ax.set_ylabel("patient id")
        ax.set_title("Top 5 patient who paid highest amount")
        st.pyplot(fig)
    
    with col2:
        fig,ax=plt.subplots(figsize=(4,4))
        ax.bar(rev_by_ethnicity['ethnicity'],rev_by_ethnicity['paid_amount'])
        ax.set_xlabel("no. of visits")
        ax.set_ylabel("patient")
        st.pyplot(fig)

   with tab3:
    col1,col2=st.columns(2)
    by_age_bins=fil_pat_360.groupby(by="age_bins")['patient_id'].count()
    rev_by_agebins=fil_pat_360.groupby(by="age_bins")['paid_amount'].sum().reset_index()

    with col1:
        fig,ax=plt.subplots(figsize=(5,5))
        ax.pie(by_age_bins,labels=by_age_bins.index,autopct="%1.0f%%")
        ax.set_title("Count of patients by age bins")
        st.pyplot(fig)
    with col2:
        fig,ax=plt.subplots(figsize=(4,4))
        ax.bar(rev_by_agebins['age_bins'],rev_by_agebins['paid_amount'])
        ax.set_title("paid amount by age bins")
        ax.set_xlabel("age bins")
        ax.set_ylabel("paid_amount")
        st.pyplot(fig)


elif option=='encounters overview':
    st.sidebar.header("choose filters")
    fil_enc_360=encounters_360.copy()

    visit_month=st.sidebar.multiselect("visit month",fil_enc_360["visit_month"].unique())
    if visit_month:
        fil_enc_360=fil_enc_360[fil_enc_360['visit_month'].isin(visit_month)]

    discharge_month = st.sidebar.multiselect("discharge month",fil_enc_360['discharge_month'].unique())
    if discharge_month:
        fil_enc_360=fil_enc_360[fil_enc_360['discharge_month'].isin(discharge_month)]

    primary_flag = st.sidebar.multiselect("primary flag",fil_enc_360["primary_flag"].unique())
    if primary_flag:
        fil_enc_360=fil_enc_360[fil_enc_360['primary_flag'].isin(primary_flag)]
    
    chronic_flag=st.sidebar.multiselect("chronic flag",fil_enc_360['chronic_flag'].unique())
    if chronic_flag:
        fil_enc_360=fil_enc_360[fil_enc_360['chronic_flag'].isin(chronic_flag)]

    #calculate metrics
    Number_of_visits=fil_enc_360['encounter_id'].count()
    Average_billed_amount=fil_enc_360['billed_amount'].mean()
    Average_paid_amount=fil_enc_360['paid_amount'].mean()

    col1,col2,col3=st.columns(3)
    #creating metrics to website
    col1.metric("Number of visits",Number_of_visits)
    col2.metric("Average billed amount per visit",f"{Average_billed_amount:,.1f}")
    col3.metric("Average paid amount per visit",f"{Average_paid_amount:,.1f}")

    #creating tabs
    tab1,tab2,tab3=st.tabs(["encounter_visit","admission type and department","Billings and claims "])

    with tab1 :
        col1,col2=st.columns(2)
        enc_visit_type=fil_enc_360.groupby('visit_type')['encounter_id'].count().reset_index()
        enc_readmitted=fil_enc_360.groupby('readmitted_flag')['encounter_id'].count()
        with col1:
            fig,ax=plt.subplots(figsize=(4,4))
            ax.bar(enc_visit_type['visit_type'],enc_visit_type['encounter_id'])
            ax.set_title("Number of visits by visit type")
            ax.set_xlabel('visit type')
            ax.set_ylabel("Number of visits")
            st.pyplot(fig)
        with col2:
            fig,ax=plt.subplots(figsize=(4,4))
            ax.pie(enc_readmitted,labels=enc_readmitted.index,autopct="%1.0f%%")
            ax.set_title("number of visites by readmitted flag")
            st.pyplot(fig)
    

    with tab2:
        col1,col2=st.columns(2)
        with col1:
            admission_type=fil_enc_360.groupby(by="admission_type")['encounter_id'].count().reset_index()
            
            fig,ax=plt.subplots(figsize=(4,4))
            ax.bar(admission_type['admission_type'],admission_type['encounter_id'])
            ax.set_title("Number of visits by admission type")
            ax.set_xlabel("admission type")
            ax.set_ylabel("number of visits")
            st.pyplot(fig)
        with col2:
            department=fil_enc_360.groupby(by="department")['encounter_id'].count().reset_index()

            fig,ax=plt.subplots(figsize=(6,8))
            ax.barh(department['department'],department['encounter_id'])
            ax.set_title("Number of visits by department")
            ax.set_xlabel("department")
            ax.set_ylabel("visits")
            st.pyplot(fig)

    with tab3:
        col1,col2=st.columns(2)
        payment_method=fil_enc_360.groupby(by='payment_method')['encounter_id'].count()
        payment_method_amount=fil_enc_360.groupby(by='payment_method')['paid_amount'].sum()

        claim_status=fil_enc_360.groupby(by='claim_status')['encounter_id'].count()

        with col1:
            fig,ax=plt.subplots(figsize=(4,4))
            ax.pie(payment_method_amount,labels=payment_method_amount.index,autopct="%1.0f%%")
            ax.set_title("Paid amount by payment method")
            st.pyplot(fig)
        with col2:
            fig,ax=plt.subplots(figsize=(3,3))
            ax.pie(claim_status,labels=claim_status.index,autopct="%1.0f%%")
            ax.set_title("encounters by claim status")
            st.pyplot(fig)
        
        denial_reason=fil_enc_360.groupby(by='denial_reason')['encounter_id'].count().reset_index()
        
        fig,ax=plt.subplots(figsize=(25,6))
        ax.barh(denial_reason['denial_reason'],denial_reason['encounter_id'])
        ax.set_title("Count of encounters by denial reason")
        ax.set_xlabel("count of encounter ids")
        ax.set_ylabel("denial reason")
        st.pyplot(fig)
    


#providers dashboard

else :
    st.sidebar.header("choose filter")
    fil_pro_360=providers_360.copy()

    location=st.sidebar.multiselect("location",fil_pro_360['location'].unique())
    if location : 
        fil_pro_360=fil_pro_360[fil_pro_360['location'].isin(location)]

    inhouse=st.sidebar.multiselect("Inhouse",fil_pro_360['inhouse'].unique())
    if inhouse : 
        fil_pro_360=fil_pro_360[fil_pro_360['inhouse'].isin(inhouse)]

    experience_type=st.sidebar.multiselect("experience type",fil_pro_360['experience_type'].unique())
    if experience_type:
        fil_pro_360=fil_pro_360[fil_pro_360['experience_type'].isin(experience_type)]

    tab1,tab2,tab3=st.tabs(['providers information','department and speciality','Available visit type'])
    with tab1:
        col1,col2=st.columns(2)
        with col1:
            top_providers=fil_pro_360.sort_values(by="no_of_patients_treated",ascending=False).head(10)
            fig,ax=plt.subplots(figsize=(4,4))
            ax.barh(top_providers["name"],top_providers['no_of_patients_treated'])
            ax.set_title("top 10 providers treated more patients")
            ax.set_xlabel("providers name")
            ax.set_ylabel("count of patients")
            st.pyplot(fig)

        with col2:
            top_paid_amount=fil_pro_360.sort_values(by="paid_amount",ascending=False).head(10)
            fig,ax=plt.subplots(figsize=(4,4))
            ax.barh(top_paid_amount['name'],top_paid_amount['paid_amount'])
            ax.set_title("Top 10 providers by revenue generated")
            ax.set_xlabel("revenue generated")
            ax.set_ylabel("provider name")
            st.pyplot(fig)

    with tab2:
        col1,col2=st.columns(2)
        with col1:
            department=fil_pro_360.groupby(by='department')['provider_id'].count().reset_index()

            fig,ax=plt.subplots(figsize=(4,4))
            ax.barh(department['department'],department['provider_id'])
            ax.set_title("Number of providers by department")
            ax.set_xlabel("department")
            ax.set_ylabel("count of providers")
            st.pyplot(fig)

        with col2:
           specialty=fil_pro_360.groupby(by='specialty')['provider_id'].count().reset_index()
           fig,ax=plt.subplots(figsize=(4,4))
           ax.barh(specialty['specialty'],specialty['provider_id'])
           ax.set_title("Number of providers by speciality")
           ax.set_xlabel("specialty")
           ax.set_ylabel("Number of providers")
           st.pyplot(fig)
    with tab3:
        col1,col2=st.columns(2)
        with col1:
            available_visit_type=fil_pro_360.groupby(by="frequent_visit_type")['provider_id'].count()
            patients_by_visit_type=fil_pro_360.groupby(by="frequent_visit_type")['no_of_patients_treated'].sum()


            fig,ax=plt.subplots(figsize=(4,4))
            ax.pie(available_visit_type,labels=available_visit_type.index,autopct="%1.0f%%")
            ax.set_title("Providers by visit type")
            st.pyplot(fig)
            
        with col2:
            fig,ax=plt.subplots(figsize=(4,4))
            ax.pie(patients_by_visit_type,labels=patients_by_visit_type.index,autopct="%1.0f%%")
            ax.set_title("patinets by visit type")
            st.pyplot(fig)