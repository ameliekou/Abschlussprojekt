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
        st.session_state.user_notes.get(notes_key, ""),
        key=notes_key
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
    
    #fig = current_ekg_data_class.plot_time_series()
    #st.plotly_chart(fig)

    st.subheader("Wählen sie eine Zeitperiode aus:")
    slider_range = st.slider("Zeitbereich:", value=[float(0), current_ekg_data_class.time_in_seconds()/60], min_value=float(0), max_value=current_ekg_data_class.time_in_seconds()/60, step=1/60)
    start, end = slider_range
    st.write("Von: ", round(start, 2), " bis: ", round(end, 2), "Minuten")
    
    # Update the plot with the selected range
    fig = current_ekg_data_class.plot_time_series()
    fig.update_layout(xaxis=dict(range=[start, end]))
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
    def calculate_angle_for_bmi(sizes, labels, bmi_category):
        category_index = labels.index(bmi_category)
        start_angle = sum(sizes[:category_index]) / sum(sizes) * 360
        slice_angle = sizes[category_index] / sum(sizes) * 360
        return start_angle + slice_angle / 2
    
    def calculate_angle_and_label_positions(sizes, labels):
        angles = []
        label_positions = []

        total = sum(sizes)
        cumulative_sizes = np.cumsum(sizes)
    
        for i in range(len(labels)):
            if i == 0:
                start_angle = 0
            else:
                start_angle = cumulative_sizes[i - 1] / total * 360
        
            slice_angle = sizes[i] / total * 360
            angle = start_angle + slice_angle / 2
            angles.append(angle)
        
        # Position für die Label-Beschriftung
            label_angle = start_angle + slice_angle / 2
            label_x = 0.7 * np.cos(np.radians(label_angle))  # Grobe Anpassung mit 0.7 um näher am Kreisrand zu sein
            label_y = 0.7 * np.sin(np.radians(label_angle))  
            label_positions.append((label_x, label_y))

        return angles, label_positions
    


with st.container():
    gewicht = st.number_input("Gewicht in kg")
    groesse = st.number_input("Größe in cm")
    
    if groesse > 0 and gewicht > 0:
        try:
            bmi = gewicht / (groesse / 100) ** 2
            if bmi > 105:
                st.write("Bitte Größe in cm eingeben")
            else:
                bmi_rounded = round(bmi, 1)
                st.write("Ihr BMI beträgt: {:.1f}".format(bmi_rounded))
                
                # BMI Kategorien
                if bmi < 18.5:
                    bmi_kategorie = 'Untergewicht'
                    bmi_value = '105'
                    farbe = 'yellow'
                elif 18.5 <= bmi < 25:
                    bmi_kategorie = 'Normalgewicht'
                    bmi_value = '18.5'
                    farbe = 'green'
                elif 25 <= bmi < 30:
                    bmi_kategorie = 'Übergewicht'
                    bmi_value = '25'
                    farbe = 'orange'
                else:
                    bmi_kategorie = 'Adipositas'
                    bmi_value = '30'
                    farbe = 'red'

                # Daten für das Kuchendiagramm
                labels = ['Untergewicht', 'Normalgewicht', 'Übergewicht', 'Adipositas']
                sizes = [18.5, 6.5, 5, 100 - 30]  # Anteile basierend auf BMI-Grenzen
                colors = ['yellow', 'green', 'orange', 'red']
                bmi_Werte = ["0 - 18.5", "18.5 - 25", "25 - 30", "30 - 105"]

                fig1, ax1 = plt.subplots()
                angles, label_positions = calculate_angle_and_label_positions(sizes, labels)
                
                wedges, texts = ax1.pie(sizes, labels=labels, colors=colors, startangle=0, 
                                                   textprops=dict(color="black", fontsize=10))
            
                ax1.legend(wedges, labels, title="BMI Kategorien", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
                ax1.axis('equal')  # Gleichmäßiger Kreis
                
                for i, wedge in enumerate(wedges):
                    angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
                    x = wedge.r * 0.8 * np.cos(np.deg2rad(angle))
                    y = wedge.r * 0.8 * np.sin(np.deg2rad(angle))
                    ax1.text(x, y, bmi_Werte[i], ha='center', va='center', fontsize=6.5, color='black')

                # Anzeige des Kuchendiagramms in Streamlit
                
                st.pyplot(fig1)

                # Anzeige der BMI Kategorie und Farbe in HTML
                st.markdown("### BMI Kategorie")
                st.markdown(f"Der BMI entspricht der Kategorie: <span style='color:{farbe}'>{bmi_kategorie}</span>", unsafe_allow_html=True)

                # Erklärung für jede Kategorie
                if bmi_kategorie == 'Untergewicht':
                    st.write("Untergewicht kann auf verschiedene Ursachen zurückzuführen sein, wie beispielsweise eine unzureichende Nährstoffaufnahme oder eine Stoffwechselerkrankung. Es ist wichtig, die Ursache zu identifizieren und gegebenenfalls einen Arzt zu konsultieren.")
                elif bmi_kategorie == 'Normalgewicht':
                    st.write("Normalgewicht ist ein Indikator für ein gesundes Körpergewicht. Es ist wichtig, auf eine ausgewogene Ernährung und regelmäßige Bewegung zu achten, um das Gewicht zu halten.")
                elif bmi_kategorie == 'Übergewicht':
                    st.write("Übergewicht kann das Risiko für verschiedene Erkrankungen wie Diabetes oder Herz-Kreislauf-Erkrankungen erhöhen. Es ist ratsam, auf eine gesunde Ernährung und ausreichend Bewegung zu achten, um das Gewicht zu reduzieren. Jedoch kann vor allem leichtes Übergewicht auch durch Muskelmasse bedingt sein und muss nicht zwangsläufig ungesund sein.")
                else:
                    st.write("Adipositas ist eine ernsthafte Erkrankung, die das Risiko für verschiedene gesundheitliche Probleme wie Diabetes, Herz-Kreislauf-Erkrankungen oder Gelenkprobleme erhöhen kann. Es könnte hilfreich sein, professionelle Hilfe in Anspruch zu nehmen, um das Gewicht zu reduzieren und die Gesundheit zu verbessern.")

                # Hinweis
                st.markdown("### HINWEIS!")
                st.write("Zu beachten ist, dass der BMI ein einfacher Indikator für das Körpergewicht ist, der jedoch nicht zwischen Muskelmasse und Fettmasse unterscheidet. Daher kann er bei sehr muskulösen Personen zu einem falschen Ergebnis führen.")

        except Exception as e:
            st.write(f"Ein Fehler ist aufgetreten: {e}")


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