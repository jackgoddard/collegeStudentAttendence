import pandas as pd
from dfAlgebra.dfAlgebra import algebra as alg

class Attendence:
    
    def __init__(self,df_input):
        self.df_input = df_input
        
        self.df_simple = df_input
        
        ### classes where the student was present
        self.df_simple.mark.replace('/ ', 'P',  inplace=True)
        self.df_simple.mark.replace('  ', 'P',  inplace=True)  #<---- Benefit of the doubt
        self.df_simple.mark.replace('L ', 'P',  inplace=True)
        ### classes where the student was absent
        self.df_simple.mark.replace('A ', 'Ab', inplace=True)
        self.df_simple.mark.replace('C ', 'Ab', inplace=True)
        ### classes where the student was not required
        self.df_simple.mark.replace('E ', 'NR', inplace=True)
        self.df_simple.mark.replace('W ', 'NR', inplace=True)
        self.df_simple.mark.replace('X ', 'NR', inplace=True)
        self.df_simple.mark.replace('Y ', 'NR', inplace=True)
        self.df_simple.mark.replace('Z ', 'NR', inplace=True)

        ### Create summary tables ###

        self.late         = alg(pd.pivot_table(self.df_input[self.df_input.mark  == 'L ' ],  index='student_id', columns='weekno', values='mark_count' ))
        self.present      = alg(pd.pivot_table(self.df_simple[self.df_simple.mark == 'P' ],  index='student_id', columns='weekno', values='mark_count' ))
        self.absent       = alg(pd.pivot_table(self.df_simple[self.df_simple.mark == 'Ab'],  index='student_id', columns='weekno', values='mark_count' ))
        self.not_required = alg(pd.pivot_table(self.df_simple[self.df_simple.mark == 'NR'],  index='student_id', columns='weekno', values='mark_count' ))
        self.required     = alg(self.present.df.add(self.absent.df))
     
    def simpleTable(self):
        return self.df_simple

    def lateTable(self):
        return self.late.df
    
    def presentTable(self):
        return self.present

    def absentTable(self):
        return self.absent

    def requiredTable(self):
        return self.required

    def notRequiredTable(self):
        return self.not_required.df

    def fracPresentTable(self):
         self.df_frac_present = self.present.df / self.required.df
         return self.df_frac_present

    def fracAbsentTable(self):
         self.df_frac_absent = self.absent.df / self.required.df 
         return self.df_frac_absent

    def fracLateTable(self):
         self.df_frac_late = self.late.df / self.required.df
         return self.df_frac_late

    def weeklyChangeFracPresentTable(self):
        self.fracPresentTable()
        weeks = list(self.df_frac_present)
        
        self.df_frac_change_present = self.fracPresentTable()
        for w in range(1,len(weeks)):
         #   print( str(w)+'  '+str(weeks[w]) )
            current = self.fracPresentTable()[weeks[w]]
            past    = self.fracPresentTable()[weeks[w-1]]

            self.df_frac_change_present[weeks[w]] = current/past

        return self.df_frac_change_present

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

        df_cumfrac = self.required.cumsum(axis=1) # / self.df_required.count(axis = 1 )

        return df_cummean

