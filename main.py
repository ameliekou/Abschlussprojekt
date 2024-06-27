import streamlit as st
import ekgdata
import matplotlib.pyplot as plt
import Person
import numpy as np
from read_pandas import read_my_csv, read_activity_csv, compute_HR_statistics, compute_power_statistics, make_pow_HR_plot, add_HR_zones, make_plot, compute_power_in_zones, compute_time_in_zones
# Zu Beginn

ekg_tab, bmi_taab, zonen_taaab=st.tabs(["EKG-Daten", "BMI Rechner" ," Zonen"])


db = Person.DB()

# Lade alle Personen
person_names = db.get_person_list()

# Anlegen diverser Session States
## Gewählte Versuchsperson
if 'aktuelle_versuchsperson' not in st.session_state:
    st.session_state.aktuelle_versuchsperson = 'None'

## Anlegen des Session State. Bild, wenn es kein Bild gibt
if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

## TODO: Session State für Pfad zu EKG Daten
if 'ekg_test' not in st.session_state:
    st.session_state.ekg_test = None

## Session State für Notizen je Nutzer
if 'user_notes' not in st.session_state:
    st.session_state.user_notes = {}

with ekg_tab:

    # Schreibe die Überschrift
    st.write("# EKG APP")
    

    col_left, col_right = st.columns(2)
    with col_left:
        st.write("##### Versuchsperson auswählen:")
    
    # Auswahlbox, wenn Personen anzulegen sind
    with col_right:
        st.session_state.aktuelle_versuchsperson = st.selectbox(
            'Versuchsperson',
            options = person_names, key="sbVersuchsperson", label_visibility="hidden")

    # Name der Versuchsperson
    #st.write("Der Name ist: ", st.session_state.aktuelle_versuchsperson) 

    # Weitere Daten wie Geburtsdatum etc. schön anzeigen
    person = db.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)

    with col_right:
        st.write("Geburtsdatum: ", person.date_of_birth)
        st.write("Alter: ", person.calc_age())
        st.write("ID: ", person.id)
        
        #Öffne EKG-Daten
        ekgdata_dict = ekgdata.EKGdata.load_by_id(person.id)

    # TODO: Für eine Person gibt es ggf. mehrere EKG-Daten. Diese müssen über den Pfad ausgewählt werden können
        ekg_list = []
        for ekg in ekgdata_dict:
            ekg_list.append(ekg["id"])

    # Auswahlbox für EKG-Daten
        st.session_state.ekg_test = st.selectbox(
            'EKG-Test auswählen:',
            options = ekg_list)



    # Nachdem eine  ausgewählt wurde, die auch in der Datenbank ist
    # Finde den Pfad zur Bilddatei
    if st.session_state.aktuelle_versuchsperson in person_names:
        st.session_state.picture_path = person.picture_path
        # st.write("Der Pfad ist: ", st.session_state.picture_path) 

    #Bild anzeigen
    from PIL import Image
    image = Image.open(st.session_state.picture_path)

    with col_left:
        st.image(image, caption=st.session_state.aktuelle_versuchsperson)
   
   # Textfeld für Notizen
    notes_key = f"notes_{person.id}_{st.session_state.aktuelle_versuchsperson}"
    st.session_state.user_notes.setdefault(notes_key, "")
    user_notes = st.text_area(
        'Platz für Notizen:',
        st.session_state.user_notes.get(notes_key, "")
    )
    st.session_state.user_notes[notes_key] = user_notes



    # EKG-Daten anzeigen
    current_ekg_data = ekgdata.EKGdata.load_by_id(person.id, st.session_state.ekg_test)
    current_ekg_data_class = ekgdata.EKGdata(current_ekg_data)

    st.write("##### EKG-Daten")
    st.write("Datum: ", current_ekg_data["date"])
    st.write("dauer in Sekunden:", int(current_ekg_data_class.time_in_seconds()))
    st.write("durchschnittliche Herzfrequenz: ", int(current_ekg_data_class.mean_heart_rate()))
    st.write("maximale Herzfrequenz: ", person.calc_max_heart_rate())

 
    # EKG-Daten als Matplotlib Plot anzeigen
    
    fig = current_ekg_data_class.plot_time_series()
    

    st.plotly_chart(fig)

   

    #st.slider("von", 0, current_ekg_data_class.max_time(), 0)
    #st.slider("bis", 0, current_ekg_data_class.max_time(), current_ekg_data_class.max_time() - 1)

    # Berechnung der HRV (anpassen an Ihre EKGdata-Klasse)
    if current_ekg_data_class:
        r_peaks = current_ekg_data_class.find_peaks()  # Annahme: Methode zur Erkennung von R-Zacken implementiert
        rr_intervals = np.diff(current_ekg_data_class.df['Time in ms'][r_peaks]) / 1000  # Zeitintervalle in Sekunden
        hrv = np.std(rr_intervals)  # Standardabweichung der RR-Intervalle als Maß für HRV

        # Anzeigen der HRV
        st.write("##### Herzratenvariabilität")
        st.write("Standardabweichung der RR-Intervalle: {:.4f} Sekunden".format(hrv))

        # Optional: Weitere Visualisierung der HRV (Histogramm der RR-Intervalle oder ähnliches)
        plt.figure(figsize=(5, 3))
        plt.hist(rr_intervals, bins=20, color='blue', alpha=0.7)
        plt.xlabel('RR-Intervalle (Sekunden)')
        plt.ylabel('Häufigkeit')
        st.pyplot(plt)

        


with bmi_taab:
    gewicht = st.number_input("Gewicht in kg")
    groesse = st.number_input("Größe in cm")

    #if st.button("BMI berechnen"):
        #st.write("Der BMI beträgt: ", gewicht / (groesse/100)**2)
    if groesse > 0 and gewicht > 0:
            bmi = gewicht / (groesse / 100) ** 2
            bmi_rounded = round(bmi, 1)
            st.write("Der BMI beträgt: {:.1f}".format(bmi_rounded))

with zonen_taaab:
    st.header("EKG-Data")
    st.write("# My Plot")

    df_ekg = read_my_csv()
    fig_ekg = make_plot(df_ekg)

    st.plotly_chart(fig_ekg)
    st.header("Power-Data")
    
    df = read_activity_csv(path="activities/activity.csv")
    hf_max, hf_mean = compute_HR_statistics(df)
    p_mean, p_max = compute_power_statistics(df)
    df = add_HR_zones(df, hf_max)

    p_zones = compute_power_in_zones(df)

    t_zones = compute_time_in_zones(df)

    
    fig = make_pow_HR_plot(df)


    #einfügen von durchgezogenen waagrechen Linien bei verschiednen Zonen-Werten von hf_max
    fig.add_hline(y=0.5*hf_max, line_dash="dash", line_color="Light Yellow")
    fig.add_hline(y=0.6*hf_max, line_dash="dash", line_color="LightGreen")
    fig.add_hline(y=0.7*hf_max, line_dash="dash", line_color="Green")
    fig.add_hline(y=0.8*hf_max, line_dash="dash", line_color="Yellow")
    fig.add_hline(y=0.9*hf_max, line_dash="dash", line_color="Red")


    #trying to color the zones:
    fig.add_hrect(y0=0.5*hf_max, y1=0.6*hf_max, fillcolor="LightYellow", opacity=0.5, line_width=0)
    fig.add_hrect(y0=0.6*hf_max, y1=0.7*hf_max, fillcolor="LightGreen", opacity=0.5, line_width=0)
    fig.add_hrect(y0=0.7*hf_max, y1=0.8*hf_max, fillcolor="Green", opacity=0.5, line_width=0)
    fig.add_hrect(y0=0.8*hf_max, y1=0.9*hf_max, fillcolor="Yellow", opacity=0.5, line_width=0)
    fig.add_hrect(y0=0.9*hf_max, y1=hf_max, fillcolor="Red", opacity=0.5, line_width=0)


    #benennen von add_hlines
    fig.add_annotation(x=0, y=0.5*hf_max, text="Start Zone 1", showarrow=False)
    fig.add_annotation(x=0, y=0.6*hf_max, text="Start Zone 2", showarrow=False)
    fig.add_annotation(x=0, y=0.7*hf_max, text="Start Zone 3", showarrow=False)
    fig.add_annotation(x=0, y=0.8*hf_max, text="Start Zone 4", showarrow=False)
    fig.add_annotation(x=0, y=0.9*hf_max, text="Start Zone 5", showarrow=False)
    

    fig.update_layout(title="Power and Heart Rate", xaxis_title="Time", yaxis_title="Power/Heart Rate")
    #fig.update_layout(color_zones(df))
    st.plotly_chart(fig)

    st.write(f"- Maximale Herzfrequenz: {round(hf_max)}")
    st.write(f"- Durchschnittliche Herzfrequenz: {round(hf_mean)}")
    st.write(f"- Durchschnittliche Leistung: {round(p_mean)}")
    st.write(f"- Maximale Leistung: {round(p_max)}")
    

    # Darstellen der Zeiten und power in den Zonen
    st.write("- Power in Zone 1:", round(p_zones[0]))
    st.write("- Power in Zone 2:", round(p_zones[1]))
    st.write("- Power in Zone 3:", round(p_zones[2]))
    st.write("- Power in Zone 4:", round(p_zones[3]))
    st.write("- Power in Zone 5:", round(p_zones[4]))

    st.write("- in Zone 1 verbrachte Zeit:", round(t_zones[0])," Sekunden")
    st.write("- in Zone 2 verbrachte Zeit:", round(t_zones[1])," Sekunden")
    st.write("- in Zone 3 verbrachte Zeit:", round(t_zones[2])," Sekunden")
    st.write("- in Zone 4 verbrachte Zeit:", round(t_zones[3])," Sekunden")
    st.write("- in Zone 5 verbrachte Zeit:", round(t_zones[4])," Sekunden")