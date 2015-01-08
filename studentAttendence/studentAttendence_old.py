##########################################################################
###                                                                    ###
###  Student Attendence                                                ###
###                                                                    ###
###     Study to predict students at risk of dropping out              ###
###                                                                    ###
###     Author:  Jack Goddard                                          ###
###     Created: December 2014                                         ###
###                                                                    ###
##########################################################################

import os
import numpy as np
import pandas as pd
from AttendenceTables import Attendence as att 
import createFeatures.featureTools as ft
import featurePlotting as fp

def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text

def negReplace(val):
    rval = val
    if (val < 0.0) or (val > 52):
        rval = 0 
    return rval

          

def createTruthTable(df_in):

    df = pd.DataFrame('', index=df_in.index, columns=range(0,53))

    for idx, row in df_in.iterrows():
        if np.isfinite(row['active_week_corr']):
            df[int(row['active_week_corr'])].ix[idx] = 'A'
        if np.isfinite(row['withdraw_week']):
            df[int(row['withdraw_week'])].ix[idx] = 'W'
        if np.isfinite(row['complete_week']):
            df[int(row['complete_week'])].ix[idx] = 'D'

    ### fill forward for active weeks ###
    for idx, row in df.iterrows():
        for week in range(0,len(row)):
            print(row[week])
            if not row[week] and (week != 0):
                if row[week-1] == 'A':
                    row[week] = 'A'
                
    return df


   
def getTruthTable(recreate=False, path='..\\data\\1314\\truthTable.csv'):


    if not recreate:

        df = pd.read_csv(path, header=0, index_col=0)

    else:
        
        ##### read in student status info #####
        enrolment_cols = [ 'stuID', 'student_id',  'acad_period', 'stage_code', 'dt_achieved', 'grup', 'week_no', 'active_date', 'active_week' ]
        use_cols       = [ 'stuID', 'acad_period', 'stage_code',  'week_no',    'active_week' ]
     
        df_status = pd.read_csv('..\data\\1314\\student_enrolement_info.csv',  header = 0, index_col = 0 , names = enrolment_cols, usecols = use_cols, converters = {'stage_code':strip} )

        ### only use first 500 entries for testing ###
        #df_status = df_status.head(5000)

        #### simplify the stage_code variables ####
        df_status.stage_code.replace( 'HEC', np.nan, inplace = True )  # Null values
        df_status.stage_code.replace( 'MEX', np.nan, inplace = True )
        df_status.stage_code.replace( 'DEF', np.nan, inplace = True )
        df_status.stage_code.replace( 'CTG', np.nan, inplace = True )
        df_status.stage_code.replace( 'C',   np.nan, inplace = True )
        df_status.stage_code.replace( 'N',   np.nan, inplace = True )
        df_status.stage_code.replace( 'P',   'A'   , inplace = True ) # Active
        df_status.stage_code.replace( 'SUS', 'W'   , inplace = True ) # Withdrawn

        #### set negative start weeks and start weeks beyond the end of the year to be the start of the year (week 0) ####
        df_status['week_no_corr']     = df_status['week_no'].apply(negReplace) 
        df_status['active_week_corr'] = df_status['active_week'].apply(negReplace) 

        #### add columns for the week students withdraw or complete ####
        df_status['withdraw_week'] = df_status[df_status.stage_code == 'W'].week_no_corr
        df_status['complete_week'] = df_status[df_status.stage_code == 'D'].week_no_corr
        

        ##df_status['withdraw_week'].fillna(-1, inplace=True)
        print(df_status.head(20))

        #### remove students if we don't know when they start ####
        df_status = df_status[df_status['active_week_corr'].notnull()]

        #### create table with student status for each week ####
        df = createTruthTable(df_status[['active_week_corr', 'withdraw_week', 'complete_week']])
    
        #### write table to csv to save time later ####
        df.to_csv(path)
    
        #### examine development progress ####
        print('--- completing student ---')
        print(df_status[df_status.index=='BAC12414185062DPXXCEESE312AA1'])
        print(df[df.index=='BAC12414185062DPXXCEESE312AA1'].values)
        print('---')
        print('--- withdrawing student ---')
        print(df_status[df_status.index=='BEL14428815065CPBED3WHSC141F03'])
        print(df[df.index=='BEL14428815065CPBED3WHSC141F03'].values)
        print('---')

        #print(df.head(15))

    
    return df





def createDesignMatrices():
           
    ##### Read in info for contact time #####
    df_contact_1314_1 = pd.read_csv('..\data\\1314\\contact_time_1314_1.csv', names=['student_id', 'day', 'time' ], header=0 )
    df_contact_1314_2 = pd.read_csv('..\data\\1314\\contact_time_1314_2.csv', names=['student_id', 'day', 'time' ], header=0 )
    df_contact_1314 = df_contact_1314_1.append(df_contact_1314_2)
    df_contact = ft.contact_summary( df_contact_1314 )
 
    df_contact.fillna(0, inplace=True)    

    static_features_series = [ df_contact['total'], df_contact['active_days']/df_contact['total'] ]
    static_features_names  = [ 'contact_time',        'contact_density'  ] 
    
    static_features = ft.concatStaticFeatures( static_features_series, static_features_names )

    ##### Read info for weekly attendence #####
    df_att_weekly_1 = pd.read_csv('..\data\\1314\\student_weekly_attendence_1314_1.csv', names=['student_id', 'weekno', 'mark', 'mark_count', 'mins_late', 'contact_mins' ], header=0, dtype={'mark':str}  )
    df_att_weekly_2 = pd.read_csv('..\data\\1314\\student_weekly_attendence_1314_2.csv', names=['student_id', 'weekno', 'mark', 'mark_count', 'mins_late', 'contact_mins' ], header=0, dtype={'mark':str}  )
    
    df_att_weekly = df_att_weekly_1.append(df_att_weekly_2)
    df_att_weekly.drop_duplicates(inplace=True)
        
    weekly_att = att(df_att_weekly)

    time_features = []
    time_features.append(ft.weekNumberFeature( weekly_att.presentTable() ) )
    time_features.append(weekly_att.fracPresentTable())                       ## Fractional lesson attendence
    time_features.append(weekly_att.fracLateTable())                          ## Fractional late lesssons
    time_features.append(weekly_att.weeklyChangeFracPresentTable())           ## Change in fractional attendence from last week
    time_features.append(weekly_att.avFracPresentTable())                     ## Average fractional attendence to date
    time_features.append(weekly_att.fracLateByMeanTable())                    ## This weeks lates / Average lates lessons to date
    time_features.append(weekly_att.fracPresentByMeanTable())                 ## This weeks attendence / Average attendence lessons to date
    time_features.append(weekly_att.fracMinsLateTable())                      ## Fraction of time missed in the late lessons 
    time_features.append(weekly_att.contactMinsTable()/60.0 )                 ## Contact time that week
    time_features.append(weekly_att.contactMinsPassedTable()/60.0)            ## Cumlative contact time up until this week
    time_features.append(weekly_att.fracContactTimePassedTable())             ## Fraction of total contact time that has been completed
 #   time_features.append(weekly_att.weeklyChangeFracLateTable())
  
   # print(weekly_att.presentTable())
 ### DEFINE attendence = lessons_present / lessons_required

    time_feature_names = []
    time_feature_names.append('week_no')
    time_feature_names.append('frac_present')
    time_feature_names.append('frac_late')
    time_feature_names.append('presence_change')
    time_feature_names.append('mean_attendence')
    time_feature_names.append('frac_late_by_frac_mean')
    time_feature_names.append('frac_pres_by_frac_mean')
    time_feature_names.append('frac_mins_late')
    time_feature_names.append('weekly_contact_time')
    time_feature_names.append('contact_time_to_date')
    time_feature_names.append('frac_contact_time_to_date')
    #  time_feature_names.append('late_change')

    ##### Create the design matrices #####
    matrices = ft.createFeatureMatrix( time_features, time_feature_names, static_features )
 

    return matrices, weekly_att, static_features





#################################################
###                  MAIN                     ###
#################################################

def main():

    ##### Create Truth Vectors #####
    df_y = getTruthTable(recreate=False)

    # print(df_y)

    ########################################################
    ### Want to answer 3 questions:                      ###
    ###   (1) Does this student drop out?                ###
    ###   (2) Does this student drop out in two weeks?   ###
    ###   (3) Does this student drop out next week?      ###
    ########################################################

    ### (1): list of students who drop out ###
     
    #   all_students     = pd.DataFrame(0, index=df.index,            columns=['drop'])
    withdrawn_students = df_y.isin(['W']).any(axis=1)

    # print(withdrawn_students)

    ### (2): list of (weekly) series indicating if a student drops out in 2 weeks ###
   
    # weekly_status = []

    #for i in range(0,53):
    #   weekly_status.append(df[i])





    ##### create a matrix of features vs student_id of each week #####
     
    X, time_features, static_features = createDesignMatrices()
    
    #print(X[25])


    fp.plotFeatures(time_features,df_y,withdrawn_students,limit=500)#    X.contact_time.plot()
    
    print(time_features.fracPresentTable().head(10))
    


main()