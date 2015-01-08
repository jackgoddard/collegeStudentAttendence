class Attendence:
    def __init__(self,df_input):
        self.df_input = df_input
        
        self.df_simple = df_input
        
        ### classes where the student was present
        df_simple.mark.replace('/ ', 'P',  inplace=True)
        df_simple.mark.replace('  ', 'P',  inplace=True)  #<---- Benefit of the doubt
        df_simple.mark.replace('L ', 'P',  inplace=True)
        ### classes where the student was absent
        df_simple.mark.replace('A ', 'Ab', inplace=True)
        df_simple.mark.replace('C ', 'Ab', inplace=True)
        ### classes where the student was not required
        df_simple.mark.replace('E ', 'NR', inplace=True)
        df_simple.mark.replace('W ', 'NR', inplace=True)
        df_simple.mark.replace('X ', 'NR', inplace=True)
        df_simple.mark.replace('Y ', 'NR', inplace=True)
        df_simple.mark.replace('Z ', 'NR', inplace=True)

    
    def simpleTable(self):
        return self.df_simple


    def lateTable(self):
        self.df_late = pd.pivot_table(self.df_input[self.df_input.mark == 'L ' ], index='student_id', columns='weekno', values='mark_count' ).fillna(0)
        return self.df_late
    
    def presentTable(self):
        self.df_present = pd.pivot_table(self.df_simple[self.df_simple == 'P' ], index='student_id', columns='weekno', values='mark_count' ).fillna(0)
        return self.df_present

    def absentTable(self):
        self.df_absent = pd.pivot_table(self.df_simple[self.df_simple.mark == 'Ab'], index='student_id', columns='weekno', values='mark_count' ).fillna(0)
        return self.df_absent

    def requiredTable(self):
        self.df_required = self.df_present.add(self.df_absent)
        return self.df_required

    def notRequiredTable(self):
        self.df_not_required = pd.pivot_table(self.df_simple[self.df_simple.mark == 'NR'], index='student_id', columns='weekno', values='mark_count' ).fillna(0)
        return self.df_not_required



