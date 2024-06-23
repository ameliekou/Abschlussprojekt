#read_pandas_Aufgabe_3

# Paket für Bearbeitung von Tabellen
import pandas as pd


# Paket
## zuvor !pip install plotly
## ggf. auch !pip install nbformat
import plotly.express as px

def read_my_csv(): #TODO change path to EKG data
    # Einlesen eines Dataframes
    ## "\t" steht für das Trennzeichen in der txt-Datei (Tabulator anstelle von Beistrich)
    ## header = None: es gibt keine Überschriften in der txt-Datei
    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep="\t", header=None)

    # Setzt die Columnnames im Dataframe
    df.columns = ["Messwerte in Watt", "Zeit in Sekunden"]
    
    # Gibt den geladen Dataframe zurück
    return df

def make_plot(df):
    #Erstelle plot mit Power und HR als y-Achse und Zeit als x-Achse
    fig = px.line(df.head(2000), x= "Zeit in Sekunden", y="Messwerte in Watt")
    
    return fig

def read_activity_csv(path="data/activities/activity.csv"):
    # Einlesen eines Dataframes
    ## "\t" steht für das Trennzeichen in der txt-Datei (Tabulator anstelle von Beistrich)
    ## header = None: es gibt keine Überschriften in der txt-Datei
    df = pd.read_csv(path)

    #TODO add 'time' column DONE
    df['time'] = [i for i in range(len(df))]

    # Gibt den geladen Dataframe zurück
    return df

def compute_HR_statistics(df):
    hf_max = df['HeartRate'].max()
    hf_mean = df['HeartRate'].mean()

    return hf_max, hf_mean

def compute_power_statistics(df):
    # compute mean and max
    p_mean = df['PowerOriginal'].mean()
    p_max = df['PowerOriginal'].max()


    return p_mean, p_max


def make_pow_HR_plot(df):
    #Erstelle plot mit Power und HR als y-Achse und Zeit als x-Achse
    fig = px.line(df, x= "time", y=["PowerOriginal", "HeartRate"])
    # fig.add_scatter(df, x="time", y="HeartRate", mode='lines', name='HeartRate')
    fig.update_layout(title='Power and HeartRate over time')
    return fig


def add_HR_zones(df, hf_max):
    #create 5 Zones for HR based on hf_max
    zone_1_min = 0.5 * hf_max
    zone_1_max = 0.6 * hf_max
    zone_2_max = 0.7 * hf_max
    zone_3_max = 0.8 * hf_max
    zone_4_max = 0.9 * hf_max
    zone_5_max = 1 * hf_max
    df['zone_1'] = (df['HeartRate'] > zone_1_min) & (df['HeartRate'] <= zone_1_max)
    df['zone_2'] = (df['HeartRate'] > zone_1_max) & (df['HeartRate'] <= zone_2_max)
    df['zone_3'] = (df['HeartRate'] > zone_2_max) & (df['HeartRate'] <= zone_3_max)
    df['zone_4'] = (df['HeartRate'] > zone_3_max) & (df['HeartRate'] <= zone_4_max)
    df['zone_5'] = (df['HeartRate'] > zone_4_max) & (df['HeartRate'] <= zone_5_max)

    return df


def compute_time_in_zones(df):
    #compute time in each zone
    t_1 = df['zone_1'].sum() #where zone_1 is True
    t_2 = df['zone_2'].sum() #where zone_2 is True
    t_3 = df['zone_3'].sum() #where zone_3 is True
    t_4 = df['zone_4'].sum() #where zone_4 is True
    t_5 = df['zone_5'].sum() #where zone_5 is True

    return [t_1, t_2, t_3, t_4, t_5]


def compute_power_in_zones(df):
    #compute power in each zone
    p_1 = df['PowerOriginal'][df['zone_1']].mean() #where zone_1 is True
    p_2 = df['PowerOriginal'][df['zone_2']].mean() #where zone_2 is True
    p_3 = df['PowerOriginal'][df['zone_3']].mean() #where zone_3 is True
    p_4 = df['PowerOriginal'][df['zone_4']].mean() #where zone_4 is True
    p_5 = df['PowerOriginal'][df['zone_5']].mean() #where zone_5 is True

    return [p_1, p_2, p_3, p_4, p_5]





'''def color_zones(df):
    #TODO color zones in plot
    if 'zone_1' == True:
        plot_bgcolor = 'green'          --> bereits in main.py überholt
    elif 'zone_2' == True:
        plot_bgcolor = 'yellow'
    elif 'zone_3' == True:
        plot_bgcolor = 'orange'
    elif 'zone_4' == True:
        plot_bgcolor = 'red'
    elif 'zone_5' == True:
        plot_bgcolor = 'purple'
    else:
        pass'''


if __name__ == '__main__':
    # Test all blocks
    df = read_activity_csv()
    print(df.head())
    print("p_mean, p_max:", compute_power_statistics(df))
    hf_max, hf_mean = compute_HR_statistics(df)	
    df = add_HR_zones(df, hf_max)
    print("time in zones:", compute_time_in_zones(df))
    print("power in zones:", compute_power_in_zones(df)) 
    fig = make_pow_HR_plot(df)
    fig.show()
