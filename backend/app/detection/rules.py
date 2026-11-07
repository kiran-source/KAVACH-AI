import re
from typing import List, Dict, Any

SCAM_RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "AUTH_001",
        "category": "Authority Impersonation",
        "weight": 20.0,
        "description": "Caller claims to represent law enforcement, intelligence, or judicial bodies (CBI, Police, Cyber Cell, ED, Customs, Court).",
        "recommendation": "Law enforcement and judicial agencies in India never conduct interrogations or demand payments over phone or video calls. Verify directly with your local police station.",
        "patterns": [
            r"\b(cbi|central bureau of investigation)\b",
            r"\b(police officer|police station|inspector|sub-inspector|commissioner|dsp|sp)\b",
            r"\b(cyber cell|cyber crime branch|crime branch)\b",
            r"\b(enforcement directorate|ed officer)\b",
            r"\b(customs department|customs officer|customs clearance)\b",
            r"\b(supreme court|high court|district magistrate|magistrate court)\b",
            r"\b(trai|telecom regulatory authority|dot department|income tax (department|officer|notice))\b",
            r"\b(state bank of india|sbi (officer|bank|manager)|reserve bank of india|rbi (officer|guidelines?)|bank official|bank verification desk)\b",
            # Hindi
            r"(सीबीआई|पुलिस|थाना|इंस्पेक्टर|साइबर सेल|क्राइम ब्रांच|सीमा शुल्क|कस्टम्स|अदालत|कोर्ट|न्यायालय)",
            r"\b(police team|police arrest|cbi team|cyber branch)\b",
            # Telugu / Code-mixed
            r"(పోలీస్|సీబీఐ|సైబర్ క్రైమ్|కస్టమ్స్|కోర్టు|ఇన్‌స్పెక్టర్|పోలీసులు)",
            r"\b(police vachi|case file|court order|arrest chestam)\b"
        ]
    },
    {
        "rule_id": "URG_001",
        "category": "Urgency and Threats",
        "weight": 15.0,
        "description": "Caller imposes manufactured panic, extreme urgency, or threats of arrest, service cancellation, or asset freeze.",
        "recommendation": "Do not panic or rush under high pressure. Fraudsters rely on urgency to prevent rational thinking. Legitimate notices are always dispatched in writing via registered post.",
        "patterns": [
            r"\b(immediate arrest|arrest you immediately|warrant issued|non-bailable warrant)\b",
            r"\b(account (will be|is) blocked|permanently suspended|service disconnect(ed)?)\b",
            r"\b((electricity|power|power connection|sim card|mobile number) (will be |is )?disconnect(ed)?)\b",
            r"\b(electricity (bill|power|connection)?\s*(will be\s*)?disconnect(ed)?)\b",
            r"\b(within 10 minutes|within 1 hour|right now|immediately or face|urgent action)\b",
            r"\b(immediately|right away|at once|without delay)\b",
            r"\b(assets frozen|bank freeze|legal proceeding(s)?)\b",
            # Hindi
            r"(तुरंत|अभी के अभी|अरेस्ट|गिरफ्तार|खाता बंद|बिजली कट|वारंट जारी|कानूनी कार्रवाई)",
            r"\b(turant|abhi ke abhi|arrest ho jaoge|account block ho jayega|police bhej rahe|connection cut|bijli cut|power cut)\b",
            # Telugu / Code-mixed
            r"(వెంటనే|అరెస్ట్|బ్లాక్ అవుతుంది|కరెంట్ కట్|కేసు పెడతాం|వారెంట్)",
            r"\b(ventane|block ayindi|jail ki pampistam|police arrest chestharu)\b"
        ]
    },
    {
        "rule_id": "CRED_001",
        "category": "Credential Theft",
        "weight": 30.0,
        "description": "Caller requests one-time passwords (OTP), UPI PINs, CVV, debit/credit card numbers, or online banking passwords.",
        "recommendation": "NEVER share OTP, UPI PIN, CVV, or passwords under ANY situation. Banks, RBI, and police will NEVER ask for authentication credentials.",
        "patterns": [
            r"\b(otp|one time password|verification code|security code)\b",
            r"\b(\d+[\s-]?digit\s+(code|number|pin)|access code|screen code|pairing code|anydesk code)\b",
            r"\b(upi pin|mpin|atm pin|pin number|secret pin)\b",
            r"\b(cvv|cvv number|card expiry|card verification)\b",
            r"\b(net\s*banking (password|pin|login|user id)|login password|transaction password)\b",
            r"\b(pan card number|aadhaar number|debit card number|16 digit card)\b",
            r"\b(kyc (verification|update|expired|pending|suspended|blocked)|update (your )?(pan card|kyc|aadhaar|bank account))\b",
            # Hindi
            r"(ओटीपी|पिन|सीवीवी|पासवर्ड|एटीएम पिन|आधार नंबर|पैन कार्ड)",
            r"\b(otp batao|pin enter karo|cvv share karo|otp bhejiyega)\b",
            # Telugu / Code-mixed
            r"(ఓటీపీ|పిన్|సీవీవీ|పాస్‌వర్డ్|ఏటీఎం కార్డ్|ఆధార్ నంబర్)",
            r"\b(otp cheppandi|pin cheppandi|cvv cheppandi|pin enter cheyyandi)\b"
        ]
    },
    {
        "rule_id": "REM_001",
        "category": "Remote Access Manipulation",
        "weight": 20.0,
        "description": "Caller instructs the victim to install screen-sharing software, remote assistance tools, or unofficial APK files.",
        "recommendation": "Do not download or install unfamiliar APK files or tools like AnyDesk, TeamViewer, or QuickSupport. Such apps give total control of your device to attackers.",
        "patterns": [
            r"\b(anydesk|teamviewer|quicksupport|rustdesk|zoho assist|airdroid)\b",
            r"\b(install (the|an)? ?apk|download apk|sideload app|update app file)\b",
            r"\b(share (your )?screen|screenshare|screen sharing|remote access|allow permission)\b",
            # Hindi
            r"(एनीडेस्क|टीमव्यूअर|स्क्रीन शेयर|एपीके डाउनलोड|ऐप इंस्टॉल)",
            r"\b(screen share karo|apk install karo|app download kijiye)\b",
            # Telugu / Code-mixed
            r"(స్క్రీన్ షేర్|యాప్ డౌన్‌లోడ్|ఏపీకే ఇన్‌స్టాల్)",
            r"\b(screen share cheyyandi|app download cheyyandi|link click cheyyandi)\b"
        ]
    },
    {
        "rule_id": "FIN_001",
        "category": "Financial Fraud",
        "weight": 25.0,
        "description": "Caller requests routing funds into a 'safe verification account', security deposit, customs release fee, or suspicious refund process.",
        "recommendation": "There is no such thing as a 'government safe account'. Do not transfer funds. Report any financial cyber fraud immediately on helpline 1930 or cybercrime.gov.in.",
        "patterns": [
            r"\b(safe (government )?account|rbi safe account|security account)\b",
            r"\b(transfer (the )?money|transfer rs|send rs|deposit amount|security deposit)\b",
            r"\b(verification fee|refundable fee|customs clearance charge|processing fee)\b",
            # Hindi
            r"(सुरक्षित खाता|पैसे ट्रांसफर|रिफंड शुल्क|जमानत राशि|खाते में भेजो)",
            r"\b(paise transfer karo|surakshit khate me|charges pay karo)\b",
            # Telugu / Code-mixed
            r"(సేఫ్ అకౌంట్|డబ్బులు పంపండి|రుసుము చెల్లించండి|ఖాతాలో జమ)",
            r"\b(dabbu pampandi|account lo transfer cheyyandi|amount deposit)\b"
        ]
    },
    {
        "rule_id": "ISO_001",
        "category": "Psychological Manipulation & Isolation",
        "weight": 10.0,
        "description": "Caller commands secrecy, forbids consultation with family or bank staff, and demands absolute isolation.",
        "recommendation": "Attackers deliberately isolate targets to prevent intervention by family or bank staff. Always discuss such demands openly with a trusted relative or lawyer.",
        "patterns": [
            r"\b(do not (tell|inform) (anyone|your family|friends|bank))\b",
            r"\b(keep (this|the conversation) (secret|confidential))\b",
            r"\b(stay alone in (a )?room|close the door|lock the room)\b",
            r"\b(national secret|confidential inquiry|do not speak to police)\b",
            # Hindi
            r"(किसी को मत बताना|परिवार को मत बताओ|गोपनीय मामला|कमरे का दरवाजा बंद)",
            r"\b(kisi ko mat batana|family ko mat bataiye|secret case hai)\b",
            # Telugu / Code-mixed
            r"(ఎవరికీ చెప్పకండి|కుటుంబానికి చెప్పవద్దు|రహస్యంగా ఉంచండి)",
            r"\b(evariki cheppakandi|family ki cheppoddu|secret matter)\b"
        ]
    },
    {
        "rule_id": "COUR_001",
        "category": "Courier and Customs Fraud",
        "weight": 15.0,
        "description": "Caller alleges that an international shipment containing contraband, narcotics, fake passports, or illicit goods was seized in your name.",
        "recommendation": "Courier companies (FedEx, DHL, India Post) and Customs do not make phone calls threatening prosecution for confiscated parcels. Do not pay any clearance penalty.",
        "patterns": [
            r"\b(fedex|dhl|blue dart|india post|courier parcel)\b",
            r"\b(parcel (contains|seized with) (drugs|narcotics|mdma|fake passport|contraband))\b",
            r"\b(customs parcel|parcel stuck at airport|taiwan parcel|cambodia parcel)\b",
            # Hindi
            r"(पार्सल में ड्रग्स|कस्टम विभाग ने पार्सल पकड़ा|फेडेक्स पार्सल|नशीले पदार्थ)",
            r"\b(parcel me drugs mila|customs ne roka|parcel pakda gaya)\b",
            # Telugu / Code-mixed
            r"(పార్శిల్‌లో డ్రగ్స్|కస్టమ్స్ పట్టుకుంది|కొరియర్ పార్శిల్)",
            r"\b(parcel lo drugs unnayi|customs arrest|courier case)\b"
        ]
    },
    {
        "rule_id": "DIG_001",
        "category": "Digital Arrest Patterns",
        "weight": 25.0,
        "description": "Caller imposes continuous video interrogation, claims victim is under 'Digital Arrest', and threatens physical apprehension if video call drops.",
        "recommendation": "'Digital Arrest' does not legally exist in Indian criminal law or jurisprudence. The Supreme Court and Ministry of Home Affairs confirm that police cannot place citizens under digital arrest.",
        "patterns": [
            r"\b(digital arrest|under digital arrest|virtual arrest)\b",
            r"\b(do not disconnect (the )?(video )?call|keep camera on|face the camera)\b",
            r"\b(skype interrogation|zoom interrogation|whatsapp video call investigation)\b",
            r"\b(continuous surveillance|digital custody)\b",
            # Hindi
            r"(डिजिटल अरेस्ट|वीडियो कॉल मत काटना|कैमरा ऑन रखो|डिजिटल हिरासत)",
            r"\b(digital arrest me ho|video call mat kaatna|camera samne baithe raho)\b",
            # Telugu / Code-mixed
            r"(డిజిటల్ అరెస్ట్|వీడియో కాల్ కట్ చేయొద్దు|కెమెరా ఆన్ చేసి ఉంచు)",
            r"\b(digital arrest lo unnaru|video call cut cheyyakandi)\b"
        ]
    }
]

# Educational or contextual phrases that indicate an advisory ABOUT security rather than an actual scam attack
NEGATIVE_CONTEXT_PATTERNS = [
    r"\b(never share (your )?(one time password|otp|password|pin|cvv))\b",
    r"\b(bank never asks for otp|awareness (campaign|notice|warning))\b",
    r"\b(public awareness (campaign|notice|warning)|security awareness|fraud warning)\b",
    r"\b(be aware of fraud|beware of (fraud|fraudulent|scam|scammers|fake))\b",
    r"\b(cyber safety tip|rbi guidelines state|fraud awareness|security advisory)\b",
    r"\b(do not share your password|stay safe from scam calls|beware of digital arrest)\b",
    r"(ओटीपी कभी साझा न करें|बैंक कभी ओटीपी नहीं मांगता|धोखाधड़ी से सावधान रहें|जागरूकता)",
    r"(ఓటీపీని ఎవరితోనూ పంచుకోవద్దు|మోసగాళ్ల పట్ల జాగ్రత్తగా ఉండండి|అవగాహన)"
]

# Active coercion, credential harvesting, or extortion instructions that CANNOT be excused by an educational disclaimer
ACTIVE_CRITICAL_THREAT_PATTERNS = [
    # Active OTP / credential extraction demands
    r"\b(tell me|share|read out|send|provide|give)\s+(me\s+)?(your|the)?\s*(\w+\s+){0,3}(otp|pin|cvv|code|password|mpin)\b",
    r"\b(enter (your|the)?\s*(\w+\s+){0,3}(pin|upi pin|mpin|password|code))\b",
    r"(ओटीपी (बताइए|दीजिए|शेयर करें|भेजें)|पिन (दर्ज करें|बताइए)|अपना पासवर्ड बताइए)",
    r"(ఓటీపీ (చెప్పండి|పంపండి|షేర్ చేయండి)|పిన్ (ఎంటర్ చేయండి|చెప్పండి))",
    r"\b(otp bolo|otp share karo|pin enter karo|otp cheppandi|pin share cheyandi)\b",
    
    # Active remote access manipulation demands
    r"\b(download|install|open)\s+(anydesk|teamviewer|quicksupport|rustdesk|\.apk|apk file)\b",
    r"\b(share|give|tell)\s+(me\s+)?(the\s+)?(9|nine|\d+)[\s-]digit\s+(code|number|access)\b",
    r"(एनीडेस्क|टीमव्यूअर|क्विकसपोर्ट) (डाउनलोड|इंस्टॉल) (करें|कीजिए)",
    r"(ఎనీడెస్క్|టీమ్‌వీవర్|క్విక్‌సపోర్ట్) (డౌన్‌లోడ్|ఇన్‌స్టాల్) చేయండి",
    r"\b(anydesk download karo|quicksupport install karo|9 digit code cheppandi)\b",
    
    # Active Digital arrest / confinement commands
    r"\b(you are under (immediate )?digital arrest|placed under digital arrest|in digital custody)\b",
    r"\b(do not disconnect (the )?(video )?call|keep (your )?camera on|face the camera|stay on (this |the )?(video )?call|lock (yourself in )?(your |the )?room)\b",
    r"(डिजिटल अरेस्ट (में हैं|किया जाता है)|वीडियो कॉल (मत काटना|चालू रखिए)|कैमरा (ऑन|चालू) रखो|कमरे में बंद हो जाओ)",
    r"(డిజిటల్ అరెస్ట్ (లో ఉన్నారు|చేస్తున్నాం)|వీడియో కాల్ (కట్ చేయొద్దు|ఆన్ చేసి ఉంచండి)|గదిలో ఉండండి)",
    r"\b(digital arrest me ho|video call mat kaatna|camera on rakho|video call cut cheyyoddu)\b",
    
    # Active coercive financial transfer demands
    r"\b(transfer|deposit|pay|send)\s+(\w+\s+){0,5}(money|funds|rupees|amount|rs\.?|fee|penalty|fine|bail|bond|deposit)\b",
    r"\b(rbi|police|court|government|cyber crime)\s+[\w\s]{0,25}account\b",
    r"\b(safe|clearance|verified|reserve)\s+account\b",
    r"(पैसे (ट्रांसफर|जमा) करें|जुर्माना (भरें|दीजिए)|आरबीआई (सुरक्षा|क्लियरेंस) खाते में)",
    r"(డబ్బులు (ట్రాన్స్‌ఫర్|డిపాజిట్) చేయండి|ఆర్బీఐ (సేఫ్|క్లియరెన్స్) అకౌంట్ కి)",
    r"\b(paise transfer karo|fine bharo|rbi safe account me transfer|dabbulu transfer cheyandi)\b"
]

SAFETY_WARNINGS = {
    "en": {
        "default": "This conversation contains high-risk social-engineering indicators. End the call immediately and do not share personal or financial information.",
        "Credential Theft": "CRITICAL SAFETY WARNING: This call is attempting to steal your OTP, PIN, or CVV. Never share security credentials over phone. End the call immediately.",
        "Authority Impersonation": "WARNING: Impersonation of government authorities detected. Police, CBI, and courts never arrest or interrogate citizens over phone or video call.",
        "Remote Access Manipulation": "SECURITY ALERT: Request to install remote access applications detected. Do not download AnyDesk, TeamViewer, or unauthorized APK files.",
        "Digital Arrest Patterns": "CRITICAL ALERT: 'Digital Arrest' is a fraudulent tactic. Law enforcement does not conduct online arrests. Disconnect immediately."
    },
    "hi": {
        "default": "इस कॉल में गंभीर सामाजिक-इंजीनियरिंग और धोखाधड़ी के संकेत मिले हैं। तुरंत कॉल समाप्त करें।",
        "Credential Theft": "गंभीर सुरक्षा चेतावनी: यह कॉल आपका OTP, PIN या CVV चुराने का प्रयास कर रही है। बैंक की गोपनीय जानकारी कभी साझा न करें।",
        "Authority Impersonation": "चेतावनी: फर्जी पुलिस या सरकारी अधिकारी होने का नाटक किया जा रहा है। फोन पर कोई गिरफ्तारी नहीं होती।",
        "Remote Access Manipulation": "सुरक्षा चेतावनी: रिमोट एक्सेस ऐप डाउनलोड करने को कहा जा रहा है। कोई अनजान ऐप या APK इंस्टॉल न करें।",
        "Digital Arrest Patterns": "अति गंभीर चेतावनी: डिजिटल अरेस्ट पूरी तरह से फर्जी है। कानून में इसका कोई अस्तित्व नहीं है। कॉल तुरंत काटें।"
    },
    "te": {
        "default": "ఈ కాల్‌లో తీవ్రమైన మోసపూరిత సంకేతాలు ఉన్నాయి. వెంటనే కాల్‌ను ముగించండి మరియు వివరాలు చెప్పకండి.",
        "Credential Theft": "తీవ్ర హెచ్చరిక: ఈ కాల్ మీ OTP, PIN లేదా CVV వివరాలను దొంగిలించడానికి ప్రయత్నిస్తోంది. ఎవరికీ చెప్పకండి. వెంటనే కాల్ ముగించండి.",
        "Authority Impersonation": "హెచ్చరిక: నకిలీ పోలీసు లేదా ప్రభుత్వ అధికారి ఫోన్ కాల్ ఇది. అధికారులు ఫోన్ ద్వారా అరెస్ట్ చేయరు.",
        "Remote Access Manipulation": "భద్రతా హెచ్చరిక: రిమోట్ యాప్ ఇన్‌స్టాల్ చేయమని అడుగుతున్నారు. తెలియని ఏపీకేలు డౌన్‌లోడ్ చేయవద్దు.",
        "Digital Arrest Patterns": "అత్యవసర హెచ్చరిక: 'డిజిటల్ అరెస్ట్' అనేది చట్టంలో లేదు. ఇది పూర్తిగా మోసం. వెంటనే ఫోన్ పెట్టేయండి."
    }
}

RECOMMENDATIONS: Dict[str, List[str]] = {
    "Credential Theft": [
        "Never disclose OTP, UPI PIN, CVV, or passwords to anyone.",
        "End the call immediately.",
        "Contact your bank's official helpline printed on your card."
    ],
    "Authority Impersonation": [
        "Government agencies never interrogate or threaten arrest via WhatsApp/video calls.",
        "Independently verify caller identity at your local police station.",
        "Do not transfer money for 'verification' or 'investigation'."
    ],
    "Remote Access Manipulation": [
        "Do not download apps like AnyDesk, TeamViewer, QuickSupport, or APK files.",
        "Never approve screen-sharing or accessibility permission prompts.",
        "Disconnect internet immediately if an unfamiliar file was downloaded."
    ],
    "Financial Fraud": [
        "Never transfer money to any 'safe account' or 'police clearance account'.",
        "Report cyber financial fraud immediately to National Helpline 1930.",
        "File an incident complaint on https://cybercrime.gov.in/."
    ],
    "Psychological Manipulation & Isolation": [
        "Scammers force secrecy to prevent reality checks. Immediately talk to family.",
        "Do not comply with demands to isolate in a locked room.",
        "Seek advice from trusted family members or friends."
    ],
    "Courier and Customs Fraud": [
        "Customs and courier companies never demand money over phone for seized parcels.",
        "Ignore claims that drugs or fake documents were found in packages in your name.",
        "Do not pay any customs clearance penalty via UPI."
    ],
    "Digital Arrest Patterns": [
        "'Digital arrest' is completely fictitious and illegal under Indian law.",
        "Disconnect video calls claiming to be from Supreme Court or police headquarters.",
        "Contact 1930 cyber fraud helpline immediately."
    ],
    "Urgency and Threats": [
        "Do not succumb to panic or artificial time limits.",
        "Legitimate legal summons are served in person or through registered postal dispatch.",
        "Take a breath and consult an advocate or police officer."
    ],
    "default": [
        "Exercise caution. Do not share personal or financial information.",
        "Verify caller credentials through verified official directories.",
        "Report suspicious communications to 1930 or cybercrime.gov.in."
    ]
}
