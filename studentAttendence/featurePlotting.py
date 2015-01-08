import random


def plotFeatures( features, y, y_drop, limit=500 ):

    colours = y_drop
    colours.replace(True,  'r', inplace=True)
    colours.replace(False, 'b', inplace=True)

    print(colours.values)

    pl_present = features.presentTable().head(limit).T.plot(legend=False, color = colours.values)
    pl_present.set_xlabel('Week')
    pl_present.set_ylabel('Attendence [Days]')
    #print( some(features.fracPresentTable(),20) )

    pl_attendence = features.fracPresentTable().head(limit).T.plot(legend=False, ylim=[0,1.1])
    pl_attendence.set_xlabel('Week')
    pl_attendence.set_ylabel('Attendence [Fraction]')
    #print( some(features.fracPresentTable(),20) )


    pl_av_attendence = features.avFracPresentTable().head(limit).T.plot(legend=False, ylim=[0,1.1])
    pl_av_attendence.set_xlabel('Week')
    pl_av_attendence.set_ylabel('Average Attendence To Date')


    #pl_status = y.head(limit).T.plot(legend=False)
    #pl_status.set_xlabel('Week')
    #pl_status.set_ylabel('Status')


    #time_features = []
    #time_features.append(ft.weekNumberFeature( weekly_att.presentTable() ) )
    #time_features.append(weekly_att.fracPresentTable())                       ## Fractional lesson attendence
    #time_features.append(weekly_att.fracLateTable())                          ## Fractional late lesssons
    #time_features.append(weekly_att.weeklyChangeFracPresentTable())           ## Change in fractional attendence from last week
    #time_features.append(weekly_att.avFracPresentTable())                     ## Average fractional attendence to date
    #time_features.append(weekly_att.fracLateByMeanTable())                    ## This weeks lates / Average lates lessons to date
    #time_features.append(weekly_att.fracPresentByMeanTable())                 ## This weeks attendence / Average attendence lessons to date
    #time_features.append(weekly_att.fracMinsLateTable())                      ## Fraction of time missed in the late lessons 
    #time_features.append(weekly_att.contactMinsTable()/60.0 )                 ## Contact time that week
    #time_features.append(weekly_att.contactMinsPassedTable()/60.0)            ## Cumlative contact time up until this week
    #time_features.append(weekly_att.fracContactTimePassedTable())             ## Fraction of total contact time that has been completed