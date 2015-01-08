import numpy as np
import pandas as pd


def test():

    print('This is a test....')



def attendence_summary( df, inc_withdrawn = bool(1) ):

    df_summary = df.pivot(index='student_id', columns='mark', values='count')  
    
    ### Students were present (inc. late)
    df_summary['P ']  = df_summary[['  ', '/ ', 'L ']].sum(axis=1)

    ### Students were absent
    df_summary['Ab '] = df_summary[['A ', 'C ']].sum(axis=1)

    ### Student's were required in class (class not cancelled)
    df_summary['R ']  = df_summary[['P ', 'Ab ']].sum(axis=1)

    return df_summary


def contact_summary( df ):

    df_summary = pd.pivot_table(df, index='student_id', columns='day', values='time', aggfunc= np.sum )

    days = list(df_summary.copy())
    df_summary['active_days'] = df_summary[days].notnull().sum(axis=1)
    df_summary['total']       = df_summary[days].sum(axis=1)

    return df_summary


def attendence_per_week( df ):

    pass

   
def weekNumberFeature( df_input ):
    
    weeks = list( df_input )
    df    = df_input.copy()

    for w in weeks:
        s = pd.Series( w, index=df_input.index )
        df[w] = s     

    return df
    

def concatStaticFeatures( features, feature_names ):
        
        df = pd.concat(features, axis=1)
        df.columns = feature_names 

        return df



def createFeatureMatrix( features, feature_names, static_features ):

    weeks = list( features[1] )

    ## create an empty dataframe of students vs features
    df = pd.DataFrame( index = features[1].index, columns=feature_names )
    
    ## make a copy the empty dataframe for each week of the year
    frames = []
    for w in range(0, len(weeks)+2):
        frames.append( df.copy() )

    ## ensure that all the feature dataframes have the same column titles
    for f in features:
        assert list(f) == weeks
        
    ## copy the feature vector for each week into the correct week matrix
    f_count = 0
    w_count = 0
    for df in features:
        for w in weeks:
            frames[w-1][feature_names[f_count]] = df[w]
            w_count += 1
        w_count = 0
        f_count += 1
    
    ## add the static features

    new_frames = frames

    for f in range(0,len(frames)): 
        new_frames[f] = pd.concat( [frames[f], static_features], axis=1 )


    return new_frames

        