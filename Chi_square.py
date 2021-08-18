import pandas as pd
import numpy as np
from scipy.stats import chi2


def contingency_table(tb):
    tb1 = pd.DataFrame()
    for name in tb.columns:
        tb1[name] = tb[name].value_counts()
    tb1.loc['Всего_Cтолбцы']= tb1.sum(numeric_only=True, axis=0)
    tb1.loc[:,'Всего_Строки'] = tb1.sum(numeric_only=True, axis=1)
    return tb1

def chi_square(df, output='coef'):
    K = list(df.index)
    L = list(df.columns)
    n = df.loc['Всего_Cтолбцы','Всего_Строки']
    
    chi = sum(((df.loc[i,j] - (df.loc[i, "Всего_Строки"]*df.loc['Всего_Cтолбцы', j]/n))**2) / (
                df.loc[i, "Всего_Строки"]*df.loc['Всего_Cтолбцы', j]/n)   
              for j in L for i in K)
    
    
    if output == 'coef':
        return chi
    elif output == 'conclusion':
        value = chi2.ppf(0.95, 1)
        if chi < value:
            print("Статистическая значимость наблюдаемой связи отсутствует с вероятностью 95%. табличное: ", value,
                  " расчётное: ", chi)
        else:
            print("Наблюдается статистическая значимость связи с вероятностью 95%. табличное: ", value,
                  " расчётное: ", chi)
    else:
        raise ValueError("Доступные опции вывода: coef, conclusion")
