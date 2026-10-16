import os
import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="AGRI//NOVA — Intelligence for Every Acre", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

# ── Visual system ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#070a08;--surface:#101612;--line:#28372c;--lime:#c7ff5e;--green:#65e58b;--cream:#f4f4e9;--muted:#8e9a8d}
html,body,[class*="css"]{font-family:'Manrope',sans-serif}
.stApp{background:#070a08;color:var(--cream)}
[data-testid="stHeader"]{background:rgba(7,10,8,.92)}
[data-testid="stSidebar"]{background:#0b100c;border-right:1px solid #263429}
[data-testid="stSidebar"] *{color:#e7ecdf}
.block-container{max-width:1600px;padding:1.1rem 2.2rem 2.5rem}
h1,h2,h3{font-family:'Manrope',sans-serif;letter-spacing:-.055em}
h1{font-size:clamp(2.5rem,4vw,4.6rem);line-height:.98;font-weight:800}
h2{font-weight:800}
[data-testid="stMetric"]{background:#111812;border:1px solid #29382b;border-radius:16px;padding:15px 17px}
[data-testid="stMetricLabel"]{color:#9aa998}
[data-testid="stMetricValue"]{color:#f4f4e9;font-weight:800}
[data-testid="stMetricDelta"]{font-family:'DM Mono',monospace}
.hero{position:relative;overflow:hidden;background:#c7ff5e;color:#10160b;border-radius:26px;padding:34px 38px 30px;margin:5px 0 22px;min-height:275px}
.hero:after{content:'N';font-family:'Manrope';font-size:320px;line-height:.8;font-weight:800;position:absolute;right:2%;bottom:-27%;color:#15220c;opacity:.07;transform:rotate(-10deg)}
.hero-kicker{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.15em;font-weight:500}
.hero-title{font-size:clamp(40px,5.2vw,76px);font-weight:800;letter-spacing:-.075em;line-height:.92;margin:22px 0 16px;max-width:850px}
.hero-copy{font-size:14px;line-height:1.7;max-width:650px;color:#2b3820}
.topline{display:flex;justify-content:space-between;align-items:center;padding:6px 2px 17px;color:#a9b6a5;font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.07em}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#c7ff5e;margin-right:8px;box-shadow:0 0 12px #c7ff5e}
.section-head{display:flex;align-items:baseline;justify-content:space-between;margin:22px 0 12px}
.section-head h3{font-size:21px;margin:0;font-weight:800}
.micro{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.12em;color:#91a18f}
.tile{background:linear-gradient(145deg,#151d16,#0e140f);border:1px solid #29372b;border-radius:19px;padding:18px;min-height:140px}
.tile-label{color:#a4b29f;font-size:12px}
.tile-value{font-size:31px;font-weight:800;letter-spacing:-.06em;margin:12px 0 5px}
.tile-foot{font-family:'DM Mono',monospace;font-size:10px;color:#a7b5a0}
.feature{border:1px solid #29382b;border-radius:19px;padding:19px;background:#0d130f;min-height:185px}
.feature-no{font-family:'DM Mono',monospace;color:#c7ff5e;font-size:11px}
.feature-title{font-size:20px;font-weight:800;letter-spacing:-.04em;margin:14px 0 8px}
.feature-copy{font-size:12px;line-height:1.65;color:#a9b5a3}
.stButton>button{background:#c7ff5e;color:#11170a;border:1px solid #c7ff5e;border-radius:11px;font-weight:800;min-height:43px;transition:all .2s}
.stButton>button:hover{background:#d9ff8d;color:#11170a;border-color:#e4ffb2;box-shadow:0 0 22px #c7ff5e20;transform:translateY(-1px)}
.stTextInput input,.stTextArea textarea{background:#111812!important;color:#f4f4e9!important;border:1px solid #354637!important;border-radius:10px!important}
.stSelectbox div[data-baseweb="select"]{background:#111812;border-color:#354637}
div[data-testid="stChatMessage"]{background:#111812;border:1px solid #29382b;border-radius:15px}
[data-testid="stFileUploader"]{background:#111812;border:1px dashed #56654f;border-radius:15px;padding:10px}
hr{border-color:#28372c}
.sidebar-brand{font-size:23px;font-weight:800;letter-spacing:-.06em}
.sidebar-brand span{color:#c7ff5e}
.sidebar-caption{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.12em;color:#82917e}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

PAGES = ["Overview", "Field Twin", "Decision Lab", "AI Copilot", "Crop Clinic", "Connect Hardware"]
if "page" not in st.session_state:
    st.session_state.page = "Overview"

with st.sidebar:
    st.markdown('<div class="sidebar-brand">AGRI<span>//</span>NOVA</div><div class="sidebar-caption">INTELLIGENCE FOR EVERY ACRE</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("WORKSPACE")
    selected = st.radio("Navigation", PAGES, key="page", label_visibility="collapsed")
    st.markdown("---")
    st.caption("YOUR FIELD")
    crop = st.selectbox("Crop", ["Rice", "Cotton", "Chilli", "Maize", "Tomato"])
    soil = st.selectbox("Soil profile", ["Clay", "Red", "Black", "Sandy"])
    language = st.selectbox("Language / భాష", ["English", "Telugu", "Hindi", "Tamil", "Kannada"], key="ui_language")
    st.markdown("---")
    st.markdown('<div class="sidebar-caption">SYSTEM STATUS</div>', unsafe_allow_html=True)
    st.markdown('<span class="dot"></span>WEB APP ONLINE', unsafe_allow_html=True)
    st.caption("SENSOR FEED · DEMO")
    st.caption("AI ENGINE · " + ("API CONFIGURED" if os.getenv("GEMINI_API_KEY") else "KEY NOT SET"))

st.markdown('<div class="topline"><span>AGRI//NOVA &nbsp; / &nbsp; FIELD INTELLIGENCE</span><span><span class="dot"></span>PROTOTYPE ONLINE &nbsp; · &nbsp; 01.0</span></div>', unsafe_allow_html=True)

def chart_style(fig, height=300):
    fig.update_layout(height=height,margin=dict(l=0,r=0,t=20,b=0),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#b7c2b0",family="Manrope"),legend=dict(orientation="h",y=1.14,x=0,font=dict(size=10)),xaxis=dict(showgrid=False,zeroline=False),yaxis=dict(gridcolor="#27362a",zeroline=False))
    return fig

if selected == "Overview":
    st.markdown("""
    <div class="hero">
      <div class="hero-kicker">FIELD INTELLIGENCE SYSTEM &nbsp; / &nbsp; EARLY ACCESS</div>
      <div class="hero-title">Make every<br>acre <span style="color:#40591c">count.</span></div>
      <div class="hero-copy">One connected workspace for soil signals, crop observations and smarter farming decisions. Built to turn complex technology into simple actions for farmers.</div>
    </div>""",unsafe_allow_html=True)
    st.markdown('<div class="section-head"><h3>Field snapshot</h3><span class="micro">DEMO VALUES · NOT LIVE SENSOR DATA</span></div>',unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    for col,label,value,delta in [
        (a,"SOIL MOISTURE","68%","EXAMPLE READING"),
        (b,"AIR TEMPERATURE","28.4°","EXAMPLE READING"),
        (c,"AIR HUMIDITY","72%","EXAMPLE READING"),
        (d,"SOIL PH","6.8","EXAMPLE TEST"),
    ]:
        with col: st.metric(label,value,delta)
    left,right=st.columns([1.35,1],gap="large")
    with left:
        st.markdown('<div class="section-head"><h3>Field signals</h3><span class="micro">LAST 8 HOURS · SIMULATED</span></div>',unsafe_allow_html=True)
        times=["09","10","11","12","13","14","15","16"]
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=times,y=[62,65,66,72,74,69,67,68],name="Moisture %",mode="lines+markers",line=dict(color="#c7ff5e",width=3),fill="tozeroy",fillcolor="rgba(199,255,94,.07)"))
        fig.add_trace(go.Scatter(x=times,y=[25,26,28,30,29,28,27,28.4],name="Temp °C",mode="lines+markers",line=dict(color="#78c6ff",width=2)))
        st.plotly_chart(chart_style(fig,280),use_container_width=True)
        st.caption("Demo trend. Connect the sensor in the Hardware workspace to show real measurements.")
    with right:
        st.markdown('<div class="section-head"><h3>Decision brief</h3><span class="micro">RULE ENGINE</span></div>',unsafe_allow_html=True)
        st.markdown("""
        <div class="tile" style="min-height:240px">
          <div class="micro">01 / WATER MANAGEMENT</div>
          <div class="tile-value" style="font-size:25px;color:#c7ff5e">Observe before irrigating.</div>
          <div style="color:#bdc8b6;font-size:13px;line-height:1.8">The illustrative moisture value is above the demo threshold. Confirm root-zone moisture, crop stage and expected rainfall before deciding.</div>
          <hr><div class="tile-foot">REASON · DEMO MOISTURE ABOVE THRESHOLD</div>
        </div>""",unsafe_allow_html=True)
        st.markdown("")
        st.markdown(f'<div class="tile"><div class="tile-label">CURRENT FIELD PROFILE</div><div class="tile-value" style="font-size:23px">{crop} / {soil} soil</div><div class="tile-foot">LANGUAGE · {language.upper()}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-head"><h3>Explore the system</h3><span class="micro">CHOOSE YOUR NEXT MOVE</span></div>',unsafe_allow_html=True)
    cols=st.columns(3,gap="medium")
    features=[
        ("01","FIELD TWIN","Explore moisture zones across a simulated field.","Field Twin"),
        ("02","DECISION LAB","Compare irrigation choices and assumptions.","Decision Lab"),
        ("03","AI COPILOT","Ask practical questions in plain language.","AI Copilot"),
    ]
    for col,(num,title,desc,target) in zip(cols,features):
        with col:
            st.markdown(f'<div class="feature"><div class="feature-no">/ {num}</div><div class="feature-title">{title}</div><div class="feature-copy">{desc}</div></div>',unsafe_allow_html=True)
            if st.button(f"Open {title.lower()} ↗",key="go_"+num,use_container_width=True):
                st.session_state.page=target
                st.rerun()

elif selected == "Field Twin":
    st.markdown('<div class="hero"><div class="hero-kicker">01 / SPATIAL VIEW</div><div class="hero-title">Your field,<br><span style="color:#40591c">in signals.</span></div><div class="hero-copy">Explore simulated zones. In deployment, each zone can represent real measurements from sensors placed across the farm.</div></div>',unsafe_allow_html=True)
    st.warning("SIMULATION MODE — this is not GPS, satellite imagery or live sensor data.")
    level=st.slider("Set simulated field moisture",0,100,68)
    matrix=[]
    for r in range(6):
        matrix.append([max(0,min(100,level+((r*17+c*11)%31)-15)) for c in range(9)])
    fig=go.Figure(go.Heatmap(z=matrix,x=[f"Z{i+1}" for i in range(9)],y=[f"ROW {i+1}" for i in range(6)],colorscale=[[0,"#f07167"],[.3,"#f0bd5d"],[.58,"#719c42"],[1,"#c7ff5e"]],zmin=0,zmax=100,colorbar=dict(title="MOISTURE %",tickfont=dict(color="#bbc5b4"))))
    fig.update_layout(height=430,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#dfe8d8"),margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig,use_container_width=True)
    dry=sum(v<35 for row in matrix for v in row); watch=sum(35<=v<50 for row in matrix for v in row)
    x,y,z=st.columns(3); x.metric("DRY ZONES",dry); y.metric("MONITOR",watch); z.metric("FIELD CELLS",54)
    st.caption("A real deployment should show each sensor's timestamp and mark stale/offline readings clearly.")

elif selected == "Decision Lab":
    st.markdown('<div class="hero"><div class="hero-kicker">02 / SCENARIO ENGINE</div><div class="hero-title">Think it<br><span style="color:#40591c">through first.</span></div><div class="hero-copy">Explore how different assumptions change a simple irrigation estimate. This is a concept simulator, not a crop-specific scientific prediction.</div></div>',unsafe_allow_html=True)
    l,r=st.columns(2)
    with l:
        start=st.slider("Starting moisture (%)",0,100,42)
        amount=st.slider("Irrigation amount (demo units)",0,10,3)
    with r:
        hours=st.slider("Hours until next check",1,24,6)
        rain=st.selectbox("Rain scenario",["No rain","Light rain","Heavy rain"])
    bonus={"No rain":0,"Light rain":8,"Heavy rain":20}[rain]
    estimate=max(0,min(100,start+amount*4+bonus-hours*.7))
    x,y,z=st.columns(3); x.metric("START",f"{start}%"); y.metric("ESTIMATE",f"{estimate:.0f}%",f"{estimate-start:+.0f} pts"); z.metric("SCENARIO",rain)
    fig=go.Figure(go.Bar(x=["Current","After scenario"],y=[start,estimate],marker_color=["#78c6ff","#c7ff5e"],text=[f"{start}%",f"{estimate:.0f}%"],textposition="outside"))
    fig.update_layout(height=330,yaxis=dict(range=[0,112],gridcolor="#27362a",title="Illustrative moisture"),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#e4ecde"),margin=dict(l=0,r=0,t=25,b=0))
    st.plotly_chart(fig,use_container_width=True)
    st.info("Toy formula for demonstration only. Real soil-water changes depend on soil structure, crop stage, drainage, irrigation method and weather.")
    st.markdown("### Before acting")
    st.write("Confirm the physical sensor, check root-zone moisture, review a trusted local forecast, and use crop-specific advice.")

elif selected == "AI Copilot":
    st.markdown('<div class="hero"><div class="hero-kicker">03 / FARMER INTERFACE</div><div class="hero-title">Ask naturally.<br><span style="color:#40591c">Act clearly.</span></div><div class="hero-copy">A plain-language assistant concept for crop care. Live model answers require a configured Gemini API key.</div></div>',unsafe_allow_html=True)
    if not os.getenv("GEMINI_API_KEY"): st.info("Demo mode: no API key configured. Responses below are predefined examples, not live AI.")
    if "chat_history" not in st.session_state: st.session_state.chat_history=[]
    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]): st.markdown(item["content"])
    lang_codes = {"English":"en-IN", "Telugu":"te-IN", "Hindi":"hi-IN", "Tamil":"ta-IN", "Kannada":"kn-IN"}
    st.caption({"English":"Type a question or use the microphone.", "Telugu":"ప్రశ్న టైప్ చేయండి లేదా మైక్రోఫోన్ ఉపయోగించండి.", "Hindi":"प्रश्न लिखें या माइक्रोफ़ोन का उपयोग करें।", "Tamil":"கேள்வியைத் தட்டச்சு செய்யவும் அல்லது மைக்ரோஃபோனைப் பயன்படுத்தவும்.", "Kannada":"ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ ಅಥವಾ ಮೈಕ್ರೊಫೋನ್ ಬಳಸಿ."}[language])
    voice_text = speech_to_text(language=lang_codes[language], start_prompt="🎙️ Speak", stop_prompt="⏹️ Stop", just_once=True, key="voice_input")
    if voice_text:
        st.session_state["voice_question"] = voice_text
    with st.form("copilot_question_form", clear_on_submit=True):
        typed_prompt = st.text_input("Question", value=st.session_state.pop("voice_question", ""), placeholder="Ask about watering, yellow leaves, pests or soil...")
        send_question = st.form_submit_button("Send question")
    prompt = typed_prompt.strip() if send_question else None
    if prompt:
        st.session_state.chat_history.append({"role":"user","content":prompt})
        answer=""
        key=os.getenv("GEMINI_API_KEY")
        if key:
            try:
                from google import genai
                client=genai.Client(api_key=key)
                response=client.models.generate_content(model="gemini-2.5-flash",contents=f"You are a cautious farming assistant. Respond in {language}. Crop {crop}, soil {soil}. Give simple practical general advice, explain uncertainty, never invent live weather or prices, and recommend local agricultural experts for diagnosis or pesticide choices. Question: {prompt}")
                answer=response.text
            except Exception as exc: answer="AI connection failed. Verify the API key and model access. "+str(exc)[:160]
        else:
            q=prompt.lower()
            if language == "Telugu":
                if any(w in q for w in ["yellow", "pasupu", "పసుపు"]): answer=f"మీ {crop} పంటలో ఆకులు పసుపు రంగులోకి మారడానికి అధిక నీరు, పోషకాల లోపం, పురుగులు లేదా వ్యాధి కారణం కావచ్చు. పాత, కొత్త ఆకులను పరిశీలించండి. కారణం స్పష్టమయ్యే వరకు మందులు వాడకండి. ఇది ముందుగా సిద్ధం చేసిన డెమో సూచన మాత్రమే."
                elif any(w in q for w in ["water", "నీరు", "irrig"]): answer=f"మీ {crop} పంటకు నీరు పెట్టే ముందు వేర్ల దగ్గర నేల తేమ, పంట దశ, ఇటీవలి వర్షాన్ని పరిశీలించండి. ఈ డెమో నిజమైన పొలం పరిస్థితులను చూడలేదు."
                else: answer=f"మీ {crop} పంట వయస్సు, కనిపిస్తున్న లక్షణాలు, ఇటీవలి నీరు లేదా వర్షం గురించి చెప్పండి. ఇది ముందుగా సిద్ధం చేసిన డెమో సూచన మాత్రమే; ప్రత్యక్ష AI నిర్ధారణ కాదు."
            elif language == "Hindi":
                if "yellow" in q or "पीला" in q: answer=f"आपकी {crop} फसल की पीली पत्तियों का कारण अधिक पानी, पोषक तत्वों की कमी, कीट या रोग हो सकता है। पुरानी और नई पत्तियों की जाँच करें। कारण स्पष्ट होने तक रसायन न डालें। यह केवल डेमो सलाह है।"
                elif "water" in q or "पानी" in q or "irrig" in q: answer=f"{crop} में पानी देने से पहले जड़ों के पास मिट्टी की नमी, फसल की अवस्था और हाल की बारिश जाँचें। यह डेमो वास्तविक खेत की स्थिति नहीं देख सकता।"
                else: answer=f"अपनी {crop} फसल की उम्र, लक्षण और हाल की सिंचाई या बारिश बताएँ। यह पहले से तैयार डेमो सलाह है, लाइव निदान नहीं।"
            elif language == "Tamil":
                if "yellow" in q or "மஞ்சள்" in q: answer=f"உங்கள் {crop} பயிரின் இலைகள் மஞ்சளாக மாறுவதற்கு அதிக நீர், ஊட்டச்சத்து குறைபாடு, பூச்சி அல்லது நோய் காரணமாக இருக்கலாம். பழைய மற்றும் புதிய இலைகளைப் பாருங்கள். காரணம் தெளிவாகும் வரை ரசாயனங்களைப் பயன்படுத்த வேண்டாம். இது டெமோ ஆலோசனை மட்டுமே."
                elif "water" in q or "நீர்" in q or "irrig" in q: answer=f"{crop} பயிருக்கு நீர் பாய்ச்சுவதற்கு முன் வேர் பகுதி மண் ஈரப்பதம், பயிரின் வளர்ச்சி நிலை மற்றும் சமீபத்திய மழையைச் சரிபார்க்கவும். இது டெமோ மட்டுமே."
                else: answer=f"உங்கள் {crop} பயிரின் வயது, அறிகுறிகள் மற்றும் சமீபத்திய நீர்ப்பாசனம் அல்லது மழை பற்றி பகிரவும். இது முன்கூட்டியே அமைக்கப்பட்ட டெமோ ஆலோசனை."
            elif language == "Kannada":
                if "yellow" in q or "ಹಳದಿ" in q: answer=f"ನಿಮ್ಮ {crop} ಬೆಳೆಯ ಎಲೆಗಳು ಹಳದಿಯಾಗಲು ಹೆಚ್ಚು ನೀರು, ಪೋಷಕಾಂಶಗಳ ಕೊರತೆ, ಕೀಟಗಳು ಅಥವಾ ರೋಗ ಕಾರಣವಾಗಿರಬಹುದು. ಹಳೆಯ ಮತ್ತು ಹೊಸ ಎಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ. ಕಾರಣ ತಿಳಿಯುವವರೆಗೆ ರಾಸಾಯನಿಕಗಳನ್ನು ಬಳಸಬೇಡಿ. ಇದು ಡೆಮೋ ಸಲಹೆ ಮಾತ್ರ."
                elif "water" in q or "ನೀರು" in q or "irrig" in q: answer=f"{crop} ಬೆಳೆಗೆ ನೀರು ಹಾಕುವ ಮೊದಲು ಬೇರು ಭಾಗದ ಮಣ್ಣಿನ ತೇವಾಂಶ, ಬೆಳೆಯ ಹಂತ ಮತ್ತು ಇತ್ತೀಚಿನ ಮಳೆಯನ್ನು ಪರಿಶೀಲಿಸಿ. ಇದು ನೈಜ ಹೊಲದ ಸ್ಥಿತಿಯನ್ನು ನೋಡುವುದಿಲ್ಲ."
                else: answer=f"ನಿಮ್ಮ {crop} ಬೆಳೆಯ ವಯಸ್ಸು, ಲಕ್ಷಣಗಳು ಮತ್ತು ಇತ್ತೀಚಿನ ನೀರಾವರಿ ಅಥವಾ ಮಳೆಯ ಬಗ್ಗೆ ತಿಳಿಸಿ. ಇದು ಪೂರ್ವನಿರ್ಧರಿತ ಡೆಮೋ ಸಲಹೆ ಮಾತ್ರ."
            else:
                if "yellow" in q or "pasupu" in q: answer=f"Yellow leaves on {crop} may be caused by excess water, nutrient problems, pests or disease. Check old vs new leaves and inspect both sides. Avoid applying chemicals until the cause is clearer. This is predefined demo guidance, not a diagnosis."
                elif "water" in q or "irrig" in q: answer=f"For {crop} in {soil} soil, check root-zone moisture, crop stage and recent rainfall before watering. This demo cannot see actual field conditions."
                else: answer=f"To help with your {crop} crop, share its age, visible symptoms and recent watering or rainfall. This is predefined demo guidance, not a live diagnosis."
        st.session_state.chat_history.append({"role":"assistant","content":answer})
        st.rerun()

elif selected == "Crop Clinic":
    st.markdown('<div class="hero"><div class="hero-kicker">04 / CROP OBSERVATION</div><div class="hero-title">Look closer.<br><span style="color:#40591c">Know what to check.</span></div><div class="hero-copy">Organize field observations into a useful inspection checklist. Image-based disease diagnosis is not enabled in this version.</div></div>',unsafe_allow_html=True)
    photo=st.file_uploader("Add a crop photo",type=["jpg","jpeg","png"])
    if photo: st.image(photo,width=420)
    symptom=st.selectbox("Main symptom",["Yellow leaves","Brown spots","Wilting","Holes in leaves","Slow growth","Other"])
    stage=st.selectbox("Growth stage",["Seedling","Vegetative","Flowering","Fruiting / grain filling","Unknown"])
    if st.button("Build inspection checklist"):
        st.markdown("### Field checklist")
        st.write(f"**Crop:** {crop} · **Stage:** {stage} · **Symptom:** {symptom}")
        st.write("1. Check whether one plant or a wider area is affected.")
        st.write("2. Inspect the top and underside of leaves for insects and spots.")
        st.write("3. Review recent watering, rainfall and fertilizer use.")
        st.write("4. Photograph both the full plant and close-up symptoms.")
        st.warning("This is not a disease diagnosis. Confirm with a local agriculture specialist before chemical treatment.")

elif selected == "Connect Hardware":
    st.markdown('<div class="hero"><div class="hero-kicker">05 / EDGE DEVICE INTEGRATION</div><div class="hero-title">Bring the<br><span style="color:#40591c">real field online.</span></div><div class="hero-copy">Connect calibrated soil measurements to the interface and distinguish live values from demo values.</div></div>',unsafe_allow_html=True)
    st.markdown("### Proposed data path")
    st.code("Capacitive soil sensor → ESP32 ADC → Wi-Fi → authenticated endpoint → AGRI//NOVA dashboard",language="text")
    st.error("No physical sensor is connected in this version. Values are illustrative.")
    st.markdown("### Integration checklist")
    st.write("1. Read the sensor with a compatible ESP32 ADC input.")
    st.write("2. Calibrate dry and wet readings for the actual soil.")
    st.write("3. Send timestamped measurements through an authenticated endpoint.")
    st.write("4. Replace demo values and show a connection-lost state when data is stale.")
    st.warning("Never power a pump directly from a microcontroller GPIO. Use a suitable driver and safe power supply.")

st.markdown("---")
st.markdown('<div class="topline"><span>AGRI//NOVA — HACKATHON PROTOTYPE</span><span>SIMULATED VALUES ARE LABELLED · VERIFY BEFORE FIELD USE</span></div>',unsafe_allow_html=True)
