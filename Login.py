import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="Contracta Dashboard", page_icon=":bar_chart:", layout="centered")

url = 'https://raw.githubusercontent.com/Schesch/accounting_dashboard/main/config_files/config.yaml'
response = requests.get(url)

if response.status_code == 200:
    # Load YAML content from the fetched data
    config = yaml.load(response.content, Loader=yaml.SafeLoader)
else:
    print(f"Failed to retrieve the YAML file: HTTP {response.status_code}")

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


authenticator.login()


if st.session_state["authentication_status"]:
    authenticator.logout()
    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)
    st.image('https://raw.githubusercontent.com/Schesch/accounting_dashboard/main/contracta.png', width= 600, caption="Ihre Wirtschafts- und Steuerberatung: Contracta")
    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)
    st.header(f'Willkommen {st.session_state["name"]} bei Ihrem Finance Dashboard von Contracta')
    st.markdown("<div style='margin: 25px;'></div>", unsafe_allow_html=True)
    st.markdown("Auf dieser Seite finden Sie in Echtzeit Informationen zu Ihrem Betrieb:")
    st.markdown(
        """ 
                * **Allgemeine Daten**
                * **Bilanz**
                * **Umsatz**
                * **Liquidität und Zahlungsfähigkeit**
                * **Google Bewertungen**
                """
    )
elif st.session_state["authentication_status"] is False:
    st.error('Username oder Passwort sind nicht korrekt')
elif st.session_state["authentication_status"] is None:
    st.warning('Bitte Username und Passwort eingeben')