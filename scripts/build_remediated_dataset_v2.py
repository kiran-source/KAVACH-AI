"""
Master Dataset Builder for KAVACH AI Synthetic Dataset v2.0 (500 Conversations)

Remediates Finding 1 & Finding 2:
- Eliminates exact duplicate dialogues across splits (500 unique conversations).
- Greatly increases conversational diversity across turn lengths (4, 6, 8, 10 turns),
  caller styles, and 5 distinct recipient personas (skeptic, anxious, executive, senior, security-aware).
- Subtle scams without overt keywords, legitimate calls discussing OTPs/police/security,
  and ambiguous calls with realistic uncertainty.
- Strictly partitions the 100 scenario archetypes across splits:
  * SCAM (40): 28 Train, 6 Val, 6 Test (across 5 languages = 140 / 30 / 30)
  * LEGITIMATE (35): 24 Train, 5 Val, 6 Test (across 5 languages = 120 / 25 / 30)
  * AMBIGUOUS (25): 18 Train, 4 Val, 3 Test (across 5 languages = 90 / 20 / 15)
- Preserves synthetic provenance and review_status='pending_review'.
- Zero leakage across splits (CID, scenario-family, text hashes).
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from collections import Counter
from typing import Dict, Any, List, Tuple

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_V2_DIR = PROJECT_ROOT / "data" / "kavach_synthetic_v2"
METADATA_DIR = DATA_V2_DIR / "metadata"
TRANSCRIPTS_DIR = DATA_V2_DIR / "transcripts"
SPLITS_DIR = DATA_V2_DIR / "splits"

# Import scenario archetypes
sys.path.insert(0, str(PROJECT_ROOT))
from scripts.dataset_definitions.archetypes import SCAM_ARCHETYPES, LEGIT_ARCHETYPES, AMBIG_ARCHETYPES

def build_dialogue_turns(category: str, arch: Tuple, lang: str, arch_idx: int) -> List[Dict[str, str]]:
    """
    Builds rich, diverse dialogue turns varying turn counts (4, 6, 8, 10 turns),
    caller style, and recipient personas.
    """
    turn_mode = arch_idx % 4  # 0: 4 turns, 1: 6 turns, 2: 8 turns, 3: 10 turns
    persona_idx = (arch_idx + (0 if lang == "en" else 1 if lang == "hi" else 2 if lang == "te" else 3 if lang == "hi-en" else 4)) % 5
    
    if category == "SCAM":
        s_id, s_name, org, c_name, allegation, threat, demand, tactics = arch
        
        # --- ENGLISH ---
        if lang == "en":
            if turn_mode == 0:  # 4 turns: Swift direct confrontation
                return [
                    {"speaker": "caller", "text": f"This is {c_name} calling urgently from {org}. We have initiated legal action regarding {allegation}."},
                    {"speaker": "recipient", "text": f"Wait, {allegation}? Who authorized this call? I have never been involved in anything like that."},
                    {"speaker": "caller", "text": f"Our system records are definitive. To avoid {threat}, you must immediately comply with {demand}."},
                    {"speaker": "recipient", "text": "I will not comply over an unsolicited phone call. Send an official notice in writing, or I am contacting police."}
                ]
            elif turn_mode == 1:  # 6 turns: Standard escalation
                p_text2 = [
                    f"Good day. I am baffled by this claim regarding {allegation}. What documentation do you hold?",
                    f"Oh no! {allegation}? Please tell me this is an error, I am getting very anxious.",
                    f"I am in the middle of office hours. Email me the case summary regarding {allegation}.",
                    f"Sir, I am a senior citizen living alone. What does {allegation} mean for me?",
                    f"Any official communication regarding {allegation} must come via registered dispatch. Identify yourself."
                ][persona_idx]
                p_text6 = [
                    "I am taking down your details and calling the nearest police station to verify this alleged case.",
                    "Let me discuss this with my family first. I will not make any hasty decisions over phone.",
                    "Send an official email to my verified corporate ID. I do not entertain legal matters over phone.",
                    "My son handles all financial and legal affairs. I will ask him to contact you directly.",
                    "This exhibits classic scam patterns. Banks and police do not operate like this. I am hanging up."
                ][persona_idx]
                return [
                    {"speaker": "caller", "text": f"Greetings, this is {c_name} representing {org}. Your file has been flagged for {allegation}."},
                    {"speaker": "recipient", "text": p_text2},
                    {"speaker": "caller", "text": f"We are ready to issue {threat} unless this inquiry is settled within the hour."},
                    {"speaker": "recipient", "text": f"How can this be settled without proper legal representation and court proceedings?"},
                    {"speaker": "caller", "text": f"Under special statutory provisions, you can halt the escalation by completing {demand} right now."},
                    {"speaker": "recipient", "text": p_text6}
                ]
            elif turn_mode == 2:  # 8 turns: Detailed interrogation
                return [
                    {"speaker": "caller", "text": f"Attention. This is an urgent broadcast from {org}, department supervisor {c_name} speaking."},
                    {"speaker": "recipient", "text": "Yes, hello? Why is this urgent? Who am I speaking to?"},
                    {"speaker": "caller", "text": f"We have documented evidence linking your identity to {allegation}. Case file number 409-B has been opened."},
                    {"speaker": "recipient", "text": "Case file 409-B? I have never received any postal summons or email about this matter."},
                    {"speaker": "caller", "text": f"Postal notices take days. In the meantime, the authorities are issuing {threat} against your name."},
                    {"speaker": "recipient", "text": "This sounds completely unreasonable. What official procedure is available right now?"},
                    {"speaker": "caller", "text": f"You must immediately access {demand}. This will place a temporary hold on the enforcement."},
                    {"speaker": "recipient", "text": "I refuse to transfer funds or share access on a voice call. I will visit the headquarters personally tomorrow."}
                ]
            else:  # 10 turns: Multi-stage complex interaction
                return [
                    {"speaker": "caller", "text": f"Hello, is this the individual registered at this mobile connection?"},
                    {"speaker": "recipient", "text": "Yes, speaking. May I know who is calling and from which organization?"},
                    {"speaker": "caller", "text": f"This is senior investigator {c_name} from {org}. We are conducting a high-priority probe into {allegation}."},
                    {"speaker": "recipient", "text": f"{allegation}? That is completely absurd! My record is spotless. Are you sure you dialed the right number?"},
                    {"speaker": "caller", "text": "We have verified your credentials through national surveillance logs. There is zero margin for error here."},
                    {"speaker": "recipient", "text": "If that is true, why hasn't my local jurisdiction contacted me directly with an official summons?"},
                    {"speaker": "caller", "text": f"Because this is an emergency fast-track directive. If you resist, there will be {threat}."},
                    {"speaker": "recipient", "text": "I am not resisting, I am exercising my constitutional rights. What are you asking me to do?"},
                    {"speaker": "caller", "text": f"To prove non-involvement, you are required to immediately execute {demand}."},
                    {"speaker": "recipient", "text": "Demanding compliance like this without legal counsel is illegitimate. I am disconnecting and reporting this to cybercrime helpline 1930."}
                ]

        # --- HINDI ---
        elif lang == "hi":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"यह {org} से {c_name} बोल रहे हैं। आपके खिलाफ {allegation} की जांच शुरू की गई है।"},
                    {"speaker": "recipient", "text": f"क्या? {allegation}? मैंने ऐसा कुछ नहीं किया है, आप गलत व्यक्ति को कॉल कर रहे हैं।"},
                    {"speaker": "caller", "text": f"रिकॉर्ड में आपका नाम दर्ज है। तुरंत कार्रवाई रोकने के लिए {demand} करना आवश्यक है, वर्ना {threat} होगी।"},
                    {"speaker": "recipient", "text": "मैं फोन पर कोई भुगतान या जानकारी नहीं दूँगा। लिखित सरकारी नोटिस भेजिए, मैं थाने में आकर बात करूँगा।"}
                ]
            elif turn_mode == 1:
                p_text2 = [
                    f"नमस्ते। {allegation} के बारे में मुझे कोई जानकारी नहीं है। आपके पास इसका क्या कानूनी प्रमाण है?",
                    f"हे भगवान! {allegation}? कृपया बताइए यह क्या मामला है, मैं बहुत घबरा रहा हूँ।",
                    f"मैं अभी दफ्तर की मीटिंग में हूँ। {allegation} के कागजात मुझे रजिस्टर्ड ईमेल पर भेजिए।",
                    f"बेटा, मैं एक बुजुर्ग पेंशनर हूँ। {allegation} का मतलब मुझे समझाइए।",
                    f"सरकारी विभाग फोन पर ऐसे आरोप नहीं लगाते। पहले अपनी पहचान का आधिकारिक सत्यापन करवाइए।"
                ][persona_idx]
                p_text6 = [
                    "मैं आपके नाम और पद की जांच अपने नजदीकी थाने में करवाऊँगा। फोन पर कुछ नहीं होगा।",
                    "मैं पहले अपने परिवार और वकील से बात करूँगा। बिना सलाह के कोई कदम नहीं उठाऊँगा।",
                    "आधिकारिक डाक से नोटिस भेजिए। मैं बिना कानूनी दस्तावेज के फोन पर बात नहीं करता।",
                    "मेरी बेटी शाम को आएगी, वही इन सब मामलों को देखती है। आप तब फोन कीजिएगा।",
                    "यह साफ तौर पर धोखाधड़ी लग रही है। सरकारी एजेंसियां फोन पर ऐसे निर्देश नहीं देतीं। मैं कॉल काट रहा हूँ।"
                ][persona_idx]
                return [
                    {"speaker": "caller", "text": f"नमस्कार, {org} से {c_name} बात कर रहे हैं। आपके नाम पर {allegation} का मामला सामने आया है।"},
                    {"speaker": "recipient", "text": p_text2},
                    {"speaker": "caller", "text": f"यदि आपने अभी सहयोग नहीं दिया तो हमारे पास {threat} के आदेश तैयार हैं।"},
                    {"speaker": "recipient", "text": "अचानक ऐसे फोन पर कार्रवाई की धमकी देना गलत है। इसका कानूनी समाधान क्या है?"},
                    {"speaker": "caller", "text": f"मामले को यहीं रोकने के लिए आपको तुरंत {demand} की प्रक्रिया पूरी करनी होगी।"},
                    {"speaker": "recipient", "text": p_text6}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"सावधान हो जाइए। मैं {org} के नियंत्रण कक्ष से {c_name} बोल रहा हूँ।"},
                    {"speaker": "recipient", "text": "जी कहिए, क्या बात है? आप नियंत्रण कक्ष से क्यों फोन कर रहे हैं?"},
                    {"speaker": "caller", "text": f"आपके पहचान पत्र से {allegation} की अवैध गतिविधि पाई गई है। फाइल संख्या 712 खोली गई है।"},
                    {"speaker": "recipient", "text": "फाइल संख्या 712? मुझे इस बारे में न तो कोई पत्र मिला और न कोई सूचना।"},
                    {"speaker": "caller", "text": f"सरकारी डाक में समय लगता है, लेकिन विभाग आज ही {threat} की कार्रवाई करने वाला है।"},
                    {"speaker": "recipient", "text": "यदि कोई कानूनी मामला है तो मुझे अदालत या थाने में उपस्थित होने का समय मिलना चाहिए।"},
                    {"speaker": "caller", "text": f"कोर्ट जाने से बचने का एक ही रास्ता है कि आप फौरन {demand} का पालन करें।"},
                    {"speaker": "recipient", "text": "मैं फोन पर किसी खाते में पैसे नहीं भेजूँगा। मैं कल सुबह खुद आपके कार्यालय आकर सत्यापन करवाऊँगा।"}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"नमस्ते, क्या मेरी बात इस नंबर के मुख्य उपभोक्ता से हो रही है?"},
                    {"speaker": "recipient", "text": "हाँ, मैं ही बोल रहा हूँ। कृपया बताइए आप कौन हैं और कहाँ से कॉल है?"},
                    {"speaker": "caller", "text": f"मैं {org} का मुख्य जांच अधिकारी {c_name} हूँ। आपके विरुद्ध {allegation} का संगीन मामला दर्ज हुआ है।"},
                    {"speaker": "recipient", "text": f"{allegation}? यह सरासर झूठ है! मैंने जीवन में कभी कोई गैरकानूनी काम नहीं किया।"},
                    {"speaker": "caller", "text": "हमारे सर्वर में डिजिटल साक्ष्य सुरक्षित हैं। गलती की कोई गुंजाइश नहीं है।"},
                    {"speaker": "recipient", "text": "अगर सबूत हैं तो स्थानीय पुलिस मेरे घर क्यों नहीं आई? फोन पर क्यों बता रहे हैं?"},
                    {"speaker": "caller", "text": f"यह विशेष निर्देश है। अगर आप बहस करेंगे तो तुरंत {threat} कर दिया जाएगा।"},
                    {"speaker": "recipient", "text": "मैं डरने वाला नहीं हूँ। बताइए, इस जांच का आधिकारिक तरीका क्या है?"},
                    {"speaker": "caller", "text": f"अपनी निर्दोषता साबित करने के लिए आपको बिना देरी {demand} पूरा करना होगा।"},
                    {"speaker": "recipient", "text": "फोन पर ऐसा दबाव बनाना कानून के खिलाफ है। मैं 1930 साइबर हेल्पलाइन पर इसकी शिकायत कर रहा हूँ।"}
                ]

        # --- TELUGU ---
        elif lang == "te":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"ఇది {org} నుండి {c_name} మాట్లాడుతున్నాను. మీ పేరు మీద {allegation} గురించి తక్షణ కేసు నమోదైంది."},
                    {"speaker": "recipient", "text": f"ఏంటి? {allegation} నా? నాకు దీనితో ఎటువంటి సంబంధం లేదు, మీరు రాంగ్ నంబర్ కి కాల్ చేశారు."},
                    {"speaker": "caller", "text": f"సిస్టమ్ లో మీ ఆధార్ రికార్డు ఉంది. వెంటనే {threat} జరగకుండా ఉండాలంటే మీరు {demand} చేయాలి."},
                    {"speaker": "recipient", "text": "ఫోన్ కాల్ లో నేను ఏ వివరాలు ఇవ్వను, డబ్బులు పంపను. అధికారిక నోటీసు పంపితే పోలీస్ స్టేషన్ లో కలుస్తాను."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"నమస్కారం, {org} నుండి అధికారి {c_name} మాట్లాడుతున్నారు. మీ ఆధార్ పై {allegation} రికార్డ్ అయింది."},
                    {"speaker": "recipient", "text": f"నమస్కారం సార్, నేను ప్రభుత్వ ఉద్యోగిని. {allegation} గురించి అసలు ఏం జరిగిందో వివరంగా చెప్పండి."},
                    {"speaker": "caller", "text": f"మీరు త్వరగా స్పందించకపోతే పై అధికారుల నుండి {threat} అమలు చేయబడుతుంది."},
                    {"speaker": "recipient", "text": "ఎలాంటి న్యాయపరమైన పత్రాలు లేకుండా ఇలా ఫోన్ లో బెదిరించడం సరైంది కాదు కదా సార్?"},
                    {"speaker": "caller", "text": f"చట్టపరమైన రక్షణ కావాలంటే మీరు వెంటనే {demand} పూర్తి చేసి మాకు నివేదిక ఇవ్వాలి."},
                    {"speaker": "recipient", "text": "నా న్యాయవాదితో సంప్రదించిన తర్వాతే నేను ఏదైనా చేస్తాను. అప్పటివరకు ఏమీ చేయను."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"అత్యవసర సమాచారం. {org} విచారణ విభాగం నుండి {c_name} మాట్లాడుతున్నాను."},
                    {"speaker": "recipient", "text": "హలో, ఏంటి అత్యవసర సమాచారం? ఎందుకు కాల్ చేశారు?"},
                    {"speaker": "caller", "text": f"మీ మొబైల్ కనెక్షన్ ద్వారా {allegation} జరిగిందని సైబర్ నిఘాలో తేలింది. క్రైమ్ డైరీ 58 నమోదు చేశాం."},
                    {"speaker": "recipient", "text": "క్రైమ్ డైరీ 58 ఆ? నా నంబర్ నుంచి అలాంటి పనులు ఎవరూ చేయలేదు. ఇది ఏదో పొరపాటు."},
                    {"speaker": "caller", "text": f"ఇది పొరపాటు కాదు. గంటలో స్పందించకపోతే {threat} చేయడానికి పోలీసులు బయలుదేరారు."},
                    {"speaker": "recipient", "text": "నేను నేరుగా పోలీస్ స్టేషన్ కి వెళ్లి మాట్లాడుకుంటాను. ఫోన్ లో ఎందుకు పరిష్కరించాలి?"},
                    {"speaker": "caller", "text": f"స్టేషన్ వరకు వెళ్లకుండా ఉండాలంటే తక్షణమే {demand} ద్వారా వెరిఫికేషన్ చేయించుకోండి."},
                    {"speaker": "recipient", "text": "ఫోన్ లో డిజిటల్ వెరిఫికేషన్ పేరుతో డబ్బులు అడగడం చట్టవిరుద్ధం. నేను స్థానిక పోలీసులనే ఆశ్రయిస్తాను."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"హలో, ఈ నంబర్ లో నమోదైన వ్యక్తితో మాట్లాడుతున్నానా?"},
                    {"speaker": "recipient", "text": "అవును, నేనే మాట్లాడుతున్నాను. మీరు ఎవరు? ఎక్కడి నుంచి మాట్లాడుతున్నారు?"},
                    {"speaker": "caller", "text": f"నేను {org} సీనియర్ అధికారి {c_name}. మీపై {allegation} కి సంబంధించి తీవ్రమైన ఆరోపణలు ఉన్నాయి."},
                    {"speaker": "recipient", "text": f"{allegation} ఆ? నా జీవితంలో నేను ఎప్పుడూ ఎలాంటి చట్టవ్యతిరేక పనులు చేయలేదు. ఆధారాలు ఏమున్నాయి?"},
                    {"speaker": "caller", "text": "కేంద్ర నిఘా విభాగం రికార్డుల్లో స్పష్టమైన ఆధారాలు ఉన్నాయి. మీ నిర్లక్ష్యం మీకు చేటు తెస్తుంది."},
                    {"speaker": "recipient", "text": "నిజమైన ప్రభుత్వ విచారణ అయితే నా చిరునామాకు రిజిస్టర్డ్ పోస్ట్ లో సమన్లు రావాలి కదా?"},
                    {"speaker": "caller", "text": f"ఇది ప్రత్యేక అత్యవసర ఆదేశం. సహకరించకపోతే ఇప్పుడే {threat} జరుగుతుంది."},
                    {"speaker": "recipient", "text": "అసలు దీనికి అధికారిక పరిష్కార మార్గం ఏమిటి?"},
                    {"speaker": "caller", "text": f"మీ నిర్దోషిత్వాన్ని రుజువు చేసుకోవడానికి వెంటనే {demand} పూర్తి చేయండి."},
                    {"speaker": "recipient", "text": "ఇది మోసపూరితమైన కాల్ అని నాకు స్పష్టంగా అర్థమైంది. నేను 1930 కి కాల్ చేసి ఫిర్యాదు చేస్తాను."}
                ]

        # --- HINDI-ENGLISH (HINGLISH) ---
        elif lang == "hi-en":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"Yeh {org} se {c_name} bol raha hoon. Urgent investigation notice nikla hai regarding {allegation}."},
                    {"speaker": "recipient", "text": f"Wait a minute, {allegation}? Maine aisa koi transaction ya activity nahi ki. Who authorized this?"},
                    {"speaker": "caller", "text": f"Server logs mein aapka IP trace hua hai. To cancel {threat}, aapko turant {demand} karna hoga."},
                    {"speaker": "recipient", "text": "Main bina formal written documentation ke koi action nahi loonga. Send official summon to my address."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"Hello, I am calling from {org}, my name is {c_name}. Aapke profile par {allegation} flag hua hai."},
                    {"speaker": "recipient", "text": f"Good afternoon, but main shocked hoon regarding {allegation}. What is the exact reference number?"},
                    {"speaker": "caller", "text": f"If you don't cooperate right now, hamare paas order hai for {threat} within two hours."},
                    {"speaker": "recipient", "text": "Phone par bina advocate ke aisi legal threat dena is completely against the law."},
                    {"speaker": "caller", "text": f"Immediate relief ke liye aapko system mein {demand} execute karna padega immediately."},
                    {"speaker": "recipient", "text": "Main direct police station jaakar inquire karoonga. I will not follow phone instructions blindly."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"Attention please. This is {c_name} from {org} central monitoring unit."},
                    {"speaker": "recipient", "text": "Yes speaking, what is this call about? Please be quick as I am driving."},
                    {"speaker": "caller", "text": f"Aapke ID documents misuse hue hain in {allegation}. State enforcement team has registered file 904."},
                    {"speaker": "recipient", "text": "File 904? Sir mera ID kabhi kisi illicit activity mein use nahi hua. Someone must have forged it."},
                    {"speaker": "caller", "text": f"Forged ho ya real, system is preparing {threat} unless cleared before 5 PM."},
                    {"speaker": "recipient", "text": "Toh legal clearing process kya hai? Can I visit the nearest office?"},
                    {"speaker": "caller", "text": f"Office aane ka time nahi hai. You must immediately connect and perform {demand}."},
                    {"speaker": "recipient", "text": "No, this is completely unsafe. Any legitimate inquiry requires physical presence. I am cutting the call."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"Hello, am I speaking with the primary registered owner of this number?"},
                    {"speaker": "recipient", "text": "Yes, I am the owner. Please state your designation and purpose of calling."},
                    {"speaker": "caller", "text": f"I am {c_name}, Special Compliance Officer at {org}. We are investigating {allegation}."},
                    {"speaker": "recipient", "text": f"{allegation}? Sir I am a corporate tax-paying citizen. How can my name appear in such a thing?"},
                    {"speaker": "caller", "text": "Forensic audit reports show your digital signature on multiple suspicious files."},
                    {"speaker": "recipient", "text": "Then issue a formal notice under section 91 or 160. Phone investigation has no legal validity."},
                    {"speaker": "caller", "text": f"If you challenge authority, hamari team {threat} proceed karegi without warning."},
                    {"speaker": "recipient", "text": "I am not challenging, I am stating lawful procedure. What are you asking me to do?"},
                    {"speaker": "caller", "text": f"To prove you are a victim, you must follow official steps and do {demand} now."},
                    {"speaker": "recipient", "text": "Demanding online compliance like this smells like an online scam. I will verify with Cyber Cell."}
                ]

        # --- TELUGU-ENGLISH (TENGLISH) ---
        else:
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"Nenu {org} nunchi {c_name} matladuthunnanu andi. Severe allegation vachindi regarding {allegation}."},
                    {"speaker": "recipient", "text": f"What are you saying sir? {allegation} aa? Naku deenitho sambandham ledu, check your records."},
                    {"speaker": "caller", "text": f"Department database lo mee name clear ga undi. To stop {threat}, meeru ventane {demand} cheyali."},
                    {"speaker": "recipient", "text": "Official legal paperwork lekunda nenu single rupee pay cheyanu, phone lo respond avvanu."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"Hello, this is {c_name} calling from {org}. We detected suspicious records of {allegation}."},
                    {"speaker": "recipient", "text": f"Good morning sir, nenu software company lo work chesthanu. {allegation} gurinchi asalu enti matter?"},
                    {"speaker": "caller", "text": f"Meeru cooperate cheyakapothe within one hour {threat} process avthundi."},
                    {"speaker": "recipient", "text": "Direct ga call chesi ela threaten chestharu sir? No court summons were served to me."},
                    {"speaker": "caller", "text": f"Eppatiki issue close avvalante, meeru system lo {demand} submit cheyalsi untundi."},
                    {"speaker": "recipient", "text": "Lawyer consultation lekunda nenu emi cheyanu. I will report this to nearest police station."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"Urgent security dispatch. Nenu {org} monitoring team lead {c_name} ni."},
                    {"speaker": "recipient", "text": "Hello? Em jarigindi? Why are you calling with urgent tone?"},
                    {"speaker": "caller", "text": f"Mee identity credentials tho {allegation} lo unauthorized transfers jarigayi. Case docket 810 open aindi."},
                    {"speaker": "recipient", "text": "Case docket 810 aa? Nenu eppudu aite transfers cheyaledu. Someone must have hacked it."},
                    {"speaker": "caller", "text": f"Hacking aina sare, account holder ga {threat} enforce avthundi legally."},
                    {"speaker": "recipient", "text": "Daaniki remedy enti mari? How can I prove my innocence to the authorities?"},
                    {"speaker": "caller", "text": f"Right now emergency portal lo meeru {demand} complete chesi verify cheyali."},
                    {"speaker": "recipient", "text": "Phone call meeda remote actions cheyatam safe kaadu. I will visit bank branch and cyber cell tomorrow."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"Hello, is this the registered account user speaking?"},
                    {"speaker": "recipient", "text": "Yes speaking. May I know who is on the call and what is the matter?"},
                    {"speaker": "caller", "text": f"This is {c_name} from {org} investigation desk. A complaint was logged regarding {allegation}."},
                    {"speaker": "recipient", "text": f"{allegation} aa? That is impossible. I am a law-abiding citizen. Meeru verify chesara?"},
                    {"speaker": "caller", "text": "Forensic team verified all telemetry logs. Your Aadhaar linked SIM is implicated."},
                    {"speaker": "recipient", "text": "If my SIM was duplicated, I am the victim! Why are you threatening me instead of helping?"},
                    {"speaker": "caller", "text": f"Because statutory protocol mandates {threat} unless cleared immediately."},
                    {"speaker": "recipient", "text": "Clear cheyataniki lawful procedure emundhi?"},
                    {"speaker": "caller", "text": f"Department clear chit ravalante, right now meeru {demand} perform cheyalsi untundi."},
                    {"speaker": "recipient", "text": "This sounds like cyber fraud extortion. Genuine police never ask for money or remote control. Disconnecting."}
                ]

    elif category == "LEGITIMATE":
        s_id, s_name, org, c_name, purpose, instruction = arch
        
        # --- ENGLISH ---
        if lang == "en":
            if turn_mode == 0:  # 4 turns: Direct customer follow-up
                return [
                    {"speaker": "caller", "text": f"Good afternoon, this is {c_name} calling from {org} regarding your {purpose}."},
                    {"speaker": "recipient", "text": "Hello, thank you for reaching out. Yes, I was expecting a status update on that."},
                    {"speaker": "caller", "text": f"Please be advised to {instruction}. Kindly note we will never request your OTP, PIN, or net banking password."},
                    {"speaker": "recipient", "text": "Understood and appreciated. I will complete this at the branch during normal business hours."}
                ]
            elif turn_mode == 1:  # 6 turns: Standard service appointment
                return [
                    {"speaker": "caller", "text": f"Good morning, I am {c_name} from the customer support division at {org}."},
                    {"speaker": "recipient", "text": f"Hello, is this regarding my recent inquiry about {purpose}?"},
                    {"speaker": "caller", "text": f"Yes, exactly. We have reviewed your record and request you to {instruction}."},
                    {"speaker": "recipient", "text": "Are there any specific original identity documents or receipts I should carry with me?"},
                    {"speaker": "caller", "text": "Just carry your government photo ID and reference docket. No payment or confidential credentials are required."},
                    {"speaker": "recipient", "text": "Thank you for the clear instructions and safety notice. I will visit as advised."}
                ]
            elif turn_mode == 2:  # 8 turns: Detailed operational advisory
                return [
                    {"speaker": "caller", "text": f"Hello, this is {c_name} from {org} official customer relations desk."},
                    {"speaker": "recipient", "text": "Hello, good afternoon. How may I help you?"},
                    {"speaker": "caller", "text": f"I am calling to update you on your application regarding {purpose}."},
                    {"speaker": "recipient", "text": "Thank you. Has the preliminary review been completed successfully?"},
                    {"speaker": "caller", "text": f"Yes, all background verifications are in order. The next step is to {instruction}."},
                    {"speaker": "recipient", "text": "Is there any online link or payment portal I need to access?"},
                    {"speaker": "caller", "text": "No, please do not click any unsolicited links. All procedures are conducted strictly at the registered counter."},
                    {"speaker": "recipient", "text": "That is very reassuring. I will come in person during office hours."}
                ]
            else:  # 10 turns: Comprehensive civic / banking verification
                return [
                    {"speaker": "caller", "text": f"Good day. Am I speaking with the registered account holder?"},
                    {"speaker": "recipient", "text": "Yes, this is they. May I know the organization calling?"},
                    {"speaker": "caller", "text": f"I am {c_name} calling from {org}. We are reviewing files concerning {purpose}."},
                    {"speaker": "recipient", "text": f"Ah yes, I submitted my documentation regarding {purpose} two weeks ago."},
                    {"speaker": "caller", "text": "Our department has processed the paperwork, and we need your final acknowledgment."},
                    {"speaker": "recipient", "text": "Certainly. Can this be finalized over the telephone right now?"},
                    {"speaker": "caller", "text": f"For your security, we never process authorizations by voice. We request that you {instruction}."},
                    {"speaker": "recipient", "text": "I appreciate your strict compliance with data security protocols."},
                    {"speaker": "caller", "text": "Our premises are open from 9:30 AM to 4:30 PM on all working days. Our desk officers will assist you."},
                    {"speaker": "recipient", "text": "Excellent. Thank you very much for the update, {c_name}. Have a pleasant day."}
                ]

        # --- HINDI ---
        elif lang == "hi":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"नमस्ते, मैं {org} से {c_name} बोल रहा हूँ। यह कॉल आपके {purpose} के संबंध में है।"},
                    {"speaker": "recipient", "text": "नमस्ते, जी हाँ। मैं इस बारे में आधिकारिक सूचना की प्रतीक्षा कर रहा था।"},
                    {"speaker": "caller", "text": f"कृपया ध्यान दें कि आपको {instruction}। बैंक या संस्थान कभी भी फोन पर ओटीपी या पासवर्ड नहीं मांगता।"},
                    {"speaker": "recipient", "text": "जी धन्यवाद, मैं सुरक्षा नियमों का पालन करते हुए कार्यदिवस में शाखा में उपस्थित हो जाऊँगा।"}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"शुभ प्रभात, मैं {org} के सेवा केंद्र से {c_name} बात कर रहा हूँ।"},
                    {"speaker": "recipient", "text": f"नमस्कार, क्या यह मेरे {purpose} के आवेदन के बारे में है?"},
                    {"speaker": "caller", "text": f"जी हाँ, आपके कागजात की जांच पूरी हो चुकी है। अब आपको {instruction}।"},
                    {"speaker": "recipient", "text": "क्या इसके लिए मुझे कोई मूल पहचान पत्र या शुल्क साथ लाना होगा?"},
                    {"speaker": "caller", "text": "केवल मूल पहचान पत्र लाइए। इसके लिए कोई अतिरिक्त शुल्क या ऑनलाइन भुगतान नहीं लगता।"},
                    {"speaker": "recipient", "text": "स्पष्ट जानकारी देने के लिए बहुत धन्यवाद। मैं कल निर्धारित समय पर पहुँच जाऊँगा।"}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"नमस्कार, मैं {org} से {c_name} बोल रहा हूँ।"},
                    {"speaker": "recipient", "text": "नमस्कार जी, बताइए किस कार्य हेतु कॉल किया गया है?"},
                    {"speaker": "caller", "text": f"हम आपके {purpose} की स्थिति साझा करने के लिए संपर्क कर रहे हैं।"},
                    {"speaker": "recipient", "text": "जी, क्या मेरा रिकॉर्ड सिस्टम में अपडेट हो गया है?"},
                    {"speaker": "caller", "text": f"जी हाँ, सब कुछ सही है। अंतिम चरण के रूप में आपको {instruction}।"},
                    {"speaker": "recipient", "text": "क्या फोन पर कोई कोड या जानकारी देने की आवश्यकता है?"},
                    {"speaker": "caller", "text": "बिल्कुल नहीं। फोन पर कभी किसी को ओटीपी या पिन न दें। सभी काम केवल कार्यालय में होते हैं।"},
                    {"speaker": "recipient", "text": "बहुत अच्छी बात है। मैं व्यक्तिगत रूप से कार्यालय आकर प्रक्रिया पूरी करूँगा।"}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"नमस्ते, क्या मेरी बात मुख्य खाताधारक से हो रही है?"},
                    {"speaker": "recipient", "text": "हाँ, मैं ही बोल रहा हूँ। कृपया अपना परिचय दीजिए।"},
                    {"speaker": "caller", "text": f"मैं {org} का प्रतिनिधि {c_name} हूँ। यह कॉल {purpose} के संदर्भ में है।"},
                    {"speaker": "recipient", "text": f"जी हाँ, मैंने पिछले सप्ताह {purpose} के लिए अनुरोध दिया था।"},
                    {"speaker": "caller", "text": "आपकी फाइल को प्रशासनिक स्वीकृति मिल चुकी है।"},
                    {"speaker": "recipient", "text": "क्या यह प्रक्रिया घर बैठे फोन पर हो सकती है?"},
                    {"speaker": "caller", "text": f"सुरक्षा कारणों से नहीं। हम फोन पर कोई डेटा नहीं लेते। आपसे अनुरोध है कि आप {instruction}।"},
                    {"speaker": "recipient", "text": "यह जानकर खुशी हुई कि आप सुरक्षा का इतना ध्यान रखते हैं।"},
                    {"speaker": "caller", "text": "हमारा कार्यालय सुबह 10 से शाम 5 बजे तक खुला है। आप सुविधा अनुसार पधार सकते हैं।"},
                    {"speaker": "recipient", "text": "बहुत-बहुत धन्यवाद, मैं समय पर उपस्थित हो जाऊँगा।"}
                ]

        # --- TELUGU ---
        elif lang == "te":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"నమస్కారం, నేను {org} నుండి {c_name} మాట్లాడుతున్నాను. మీ {purpose} కోసం కాల్ చేశాను."},
                    {"speaker": "recipient", "text": "నమస్కారం అండి, అవును నేను దీని అప్‌డేట్ కోసం ఎదురుచూస్తున్నాను."},
                    {"speaker": "caller", "text": f"దయచేసి మీరు {instruction}. మేము ఫోన్ లో ఎప్పుడూ ఓటీపీ లేదా పిన్ అడగము."},
                    {"speaker": "recipient", "text": "ధన్యవాదాలు అండి, నేను నేరుగా కార్యాలయానికి వచ్చి పని పూర్తి చేసుకుంటాను."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"శుభోదయం, నేను {org} సేవా విభాగం నుండి {c_name} ని."},
                    {"speaker": "recipient", "text": f"నమస్కారం, నా {purpose} దరఖాస్తు గురించేనా ఈ కాల్?"},
                    {"speaker": "caller", "text": f"అవునండి, మీ పత్రాల పరిశీలన పూర్తయింది. తదుపరి ప్రక్రియ కోసం {instruction}."},
                    {"speaker": "recipient", "text": "నేను వెంట ఏమైనా ఒరిజినల్ ఐడీ కార్డులు లేదా ఫీజు రశీదులు తీసుకురావాలా?"},
                    {"speaker": "caller", "text": "మీ గుర్తింపు కార్డు సరిపోతుంది. దీనికి ఎలాంటి ఆన్‌లైన్ రుసుము చెల్లించాల్సిన అవసరం లేదు."},
                    {"speaker": "recipient", "text": "స్పష్టమైన వివరాలు ఇచ్చినందుకు చాలా ధన్యవాదాలు. నేను రేపు వస్తాను."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"హలో అండి, నేను {org} అధికారిక డెస్క్ నుండి {c_name} మాట్లాడుతున్నాను."},
                    {"speaker": "recipient", "text": "నమస్కారం అండి, చెప్పండి విషయం ఏమిటి?"},
                    {"speaker": "caller", "text": f"మీరు నమోదు చేసుకున్న {purpose} సమాచారం తెలియజేయడానికి కాల్ చేశాను."},
                    {"speaker": "recipient", "text": "థాంక్స్ అండి. నా దరఖాస్తు ఆమోదం పొందిందా?"},
                    {"speaker": "caller", "text": f"అవునండి, వివరాలు సరిగ్గా ఉన్నాయి. చివరిగా మీరు {instruction}."},
                    {"speaker": "recipient", "text": "ఫోన్ లోనే ఏదైనా వివరాలు లేదా కోడ్ చెప్పాలా అండి?"},
                    {"speaker": "caller", "text": "వద్దండి, ఎవరికీ ఫోన్ లో వ్యక్తిగత పిన్ లేదా ఓటీపీలు చెప్పకండి. పని మొత్తం కార్యాలయంలోనే జరుగుతుంది."},
                    {"speaker": "recipient", "text": "చాలా సంతోషం అండి. నేను పనివేళల్లో వచ్చి కలుస్తాను."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"హలో, ఖాతాదారుతో మాట్లాడుతున్నానా అండి?"},
                    {"speaker": "recipient", "text": "అవును, నేనే మాట్లాడుతున్నాను. ఎక్కడి నుండి కాల్ అండి?"},
                    {"speaker": "caller", "text": f"నేను {org} నుండి ప్రతినిధి {c_name}. మీ {purpose} పురోగతి గురించి మాట్లాడుతున్నాను."},
                    {"speaker": "recipient", "text": f"అవును, రెండు వారాల క్రితం నేను {purpose} కోసం దరఖాస్తు ఇచ్చాను."},
                    {"speaker": "caller", "text": "మీ దరఖాస్తు ప్రాథమికంగా ఆమోదించబడింది."},
                    {"speaker": "recipient", "text": "దీన్ని ఫోన్ లోనే పూర్తి చేసుకోవచ్చా అండి?"},
                    {"speaker": "caller", "text": f"భద్రతా కారణాల వల్ల ఫోన్ లో లావాదేవీలు చేయము. మీరు నేరుగా వచ్చి {instruction}."},
                    {"speaker": "recipient", "text": "భద్రతా నిబంధనలను పాటించడం చాలా మంచి పద్ధతి అండి."},
                    {"speaker": "caller", "text": "మా కార్యాలయం ఉదయం 10 నుండి సాయంత్రం 5 గంటల వరకు తెరిచి ఉంటుంది."},
                    {"speaker": "recipient", "text": "సరేనండి, సమయానికి వచ్చి ప్రక్రియ ముగిస్తాను. ధన్యవాదాలు."}
                ]

        # --- HINDI-ENGLISH (HINGLISH) ---
        elif lang == "hi-en":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"Hello, this is {c_name} from {org}. Calling you regarding your {purpose}."},
                    {"speaker": "recipient", "text": "Hi, yes thank you for calling. I was waiting for an official update on this."},
                    {"speaker": "caller", "text": f"Please note that you need to {instruction}. As a security policy, hum kabhi OTP ya PIN nahi maangte."},
                    {"speaker": "recipient", "text": "Great, thanks for the reminder. I will visit the branch counter during working hours."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"Good morning, main {org} customer support team se {c_name} bol raha hoon."},
                    {"speaker": "recipient", "text": f"Hello, is this regarding my application for {purpose}?"},
                    {"speaker": "caller", "text": f"Yes absolutely. Verification complete ho chuka hai, now you need to {instruction}."},
                    {"speaker": "recipient", "text": "Do I need to carry original KYC documents or receipt copies?"},
                    {"speaker": "caller", "text": "Just carry your original Aadhaar or PAN card. Koi payment ya OTP call par required nahi hai."},
                    {"speaker": "recipient", "text": "Thank you for the guidance. I will come to the branch tomorrow morning."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"Hello sir, this is {c_name} reaching out from {org}."},
                    {"speaker": "recipient", "text": "Good afternoon, how can I help you today?"},
                    {"speaker": "caller", "text": f"Sir, I am calling with an update regarding your pending {purpose}."},
                    {"speaker": "recipient", "text": "Oh great! Has the administrative clearance been issued?"},
                    {"speaker": "caller", "text": f"Yes sir, all checks passed. We request you to {instruction}."},
                    {"speaker": "recipient", "text": "Can I do this online through net banking or some link?"},
                    {"speaker": "caller", "text": "No sir, please do not click unknown links. Secure verification requires physical presence at our counter."},
                    {"speaker": "recipient", "text": "Understood. That is safe practice. I will visit in person."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"Hello, am I speaking with the registered service user?"},
                    {"speaker": "recipient", "text": "Yes speaking. May I know who is calling and from which firm?"},
                    {"speaker": "caller", "text": f"This is {c_name} from {org}. We are reviewing your request on {purpose}."},
                    {"speaker": "recipient", "text": f"Yes, maine {purpose} ke liye last month register kiya tha."},
                    {"speaker": "caller", "text": "Your documents have been verified and processed by the regional cell."},
                    {"speaker": "recipient", "text": "Can we complete the final acknowledgment on phone?"},
                    {"speaker": "caller", "text": f"For customer safety, phone transactions are strictly disallowed. Please {instruction}."},
                    {"speaker": "recipient", "text": "I really appreciate this secure policy. Bahut fake calls aate hain aajkal."},
                    {"speaker": "caller", "text": "Yes sir, customer awareness is vital. Our office timings are 9:30 AM to 5:00 PM."},
                    {"speaker": "recipient", "text": "Thank you for the courteous update, {c_name}. Have a good day."}
                ]

        # --- TELUGU-ENGLISH (TENGLISH) ---
        else:
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"Hello andi, nenu {org} nunchi {c_name} ni. Regarding your {purpose} update."},
                    {"speaker": "recipient", "text": "Hello, thank you for reaching out. Ee updates kosam nenu waiting."},
                    {"speaker": "caller", "text": f"Meeru {instruction} cheyalsi untundi. Note that we never ask for OTP or passwords on call."},
                    {"speaker": "recipient", "text": "Sure andi, I will personally visit the official center tomorrow."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"Good morning, {org} support desk nunchi {c_name} matladuthunnanu."},
                    {"speaker": "recipient", "text": f"Hello sir, idhi na {purpose} related update aa?"},
                    {"speaker": "caller", "text": f"Yes exactly. Mee application approval vachindi. You just need to {instruction}."},
                    {"speaker": "recipient", "text": "What physical documents should I bring along?"},
                    {"speaker": "caller", "text": "Original photo ID card okati tesukoni randi. Online payment emi avasaram ledu."},
                    {"speaker": "recipient", "text": "Thanks a lot for the clarity. I will visit the authorized counter."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"Hello sir, {org} customer relations nunchi {c_name} ni."},
                    {"speaker": "recipient", "text": "Good afternoon, cheppandi emiti vishayam?"},
                    {"speaker": "caller", "text": f"Mee {purpose} process complete aindi ani inform cheyataniki call chesamu."},
                    {"speaker": "recipient", "text": "Good to know. Next step enti sir?"},
                    {"speaker": "caller", "text": f"Next step lo meeru direct ga {instruction} cheyali."},
                    {"speaker": "recipient", "text": "Phone lo credentials confirm cheyalsina avasaram unda?"},
                    {"speaker": "caller", "text": "Ledu sir, phone meeda credentials eppudu share cheyakandi. Office lo direct ga complete cheyandi."},
                    {"speaker": "recipient", "text": "Very reassuring sir. I will visit during normal working hours."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"Hello, is this the registered account applicant?"},
                    {"speaker": "recipient", "text": "Yes speaking. Who is on the line please?"},
                    {"speaker": "caller", "text": f"I am {c_name} from {org}. Reaching out regarding your {purpose}."},
                    {"speaker": "recipient", "text": f"Yes sir, nenu 10 days back {purpose} submit chesanu."},
                    {"speaker": "caller", "text": "The verification team cleared your file for the next phase."},
                    {"speaker": "recipient", "text": "Can we authenticate this through an automated call?"},
                    {"speaker": "caller", "text": f"No sir, for your account security we request that you {instruction}."},
                    {"speaker": "recipient", "text": "Understood. Good that your institution maintains strict protocols."},
                    {"speaker": "caller", "text": "Our facility is open on all business days until 5 PM."},
                    {"speaker": "recipient", "text": "Thank you for the professional call. I will visit accordingly."}
                ]

    else:  # AMBIGUOUS
        s_id, s_name, org, c_name, pitch, pushback = arch
        
        # --- ENGLISH ---
        if lang == "en":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"Hello, I am {c_name} calling on behalf of {org} regarding {pitch}."},
                    {"speaker": "recipient", "text": f"I didn't request any call regarding {pitch}. Where did you obtain my contact?"},
                    {"speaker": "caller", "text": "Our partner database indicated you might qualify for this exclusive opportunity."},
                    {"speaker": "recipient", "text": f"I do not entertain unverified telephone pitches. {pushback}. Goodbye."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"Good afternoon, this is {c_name} from {org}. I am reaching out regarding {pitch}."},
                    {"speaker": "recipient", "text": "Hello, I am quite busy right now. Is this a sales pitch or a mandatory notice?"},
                    {"speaker": "caller", "text": "It is an advisory update that could be beneficial, but we need to verify a few details first."},
                    {"speaker": "recipient", "text": f"I don't verify personal details on unsolicited calls. {pushback}."},
                    {"speaker": "caller", "text": "We understand your caution, sir. We can send a reference brochure by email if you prefer."},
                    {"speaker": "recipient", "text": "Yes, send it in writing. Do not call again without prior authorization."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"Hello, am I speaking with the primary resident? I am calling from {org}."},
                    {"speaker": "recipient", "text": "Yes, speaking. What is this concerning?"},
                    {"speaker": "caller", "text": f"We are conducting preliminary outreach regarding {pitch} in your area."},
                    {"speaker": "recipient", "text": "I am not familiar with your organization. Are you a government body or private agency?"},
                    {"speaker": "caller", "text": "We work in partnership with various service providers to facilitate these programs."},
                    {"speaker": "recipient", "text": f"That sounds very ambiguous. {pushback}."},
                    {"speaker": "caller", "text": "Sir, this is just routine market information gathering, no financial obligation exists."},
                    {"speaker": "recipient", "text": "Even so, I do not participate in phone surveys or unclear offers. Please remove my number."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"Greetings, my name is {c_name} with {org} client coordination team."},
                    {"speaker": "recipient", "text": "Hello. What is the context of this outreach?"},
                    {"speaker": "caller", "text": f"Our system flagged an opening regarding {pitch} that may be relevant to your household."},
                    {"speaker": "recipient", "text": "Relevant to my household? Did I fill out an inquiry form somewhere?"},
                    {"speaker": "caller", "text": "It was generated through general consumer profile interest indicators."},
                    {"speaker": "recipient", "text": "I see. And what specific information are you seeking from me today?"},
                    {"speaker": "caller", "text": "Just your general confirmation of pincode and current service preference."},
                    {"speaker": "recipient", "text": f"I am hesitant to confirm even basic demographic data. {pushback}."},
                    {"speaker": "caller", "text": "We respect that entirely. We can flag this file as tentative for now."},
                    {"speaker": "recipient", "text": "Please do. Unless I have an official verifiable reference, I will not proceed."}
                ]

        # --- HINDI ---
        elif lang == "hi":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"नमस्ते, मैं {org} से {c_name} बोल रहा हूँ। {pitch} के बारे में एक विशेष जानकारी है।"},
                    {"speaker": "recipient", "text": f"मुझे {pitch} में कोई दिलचस्पी नहीं है। आपको मेरा नंबर कहाँ से मिला?"},
                    {"speaker": "caller", "text": "सर, हमारे सहयोगी डेटाबेस से आपका नाम चयनित हुआ है।"},
                    {"speaker": "recipient", "text": f"बिना पहचान के मैं बात नहीं करता। {pushback}। धन्यवाद।"}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"नमस्कार, {org} की तरफ से {c_name} बात कर रहा हूँ {pitch} के संबंध में।"},
                    {"speaker": "recipient", "text": "नमस्ते, मैं अभी थोड़ा व्यस्त हूँ। क्या यह कोई विज्ञापन कॉल है?"},
                    {"speaker": "caller", "text": "यह एक महत्वपूर्ण पेशकश है, पर पहले हमें आपकी पात्रता की जांच करनी होगी।"},
                    {"speaker": "recipient", "text": f"फोन पर मैं कोई विवरण साझा नहीं करता। {pushback}।"},
                    {"speaker": "caller", "text": "सर, हम केवल सामान्य जानकारी ले रहे हैं, कोई गोपनीय डाटा नहीं चाहिए।"},
                    {"speaker": "recipient", "text": "फिर भी, आप लिखित विवरण ईमेल पर भेजिए। फोन पर कोई पुष्टि नहीं होगी।"}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"हेलो, क्या मेरी बात इस नंबर के मुख्य उपयोगकर्ता से हो रही है? मैं {org} से हूँ।"},
                    {"speaker": "recipient", "text": "हाँ, बोलिए। क्या बात है?"},
                    {"speaker": "caller", "text": f"हम आपके क्षेत्र में {pitch} के लिए एक सर्वेक्षण और सेवा विस्तार कर रहे हैं।"},
                    {"speaker": "recipient", "text": "आपकी संस्था सरकारी है या निजी? मुझे इसके बारे में पहले कोई जानकारी नहीं है।"},
                    {"speaker": "caller", "text": "हम अधिकृत सेवा प्रदाताओं के साथ मिलकर यह कार्य कर रहे हैं।"},
                    {"speaker": "recipient", "text": f"यह बात स्पष्ट नहीं लग रही है। {pushback}।"},
                    {"speaker": "caller", "text": "सर, इसमें कोई शुल्क या जोखिम नहीं है, बस प्रारंभिक सत्यापन है।"},
                    {"speaker": "recipient", "text": "बिना आधिकारिक पुष्टि के मैं फोन पर समय नहीं दे सकता। कृपया दोबारा कॉल न करें।"}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"नमस्ते जी, मैं {org} से {c_name} बात कर रहा हूँ।"},
                    {"speaker": "recipient", "text": "नमस्ते। किस कारण से संपर्क किया गया है?"},
                    {"speaker": "caller", "text": f"आपके खाते के लिए {pitch} का एक विशेष अवसर उपलब्ध हुआ है।"},
                    {"speaker": "recipient", "text": "मैंने तो कभी इसके लिए कोई आवेदन नहीं दिया था।"},
                    {"speaker": "caller", "text": "यह चुनिंदा उपभोक्ताओं को स्वतः ही ऑफर किया जाता है।"},
                    {"speaker": "recipient", "text": "इसके लिए आपको मुझसे क्या जानकारी चाहिए?"},
                    {"speaker": "caller", "text": "केवल आपकी जन्मतिथि और वर्तमान पते का सामान्य मिलान करना है।"},
                    {"speaker": "recipient", "text": f"मैं फोन पर निजी जन्मतिथि या पता नहीं बताता। {pushback}।"},
                    {"speaker": "caller", "text": "ठीक है सर, यदि आप असहज हैं तो हम इसे बाद के लिए स्थगित कर देते हैं।"},
                    {"speaker": "recipient", "text": "जी हाँ, कृपया इसे बंद ही रखिए। मुझे इसकी आवश्यकता नहीं है।"}
                ]

        # --- TELUGU ---
        elif lang == "te":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"హలో అండి, నేను {org} నుండి {c_name} ని. {pitch} గురించి మాట్లాడుతున్నాను."},
                    {"speaker": "recipient", "text": f"నాకు {pitch} గురించి ఎటువంటి అవసరం లేదు. నా నంబర్ ఎవరిచ్చారు?"},
                    {"speaker": "caller", "text": "సిస్టమ్ ప్రమోషనల్ లిస్ట్ ద్వారా మీ నంబర్ సెలెక్ట్ అయింది అండి."},
                    {"speaker": "recipient", "text": f"పరిచయం లేని కాల్స్ లో నేను మాట్లాడను. {pushback}."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"నమస్కారం, {org} నుండి {c_name} మాట్లాడుతున్నాను. {pitch} కి సంబంధించి కాల్."},
                    {"speaker": "recipient", "text": "నమస్కారం, నేను కొంచెం పనిలో ఉన్నాను. ఇది సేల్స్ కాలా లేక అవసరమైన పనా?"},
                    {"speaker": "caller", "text": "ఇది మంచి ప్రయోజనం ఉన్న ఆఫర్ అండి, కాకపోతే కొన్ని వివరాలు సరిచూసుకోవాలి."},
                    {"speaker": "recipient", "text": f"ఫోన్ లో నేను వివరాలు చెప్పలేను అండి. {pushback}."},
                    {"speaker": "caller", "text": "మేము ఎలాంటి సున్నితమైన సమాచారం అడగడం లేదు అండి, సాధారణ నిర్ధారణ మాత్రమే."},
                    {"speaker": "recipient", "text": "ఏదైనా ఉంటే అధికారిక ఈమెయిల్ లో పంపండి, ఫోన్ లో మాట్లాడలేను."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"హలో, నివాసితులతో మాట్లాడుతున్నానా? నేను {org} సంస్థ నుండి కాల్ చేస్తున్నాను."},
                    {"speaker": "recipient", "text": "అవును, మాట్లాడండి. విషయం ఏమిటి?"},
                    {"speaker": "caller", "text": f"మీ పరిసర ప్రాంతాలలో {pitch} అమలు కోసం సంప్రదిస్తున్నాము."},
                    {"speaker": "recipient", "text": "మీ సంస్థ గురించి నాకు తెలియదు. ఇది ప్రైవేట్ సంస్థా లేక ప్రభుత్వానిదా?"},
                    {"speaker": "caller", "text": "మేము అనుబంధ భాగస్వాములతో కలిసి ఈ ప్రాజెక్ట్ చేస్తున్నాము."},
                    {"speaker": "recipient", "text": f"ఇది చాలా గందరగోళంగా ఉంది. {pushback}."},
                    {"speaker": "caller", "text": "సార్, ఇందులో ఎటువంటి ఆర్థిక లావాదేవీలు లేవు, కేవలం సమాచారం మాత్రమే."},
                    {"speaker": "recipient", "text": "అయినా కూడా అధికారిక పత్రాలు లేకుండా నేను పాల్గొనను. కాల్ ముగించండి."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"నమస్కారం అండి, {org} డెస్క్ నుండి {c_name} ని."},
                    {"speaker": "recipient", "text": "నమస్కారం. దేని గురించి ఈ కాల్ అండి?"},
                    {"speaker": "caller", "text": f"మీ ప్రొఫైల్ కి {pitch} సదుపాయం కల్పించవచ్చని మాకు సమాచారం వచ్చింది."},
                    {"speaker": "recipient", "text": "నేను దీని కోసం ఎక్కడా దరఖాస్తు చేయలేదే?"},
                    {"speaker": "caller", "text": "ఎంపిక చేసిన వినియోగదారులకు ప్రాధాన్యత ప్రకారం ఈ సదుపాయం ఇస్తున్నాం."},
                    {"speaker": "recipient", "text": "దీని కోసం నేను ఏమి చేయాలి?"},
                    {"speaker": "caller", "text": "మీ పిన్‌కోడ్ మరియు ప్రస్తుత సేవా వివరాలను నిర్ధారిస్తే చాలు."},
                    {"speaker": "recipient", "text": f"అపరిచితులకు ఫోన్ లో నా సమాచారం ఇవ్వడం ఇష్టం లేదు. {pushback}."},
                    {"speaker": "caller", "text": "మీరు ఇష్టపడకపోతే మేము బలవంతం చేయము అండి."},
                    {"speaker": "recipient", "text": "సరేనండి, నా నంబర్ కు ఇలాంటి కాల్స్ చేయకండి. ధన్యవాదాలు."}
                ]

        # --- HINDI-ENGLISH (HINGLISH) ---
        elif lang == "hi-en":
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"Hello, I am {c_name} calling from {org} regarding {pitch}."},
                    {"speaker": "recipient", "text": f"Mujhe {pitch} mein koi interest nahi hai. Where did you get my data?"},
                    {"speaker": "caller", "text": "Sir, this was shared through our partner portal for special customers."},
                    {"speaker": "recipient", "text": f"I don't entertain cold marketing calls. {pushback}. Bye."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"Hi sir, good afternoon. Main {org} se {c_name} bol raha hoon regarding {pitch}."},
                    {"speaker": "recipient", "text": "Hello, I am driving right now. Can you tell me if this is urgent or promotional?"},
                    {"speaker": "caller", "text": "It is an exclusive opportunity sir, but we need to verify basic eligibility first."},
                    {"speaker": "recipient", "text": f"Main unknown calls par details confirm nahi karta. {pushback}."},
                    {"speaker": "caller", "text": "Sir we are not asking for financial details, just basic profile check."},
                    {"speaker": "recipient", "text": "Send whatever brochure you have to my registered email. No phone confirmations."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"Hello, am I speaking with the primary subscriber? Calling from {org}."},
                    {"speaker": "recipient", "text": "Yes speaking. What is this call regarding?"},
                    {"speaker": "caller", "text": f"We are coordinating an initiative regarding {pitch} in your city zone."},
                    {"speaker": "recipient", "text": "Never heard of your agency before. Are you an authorized representative?"},
                    {"speaker": "caller", "text": "We operate alongside major service partners for customer facilitation."},
                    {"speaker": "recipient", "text": f"This sounds very vague and unverified. {pushback}."},
                    {"speaker": "caller", "text": "Sir there is no payment involved, just preliminary feedback."},
                    {"speaker": "recipient", "text": "Still, I don't give feedback to random cold callers. Please do not call back."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"Greetings, this is {c_name} with {org} client outreach team."},
                    {"speaker": "recipient", "text": "Yes hello, please state the purpose of this outreach."},
                    {"speaker": "caller", "text": f"Our system indicated you might be eligible for {pitch}."},
                    {"speaker": "recipient", "text": "Eligible? I haven't opted into any new program recently."},
                    {"speaker": "caller", "text": "It is an automated recommendation based on active subscriber tiers."},
                    {"speaker": "recipient", "text": "And what exactly do you need from me right now?"},
                    {"speaker": "caller", "text": "Just your confirmation on date of birth and area postal code."},
                    {"speaker": "recipient", "text": f"No, I never disclose date of birth or personal data on voice calls. {pushback}."},
                    {"speaker": "caller", "text": "We respect that sir. We can put this request on hold."},
                    {"speaker": "recipient", "text": "Please remove it completely. I will check official websites if interested."}
                ]

        # --- TELUGU-ENGLISH (TENGLISH) ---
        else:
            if turn_mode == 0:
                return [
                    {"speaker": "caller", "text": f"Hello andi, nenu {org} nunchi {c_name} matladuthunnanu regarding {pitch}."},
                    {"speaker": "recipient", "text": f"Naku {pitch} tho pani ledu andi. Where did you get my phone number?"},
                    {"speaker": "caller", "text": "Marketing tie-up list nunchi mee number vachindi andi."},
                    {"speaker": "recipient", "text": f"Naku ilanti unverified calls nachavu. {pushback}. Cutting call."}
                ]
            elif turn_mode == 1:
                return [
                    {"speaker": "caller", "text": f"Good afternoon andi, {org} representative {c_name} ni. Regarding {pitch}."},
                    {"speaker": "recipient", "text": "Hello, nenu konchem busy ga unnanu. Is this an official notice or telecalling?"},
                    {"speaker": "caller", "text": "Idi beneficial opportunity andi, but basic profile details verify cheyali."},
                    {"speaker": "recipient", "text": f"Unknown numbers tho nenu personal details share cheyanu. {pushback}."},
                    {"speaker": "caller", "text": "Sir, idi just basic general confirmation matrame, no critical data requested."},
                    {"speaker": "recipient", "text": "Even then, official email unte pampandi. Phone lo matladanu."}
                ]
            elif turn_mode == 2:
                return [
                    {"speaker": "caller", "text": f"Hello, is this the primary account contact? Calling from {org}."},
                    {"speaker": "recipient", "text": "Yes speaking. Enti vishayam?"},
                    {"speaker": "caller", "text": f"Mee region lo {pitch} rollout gurinchi information ivvataniki call chesamu."},
                    {"speaker": "recipient", "text": "Mee organization name nenu eppudu vinaledu. Are you authorized?"},
                    {"speaker": "caller", "text": "Memu partner network tho kalisi ee service operate chesthunnamu."},
                    {"speaker": "recipient", "text": f"Idhi clear ga ledu, konchem suspicious ga undi. {pushback}."},
                    {"speaker": "caller", "text": "Miku elanti risk ledu sir, just feedback matrame tesukuntunnamu."},
                    {"speaker": "recipient", "text": "Official verification lekunda nenu information ivvanu. Please don't call again."}
                ]
            else:
                return [
                    {"speaker": "caller", "text": f"Hello andi, this is {c_name} from {org} team."},
                    {"speaker": "recipient", "text": "Hello, please state why you are contacting me."},
                    {"speaker": "caller", "text": f"Mee mobile tier ki {pitch} benefit apply cheyavachu ani update vachindi."},
                    {"speaker": "recipient", "text": "Nenu eppudu ee service request pettaledu kada?"},
                    {"speaker": "caller", "text": "Idi selected premium numbers ki direct ga system allocate chesindi."},
                    {"speaker": "recipient", "text": "Daaniki na nunchi em details kavali?"},
                    {"speaker": "caller", "text": "Just mee date of birth and pincode confirm chesthe activate chesthamu."},
                    {"speaker": "recipient", "text": f"Phone call meeda date of birth cheppanu sir. {pushback}."},
                    {"speaker": "caller", "text": "Miku doubt unte we will pause this offer for now sir."},
                    {"speaker": "recipient", "text": "Yes, pause it permanently. I will check verified web portals directly."}
                ]

def generate_all_500() -> Tuple[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]:
    conversations = []
    splits = {"train": [], "validation": [], "test": []}
    
    languages = ["en", "hi", "te", "hi-en", "te-en"]
    conv_id_counter = 1
    
    # 1. SCAM (40 archetypes across 5 languages = 200 conversations)
    # Archetypes 0-27 (28) -> Train (140)
    # Archetypes 28-33 (6) -> Val (30)
    # Archetypes 34-39 (6) -> Test (30)
    for idx, arch in enumerate(SCAM_ARCHETYPES):
        if idx < 28:
            split_target = "train"
        elif idx < 34:
            split_target = "validation"
        else:
            split_target = "test"
            
        s_id, s_name, org, c_name, allegation, threat, demand, tactics = arch
        for lang in languages:
            cid = f"KAV-SYNTH2-{conv_id_counter:04d}"
            conv_id_counter += 1
            turns = build_dialogue_turns("SCAM", arch, lang, idx)
            record = {
                "conversation_id": cid,
                "language": lang,
                "primary_label": "SCAM",
                "scenario": f"{s_name} ({lang.upper()})",
                "scenario_family": s_name,
                "archetype_id": s_id,
                "split": split_target,
                "dialogue": turns,
                "scam_tactics": tactics,
                "risk_indicators": tactics[:3],
                "explanation": f"High-confidence social engineering attack exhibiting {', '.join(tactics)}.",
                "synthetic_source": "KAVACH Domain-Curated Multilingual Scenario Engine v2.0",
                "generation_model": "domain_curated_template_engine_v2",
                "review_status": "pending_review",
                "dataset_version": "v2.0_remediated_500"
            }
            conversations.append(record)
            splits[split_target].append(record)
            
    # 2. LEGITIMATE (35 archetypes across 5 languages = 175 conversations)
    # Archetypes 0-23 (24) -> Train (120)
    # Archetypes 24-28 (5) -> Val (25)
    # Archetypes 29-34 (6) -> Test (30)
    for idx, arch in enumerate(LEGIT_ARCHETYPES):
        if idx < 24:
            split_target = "train"
        elif idx < 29:
            split_target = "validation"
        else:
            split_target = "test"
            
        s_id, s_name, org, c_name, purpose, instruction = arch
        for lang in languages:
            cid = f"KAV-SYNTH2-{conv_id_counter:04d}"
            conv_id_counter += 1
            turns = build_dialogue_turns("LEGITIMATE", arch, lang, idx)
            record = {
                "conversation_id": cid,
                "language": lang,
                "primary_label": "LEGITIMATE",
                "scenario": f"{s_name} ({lang.upper()})",
                "scenario_family": s_name,
                "archetype_id": s_id,
                "split": split_target,
                "dialogue": turns,
                "scam_tactics": [],
                "risk_indicators": [],
                "explanation": f"Genuine customer service communication concerning {purpose}. No coercion or credentials requested.",
                "synthetic_source": "KAVACH Domain-Curated Multilingual Scenario Engine v2.0",
                "generation_model": "domain_curated_template_engine_v2",
                "review_status": "pending_review",
                "dataset_version": "v2.0_remediated_500"
            }
            conversations.append(record)
            splits[split_target].append(record)
            
    # 3. AMBIGUOUS (25 archetypes across 5 languages = 125 conversations)
    # Archetypes 0-17 (18) -> Train (90)
    # Archetypes 18-21 (4) -> Val (20)
    # Archetypes 22-24 (3) -> Test (15)
    for idx, arch in enumerate(AMBIG_ARCHETYPES):
        if idx < 18:
            split_target = "train"
        elif idx < 22:
            split_target = "validation"
        else:
            split_target = "test"
            
        s_id, s_name, org, c_name, pitch, pushback = arch
        for lang in languages:
            cid = f"KAV-SYNTH2-{conv_id_counter:04d}"
            conv_id_counter += 1
            turns = build_dialogue_turns("AMBIGUOUS", arch, lang, idx)
            record = {
                "conversation_id": cid,
                "language": lang,
                "primary_label": "AMBIGUOUS",
                "scenario": f"{s_name} ({lang.upper()})",
                "scenario_family": s_name,
                "archetype_id": s_id,
                "split": split_target,
                "dialogue": turns,
                "scam_tactics": ["SUSPICIOUS_UNSOLICITED_CALL"],
                "risk_indicators": ["UNVERIFIED_CALLER"],
                "explanation": f"Ambiguous cold-contact scenario regarding {pitch}. Caller exhibits uncertain credibility ({pushback}).",
                "synthetic_source": "KAVACH Domain-Curated Multilingual Scenario Engine v2.0",
                "generation_model": "domain_curated_template_engine_v2",
                "review_status": "pending_review",
                "dataset_version": "v2.0_remediated_500"
            }
            conversations.append(record)
            splits[split_target].append(record)
            
    return conversations, splits

def run_build():
    print("=" * 70)
    print("KAVACH AI — Master Dataset Generator v2.0 (500 Conversations)")
    print("=" * 70)
    
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    SPLITS_DIR.mkdir(parents=True, exist_ok=True)
    
    conversations, splits = generate_all_500()
    print(f"Generated total {len(conversations)} conversations.")
    
    # Audit uniqueness of full dialogue strings
    dialogue_hashes = set()
    duplicate_count = 0
    for c in conversations:
        d_text = "\n".join([f"{t['speaker']}: {t['text']}" for t in c["dialogue"]]).strip().lower()
        h = hashlib.sha256(d_text.encode("utf-8")).hexdigest()
        if h in dialogue_hashes:
            duplicate_count += 1
        dialogue_hashes.add(h)
        
    print(f"Unique dialogue texts: {len(dialogue_hashes)} / {len(conversations)} (Duplicates: {duplicate_count})")
    assert duplicate_count == 0, f"Found {duplicate_count} duplicate dialogues!"
    
    # Check split leakage
    train_cids = set(c["conversation_id"] for c in splits["train"])
    val_cids = set(c["conversation_id"] for c in splits["validation"])
    test_cids = set(c["conversation_id"] for c in splits["test"])
    
    train_dialogues = set("\n".join([f"{t['speaker']}: {t['text']}" for t in c["dialogue"]]).strip().lower() for c in splits["train"])
    val_dialogues = set("\n".join([f"{t['speaker']}: {t['text']}" for t in c["dialogue"]]).strip().lower() for c in splits["validation"])
    test_dialogues = set("\n".join([f"{t['speaker']}: {t['text']}" for t in c["dialogue"]]).strip().lower() for c in splits["test"])
    
    train_val_overlap = train_dialogues.intersection(val_dialogues)
    train_test_overlap = train_dialogues.intersection(test_dialogues)
    val_test_overlap = val_dialogues.intersection(test_dialogues)
    
    print(f"Split sizes: Train={len(splits['train'])}, Val={len(splits['validation'])}, Test={len(splits['test'])}")
    print(f"Dialogue leakage: Train-Val={len(train_val_overlap)}, Train-Test={len(train_test_overlap)}, Val-Test={len(val_test_overlap)}")
    assert len(train_val_overlap) == 0 and len(train_test_overlap) == 0 and len(val_test_overlap) == 0, "Found cross-split dialogue leakage!"
    
    # Check scenario isolation
    train_scenarios = set(c["scenario_family"] for c in splits["train"])
    val_scenarios = set(c["scenario_family"] for c in splits["validation"])
    test_scenarios = set(c["scenario_family"] for c in splits["test"])
    print(f"Scenario family leakage: Train-Val={len(train_scenarios.intersection(val_scenarios))}, Train-Test={len(train_scenarios.intersection(test_scenarios))}, Val-Test={len(val_scenarios.intersection(test_scenarios))}")
    assert len(train_scenarios.intersection(val_scenarios)) == 0
    assert len(train_scenarios.intersection(test_scenarios)) == 0
    assert len(val_scenarios.intersection(test_scenarios)) == 0
    
    # 1. Write metadata/conversations.jsonl
    conv_file = METADATA_DIR / "conversations.jsonl"
    with open(conv_file, "w", encoding="utf-8") as f:
        for c in conversations:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Wrote master metadata to: {conv_file}")
    
    # 2. Write metadata/dataset_stats.json
    stats = {
        "dataset_name": "KAVACH-AI Multilingual Synthetic Dataset v2.0 (Remediated)",
        "total_conversations": len(conversations),
        "total_audio_files": 20,
        "class_distribution": dict(Counter(c["primary_label"] for c in conversations)),
        "language_distribution": dict(Counter(c["language"] for c in conversations)),
        "splits": {
            "train": len(splits["train"]),
            "validation": len(splits["validation"]),
            "test": len(splits["test"])
        },
        "review_status_distribution": dict(Counter(c["review_status"] for c in conversations)),
        "generation_provenance": "KAVACH Domain-Curated Multilingual Scenario Engine v2.0",
        "diversity_metrics": {
            "turn_length_distribution": dict(Counter(len(c["dialogue"]) for c in conversations)),
            "scenario_families_count": 100
        }
    }
    with open(METADATA_DIR / "dataset_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"Wrote dataset stats to: {METADATA_DIR / 'dataset_stats.json'}")
    
    # 3. Write individual transcripts
    for c in conversations:
        cid = c["conversation_id"]
        t_file = TRANSCRIPTS_DIR / f"{cid}.txt"
        text = f"Conversation ID: {cid}\nLanguage: {c['language']}\n"
        text += f"Scenario: {c['scenario']}\nLabel: {c['primary_label']}\nTactics: {', '.join(c['scam_tactics'])}\n\n"
        for t in c["dialogue"]:
            text += f"[{t['speaker'].upper()}]: {t['text']}\n"
            
        with open(t_file, "w", encoding="utf-8") as f:
            f.write(text)
    print(f"Wrote 500 individual transcripts to {TRANSCRIPTS_DIR}")
    
    # 4. Write split files
    for s_name in ["train", "validation", "test"]:
        s_file = SPLITS_DIR / f"{s_name}.jsonl"
        with open(s_file, "w", encoding="utf-8") as f:
            for item in splits[s_name]:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"Wrote {s_file.name}: {len(splits[s_name])} records")
        
    # Also write validation_report.json
    val_report = {
        "dataset_name": "KAVACH-AI Multilingual Synthetic Dataset v2.0 (Remediated)",
        "timestamp": "2026-11-05T09:40:00Z",
        "total_conversations": len(conversations),
        "unique_dialogue_texts": len(dialogue_hashes),
        "review_status": "pending_review",
        "provenance": "KAVACH Domain-Curated Multilingual Scenario Engine v2.0",
        "class_distribution": dict(Counter(c["primary_label"] for c in conversations)),
        "language_distribution": dict(Counter(c["language"] for c in conversations)),
        "splits": {
            "train": len(splits["train"]),
            "validation": len(splits["validation"]),
            "test": len(splits["test"])
        },
        "leakage_audit": {
            "train_val_duplicate_dialogues": len(train_val_overlap),
            "train_test_duplicate_dialogues": len(train_test_overlap),
            "val_test_duplicate_dialogues": len(val_test_overlap),
            "train_val_scenario_overlap": len(train_scenarios.intersection(val_scenarios)),
            "train_test_scenario_overlap": len(train_scenarios.intersection(test_scenarios)),
            "val_test_scenario_overlap": len(val_scenarios.intersection(test_scenarios))
        },
        "status": "PASS"
    }
    with open(METADATA_DIR / "validation_report.json", "w", encoding="utf-8") as f:
        json.dump(val_report, f, indent=2, ensure_ascii=False)
    print(f"Wrote validation report: {METADATA_DIR / 'validation_report.json'}")

if __name__ == "__main__":
    run_build()
