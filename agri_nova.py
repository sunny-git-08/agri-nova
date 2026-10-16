import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="AGRI//NOVA — Intelligence for Every Acre", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

# ── UI translations: all app pages use the selected language ───────────────────
LANGUAGES = {
    "English": {
        "nav":"Navigation","workspace":"WORKSPACE","field":"YOUR FIELD","crop":"Crop","soil":"Soil profile","language":"Language / భాష",
        "status":"SYSTEM STATUS","online":"WEB APP ONLINE","sensor_demo":"SENSOR FEED · DEMO","ai_config":"AI ENGINE",
        "Overview":"Overview","Field Twin":"Field Twin","Decision Lab":"Decision Lab","AI Copilot":"AI Copilot","Crop Clinic":"Crop Clinic","Connect Hardware":"Connect Hardware",
        "kicker":"FIELD INTELLIGENCE SYSTEM / EARLY ACCESS","hero_title":"Make every<br>acre <span style='color:#40591c'>count.</span>",
        "hero_copy":"One connected workspace for soil signals, crop observations and smarter farming decisions. Built to turn complex technology into simple actions for farmers.",
        "snapshot":"Field snapshot","demo_values":"DEMO VALUES · NOT LIVE SENSOR DATA","moisture":"SOIL MOISTURE","temperature":"AIR TEMPERATURE","humidity":"AIR HUMIDITY","ph":"SOIL PH","example":"EXAMPLE READING","example_test":"EXAMPLE TEST",
        "signals":"Field signals","simulated":"LAST 8 HOURS · SIMULATED","moisture_pct":"Moisture %","temp_c":"Temp °C","trend_caption":"Demo trend. Connect a sensor in the Hardware workspace to show real measurements.",
        "brief":"Decision brief","rule":"RULE ENGINE","water_management":"01 / WATER MANAGEMENT","observe":"Observe before irrigating.","brief_copy":"The illustrative moisture value is above the demo threshold. Confirm root-zone moisture, crop stage and expected rainfall before deciding.",
        "reason":"REASON · DEMO MOISTURE ABOVE THRESHOLD","profile":"CURRENT FIELD PROFILE","explore":"Explore the system","next_move":"CHOOSE YOUR NEXT MOVE",
        "feature_twin":"Explore moisture zones across a simulated field.","feature_lab":"Compare irrigation choices and assumptions.","feature_copilot":"Ask practical questions in plain language.","open":"Open",
        "field_kicker":"01 / SPATIAL VIEW","field_title":"Your field,<br><span style='color:#40591c'>in signals.</span>","field_copy":"Explore simulated zones. In deployment, each zone can represent real measurements from sensors placed across the farm.",
        "simulation_warning":"SIMULATION MODE — this is not GPS, satellite imagery or live sensor data.","set_moisture":"Set simulated field moisture","dry":"DRY ZONES","monitor":"MONITOR","cells":"FIELD CELLS","field_caption":"A real deployment should show each sensor's timestamp and mark stale/offline readings clearly.",
        "lab_kicker":"02 / SCENARIO ENGINE","lab_title":"Think it<br><span style='color:#40591c'>through first.</span>","lab_copy":"Explore how different assumptions change a simple irrigation estimate. This is a concept simulator, not a crop-specific scientific prediction.",
        "starting":"Starting moisture (%)","amount":"Irrigation amount (demo units)","hours":"Hours until next check","rain":"Rain scenario","no_rain":"No rain","light_rain":"Light rain","heavy_rain":"Heavy rain",
        "start":"START","estimate":"ESTIMATE","scenario":"SCENARIO","current":"Current","after":"After scenario","illustrative":"Illustrative moisture",
        "toy_warning":"Toy formula for demonstration only. Real soil-water changes depend on soil structure, crop stage, drainage, irrigation method and weather.",
        "before_acting":"Before acting","before_copy":"Confirm the physical sensor, check root-zone moisture, review a trusted local forecast, and use crop-specific advice.",
        "copilot_kicker":"03 / FARMER INTERFACE","copilot_title":"Ask naturally.<br><span style='color:#40591c'>Act clearly.</span>","copilot_copy":"A plain-language assistant concept for crop care. Live model answers require a configured Gemini API key.",
        "demo_mode":"Demo mode: no API key configured. Responses below are predefined examples, not live AI.","ask_voice":"Type a question or use the microphone.","speak":"🎙️ Speak","stop":"⏹️ Stop","question":"Question","placeholder":"Ask about watering, yellow leaves, pests or soil...","send":"Send question",
        "ai_failed":"AI connection failed. Verify the API key and model access.","clinic_kicker":"04 / CROP OBSERVATION","clinic_title":"Look closer.<br><span style='color:#40591c'>Know what to check.</span>",
        "clinic_copy":"Organize field observations into a useful inspection checklist. Image-based disease diagnosis is not enabled in this version.",
        "photo":"Add a crop photo","symptom":"Main symptom","yellow":"Yellow leaves","brown":"Brown spots","wilting":"Wilting","holes":"Holes in leaves","slow":"Slow growth","other":"Other",
        "stage":"Growth stage","seedling":"Seedling","vegetative":"Vegetative","flowering":"Flowering","fruiting":"Fruiting / grain filling","unknown":"Unknown",
        "build":"Build inspection checklist","checklist":"Field checklist","check1":"Check whether one plant or a wider area is affected.","check2":"Inspect the top and underside of leaves for insects and spots.",
        "check3":"Review recent watering, rainfall and fertilizer use.","check4":"Photograph both the full plant and close-up symptoms.",
        "not_diagnosis":"This is not a disease diagnosis. Confirm with a local agriculture specialist before chemical treatment.",
        "hardware_kicker":"05 / EDGE DEVICE INTEGRATION","hardware_title":"Bring the<br><span style='color:#40591c'>real field online.</span>",
        "hardware_copy":"Connect calibrated soil measurements to the interface and distinguish live values from demo values.",
        "data_path":"Proposed data path","no_sensor":"No physical sensor is connected in this version. Values are illustrative.","integration":"Integration checklist",
        "hw1":"Read the sensor with a compatible ESP32 ADC input.","hw2":"Calibrate dry and wet readings for the actual soil.",
        "hw3":"Send timestamped measurements through an authenticated endpoint.","hw4":"Replace demo values and show a connection-lost state when data is stale.",
        "pump_warning":"Never power a pump directly from a microcontroller GPIO. Use a suitable driver and safe power supply.",
        "footer1":"AGRI//NOVA — HACKATHON PROTOTYPE","footer2":"SIMULATED VALUES ARE LABELLED · VERIFY BEFORE FIELD USE",
        "yellow_answer":"Yellow leaves on {crop} may be caused by excess water, nutrient problems, pests or disease. Check old vs new leaves and inspect both sides. Avoid applying chemicals until the cause is clearer. This is predefined demo guidance, not a diagnosis.",
        "water_answer":"For {crop} in {soil} soil, check root-zone moisture, crop stage and recent rainfall before watering. This demo cannot see actual field conditions.",
        "general_answer":"To help with your {crop} crop, share its age, visible symptoms and recent watering or rainfall. This is predefined demo guidance, not a live diagnosis.",
    },
    "Telugu": {
        "nav":"నావిగేషన్","workspace":"పని విభాగం","field":"మీ పొలం","crop":"పంట","soil":"నేల రకం","language":"భాష",
        "status":"సిస్టమ్ స్థితి","online":"వెబ్ యాప్ ఆన్‌లైన్‌లో ఉంది","sensor_demo":"సెన్సార్ డేటా · డెమో","ai_config":"AI ఇంజిన్",
        "Overview":"అవలోకనం","Field Twin":"పొలం వీక్షణ","Decision Lab":"నిర్ణయ ప్రయోగశాల","AI Copilot":"AI సహాయకుడు","Crop Clinic":"పంట క్లినిక్","Connect Hardware":"హార్డ్‌వేర్ కనెక్షన్",
        "kicker":"వ్యవసాయ సమాచారం / ప్రారంభ వెర్షన్","hero_title":"ప్రతి<br>ఎకరానికీ <span style='color:#40591c'>విలువ ఇవ్వండి.</span>",
        "hero_copy":"నేల సమాచారం, పంట పరిశీలనలు, మెరుగైన వ్యవసాయ నిర్ణయాల కోసం ఒకే వేదిక. క్లిష్టమైన సాంకేతికతను రైతులకు సులభమైన చర్యలుగా మార్చేందుకు రూపొందించబడింది.",
        "snapshot":"పొలం సారాంశం","demo_values":"డెమో విలువలు · ప్రత్యక్ష సెన్సార్ డేటా కాదు","moisture":"నేల తేమ","temperature":"గాలి ఉష్ణోగ్రత","humidity":"గాలి తేమ","ph":"నేల pH","example":"ఉదాహరణ రీడింగ్","example_test":"ఉదాహరణ పరీక్ష",
        "signals":"పొలం సంకేతాలు","simulated":"గత 8 గంటలు · అనుకరణ డేటా","moisture_pct":"తేమ %","temp_c":"ఉష్ణోగ్రత °C","trend_caption":"ఇది డెమో ట్రెండ్. నిజమైన కొలతల కోసం హార్డ్‌వేర్ విభాగంలో సెన్సార్‌ను కనెక్ట్ చేయండి.",
        "brief":"నిర్ణయ సూచన","rule":"నియమాల ఆధారిత వ్యవస్థ","water_management":"01 / నీటి నిర్వహణ","observe":"నీరు పెట్టే ముందు పరిశీలించండి.","brief_copy":"డెమోలో చూపిన తేమ విలువ నిర్ణయించిన పరిమితి కంటే ఎక్కువగా ఉంది. నిర్ణయం తీసుకునే ముందు వేర్ల దగ్గర తేమ, పంట దశ, వర్ష సూచనను నిర్ధారించండి.",
        "reason":"కారణం · డెమో తేమ పరిమితి కంటే ఎక్కువ","profile":"ప్రస్తుత పొలం వివరాలు","explore":"వ్యవస్థను చూడండి","next_move":"తదుపరి ఎంపికను ఎంచుకోండి",
        "feature_twin":"అనుకరణ పొలంలోని తేమ ప్రాంతాలను చూడండి.","feature_lab":"నీటిపారుదల ఎంపికలను పోల్చండి.","feature_copilot":"సాధారణ భాషలో వ్యవసాయ ప్రశ్నలు అడగండి.","open":"తెరవండి",
        "field_kicker":"01 / ప్రాంతాల వీక్షణ","field_title":"మీ పొలం,<br><span style='color:#40591c'>సంకేతాల్లో.</span>","field_copy":"అనుకరణ తేమ ప్రాంతాలను పరిశీలించండి. నిజమైన అమలులో ప్రతి ప్రాంతం పొలంలోని సెన్సార్ కొలతలను చూపవచ్చు.",
        "simulation_warning":"అనుకరణ మాత్రమే — ఇది GPS, ఉపగ్రహ చిత్రం లేదా ప్రత్యక్ష సెన్సార్ డేటా కాదు.","set_moisture":"అనుకరణ పొలం తేమను ఎంచుకోండి","dry":"పొడి ప్రాంతాలు","monitor":"గమనించాల్సినవి","cells":"పొలం కణాలు","field_caption":"నిజమైన అమలులో ప్రతి సెన్సార్ సమయం చూపాలి; పాత లేదా ఆఫ్‌లైన్ డేటాను గుర్తించాలి.",
        "lab_kicker":"02 / పరిస్థితుల ప్రయోగం","lab_title":"ముందుగా<br><span style='color:#40591c'>ఆలోచించి నిర్ణయించండి.</span>","lab_copy":"వేర్వేరు అంచనాలు నీటిపారుదల అంచనాను ఎలా మార్చుతాయో చూడండి. ఇది నమూనా మాత్రమే; నిర్దిష్ట పంటకు శాస్త్రీయ అంచనా కాదు.",
        "starting":"ప్రారంభ తేమ (%)","amount":"నీటి పరిమాణం (డెమో యూనిట్లు)","hours":"తదుపరి పరిశీలనకు గంటలు","rain":"వర్ష పరిస్థితి","no_rain":"వర్షం లేదు","light_rain":"తేలికపాటి వర్షం","heavy_rain":"భారీ వర్షం",
        "start":"ప్రారంభం","estimate":"అంచనా","scenario":"పరిస్థితి","current":"ప్రస్తుతం","after":"పరిస్థితి తర్వాత","illustrative":"ఉదాహరణ తేమ",
        "toy_warning":"ఇది ప్రదర్శన కోసం మాత్రమే. నేల స్వభావం, పంట దశ, నీటి పారుదల, పద్ధతి, వాతావరణంపై నిజమైన తేమ మార్పులు ఆధారపడతాయి.",
        "before_acting":"చర్యకు ముందు","before_copy":"సెన్సార్‌ను నిర్ధారించండి, వేర్ల దగ్గర తేమను పరిశీలించండి, నమ్మదగిన స్థానిక వాతావరణ సూచన చూడండి, పంటకు సరిపోయే సలహా తీసుకోండి.",
        "copilot_kicker":"03 / రైతు సహాయక వేదిక","copilot_title":"సహజంగా అడగండి.<br><span style='color:#40591c'>స్పష్టంగా చర్య తీసుకోండి.</span>","copilot_copy":"పంట సంరక్షణ కోసం సాధారణ భాషలో సహాయక నమూనా. ప్రత్యక్ష AI సమాధానాలకు Gemini API కీ అవసరం.",
        "demo_mode":"డెమో మోడ్: API కీ లేదు. క్రింది సమాధానాలు ముందుగా సిద్ధం చేసినవి; ప్రత్యక్ష AI కాదు.","ask_voice":"ప్రశ్న టైప్ చేయండి లేదా మైక్రోఫోన్ ఉపయోగించండి.","speak":"🎙️ మాట్లాడండి","stop":"⏹️ ఆపండి","question":"ప్రశ్న","placeholder":"నీరు, పసుపు ఆకులు, పురుగులు లేదా నేల గురించి అడగండి...","send":"ప్రశ్న పంపండి",
        "ai_failed":"AI కనెక్షన్ విఫలమైంది. API కీ, మోడల్ అనుమతులను తనిఖీ చేయండి.","clinic_kicker":"04 / పంట పరిశీలన","clinic_title":"జాగ్రత్తగా చూడండి.<br><span style='color:#40591c'>ఏమి పరిశీలించాలో తెలుసుకోండి.</span>",
        "clinic_copy":"పొలంలో గమనించిన విషయాలను పరిశీలన జాబితాగా మార్చండి. ఈ వెర్షన్‌లో చిత్రాల ఆధారిత వ్యాధి నిర్ధారణ లేదు.",
        "photo":"పంట ఫోటో జోడించండి","symptom":"ప్రధాన లక్షణం","yellow":"పసుపు ఆకులు","brown":"గోధుమ మచ్చలు","wilting":"వాడిపోవడం","holes":"ఆకుల్లో రంధ్రాలు","slow":"నెమ్మదిగా పెరుగుదల","other":"ఇతర",
        "stage":"పంట ఎదుగుదల దశ","seedling":"మొలక దశ","vegetative":"ఆకు/కొమ్మల పెరుగుదల","flowering":"పూత దశ","fruiting":"కాయ / గింజ నింపే దశ","unknown":"తెలియదు",
        "build":"పరిశీలన జాబితా తయారు చేయండి","checklist":"పొలం పరిశీలన జాబితా","check1":"ఒక మొక్క మాత్రమేనా లేదా పెద్ద ప్రాంతమా ప్రభావితమైందో చూడండి.","check2":"ఆకుల పైభాగం, కిందభాగంలో పురుగులు మరియు మచ్చలు చూడండి.",
        "check3":"ఇటీవలి నీరు, వర్షం, ఎరువుల వినియోగాన్ని పరిశీలించండి.","check4":"మొక్క మొత్తం ఫోటోతో పాటు లక్షణాల దగ్గరి ఫోటో తీయండి.",
        "not_diagnosis":"ఇది వ్యాధి నిర్ధారణ కాదు. రసాయనాలు వాడే ముందు స్థానిక వ్యవసాయ నిపుణుడిని సంప్రదించండి.",
        "hardware_kicker":"05 / పరికరాల అనుసంధానం","hardware_title":"నిజమైన<br><span style='color:#40591c'>పొలాన్ని ఆన్‌లైన్‌లోకి తీసుకురండి.</span>",
        "hardware_copy":"కాలిబ్రేట్ చేసిన నేల కొలతలను ఇంటర్‌ఫేస్‌కు అనుసంధానించి, ప్రత్యక్ష విలువలను డెమో విలువల నుంచి వేరు చేయండి.",
        "data_path":"ప్రతిపాదిత డేటా మార్గం","no_sensor":"ఈ వెర్షన్‌లో భౌతిక సెన్సార్ కనెక్ట్ కాలేదు. విలువలు ఉదాహరణ మాత్రమే.","integration":"అనుసంధాన చెక్‌లిస్ట్",
        "hw1":"అనుకూల ESP32 ADC ఇన్‌పుట్‌తో సెన్సార్ చదవండి.","hw2":"నిజమైన నేలలో పొడి, తడి రీడింగ్‌లను కాలిబ్రేట్ చేయండి.",
        "hw3":"ధృవీకరించిన ఎండ్‌పాయింట్ ద్వారా సమయంతో కూడిన కొలతలను పంపండి.","hw4":"డెమో విలువలను మార్చి, పాత డేటా వచ్చినప్పుడు కనెక్షన్ కోల్పోయినట్లు చూపండి.",
        "pump_warning":"మైక్రోకంట్రోలర్ GPIO నుంచి పంపును నేరుగా నడపవద్దు. సరైన డ్రైవర్, సురక్షిత విద్యుత్ సరఫరా ఉపయోగించండి.",
        "footer1":"AGRI//NOVA — హ్యాకథాన్ నమూనా","footer2":"అనుకరణ విలువలు గుర్తించబడ్డాయి · పొలంలో ఉపయోగించే ముందు నిర్ధారించండి",
        "yellow_answer":"మీ {crop} పంటలో ఆకులు పసుపు రంగులోకి మారడానికి అధిక నీరు, పోషకాల లోపం, పురుగులు లేదా వ్యాధి కారణం కావచ్చు. పాత, కొత్త ఆకులను పరిశీలించండి. కారణం స్పష్టమయ్యే వరకు రసాయనాలు వాడకండి. ఇది డెమో సూచన మాత్రమే.",
        "water_answer":"మీ {crop} పంటకు నీరు పెట్టే ముందు వేర్ల దగ్గర నేల తేమ, పంట దశ, ఇటీవలి వర్షాన్ని పరిశీలించండి. ఈ డెమో నిజమైన పొలం పరిస్థితులను చూడలేదు.",
        "general_answer":"మీ {crop} పంటకు సహాయం చేయడానికి పంట వయస్సు, కనిపిస్తున్న లక్షణాలు, ఇటీవలి నీరు లేదా వర్షం గురించి చెప్పండి. ఇది డెమో సూచన మాత్రమే.",
    }
}
# Additional languages reuse complete navigation plus translated key labels; untranslated values safely fall back to English.
LANGUAGES["Hindi"] = {**LANGUAGES["English"], **{
    "nav":"नेविगेशन","workspace":"कार्य क्षेत्र","field":"आपका खेत","crop":"फसल","soil":"मिट्टी का प्रकार","language":"भाषा","status":"सिस्टम स्थिति","online":"वेब ऐप ऑनलाइन","sensor_demo":"सेंसर डेटा · डेमो",
    "Overview":"अवलोकन","Field Twin":"खेत दृश्य","Decision Lab":"निर्णय प्रयोगशाला","AI Copilot":"AI सहायक","Crop Clinic":"फसल क्लिनिक","Connect Hardware":"हार्डवेयर जोड़ें",
    "snapshot":"खेत का सारांश","demo_values":"डेमो मान · लाइव सेंसर डेटा नहीं","moisture":"मिट्टी की नमी","temperature":"हवा का तापमान","humidity":"हवा की नमी","ph":"मिट्टी का pH","signals":"खेत संकेत","brief":"निर्णय सारांश",
    "observe":"सिंचाई से पहले जाँचें।","set_moisture":"डेमो खेत की नमी चुनें","dry":"सूखे क्षेत्र","monitor":"निगरानी","cells":"खेत के सेल",
    "starting":"शुरुआती नमी (%)","amount":"सिंचाई मात्रा (डेमो इकाई)","hours":"अगली जाँच तक घंटे","rain":"बारिश की स्थिति","no_rain":"बारिश नहीं","light_rain":"हल्की बारिश","heavy_rain":"तेज़ बारिश",
    "ask_voice":"प्रश्न लिखें या माइक्रोफ़ोन का उपयोग करें।","question":"प्रश्न","placeholder":"पानी, पीली पत्तियों, कीट या मिट्टी के बारे में पूछें...","send":"प्रश्न भेजें",
    "photo":"फसल की तस्वीर जोड़ें","symptom":"मुख्य लक्षण","yellow":"पीली पत्तियाँ","brown":"भूरे धब्बे","wilting":"मुरझाना","holes":"पत्तियों में छेद","slow":"धीमी वृद्धि","other":"अन्य",
    "stage":"विकास अवस्था","seedling":"अंकुर","vegetative":"विकास","flowering":"फूल आना","fruiting":"फल / दाना भरना","unknown":"अज्ञात","build":"निरीक्षण सूची बनाएँ","checklist":"खेत निरीक्षण सूची",
    "not_diagnosis":"यह रोग का निदान नहीं है। रसायन इस्तेमाल करने से पहले स्थानीय कृषि विशेषज्ञ से सलाह लें.",
    "no_sensor":"इस संस्करण में कोई भौतिक सेंसर जुड़ा नहीं है। मान केवल उदाहरण हैं।","integration":"एकीकरण चेकलिस्ट",
    "yellow_answer":"आपकी {crop} फसल की पीली पत्तियों का कारण अधिक पानी, पोषक तत्वों की कमी, कीट या रोग हो सकता है। पुरानी और नई पत्तियों की जाँच करें। कारण स्पष्ट होने तक रसायन न डालें। यह केवल डेमो सलाह है।",
    "water_answer":"{crop} में पानी देने से पहले जड़ों के पास मिट्टी की नमी, फसल की अवस्था और हाल की बारिश जाँचें। यह डेमो वास्तविक खेत की स्थिति नहीं देख सकता।",
    "general_answer":"अपनी {crop} फसल की उम्र, लक्षण और हाल की सिंचाई या बारिश बताएँ। यह डेमो सलाह है, लाइव निदान नहीं।"
}}
LANGUAGES["Tamil"] = {**LANGUAGES["English"], **{
    "nav":"வழிசெலுத்தல்","workspace":"பணியிடம்","field":"உங்கள் வயல்","crop":"பயிர்","soil":"மண் வகை","language":"மொழி","status":"அமைப்பு நிலை","online":"வலைச் செயலி ஆன்லைனில்",
    "Overview":"கண்ணோட்டம்","Field Twin":"வயல் காட்சி","Decision Lab":"முடிவு ஆய்வகம்","AI Copilot":"AI உதவியாளர்","Crop Clinic":"பயிர் மருத்துவமனை","Connect Hardware":"கருவியை இணைக்கவும்",
    "snapshot":"வயல் சுருக்கம்","demo_values":"டெமோ மதிப்புகள் · நேரடி சென்சார் தரவு அல்ல","moisture":"மண் ஈரப்பதம்","temperature":"காற்று வெப்பநிலை","humidity":"காற்று ஈரப்பதம்","ph":"மண் pH",
    "set_moisture":"டெமோ வயல் ஈரப்பதத்தை அமைக்கவும்","dry":"உலர் பகுதிகள்","monitor":"கண்காணிப்பு","cells":"வயல் பகுதிகள்",
    "starting":"தொடக்க ஈரப்பதம் (%)","amount":"நீர்ப்பாசன அளவு (டெமோ அலகுகள்)","hours":"அடுத்த சோதனைக்கான மணிநேரம்","rain":"மழை நிலை","no_rain":"மழை இல்லை","light_rain":"லேசான மழை","heavy_rain":"கனமழை",
    "ask_voice":"கேள்வியைத் தட்டச்சு செய்யவும் அல்லது மைக்ரோஃபோனைப் பயன்படுத்தவும்.","question":"கேள்வி","placeholder":"நீர்ப்பாசனம், மஞ்சள் இலைகள், பூச்சிகள் அல்லது மண் பற்றி கேளுங்கள்...","send":"கேள்வியை அனுப்பு",
    "photo":"பயிர் படத்தைச் சேர்க்கவும்","symptom":"முக்கிய அறிகுறி","yellow":"மஞ்சள் இலைகள்","brown":"பழுப்பு புள்ளிகள்","wilting":"வாடுதல்","holes":"இலைகளில் துளைகள்","slow":"மெதுவான வளர்ச்சி","other":"மற்றவை",
    "stage":"வளர்ச்சி நிலை","seedling":"நாற்று","vegetative":"வளர்ச்சி","flowering":"பூக்கும் நிலை","fruiting":"காய் / தானியம் நிரம்புதல்","unknown":"தெரியவில்லை","build":"ஆய்வு பட்டியலை உருவாக்கு","checklist":"வயல் ஆய்வு பட்டியல்",
    "no_sensor":"இந்த பதிப்பில் உண்மையான சென்சார் இணைக்கப்படவில்லை. மதிப்புகள் எடுத்துக்காட்டுகள் மட்டுமே.",
    "yellow_answer":"உங்கள் {crop} பயிரின் இலைகள் மஞ்சளாக மாறுவதற்கு அதிக நீர், ஊட்டச்சத்து குறைபாடு, பூச்சி அல்லது நோய் காரணமாக இருக்கலாம். பழைய மற்றும் புதிய இலைகளைப் பாருங்கள். இது டெமோ ஆலோசனை மட்டுமே.",
    "water_answer":"{crop} பயிருக்கு நீர் பாய்ச்சுவதற்கு முன் வேர் பகுதி மண் ஈரப்பதம், பயிரின் வளர்ச்சி நிலை மற்றும் சமீபத்திய மழையைச் சரிபார்க்கவும். இது டெமோ மட்டுமே.",
    "general_answer":"உங்கள் {crop} பயிரின் வயது, அறிகுறிகள் மற்றும் சமீபத்திய நீர்ப்பாசனம் அல்லது மழை பற்றி பகிரவும். இது டெமோ ஆலோசனை மட்டுமே."
}}
LANGUAGES["Kannada"] = {**LANGUAGES["English"], **{
    "nav":"ನ್ಯಾವಿಗೇಶನ್","workspace":"ಕಾರ್ಯಸ್ಥಳ","field":"ನಿಮ್ಮ ಹೊಲ","crop":"ಬೆಳೆ","soil":"ಮಣ್ಣಿನ ವಿಧ","language":"ಭಾಷೆ","status":"ವ್ಯವಸ್ಥೆಯ ಸ್ಥಿತಿ","online":"ವೆಬ್ ಆಪ್ ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ",
    "Overview":"ಅವಲೋಕನ","Field Twin":"ಹೊಲದ ನೋಟ","Decision Lab":"ನಿರ್ಧಾರ ಪ್ರಯೋಗಾಲಯ","AI Copilot":"AI ಸಹಾಯಕ","Crop Clinic":"ಬೆಳೆ ಕ್ಲಿನಿಕ್","Connect Hardware":"ಹಾರ್ಡ್‌ವೇರ್ ಸಂಪರ್ಕಿಸಿ",
    "snapshot":"ಹೊಲದ ಸಾರಾಂಶ","demo_values":"ಡೆಮೋ ಮೌಲ್ಯಗಳು · ನೈಜ ಸೆನ್ಸರ್ ಡೇಟಾ ಅಲ್ಲ","moisture":"ಮಣ್ಣಿನ ತೇವಾಂಶ","temperature":"ಗಾಳಿಯ ತಾಪಮಾನ","humidity":"ಗಾಳಿಯ ತೇವಾಂಶ","ph":"ಮಣ್ಣಿನ pH",
    "set_moisture":"ಡೆಮೋ ಹೊಲದ ತೇವಾಂಶ ಆಯ್ಕೆಮಾಡಿ","dry":"ಒಣ ಪ್ರದೇಶಗಳು","monitor":"ಗಮನಿಸಿ","cells":"ಹೊಲದ ಕೋಶಗಳು",
    "starting":"ಆರಂಭಿಕ ತೇವಾಂಶ (%)","amount":"ನೀರಾವರಿ ಪ್ರಮಾಣ (ಡೆಮೋ ಘಟಕಗಳು)","hours":"ಮುಂದಿನ ಪರಿಶೀಲನೆಗೆ ಗಂಟೆಗಳು","rain":"ಮಳೆಯ ಸ್ಥಿತಿ","no_rain":"ಮಳೆ ಇಲ್ಲ","light_rain":"ಲಘು ಮಳೆ","heavy_rain":"ಭಾರೀ ಮಳೆ",
    "ask_voice":"ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ ಅಥವಾ ಮೈಕ್ರೊಫೋನ್ ಬಳಸಿ.","question":"ಪ್ರಶ್ನೆ","placeholder":"ನೀರು, ಹಳದಿ ಎಲೆಗಳು, ಕೀಟಗಳು ಅಥವಾ ಮಣ್ಣಿನ ಬಗ್ಗೆ ಕೇಳಿ...","send":"ಪ್ರಶ್ನೆ ಕಳುಹಿಸಿ",
    "photo":"ಬೆಳೆ ಫೋಟೋ ಸೇರಿಸಿ","symptom":"ಮುಖ್ಯ ಲಕ್ಷಣ","yellow":"ಹಳದಿ ಎಲೆಗಳು","brown":"ಕಂದು ಕಲೆಗಳು","wilting":"ಬಾಡುವುದು","holes":"ಎಲೆಗಳಲ್ಲಿ ರಂಧ್ರಗಳು","slow":"ನಿಧಾನ ಬೆಳವಣಿಗೆ","other":"ಇತರೆ",
    "stage":"ಬೆಳವಣಿಗೆಯ ಹಂತ","seedling":"ಸಸಿ","vegetative":"ಬೆಳವಣಿಗೆ","flowering":"ಹೂ ಬಿಡುವ ಹಂತ","fruiting":"ಹಣ್ಣು / ಧಾನ್ಯ ತುಂಬುವ ಹಂತ","unknown":"ಗೊತ್ತಿಲ್ಲ","build":"ಪರಿಶೀಲನಾ ಪಟ್ಟಿ ರಚಿಸಿ","checklist":"ಹೊಲ ಪರಿಶೀಲನಾ ಪಟ್ಟಿ",
    "no_sensor":"ಈ ಆವೃತ್ತಿಯಲ್ಲಿ ನೈಜ ಸೆನ್ಸರ್ ಸಂಪರ್ಕಗೊಂಡಿಲ್ಲ. ಮೌಲ್ಯಗಳು ಉದಾಹರಣೆ ಮಾತ್ರ.",
    "yellow_answer":"ನಿಮ್ಮ {crop} ಬೆಳೆಯ ಎಲೆಗಳು ಹಳದಿಯಾಗಲು ಹೆಚ್ಚು ನೀರು, ಪೋಷಕಾಂಶಗಳ ಕೊರತೆ, ಕೀಟಗಳು ಅಥವಾ ರೋಗ ಕಾರಣವಾಗಿರಬಹುದು. ಹಳೆಯ ಮತ್ತು ಹೊಸ ಎಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ. ಇದು ಡೆಮೋ ಸಲಹೆ ಮಾತ್ರ.",
    "water_answer":"{crop} ಬೆಳೆಗೆ ನೀರು ಹಾಕುವ ಮೊದಲು ಬೇರು ಭಾಗದ ಮಣ್ಣಿನ ತೇವಾಂಶ, ಬೆಳೆಯ ಹಂತ ಮತ್ತು ಇತ್ತೀಚಿನ ಮಳೆಯನ್ನು ಪರಿಶೀಲಿಸಿ. ಇದು ಡೆಮೋ ಮಾತ್ರ.",
    "general_answer":"ನಿಮ್ಮ {crop} ಬೆಳೆಯ ವಯಸ್ಸು, ಲಕ್ಷಣಗಳು ಮತ್ತು ಇತ್ತೀಚಿನ ನೀರಾವರಿ ಅಥವಾ ಮಳೆಯ ಬಗ್ಗೆ ತಿಳಿಸಿ. ಇದು ಡೆಮೋ ಸಲಹೆ ಮಾತ್ರ."
}}

def T(key):
    return LANGUAGES.get(language, LANGUAGES["English"]).get(key, LANGUAGES["English"].get(key, key))

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

# Language selector is first so the chosen dictionary is active for the whole app.
if "ui_language" not in st.session_state:
    st.session_state.ui_language = "English"
language = st.session_state.ui_language
PAGES = ["Overview", "Field Twin", "Decision Lab", "AI Copilot", "Crop Clinic", "Connect Hardware"]

with st.sidebar:
    st.markdown('<div class="sidebar-brand">AGRI<span>//</span>NOVA</div><div class="sidebar-caption">INTELLIGENCE FOR EVERY ACRE</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption(T("workspace"))
    selected = st.radio(T("nav"), PAGES, format_func=lambda p: T(p), key="page", label_visibility="collapsed")
    st.markdown("---")
    st.caption(T("field"))
    crop = st.selectbox(T("crop"), ["Rice", "Cotton", "Chilli", "Maize", "Tomato"])
    soil = st.selectbox(T("soil"), ["Clay", "Red", "Black", "Sandy"])
    language = st.selectbox(T("language"), ["English", "Telugu", "Hindi", "Tamil", "Kannada"], key="ui_language")
    st.markdown("---")
    st.markdown(f'<div class="sidebar-caption">{T("status")}</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="dot"></span>{T("online")}', unsafe_allow_html=True)
    st.caption(T("sensor_demo"))
    st.caption(f'{T("ai_config")} · ' + ("API CONFIGURED" if os.getenv("GEMINI_API_KEY") else "KEY NOT SET"))

def hero(kicker, title, copy):
    st.markdown(f'<div class="hero"><div class="hero-kicker">{kicker}</div><div class="hero-title">{title}</div><div class="hero-copy">{copy}</div></div>', unsafe_allow_html=True)

def chart_style(fig, height=300):
    fig.update_layout(height=height, margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#b7c2b0",family="Manrope"), legend=dict(orientation="h",y=1.14,x=0,font=dict(size=10)), xaxis=dict(showgrid=False,zeroline=False), yaxis=dict(gridcolor="#27362a",zeroline=False))
    return fig

st.markdown(f'<div class="topline"><span>AGRI//NOVA &nbsp; / &nbsp; {T("kicker")}</span><span><span class="dot"></span>PROTOTYPE ONLINE &nbsp; · &nbsp; 01.0</span></div>', unsafe_allow_html=True)

if selected == "Overview":
    hero(T("kicker"), T("hero_title"), T("hero_copy"))
    st.markdown(f'<div class="section-head"><h3>{T("snapshot")}</h3><span class="micro">{T("demo_values")}</span></div>', unsafe_allow_html=True)
    a,b,c,d = st.columns(4)
    for col,label,value,delta in [(a,T("moisture"),"68%",T("example")),(b,T("temperature"),"28.4°",T("example")),(c,T("humidity"),"72%",T("example")),(d,T("ph"),"6.8",T("example_test"))]:
        with col: st.metric(label,value,delta)
    left,right = st.columns([1.35,1],gap="large")
    with left:
        st.markdown(f'<div class="section-head"><h3>{T("signals")}</h3><span class="micro">{T("simulated")}</span></div>',unsafe_allow_html=True)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=["09","10","11","12","13","14","15","16"],y=[62,65,66,72,74,69,67,68],name=T("moisture_pct"),mode="lines+markers",line=dict(color="#c7ff5e",width=3),fill="tozeroy",fillcolor="rgba(199,255,94,.07)"))
        fig.add_trace(go.Scatter(x=["09","10","11","12","13","14","15","16"],y=[25,26,28,30,29,28,27,28.4],name=T("temp_c"),mode="lines+markers",line=dict(color="#78c6ff",width=2)))
        st.plotly_chart(chart_style(fig,280),width="stretch")
        st.caption(T("trend_caption"))
    with right:
        st.markdown(f'<div class="section-head"><h3>{T("brief")}</h3><span class="micro">{T("rule")}</span></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="tile" style="min-height:240px"><div class="micro">{T("water_management")}</div><div class="tile-value" style="font-size:25px;color:#c7ff5e">{T("observe")}</div><div style="color:#bdc8b6;font-size:13px;line-height:1.8">{T("brief_copy")}</div><hr><div class="tile-foot">{T("reason")}</div></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="tile"><div class="tile-label">{T("profile")}</div><div class="tile-value" style="font-size:23px">{crop} / {soil}</div><div class="tile-foot">{T("language")} · {language.upper()}</div></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-head"><h3>{T("explore")}</h3><span class="micro">{T("next_move")}</span></div>',unsafe_allow_html=True)
    cols=st.columns(3,gap="medium")
    features=[("01","FIELD TWIN",T("feature_twin"),"Field Twin"),("02","DECISION LAB",T("feature_lab"),"Decision Lab"),("03","AI COPILOT",T("feature_copilot"),"AI Copilot")]
    for col,(num,title,desc,target) in zip(cols,features):
        with col:
            st.markdown(f'<div class="feature"><div class="feature-no">/ {num}</div><div class="feature-title">{T(target)}</div><div class="feature-copy">{desc}</div></div>',unsafe_allow_html=True)
            if st.button(f'{T("open")} {T(target)} ↗',key="go_"+num,width="stretch"):
                st.session_state.page=target
                st.rerun()

elif selected == "Field Twin":
    hero(T("field_kicker"),T("field_title"),T("field_copy"))
    st.warning(T("simulation_warning"))
    level=st.slider(T("set_moisture"),0,100,68)
    matrix=[[max(0,min(100,level+((r*17+c*11)%31)-15)) for c in range(9)] for r in range(6)]
    fig=go.Figure(go.Heatmap(z=matrix,x=[f"Z{i+1}" for i in range(9)],y=[f"ROW {i+1}" for i in range(6)],colorscale=[[0,"#f07167"],[.3,"#f0bd5d"],[.58,"#719c42"],[1,"#c7ff5e"]],zmin=0,zmax=100,colorbar=dict(title=T("moisture_pct"),tickfont=dict(color="#bbc5b4"))))
    fig.update_layout(height=430,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#dfe8d8"),margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig,width="stretch")
    dry=sum(v<35 for row in matrix for v in row); watch=sum(35<=v<50 for row in matrix for v in row)
    x,y,z=st.columns(3); x.metric(T("dry"),dry); y.metric(T("monitor"),watch); z.metric(T("cells"),54)
    st.caption(T("field_caption"))

elif selected == "Decision Lab":
    hero(T("lab_kicker"),T("lab_title"),T("lab_copy"))
    l,r=st.columns(2)
    with l:
        start=st.slider(T("starting"),0,100,42)
        amount=st.slider(T("amount"),0,10,3)
    with r:
        hours=st.slider(T("hours"),1,24,6)
        rain=st.selectbox(T("rain"),[T("no_rain"),T("light_rain"),T("heavy_rain")])
    bonus={T("no_rain"):0,T("light_rain"):8,T("heavy_rain"):20}[rain]
    estimate=max(0,min(100,start+amount*4+bonus-hours*.7))
    x,y,z=st.columns(3); x.metric(T("start"),f"{start}%"); y.metric(T("estimate"),f"{estimate:.0f}%",f"{estimate-start:+.0f} pts"); z.metric(T("scenario"),rain)
    fig=go.Figure(go.Bar(x=[T("current"),T("after")],y=[start,estimate],marker_color=["#78c6ff","#c7ff5e"],text=[f"{start}%",f"{estimate:.0f}%"],textposition="outside"))
    fig.update_layout(height=330,yaxis=dict(range=[0,112],gridcolor="#27362a",title=T("illustrative")),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#e4ecde"),margin=dict(l=0,r=0,t=25,b=0))
    st.plotly_chart(fig,width="stretch")
    st.info(T("toy_warning"))
    st.markdown("### "+T("before_acting"))
    st.write(T("before_copy"))

elif selected == "AI Copilot":
    hero(T("copilot_kicker"),T("copilot_title"),T("copilot_copy"))
    if not os.getenv("GEMINI_API_KEY"): st.info(T("demo_mode"))
    if "chat_history" not in st.session_state: st.session_state.chat_history=[]
    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]): st.markdown(item["content"])
    lang_codes={"English":"en-IN","Telugu":"te-IN","Hindi":"hi-IN","Tamil":"ta-IN","Kannada":"kn-IN"}
    st.caption(T("ask_voice"))
    voice_text=speech_to_text(language=lang_codes[language],start_prompt=T("speak"),stop_prompt=T("stop"),just_once=True,key="voice_input")
    if voice_text: st.session_state["voice_question"]=voice_text
    with st.form("copilot_question_form",clear_on_submit=True):
        typed_prompt=st.text_input(T("question"),value=st.session_state.pop("voice_question",""),placeholder=T("placeholder"))
        send_question=st.form_submit_button(T("send"))
    prompt=typed_prompt.strip() if send_question else None
    if prompt:
        st.session_state.chat_history.append({"role":"user","content":prompt})
        answer=""
        key=os.getenv("GEMINI_API_KEY")
        if key:
            try:
                from google import genai
                client=genai.Client(api_key=key)
                response=client.models.generate_content(model="gemini-2.5-flash",contents=f"You are a cautious farming assistant. Respond in {language}. Crop {crop}, soil {soil}. Give simple practical general advice, explain uncertainty, never invent live weather or prices, and recommend local agricultural experts for diagnosis or pesticide choices. Question: {prompt}")
                answer=response.text or T("general_answer").format(crop=crop)
            except Exception as exc: answer=T("ai_failed")+" "+str(exc)[:120]
        else:
            q=prompt.lower()
            if language=="Telugu":
                if any(w in q for w in ["yellow","pasupu","పసుపు"]): answer=T("yellow_answer").format(crop=crop)
                elif any(w in q for w in ["water","నీరు","irrig"]): answer=T("water_answer").format(crop=crop,soil=soil)
                else: answer=T("general_answer").format(crop=crop)
            elif language=="Hindi":
                if any(w in q for w in ["yellow","पीला"]): answer=T("yellow_answer").format(crop=crop)
                elif any(w in q for w in ["water","पानी","irrig"]): answer=T("water_answer").format(crop=crop,soil=soil)
                else: answer=T("general_answer").format(crop=crop)
            elif language=="Tamil":
                if any(w in q for w in ["yellow","மஞ்சள்"]): answer=T("yellow_answer").format(crop=crop)
                elif any(w in q for w in ["water","நீர்","irrig"]): answer=T("water_answer").format(crop=crop,soil=soil)
                else: answer=T("general_answer").format(crop=crop)
            elif language=="Kannada":
                if any(w in q for w in ["yellow","ಹಳದಿ"]): answer=T("yellow_answer").format(crop=crop)
                elif any(w in q for w in ["water","ನೀರು","irrig"]): answer=T("water_answer").format(crop=crop,soil=soil)
                else: answer=T("general_answer").format(crop=crop)
            else:
                if "yellow" in q or "pasupu" in q: answer=T("yellow_answer").format(crop=crop)
                elif "water" in q or "irrig" in q: answer=T("water_answer").format(crop=crop,soil=soil)
                else: answer=T("general_answer").format(crop=crop)
        st.session_state.chat_history.append({"role":"assistant","content":answer})
        st.rerun()

elif selected == "Crop Clinic":
    hero(T("clinic_kicker"),T("clinic_title"),T("clinic_copy"))
    photo=st.file_uploader(T("photo"),type=["jpg","jpeg","png"])
    if photo: st.image(photo,width=420)
    symptom=st.selectbox(T("symptom"),[T("yellow"),T("brown"),T("wilting"),T("holes"),T("slow"),T("other")])
    stage=st.selectbox(T("stage"),[T("seedling"),T("vegetative"),T("flowering"),T("fruiting"),T("unknown")])
    if st.button(T("build"),width="stretch"):
        st.markdown("### "+T("checklist"))
        st.write(f"**{T('crop')}:** {crop} · **{T('stage')}:** {stage} · **{T('symptom')}:** {symptom}")
        for item in ["check1","check2","check3","check4"]: st.write("• "+T(item))
        st.warning(T("not_diagnosis"))

elif selected == "Connect Hardware":
    hero(T("hardware_kicker"),T("hardware_title"),T("hardware_copy"))
    st.markdown("### "+T("data_path"))
    st.code("Capacitive soil sensor → ESP32 ADC → Wi-Fi → authenticated endpoint → AGRI//NOVA dashboard",language="text")
    st.error(T("no_sensor"))
    st.markdown("### "+T("integration"))
    for item in ["hw1","hw2","hw3","hw4"]: st.write("• "+T(item))
    st.warning(T("pump_warning"))

st.markdown("---")
st.markdown(f'<div class="topline"><span>{T("footer1")}</span><span>{T("footer2")}</span></div>',unsafe_allow_html=True)
