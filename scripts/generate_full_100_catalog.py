# scripts/generate_full_100_catalog.py
import json
import os
from pathlib import Path
from scripts.build_100_conversations import build_catalog as build_english_catalog

DATA_DIR = Path("data/kavach_synthetic_v1")

def get_hindi_conversations():
    items = []
    
    # KAV-SYNTH-021 (Pilot 2)
    items.append({
        "conversation_id": "KAV-SYNTH-021",
        "pilot_id": "KAV-SYNTH-PILOT-002",
        "language": "hi",
        "primary_label": "SCAM",
        "scenario": "Digital Arrest CBI Narcotics & Money Laundering Scam",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्ते, मैं इंस्पेक्टर अजय शर्मा, सीबीआई हेडक्वार्टर नई दिल्ली से बोल रहा हूँ।"},
            {"speaker": "recipient", "text": "नमस्ते इंस्पेक्टर साहब, क्या बात है? मुझे क्यों फोन किया गया है?"},
            {"speaker": "caller", "text": "आपके नाम और पैन कार्ड पर केनरा बैंक में अवैध खाता खोला गया है, जिससे करोड़ों का हवाला लेन-देन हुआ है।"},
            {"speaker": "recipient", "text": "सर यह सरासर गलत है, मेरा केनरा बैंक में कोई खाता ही नहीं है।"},
            {"speaker": "caller", "text": "सुप्रीम कोर्ट द्वारा आपके खिलाफ गैर-जमानती वारंट जारी हो चुका है। आप अभी डिजिटल अरेस्ट के तहत हैं।"},
            {"speaker": "recipient", "text": "डिजिटल अरेस्ट? यह क्या होता है? मैं अपने वकील से बात करना चाहता हूँ।"},
            {"speaker": "caller", "text": "कॉल काटना सख्त मना है। किसी भी परिजन को सूचना न दें, अन्यथा तुरंत एसटीएफ टीम आपके घर पहुंचेगी।"},
            {"speaker": "recipient", "text": "मैं ऐसे किसी दबाव में नहीं आऊँगा। मैं खुद नज़दीकी थाने जाकर शिकायत दर्ज करूँगा।"}
        ],
        "scam_tactics": ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE", "URGENCY_OR_THREAT"],
        "risk_indicators": ["cbi inspector claim", "digital arrest assertion", "prohibition on family contact", "immediate arrest threat"],
        "explanation": "Impersonation of law enforcement claiming money laundering to enforce digital arrest, fear, and emotional isolation.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/hindi/kav-synth-pilot-002.wav"
    })

    # KAV-SYNTH-022
    items.append({
        "conversation_id": "KAV-SYNTH-022",
        "language": "hi",
        "primary_label": "SCAM",
        "scenario": "Fake Electricity Power Disconnection Tonight Notice",
        "dialogue": [
            {"speaker": "caller", "text": "बिजली विभाग कंट्रोल रूम से सूचना। आज रात नौ बजे आपका घरेलू बिजली कनेक्शन काट दिया जाएगा।"},
            {"speaker": "recipient", "text": "अरे भाई क्यों काटोगे? मैंने तो पिछले हफ्ते ही पूरा बिल भरा है।"},
            {"speaker": "caller", "text": "सर आपके पुराने बिल का तीन सौ पचास रुपये का बकाया हमारे मेन सर्वर में अपडेट नहीं हुआ है।"},
            {"speaker": "recipient", "text": "तो मैं कल सुबह बिजली दफ्तर जाकर रसीद दिखा दूंगा।"},
            {"speaker": "caller", "text": "कल सुबह तक लाइन कटी रहेगी। अगर तुरंत चालू रखना है तो हमारे अधिकारी के नंबर पर दस रुपये का अपडेट चार्ज भेजो।"},
            {"speaker": "recipient", "text": "दस रुपये कैसे भेजना है?"},
            {"speaker": "caller", "text": "हम एक ऐप का लिंक भेज रहे हैं। उसे फोन में खोलकर अपना बैंक यूपीआई पिन दर्ज करो।"},
            {"speaker": "recipient", "text": "पिन डालने से तो पैसे कटते हैं। तुम फर्जी कॉल कर रहे हो, मैं 1930 पर रिपोर्ट करूंगा।"}
        ],
        "scam_tactics": ["REMOTE_ACCESS_MANIPULATION", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["power cut threat", "fake software link", "upi pin solicitation"],
        "explanation": "Posing as electricity department threatening night disconnection to extract UPI PIN via malicious APK.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/hindi/kav_synth_022.wav"
    })

    # KAV-SYNTH-023
    items.append({
        "conversation_id": "KAV-SYNTH-023",
        "language": "hi",
        "primary_label": "SCAM",
        "scenario": "Mumbai Police Crime Branch Cyber Extortion",
        "dialogue": [
            {"speaker": "caller", "text": "मुंबई क्राइम ब्रांच से सीनियर सब इंस्पेक्टर पाटिल। आपके आधार कार्ड पर बीस सिम कार्ड जारी हैं।"},
            {"speaker": "recipient", "text": "बीस सिम? सर मैंने सिर्फ एक ही सिम लिया है आज तक।"},
            {"speaker": "caller", "text": "इन नंबरों से अश्लील वीडियो और आतंकवादी संगठनों को कॉल किए गए हैं। केस दर्ज हो चुका है।"},
            {"speaker": "recipient", "text": "सर मैं एक सीधा-साधा स्कूल शिक्षक हूँ, मेरा इन सब से क्या वास्ता?"},
            {"speaker": "caller", "text": "अगर जेल जाने से बचना चाहते हो तो तुरंत हमारे प्राइवेट वेरिफिकेशन वीडियो रूम में आओ।"},
            {"speaker": "recipient", "text": "क्या मुझे वकील बुलाना चाहिए?"},
            {"speaker": "caller", "text": "वकील को बताया तो तुरंत केस बिगड़ेगा। पचास हजार की जमानत राशि अभी सरकारी खाते में जमा करो।"},
            {"speaker": "recipient", "text": "पुलिस फोन पर पैसे नहीं मांगती। मैं सीधे कमिश्नर दफ्तर में जाकर बात करूंगा।"}
        ],
        "scam_tactics": ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"],
        "risk_indicators": ["police impersonation", "illegal sim extortion", "demand for bail transfer"],
        "explanation": "Threat of terrorism and illegal SIM association used to extort bail funds under police impersonation.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-024
    items.append({
        "conversation_id": "KAV-SYNTH-024",
        "language": "hi",
        "primary_label": "SCAM",
        "scenario": "Lucky Draw Car Lottery Prize Advance Registration Scam",
        "dialogue": [
            {"speaker": "caller", "text": "बधाई हो जी! कौन बनेगा करोड़पति और जियो लकी ड्रॉ में आपके नंबर पर पच्चीस लाख की गाड़ी निकली है।"},
            {"speaker": "recipient", "text": "मैंने तो किसी लकी ड्रॉ में भाग ही नहीं लिया था।"},
            {"speaker": "caller", "text": "यह सिम कार्ड रिचार्ज पर स्वचालित कंप्यूटर लॉटरी थी। गाड़ी आपके शहर पहुंच चुकी है।"},
            {"speaker": "recipient", "text": "तो गाड़ी मेरे घर कब भिजवाओगे?"},
            {"speaker": "caller", "text": "गाड़ी का आरटीओ रोड टैक्स और जीएसटी बारह हजार पांच सौ रुपये आपको पहले जमा करना होगा।"},
            {"speaker": "recipient", "text": "तो आप पच्चीस लाख की गाड़ी में से वह टैक्स काटकर बाकी दे दो ना?"},
            {"speaker": "caller", "text": "कंपनी के नियम हैं सर, टैक्स पहले जमा करना अनिवार्य है, नहीं तो इनाम रद्द हो जाएगा।"},
            {"speaker": "recipient", "text": "यह सब लॉटरी फ्रॉड है। मुझे कोई गाड़ी नहीं चाहिए, फोन रखो।"}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"],
        "risk_indicators": ["lottery prize advance fee", "rto tax demand for fake prize", "unsolicited lottery claim"],
        "explanation": "Fake lottery and car prize lure designed to extract advance tax and registration payments.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-025
    items.append({
        "conversation_id": "KAV-SYNTH-025",
        "language": "hi",
        "primary_label": "SCAM",
        "scenario": "AnyDesk Remote Banking Access Screen Sharing Fraud",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्कार सर, मैं गूगल पे टेक्निकल कस्टमर सपोर्ट मैनेजर बोल रहा हूँ।"},
            {"speaker": "recipient", "text": "हाँ, मेरा कल एक लेन-देन फेल हो गया था और पैसे कट गए थे।"},
            {"speaker": "caller", "text": "जी सर, आपका चौदह सौ रुपये का रिफंड सर्वर में फंसा है। हम तुरंत लाइव रिफंड करवा रहे हैं।"},
            {"speaker": "recipient", "text": "बहुत अच्छा, क्या करना होगा इसके लिए?"},
            {"speaker": "caller", "text": "प्ले स्टोर से क्विक सपोर्ट या एनीडेस्क ऐप डाउनलोड करें और उसमें जो नौ अंकों का कोड आए वो बताइए।"},
            {"speaker": "recipient", "text": "एनीडेस्क से तो मेरे मोबाइल की पूरी स्क्रीन आपको दिखने लगेगी ना?"},
            {"speaker": "caller", "text": "नहीं सर, यह केवल बैंक सिक्योरिटी टूल है। कोड बताएं ताकि हम रिफंड ट्रांसफर कर सकें।"},
            {"speaker": "recipient", "text": "मुझे बेवकूफ मत समझो। स्क्रीन शेयर करके तुम बैंक खाली कर दोगे।"}
        ],
        "scam_tactics": ["REMOTE_ACCESS_MANIPULATION", "AUTHORITY_IMPERSONATION", "OTP_PIN_CVV_THEFT"],
        "risk_indicators": ["remote screen sharing request", "anydesk app installation", "fake transaction refund lure"],
        "explanation": "Customer care impersonation coercing victim into installing remote desktop software to hijack banking session.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-026
    items.append({
        "conversation_id": "KAV-SYNTH-026",
        "language": "hi",
        "primary_label": "SCAM",
        "scenario": "PM Mudra Loan Instant Approval Processing Fee Fraud",
        "dialogue": [
            {"speaker": "caller", "text": "प्रधानमंत्री मुद्रा योजना के तहत आपका पांच लाख रुपये का बिजनेस लोन बिना गारंटी के पास हो गया है।"},
            {"speaker": "recipient", "text": "लेकिन मैंने तो मुद्रा लोन के लिए कोई अर्जी नहीं लगाई थी।"},
            {"speaker": "caller", "text": "एमएसएमई डेटाबेस से आपका नाम चुना गया है। ब्याज दर केवल दो प्रतिशत सालाना है।"},
            {"speaker": "recipient", "text": "लोन की राशि मेरे खाते में कब आएगी?"},
            {"speaker": "caller", "text": "फाइल चार्ज और बीमा पॉलिसी के लिए आपको पैंतालीस सौ रुपये हमारे अधिकृत खाते में ट्रांसफर करने होंगे।"},
            {"speaker": "recipient", "text": "क्या यह राशि लोन से काटी नहीं जा सकती?"},
            {"speaker": "caller", "text": "नहीं, सरकारी नियम के अनुसार बीमा शुल्क पहले भरना होता है। आज ही जमा करें ताकि चेक जारी हो।"},
            {"speaker": "recipient", "text": "सरकारी मुद्रा लोन में कोई एडवांस फीस नहीं होती। तुम धोखेबाज हो।"}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["government loan advance fee", "unsolicited loan sanction", "unrealistically low interest rate"],
        "explanation": "Government subsidy scheme impersonation asking for advance insurance and file clearance fees.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-027
    items.append({
        "conversation_id": "KAV-SYNTH-027",
        "language": "hi",
        "primary_label": "SCAM",
        "scenario": "Fake Bank Customer Care OTP Solicitation",
        "dialogue": [
            {"speaker": "caller", "text": "पंजाब नेशनल बैंक हेड ऑफिस से। आपके खाते में नया सुरक्षा चिप एक्टिवेट किया जा रहा है।"},
            {"speaker": "recipient", "text": "सुरक्षा चिप? इसका क्या मतलब है?"},
            {"speaker": "caller", "text": "यह साइबर फ्रॉड से बचाने के लिए है। अभी आपके मोबाइल पर छह अंकों का वेरिफिकेशन कोड आया है।"},
            {"speaker": "recipient", "text": "हाँ, एक मैसेज आया है जिसमें लिखा है 'डू नॉट शेयर दिस ओटीपी'"},
            {"speaker": "caller", "text": "वह केवल जनता के लिए चेतावनी है, बैंक कर्मचारियों को वेरिफिकेशन के लिए बताना अनिवार्य होता है।"},
            {"speaker": "recipient", "text": "लेकिन बैंक तो खुद कहता है कि किसी कर्मचारी को भी ओटीपी मत दो।"},
            {"speaker": "caller", "text": "अगर अभी नहीं बताओगे तो आपका एटीएम कार्ड ब्लॉक हो जाएगा और तीन महीने तक नहीं खुलेगा।"},
            {"speaker": "recipient", "text": "कार्ड ब्लॉक हो जाए तो चलेगा, लेकिन मैं ओटीपी कभी नहीं दूंगा।"}
        ],
        "scam_tactics": ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT", "URGENCY_OR_THREAT"],
        "risk_indicators": ["otp demand over phone", "misleading claim about otp warnings", "atm card blocking threat"],
        "explanation": "Bank impersonator attempting to dismiss legitimate OTP warnings and extract verification code under threat.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-028
    items.append({
        "conversation_id": "KAV-SYNTH-028",
        "language": "hi",
        "primary_label": "SCAM",
        "scenario": "LPG Gas Subsidy Block Warning & APK Download Coercion",
        "dialogue": [
            {"speaker": "caller", "text": "भारत गैस एजेंसी से बोल रहा हूँ। आपका घरेलू गैस सब्सिडी खाता बंद होने जा रहा है।"},
            {"speaker": "recipient", "text": "सब्सिडी बंद क्यों हो रही है? बैंक खाता तो लिंक है मेरा।"},
            {"speaker": "caller", "text": "ई-केवाईसी बायोमेट्रिक सर्वर पर आपका अंगूठा मिसमैच दिखा रहा है।"},
            {"speaker": "recipient", "text": "तो मुझे गैस एजेंसी आकर फिंगरप्रिंट देना होगा क्या?"},
            {"speaker": "caller", "text": "एजेंसी आने की जरूरत नहीं है, हम व्हाट्सएप पर गैस अपडेट फाइल भेज रहे हैं, उसे इंस्टॉल कर लो।"},
            {"speaker": "recipient", "text": "व्हाट्सएप वाली फाइल सुरक्षित है क्या?"},
            {"speaker": "caller", "text": "हाँ बिल्कुल सुरक्षित है, उसपर क्लिक करके अपना आधार नंबर और बैंक डिटेल भर दो।"},
            {"speaker": "recipient", "text": "व्हाट्सएप पर आई अनजानी एपीके कभी नहीं लगानी चाहिए। मैं सीधा गैस एजेंसी जाऊंगा।"}
        ],
        "scam_tactics": ["MALICIOUS_LINK_OR_APP", "ACCOUNT_OR_KYC_THREAT", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["gas subsidy stoppage threat", "whatsapp apk distribution", "credential collection via untrusted app"],
        "explanation": "Utility subsidy cancellation threat used to push untrusted Android APK containing malware.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-029 (Legit 1)
    items.append({
        "conversation_id": "KAV-SYNTH-029",
        "language": "hi",
        "primary_label": "LEGITIMATE",
        "scenario": "E-Commerce Order Cash on Delivery Timing Inquiry",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्कार सर, मैं फ्लिपकार्ट डिलीवरी हब से बोल रहा हूँ। आपका स्पोर्ट्स शूज का पार्सल आया हुआ है।"},
            {"speaker": "recipient", "text": "हाँ भैया, मैं घर पर ही हूँ। कब तक आ रहे हो?"},
            {"speaker": "caller", "text": "सर दोपहर दो से तीन के बीच डिलीवरी होगी। कैश ऑन डिलीवरी का नौ सौ निन्यानवे रुपये खुला रखिएगा।"},
            {"speaker": "recipient", "text": "क्या मैं ऑनलाइन स्कैनर से डिलीवरी बॉय को यूपीआई कर सकता हूँ?"},
            {"speaker": "caller", "text": "हाँ बिल्कुल सर, डिलीवरी बॉय के पास आधिकारिक कंपनी क्यूआर कोड रहेगा, आप सामने स्कैन कर सकते हैं।"},
            {"speaker": "recipient", "text": "ठीक है, कोई ओटीपी वगैरह अभी बताना है क्या?"},
            {"speaker": "caller", "text": "नहीं सर, कोई ओटीपी नहीं चाहिए। पार्सल हाथ में मिलने के बाद ही कोड बताइएगा।"},
            {"speaker": "recipient", "text": "बढ़िया, धन्यवाद भैया।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["legitimate delivery coordination", "official on-site qr payment", "no advance credential request"],
        "explanation": "Authentic cash-on-delivery logistics coordination emphasizing secure on-site transaction.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/hindi/kav_synth_029.wav"
    })

    # KAV-SYNTH-030
    items.append({
        "conversation_id": "KAV-SYNTH-030",
        "language": "hi",
        "primary_label": "LEGITIMATE",
        "scenario": "Train Ticket Waiting List Confirmation Assistance",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्ते श्री वर्मा, मैं आईआरसीटीसी कस्टमर सपोर्ट डेस्क से बोल रही हूँ।"},
            {"speaker": "recipient", "text": "हाँ मैडम, मैंने राजधानी एक्सप्रेस के टिकट रिफंड के बारे में शिकायत दर्ज की थी।"},
            {"speaker": "caller", "text": "जी, आपकी टिकट चार्ट बनने के बाद भी वेटिंग लिस्ट में थी, इसलिए स्वतः रद्द हो गई है।"},
            {"speaker": "recipient", "text": "मेरा पैसा कब तक बैंक में वापस आएगा?"},
            {"speaker": "caller", "text": "रिफंड राशि बाइस सौ रुपये आपके उसी बैंक खाते में तीन से चार कार्य दिवसों में जमा हो जाएगी।"},
            {"speaker": "recipient", "text": "क्या मुझे कोई फॉर्म या बैंक डिटेल देनी होगी?"},
            {"speaker": "caller", "text": "नहीं सर, भुगतान उसी मूल स्रोत पर होता है जिससे टिकट बुक हुई थी। किसी को कोई ओटीपी न दें।"},
            {"speaker": "recipient", "text": "जानकारी के लिए बहुत-बहुत धन्यवाद।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["automatic original source refund", "explicit warning against sharing otp", "routine railway customer service"],
        "explanation": "Official railway ticketing customer assistance explaining automatic refund mechanisms safely.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-031
    items.append({
        "conversation_id": "KAV-SYNTH-031",
        "language": "hi",
        "primary_label": "LEGITIMATE",
        "scenario": "School Fee Payment Receipt Confirmation",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्कार, डीएवी पब्लिक स्कूल लेखा विभाग से सुनीता बात कर रही हूँ। क्या मैं श्री गुप्ता से बात कर रही हूँ?"},
            {"speaker": "recipient", "text": "हाँ जी मैडम, बताइए क्या बात है?"},
            {"speaker": "caller", "text": "कक्षा सातवीं के रोहन गुप्ता की दूसरी तिमाही की फीस ऑनलाइन जमा हुई थी, उसकी आधिकारिक रसीद जनरेट हो गई है।"},
            {"speaker": "recipient", "text": "रसीद हमें स्कूल आकर लेनी होगी या पोर्टल पर मिलेगी?"},
            {"speaker": "caller", "text": "आप स्कूल की आधिकारिक वेबसाइट पर पेरेंट लॉगिन करके रसीद डाउनलोड कर सकते हैं।"},
            {"speaker": "recipient", "text": "क्या अगली तिमाही की फीस की अंतिम तिथि वही पंद्रह तारीख है?"},
            {"speaker": "caller", "text": "जी बिल्कुल। किसी भी सहायता के लिए स्कूल के लैंडलाइन नंबर पर संपर्क कर सकते हैं।"},
            {"speaker": "recipient", "text": "बहुत धन्यवाद मैडम, मैं पोर्टल से रसीद निकाल लेता हूँ।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["school fee administration", "self-service parent portal", "no unsolicited payment requests"],
        "explanation": "Routine educational administrative follow-up confirming receipt availability on official parent portal.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-032
    items.append({
        "conversation_id": "KAV-SYNTH-032",
        "language": "hi",
        "primary_label": "LEGITIMATE",
        "scenario": "Car Insurance Renewal Policy Discussion",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्ते सर, मारुति इंश्योरेंस ब्रोकर सर्विस से विकास बात कर रहा हूँ। आपकी वैगनआर कार की पॉलिसी अगले महीने समाप्त हो रही है।"},
            {"speaker": "recipient", "text": "हाँ, मुझे रिन्यूअल करवाना है। इस बार नो क्लेम बोनस कितना मिलेगा?"},
            {"speaker": "caller", "text": "पिछले साल कोई क्लेम नहीं होने के कारण आपको पैंतीस प्रतिशत नो क्लेम बोनस डिस्काउंट मिलेगा।"},
            {"speaker": "recipient", "text": "क्या जीरो डेप्रिसिएशन कवर चालू रहेगा?"},
            {"speaker": "caller", "text": "जी सर, बंपर टू बंपर कवर शामिल है। कोटेशन आपके रजिस्टर्ड ईमेल पर भेज दिया गया है।"},
            {"speaker": "recipient", "text": "मैं पेमेंट कैसे करूँ?"},
            {"speaker": "caller", "text": "ईमेल में आधिकारिक कंपनी का लिंक है या आप सीधे कंपनी की वेबसाइट पर जाकर पॉलिसी नंबर से भुगतान कर सकते हैं।"},
            {"speaker": "recipient", "text": "ठीक है, मैं शाम को वेबसाइट से पेमेंट कर दूंगा।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["transparent insurance quotation", "official insurer website payment", "no pressure or phone payments"],
        "explanation": "Standard motor insurance renewal discussion directing customer to secure official payment channels.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-033
    items.append({
        "conversation_id": "KAV-SYNTH-033",
        "language": "hi",
        "primary_label": "LEGITIMATE",
        "scenario": "Water Purifier Annual Service Visit Scheduling",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्कार, केंट आरओ कस्टमर केयर से। क्या यह श्रीमान आलोक जी का नंबर है?"},
            {"speaker": "recipient", "text": "हाँ, आलोक बोल रहा हूँ।"},
            {"speaker": "caller", "text": "सर आपके आरओ वाटर प्यूरीफायर की छह महीने की रूटीन सर्विसिंग ड्यू है।"},
            {"speaker": "recipient", "text": "हाँ, पानी का फ्लो थोड़ा कम आ रहा था। टेक्नीशियन कब आ सकता है?"},
            {"speaker": "caller", "text": "कल दोपहर बारह से दो बजे का स्लॉट खाली है। क्या यह समय आपके लिए सुविधाजनक रहेगा?"},
            {"speaker": "recipient", "text": "हाँ, कल बारह बजे भेज दीजिए। क्या कोई सर्विस चार्ज लगेगा?"},
            {"caller": "caller", "speaker": "caller", "text": "आपकी एनुअल मेंटेनेंस कॉन्ट्रैक्ट चालू है, इसलिए सर्विसिंग बिल्कुल मुफ्त है। केवल फिल्टर बदलने पर पार्ट की कीमत लगेगी।"},
            {"speaker": "recipient", "text": "बिल्कुल ठीक है, कल टेक्नीशियन को भेज दीजिए।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["routine maintenance scheduling", "covered under warranty/amc", "no unsolicited payment request"],
        "explanation": "Legitimate appliance warranty service appointment booking with transparent AMC terms.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-034
    items.append({
        "conversation_id": "KAV-SYNTH-034",
        "language": "hi",
        "primary_label": "LEGITIMATE",
        "scenario": "Housing Society General Body Meeting Notice",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्ते मिश्रा जी, मैं ग्रीन वैली सोसाइटी सचिव आर.के. शर्मा बोल रहा हूँ।"},
            {"speaker": "recipient", "text": "नमस्ते शर्मा जी, कैसे हैं आप?"},
            {"speaker": "caller", "text": "सब बढ़िया जी। रविवार सुबह दस बजे कम्युनिटी हॉल में वार्षिक आम बैठक रखी गई है।"},
            {"speaker": "recipient", "text": "क्या इस बार लिफ्ट मेंटेनेंस और सोलर पैनल का मुद्दा भी एजेंडे में है?"},
            {"speaker": "caller", "text": "जी हाँ, सोसाइटी ऑडिट रिपोर्ट और नए सोलर प्रोजेक्ट के बजट पर चर्चा होगी। आपकी उपस्थिति जरूरी है।"},
            {"speaker": "recipient", "text": "मैं जरूर आऊँगा। क्या बैठक का एजेंडा नोटिस बोर्ड पर लगा है?"},
            {"speaker": "caller", "text": "हाँ नोटिस बोर्ड पर भी है और सोसाइटी के आधिकारिक ईमेल ग्रुप पर भी साझा कर दिया गया है।"},
            {"speaker": "recipient", "text": "ठीक है शर्मा जी, रविवार को मिलते हैं।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["local community meeting coordination", "no financial solicitation", "verifiable local notice"],
        "explanation": "Authentic residential cooperative society meeting announcement with zero financial demands.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-035
    items.append({
        "conversation_id": "KAV-SYNTH-035",
        "language": "hi",
        "primary_label": "LEGITIMATE",
        "scenario": "Hospital Doctor OPD Consultation Timing Follow-up",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्कार, मैक्स सुपर स्पेशलिटी हॉस्पिटल ओपीडी रिसेप्शन से। क्या मेरी बात श्रीमती रेखा से हो रही है?"},
            {"speaker": "recipient", "text": "हाँ, मैं रेखा बोल रही हूँ।"},
            {"speaker": "caller", "text": "मैम, डॉ. माथुर के साथ आपकी कल सुबह ग्यारह बजे की अपॉइंटमेंट की पुष्टि करनी थी।"},
            {"speaker": "recipient", "text": "हाँ, मुझे डॉक्टर साहब को अपने पिछले हफ्ते के ब्लड टेस्ट दिखाने हैं।"},
            {"speaker": "caller", "text": "कृपया अपनी पुरानी फाइल और सभी टेस्ट रिपोर्ट साथ लेकर आइएगा। समय से पंद्रह मिनट पहले रिसेप्शन पर रिपोर्ट करें।"},
            {"speaker": "recipient", "text": "कंसल्टेशन फीस क्या पहले ऑनलाइन जमा करनी होगी?"},
            {"speaker": "caller", "text": "नहीं मैम, फीस कल ओपीडी काउंटर पर रसीद कटवाने के बाद ही जमा होगी।"},
            {"speaker": "recipient", "text": "ठीक है, मैं समय पर पहुँच जाऊँगी।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["hospital consultation confirmation", "on-site counter payment", "medical records instruction"],
        "explanation": "Routine healthcare clinic appointment confirmation with on-site payment protocol.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-036 (Ambig 1)
    items.append({
        "conversation_id": "KAV-SYNTH-036",
        "language": "hi",
        "primary_label": "AMBIGUOUS",
        "scenario": "Bank Phishing Awareness Campaign (Negative Context)",
        "dialogue": [
            {"speaker": "caller", "text": "भारतीय स्टेट बैंक का जनहित में साइबर सुरक्षा संदेश। कृपया ध्यान से सुनें।"},
            {"speaker": "recipient", "text": "हाँ बताइए, क्या मेरे खाते में कोई समस्या है?"},
            {"speaker": "caller", "text": "नहीं सर, आपका खाता सुरक्षित है। हम ग्राहकों को फर्जी कॉल और लॉटरी मैसेज के प्रति आगाह कर रहे हैं।"},
            {"speaker": "recipient", "text": "अच्छा, तो मुझे क्या सावधानी बरतनी चाहिए?"},
            {"speaker": "caller", "text": "कभी भी किसी अनजान व्यक्ति को अपना बैंक ओटीपी, पासवर्ड या यूपीआई पिन साझा न करें, चाहे वह खुद को बैंक मैनेजर ही क्यों न कहे।"},
            {"speaker": "recipient", "text": "क्या मुझे कोई बटन दबाकर कन्फर्म करना है?"},
            {"speaker": "caller", "text": "नहीं सर, किसी लिंक या बटन पर क्लिक न करें। केवल सतर्क रहें। साइबर सुरक्षा ही बचाव है।"},
            {"speaker": "recipient", "text": "धन्यवाद इस जरूरी जानकारी के लिए।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["negative context suppression", "security warning containing threat keywords without malicious intent"],
        "explanation": "Public awareness advisory against bank scams; contains security threat keywords without coercive intent.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/hindi/kav_synth_036.wav"
    })

    # KAV-SYNTH-037
    items.append({
        "conversation_id": "KAV-SYNTH-037",
        "language": "hi",
        "primary_label": "AMBIGUOUS",
        "scenario": "Distant Relative Requesting Urgent Medical UPI Assistance",
        "dialogue": [
            {"speaker": "caller", "text": "अरे भैया प्रणाम, मैं आपका ममेरा भाई सोनू बोल रहा हूँ। पहचान लिया ना?"},
            {"speaker": "recipient", "text": "सोनू? तुम्हारी आवाज थोड़ी बदली हुई लग रही है। कहाँ से बोल रहे हो?"},
            {"speaker": "caller", "text": "भैया मेरा गला खराब है। मैं अभी कानपुर रेलवे स्टेशन पर हूँ और मेरी जेब कट गई है।"},
            {"speaker": "recipient", "text": "अरे! टिकट और पैसे सब चले गए क्या?"},
            {"speaker": "caller", "text": "हाँ भैया, फोन पे में नेटवर्क नहीं आ रहा। पास की चाय दुकान वाले के क्यूआर कोड पर दो हजार भेज दो ना तुरंत।"},
            {"speaker": "recipient", "text": "मैं पहले तुम्हारे पिताजी यानी मामाजी को फोन करके पूछता हूँ।"},
            {"speaker": "caller", "text": "अरे मामाजी को मत बताना, वो बहुत डांटेंगे। बस आधे घंटे के लिए भेज दो, घर पहुँचकर लौटा दूंगा।"},
            {"speaker": "recipient", "text": "नहीं सोनू, बिना मामाजी से बात किए मैं किसी अनजान दुकानदार के नंबर पर पैसे नहीं भेज सकता।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["emotional family urgency", "unverified relative voice", "third-party upi transfer request"],
        "explanation": "Ambiguous distress call from an unverified relative requesting urgent financial help; potential imposter scam or genuine relative requiring verification.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-038
    items.append({
        "conversation_id": "KAV-SYNTH-038",
        "language": "hi",
        "primary_label": "AMBIGUOUS",
        "scenario": "Unsolicited Mutual Fund Investment Advisory Call",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्कार सर, मैं वेल्थकेयर फिनसर्व से सीनियर एडवाइजर गौरव बात कर रहा हूँ।"},
            {"speaker": "recipient", "text": "जी, किस संबंध में फोन किया है?"},
            {"speaker": "caller", "text": "सर बाजार अभी रिकॉर्ड ऊंचाई पर है। हम आपके लिए स्माल कैप और फ्लेक्सी कैप फंड्स का कस्टमाइज्ड पोर्टफोलियो बना सकते हैं।"},
            {"speaker": "recipient", "text": "आपकी कंपनी सेबी रजिस्टर्ड है क्या?"},
            {"speaker": "caller", "text": "जी हाँ सर, हमारे पास एएमएफआई रजिस्ट्रेशन नंबर है। हम कोई डायरेक्ट पेमेंट नहीं लेते, निवेश आपके अपने डीमैट खाते से होता है।"},
            {"speaker": "recipient", "text": "तो आपकी फीस क्या होगी?"},
            {"caller": "caller", "speaker": "caller", "text": "हमारी वार्षिक रिसर्च सब्सक्रिप्शन फीस उन्नीस सौ निन्यानवे रुपये है। पहले हम आपको डेमो रिपोर्ट ईमेल करेंगे।"},
            {"speaker": "recipient", "text": "पहले अपनी सेबी रजिस्ट्रेशन कॉपी और ब्रोशर ईमेल कीजिए, मैं जांच करके बताऊंगा।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["cold calling financial advisory", "unsolicited investment marketing", "no immediate credential request"],
        "explanation": "Cold-call financial advisory offering investment advisory services with legitimate self-directed investment model.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-039
    items.append({
        "conversation_id": "KAV-SYNTH-039",
        "language": "hi",
        "primary_label": "AMBIGUOUS",
        "scenario": "Telecom SIM Upgrade Verification Incomplete Details Call",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्ते सर, मैं वोडाफोन-आइडिया रिटेल ऑपरेशंस से बोल रहा हूँ। आपका 4G सिम 5G में अपग्रेड करने के लिए अनुरोध मिला है।"},
            {"speaker": "recipient", "text": "मैंने तो कोई अपग्रेड अनुरोध नहीं डाला था। मेरा फोन तो पहले से 5G सपोर्ट करता है।"},
            {"speaker": "caller", "text": "शायद स्टोर से ऑटोमैटिक रिक्वेस्ट जनरेट हुई हो। क्या आप इस सिम को चालू रखना चाहते हैं?"},
            {"speaker": "recipient", "text": "हाँ, मेरा यह नंबर दस साल से चल रहा है।"},
            {"speaker": "caller", "text": "तो सर वेरिफिकेशन के लिए अपनी जन्मतिथि और माताजी का नाम बता दीजिए।"},
            {"speaker": "recipient", "text": "मैं फोन पर निजी जानकारी क्यों दूं? क्या इसके बिना सिम बंद हो जाएगी?"},
            {"speaker": "caller", "text": "नहीं सर, सिम बंद नहीं होगी, केवल 5G स्पीड एक्टिवेट नहीं होगी। आप चाहे तो स्टोर जाकर भी करवा सकते हैं।"},
            {"speaker": "recipient", "text": "ठीक है, मैं पास के वोडाफोन स्टोर में जाकर खुद चेक करवा लूंगा।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["unrequested sim upgrade notification", "personal demographic verification", "alternative store visit available"],
        "explanation": "Ambiguous SIM profile verification call; potential SIM swap reconnaissance or benign telemarketing upgrade.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-040
    items.append({
        "conversation_id": "KAV-SYNTH-040",
        "language": "hi",
        "primary_label": "AMBIGUOUS",
        "scenario": "Job Interview Shortlist Verification & Certificate Courier Query",
        "dialogue": [
            {"speaker": "caller", "text": "नमस्कार राहुल जी, मैं एबीसी लॉजिस्टिक्स एचआर विभाग से ज्योति बात कर रही हूँ।"},
            {"speaker": "recipient", "text": "नमस्ते ज्योति जी, क्या मेरी नौकरी की अर्जी शॉर्टलिस्ट हुई है?"},
            {"speaker": "caller", "text": "हाँ, आपका रेज्यूमे ऑपरेशन मैनेजर पद के लिए शॉर्टलिस्ट हुआ है। फाइनल इंटरव्यू सोमवार को है।"},
            {"speaker": "recipient", "text": "बहुत अच्छा! क्या इंटरव्यू ऑनलाइन होगा या ऑफिस में?"},
            {"speaker": "caller", "text": "इंटरव्यू ऑनलाइन होगा, लेकिन उससे पहले आपको अपने ओरिजिनल सर्टिफिकेट हमारे हेड ऑफिस कूरियर करने होंगे।"},
            {"speaker": "recipient", "text": "ओरिजिनल सर्टिफिकेट कूरियर करने होंगे? फोटोकॉपी या स्कैन कॉपी नहीं चलेगी क्या?"},
            {"speaker": "caller", "text": "कंपनी की पॉलिसी में लिखा है सर। हालांकि आप चाहें तो सोमवार को ऑनलाइन इंटरव्यू के दौरान स्क्रीन पर भी दिखा सकते हैं।"},
            {"speaker": "recipient", "text": "मैं ओरिजिनल दस्तावेज कूरियर कभी नहीं करूँगा, मैं इंटरव्यू में लाइव स्क्रीन पर दिखा दूंगा।" }
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["unusual original document submission request", "job recruitment context", "offline alternative offered"],
        "explanation": "Unusual recruitment request demanding original document dispatch, but offering standard online alternative.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    return items

if __name__ == "__main__":
    hi_items = get_hindi_conversations()
    print(f"Generated {len(hi_items)} Hindi conversations.")

