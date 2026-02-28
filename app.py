import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import requests
from datetime import datetime
import time

###################################
# SETTINGS
###################################

PHONE_IP = "10.145.180.40"

###################################
# LOAD MODEL
###################################

model = pickle.load(open("model.pkl","rb"))

st.set_page_config(
page_title="Women Safety AI",
layout="wide"
)

###################################
# HEADER
###################################

st.markdown("""
<h1 style='text-align:center'>
🚨 AI Freeze Response Detection
</h1>
""",unsafe_allow_html=True)

st.markdown("""
<h4 style='text-align:center'>
Safety when you can't react
</h4>
""",unsafe_allow_html=True)

st.divider()

###################################
# SOS BUTTON
###################################

if st.button("🚨 SOS EMERGENCY"):

    st.session_state.sms_sent=False
    st.session_state.force_alert=True

###################################
# SESSION VARIABLES
###################################

if "movement_list" not in st.session_state:
    st.session_state.movement_list=[]

if "history" not in st.session_state:
    st.session_state.history=[]

if "still_time" not in st.session_state:
    st.session_state.still_time=0

if "sms_sent" not in st.session_state:
    st.session_state.sms_sent=False

if "force_alert" not in st.session_state:
    st.session_state.force_alert=False

###################################
# SMS FUNCTION
###################################

def send_sms():

    lat=28.61
    lon=77.23

    link=f"https://maps.google.com/?q={lat},{lon}"

    now=datetime.now().strftime("%H:%M:%S")

    st.error("🚨 EMERGENCY ALERT SENT")

    st.write("Mom Notified")
    st.write("Friend Notified")
    st.write("Brother Notified")

    st.code(f"""
EMERGENCY ALERT

Possible danger detected

Location:
{link}

Time:
{now}
""")

###################################
# SENSOR DATA
###################################

try:

    url=f"http://{PHONE_IP}:8080/get?accX&accY&accZ"

    r=requests.get(url,timeout=1)

    sensor=r.json()

    ax=sensor["buffer"]["accX"]["buffer"][0]
    ay=sensor["buffer"]["accY"]["buffer"][0]
    az=sensor["buffer"]["accZ"]["buffer"][0]

    movement=abs(ax)+abs(ay)+abs(az)

    ###################################
    # NOISE FILTER
    ###################################

    if movement < 0.08:
        movement=0

except:

    st.warning("Phone sensor not connected")

    movement=1


###################################
# FREEZE TIMER
###################################

if movement==0:
    st.session_state.still_time+=2
else:
    st.session_state.still_time=0
    st.session_state.sms_sent=False

duration=st.session_state.still_time

###################################
# SAVE GRAPH
###################################

st.session_state.movement_list.append(movement)

if len(st.session_state.movement_list)>30:
    st.session_state.movement_list.pop(0)

###################################
# AI MODEL
###################################

data=pd.DataFrame(
[[movement,0.5,duration]],
columns=['movement','audio','duration']
)

prediction=model.predict(data)

prob=model.predict_proba(data)[0][1]

###################################
# RISK SCORE
###################################

movement_score=max(0,1-movement)
duration_score=duration/300

risk_score=movement_score*0.6 + duration_score*0.4

safe_risk=max(0,min(risk_score,1))

###################################
# DASHBOARD
###################################

st.subheader("Live Safety Status")

c1,c2,c3,c4=st.columns(4)

c1.metric("Movement",round(movement,3))
c2.metric("Freeze Time",duration)
c3.metric("Risk Score",round(risk_score,2))
c4.metric("Freeze Probability",round(prob*100,1))

st.progress(safe_risk)

###################################
# RISK LEVEL
###################################

if risk_score<0.3:

    st.success("🟢 LOW RISK")

elif risk_score<0.6:

    st.warning("🟡 MEDIUM RISK")

else:

    st.error("🔴 HIGH RISK")

###################################
# ALERT LOGIC
###################################

if (prediction[0]==1 and risk_score>0.6) or st.session_state.force_alert:

    st.markdown("""
    <h1 style='text-align:center;color:red'>
    🚨 DANGER 🚨
    </h1>
    """,unsafe_allow_html=True)

    if st.session_state.sms_sent==False:

        send_sms()

        st.session_state.sms_sent=True

        st.session_state.history.append(
        "Emergency Alert Sent"
        )

###################################
# GRAPH
###################################

st.subheader("Movement History")

fig,ax=plt.subplots(figsize=(6,3))

ax.plot(st.session_state.movement_list)

st.pyplot(fig)

###################################
# MAP
###################################

lat=28.61
lon=77.23

m=folium.Map(location=[lat,lon],zoom_start=15)

folium.Marker([lat,lon]).add_to(m)

st.subheader("Location")

st_folium(m,width=700)

###################################
# HISTORY
###################################

st.divider()

st.header("Alert History")

for h in st.session_state.history:

    st.write("⚠",h)

###################################
# AUTO REFRESH
###################################

time.sleep(2)
st.rerun()