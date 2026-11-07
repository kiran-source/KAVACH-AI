# scripts/catalog_telugu_and_codemixed.py
import json

def get_telugu_conversations():
    items = []

    # KAV-SYNTH-041 (Pilot 3)
    items.append({
        "conversation_id": "KAV-SYNTH-041",
        "pilot_id": "KAV-SYNTH-PILOT-003",
        "language": "te",
        "primary_label": "SCAM",
        "scenario": "Bank Account Freeze & Urgent PIN/OTP Credential Theft",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం అండి, నేను ఎస్బీఐ సెంట్రల్ హెల్ప్‌డెస్క్ మేనేజర్ రాజేష్ మాట్లాడుతున్నాను."},
            {"speaker": "recipient", "text": "చెప్పండి సార్, ఏంటి విషయం?"},
            {"speaker": "caller", "text": "మీ బ్యాంక్ అకౌంట్ కేవైసీ అప్‌డేట్ చేయకపోవడం వల్ల తాత్కాలికంగా బ్లాక్ చేయబడింది."},
            {"speaker": "recipient", "text": "అవునా? మొన్ననే బ్రాంచ్‌కి వెళ్లి ఆధార్ ఇచ్చాను కదా?"},
            {"speaker": "caller", "text": "సిస్టమ్‌లో సర్వర్ అప్‌డేట్ కాలేదు. ఇప్పుడు ఆన్‌లైన్‌లో వెరిఫై చేయకపోతే అకౌంట్ శాశ్వతంగా రద్దు అవుతుంది."},
            {"speaker": "recipient", "text": "సరే, నేను ఎలా అప్‌డేట్ చేయాలి?"},
            {"speaker": "caller", "text": "మీ మొబైల్‌కి వచ్చిన ఆరు అంకెల ఓటీపీ మరియు మీ ఏటీఎం కార్డ్ పిన్ నంబర్ వెంటనే చెప్పండి."},
            {"speaker": "recipient", "text": "బ్యాంకు వాళ్ళు ఎప్పుడూ పిన్ నంబర్ అడగరని చెప్పారు. నేను బ్యాంకు బ్రాంచ్‌కి వెళ్లి కనుక్కుంటాను."}
        ],
        "scam_tactics": ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"],
        "risk_indicators": ["account block urgency", "permanent cancellation threat", "demand for otp and atm pin"],
        "explanation": "Impersonates bank manager threatening immediate account closure to solicit secret OTP and ATM PIN credentials.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/telugu/kav-synth-pilot-003.wav"
    })

    # KAV-SYNTH-042
    items.append({
        "conversation_id": "KAV-SYNTH-042",
        "language": "te",
        "primary_label": "SCAM",
        "scenario": "Hyderabad Cyber Crime Police Station Arrest Threat",
        "dialogue": [
            {"speaker": "caller", "text": "హైదరాబాద్ సైబర్ క్రైమ్ పోలీస్ స్టేషన్ నుండి ఎస్ఐ శ్రీనివాస్ రావు మాట్లాడుతున్నాను."},
            {"speaker": "recipient", "text": "పోలీస్ స్టేషన్ నుండా? నేను ఏం తప్పు చేశాను సార్?"},
            {"speaker": "caller", "text": "మీ ఆధార్ నంబర్ పై రిజిస్టర్ అయిన సిమ్ ద్వారా ముంబైలో ఇరవై కోట్ల హవాలా మరియు డ్రగ్స్ సప్లై జరిగింది."},
            {"speaker": "recipient", "text": "అయ్యో దేవుడా! నేను అలాంటి పనులు ఎప్పుడూ చేయలేదు సార్."},
            {"speaker": "caller", "text": "కోర్టు నుండి అరెస్ట్ వారెంట్ జారీ అయింది. మీరు వెంటనే వీడియో కాల్ లో హాజరై మీ నిర్దోషిత్వాన్ని నిరూపించుకోవాలి."},
            {"speaker": "recipient", "text": "నేను మా బంధువు లాయర్ తో మాట్లాడతాను సార్."},
            {"speaker": "caller", "text": "ఎవరితో మాట్లాడినా కేసు తీవ్రమవుతుంది. అరెస్ట్ ఆపాలంటే ఇరవై వేల రూపాయల బెయిల్ డిపాజిట్ వెంటనే చెల్లించాలి."},
            {"speaker": "recipient", "text": "పోలీసులు ఫోన్ లో డబ్బులు అడగరని తెలుసు. నేను నేరుగా పోలీస్ స్టేషన్ కి వస్తాను."}
        ],
        "scam_tactics": ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"],
        "risk_indicators": ["police officer impersonation", "hawala and drug allegation", "immediate bail transfer demand"],
        "explanation": "Law enforcement impersonation fabricating severe narcotics charges to demand instant bail money over phone.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/telugu/kav_synth_042.wav"
    })

    # KAV-SYNTH-043
    items.append({
        "conversation_id": "KAV-SYNTH-043",
        "language": "te",
        "primary_label": "SCAM",
        "scenario": "Instant Personal Loan Approval APK Malware Scam",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం, ధనీ ఫైనాన్స్ నుండి. మీకు రెండు లక్షల ఇన్స్టంట్ పర్సనల్ లోన్ కేవలం నిమిషాల్లో మంజూరు అయింది."},
            {"speaker": "recipient", "text": "నాకు ఎలాంటి డాక్యుమెంట్లు లేకుండా లోన్ ఎలా ఇస్తారు?"},
            {"speaker": "caller", "text": "ఆధార్ కార్డ్ సరిపోతుంది. ఎలాంటి షూరిటీ అవసరం లేదు, వడ్డీ కేవలం మూడు శాతం మాత్రమే."},
            {"speaker": "recipient", "text": "డబ్బులు నా అకౌంట్ లో ఎప్పుడు పడతాయి?"},
            {"speaker": "caller", "text": "నేను వాట్సాప్ లో ఒక ఏపీకే అప్లికేషన్ లింక్ పంపుతాను, దాన్ని ఫోన్ లో ఇన్స్టాల్ చేసి మీ బ్యాంక్ అకౌంట్ నంబర్ ఇవ్వండి."},
            {"speaker": "recipient", "text": "ప్లేస్టోర్ లో ఈ యాప్ దొరకదా సార్?"},
            {"speaker": "caller", "text": "ఇది ప్రత్యేకమైన ప్రైవేట్ సర్వర్ యాప్. వెంటనే ఇన్స్టాల్ చేసి యాక్సెస్ పర్మిషన్లు ఇవ్వండి, లోన్ క్రెడిట్ అవుతుంది."},
            {"speaker": "recipient", "text": "వాట్సాప్ ఏపీకేలు ఫోన్ డేటా దొంగిలిస్తాయని విన్నాను. నాకు లోన్ వద్దు, యాప్ వద్దు."}
        ],
        "scam_tactics": ["MALICIOUS_LINK_OR_APP", "REMOTE_ACCESS_MANIPULATION", "FINANCIAL_REDIRECTION"],
        "risk_indicators": ["untrusted whatsapp apk distribution", "unrealistically easy loan lure", "device permission demand"],
        "explanation": "Pretending to offer instant loan to distribute malicious Android APK to compromise user's smartphone.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-044
    items.append({
        "conversation_id": "KAV-SYNTH-044",
        "language": "te",
        "primary_label": "SCAM",
        "scenario": "Fake Gold Loan Auction Refund Scheme",
        "dialogue": [
            {"speaker": "caller", "text": "ముత్తూట్ గోల్డ్ ఫైనాన్స్ నుండి శేఖర్ మాట్లాడుతున్నాను. వేలం వేసిన పాత బంగారు ఆభరణాలు తక్కువ ధరకు ఉన్నాయి."},
            {"speaker": "recipient", "text": "వేలం వేసిన బంగారమా? గ్రామ ఎంత పడుతుంది?"},
            {"speaker": "caller", "text": "బహిరంగ మార్కెట్ లో ఏడు వేలు ఉంటే, మా దగ్గర కేవలం నాలుగు వేలకే ఇస్తున్నాము."},
            {"speaker": "recipient", "text": "అంత తక్కువకు ఎలా ఇస్తారు?"},
            {"speaker": "caller", "text": "డిఫాల్ట్ అయిన కస్టమర్ల బంగారం కాబట్టి గవర్నమెంట్ సీలింగ్ లో వచ్చింది. కేవలం ఐదుగురికి మాత్రమే ఈ అవకాశం."},
            {"speaker": "recipient", "text": "నేను నేరుగా మీ బ్రాంచ్ కి వచ్చి చూడొచ్చా?"},
            {"speaker": "caller", "text": "బ్రాంచ్ లో రద్దీ ఎక్కువ. మీ పేరు రిజిస్టర్ అవ్వాలంటే ముందస్తుగా పదివేల టోకెన్ అమౌంట్ గూగుల్ పే చేయాలి."},
            {"speaker": "recipient", "text": "బంగారం చూడకుండా అడ్వాన్స్ పంపడం కుదరదు. ఇది మోసంలా ఉంది."}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["unrealistically cheap gold lure", "advance token money demand", "limited availability pressure"],
        "explanation": "Fake gold auction investment scheme soliciting advance token payments for non-existent discounted gold.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-045
    items.append({
        "conversation_id": "KAV-SYNTH-045",
        "language": "te",
        "primary_label": "SCAM",
        "scenario": "Electricity Bill Non-Payment Power Cut Notice",
        "dialogue": [
            {"speaker": "caller", "text": "విద్యుత్ శాఖ హెచ్చరిక. మీ ఇంటి కరెంట్ బిల్లు చెల్లించనందున ఈ రాత్రి తొమ్మిది గంటలకు విద్యుత్ సరఫరా నిలిపివేయబడుతుంది."},
            {"speaker": "recipient", "text": "అదేంటి సార్, నేను నిన్ననే ఆన్లైన్ లో బిల్లు కట్టేశాను కదా?"},
            {"speaker": "caller", "text": "మీ పాత బాకీ నాలుగు వందల రూపాయలు అప్డేట్ అవ్వలేదు. లైన్ మ్యాన్ ఇప్పటికే మీ వీధికి బయలుదేరాడు."},
            {"speaker": "recipient", "text": "ఇప్పుడు వెంటనే ఎలా చెల్లించాలి?"},
            {"speaker": "caller", "text": "మేము పంపే లింక్ ద్వారా పది రూపాయల వెరిఫికేషన్ రుసుము చెల్లించి మీ కన్స్యూమర్ నంబర్ అప్డేట్ చేయండి."},
            {"speaker": "recipient", "text": "ఏ లింక్ పంపుతున్నారు?"},
            {"speaker": "caller", "text": "ఎస్ఎంఎస్ లో వచ్చిన లింక్ ఓపెన్ చేసి మీ యూపీఐ పిన్ నమోదు చేయండి, లైన్ ఆగిపోకుండా ఉంటుంది."},
            {"speaker": "recipient", "text": "యూపీఐ పిన్ ఎంటర్ చేస్తే ఖాతాలో డబ్బులు పోతాయి. నేను రేపు విద్యుత్ ఆఫీస్ కి వెళ్లి తేల్చుకుంటాను."}
        ],
        "scam_tactics": ["URGENCY_OR_THREAT", "OTP_PIN_CVV_THEFT", "MALICIOUS_LINK_OR_APP", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["immediate power cut threat", "malicious payment link", "upi pin solicitation"],
        "explanation": "Electricity disconnection threat used to induce urgency and extract UPI PIN via phishing link.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-046
    items.append({
        "conversation_id": "KAV-SYNTH-046",
        "language": "te",
        "primary_label": "SCAM",
        "scenario": "Post Office Speed Post Courier Seizure Scam",
        "dialogue": [
            {"speaker": "caller", "text": "భారత తపాలా శాఖ పార్శిల్ డివిజన్ నుండి అధికారి శ్రీధర్. మీ పేరు మీద వచ్చిన ఒక స్పీడ్ పోస్ట్ పార్శిల్ ఆగిపోయింది."},
            {"speaker": "recipient", "text": "నా పేరు మీద పార్శిలా? ఎవరు పంపించారు?"},
            {"speaker": "caller", "text": "పార్శిల్ లో పది లక్షల నకిలీ కరెన్సీ నోట్లు మరియు విదేశీ సిమ్ కార్డులు లభించాయి."},
            {"speaker": "recipient", "text": "నాకు ఎలాంటి పార్శిల్స్ తో సంబంధం లేదు సార్, ఎవరో కావాలని నా పేరు వాడారు."},
            {"speaker": "caller", "text": "ఈ కేసు కస్టమ్స్ మరియు పోలీసులకు బదిలీ చేయబడుతోంది. మీరు జైలుకు వెళ్ళవలసి ఉంటుంది."},
            {"speaker": "recipient", "text": "నేను నిర్దోషిని సార్, దీని నుండి ఎలా బయటపడాలి?"},
            {"speaker": "caller", "text": "డిపార్ట్మెంట్ క్లియరెన్స్ కోసం తక్షణమే పాతిక వేల రూపాయల ఫైన్ ఆన్లైన్ లో కడితే ఫైల్ క్లోజ్ చేస్తాం."},
            {"speaker": "recipient", "text": "తపాలా శాఖ ఫోన్ లో లంచం అడగదు. నేను ప్రధాన పోస్టాఫీస్ కి వెళ్లి ఫిర్యాదు చేస్తాను."}
        ],
        "scam_tactics": ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"],
        "risk_indicators": ["postal package contraband claim", "threat of arrest and jail", "demand for instant clearance fine"],
        "explanation": "Postal department impersonation claiming illegal cash in parcel to extort clearance penalty.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-047
    items.append({
        "conversation_id": "KAV-SYNTH-047",
        "language": "te",
        "primary_label": "SCAM",
        "scenario": "RTO Traffic Challan Penalty Payment Link Fraud",
        "dialogue": [
            {"speaker": "caller", "text": "ట్రాఫిక్ పోలీస్ మరియు ఆర్టీవో ఈ-చలాన్ విభాగం. మీ వాహనంపై పదివేల రూపాయల పెండింగ్ చలాన్లు ఉన్నాయి."},
            {"speaker": "recipient", "text": "పదివేల చలానా? నేను ట్రాఫిక్ నిబంధనలు ఎప్పుడూ ఉల్లంఘించలేదు."},
            {"speaker": "caller", "text": "ఓవర్ స్పీడింగ్ మరియు రాంగ్ రూట్ డ్రైవింగ్ కెమెరా రికార్డ్ అయింది. ఈ రోజు లోగా చెల్లించకపోతే వాహనం సీజ్ చేస్తాం."},
            {"speaker": "recipient", "text": "నేను ఆర్టీవో అధికారిక వెబ్సైట్ లో చూస్తాను సార్."},
            {"speaker": "caller", "text": "వెబ్సైట్ పని చేయడం లేదు. మేము పంపిన వాట్సాప్ లింక్ లో వెళ్లి వెంటనే యాభై శాతం డిస్కౌంట్ తో కట్టండి."},
            {"speaker": "recipient", "text": "చలానా పై డిస్కౌంట్ ఎక్కడైనా ఇస్తారా సార్?"},
            {"speaker": "caller", "text": "ఇది ప్రత్యేక లోక్ అదాలత్ స్కీమ్. ఇప్పుడే లింక్ క్లిక్ చేసి పేమెంట్ పూర్తి చేయండి."},
            {"speaker": "recipient", "text": "వాట్సాప్ లింక్స్ ఫేక్ అని పోలీసులు చెప్పారు. నేను పోలీస్ కమిషనరేట్ లోని ట్రాఫిక్ విభాగానికి వెళ్తాను."}
        ],
        "scam_tactics": ["MALICIOUS_LINK_OR_APP", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"],
        "risk_indicators": ["rto challan vehicle seizure threat", "fake discount lure on whatsapp link", "unverified traffic payment link"],
        "explanation": "Fake traffic fine notification promising discounts on WhatsApp link to capture payment credentials.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-048
    items.append({
        "conversation_id": "KAV-SYNTH-048",
        "language": "te",
        "primary_label": "SCAM",
        "scenario": "Ayushman Bharat Health Card Activation Fee Extortion",
        "dialogue": [
            {"speaker": "caller", "text": "ప్రభుత్వ ఆరోగ్య సంక్షేమ శాఖ నుండి మాట్లాడుతున్నాను. మీ కుటుంబానికి ఐదు లక్షల ఉచిత ఆరోగ్య కార్డు మంజూరైంది."},
            {"speaker": "recipient", "text": "ఆరోగ్య కార్డు ప్రభుత్వం ఉచితంగా ఇస్తుంది కదా?"},
            {"speaker": "caller", "text": "కార్డు ఉచితమే, కానీ డిజిటల్ స్మార్ట్ కార్డు యాక్టివేషన్ కోసం ఆధార్ వెరిఫికేషన్ రుసుము పన్నెండు వందలు చెల్లించాలి."},
            {"speaker": "recipient", "text": "ఈ డబ్బులు ఎవరికి కట్టాలి?"},
            {"speaker": "caller", "text": "మా ఆఫీసర్ యూపీఐ ఐడీకి వెంటనే ట్రాన్స్ఫర్ చేయండి. రసీదు మరియు ప్లాస్టిక్ కార్డు పోస్ట్ లో వస్తాయి."},
            {"speaker": "recipient", "text": "గ్రామ సచివాలయంలో ఎవరూ డబ్బులు అడగలేదు సార్."},
            {"speaker": "caller", "text": "ఈ రోజు చివరి తేదీ. డబ్బులు కట్టకపోతే మీ పేరు ఆరోగ్యశ్రీ జాబితా నుండి శాశ్వతంగా తొలగించబడుతుంది."},
            {"speaker": "recipient", "text": "ప్రభుత్వ పథకాలకు ప్రైవేట్ యూపీఐ లో డబ్బులు అడిగే మోసగాళ్ళు మీరు. నేను సచివాలయంలో చెబుతాను."}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"],
        "risk_indicators": ["government scheme activation fee", "private upi collection", "permanent beneficiary removal threat"],
        "explanation": "Government health insurance impersonation extorting upfront activation fee under threat of disqualification.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-049 (Legit 1)
    items.append({
        "conversation_id": "KAV-SYNTH-049",
        "language": "te",
        "primary_label": "LEGITIMATE",
        "scenario": "RTC Bus Online Ticket Booking Confirmation",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం అండి, ఏపీఎస్ఆర్టీసీ ఆన్లైన్ రిజర్వేషన్ హెల్ప్‌డెస్క్ నుండి రమ్య మాట్లాడుతున్నాను."},
            {"speaker": "recipient", "text": "నమస్కారం అండి, చెప్పండి."},
            {"speaker": "caller", "text": "రేపు రాత్రి తొమ్మిది గంటలకు విజయవాడ నుండి తిరుపతికి మీరు బుక్ చేసుకున్న అమరావతి వోల్వో బస్సు టికెట్ కన్ఫర్మ్ అయింది."},
            {"speaker": "recipient", "text": "సంతోషం అండి. బస్సు పండిట్ నెహ్రూ బస్టాండ్ లో ఏ ప్లాట్‌ఫారమ్ మీదకు వస్తుంది?"},
            {"speaker": "caller", "text": "ప్లాట్‌ఫారమ్ నంబర్ పదహారు అండి. ప్రయాణానికి అరగంట ముందే అక్కడకు చేరుకోవాలి."},
            {"speaker": "recipient", "text": "డ్రైవర్ ఫోన్ నంబర్ ఎప్పుడు వస్తుంది?"},
            {"caller": "caller", "speaker": "caller", "text": "బస్సు బయలుదేరడానికి రెండు గంటల ముందు డ్రైవర్ వివరాలు మీ మొబైల్ కి అధికారిక ఎస్ఎంఎస్ ద్వారా వస్తాయి."},
            {"speaker": "recipient", "text": "చాలా ధన్యవాదాలు అండి, సమాచారం ఇచ్చినందుకు."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["official bus ticket coordination", "no financial solicitation", "official sms confirmation"],
        "explanation": "Authentic state transport corporation travel confirmation with routine boarding details.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/telugu/kav_synth_049.wav"
    })

    # KAV-SYNTH-050
    items.append({
        "conversation_id": "KAV-SYNTH-050",
        "language": "te",
        "primary_label": "LEGITIMATE",
        "scenario": "College Admission Certificate Verification Query",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం, ఆంధ్రా లయోలా కాలేజ్ అడ్మిషన్స్ విభాగం నుండి సీతారామయ్య మాట్లాడుతున్నాను."},
            {"speaker": "recipient", "text": "నమస్కారం సర్, నా అడ్మిషన్ అప్లికేషన్ గురించా సర్?"},
            {"speaker": "caller", "text": "అవును బాబూ, మీ డిగ్రీ అడ్మిషన్ ఫారంలో ఇంటర్మీడియట్ ఒరిజినల్ మార్కుల మెమో జతపరచడం మర్చిపోయారు."},
            {"speaker": "recipient", "text": "అయ్యో సర్, నెట్ కాపీ పెట్టాను సర్. ఒరిజినల్ మెమో కాలేజీకి తీసుకురావాలా?"},
            {"speaker": "caller", "text": "అవును, సోమవారం ఉదయం పది గంటలకు అడ్మినిస్ట్రేటివ్ ఆఫీస్ కి వచ్చి మీ ఒరిజినల్ సర్టిఫికెట్స్ చూపించి వెరిఫై చేయించుకోండి."},
            {"speaker": "recipient", "text": "ఫీజు ఏమైనా తీసుకురావాలా సర్?"},
            {"speaker": "caller", "text": "ఫీజు మొత్తం కాలేజీ అధికారిక బ్యాంకు చలానా ద్వారా మాత్రమే కట్టాలి, ఎవరికీ నగదు ఇవ్వకూడదు."},
            {"speaker": "recipient", "text": "సరే సర్, సోమవారం ఉదయమే వచ్చి సర్టిఫికెట్లు చూపిస్తాను."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["academic certificate verification", "official bank challan payment", "in-person campus verification"],
        "explanation": "Legitimate college administrative communication requesting in-person certificate verification.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-051
    items.append({
        "conversation_id": "KAV-SYNTH-051",
        "language": "te",
        "primary_label": "LEGITIMATE",
        "scenario": "Agricultural Borewell Equipment Subsidy Inquiry",
        "dialogue": [
            {"speaker": "caller", "text": "రైతు భరోసా కేంద్రం నుండి వ్యవసాయ విస్తరణాధికారి వెంకటేశ్వర్లు మాట్లాడుతున్నాను."},
            {"speaker": "recipient", "text": "నమస్కారం సార్, బోరుబావి సోలార్ మోటార్ సబ్సిడీ అప్లికేషన్ గురించా?"},
            {"speaker": "caller", "text": "అవును రామయ్య గారు. మీ భూమి పట్టాదారు పాస్ బుక్ మరియు ఆధార్ వెరిఫికేషన్ పూర్తయింది."},
            {"speaker": "recipient", "text": "సబ్సిడీ మోటార్ ఎప్పుడు మంజూరవుతుంది సార్?"},
            {"speaker": "caller", "text": "వచ్చే నెల మొదటి వారంలో జిల్లా కలెక్టరేట్ నుండి అనుమతి వస్తుంది. మీ వాటా సొమ్ము డీడీ తీసి ఆర్బీకే కేంద్రంలో ఇవ్వాలి."},
            {"speaker": "recipient", "text": "ఆన్లైన్ లో ఎవరికైనా డబ్బులు పంపించాలా సార్?"},
            {"caller": "caller", "speaker": "caller", "text": "ఎవరికీ ఆన్లైన్ లో పంపకూడదు. కేవలం ప్రభుత్వం పేరిట మాత్రమే డీడీ తీయాలి."},
            {"speaker": "recipient", "text": "చాలా మంచిది సార్, సమాచారం ఇచ్చినందుకు ధన్యవాదాలు."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["government farmer welfare verification", "demand draft payment protocol", "explicit warning against online transfers"],
        "explanation": "Legitimate agricultural center communication on irrigation subsidy with strict official banking protocol.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-052
    items.append({
        "conversation_id": "KAV-SYNTH-052",
        "language": "te",
        "primary_label": "LEGITIMATE",
        "scenario": "Local Tailoring Boutique Dress Ready Notice",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం మేడం, శ్రీ లక్ష్మి లేడీస్ టైలర్స్ నుండి పద్మ మాట్లాడుతున్నాను."},
            {"speaker": "recipient", "text": "నమస్తే పద్మ గారు, నా బ్లౌజులు మరియు డ్రెస్సులు కుట్టడం పూర్తయిందా?"},
            {"speaker": "caller", "text": "అవును మేడం, మీరు ఇచ్చిన రెండు పట్టు చీరల బ్లౌజులు మగ్గం వర్క్ తో సహా సిద్ధంగా ఉన్నాయి."},
            {"speaker": "recipient", "text": "అనుకున్న సమయానికి పూర్తి చేసినందుకు చాలా సంతోషం. బిల్లు ఎంతయింది?"},
            {"speaker": "caller", "text": "మొత్తం బిల్లు పన్నెండు వందలు అయింది మేడం. షాపుకి వచ్చినప్పుడు చూసుకుని ఇవ్వండి."},
            {"speaker": "recipient", "text": "నేను ఈ సాయంత్రం వచ్చి ట్రయల్ వేసుకుంటాను."},
            {"speaker": "caller", "text": "సరే మేడం, రాత్రి ఎనిమిది గంటల వరకు షాప్ తెరిచే ఉంటుంది."},
            {"speaker": "recipient", "text": "సరే అండి, సాయంత్రం వస్తాను."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["local merchant service update", "payment upon physical collection", "no advance money pressure"],
        "explanation": "Local small business service completion notice with standard physical trial and pickup.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-053
    items.append({
        "conversation_id": "KAV-SYNTH-053",
        "language": "te",
        "primary_label": "LEGITIMATE",
        "scenario": "Apartment Resident Association Maintenance Collection",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం శర్మ గారు, నేను మన అపార్ట్మెంట్ అసోసియేషన్ ట్రెజరర్ సురేష్ ని."},
            {"speaker": "recipient", "text": "నమస్కారం సురేష్ గారు, బాగున్నారా?"},
            {"speaker": "caller", "text": "బాగున్నాను అండి. ఈ నెల అపార్ట్మెంట్ మెయింటెనెన్స్ రెండు వేల రూపాయలు అసోసియేషన్ ఖాతాలో జమ చేయగలరా?"},
            {"speaker": "recipient", "text": "తప్పకుండా అండి, అసోసియేషన్ బ్యాంక్ కరెంట్ అకౌంట్ కి నెఫ్ట్ ద్వారా పంపించమంటారా?"},
            {"speaker": "caller", "text": "అవును అండి, అసోసియేషన్ అధికారిక అకౌంట్ కి పంపించి ఆ యుటిఆర్ నంబర్ వాట్సాప్ గ్రూప్ లో షేర్ చేయండి."},
            {"speaker": "recipient", "text": "సరే సురేష్ గారు, ఈ రోజే ఆఫీస్ నుండి వచ్చాక ట్రాన్స్ఫర్ చేసి రసీదు పంపుతాను."},
            {"speaker": "caller", "text": "చాలా ధన్యవాదాలు శర్మ గారు. రసీదు అందిన వెంటనే అధికారిక బుక్ లో ఎంట్రీ చేస్తాను."},
            {"speaker": "recipient", "text": "సరే అండి."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["residential association maintenance", "official society bank transfer", "verifiable community members"],
        "explanation": "Routine residential association maintenance dues coordination between verified neighbors.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-054
    items.append({
        "conversation_id": "KAV-SYNTH-054",
        "language": "te",
        "primary_label": "LEGITIMATE",
        "scenario": "Dental Clinic Regular Checkup Appointment Reminder",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం, స్మైల్ డెంటల్ హాస్పిటల్ రిసెప్షన్ నుండి లత మాట్లాడుతున్నాను. సుబ్బారావు గారి నంబరేనా?"},
            {"speaker": "recipient", "text": "అవునమ్మా, సుబ్బారావునే మాట్లాడుతున్నాను."},
            {"speaker": "caller", "text": "సర్, డాక్టర్ కృష్ణ గారి దగ్గర రేపు సాయంత్రం ఐదు గంటలకు మీ పంటి రూట్ కెనాల్ చెకప్ ఉంది."},
            {"speaker": "recipient", "text": "గుర్తు చేసినందుకు ధన్యవాదాలు అమ్మా. రేపు సాయంత్రం తప్పకుండా వస్తాను."},
            {"speaker": "caller", "text": "వచ్చేటప్పుడు గతంలో తీయించుకున్న ఎక్స్-రే కాపీలు వెంట తీసుకురండి సర్."},
            {"speaker": "recipient", "text": "ఫీజు ఆన్లైన్ లో కట్టాలా లేక అక్కడికి వచ్చాక ఇవ్వాలా?"},
            {"caller": "caller", "speaker": "caller", "text": "హాస్పిటల్ లో డాక్టర్ గారి చెకప్ పూర్తయ్యాక రిసెప్షన్ కౌంటర్ లో బిల్లు చెల్లించవచ్చు సర్."},
            {"speaker": "recipient", "text": "సరేనమ్మా, రేపు ఐదు గంటలకు వస్తాను."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["medical clinic appointment reminder", "payment at counter after treatment", "no remote payment demands"],
        "explanation": "Authentic healthcare appointment reminder with standard in-person consultation payment.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-055
    items.append({
        "conversation_id": "KAV-SYNTH-055",
        "language": "te",
        "primary_label": "LEGITIMATE",
        "scenario": "Bank Home Loan EMI Deduction Notification",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం సర్, యూనియన్ బ్యాంక్ హోమ్ లోన్ విభాగం నుండి మేనేజర్ ప్రసాద్ మాట్లాడుతున్నాను."},
            {"speaker": "recipient", "text": "నమస్కారం ప్రసాద్ గారు, చెప్పండి."},
            {"speaker": "caller", "text": "మీ హోమ్ లోన్ ఈఎంఐ వచ్చే నెల నుండి వడ్డీ రేటు తగ్గడం వల్ల ఐదు వందల రూపాయలు తగ్గింది."},
            {"speaker": "recipient", "text": "అవునా సర్! చాలా సంతోషం. దీని కోసం నేను కొత్త ఈసీఎస్ ఫారమ్ ఇవ్వాలా?"},
            {"speaker": "caller", "text": "ఏం అవసరం లేదు సర్. సిస్టమ్ లో ఆటోమేటిక్ గా కొత్త ఈఎంఐ మొత్తం ముప్పై రెండు వేలు డెబిట్ అవుతుంది."},
            {"speaker": "recipient", "text": "కొత్త లోన్ రీపేమెంట్ షెడ్యూల్ పంపుతారా సర్?"},
            {"speaker": "caller", "text": "మీ రిజిస్టర్డ్ ఈమెయిల్ కి కొత్త అమోర్టైజేషన్ చార్ట్ పంపబడింది. మీరు నెట్ బ్యాంకింగ్ లో కూడా చూసుకోవచ్చు."},
            {"speaker": "recipient", "text": "చాలా ధన్యవాదాలు ప్రసాద్ గారు, మంచి శుభవార్త చెప్పారు."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["beneficial bank rate update", "automated system adjustment", "no credential or fee request"],
        "explanation": "Legitimate banking customer relationship call notifying interest rate reduction without credential requests.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-056 (Ambig 1)
    items.append({
        "conversation_id": "KAV-SYNTH-056",
        "language": "te",
        "primary_label": "AMBIGUOUS",
        "scenario": "Cyber Police Public Awareness Announcement",
        "dialogue": [
            {"speaker": "caller", "text": "తెలంగాణ సైబర్ సెక్యూరిటీ బ్యూరో ప్రజాహిత హెచ్చరిక. శ్రద్ధగా వినండి."},
            {"speaker": "recipient", "text": "చెప్పండి సార్, ఏమైనా సమస్యా?"},
            {"speaker": "caller", "text": "మీ అకౌంట్ సురక్షితంగానే ఉంది. ప్రస్తుతం జరుగుతున్న డిజిటల్ అరెస్ట్ మరియు కొరియర్ మోసాల పట్ల ప్రజలను అప్రమత్తం చేస్తున్నాము."},
            {"speaker": "recipient", "text": "ప్రజలు ఎలాంటి జాగ్రత్తలు తీసుకోవాలి సార్?"},
            {"speaker": "caller", "text": "పోలీసులు గానీ సీబీఐ అధికారులు గానీ ఎప్పుడూ వీడియో కాల్స్ చేసి డిజిటల్ అరెస్ట్ చేయరు మరియు డబ్బులు డిమాండ్ చేయరు."},
            {"speaker": "recipient", "text": "మేము ఏదైనా నంబర్ నొక్కాలా సార్?"},
            {"speaker": "caller", "text": "ఏ నంబర్ నొక్కాల్సిన పనిలేదు. మోసపూరిత కాల్స్ వస్తే తక్షణమే 1930 టోల్ ఫ్రీ నంబర్ కి ఫిర్యాదు చేయండి."},
            {"speaker": "recipient", "text": "చాలా మంచి సమాచారం సార్, ధన్యవాదాలు."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["negative context suppression", "security warning with threat keywords without scam intent"],
        "explanation": "Law enforcement cyber safety public announcement warning against digital arrest and courier scams.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/telugu/kav_synth_056.wav"
    })

    # KAV-SYNTH-057
    items.append({
        "conversation_id": "KAV-SYNTH-057",
        "language": "te",
        "primary_label": "AMBIGUOUS",
        "scenario": "Urgent Money Borrowing Request from Childhood Friend",
        "dialogue": [
            {"speaker": "caller", "text": "హలో మూర్తి, నేను నీ చిన్ననాటి స్నేహితుడు వాసుని. నన్ను గుర్తుపట్టావా?"},
            {"speaker": "recipient", "text": "వాసూ! ఎన్నాళ్ళయిందిరా మాట్లాడి. ఎలా ఉన్నావ్? ఫోన్ నంబర్ మార్చావా?"},
            {"speaker": "caller", "text": "అవునురా, పాత ఫోన్ పోయింది. ప్రస్తుతం వైజాగ్ కేర్ హాస్పిటల్ లో ఉన్నానురా."},
            {"speaker": "recipient", "text": "హాస్పిటల్ లోనా? ఎవరికి ఒంట్లో బాగోలేదురా?"},
            {"speaker": "caller", "text": "మా అమ్మగారికి సడెన్ గా గుండె నొప్పి వచ్చిందిరా. అడ్మిషన్ కోసం పదివేలు అర్జెంట్ గా కావాలి, నా కార్డ్ బ్లాక్ అయింది."},
            {"speaker": "recipient", "text": "అయ్యో! మీ తమ్ముడికి ఫోన్ చేసి కనుక్కోనా?"},
            {"speaker": "caller", "text": "వాడు ఊర్లో లేడురా. దయచేసి నేను పంపిన యూపీఐ నంబర్ కి పదివేలు పంపరా, రేపు ఉదయమే ఇచ్చేస్తా."},
            {"speaker": "recipient", "text": "సరేరా, నేను మీ ఇంటి నంబర్ కి ఒకసారి కాల్ చేసి మాటాడి వెంటనే పంపిస్తాను."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["childhood friend voice impersonation risk", "medical emergency urgency", "immediate upi borrowing request"],
        "explanation": "Distress call requesting emergency hospital loan; potential voice cloning / friend imposter scam or genuine personal favor.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-058
    items.append({
        "conversation_id": "KAV-SYNTH-058",
        "language": "te",
        "primary_label": "AMBIGUOUS",
        "scenario": "Unregistered Real Estate Broker Advance Token Query",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం సార్, శంషాబాద్ ఎయిర్‌పోర్ట్ దగ్గర హైవే ఫేసింగ్ ఓపెన్ ప్లాట్లు చాలా తక్కువ ధరకు ఉన్నాయి."},
            {"speaker": "recipient", "text": "మీది ఏ రియల్ ఎస్టేట్ కంపెనీ అండి? హెచ్ఎండీఏ అనుమతులు ఉన్నాయా?"},
            {"speaker": "caller", "text": "లేఅవుట్ పర్మిషన్ ప్రాసెసింగ్ లో ఉంది సార్. చదరపు గజం కేవలం పదివేలకే ఇస్తున్నాం, వచ్చే నెల డబుల్ అవుతుంది."},
            {"speaker": "recipient", "text": "పర్మిషన్ లేకుండా రిజిస్ట్రేషన్ ఎలా చేస్తారు?"},
            {"speaker": "caller", "text": "ఇది ప్రీ-లాంచ్ ఆఫర్ సార్. రేపు సైట్ విజిట్ కోసం యాభై వేల టోకెన్ అడ్వాన్స్ ఇస్తే ప్లాట్ బుక్ చేస్తాం."},
            {"speaker": "recipient", "text": "మీ రేరా రిజిస్ట్రేషన్ నంబర్ చెప్పండి."},
            {"caller": "caller", "speaker": "caller", "text": "డాక్యుమెంట్స్ అన్నీ మా సైట్ ఆఫీస్ లో ఉన్నాయి సార్. మీరు అక్కడికి వచ్చి చూసి లాయర్ ఒపీనియన్ తీసుకున్నాకే చెల్లించవచ్చు."},
            {"speaker": "recipient", "text": "సరే, నేను డాక్యుమెంట్లు లాయర్ కి చూపించాక మాత్రమే నిర్ణయం తీసుకుంటాను."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["pre-launch real estate solicitation", "unverified layout permissions", "legal verification offered"],
        "explanation": "High-risk real estate pre-launch telemarketing call; lacks statutory RERA permits but allows offline legal vetting.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-059
    items.append({
        "conversation_id": "KAV-SYNTH-059",
        "language": "te",
        "primary_label": "AMBIGUOUS",
        "scenario": "Mobile Banking Profile Verification Incomplete Information",
        "dialogue": [
            {"speaker": "caller", "text": "నమస్కారం, బ్యాంక్ డిజిటల్ ఛానల్స్ సపోర్ట్ డెస్క్ నుండి. మీ మొబైల్ బ్యాంకింగ్ యాప్ లో కొత్త ఫీచర్లు యాక్టివేట్ అయ్యాయి."},
            {"speaker": "recipient", "text": "కొత్త ఫీచర్లా? ఏంటి అవి?"},
            {"speaker": "caller", "text": "రోజువారీ ట్రాన్సాక్షన్ పరిమితిని ఐదు లక్షల వరకు పెంచుకోవచ్చు. దీనికి ప్రొఫైల్ వెరిఫికేషన్ అవసరం."},
            {"speaker": "recipient", "text": "నాకు అంత పెద్ద పరిమితి అవసరం లేదు కదా."},
            {"speaker": "caller", "text": "సర్వర్ లో అప్డేట్ రావడం వల్ల మీ పుట్టిన తేదీ మరియు ఈమెయిల్ ఐడీని కన్ఫర్మ్ చేయాలి."},
            {"speaker": "recipient", "text": "ఫోన్ లో ఎందుకు కన్ఫర్మ్ చేయాలి? యాప్ లోనే చేసుకోవచ్చు కదా?"},
            {"caller": "caller", "speaker": "caller", "text": "మీరు యాప్ లో సెట్టింగ్స్ లోకి వెళ్లి కూడా మార్చుకోవచ్చు సర్. ఇబ్బంది ఉంటే బ్రాంచ్ ని సంప్రదించండి."},
            {"speaker": "recipient", "text": "నేను నేరుగా బ్రాంచ్ లోనే సరిచూసుకుంటాను."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["profile confirmation probe", "demographic details solicitation", "official branch option acknowledged"],
        "explanation": "Ambiguous banking profile verification call collecting demographic data with legitimate branch alternative provided.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-060
    items.append({
        "conversation_id": "KAV-SYNTH-060",
        "language": "te",
        "primary_label": "AMBIGUOUS",
        "scenario": "Old Vehicle Sale Negotiation with Unverified Online Buyer",
        "dialogue": [
            {"speaker": "caller", "text": "హలో అండి, ఓఎల్ఎక్స్ లో మీరు పెట్టిన హోండా యాక్టివా స్కూటర్ ప్రకటన చూసి కాల్ చేస్తున్నాను."},
            {"speaker": "recipient", "text": "అవునండి, నలభై వేలు చెబితే చూడ్డానికి వస్తారా?"},
            {"speaker": "caller", "text": "నేను ఆర్మీ క్యాంప్ లో పని చేస్తున్నాను సర్. స్కూటర్ నాకు నచ్చింది, వెంటనే కొనేస్తాను."},
            {"speaker": "recipient", "text": "గాడీ చూసుకోకుండా ఎలా కొంటారు బ్రదర్?"},
            {"speaker": "caller", "text": "ఫోటోలు చూశాను సర్. నేను ఆర్మీ ట్రాన్స్పోర్ట్ లో పంపిస్తాను. నా అకౌంట్ నుండి మీకు వెంటనే ఫుల్ పేమెంట్ పంపించమంటారా?"},
            {"speaker": "recipient", "text": "డబ్బులు నా అకౌంట్ కి ఎలా పంపుతారు?"},
            {"caller": "caller", "speaker": "caller", "text": "నేను మీకు ఒక క్యూఆర్ కోడ్ పంపిస్తాను, దాన్ని స్కాన్ చేస్తే డబ్బులు మీ అకౌంట్ లో పడతాయి."},
            {"speaker": "recipient", "text": "క్యూఆర్ స్కాన్ చేస్తే నా డబ్బులు కట్ అవుతాయి. ఆర్మీ పేరు చెప్పి మోసం చేయాలని చూడకు. నగదుతో నేరుగా రా."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["army personnel buyer pretext", "qr code receive money misunderstanding", "rush to purchase without inspection"],
        "explanation": "Classic OLX unverified buyer negotiation utilizing army pretext and QR code mechanism.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    return items

if __name__ == "__main__":
    items = get_telugu_conversations()
    print(f"Generated {len(items)} Telugu conversations.")

