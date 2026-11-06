# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 16:30:03 2021

@author: VDMG013
"""

import pandas as pd
from textblob import TextBlob
import seaborn as sns
import nltk

# Text mining TT

# Data frames
df = pd.read_excel('D:/Documents/Tracking_Telefonico/TextMining_TT/TT_Historico.xlsx')
df_telcel = df.query("P5 == 2") # Telcel
df_mov = df.query("P5 == 3") # Movistar
df_att = df.query("P5 == 1 or P5 == 4 or P5 == 5 or P5 == 21") # ATT
df_otra = df.query("P5 != 1 & P5 != 2 & P5 != 3 & P5 != 4 & P5 != 5 & P5 != 21") # Otros

# TELCEL
P13A_telcel = pd.DataFrame(df.query("P5 == 2 & mes == 202107").P13A) # No recomendacion P13A
P13A_telcel = P13A_telcel.dropna()
P13B_telcel = pd.DataFrame(df.query("P5 == 2 & mes == 202107").P13B) # Necesita hacer para que recomiende P13B
P13B_telcel = P13B_telcel.dropna()
P13C_telcel = pd.DataFrame(df.query("P5 == 2 & mes == 202103").P13C) # Si recomendacion P13C
P13C_telcel = P13C_telcel.dropna()
P13B_telcel.to_csv('D:/Documents/Tracking_Telefonico/TextMining_TT/Neutros/Neutros_T_202107.csv', index = False, encoding = 'latin1')

# MOVISTAR
P13A_mov = pd.DataFrame(df.query("P5 == 3").P13A) # No recomendacion P13A
P13A_mov = P13A_mov.dropna()
P13B_mov = pd.DataFrame(df.query("P5 == 3").P13B) # Necesita hacer para que recomiende P13B
P13B_mov = P13B_mov.dropna()
P13C_mov = pd.DataFrame(df.query("P5 == 3").P13C) # Si recomendacion P13C
P13C_mov = P13C_mov.dropna()

# ATT
P13A_att = pd.DataFrame(df.query("P5 == 1 or P5 == 4 or P5 == 5 or P5 == 21").P13A) # No recomendacion P13A
P13A_att = P13A_att.dropna()
P13B_att = pd.DataFrame(df.query("P5 == 1 or P5 == 4 or P5 == 5 or P5 == 21").P13B) # Necesita hacer para que recomiende P13B
P13B_att = P13B_att.dropna()
P13C_att = pd.DataFrame(df.query("P5 == 1 or P5 == 4 or P5 == 5 or P5 == 21").P13C) # Si recomendacion P13C
P13C_att = P13C_att.dropna()

# OTRAS
P13A_otra = pd.DataFrame(df.query("P5 != 1 & P5 != 2 & P5 != 3 & P5 != 4 & P5 != 5 & P5 != 21").P13A) # No recomendacion P13A
P13A_otra = P13A_otra.dropna()
P13B_otra = pd.DataFrame(df.query("P5 != 1 & P5 != 2 & P5 != 3 & P5 != 4 & P5 != 5 & P5 != 21").P13B) # Necesita hacer para que recomiende P13B
P13B_otra = P13B_otra.dropna()
P13C_otra = pd.DataFrame(df.query("P5 != 1 & P5 != 2 & P5 != 3 & P5 != 4 & P5 != 5 & P5 != 21").P13C) # Si recomendacion P13C
P13C_otra = P13C_otra.dropna()

#%% Analisis de sentimientos
rec_telcel = pd.DataFrame({
    'coms': P13A_telcel['P13A'].append(P13C_telcel['P13C'])
    })
rec_telcel['polaridad'] = rec_telcel['coms'].apply(lambda x: TextBlob(x).sentiment.polarity)
rec_telcel['subobj'] = rec_telcel['coms'].apply(lambda x: TextBlob(x).sentiment.subjectivity)

sns.distplot(rec_telcel['polaridad'])
sns.distplot(rec_telcel['subobj'])
