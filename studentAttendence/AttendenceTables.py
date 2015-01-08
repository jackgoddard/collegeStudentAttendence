import numpy as np
import pandas as pd
from dfAlgebra.dfAlgebra import algebra as alg

class Attendence:
    
    def __init__(self,df_input):
        
        self.df_input  = df_input.copy()        
        self.df_simple = df_input.copy()
        
        ### classes where the student was present
        self.df_simple.mark.replace('/ ', 'P',  inplace=True)
        self.df_simple.mark.replace('  ', 'P',  inplace=True)  #<---- Benefit of the doubt
  
        ### classers where the student is late
        self.df_simple.mark.replace('L ', 'L',  inplace=True)
  
        ### classes where the student was absent
        self.df_simple.mark.replace('A ', 'Ab', inplace=True)
        self.df_simple.mark.replace('C ', 'Ab', inplace=True)
  
        ### classes where the student was not required
        self.df_simple.mark.replace('E ', 'NR', inplace=True)
        self.df_simple.mark.replace('W ', 'NR', inplace=True)
        self.df_simple.mark.replace('X ', 'NR', inplace=True)
        self.df_simple.mark.replace('Y ', 'NR', inplace=True)
        self.df_simple.mark.replace('Z ', 'NR', inplace=True)

        ### Add columns with attendence status count 
        self.df_simple['Ab'] = self.df_simple[self.df_simple.mark=='Ab'].mark_count
        self.df_simple['P']  = self.df_simple[self.df_simple.mark=='P'].mark_count
        self.df_simple['L']  = self.df_input[self.df_simple.mark=='L'].mark_count.fillna(0)
        self.df_simple['P']  = self.df_simple['P'].fillna(0) + self.df_simple['L'].fillna(0)
        self.df_simple['R']  = self.df_simple['P'].fillna(0) + self.df_simple['Ab'].fillna(0)
        self.df_simple['NR'] = self.df_simple[self.df_simple.mark=='NR'].mark_count

        ### Create summary tables ###
        self.df_late         = pd.pivot_table( self.df_simple, index='student_id', columns='weekno', values='L',            aggfunc=np.sum ).fillna(0)
        self.df_present      = pd.pivot_table( self.df_simple, index='student_id', columns='weekno', values='P',            aggfunc=np.sum ).fillna(0)
        self.df_absent       = pd.pivot_table( self.df_simple, index='student_id', columns='weekno', values='Ab',           aggfunc=np.sum ).fillna(0)
        self.df_not_required = pd.pivot_table( self.df_simple, index='student_id', columns='weekno', values='NR',           aggfunc=np.sum ).fillna(0)
        self.df_required     = pd.pivot_table( self.df_simple, index='student_id', columns='weekno', values='R',            aggfunc=np.sum ).fillna(0)
        self.df_mins_late    = pd.pivot_table( self.df_simple, index='student_id', columns='weekno', values='mins_late',    aggfunc=np.sum ).fillna(0)          
        self.df_contact_mins = pd.pivot_table( self.df_simple, index='student_id', columns='weekno', values='contact_mins', aggfunc=np.sum ).fillna(0)

        self.df_mins_frac_late    = self.df_mins_late / self.df_contact_mins
         

     #   print(self.df_contact_mins.index[self.df_contact_mins.index =='AAN12418843'])

    def inputTable(self):
        return self.df_input
        
    def simpleTable(self):
        return self.df_simple

    def lateTable(self):
        return self.df_late
    
    def presentTable(self):
        return self.df_present

    def absentTable(self):
        return self.df_absent

    def requiredTable(self):
        return self.df_required

    def contactMinsTable(self):
        return self.df_contact_mins

    def fracMinsLateTable(self):
        return self.df_mins_frac_late    

    def notRequiredTable(self):
        return self.df_not_required

    def fracPresentTable(self):
        self.df_frac_present = self.df_present / self.df_required
        return self.df_frac_present

    def fracAbsentTable(self):
        self.df_frac_absent = self.df_absent / self.df_required 
        return self.df_frac_absent

    def fracLateTable(self):
        self.df_frac_late = self.df_late / self.df_required
        return self.df_frac_late

    def avFracPresentTable(self):
         self.df_av_frac_present = self.df_present.cumsum(axis=1) / self.df_required.cumsum(axis=1)
         return self.df_av_frac_present

    def avFracAbsentTable(self):
         self.df_av_frac_absent = self.df_absent.cumsum(axis=1) / self.df_required.cumsum(axis=1)
         return self.df_av_frac_absent

    def avFracLateTable(self):
        self.df_av_frac_late = self.df_late.cumsum(axis=1) / self.df_required.cumsum(axis=1)
        return self.df_av_frac_late

    def avChangeFracPresentTable(self):
        self.df_av_ch_frac_present = self.fracPresentTable() / self.df_av_frac_present
        return self.df_av_ch_frac_present

    def weeklyChangeFracPresentTable(self):
        self.fracPresentTable()
        weeks = list(self.df_frac_present)
        
        self.df_frac_change_present = self.presentTable().copy()
        for w in range(1,len(weeks)):
            current = self.fracPresentTable()[weeks[w]]
            past    = self.fracPresentTable()[weeks[w-1]]
            self.df_frac_change_present[weeks[w]] = (current.fillna(0) - past.fillna(0)) / past.fillna(1)

        return self.df_frac_change_present

    def weeklyChangeFracLateTable(self):
        self.fracLateTable()
        weeks = list(self.df_frac_late)
        
        self.df_frac_change_late = self.lateTable().copy()
        for w in range(1,len(weeks)):
            current = self.fracLateTable()[weeks[w]]
            past    = self.fracLateTable()[weeks[w-1]]
            self.df_frac_change_late[weeks[w]] = (current.fillna(0) - past.fillna(0)) / past.fillna(1)

        return self.df_frac_change_late


    def weeklyOverallChangeFracPresentTable(self):
        self.fracPresentTable()
        weeks = list(self.df_frac_present)
        
        self.df_frac_change_present = self.fracPresentTable()
        
       # df_cumlative = self.

        for w in range(1,len(weeks)):
         #   print( str(w)+'  '+str(weeks[w]) )
            current = self.fracPresentTable()[weeks[w]]
            past    = self.fracPresentTable()[weeks[w-1]]

            self.df_frac_change_present[weeks[w]] = current/past

        return self.df_frac_change_present
     
    def weeklyAttendenceCumFrac(self):

        df_cumfrac = self.df_required.cumsum(axis=1) # / self.df_required.count(axis = 1 )

        return df_cummean

    def fracPresentByMeanTable(self):
        self.present_by_mean = self.fracPresentTable()/self.avFracPresentTable()
        return self.present_by_mean


    def fracLateByMeanTable(self):
        self.late_by_mean = self.fracLateTable()/self.avFracLateTable()
        return self.late_by_mean


    def minsLateTable(self):
      #  print(self.df_mins_late)
        return self.df_mins_late

    def totalContactTimeTable(self):
        return self.contactMinsTable().sum(axis=1)

    def contactMinsPassedTable(self):
        df = self.contactMinsTable().cumsum(axis=1)
        return df
        

    def fracContactTimePassedTable(self):
        df = self.contactMinsPassedTable().div(self.contactMinsTable().sum(axis=1), axis='index' )
#           print(df)
        return df

