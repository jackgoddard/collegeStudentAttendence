import pandas as pd

class algebra():
    
    def __init__(self, df, exclude=False):
        #pandas.DataFrame.__init__(self, dtypes=df,dtypes)
        self.df_input = df
      #  self.df = df
        if exclude:
            self.df = df.drop(exclude, axis=1)
        else:
            self.df = df
        print(self.df)

 #   def df(self):
 #       return self.df

    def cumcount(self):
        self.df_cumcount = self.df.notnull().cumsum(axis=1)
        return self.df_cumcount

    def cummean(self):
        cumcount()
        df_cum_mean = self.df.cumsum(axis=1) / self.df_cumcount
        return df_cum_mean
     
    









