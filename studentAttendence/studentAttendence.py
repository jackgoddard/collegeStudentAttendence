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

def keepW(val):
    rval = val
    if val != 'W':
        rval = 0
    return rval

def keepA(val):
    rval = val
    if val != 'A':
        rval = 0 #np.nan
    return rval

def keepD(val):
    rval = val
    if val != 'D':
        rval = 0 #np.nan
    return rval

def rmValues( df, code ):
    if code == 'A':
        df['stage_code'].apply(keepA)
    if code == 'W':
        df['stage_code'].apply(keepW)
    if code == 'D':
        df['stage_code'].apply(keepD)
    return df
              
def createTruthVector():

    ##### read in student status info #####
    enrolment_cols = [ 'stuID', 'student_id',  'acad_period', 'stage_code', 'dt_achieved', 'grup', 'week_no', 'active_date', 'active_week' ]
    use_cols       = [ 'stuID', 'acad_period', 'stage_code',  'week_no',    'active_week' ]
     
    df_status = pd.read_csv('..\data\\1314\\student_enrolement_info.csv',  header = 0, index_col = 0 , names = enrolment_cols, usecols = use_cols, converters = {'stage_code':strip} )

    #### simplify the stage_code variables ####
    df_status.stage_code.replace( 'HEC', np.nan, inplace = True )  # Null values
    df_status.stage_code.replace( 'MEX', np.nan, inplace = True )
    df_status.stage_code.replace( 'DEF', np.nan, inplace = True )
    df_status.stage_code.replace( 'CTG', np.nan, inplace = True )
    df_status.stage_code.replace( 'C',   np.nan, inplace = True )
    df_status.stage_code.replace( 'N',   np.nan, inplace = True )
    df_status.stage_code.replace( 'P',   'A'   , inplace = True ) # Active
    df_status.stage_code.replace( 'SUS', 'W'   , inplace = True ) # Withdrawn

    #### set negative start weeks to be the start of the year (week 0) ####
    df_status['week_no_corr']     = df_status['week_no'].apply(negReplace) 
    df_status['active_week_corr'] = df_status['active_week'].apply(negReplace) 

    #### create pivot tables for active, withdrawn and completed students, and fill forward #### 
    df_active_summary = pd.pivot_table( df_status, index = df_status.index, columns='active_week_corr', values='stage_code', aggfunc='count' )
    df_active_summary.ffill(axis=1, inplace=True)
    
    df_withdrwn_summary = pd.pivot_table( rmValues(df_status.copy(), 'W'),  index=df_status.index, columns='week_no_corr', values='stage_code', aggfunc='count' )
    df_withdrwn_summary.ffill(axis=1, inplace=True)
    df_withdrwn_summary.replace(1, 2, inplace=True)

    df_completed_summary = pd.pivot_table( rmValues(df_status.copy(), 'D'), index=df_status.index, columns='week_no_corr', values='stage_code', aggfunc='count' )
    df_completed_summary.ffill(axis=1, inplace=True)
    df_completed_summary.replace(1, 6, inplace=True)

    
    #### combine the 3 pivot tables, translate numbers back into strings ####

    df = df_active_summary.fillna(0) + df_withdrwn_summary.fillna(0) # + df_completed_summary.fillna(0)

    #print('---')
    #print(df_active_summary.head(10))
    #print('---')
    #print(df_active_summary[df_active_summary.index=='BAC12414185062DPXXCEESE312AA1'])
    #print('---')
    #print('---')
    #print(df_withdrwn_summary.head(10))
    #print('---')
    #print(df_withdrwn_summary[df_withdrwn_summary.index=='BAC12414185062DPXXCEESE312AA1'])
    #print('---')
    #print(df_completed_summary.head(10))
    #print('---')
    #print(df_completed_summary[df_completed_summary.index=='BAC12414185062DPXXCEESE312AA1'])
    #print('---')

   # df = df_completed_summary.fillna(0)

   # df.replace( 1, 'A',     inplace = True )
  #  df.replace( 2, 'W',     inplace = True )
  #  df.replace( 3, 'W',     inplace = True )
   # df.replace( 6, 'D',     inplace = True )
  #  df.replace( 7, 'D',     inplace = True )
  #  df.replace( 8, 'D',     inplace = True )
  #  df.replace( 9, 'D',     inplace = True )
  #  df.replace( 0,  np.nan, inplace = True )
 
    print(df_status[df_status.index=='BAC12414185062DPXXCEESE312AA1'])
    print(df[df.index=='BAC12414185062DPXXCEESE312AA1'].values)
    print('---')
    print(df_status[df_status.index=='BEL14428815065CPBED3WHSC141F03'])
    print(df[df.index=='BEL14428815065CPBED3WHSC141F03'].values)
    print('---')

    print(df.head(15))

    ########################################################
    ### Want to answer 3 questions:                      ###
    ###   (1) Does this student drop out?                ###
    ###   (2) Does this student drop out in two weeks?   ###
    ###   (3) Does this student drop out next week?      ###
    ########################################################

    ### (1): list of students who drop out ###

    #   all_students     = pd.DataFrame(0, index=df.index,                                      columns=['drop'])
    #   dropped_students = pd.DataFrame(1, index=df_status[df_status.stage_code == 'W' ].index, columns=['drop'])

    #  print(df.isin(['D']))


   # print( df_status[df_status.stage_code == 'W' ].index in df_status.index)

   # print(dropped_students.index in all_students.index)
    
  #  print(dropped_students)


    ### (2): list of (weekly) series indicating if a student drops out in 2 weeks ###
   
    # weekly_status = []

    #for i in range(0,53):
    #   weekly_status.append(df[i])





    






def createDesignMatrices():
           
    ##### Read in info for contact time #####
    df_contact_1314 = pd.read_csv('..\data\\1314\\contact_time_1314.csv', names=['student_id', 'day', 'time' ], header=0 )
       
    df_contact = ft.contact_summary( df_contact_1314 )
 
    df_contact.fillna(0, inplace=True)    

    static_features_series = [ df_contact['total'], df_contact['active_days']/df_contact['total'] ]
    static_features_names  = [ 'contact_time',        'contact_density'  ] 
    
    static_features = ft.concatStaticFeatures( static_features_series, static_features_names )

    ##### Read info for weekly attendence #####
    df_att_weekly = pd.read_csv('..\data\\1314\\student_weekly_attendence_1314.csv', names=['student_id', 'weekno', 'mark', 'mark_count', 'mins_late', 'contact_mins' ], header=0, dtype={'mark':str}  )
    
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
 

    return matrices





#################################################
###                  MAIN                     ###
#################################################

def main():

    ##### Create Truth Vectors #####
    y = createTruthVector()

 
       ##### create a matrix of features vs student_id of each week #####
     
    #  X = createDesignMatrices()
    
    #print(X[25])
    


main()