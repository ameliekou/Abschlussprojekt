import streamlit as st
import ekgdata
import matplotlib.pyplot as plt
import Person


# Zu Beginn

ekg_tab, bmi_taab =st.tabs(["EKG-Daten", "BMI Rechner"])


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

with ekg_tab:

    # Schreibe die Überschrift
    st.write("# EKG APP")
    st.write("## Versuchsperson auswählen")

    # Auswahlbox, wenn Personen anzulegen sind
    st.session_state.aktuelle_versuchsperson = st.selectbox(
        'Versuchsperson',
        options = person_names, key="sbVersuchsperson", label_visibility="hidden")

    col_left, col_right = st.columns(2)

    # Name der Versuchsperson
    #st.write("Der Name ist: ", st.session_state.aktuelle_versuchsperson) 

    # Weitere Daten wie Geburtsdatum etc. schön anzeigen
    person = db.find_person_data_by_name(st.session_state.aktuelle_versuchsperson)

    with col_right:
        st.write("## Daten von ", st.session_state.aktuelle_versuchsperson)
        st.write("Geburtsdatum: ", person.date_of_birth)
        st.write("Alter: ", person.calc_age())
        st.write("ID: ", person.id)
        st.write("maximale Herzfrequenz: ", person.calc_max_heart_rate())



    # Nachdem eine Versuchsperson ausgewählt wurde, die auch in der Datenbank ist
    # Finde den Pfad zur Bilddatei
    if st.session_state.aktuelle_versuchsperson in person_names:
        st.session_state.picture_path = person.picture_path
        # st.write("Der Pfad ist: ", st.session_state.picture_path) 

    #Bild anzeigen
    from PIL import Image
    image = Image.open(st.session_state.picture_path)

    with col_left:
        st.image(image, caption=st.session_state.aktuelle_versuchsperson)

    #Öffne EKG-Daten
    ekgdata_dict = ekgdata.EKGdata.load_by_id(person.id)

    st.write("## EKG-Daten auswählen")
    # TODO: Für eine Person gibt es ggf. mehrere EKG-Daten. Diese müssen über den Pfad ausgewählt werden können
    ekg_list = []
    for ekg in ekgdata_dict:
        ekg_list.append(ekg["id"])

    # Auswahlbox für EKG-Daten
    st.session_state.ekg_test = st.selectbox(
        'EKG-Test',
        options = ekg_list)

    # EKG-Daten anzeigen
    current_ekg_data = ekgdata.EKGdata.load_by_id(person.id, st.session_state.ekg_test)
    current_ekg_data_class = ekgdata.EKGdata(current_ekg_data)

    st.write("## EKG-Daten")
    st.write("Datum: ", current_ekg_data["date"])
    st.write("dauer in Sekunden:", int(current_ekg_data_class.time_in_seconds()))
    st.write("durchschnittliche Herzfrequenz: ", int(current_ekg_data_class.mean_heart_rate()))

    # EKG-Daten als Matplotlib Plot anzeigen
    fig = current_ekg_data_class.plot_time_series()

    st.plotly_chart(fig)

    st.slider("von", 0, current_ekg_data_class.max_time(), 0)

    st.slider("bis", 0, current_ekg_data_class.max_time(), current_ekg_data_class.max_time() - 1)




with bmi_taab:
    gewicht = st.number_input("Gewicht in kg")
    groesse = st.number_input("Größe in cm")

    if st.button("BMI berechnen"):
        st.write("Der BMI beträgt: ", gewicht / (groesse/100)**2)