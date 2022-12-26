import pandas as pd
import re

df = pd.read_csv('./most_runs_in_cricket.csv')

def preprocess():
    
    #adding country column
    #Where the player belong
    Names =[]
    Country=[]
    for x in df['Player']:
        a=  re.split("[()\xa0]", x)
        Names.append(a[0])
        b = re.split("/",a[1])
        for y in b:
            if(y!='Asia' and y!='ICC' and y!='Afr' and y!='IRE' and y!='World'):
                Country.append(y)
                
    Names = pd.Series(Names, name='Player Name')
    Country = pd.Series(Country, name='Country Name')
    df['Player Name']= Names
    df['Country']=Country

    #adding time span column for how long the player play cricket
    Start_Y =[]
    End_Y=[]
    for x in df['Span']:
        a=  re.split("-", x)
        Start_Y.append(int(a[0]))
        End_Y.append(int(a[1]))

    Start_Y = pd.Series(Start_Y, name='Beginning Year')
    End_Y = pd.Series(End_Y, name='Retire Year')
    df['Career Span'] = End_Y - Start_Y

    #Remove the + from the ball faced
    df['BF'] = df['BF'].apply(lambda x: x.rstrip('+'))
    return df
