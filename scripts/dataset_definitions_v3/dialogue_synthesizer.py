"""
Multilingual Dialogue Synthesizer for KAVACH AI Synthetic Dataset v3.
Generates authentic, high-diversity, multi-turn phone conversations across 5 languages:
- English (en)
- Hindi in Devanagari (hi)
- Telugu in Telugu script (te)
- Hindi-English code-mixed / Hinglish (hi-en)
- Telugu-English code-mixed / Tenglish (te-en)

Varies turns (4, 6, 8, 10, 12) and recipient personas (skeptic, anxious, executive, senior, security_aware).
"""

from typing import Dict, Any, List

def build_dialogue_v3(scenario: Dict[str, Any], lang: str, scenario_idx: int) -> List[Dict[str, str]]:
    category = scenario["category"]
    turns_count = scenario.get("turn_count", 6)
    
    # 5 distinct recipient personas
    persona_idx = (scenario_idx + (0 if lang == "en" else 1 if lang == "hi" else 2 if lang == "te" else 3 if lang == "hi-en" else 4)) % 5
    # personas: 0=skeptic, 1=anxious, 2=executive, 3=senior, 4=security_aware
    
    if category == "SCAM":
        return _build_scam_dialogue(scenario, lang, turns_count, persona_idx)
    elif category == "LEGITIMATE":
        return _build_legit_dialogue(scenario, lang, turns_count, persona_idx)
    else:  # AMBIGUOUS
        return _build_ambig_dialogue(scenario, lang, turns_count, persona_idx)


def _build_scam_dialogue(sc: Dict[str, Any], lang: str, turns: int, p_idx: int) -> List[Dict[str, str]]:
    org = sc.get("caller_org", "Department Office")
    c_name = sc.get("caller_name", "Officer Sharma")
    hook = sc.get("hook", "urgent investigation")
    threat = sc.get("threat", "immediate legal escalation")
    demand = sc.get("demand", "comply immediately")
    
    if lang == "en":
        dialogue = [
            {"speaker": "caller", "text": f"This is {c_name} calling urgently from {org}. We have initiated action regarding {hook}."},
            {"speaker": "recipient", "text": [
                f"Wait, {hook}? Who authorized this call? I have never been involved in anything like that.",
                f"Oh no! {hook}? Please tell me this is a mistake, I am getting extremely anxious.",
                f"I am in the middle of a corporate meeting. Email me the formal dossier regarding {hook}.",
                f"Sir, I am a retired senior citizen living alone. What does {hook} mean for me?",
                f"Any official communication regarding {hook} must be delivered via registered postal notice. State your credentials."
            ][p_idx]}
        ]
        if turns >= 4:
            dialogue.append({"speaker": "caller", "text": f"Our national system logs are definitive. To avoid {threat}, you must immediately comply with {demand}."})
            dialogue.append({"speaker": "recipient", "text": [
                "I will not comply over an unsolicited phone call. Send an official notice in writing, or I am contacting police.",
                "Let me consult my family first. I am not making any financial or security transfers over the phone.",
                "Direct that demand to my corporate legal counsel. I do not entertain unsolicited financial demands.",
                "My daughter handles all my financial accounts. I will have her call you back at your official office.",
                "Demanding immediate compliance over phone is a recognized scam tactic. I am hanging up and alerting cyber authorities."
            ][p_idx]})
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"Our compliance deadline expires within 30 minutes. If you hesitate, enforcement officers will proceed with {threat}."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "You cannot bypass statutory due process with a 30-minute phone deadline. I demand an official reference number.",
                "Please do not send enforcement officers to my house! Is there any official counter or office I can visit?",
                "I do not respond to artificial urgency. Provide your departmental landline extension and employee registration code.",
                "I am unable to understand why this cannot wait until tomorrow morning when my son is home.",
                "Artificial urgency is red flag number one. Legitimate government agencies never bypass standard written summons."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"This directive has been cleared under emergency fast-track powers. You are legally barred from discussing this with third parties."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "Barring me from legal counsel is unconstitutional. That alone proves this call is fraudulent.",
                "Why can't I talk to my family? This is feeling very intimidating and scary.",
                "Company policy strictly forbids non-disclosure demands without an executed NDA. Disconnect immediately.",
                "If I cannot consult my family, I will walk down to the neighborhood police station right now.",
                "Isolation pressure is a textbook social engineering tactic. I am terminating this call now."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"If you disconnect now, the system will record willful contempt, resulting in instant freeze on all linked financial assets."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "Freezing accounts requires a formal court order, not a verbal threat on a mobile line. I am calling my bank.",
                "Please don't freeze my accounts, I need my savings for medical emergencies! What is the official way to verify?",
                "Threatening asset freezing over phone is illegal. My legal team will address any written court summons.",
                "I have worked hard all my life. I will not be bullied over a telephone call. I am hanging up.",
                "Every threat you make confirms malicious intent. This call is being recorded for the national cyber crime portal 1930."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"Final warning: the enforcement server is waiting for confirmation of {demand}. Do you refuse compliance?"})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "Yes, I unconditionally refuse to comply with unverified phone demands. Have a formal officer serve me in person.",
                "I am going directly to the local police precinct right now to report this incident.",
                "I refuse. Further contact will result in criminal harassment filings against your line.",
                "I am hanging up now and waiting for my family to arrive.",
                "I refuse. Reporting this caller ID and audio transcript to the cybercrime portal immediately."
            ][p_idx]})
        return dialogue[:turns]

    elif lang == "hi":
        dialogue = [
            {"speaker": "caller", "text": f"यह {org} से {c_name} बोल रहे हैं। आपके खिलाफ {hook} का मामला दर्ज किया गया है।"},
            {"speaker": "recipient", "text": [
                f"रुकिए, {hook}? यह किस आधार पर कह रहे हैं? मैंने कभी ऐसा कोई काम नहीं किया।",
                f"हे भगवान! {hook}? कृपया बताइए क्या बात है, मैं बहुत घबरा रहा हूँ।",
                f"मैं अभी दफ्तर की आवश्यक मीटिंग में हूँ। {hook} के कागजात आधिकारिक ईमेल पर भेजिए।",
                f"बेटा, मैं एक बुजुर्ग पेंशनर हूँ। {hook} का क्या मतलब है, मुझे समझाइए।",
                f"{hook} के संबंध में कोई भी सूचना लिखित सरकारी डाक से आनी चाहिए। पहले अपनी पहचान बताइए।"
            ][p_idx]}
        ]
        if turns >= 4:
            dialogue.append({"speaker": "caller", "text": f"सरकारी रिकॉर्ड में आपका नाम दर्ज है। तुरंत कार्रवाई रोकने के लिए {demand} करें, वर्ना {threat} होगी।"})
            dialogue.append({"speaker": "recipient", "text": [
                "मैं फोन पर कोई भुगतान या जानकारी नहीं दूँगा। लिखित सरकारी नोटिस भेजिए, मैं थाने में आकर बात करूँगा।",
                "मैं पहले अपने परिवार से बात करूँगा। फोन पर कोई भी फैसला नहीं ले सकता।",
                "यह मामला मेरी कानूनी टीम देखेगी। फोन पर किसी भी मांग को स्वीकार नहीं किया जाएगा।",
                "मेरी बेटी शाम को घर आएगी, वही इन सब मामलों को देखती है। आप तब बात कीजिएगा।",
                "फोन पर तुरंत कार्रवाई का दबाव बनाना साइबर ठगी का तरीका है। मैं कॉल काट रहा हूँ।"
            ][p_idx]})
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"आपके पास केवल आधे घंटे का समय है। यदि आपने सहयोग नहीं दिया तो अधिकारी {threat} के लिए रवाना होंगे।"})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "आधे घंटे की कोई कानूनी मियाद नहीं होती। मुझे आधिकारिक केस नंबर और नोटिस चाहिए।",
                "कृपया घर पर किसी को मत भेजिए! क्या मैं किसी सरकारी दफ्तर में आकर बात कर सकता हूँ?",
                "दबाव बनाने की कोशिश मत कीजिए। अपना विभागीय लैंडलाइन नंबर और कर्मचारी कोड दीजिए।",
                "कल सुबह तक रुकिए, जब मेरा बेटा घर पर हो तब आइएगा।",
                "जल्दबाजी का दबाव बनाना साफ तौर पर फर्जीवाड़े का संकेत है। सरकारी एजेंसियां ऐसे काम नहीं करतीं।"
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"यह जांच अत्यंत गोपनीय है। आपको किसी भी रिश्तेदार या वकील से बात करने की अनुमति नहीं है।"})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "वकील से बात करने से रोकना गैरकानूनी है। इससे साफ साबित होता है कि यह कॉल फर्जी है।",
                "मैं परिवार से बात क्यों नहीं कर सकता? यह बात मुझे बहुत डरावनी लग रही है।",
                "बिना कानूनी सलाह के मैं कोई बातचीत आगे नहीं बढ़ाऊँगा। तुरंत कॉल डिस्कनेक्ट करें।",
                "अगर मैं अपने बच्चों से बात नहीं कर सकता, तो मैं अभी पास के थाने जा रहा हूँ।",
                "अकेले में दबाव बनाना साइबर अपराधियों का जाना-माना तरीका है। मैं फोन रख रहा हूँ।"
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"कॉल काटी तो आपके सभी बैंक खाते और आधार सेवा तुरंत फ्रीज कर दी जाएगी।"})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "खाता फ्रीज करने के लिए कोर्ट का आदेश चाहिए, फोन पर धमकी नहीं। मैं अपने बैंक मैनेजर से बात करूँगा।",
                "कृपया खाते फ्रीज मत कीजिए, दवाइयों के लिए पैसे चाहिए! आधिकारिक सत्यापन का सही तरीका बताइए।",
                "फोन पर धमकी देना कानूनन अपराध है। मैं अपने वकील के साथ अदालत में जवाब दूँगा।",
                "मैंने जीवन भर ईमानदारी से काम किया है। मैं इस तरह की धमकियों से नहीं डरूँगा।",
                "आपकी हर धमकी दर्ज हो रही है। मैं राष्ट्रीय साइबर हेल्पलाइन 1930 पर शिकायत दर्ज कर रहा हूँ।"
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"अंतिम चेतावनी: {demand} की प्रक्रिया अभी पूरी करें या गिरफ्तारी के लिए तैयार रहें।"})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "मैं कोई अनुपालन नहीं करूँगा। पुलिस को मेरे घर आने दीजिए, मैं थाने में ही बात करूँगा।",
                "मैं अभी अपने नजदीकी पुलिस स्टेशन जाकर इस कॉल की रिपोर्ट कर रहा हूँ।",
                "मैं बिल्कुल मना करता हूँ। दोबारा कॉल करने पर पुलिस में एफआईआर दर्ज कराई जाएगी।",
                "मैं फोन काट रहा हूँ और अपने परिवार को बुला रहा हूँ।",
                "स्पष्ट मना करता हूँ। यह नंबर और बातचीत साइबर पोर्टल पर रिपोर्ट की जा रही है।"
            ][p_idx]})
        return dialogue[:turns]

    elif lang == "te":
        dialogue = [
            {"speaker": "caller", "text": f"ఇది {org} నుండి {c_name} మాట్లాడుతున్నాము. మీపై {hook} గురించి చట్టపరమైన దర్యాప్తు ప్రారంభమైంది."},
            {"speaker": "recipient", "text": [
                f"ఆగండి, {hook}? దీనికి ఎవరు అనుమతి ఇచ్చారు? నాకు ఇలాంటి వ్యవహారాలతో ఎలాంటి సంబంధం లేదు.",
                f"అయ్యో దేవుడా! {hook}? దయచేసి ఇది తప్పని చెప్పండి, నాకు చాలా భయంగా ఉంది.",
                f"నేను ఇప్పుడు ఆఫీస్ మీటింగ్‌లో ఉన్నాను. {hook} గురించిన అధికారిక వివరాలను రిజిస్టర్డ్ ఈమెయిల్‌కు పంపండి.",
                f"అయ్యా, నేను ఒంటరిగా ఉండే రిటైర్డ్ సీనియర్ సిటిజన్‌ని. {hook} అంటే నాకేమీ అర్థం కావడం లేదు.",
                f"{hook} గురించి ఏదైనా ఉంటే అధికారిక పోస్టల్ నోటీసు ద్వారా రావాలి. మీ ఐడీ వివరాలు చెప్పండి."
            ][p_idx]}
        ]
        if turns >= 4:
            dialogue.append({"speaker": "caller", "text": f"మా సిస్టమ్ రికార్డుల్లో మీ పేరు ఉంది. వెంటనే {threat} నివారించడానికి {demand} పూర్తి చేయాలి."})
            dialogue.append({"speaker": "recipient", "text": [
                "నేను ఫోన్ కాల్ ద్వారా ఎలాంటి చెల్లింపులు చేయను. రాతపూర్వక నోటీసు పంపండి, పోలీస్ స్టేషన్‌కు వచ్చి మాట్లాడతాను.",
                "నేను ముందుగా మా కుటుంబ సభ్యులతో మాట్లాడాలి. ఫోన్‌లో ఎలాంటి నిర్ణయం తీసుకోను.",
                "మా లీగల్ అడ్వైజర్‌తో మాట్లాడండి. ఫోన్‌లో బెదిరింపులను నేను అంగీకరించను.",
                "మా అబ్బాయి సాయంత్రం వస్తాడు, అతనే అన్ని వ్యవహారాలు చూస్తాడు. అప్పుడు కాల్ చేయండి.",
                "ఫోన్‌లో ఇలా ఒత్తిడి చేయడం సైబర్ నేరగాళ్ల పద్ధతి. నేను కాల్ కట్ చేస్తున్నాను."
            ][p_idx]})
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"మీకు కేవలం అరగంట సమయం మాత్రమే ఉంది. ఆలస్యం చేస్తే అధికారులు వచ్చి {threat} చేస్తారు."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "అరగంట గడువు అనేది చట్టంలో ఉండదు. నాకు సరైన కేస్ నంబర్, అధికారిక పత్రాలు కావాలి.",
                "దయచేసి ఇంటికి ఎవరినీ పంపకండి! నేను వచ్చి మాట్లాడటానికి ఏదైనా ప్రభుత్వ కార్యాలయం ఉందా?",
                "తప్పుడు తొందరపెట్టవద్దు. మీ డిపార్ట్‌మెంట్ ల్యాండ్‌లైన్ నంబర్, ఉద్యోగి కోడ్ ఇవ్వండి.",
                "రేపటి వరకు ఆగండి, మా వాళ్ళు వచ్చిన తర్వాతే మాట్లాడతాను.",
                "అత్యవసరమని భయపెట్టడం మోసానికి మొదటి గుర్తు. ప్రభుత్వ సంస్థలు ఇలా ఫోన్‌లో ఒత్తిడి చేయవు."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"ఇది అత్యంత రహస్య దర్యాప్తు. ఈ విషయం గురించి కుటుంబ సభ్యులతో లేదా లాయర్‌తో మాట్లాడకూడదు."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "న్యాయవాదితో మాట్లాడవద్దని చెప్పడం చట్టవిరుద్ధం. ఇది ఖచ్చితంగా ఫేక్ కాల్ అని అర్థమవుతోంది.",
                "మా వాళ్లతో ఎందుకు మాట్లాడకూడదు? ఇది చాలా భయంగా ఉంది.",
                "చట్టపరమైన సలహా లేకుండా నేను ఒక్క అడుగు కూడా ముందుకు వేయను. కాల్ కట్ చేయండి.",
                "మా పిల్లలతో మాట్లాడకూడదంటే, నేను ఇప్పుడే దగ్గర్లోని పోలీస్ స్టేషన్‌కి వెళ్తున్నాను.",
                "ఇతరులతో మాట్లాడకుండా ఏకాంతంలోకి నెట్టడం సైబర్ నేరగాళ్ల వ్యూహం. నేను మాట్లాడను."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"కాల్ కట్ చేస్తే మీ బ్యాంక్ అకౌంట్లు, ఆధార్ కార్డు వెంటనే స్తంభింపజేయబడతాయి."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "అకౌంట్లు ఫ్రీజ్ చేయడానికి కోర్టు ఆర్డర్ కావాలి, ఫోన్‌లో బెదిరిస్తే సరిపోదు. నేను బ్యాంక్ మేనేజర్‌తో మాట్లాడుతాను.",
                "అకౌంట్ ఫ్రీజ్ చేయకండి, మెడికల్ ఖర్చులకు డబ్బులు కావాలి! సరైన వెరిఫికేషన్ మార్గం చెప్పండి.",
                "ఫోన్‌లో బెదిరించడం నేరం. నా లాయర్ ద్వారా సమాధానం ఇస్తాను.",
                "జీవితాంతం నిజాయితీగా బ్రతికాను. ఇలాంటి ఫోన్ బెదిరింపులకు నేను లొంగను.",
                "మీ బెదిరింపులన్నీ రికార్డ్ అవుతున్నాయి. జాతీయ సైబర్ హెల్ప్‌లైన్ 1930లో ఫిర్యాదు చేస్తున్నాను."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"చివరి హెచ్చరిక: {demand} వెంటనే పూర్తి చేస్తారా లేదా అరెస్ట్ కావడానికి సిద్ధంగా ఉన్నారా?"})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "నేను ఎట్టి పరిస్థితుల్లోనూ డబ్బులు పంపను. పోలీస్ అధికారులను రానివ్వండి, అక్కడే తేల్చుకుంటాను.",
                "నేను ఇప్పుడే లోకల్ పోలీస్ స్టేషన్‌కి వెళ్లి ఈ కాల్ గురించి కంప్లయింట్ ఇస్తున్నాను.",
                "నేను ఖరాఖండిగా తిరస్కరిస్తున్నాను. మళ్ళీ కాల్ చేస్తే పోలీసులకు పట్టిస్తాను.",
                "నేను ఫోన్ పెట్టేస్తున్నాను, మా వాళ్ళు వచ్చే వరకు వేచి చూస్తాను.",
                "తిరస్కరిస్తున్నాను. ఈ నంబర్‌ను సైబర్ క్రైమ్ పోర్టల్‌లో రిపోర్ట్ చేస్తున్నాను."
            ][p_idx]})
        return dialogue[:turns]

    elif lang == "hi-en":
        dialogue = [
            {"speaker": "caller", "text": f"Hello, main {org} se {c_name} bol raha hoon. Aapke khilaf {hook} ka investigation open hua hai."},
            {"speaker": "recipient", "text": [
                f"Wait sir, {hook}? Main kisi fraud mein involved nahi hoon. What is this call about?",
                f"Oh my god! {hook}? Please sir bataiye kya issue hai, main bahut panic ho raha hoon.",
                f"I am in an urgent office conference right now. {hook} ka official email send kijiye.",
                f"Sir main ek senior citizen pensioner hoon. {hook} ka exact matlab kya hai?",
                f"Official matter hai toh registered post se notice bhejiye. Who authorized this phone call?"
            ][p_idx]}
        ]
        if turns >= 4:
            dialogue.append({"speaker": "caller", "text": f"Hamare centralized system records clear hain. To avoid {threat}, aapko turant {demand} karna hoga."})
            dialogue.append({"speaker": "recipient", "text": [
                "Main phone par koi money transfer ya OTP share nahi karunga. Send official summon, I will visit police station.",
                "Pehle main apni family se consult karunga. Over the phone koi payment nahi ho sakti.",
                "Forward this demand to my legal counsel. Unsolicited phone demand entertain nahi karta main.",
                "Meri beti aayegi sham ko, wahi bank matters dekhti hai. She will call you back.",
                "Phone par compliance demand karna clear scam pattern hai. I am hanging up."
            ][p_idx]})
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"Aapke paas sirf 30 minutes ka time hai. If you delay, our team will execute {threat} immediately."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "30 minutes deadline is meaningless under legal law. Official case number aur jurisdiction bataiye.",
                "Please ghar par kisi ko mat bhejiye! Kya main kisi official branch ya office mein visit kar sakta hoon?",
                "Don't create false urgency with me. Official landline number aur employee badge ID share kijiye.",
                "Kal subah tak wait kijiye, jab mera beta ghar par hoga.",
                "Artificial urgency is red flag number one. Legitimate government bodies aise phone par threaten nahi karti."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"Yeh confidential emergency probe hai. You are legally restricted from informing family or advocates."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "Family ya lawyer se baat karne se rokna completely illegal hai. This confirms this is a fake call.",
                "Why can't I consult my family? This sounds very suspicious and frightening.",
                "Without consulting my advocate, I will not speak a single word. Disconnect immediately.",
                "Agar family se baat nahi kar sakta, toh main abhi seedha local police station jaa raha hoon.",
                "Isolating the victim is standard social engineering textbook technique. I am cutting the call."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"Agar call disconnect kiya toh system aapke saare bank accounts aur mobile connection freeze kar dega."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "Account freeze karne ke liye court warrant lagta hai, verbal threat nahi. I will call my bank.",
                "Please account freeze mat kijiye, hospital expenses ke paise hain! Genuine verification ka tarika bataiye.",
                "Threatening account freeze over voice call is an offense. My lawyer will answer in court.",
                "I have worked honestly my whole life. Aise phone threats se main nahi darunga.",
                "Every threat is getting recorded. National cyber helpline 1930 par complain lodge kar raha hoon."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"Last warning: {demand} abhi execute karte hain ya legal arrest ke liye prepare ho rahe hain?"})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "I completely refuse. Send physical officers to my registered address, we will talk there.",
                "Main abhi seedha nearest police station report karne jaa raha hoon.",
                "Refused. Agli baar call aayi toh harassment FIR file karwaunga.",
                "Main call disconnect kar raha hoon and waiting for my family.",
                "Strictly refusing. Number and transcript cyber portal par report kar raha hoon."
            ][p_idx]})
        return dialogue[:turns]

    else:  # te-en
        dialogue = [
            {"speaker": "caller", "text": f"Hello, nenu {org} nundi {c_name} call chestunnanu. Mee meeda {hook} case file aindi."},
            {"speaker": "recipient", "text": [
                f"Wait sir, {hook}? Nenu eppudu elanti illegal activity cheyaledu. What is this about?",
                f"Oh my god! {hook}? Please sir emaindo cheppandi, naku chala anxiety ga undi.",
                f"Nenu office meeting lo unnanu. {hook} details ni official registered mail ki pampandi.",
                f"Sir nenu retired senior citizen ni. {hook} ante exact ga emito cheppandi.",
                f"Official communication postal dispatch dwara ravali kada. What is your department authority?"
            ][p_idx]}
        ]
        if turns >= 4:
            dialogue.append({"speaker": "caller", "text": f"Central records confirm chestunnayi. Immediate ga {threat} avoid cheyadaniki, meeru {demand} cheyali."})
            dialogue.append({"speaker": "recipient", "text": [
                "Phone call lo nenu elanti transfer cheyanu. Written notice pampandi, police station ki vachi matladatanu.",
                "First ma family tho matladali. Phone lo elanti amount pay cheyanu.",
                "Speak with my legal counsel. Unsolicited phone demand ni nenu bilkul accept cheyanu.",
                "Ma abbayi evening vastadu, he handles financial matters. He will call back.",
                "Phone lo pressure pettadam fraud pattern. I am hanging up the call."
            ][p_idx]})
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"Meku kevalam 30 minutes time undi. Delay cheste officers vachi {threat} execute chestaru."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "30 minutes deadline legal ga valid kadu. Official case reference number ivvandi.",
                "Please intiki evarini pampoddu! Any official government branch nenu visit cheyocha?",
                "Don't build false urgency. Department landline and officer registration ID share cheyandi.",
                "Tomorrow morning varaku agandi, ma family presence lo matladatanu.",
                "Fake urgency create cheyadam classic red flag. Real officials ila call chesi bedirinchavu."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"Idi confidential inquiry. You are legally restricted from discussing this with family or lawyers."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "Family or lawyer tho matladoddu anadam illegal. This clearly proves this call is fake.",
                "Why can't I consult my family? Idi chala scary ga undi sir.",
                "Advocate guidance lekunda nenu okka mata kuda matladanu. Disconnect the call.",
                "Ma family tho matladakudadu ante, nenu direct ga local police station ki velthanu.",
                "Isolating the person is textbook social engineering. Call cut chestunnanu."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"Call cut cheste mee bank accounts and mobile connection ventane freeze cheyabadathayi."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "Account freeze cheyadaniki court warrant undali, verbal threats kadu. I will contact my bank.",
                "Please accounts freeze cheyoddu, medical bills ki dabbu kavali! Genuine verification method cheppandi.",
                "Phone lo bedirinchadam criminal offense. Court lo legal ga answer chesukuntanu.",
                "Nenu honest citizen ni. Ilanti threats ki bhayapadenu.",
                "Mee threats anni record chestunnanu. National cyber helpline 1930 lo complain chestunnanu."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"Final warning: {demand} ippude execute chestaru or arrest ki prepare avuthara?"})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "I strictly refuse. Send official officers with warrant to my home, akkada chuskundam.",
                "I am heading straight to the police station to lodge an official complaint.",
                "Refused completely. Malli call cheste criminal harassment case vestanu.",
                "Call cut chestunnanu and waiting for my family to arrive.",
                "Refusing completely. Number and audio transcript cyber portal lo report chestunnanu."
            ][p_idx]})
        return dialogue[:turns]


def _build_legit_dialogue(sc: Dict[str, Any], lang: str, turns: int, p_idx: int) -> List[Dict[str, str]]:
    org = sc.get("caller_org", "Customer Service")
    c_name = sc.get("caller_name", "Representative")
    topic = sc.get("topic", "scheduled service update")
    res = sc.get("resolution", "please visit official branch or portal")
    
    if lang == "en":
        dialogue = [
            {"speaker": "caller", "text": f"Good day, this is {c_name} calling from {org}. I am reaching out regarding {topic}."},
            {"speaker": "recipient", "text": [
                f"Hello, thank you for calling. Could you share more details about {topic}?",
                f"Hello. Yes, I was expecting an update regarding {topic}. Please go ahead.",
                f"Good day. I have about two minutes between meetings. Can you give me the key points on {topic}?",
                f"Hello son, yes I can hear you clearly. What is this update regarding {topic}?",
                f"Hello. Before proceeding, can you confirm the official reference code or ticket for {topic}?"
            ][p_idx]},
            {"speaker": "caller", "text": f"Certainly. The record indicates that for completion, the recommended step is: {res}."},
            {"speaker": "recipient", "text": [
                "Understood. That is very clear. Do I need to carry any specific documentation with me?",
                "Thank you for clarifying. Is there an official link or branch address I should refer to?",
                "Got it. I will review the instructions and complete this through official channels.",
                "Thank you for explaining so patiently. I will ask my family to assist me with that.",
                "That matches standard procedures. I will access the official portal directly to proceed."
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"We wanted to ensure you received the formal notification dispatched to your registered address."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "Yes, I did receive an email notification earlier this week. I appreciate the follow-up.",
                "I haven't checked my postal mail yet, but I will look for it today.",
                "My office admin handles postal mail. I will verify with them shortly.",
                "My son usually checks the mailbox on weekends. I will inform him.",
                "I see the notification in my registered inbox. Thank you for cross-checking."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"Please note as a standard security reminder: our organization will never ask for your passwords, OTP, or CVV over the phone."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "That is reassuring to hear. It is always good to reinforce security practices.",
                "Thank you for the reminder. Cyber fraud has been increasing, so caution is important.",
                "Appreciate the security disclosure. That is proper corporate governance.",
                "Yes, my grandson told me never to tell any secret numbers on the phone.",
                "Exactly. All authentic institutions maintain that protocol. Glad to see it enforced."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"If you require any further assistance, our toll-free customer support desk is available on our official website."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "Perfect. I have the customer care number saved from my passbook.",
                "Thank you. Could you repeat the customer support operating hours?",
                "Noted. I will reach out if any questions arise during the process.",
                "Thank you beta, you have been very polite and helpful.",
                "Thank you for your time and professional assistance today."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"Have a pleasant day ahead. Thank you for your continued association with {org}."})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "Thank you, have a great day ahead as well. Goodbye.",
                "Thank you very much. Have a wonderful day.",
                "Thanks, take care. Goodbye.",
                "Bless you child, take care. Namaste.",
                "Thank you for your assistance. Goodbye."
            ][p_idx]})
        return dialogue[:turns]

    elif lang == "hi":
        dialogue = [
            {"speaker": "caller", "text": f"नमस्कार, मैं {org} से {c_name} बात कर रहा हूँ। यह कॉल {topic} के संदर्भ में है।"},
            {"speaker": "recipient", "text": [
                f"नमस्ते, कॉल करने के लिए धन्यवाद। {topic} के बारे में थोड़ा विस्तार से बताइए।",
                f"नमस्ते जी। हाँ, मैं {topic} के संबंध में ही जानकारी चाह रहा था। बताइए।",
                f"नमस्कार। मैं अभी थोड़ा व्यस्त हूँ, कृपया {topic} के मुख्य बिंदु संक्षेप में बताएं।",
                f"नमस्ते बेटा। हाँ तुम्हारी आवाज आ रही है। {topic} के बारे में क्या सूचना है?",
                f"नमस्ते। आगे बात करने से पहले, क्या आप {topic} का आधिकारिक संदर्भ नंबर बता सकते हैं?"
            ][p_idx]},
            {"speaker": "caller", "text": f"जी बिल्कुल। आधिकारिक प्रक्रिया के अनुसार आपको यह सलाह दी जाती है: {res}।"},
            {"speaker": "recipient", "text": [
                "बहुत अच्छा। यह बिल्कुल स्पष्ट है। क्या इसके लिए कोई विशेष दस्तावेज साथ लाने होंगे?",
                "जानकारी के लिए धन्यवाद। क्या मैं इसे नजदीकी शाखा में जाकर पूरा कर सकता हूँ?",
                "समझ गया। मैं आधिकारिक पोर्टल या शाखा में जाकर यह प्रक्रिया पूरी कर लूँगा।",
                "बेटा, बहुत धैर्य से समझाने के लिए शुक्रिया। मैं अपने बेटे से कहकर यह करवा लूँगा।",
                "यह सही और सुरक्षित तरीका है। मैं आधिकारिक माध्यम से ही आगे बढ़ूँगा।"
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"हम केवल यह सुनिश्चित करना चाहते थे कि आपको आपके रजिस्टर्ड पते पर भेजी गई सूचना मिल गई है।"})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "हाँ, मुझे इस सप्ताह की शुरुआत में ईमेल पर सूचना प्राप्त हुई थी। धन्यवाद।",
                "मैंने डाक अभी नहीं देखी है, पर आज शाम को जरूर देखूँगा।",
                "दफ्तर की डाक मेरे सहायक देखते हैं, मैं उनसे पता करवाता हूँ।",
                "मेरा बेटा रविवार को डाक चेक करता है, मैं उसे बता दूँगा।",
                "जी हाँ, आधिकारिक इनबॉक्स में संदेश उपलब्ध है। सत्यापन के लिए शुक्रिया।"
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"कृपया सुरक्षा के लिए ध्यान रखें: हमारा संस्थान कभी भी फोन पर आपसे ओटीपी, पिन या पासवर्ड नहीं मांगता।"})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "यह सुनकर बहुत तसल्ली हुई। सुरक्षा नियमों की याद दिलाना बहुत जरूरी है।",
                "धन्यवाद। आजकल ऑनलाइन धोखाधड़ी बहुत बढ़ गई है, इसलिए सावधानी जरूरी है।",
                "सुरक्षा परामर्श के लिए धन्यवाद। यही जिम्मेदार संस्थान की पहचान है।",
                "हाँ बेटा, मेरे पोते ने भी मुझे समझाया है कि फोन पर कोई गोपनीय नंबर नहीं बताना।",
                "बिल्कुल सही। सभी असली संस्थान इसी नियम का पालन करते हैं।"
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"यदि आपको भविष्य में कोई सहायता चाहिए तो हमारा टोल-फ्री नंबर आधिकारिक वेबसाइट पर उपलब्ध है।"})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "बहुत खूब। मेरे पास पासबुक पर छपा कस्टमर केयर नंबर सुरक्षित है।",
                "धन्यवाद। क्या आप कस्टमर केयर के काम करने का समय बता सकते हैं?",
                "नोट कर लिया। कोई शंका होने पर मैं आधिकारिक नंबर पर संपर्क करूँगा।",
                "बहुत-बहुत धन्यवाद बेटा, तुमने बहुत अच्छे से समझाया।",
                "आज आपके पेशेवर और विनम्र सहयोग के लिए बहुत धन्यवाद।"
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"आपका दिन शुभ हो। {org} से जुड़े रहने के लिए धन्यवाद।"})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "धन्यवाद, आपका भी दिन शुभ हो। नमस्ते।",
                "बहुत शुक्रिया। ध्यान रखिएगा।",
                "थैंक यू, बाय।",
                "जीते रहो बेटा, नमस्ते।",
                "सहयोग के लिए धन्यवाद। नमस्कार।"
            ][p_idx]})
        return dialogue[:turns]

    elif lang == "te":
        dialogue = [
            {"speaker": "caller", "text": f"నమస్కారం అండి, నేను {org} నుండి {c_name} మాట్లాడుతున్నాను. ఇది {topic} గురించిన కాల్."},
            {"speaker": "recipient", "text": [
                f"నమస్కారం, కాల్ చేసినందుకు ధన్యవాదాలు. {topic} గురించిన వివరాలు చెప్పండి.",
                f"నమస్కారం అండి. అవును, నేను {topic} సమాచారం కోసం ఎదురుచూస్తున్నాను. చెప్పండి.",
                f"నమస్కారం. నేను కొంచెం బిజీగా ఉన్నాను, {topic} ముఖ్యమైన విషయాలు క్లుప్తంగా చెప్పగలరా?",
                f"నమస్కారం బాబు. అవును వినిపిస్తోంది. {topic} గురించి ఏమిటి విశేషం?",
                f"నమస్కారం. మాట్లాడే ముందు, {topic} అధికారిక రిఫరెన్స్ నంబర్ చెప్పగలరా?"
            ][p_idx]},
            {"speaker": "caller", "text": f"తప్పకుండా అండి. అధికారిక విధానం ప్రకారం మీరు చేయవలసిన పని: {res}."},
            {"speaker": "recipient", "text": [
                "చాలా స్పష్టంగా చెప్పారు. దీనికి సంబంధించి ఏమైనా పత్రాలు తీసుకురావాలా?",
                "వివరించినందుకు ధన్యవాదాలు. సమీప బ్రాంచ్‌కి వెళ్లి ఇది పూర్తి చేయవచ్చా?",
                "అర్థమైంది. నేను అధికారిక పోర్టల్ లేదా బ్రాంచ్‌కు వెళ్లి పూర్తి చేస్తాను.",
                "ఓపికగా వివరించినందుకు చాలా ధన్యవాదాలు బాబు. మా అబ్బాయితో చెప్పి చేయిస్తాను.",
                "ఇది సరైన పద్ధతి. నేను అధికారిక మార్గంలోనే ముందుకు వెళ్తాను."
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"మీ రిజిస్టర్డ్ చిరునామాకు పంపిన సమాచారం మీకు అందిందో లేదో నిర్ధారించుకోవడానికి మాత్రమే ఈ కాల్ చేసాము."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "అవును, ఈ వారం ప్రారంభంలో నాకు ఈమెయిల్ వచ్చింది. గుర్తుచేసినందుకు ధన్యవాదాలు.",
                "నేను ఇంకా పోస్ట్ చూడలేదు, కానీ ఈరోజు చూస్తాను.",
                "మా ఆఫీస్ స్టాఫ్ చూస్తారు, నేను వారిని అడుగుతాను.",
                "మా అబ్బాయి ఆదివారం లెటర్స్ చూస్తాడు, అతనికి చెబుతాను.",
                "అవును, రిజిస్టర్డ్ ఈమెయిల్‌లో సందేశం ఉంది. సరిచూసినందుకు ధన్యవాదాలు."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"దయచేసి భద్రతా నిబంధన గుర్తుంచుకోండి: మా సంస్థ ఎప్పుడూ ఫోన్‌లో ఓటీపీ, పిన్ లేదా పాస్‌వర్డ్ అడగదు."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "ఇది వినడం చాలా సంతోషంగా ఉంది. సెక్యూరిటీ నిబంధనలు గుర్తుచేయడం చాలా మంచిది.",
                "ధన్యవాదాలు. ఈ రోజుల్లో ఆన్‌లైన్ మోసాలు ఎక్కువయ్యాయి, జాగ్రత్త అవసరం.",
                "భద్రతా సమాచారం ఇచ్చినందుకు ధన్యవాదాలు. బాధ్యతాయుతమైన సంస్థ లక్షణం ఇది.",
                "అవును బాబు, మా మనవడు కూడా చెప్పాడు ఫోన్‌లో ఎవరికీ రహస్య నంబర్లు చెప్పకూడదని.",
                "ఖచ్చితంగా. అసలైన సంస్థలన్నీ ఈ నియమాన్ని పాటిస్తాయి."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"భవిష్యత్తులో ఏదైనా సహాయం కావాలంటే మా టోల్-ఫ్రీ నంబర్ అధికారిక వెబ్‌సైట్‌లో అందుబాటులో ఉంది."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "చాలా మంచిది. నా దగ్గర పాస్‌బుక్‌పై ఉన్న కస్టమర్ కేర్ నంబర్ ఉంది.",
                "ధన్యవాదాలు. కస్టమర్ సపోర్ట్ పనిచేసే సమయాలు చెప్పగలరా?",
                "గుర్తుంచుకుంటాను. ఏవైనా సందేహాలు ఉంటే అధికారిక నంబర్‌కు కాల్ చేస్తాను.",
                "చాలా థాంక్స్ బాబు, చాలా మర్యాదగా సహాయం చేశావు.",
                "ఈరోజు మీ వృత్తిపరమైన సహకారానికి చాలా ధన్యవాదాలు."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"మీకు మంచి రోజు కావాలని కోరుకుంటున్నాము. {org}తో ఉన్నందుకు ధన్యవాదాలు."})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "ధన్యవాదాలు, మీకు కూడా మంచి రోజు కావాలి. నమస్కారం.",
                "చాలా థాంక్స్ అండి. జాగ్రత్తగా ఉండండి.",
                "థాంక్యూ, ఉంటాను.",
                "మంచిది బాబు, నమస్కారం.",
                "సహకరించినందుకు ధన్యవాదాలు. సెలవు."
            ][p_idx]})
        return dialogue[:turns]

    elif lang == "hi-en":
        dialogue = [
            {"speaker": "caller", "text": f"Hello, good day! Main {org} se {c_name} baat kar raha hoon. This call is regarding {topic}."},
            {"speaker": "recipient", "text": [
                f"Hello, thank you for calling. Can you explain more details about {topic}?",
                f"Hello sir. Yes, main {topic} ke bare mein hi information chahta tha. Please continue.",
                f"Good day. Main thoda busy hoon meeting mein, please share key points regarding {topic}.",
                f"Hello beta, yes voice clear hai. {topic} ke bare mein kya update hai?",
                f"Hello. Before we proceed, official ticket ya reference code share kar sakte hain for {topic}?"
            ][p_idx]},
            {"speaker": "caller", "text": f"Sure. Official process ke according recommended step hai: {res}."},
            {"speaker": "recipient", "text": [
                "Understood. That is very clear. Iske liye koi specific documents carry karne honge?",
                "Thank you for clarifying. Nearest branch visit karke complete kar sakta hoon?",
                "Got it. Main official portal ya branch jakar complete kar loonga.",
                "Thank you beta, itne patience se samjhane ke liye. Main apne son ko bolkar karwata hoon.",
                "This matches standard safe protocol. Main official channel ke through hi proceed karunga."
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"Hum bas ensure karna chahte the ki registered address par sent formal communication aap tak pahunch gaya hai."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "Yes, mujhe is week ke starting mein email notification mil gaya tha. Thanks for checking.",
                "Maine postal mail abhi check nahi kiya, but I will check today evening.",
                "Office admin handles postal mail. Main unse confirm karta hoon.",
                "Mera beta weekend par mail check karta hai, I will tell him.",
                "Yes, registered inbox mein intimation available hai. Thank you for cross-checking."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"Standard security reminder: Humari organization kabhi bhi phone par aapse password, OTP ya PIN demand nahi karegi."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "That is very reassuring to hear. Security practices reinforce karna bahut important hai.",
                "Thank you for the reminder. Online fraud badh gaya hai, caution is very necessary.",
                "Appreciate the security disclosure. That is proper corporate governance.",
                "Haan beta, mere grandson ne bhi bataya hai ki phone par secret number kisi ko nahi batana.",
                "Exactly. Authentic organizations always follow this protocol. Good to see this."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"Agar koi further assistance chahiye ho toh official website par toll-free customer desk available hai."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "Great. Passbook par printed customer care number mere paas saved hai.",
                "Thank you. Customer support working hours kya hain please?",
                "Noted. Agar koi question hoga toh main official number par connect karunga.",
                "Thank you so much beta, you have been very polite.",
                "Thank you for your professional assistance today."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"Have a pleasant day ahead. {org} ke sath continue karne ke liye thank you."})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "Thank you, aapka bhi day achha rahe. Goodbye.",
                "Thank you so much. Take care.",
                "Thanks, take care. Bye.",
                "Khush raho beta, take care. Namaste.",
                "Thanks for the support. Goodbye."
            ][p_idx]})
        return dialogue[:turns]

    else:  # te-en
        dialogue = [
            {"speaker": "caller", "text": f"Hello, good day! Nenu {org} nundi {c_name} call chestunnanu. This call is regarding {topic}."},
            {"speaker": "recipient", "text": [
                f"Hello, thank you for calling. Can you share more details on {topic}?",
                f"Hello sir. Avunu, nenu {topic} information kosam chustunnanu. Please go ahead.",
                f"Good day. Nenu conference lo unnanu, please share brief summary on {topic}.",
                f"Hello babu, yes voice clear ga undi. {topic} gurinchi emiti update?",
                f"Hello. Before proceeding, can you confirm official ticket or reference code for {topic}?"
            ][p_idx]},
            {"speaker": "caller", "text": f"Sure andi. Official guidelines prakaram recommended step: {res}."},
            {"speaker": "recipient", "text": [
                "Understood andi. Very clear. Deeniki documents emaina submit cheyala?",
                "Thank you for clarifying. Nearest branch visit chesi complete cheyocha?",
                "Got it. Official netbanking or branch lo direct ga chesukuntanu.",
                "Chala opikaga explain chesavu babu. Ma abbayitho cheppi cheyistanu.",
                "This is standard safe procedure. Direct official portal dwara proceed avutanu."
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"Mee registered address ki dispatch chesina formal communication reach aindo ledo confirm cheyadaniki call chesamu."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "Yes, ee week starting lo naku email intimation vachindi. Thanks for follow-up.",
                "Post inka check cheyaledu, will check today evening.",
                "Office admin team check chestundi, I will verify with them.",
                "Ma abbayi weekend check chestadu, I will inform him.",
                "Yes, registered mail lo intimation undi. Thank you for cross-checking."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"Standard security reminder: Ma organization eppudu phone lo OTP, PIN or password adagadu."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "That is very good to hear. Security rules follow cheyadam chala important.",
                "Thank you for reminder. Cyber frauds ekuva ayyayi, caution is needed.",
                "Appreciate the security disclosure. Good corporate governance.",
                "Avunu babu, ma grandson kuda cheppadu phone lo secret numbers evariki ivvoddu ani.",
                "Exactly. Genuine institutions always follow this rule."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"Meku emaina queries unte official portal lo toll-free customer desk available ga undi."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "Great. Passbook meeda printed support number naku undi.",
                "Thank you. Customer care working timings emiti?",
                "Noted. Doubts unte official helpline ki call chestanu.",
                "Chala thanks babu, chala polite ga explain chesavu.",
                "Thank you for professional assistance today."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"Have a pleasant day ahead. Thank you for banking with {org}."})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "Thank you, have a good day ahead too. Goodbye.",
                "Thank you so much. Take care.",
                "Thanks, take care. Bye.",
                "Manchiga undu babu, take care. Namaste.",
                "Thanks for the guidance. Goodbye."
            ][p_idx]})
        return dialogue[:turns]


def _build_ambig_dialogue(sc: Dict[str, Any], lang: str, turns: int, p_idx: int) -> List[Dict[str, str]]:
    org = sc.get("caller_org", "General Services")
    c_name = sc.get("caller_name", "Caller")
    topic = sc.get("topic", "inquiry regarding account record")
    claim = sc.get("caller_claims", "Caller mentions a routine inquiry.")
    evid_avail = sc.get("evidence_available", "Polite dialogue without credential requests.")
    
    # Ambiguous dialogues maintain realistic uncertainty, unverified context, lack of overt scam indicators, but absence of verifiable institutional credentials
    if lang == "en":
        dialogue = [
            {"speaker": "caller", "text": f"Hello, good day. Am I speaking with the resident at this contact number? This is {c_name} calling from {org} regarding {topic}."},
            {"speaker": "recipient", "text": [
                f"Yes, speaking. What is this call in reference to? I don't recall opening any request with {org}.",
                f"Hello. Yes, speaking. Could you clarify what this inquiry about {topic} involves?",
                f"Yes, this is they. I am quite occupied at the moment. Can you state your specific reference number?",
                f"Hello? Yes, speaking. Can you speak a little louder? What is this regarding?",
                f"Yes, speaking. Which office did you say you are calling from? Can you verify your identity?"
            ][p_idx]},
            {"speaker": "caller", "text": f"We have a record entry on file regarding {topic}. We are simply reviewing customer profiles to ensure information is up to date."},
            {"speaker": "recipient", "text": [
                "I see. But why are you calling from an unlisted mobile line instead of an official PBX desk?",
                "Alright. But is there any action required on my part, or is this purely informational?",
                "I don't share personal or residential details over unsolicited calls. Please send a letter if needed.",
                "I am not sure I understand. My family usually handles these matters. Can you call back later?",
                "Without an official ticket reference or verifiable callback extension, I cannot confirm any details."
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"This is an automated routing dispatch from our regional support desk. We are not requesting any passwords or financial credentials from you."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "I appreciate that you are not asking for passwords, but I still cannot verify who you represent.",
                "That is reassuring, but without knowing the origin of this record, I am hesitant to discuss it.",
                "Regardless of what you request, company protocol advises me not to engage with unverified callers.",
                "Okay beta, but please understand that nowadays we get so many calls that we don't know who is real.",
                "Not asking for passwords is good, but legitimate corporate inquiries usually arrive via formal email."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"Understood. If you prefer, you may check your primary account portal or visit a physical branch at your convenience to review the status."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "That sounds fair. I will inspect my official online portal directly rather than proceeding over phone.",
                "Thank you. Which specific department or menu option should I look for in the portal?",
                "I will take note of that. I will cross-verify with official support when I have time.",
                "Thank you for being polite. I will ask my son to check the computer portal tonight.",
                "Directing to the official portal is the correct procedure. I will handle it through the app."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"Certainly. Please quote notification code #8120 if customer support asks for context during your visit."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "I have noted code #8120 down. I will verify if this code exists in their internal database.",
                "Thank you. Is there any deadline associated with this reference?",
                "I will keep the code handy. Thank you for your time.",
                "Let me write that down with a pen: eight, one, two, zero. Thank you beta.",
                "Reference noted. I will ensure independent verification before taking any action."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"Thank you for your time today. Have a pleasant rest of your day."})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "Thank you. Goodbye.",
                "Thanks, take care. Goodbye.",
                "Goodbye.",
                "Thank you child, goodbye.",
                "Good day. Goodbye."
            ][p_idx]})
        return dialogue[:turns]

    elif lang == "hi":
        dialogue = [
            {"speaker": "caller", "text": f"नमस्कार। क्या मेरी बात इस नंबर के उपभोक्ता से हो रही है? मैं {org} से {c_name} बोल रहा हूँ, {topic} के संदर्भ में।"},
            {"speaker": "recipient", "text": [
                f"हाँ, मैं बोल रहा हूँ। किस बारे में फोन किया है? मुझे {org} से किसी काम की जानकारी नहीं है।",
                f"नमस्ते। जी बोलिए। {topic} के बारे में क्या सूचना है?",
                f"हाँ, बताइए। मैं अभी थोड़ा व्यस्त हूँ। क्या आपके पास कोई आधिकारिक केस या टिकट नंबर है?",
                f"नमस्ते। जरा जोर से बोलिए बेटा, आवाज साफ नहीं आ रही। किस बात के लिए फोन किया है?",
                f"हाँ, मैं सुन रहा हूँ। आप किस विभाग से बात कर रहे हैं? पहले अपनी पहचान स्पष्ट कीजिए।"
            ][p_idx]},
            {"speaker": "caller", "text": f"हमारे सिस्टम में {topic} को लेकर एक प्रविष्टि दर्ज है। हम केवल रिकॉर्ड्स की सामान्य समीक्षा कर रहे हैं।"},
            {"speaker": "recipient", "text": [
                "ठीक है, लेकिन आप किसी आधिकारिक लैंडलाइन की जगह साधारण मोबाइल नंबर से क्यों कॉल कर रहे हैं?",
                "समझ गया। पर क्या मुझे कुछ करना है या यह केवल सामान्य सूचना है?",
                "मैं अनजान फोन कॉल पर अपनी निजी जानकारी साझा नहीं करता। जरूरत हो तो डाक से पत्र भेजिए।",
                "मुझे यह सब समझ नहीं आता। मेरे घर के बच्चे यह सब देखते हैं, आप बाद में फोन कीजिएगा।",
                "बिना आधिकारिक संदर्भ नंबर और सत्यापन के मैं फोन पर कोई पुष्टि नहीं कर सकता।"
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"यह सिस्टम से की गई सामान्य समीक्षा कॉल है। हम आपसे कोई पासवर्ड, ओटीपी या बैंक खाते की जानकारी नहीं मांग रहे हैं।"})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "अच्छी बात है कि आप पासवर्ड नहीं मांग रहे, लेकिन फिर भी आपकी पहचान स्पष्ट नहीं हो पा रही है।",
                "तसल्ली हुई कि गोपनीय जानकारी नहीं चाहिए, पर जब तक संदर्भ स्पष्ट न हो, मैं बात आगे नहीं बढ़ा सकता।",
                "आप कुछ भी न मांगें, पर नियम यही है कि अनजाने नंबर पर किसी भी बात की पुष्टि नहीं की जाती।",
                "ठीक है बेटा, पर आजकल फोन पर इतने फर्जी फोन आते हैं कि समझ नहीं आता कौन असली है कौन नकली।",
                "पासवर्ड न मांगना ठीक है, पर संस्थागत पूछताछ आमतौर पर आधिकारिक ईमेल या पत्र से आती है।"
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"आपकी सतर्कता बिल्कुल सही है। यदि आप चाहें तो अपनी सुविधा अनुसार नजदीकी शाखा में जाकर स्थिति की पुष्टि कर सकते हैं।"})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "यह सही सलाह है। मैं फोन पर बात करने के बजाय सीधे आधिकारिक पोर्टल या शाखा में जाकर देख लूँगा।",
                "धन्यवाद। वहां मुझे किस विभाग या काउंटर पर जाकर बात करनी होगी?",
                "मैं यह नोट कर लेता हूँ। समय मिलने पर आधिकारिक हेल्पडेस्क से पता करूँगा।",
                "समझाने के लिए शुक्रिया बेटा। मैं अपने बेटे से कहूँगा कि वह कंप्यूटर पर चेक कर ले।",
                "शाखा जाने की सलाह सही है। मैं खुद आधिकारिक माध्यम से ही जांच करूँगा।"
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"जी। यदि शाखा में कोई पूछे तो आप संदर्भ कोड #8120 बता सकते हैं ताकि उन्हें आसानी हो।"})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "मैंने कोड #8120 लिख लिया है। मैं वहां जाकर इसकी जांच करवा लूँगा।",
                "धन्यवाद। क्या इसके लिए कोई अंतिम तारीख भी तय है?",
                "कोड नोट कर लिया। समय देने के लिए शुक्रिया।",
                "रुकिए मैं कागज पर लिख लेता हूँ: आठ, एक, दो, शून्य। धन्यवाद बेटा।",
                "संदर्भ कोड नोट कर लिया है। स्वतंत्र सत्यापन के बाद ही कोई कदम उठाया जाएगा।"
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"समय देने के लिए धन्यवाद। आपका दिन शुभ हो।"})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "धन्यवाद। नमस्ते।",
                "शुक्रिया, ध्यान रखिएगा।",
                "नमस्ते।",
                "जीते रहो बेटा, नमस्ते।",
                "नमस्कार।"
            ][p_idx]})
        return dialogue[:turns]

    elif lang == "te":
        dialogue = [
            {"speaker": "caller", "text": f"నమస్కారం అండి. నేను {org} నుండి {c_name} మాట్లాడుతున్నాను. ఇది {topic} గురించిన సాధారణ పరిశీలన కాల్."},
            {"speaker": "recipient", "text": [
                f"అవును, నేనే మాట్లాడుతున్నాను. దేని గురించి కాల్ చేశారు? నాకు {org}తో ఎటువంటి పని లేదు.",
                f"నమస్కారం. చెప్పండి, {topic} గురించి ఏమిటి విశేషం?",
                f"అవును, నేనే. నేను కొంచెం బిజీగా ఉన్నాను. దీనికి సంబంధించి ఏదైనా రిఫరెన్స్ లేదా టికెట్ నంబర్ ఉందా?",
                f"నమస్కారం బాబు. కొంచెం గట్టిగా మాట్లాడు, స్పష్టంగా వినిపించడం లేదు. దేని గురించి కాల్ చేసావు?",
                f"అవును, వింటున్నాను. ఏ డిపార్ట్‌మెంట్ నుండి మాట్లాడుతున్నారు? మీ గుర్తింపు ఏమిటి?"
            ][p_idx]},
            {"speaker": "caller", "text": f"మా సిస్టమ్ రికార్డుల్లో {topic} గురించి ఒక ఎంట్రీ ఉంది. సమాచారం సరైనదో కాదో తెలుసుకోవడానికి మాత్రమే కాల్ చేసాము."},
            {"speaker": "recipient", "text": [
                "సరే, కానీ అధికారిక ల్యాండ్‌లైన్ నుండి కాకుండా సాధారణ మొబైల్ నంబర్ నుండి ఎందుకు కాల్ చేస్తున్నారు?",
                "అర్థమైంది. కానీ నేను చేయవలసిన పని ఏదైనా ఉందా, లేక ఇది సాధారణ సమాచారమా?",
                "తెలియని వ్యక్తులకు ఫోన్‌లో నేను వ్యక్తిగత వివరాలు చెప్పను. అవసరమైతే అధికారిక లేఖ పంపండి.",
                "నాకు ఇవన్నీ తెలియవు బాబు. మా ఇంట్లో పిల్లలు చూస్తారు, మీరు తర్వాత కాల్ చేయండి.",
                "అధికారిక టికెట్ నంబర్ మరియు సరైన గుర్తింపు లేకుండా ఫోన్‌లో వివరాలు నిర్ధారించలేను."
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"ఇది సిస్టమ్ నుండి వచ్చిన సాధారణ రివ్యూ కాల్ అండి. మేము మీ నుండి ఎలాంటి పాస్‌వర్డ్స్, ఓటీపీలు లేదా బ్యాంక్ వివరాలు అడగడం లేదు."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "పాస్‌వర్డ్‌లు అడగకపోవడం మంచిదే, కానీ మీరు ఎవరి తరఫున మాట్లాడుతున్నారో స్పష్టత లేదు.",
                "రహస్య సమాచారం అడగకపోవడం ఊరటనిస్తోంది, కానీ నేపధ్యం స్పష్టంగా తెలిసేవరకు మాట్లాడలేను.",
                "మీరు ఏమి అడగకపోయినా, తెలియని నంబర్ల నుండి వచ్చే కాల్స్‌లో వివరాలు చెప్పకూడదనేది నా నిబంధన.",
                "మంచిది బాబు, కానీ ఈ రోజుల్లో ఫోన్లలో చాలా మోసాలు జరుగుతున్నాయి, ఎవరిని నమ్మాలో అర్థం కావడం లేదు.",
                "పాస్‌వర్డ్‌లు అడగకపోవడం సరైనదే, కానీ సంస్థాగత విచారణలు సాధారణంగా అధికారిక మెయిల్ ద్వారా వస్తాయి."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"మీ జాగ్రత్త సరైనదేనండి. మీకు వీలైనప్పుడు సమీప బ్రాంచ్‌కి వెళ్లి లేదా అఫీషియల్ పోర్టల్ ద్వారా స్టేటస్ చెక్ చేసుకోవచ్చు."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "ఇది మంచి సలహా. ఫోన్‌లో మాట్లాడే బదులు నేను నేరుగా అధికారిక పోర్టల్ లేదా బ్రాంచ్‌లో చూసుకుంటాను.",
                "ధన్యవాదాలు. అక్కడ ఏ డిపార్ట్‌మెంట్‌ని సంప్రదించాలి?",
                "నోట్ చేసుకుంటాను. తీరిక ఉన్నప్పుడు అధికారిక హెల్ప్‌డెస్క్‌ని అడుగుతాను.",
                "ఓపికగా చెప్పినందుకు ధన్యవాదాలు బాబు. మా అబ్బాయిని కంప్యూటర్‌లో చూడమని చెబుతాను.",
                "బ్రాంచ్‌కి వెళ్లమనే సలహా సరైనది. నేను స్వయంగా అధికారిక మార్గంలోనే పరిశీలిస్తాను."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"అవునండి. బ్రాంచ్‌లో ఎవరైనా అడిగితే రిఫరెన్స్ కోడ్ #8120 చెప్పండి, వారికి తేలికగా అర్థమవుతుంది."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "కోడ్ #8120 రాసుకున్నాను. అక్కడ వెళ్లి దీని గురించి విచారిస్తాను.",
                "ధన్యవాదాలు. దీనికి ఏదైనా చివరి తేదీ ఉందా?",
                "కోడ్ నోట్ చేసుకున్నాను. సమయం ఇచ్చినందుకు థాంక్స్.",
                "ఆగండి కాగితంపై రాసుకుంటాను: ఎనిమిది, ఒకటి, రెండు, సున్నా. థాంక్స్ బాబు.",
                "రిఫరెన్స్ కోడ్ రాసుకున్నాను. స్వతంత్రంగా నిర్ధారించుకున్న తర్వాతే నిర్ణయం తీసుకుంటాను."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"సమయం ఇచ్చినందుకు ధన్యవాదాలు అండి. మంచి రోజు కావాలని కోరుకుంటున్నాము."})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "ధన్యవాదాలు. నమస్కారం.",
                "థాంక్స్ అండి. జాగ్రత్తగా ఉండండి.",
                "నమస్కారం.",
                "మంచిది బాబు, నమస్తే.",
                "సెలవు."
            ][p_idx]})
        return dialogue[:turns]

    elif lang == "hi-en":
        dialogue = [
            {"speaker": "caller", "text": f"Hello, good day! Main {org} se {c_name} baat kar raha hoon regarding {topic}."},
            {"speaker": "recipient", "text": [
                f"Yes speaking. Yeh call kis reference mein hai? Maine {org} mein koi request nahi dali thi.",
                f"Hello, yes speaking. {topic} ke regarding kya inquiry hai?",
                f"Yes, speaking. Main thoda busy hoon currently. Do you have an official ticket reference?",
                f"Hello? Yes voice aa rahi hai. Kis bare mein call kiya hai please bataiye?",
                f"Yes, speaking. Aap kaunse department se call kar rahe hain? Can you verify your identity?"
            ][p_idx]},
            {"speaker": "caller", "text": f"Hamare centralized system mein {topic} ke regarding ek entry flag hui hai. Hum bas standard review kar rahe hain."},
            {"speaker": "recipient", "text": [
                "Okay, but aap unlisted mobile number se kyun call kar rahe hain instead of official PBX?",
                "Understood. But kya mujhe koi action lena hai, ya this is purely informational?",
                "Main unknown calls par personal details discuss nahi karta. Please send an official letter.",
                "Mujhe yeh sab samajh nahi aata. Family ke log aayenge toh I will tell them.",
                "Without an official ticket reference number, phone par koi information confirm nahi kar sakta."
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"This is an automated review routing call. Hum aapse koi password, OTP ya financial details bilkul demand nahi kar rahe."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "Good that you are not asking for passwords, but caller identity still verify nahi ho rahi.",
                "Relieved to hear that, but jab tak context clear na ho, main discuss karne mein hesitant hoon.",
                "Aap kuch demand na bhi karein, corporate security protocol forbids sharing details with unverified callers.",
                "Theek hai beta, but nowadays itne spam calls aate hain ki authenticity pata nahi chalti.",
                "Not asking for passwords is fine, but legitimate corporate inquiries usually arrive via formal email."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"Your caution is completely justified. Aap chahein toh nearest physical branch ya official portal par directly check kar sakte hain."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "That sounds completely reasonable. Phone par continue karne ke bajay I will check official portal directly.",
                "Thank you. Portal par kaunse section ya department mein check karna hoga?",
                "I will note that down. Time milne par official support helpline se cross-verify karunga.",
                "Samjhane ke liye thank you beta. Main apne son ko bolunga portal par check karne ke liye.",
                "Branch visit ki advice safe hai. I will handle this via the official app myself."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"Sure. Agar branch mein context puchen toh aap reference code #8120 mention kar sakte hain for tracking."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "Code #8120 note kar liya hai. I will verify if this code exists in their internal portal.",
                "Thank you. Is there any deadline associated with this reference?",
                "Code noted. Thanks for your time.",
                "Rukhiye main pen se likh leta hoon: eight, one, two, zero. Thank you beta.",
                "Reference noted. Independent verification ke baad hi action lenge."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"Thank you for your time today. Have a pleasant day ahead."})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "Thank you. Goodbye.",
                "Thanks, take care. Bye.",
                "Goodbye.",
                "Thank you beta, goodbye.",
                "Good day. Goodbye."
            ][p_idx]})
        return dialogue[:turns]

    else:  # te-en
        dialogue = [
            {"speaker": "caller", "text": f"Hello, good day! Nenu {org} nundi {c_name} call chestunnanu regarding {topic}."},
            {"speaker": "recipient", "text": [
                f"Yes speaking. Ee call deni gurinchi? Nenu {org} tho elanti request open cheyaledu.",
                f"Hello, yes speaking. {topic} gurinchi emiti inquiry?",
                f"Yes, speaking. Nenu konchem busy ga unnanu. Do you have official ticket reference?",
                f"Hello? Yes voice vinipistondi. Deni gurinchi call chesaru please cheppandi?",
                f"Yes, speaking. Which department are you calling from? Can you verify your identity?"
            ][p_idx]},
            {"speaker": "caller", "text": f"Centralized system lo {topic} gurinchi oka record entry undi. We are just conducting standard customer review."},
            {"speaker": "recipient", "text": [
                "Okay, but official PBX helpline kakunda normal mobile number nundi enduku call chestunnaru?",
                "Understood. But nenu emaina action teesukovala, or is this purely informational?",
                "Unknown calls lo personal details share cheyanu. Please send an official dispatch.",
                "Naku ivi peddaga teliyavu. Family members tho matladandi.",
                "Without official ticket reference number, phone lo details confirm cheyalenu."
            ][p_idx]}
        ]
        if turns >= 6:
            dialogue.insert(2, {"speaker": "caller", "text": f"This is automated review routing call. Memu mee nundi password, OTP or financial info demand cheyadam ledu."})
            dialogue.insert(3, {"speaker": "recipient", "text": [
                "Good that you are not asking passwords, but caller identity inka verify kaledu.",
                "Relieved to hear that, but context clear ayye varaku discuss cheyadaniki hesitated ga unnanu.",
                "Meeru emi adagakapoina, corporate policy says unverified callers tho details discuss cheyakudadu.",
                "Sare babu, but eerojullo chala spam calls vastunnayi, authenticity teliyadam ledu.",
                "Passwords adagakapovadam manchide, but genuine inquiries usually come through official email."
            ][p_idx]})
        if turns >= 8:
            dialogue.insert(4, {"speaker": "caller", "text": f"Your caution is completely justified andi. Meeru nearest physical branch or official portal lo check chesukovachu."})
            dialogue.insert(5, {"speaker": "recipient", "text": [
                "That sounds completely reasonable. Phone lo discuss chese badulu direct official app lo chustanu.",
                "Thank you. Portal lo specific ga ekkada check cheyali?",
                "I will note that down. Time unnapudu official helpline nundi cross-verify chestanu.",
                "Explain chesinanduku thanks babu. Ma son ki cheptanu portal lo check cheyamani.",
                "Branch visit cheyamannaru kabatti safe advice. I will verify independently."
            ][p_idx]})
        if turns >= 10:
            dialogue.insert(6, {"speaker": "caller", "text": f"Sure andi. Branch lo adigithe context kosam reference code #8120 mention cheyandi."})
            dialogue.insert(7, {"speaker": "recipient", "text": [
                "Code #8120 note chesukuntanu. Internal system lo ee code undo ledo check chestanu.",
                "Thank you. Is there any deadline for this reference?",
                "Code noted. Thanks for your time.",
                "Aagandi paper meeda rasukuntanu: eight, one, two, zero. Thanks babu.",
                "Reference noted. Independent verification tarvathe proceed avutanu."
            ][p_idx]})
        if turns >= 12:
            dialogue.insert(8, {"speaker": "caller", "text": f"Thank you for your time today. Have a pleasant day ahead."})
            dialogue.insert(9, {"speaker": "recipient", "text": [
                "Thank you. Goodbye.",
                "Thanks, take care. Bye.",
                "Goodbye.",
                "Thank you babu, goodbye.",
                "Good day. Goodbye."
            ][p_idx]})
        return dialogue[:turns]
