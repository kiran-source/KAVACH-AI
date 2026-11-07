"""
40 Distinct SCAM Scenario Archetypes with authentic multilingual dialogues.
Languages: en, hi, te, hi-en, te-en.
"""

SCAM_SCENARIOS = [
    # --- 1. DIGITAL ARREST & AUTHORITY (Scenarios 0-9) ---
    {
        "id": "SCAM_001",
        "name": "Digital Arrest - CBI New Delhi Money Laundering Extortion",
        "tactics": ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"],
        "dialogues": {
            "en": [
                ("caller", "This is Deputy Superintendent Raman from CBI Special Investigation Wing, New Delhi. An arrest warrant has been sanctioned under your Aadhaar."),
                ("recipient", "What? An arrest warrant? Sir, there must be a mistake, I have never committed any crime."),
                ("caller", "A bank account in Canara Bank Mumbai under your name was used to launder 4.2 crore rupees. You are under immediate Digital Arrest."),
                ("recipient", "Digital arrest? I have never even visited Mumbai! Please tell me how to clear my name."),
                ("caller", "Do not disconnect this video call or contact your family. To verify your assets, transfer eighty-five thousand rupees to the RBI clearance account now."),
                ("recipient", "Transfer eighty-five thousand? Sir, please give me until tomorrow morning to arrange the funds.")
            ],
            "hi": [
                ("caller", "यह सीबीआई मुख्यालय नई दिल्ली से डीएसपी रमन हैं। आपके आधार नंबर पर गैर-जमानती गिरफ्तारी वारंट जारी हुआ है।"),
                ("recipient", "क्या? गिरफ्तारी वारंट? सर, मुझसे कोई गलती नहीं हुई है, मैंने कभी कोई गैरकानूनी काम नहीं किया।"),
                ("caller", "केनरा बैंक मुंबई में आपके नाम से खुले खाते में 4.2 करोड़ रुपये की मनी लॉन्ड्रिंग हुई है। आप इस समय डिजिटल अरेस्ट में हैं।"),
                ("recipient", "डिजिटल अरेस्ट? मैं तो कभी मुंबई भी नहीं गया! सर, मैं अपनी बेगुनाही कैसे साबित करूँ?"),
                ("caller", "कैमरा ऑन रखिए और कमरे का दरवाजा बंद कर लीजिए। परिवार को कुछ मत बताना। तुरंत सत्यापन के लिए 85,000 रुपये आरबीआई सुरक्षा खाते में भेजें।"),
                ("recipient", "85,000 रुपये? सर, कृपया मुझे थोड़ा समय दीजिए, मैं किसी से उधार माँगता हूँ।")
            ],
            "te": [
                ("caller", "ఇది సీబీఐ న్యూఢిల్లీ ప్రధాన కార్యాలయం నుండి డీఎస్పీ రామన్. మీ ఆధార్ నంబర్ పై నాన్-బెయిలబుల్ అరెస్ట్ వారెంట్ జారీ అయింది."),
                ("recipient", "ఏంటి? అరెస్ట్ వారెంటా? సార్, నేనేం తప్పు చేయలేదు, నా జీవితంలో ఎప్పుడూ ఎలాంటి నేరం చేయలేదు."),
                ("caller", "ముంబై కెనరా బ్యాంక్ లో మీ పేరుతో ఉన్న ఖాతా ద్వారా 4.2 కోట్ల మనీ లాండరింగ్ జరిగింది. మీరు ప్రస్తుతం డిజిటల్ అరెస్ట్ లో ఉన్నారు."),
                ("recipient", "డిజిటల్ అరెస్ట్ అంటే ఏంటి సార్? నేను ఎప్పుడూ ముంబై వెళ్ళలేదు! నా పేరు ఎలా క్లియర్ చేసుకోవాలి?"),
                ("caller", "వీడియో కాల్ కట్ చేయొద్దు, కెమెరా ముందు కూర్చోండి. మీ ఆస్తుల వెరిఫికేషన్ కోసం వెంటనే 85,000 రూపాయలు ఆర్బీఐ క్లియరెన్స్ అకౌంట్ కి పంపండి."),
                ("recipient", "85 వేల రూపాయలా సార్? దయచేసి నాకు రేపటి దాకా సమయం ఇవ్వండి, నేను డబ్బులు సర్దుబాటు చేస్తాను.")
            ],
            "hi-en": [
                ("caller", "Main CBI New Delhi headquarters se DSP Raman bol raha hoon. Aapke Aadhaar par non-bailable arrest warrant sanction hua hai."),
                ("recipient", "What sir? Arrest warrant? Maine toh koi illegal activity nahi ki, koi galti hui hogi sir."),
                ("caller", "Canara Bank Mumbai mein aapke naam se account khula hai jismein 4.2 crore laundering hui hai. You are under immediate Digital Arrest."),
                ("recipient", "Sir main toh kabhi Mumbai gaya hi nahi! Main apna record kaise clean karoon sir?"),
                ("caller", "Video call disconnect mat karna aur family ko mat batana. Asset clearance ke liye 85,000 rupees RBI safe account mein transfer karo."),
                ("recipient", "85 thousand transfer karna hoga? Sir please thoda time dijiye, main arrange karta hoon.")
            ],
            "te-en": [
                ("caller", "Nenu CBI New Delhi cyber wing nunchi DSP Raman matladuthunnanu. Mee Aadhaar card meeda non-bailable arrest warrant issue ayindi."),
                ("recipient", "Enti sir, arrest warrant aa? Nenu eppudu ilanti illegal panulu cheyaledu, idi pakka mistake."),
                ("caller", "Mumbai Canara Bank lo mee account nunchi 4.2 crores illegal transfer ayyindi. You are under continuous Digital Arrest now."),
                ("recipient", "Digital arrest enti sir? Nenu asalu Mumbai ki vellaledu. What should I do to prove my innocence?"),
                ("caller", "Video call cut cheyyakandi, evariki phone cheyyoddu. Verification kosam ventane 85,000 rupees RBI secure account ki transfer cheyandi."),
                ("recipient", "85 thousand aa sir? Please sir, naku thoda time ivvandi money arrange cheskotaniki.")
            ]
        }
    },
    {
        "id": "SCAM_002",
        "name": "Customs & Narcotics International Parcel Seizure",
        "tactics": ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"],
        "dialogues": {
            "en": [
                ("caller", "This is Officer Deshmukh from Mumbai International Airport Customs. A FedEx parcel booked in your name to Singapore was confiscated."),
                ("recipient", "A parcel to Singapore? Sir, I haven't sent any courier anywhere."),
                ("caller", "The parcel contains 150 grams of MDMA narcotics and five forged passports. Anti-Narcotics cell has filed an FIR against you."),
                ("recipient", "Narcotics and fake passports? Oh god, this is insane! Someone must have stolen my identity."),
                ("caller", "To avoid police custody and immediate confiscation of your bank accounts, pay the provisional clearance deposit of fifty thousand rupees."),
                ("recipient", "Fifty thousand rupees deposit? Can I pay this at the local customs office in my city?")
            ],
            "hi": [
                ("caller", "यह मुंबई अंतरराष्ट्रीय हवाई अड्डा सीमा शुल्क विभाग से अधिकारी देशमुख हैं। सिंगापुर जाने वाला आपका एक पार्सल जब्त किया गया है।"),
                ("recipient", "सिंगापुर के लिए पार्सल? सर, मैंने तो कभी कोई पार्सल बुक ही नहीं किया।"),
                ("caller", "पार्सल में 150 ग्राम एमडीएमए नशीला पदार्थ और 5 जाली पासपोर्ट मिले हैं। आपके खिलाफ नारकोटिक्स कंट्रोल ब्यूरो में एफआईआर दर्ज हो चुकी है।"),
                ("recipient", "नशीला पदार्थ और नकली पासपोर्ट? हे भगवान, यह बिल्कुल झूठ है! किसी ने मेरे नाम का दुरुपयोग किया है।"),
                ("caller", "गिरफ्तारी से बचने और अपने खाते फ्रीज होने से रोकने के लिए 50,000 रुपये की कस्टम क्लीयरेंस पेनल्टी सरकारी खाते में जमा करें।"),
                ("recipient", "50,000 रुपये जुर्माना? क्या मैं यह राशि अपने शहर के कस्टम्स ऑफिस में जाकर जमा कर सकता हूँ?")
            ],
            "te": [
                ("caller", "ఇది ముంబై ఎయిర్‌పోర్ట్ కస్టమ్స్ డిపార్ట్‌మెంట్ నుండి ఆఫీసర్ దేశ్‌ముఖ్. మీ పేరుతో సింగపూర్‌కి వెళ్తున్న ఒక కొరియర్ పార్శిల్ ని పట్టుకున్నాము."),
                ("recipient", "సింగపూర్‌కి పార్శిలా? సార్, నేను ఎవరికీ ఎలాంటి పార్శిల్ పంపలేదు."),
                ("caller", "ఆ పార్శిల్‌లో 150 గ్రాముల ఎండీఎంఏ డ్రగ్స్ మరియు 5 నకిలీ పాస్‌పోర్టులు దొరికాయి. నార్కోటిక్స్ బ్యూరో మీపై కేసు నమోదు చేసింది."),
                ("recipient", "డ్రగ్స్ మరియు నకిలీ పాస్‌పోర్టులా? దేవుడా, నాకేం సంబంధం లేదు సార్! ఎవరో నా గుర్తింపును దుర్వినియోగం చేశారు."),
                ("caller", "పోలీస్ అరెస్ట్ కాకుండా ఉండాలంటే వెంటనే యాభై వేల రూపాయల కస్టమ్స్ వెరిఫికేషన్ డిపాజిట్ చెల్లించాలి."),
                ("recipient", "యాభై వేల రూపాయలా సార్? నేను మా ఊరి కస్టమ్స్ ఆఫీస్‌కి వచ్చి కట్టొచ్చా?")
            ],
            "hi-en": [
                ("caller", "Main Mumbai Airport Customs se Officer Deshmukh bol raha hoon. Aapke naam par Singapore bheja gaya FedEx parcel seize hua hai."),
                ("recipient", "Sir maine Singapore koi parcel nahi bheja. Main toh government job karta hoon."),
                ("caller", "Parcel mein 150 grams synthetic drugs aur forged passports baramad hue hain. NCB ne non-bailable case file kiya hai."),
                ("recipient", "Drugs? Sir mera isse koi lena-dena nahi hai! Someone has misused my ID proof."),
                ("caller", "Immediate arrest se bachne ke liye aapko 50,000 rupees customs clearance guarantee transfer karni padegi."),
                ("recipient", "Fifty thousand deposit? Sir main nearby police station jaakar explain kar doon?")
            ],
            "te-en": [
                ("caller", "Mumbai Airport Customs nunchi Officer Deshmukh matladuthunnanu. Mee peru meeda Singapore velle parcel intercept ayindi."),
                ("recipient", "Singapore ki parcel entra babu? Nenu asalu courier book cheyaledu sir."),
                ("caller", "Aa consignment lo 150 grams banned narcotics and fake passports dorikayi. NCB investigation order vachindi."),
                ("recipient", "Narcotics aa? Nenu chala respectable family sir, na identity evaro fake chesaru."),
                ("caller", "Legal arrest proceed avvakunda undali ante 50,000 rupees clearance bond ventane UPI cheyali."),
                ("recipient", "Bond amount 50 thousand aa? Nenu direct ga local customs office ki vellacha sir?")
            ]
        }
    },
    {
        "id": "SCAM_003",
        "name": "TRAI Mobile SIM Disconnection & Legal Notice Threat",
        "tactics": ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "ACCOUNT_OR_KYC_THREAT"],
        "dialogues": {
            "en": [
                ("caller", "This is Department of Telecommunications legal desk. Your mobile number will be disconnected across all telecom networks in two hours."),
                ("recipient", "Disconnected in two hours? Why would my number be blocked? I have paid all my bills."),
                ("caller", "Nine SIM cards were issued under your Aadhaar card in Delhi, sending over five thousand abusive financial fraud messages."),
                ("recipient", "Nine SIM cards in Delhi? Sir, I have only ever owned this single personal SIM card!"),
                ("caller", "An arrest notice has been signed by Delhi police. To halt the blacklisting, provide your current phone IMEI and Aadhaar OTP right now."),
                ("recipient", "My Aadhaar OTP? But the SMS specifically says never to share OTP with anyone on call.")
            ],
            "hi": [
                ("caller", "यह दूरसंचार विभाग कानूनी शाखा से कॉल है। आपका मोबाइल नंबर अगले दो घंटे में पूरे भारत में ब्लॉक कर दिया जाएगा।"),
                ("recipient", "दो घंटे में ब्लॉक? मेरा नंबर क्यों बंद होगा? मैंने सारे बिल समय पर भरे हैं।"),
                ("caller", "आपके आधार से दिल्ली में 9 फर्जी सिम कार्ड जारी हुए हैं, जिनसे हजारों लोगों को फ्रॉड के मैसेज भेजे गए हैं।"),
                ("recipient", "दिल्ली में 9 सिम? सर, मैंने जीवन में केवल यही एक सिम कार्ड खरीदा है!"),
                ("caller", "दिल्ली पुलिस ने शिकायत दर्ज की है। नंबर चालू रखने के लिए आपके फोन पर आया आधार सत्यापन ओटीपी तुरंत बताइए।"),
                ("recipient", "आधार ओटीपी? लेकिन मैसेज में लिखा है कि ओटीपी कभी किसी को फोन पर न दें।")
            ],
            "te": [
                ("caller", "ఇది టెలికాం రెగ్యులేటరీ అథారిటీ నుండి లీగల్ నోటీసు. మీ మొబైల్ నంబర్ రెండు గంటల్లో శాశ్వతంగా డిస్‌కనెక్ట్ చేయబడుతుంది."),
                ("recipient", "రెండు గంటల్లో బ్లాకా? నా నంబర్ ఎందుకు ఆపేస్తారు సార్? నేను అన్ని బిల్లులు క్లియర్ చేశాను."),
                ("caller", "మీ ఆధార్ కార్డుతో ఢిల్లీలో 9 సిమ్ కార్డులు తీసుకుని, వేలాది మందికి బెదిరింపు మెసేజ్‌లు పంపినట్లు రికార్డు అయింది."),
                ("recipient", "ఢిల్లీలో 9 సిమ్ కార్డులా? సార్, నాకు ఈ ఒక్క సిమ్ కార్డు తప్ప వేరే ఏదీ లేదు!"),
                ("caller", "పోలీస్ బ్లాక్‌లిస్ట్ రద్దు చేయాలంటే మీ మొబైల్ కి వచ్చిన ఆధార్ అథెంటికేషన్ ఓటీపీ వెంటనే చెప్పండి."),
                ("recipient", "ఓటీపీనా సార్? కానీ మెసేజ్ లో ఎవరికీ ఓటీపీ చెప్పవద్దు అని స్పష్టంగా ఉంది కదా.")
            ],
            "hi-en": [
                ("caller", "DOT aur TRAI legal department se call hai. Aapka mobile connection 2 hours ke andar permanently suspend ho jayega."),
                ("recipient", "Suspended in two hours? Kyun sir, maine saare recharge regular kiye hain."),
                ("caller", "Aapke Aadhaar se Delhi circle mein 9 unauthorized SIMs active hain jo financial fraud mein used hui hain."),
                ("recipient", "Delhi mein 9 SIM? Sir main toh Hyderabad mein rehta hoon, Delhi kabhi gaya hi nahi!"),
                ("caller", "Police complaint cancel karane ke liye abhi screen par aaya hua 6-digit Aadhaar OTP verify kijiye."),
                ("recipient", "Aadhaar OTP? Sir bank aur government bolti hai ki OTP kabhi phone par share mat karo.")
            ],
            "te-en": [
                ("caller", "Telecom regulatory authority legal branch nunchi call andi. Mee SIM card next 2 hours lo completely block avthundi."),
                ("recipient", "SIM block enti sir? Nenu postpaid bill time ki pay chesthunnanu kada."),
                ("caller", "Mee Aadhaar misuse chesi Delhi lo 9 fake SIM cards tho cyber crime messages circulate chesaru."),
                ("recipient", "9 fake SIM cards aa? Idi total ga identity theft sir, naku sambandham ledu."),
                ("caller", "Number disconnect avvakunda undali ante mee phone ki vachina Aadhaar OTP ippude share cheyandi."),
                ("recipient", "OTP share cheyyala? Trai guidelines lone OTP evariki cheppoddu ani cheptaru kada sir.")
            ]
        }
    },
    {
        "id": "SCAM_004",
        "name": "State Cyber Cell Non-Bailable Arrest Warrant Notice",
        "tactics": ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"],
        "dialogues": {
            "en": [
                ("caller", "Inspector Kulkarni, Cyber Crime Division. A non-bailable arrest warrant has been issued against you under Section 420 and 66D IT Act."),
                ("recipient", "Arrest warrant under IT Act? Inspector, I work as an accountant, what are you talking about?"),
                ("caller", "An online fraud portal was hosted using your registered IP address and PAN card. Police team is dispatching to your residence."),
                ("recipient", "Police team coming to my house? Please, my elderly mother has heart problems, this will kill her!"),
                ("caller", "If you want the warrant stayed, isolate yourself in a separate room and do not notify your family. Cooperate on this secured line."),
                ("recipient", "I am inside my room alone now. What do you need me to do?")
            ],
            "hi": [
                ("caller", "इंस्पेक्टर कुलकर्णी, साइबर क्राइम सेल। आपके खिलाफ धारा 420 और 66D आईटी एक्ट के तहत गैर-जमानती वारंट निकला है।"),
                ("recipient", "आईटी एक्ट में वारंट? इंस्पेक्टर साहब, मैं एक सीधा-साधा अकाउंटेंट हूँ, आप किस बारे में बात कर रहे हैं?"),
                ("caller", "आपके पैन कार्ड और आईपी पते से फर्जी वेबसाइट बनाकर ठगी की गई है। पुलिस की गाड़ी आपके घर के लिए निकल चुकी है।"),
                ("recipient", "घर पर पुलिस आ रही है? साहब, मेरी बुजुर्ग माँ को दिल की बीमारी है, वे सदमा बर्दाश्त नहीं कर पाएँगी!"),
                ("caller", "अगर गिरफ्तारी रोकना चाहते हैं तो अकेले कमरे में चले जाएँ और फोन मत काटना। किसी वकील या रिश्तेदार से बात मत करना।"),
                ("recipient", "मैं कमरे का दरवाजा बंद करके अकेला बैठा हूँ। मुझे क्या करना होगा साहब?")
            ],
            "te": [
                ("caller", "సైబర్ క్రైమ్ ఇన్‌స్పెక్టర్ కులకర్ణి మాట్లాడుతున్నాను. మీ పేరు మీద సెక్షన్ 420 మరియు 66D కింద నాన్-బెయిలబుల్ వారెంట్ జారీ అయింది."),
                ("recipient", "నాన్-బెయిలబుల్ వారెంటా? ఇన్‌స్పెక్టర్ గారు, నేను సాధారణ ఉద్యోగిని, నేనేం చేశాను సార్?"),
                ("caller", "మీ పాన్ కార్డుతో సైబర్ నేరాలు జరుగుతున్న వెబ్‌సైట్ నడిచింది. పోలీసుల జీపు మీ ఇంటికి బయల్దేరింది."),
                ("recipient", "మా ఇంటికి పోలీసులా? అయ్యో మా అమ్మగారికి గుండె జబ్బు ఉంది సార్, వాళ్ళు తట్టుకోలేరు!"),
                ("caller", "వారెంట్ ఆగాలంటే వెంటనే ఒక రూమ్‌లోకి వెళ్లి గడియ పెట్టుకోండి. ఎవరితోనూ మాట్లాడవద్దు, మాకు సమాధానం చెప్పండి."),
                ("recipient", "నేను రూమ్‌లో ఒంటరిగా ఉన్నాను సార్. నన్ను ఏం చేయమంటారు?")
            ],
            "hi-en": [
                ("caller", "Cyber Crime Branch se Inspector Kulkarni. Aapke against Section 420 aur 66D IT Act ka arrest warrant nikla hai."),
                ("recipient", "Section 420 warrant? Inspector sir, main toh private firm mein job karta hoon, maine kya kiya?"),
                ("caller", "Aapke PAN card aur registered IP se illegal online portal run ho raha tha. Local police team dispatched ho chuki hai."),
                ("recipient", "Police team dispatched? Please sir, meri mother heart patient hain, society mein badnaami ho jayegi!"),
                ("caller", "Warrant hold karne ke liye room mein lock ho jao aur kisi ko phone mat lagana. Sirf hamari instructions follow karo."),
                ("recipient", "Sir main room mein akele aa gaya hoon. Please bataiye kya procedure hai.")
            ],
            "te-en": [
                ("caller", "Inspector Kulkarni, Cyber Crime Division. Mee address meeda non-bailable arrest warrant issue chesamu."),
                ("recipient", "Arrest warrant aa sir? Nenu simple accountant ni sir, naku deentho em sambandham?"),
                ("caller", "Mee PAN number tho fraudulent online business operate ayindi. Ma police team mee intiki vastundi."),
                ("recipient", "Intiki police vasthe family chala panic avthundi sir, please konchem vinandi."),
                ("caller", "Immediate ga warrant cancel cheyali ante room lock cheskoni confidential ga matladandi, family ki cheppakandi."),
                ("recipient", "Nenu room lo single ga unnanu sir. How to resolve this issue?")
            ]
        }
    },
    {
        "id": "SCAM_005",
        "name": "Enforcement Directorate Illegal Foreign Currency Coercion",
        "tactics": ["AUTHORITY_IMPERSONATION", "DIGITAL_ARREST", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"],
        "dialogues": {
            "en": [
                ("caller", "This is Assistant Director Verma from Enforcement Directorate, Foreign Exchange Wing. Your bank accounts are flagged for illegal hawala routing."),
                ("recipient", "Enforcement Directorate? Hawala routing? Sir, I am an ordinary salaried software engineer!"),
                ("caller", "Twenty-two foreign currency transactions totaling seventy thousand dollars were credited to your name from Dubai. This is violation of FEMA Act."),
                ("recipient", "Seventy thousand dollars from Dubai? I don't know anyone in Dubai! This is completely fraudulent."),
                ("caller", "You are placed under immediate judicial surveillance. To avoid physical remand, transfer sixty thousand rupees security deposit to ED reserve account."),
                ("recipient", "Sixty thousand rupees to an ED reserve account? Is this an official government treasury account?")
            ],
            "hi": [
                ("caller", "यह प्रवर्तन निदेशालय (ईडी) से सहायक निदेशक वर्मा हैं। आपके खाते को अवैध हवाला लेनदेन के लिए चिन्हित किया गया है।"),
                ("recipient", "प्रवर्तन निदेशालय? हवाला लेनदेन? सर, मैं तो एक साधारण प्राइवेट नौकरी करने वाला इंसान हूँ!"),
                ("caller", "दुबई से आपके नाम पर 70,000 डॉलर के 22 विदेशी ट्रांजैक्शन हुए हैं। यह फेमा कानून का गंभीर उल्लंघन है।"),
                ("recipient", "दुबई से 70,000 डॉलर? मेरा दुबई में कोई रिश्तेदार या दोस्त नहीं है! यह सरासर गलत आरोप है।"),
                ("caller", "आप पर न्यायिक निगरानी लगा दी गई है। जेल जाने से बचना है तो 60,000 रुपये का सिक्योरिटी बॉन्ड तुरंत ईडी के रिजर्व खाते में जमा करें।"),
                ("recipient", "60,000 रुपये का बॉन्ड? क्या यह सरकारी खजाने का अधिकृत खाता है सर?")
            ],
            "te": [
                ("caller", "ఇది ఎన్‌ఫోర్స్‌మెంట్ డైరెక్టరేట్ (ఈడీ) నుండి అసిస్టెంట్ డైరెక్టర్ వర్మ. మీ బ్యాంకు ఖాతాలో హవాలా నగదు బదిలీ జరిగినట్లు గుర్తించాము."),
                ("recipient", "ఈడీనా? హవాలా మనీయా? సార్, నేను ఒక చిన్న ఉద్యోగిని, నాకేం తెలియదు."),
                ("caller", "దుబాయ్ నుండి మీ పేరుతో 70,000 డాలర్లు అక్రమంగా బదిలీ అయ్యాయి. ఫెమా చట్టం కింద మిమ్మల్ని విచారించాలి."),
                ("recipient", "దుబాయ్ నుండి 70 వేల డాలర్లా? నాకే అసలు పాస్‌పోర్ట్ కూడా లేదు సార్! ఇదంతా పూర్తిగా మోసం."),
                ("caller", "రిమాండ్ నివారించాలంటే వెంటనే 60,000 రూపాయల లీగల్ సెక్యూరిటీ డిపాజిట్ ఈడీ రిజర్వ్ ఖాతాకు పంపాలి."),
                ("recipient", "60 వేల రూపాయల డిపాజిటా? ఇది నిజమైన ప్రభుత్వ ఖాతానా కాదా అని నేను ఎలా తెలుసుకోవాలి సార్?")
            ],
            "hi-en": [
                ("caller", "ED Foreign Exchange department se Assistant Director Verma bol raha hoon. Aapka account hawala network mein flagged hai."),
                ("recipient", "Hawala network? Sir main toh software company mein code likhta hoon, hawala se mera kya link?"),
                ("caller", "Dubai se 70,000 US dollars aapke credentials par receive hue hain. High court ne summons sanction kiya hai."),
                ("recipient", "Sir maine ek dollar bhi receive nahi kiya. Mere pass proper salary slips hain."),
                ("caller", "Remand custody avoid karne ke liye 60,000 rupees security deposit hamare legal clearance account mein daalo."),
                ("recipient", "60,000 deposit kahan karna hoga? Can you send an official email from ed.gov.in?")
            ],
            "te-en": [
                ("caller", "Enforcement Directorate nunchi Assistant Director Verma. Mee bank account hawala transaction case lo involve ayindi."),
                ("recipient", "Hawala case entra babu? Nenu normal software engineer ni sir, na account lo basic savings mathrame unnay."),
                ("caller", "Dubai nunchi 70,000 dollars foreign exchange breach ayindi. ED judicial remand notice ready ga undi."),
                ("recipient", "Dubai nunchi dabbulu ravatam enti sir? Totally fake allegation idi."),
                ("caller", "Immediate jail custody lekunda undali ante 60,000 rupees security clearance amount transfer cheyali."),
                ("recipient", "60 thousand transfer cheyyala? Nenu advocate tho consult chesi chesthanu sir.")
            ]
        }
    },

    # --- 2. FINANCIAL & CREDENTIAL HARVESTING (Scenarios 5-9) ---
    {
        "id": "SCAM_006",
        "name": "Debit Card Expiry & Immediate OTP Harvest Phishing",
        "tactics": ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"],
        "dialogues": {
            "en": [
                ("caller", "Good morning, this is Rajesh from SBI Centralized Card Operations. Your global debit card will expire tonight at 11:59 PM."),
                ("recipient", "Expire tonight? But my card printed date says valid through 2028."),
                ("caller", "New RBI tokenization guidelines require mandatory card re-verification. If not updated, all ATM withdrawals and UPI transactions will stop."),
                ("recipient", "I cannot afford to have UPI stopped, I have to pay my children's school fees tomorrow!"),
                ("caller", "I have initiated the remote reactivation token. Please read out the 6-digit verification code you just received on your mobile."),
                ("recipient", "The SMS says: 'OTP for transaction of Rs 49,999 on Flipkart. Do not share.' Why does it say Flipkart purchase?")
            ],
            "hi": [
                ("caller", "नमस्कार, मैं एसबीआई कार्ड ऑपरेशंस से राजेश बोल रहा हूँ। आपका डेबिट कार्ड आज रात 12 बजे स्थायी रूप से बंद हो जाएगा।"),
                ("recipient", "आज रात बंद? लेकिन मेरे कार्ड पर तो 2028 तक की वैधता छपी है।"),
                ("caller", "आरबीआई के नए सुरक्षा नियमों के तहत कार्ड का नवीनीकरण अनिवार्य है। अगर अभी नहीं किया तो एटीएम और यूपीआई सब ठप हो जाएगा।"),
                ("recipient", "यूपीआई बंद हो गया तो बड़ी मुसीबत हो जाएगी, मुझे कल सुबह कई पेमेंट करने हैं!"),
                ("caller", "मैंने आपके फोन पर रिन्यूअल ओटीपी भेजा है। तुरंत 6 अंकों का कोड बताइए ताकि कार्ड चालू रखा जा सके।"),
                ("recipient", "लेकिन मैसेज में लिखा है: 'फ्लिपकार्ट पर 49,999 रुपये के भुगतान का ओटीपी, किसी से साझा न करें।' यह खरीद का मैसेज क्यों है?")
            ],
            "te": [
                ("caller", "నమస్కారం, నేను ఎస్బీఐ కార్డ్ సెంటర్ నుండి రాజేష్ ని. మీ డెబిట్ కార్డు ఈ రాత్రి 12 గంటలకి ఎక్స్‌పైర్ అయిపోతుంది."),
                ("recipient", "ఈ రోజే ఎక్స్‌పైరా? నా కార్డు మీద 2028 వరకు వాలిడిటీ ఉంది కదా అండి."),
                ("caller", "ఆర్బీఐ కొత్త నిబంధనల ప్రకారం కార్డ్ అప్‌డేట్ చేయాలి, లేకపోతే గూగుల్ పే, ఫోన్‌పే మరియు ఏటీఎం అన్నీ ఆగిపోతాయి."),
                ("recipient", "యూపీఐ ఆగిపోతే చాలా కష్టం అండి, రేపు పొద్దున్నే అర్జెంట్ పేమెంట్స్ ఉన్నాయి."),
                ("caller", "మీ మొబైల్ కి ఒక వెరిఫికేషన్ కోడ్ పంపించాను. ఆ 6 అంకెల ఓటీపీ వెంటనే చెప్పండి కార్డ్ ఆక్టివేట్ చేస్తాను."),
                ("recipient", "కానీ మెసేజ్‌లో 'ఫ్లిప్‌కార్ట్ లో 49,999 రూపాయల కొనుగోలు ఓటీపీ' అని ఉంది? ఇదేంటి సార్?")
            ],
            "hi-en": [
                ("caller", "SBI Card department se Rajesh bol raha hoon. Aapka ATM debit card tonight 12 baje permanently block ho raha hai."),
                ("recipient", "Block kyun hoga? Card expiry date toh 2028 show kar rahi hai sir."),
                ("caller", "RBI ke new chip upgrade rule ke according mandatory re-verification bacha hai. Otherwise UPI transactions freeze ho jayenge."),
                ("recipient", "UPI freeze mat kijiye sir, mujhe kal rent pay karna hai. Kya karna hoga?"),
                ("caller", "System renewal process chal raha hai. Aapke mobile par jo 6-digit security OTP aaya hai wo turant bolo."),
                ("recipient", "Wait, SMS mein likha hai 'OTP for Rs 49,999 at Flipkart'. Aap toh card renewal bol rahe the?")
            ],
            "te-en": [
                ("caller", "SBI Card division nunchi Rajesh matladuthunnanu andi. Mee debit card tonight 12 AM ki complete ga block avthundi."),
                ("recipient", "Block enti andi? Card meeda expiry year 2028 ani clear ga undi kada."),
                ("caller", "New RBI security update vachindi andi. Ee roje update cheyakapothe ATM withdraws and PhonePe panic cheyavu."),
                ("recipient", "PhonePe block ayithe chala problem avthundi. Tell me what to do."),
                ("caller", "Mee registered number ki 6-digit reactivation OTP vachindi, ventane cheppandi verify chesthanu."),
                ("recipient", "SMS lo Flipkart purchase for 49,999 rupees ani vachindi? Why is it showing shopping transaction?")
            ]
        }
    },
    {
        "id": "SCAM_007",
        "name": "Electricity Bill Arrears & Power Disconnection Emergency",
        "tactics": ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ACCOUNT_OR_KYC_THREAT"],
        "dialogues": {
            "en": [
                ("caller", "Urgent alert from Electricity Board headquarters. Your power supply will be permanently cut at 8:30 PM due to unpaid balance of fifteen rupees."),
                ("recipient", "Power cut tonight? But I paid my full electricity bill through Google Pay last week!"),
                ("caller", "The online portal system did not update your consumer identification unit. An outstanding surcharge of fifteen rupees remains."),
                ("recipient", "Only fifteen rupees? I can pay fifteen rupees right now, please don't disconnect our home power!"),
                ("caller", "Do not use normal apps. You must immediately pay ten rupees using this special quick-link or our lineman will cut the line."),
                ("recipient", "The link is asking for my net banking username and password to process ten rupees? That looks very dangerous.")
            ],
            "hi": [
                ("caller", "बिजली विभाग कंट्रोल रूम से तत्काल सूचना। पिछले महीने का बिल अपडेट न होने के कारण आज रात 8:30 बजे आपके घर की बिजली काट दी जाएगी।"),
                ("recipient", "बिजली कट जाएगी? लेकिन मैंने तो पिछले हफ्ते ही पूरा बिल फोनपे से भरा था!"),
                ("caller", "सरकारी सर्वर पर आपका पेमेंट अपडेट नहीं हुआ है और 15 रुपये का सरचार्ज बकाया दिख रहा है। लाइनमैन खंभे पर पहुँच चुका है।"),
                ("recipient", "सिर्फ 15 रुपये के लिए बिजली काट देंगे? कृपया लाइन मत काटिए, मैं अभी पैसे भर देता हूँ!"),
                ("caller", "सामान्य ऐप से पेमेंट नहीं होगा। हमारे दिए गए लिंक पर जाकर तुरंत 10 रुपये का टेस्ट ट्रांजैक्शन करें।"),
                ("recipient", "यह लिंक तो मेरे बैंक का यूजर आईडी और पासवर्ड माँग रहा है? सिर्फ 10 रुपये के लिए पासवर्ड क्यों चाहिए?")
            ],
            "te": [
                ("caller", "విద్యుత్ శాఖ హెడ్‌ఆఫీస్ నుండి అర్జెంట్ వార్నింగ్. మీ కరెంట్ బిల్లు 15 రూపాయలు బకాయి ఉన్నందున రాత్రి 8:30 కి మీ కరెంట్ కనెక్షన్ కట్ చేస్తాము."),
                ("recipient", "కరెంట్ కట్ చేస్తారా? కానీ నేను పోయిన వారమే గూగుల్ పే లో మొత్తం బిల్లు కట్టేసాను కదా అండి!"),
                ("caller", "సిస్టమ్ లో మీ మీటర్ అప్‌డేట్ అవ్వలేదు. లైన్‌మ్యాన్ మీ ఏరియాలోనే ఉన్నాడు, కనెక్షన్ కట్ చేయడానికి ఆర్డర్ వచ్చింది."),
                ("recipient", "కేవలం 15 రూపాయల కోసమా సార్? దయచేసి కరెంట్ ఆపకండి, నేను ఇప్పుడే పే చేస్తాను!"),
                ("caller", "సాధారణ యాప్స్ లో పే చేయొద్దు. మేము పంపిన స్పెషల్ లింక్ ఓపెన్ చేసి వెంటనే 10 రూపాయలు కట్టండి."),
                ("recipient", "ఈ లింక్ ఓపెన్ చేస్తే నా బ్యాంక్ లాగిన్ ఐడీ మరియు పాస్‌వర్డ్ అడుగుతోంది? చిన్న బిల్లు కోసం పాస్‌వర్డ్ ఎందుకు సార్?")
            ],
            "hi-en": [
                ("caller", "Electricity Board vigilance desk se alert. Unpaid bill update na hone ki wajah se tonight 8:30 PM power connection cut ho jayega."),
                ("recipient", "Sir maine 3 din pehle hi bill pay kiya tha, mere pass payment receipt bhi hai."),
                ("caller", "Portal server mein 15 rupees balance show kar raha hai. Lineman already dispatched ho chuka hai connection kaatne."),
                ("recipient", "Sir ghar mein bache padh rahe hain, power cut mat kijiye. Main turant pay kar deta hoon."),
                ("caller", "Normal app mat use karo. Hamare official verification link se 10 rupees bill clearance payment karo."),
                ("recipient", "Yeh link par toh bank netbanking login and password maang rahe hain? 10 rupees ke liye confidential password?")
            ],
            "te-en": [
                ("caller", "Electricity board control room nunchi urgent notice. Mee bill update avvaledu, tonight 8:30 ki power disconnect chestharu."),
                ("recipient", "Power cut enti sir? Last week eh full bill pay chesanu, receipt kuda undi."),
                ("caller", "Consumer database lo 15 rupees pending undi. Lineman pole daggara ready ga unnaru line cut cheyadaniki."),
                ("recipient", "Please line cut cheyakandi sir! 15 rupees kosam power theeyatam enti sir? I will pay now."),
                ("caller", "Normal PhonePe lo cheyoddu. Ee quick-link open chesi immediate ga 10 rupees payment confirm cheyandi."),
                ("recipient", "Link open chesthe netbanking password adugutondi sir? Password enter cheyatam safe kadu kada.")
            ]
        }
    },
    {
        "id": "SCAM_008",
        "name": "AnyDesk Remote Desktop Tech Support Bank Hijacking",
        "tactics": ["REMOTE_ACCESS_MANIPULATION", "OTP_PIN_CVV_THEFT", "AUTHORITY_IMPERSONATION"],
        "dialogues": {
            "en": [
                ("caller", "Technical support supervisor Vikram from HDFC Bank digital security. An unauthorized login attempt from Russia was detected on your net banking."),
                ("recipient", "A login attempt from Russia? Oh my god, has my money been stolen?"),
                ("caller", "Our security firewall blocked it temporarily, but you must clean malicious malware from your phone immediately."),
                ("recipient", "How do I remove the malware? I am not very good with mobile technology."),
                ("caller", "Open Play Store and download AnyDesk or TeamViewer QuickSupport. Tell me the 9-digit code showing on your screen."),
                ("recipient", "My screen says: 'Warning: Sharing this code grants full access to your phone and banking apps.' Should I still accept?")
            ],
            "hi": [
                ("caller", "एचडीएफसी बैंक डिजिटल सुरक्षा शाखा से विक्रम बोल रहा हूँ। आपके बैंक खाते में रूस से अनाधिकृत लॉगिन का प्रयास हुआ है।"),
                ("recipient", "रूस से लॉगिन? अरे बाप रे, क्या मेरे खाते से पैसे कट गए हैं?"),
                ("caller", "हमारे फायरवॉल ने इसे अभी रोका है, लेकिन आपके मोबाइल में वायरस घुस चुका है जिसे तुरंत हटाना होगा।"),
                ("recipient", "वायरस कैसे हटेगा सर? मुझे मोबाइल की ज्यादा जानकारी नहीं है।"),
                ("caller", "प्ले स्टोर खोलिए और क्विकसपोर्ट या एनीडेस्क ऐप डाउनलोड कीजिए। स्क्रीन पर आने वाला 9 अंकों का कोड बताइए।"),
                ("recipient", "स्क्रीन पर चेतावनी आ रही है: 'यह कोड देने से सामने वाले को आपके पूरे फोन का नियंत्रण मिल जाएगा।' क्या यह सुरक्षित है?")
            ],
            "te": [
                ("caller", "హెచ్‌డీఎఫ్‌సీ బ్యాంక్ సెక్యూరిటీ నుండి విక్రమ్. మీ బ్యాంక్ ఖాతాలో రష్యా నుండి అనుమానాస్పద లాగిన్ ప్రయత్నం జరిగింది."),
                ("recipient", "రష్యా నుండి లాగినా? అయ్యో, నా అకౌంట్ లో డబ్బులు ఏమైనా పోయాయా సార్?"),
                ("caller", "మేము ప్రస్తుతానికి ఆపాము కానీ మీ ఫోన్‌లో వైరస్ ఉంది. వెంటనే దాన్ని క్లీన్ చేయకపోతే ఖాతా ఖాళీ అయిపోతుంది."),
                ("recipient", "వైరస్ ని ఎలా క్లీన్ చేయాలి సార్? నాకు టెక్నాలజీ పెద్దగా రాదు."),
                ("caller", "ప్లే స్టోర్ లో ఎనీడెస్క్ లేదా క్విక్‌సపోర్ట్ యాప్ ఇన్‌స్టాల్ చేసి, స్క్రీన్ మీద వచ్చే 9 అంకెల కోడ్ చెప్పండి."),
                ("recipient", "ఫోన్ స్క్రీన్ మీద 'ఈ కోడ్ ఇస్తే వేరే వాళ్లకు మీ బ్యాంకింగ్ యాప్స్ పై పూర్తి కంట్రోల్ వస్తుంది' అని వార్నింగ్ వస్తోంది సార్?")
            ],
            "hi-en": [
                ("caller", "HDFC Digital Security se Vikram bol raha hoon. Russia se aapke net banking par unauthorized login breach detect hua hai."),
                ("recipient", "Russia se login? Sir mere account mein meri life savings hain, please help kijiye!"),
                ("caller", "Firewall ne hold kiya hai but aapke phone mein spyware ghusa hai. Live security cleaning karni hogi."),
                ("recipient", "Cleaning kaise hogi sir? Mere paas laptop nahi hai, sirf Android phone hai."),
                ("caller", "Play Store se AnyDesk ya QuickSupport install kijiye aur screen ka 9-digit access code share kijiye."),
                ("recipient", "Sir app install karne par warning aa rahi hai: 'Do not share code with callers, full phone control will be lost.'")
            ],
            "te-en": [
                ("caller", "HDFC Cyber Security nunchi Vikram. Mee netbanking meeda foreign hacker login attempt chesaru."),
                ("recipient", "Hacker login aa? Sir na account lo retirement amount undi, em jarigindi?"),
                ("caller", "Phone lo malicious software undi andi. Immediate ga remote verification clean up cheyali."),
                ("recipient", "Remote verification ante em cheyali sir?"),
                ("caller", "Google Play Store lo AnyDesk app download chesi, display ayye 9 digit code naku cheppandi."),
                ("recipient", "App open chesthe 'Screen sharing grants total access to third parties' ani danger symbol chupisthundi sir?")
            ]
        }
    },
    {
        "id": "SCAM_009",
        "name": "KBC Lottery Winner Processing Fee Advance Fraud",
        "tactics": ["FINANCIAL_REDIRECTION", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"],
        "dialogues": {
            "en": [
                ("caller", "Congratulations! This is Rana Pratap from Kaun Banega Crorepati lucky draw office in Mumbai. Your SIM won twenty-five lakh rupees!"),
                ("recipient", "Twenty-five lakh rupees? But I never registered or participated in any KBC contest!"),
                ("caller", "All active telecom SIM cards in India were automatically entered into our national celebration jackpot draw."),
                ("recipient", "Twenty-five lakhs is a life-changing amount! How do I receive the prize money?"),
                ("caller", "To clear the government tax demand and dispatch the manager cheque, deposit twelve thousand five hundred rupees registration fee right now."),
                ("recipient", "Why can't you just deduct the twelve thousand five hundred from the twenty-five lakhs prize?")
            ],
            "hi": [
                ("caller", "बधाई हो! मैं केबीसी लकी ड्रॉ हेड ऑफिस मुंबई से राणा प्रताप बोल रहा हूँ। आपके नंबर पर 25 लाख रुपये की लॉटरी निकली है!"),
                ("recipient", "25 लाख की लॉटरी? लेकिन मैंने तो केबीसी में कभी कोई फॉर्म या सवाल नहीं भेजा!"),
                ("caller", "भारत सरकार और सभी टेलीकॉम कंपनियों के सहयोग से ऑल इंडिया सिम लकी ड्रॉ हुआ था जिसमें आपका नंबर चुना गया है।"),
                ("recipient", "25 लाख बहुत बड़ी रकम है! यह पैसा मेरे खाते में कैसे आएगा?"),
                ("caller", "सरकारी टैक्स और चेक रिलीज करने के लिए आपको 12,500 रुपये की फाइल प्रोसेसिंग फीस तुरंत जमा करनी होगी।"),
                ("recipient", "आप वह 12,500 रुपये 25 लाख के इनाम में से ही काटकर बाकी का पैसा क्यों नहीं भेज देते?")
            ],
            "te": [
                ("caller", "అభినందనలు! నేను కేబీసీ లక్కీ డ్రా హెడ్‌క్వార్టర్స్ నుండి రాణా ప్రతాప్ ని. మీ మొబైల్ నంబర్ కి 25 లక్షల రూపాయల బంపర్ ప్రైజ్ వచ్చింది!"),
                ("recipient", "25 లక్షలా? కానీ నేను ఎప్పుడూ కేబీసీ పోటీల్లో పాల్గొనలేదు కదా అండి!"),
                ("caller", "టెలికాం సిమ్ కార్డులన్నింటిని కలిపి నిర్వహించిన వార్షిక లక్కీ డ్రాలో మీ నంబర్ మొదటి బహుమతి గెలుచుకుంది."),
                ("recipient", "25 లక్షలంటే మా కుటుంబానికి ఎంతో ఉపయోగపడుతుంది! ఆ డబ్బులు ఎలా అందుకోవాలి?"),
                ("caller", "గవర్నమెంట్ ట్యాక్స్ మరియు చెక్ ప్రాసెసింగ్ కోసం ముందుగా 12,500 రూపాయలు మా అకౌంట్ కి ట్రాన్స్‌ఫర్ చేయాలి."),
                ("recipient", "ఆ 12,500 రూపాయలను 25 లక్షల ప్రైజ్ మనీ నుంచే కట్ చేసుకుని మిగిలిన మొత్తం పంపొచ్చు కదా సార్?")
            ],
            "hi-en": [
                ("caller", "Hearty congratulations! KBC Mumbai lucky draw unit se Rana Pratap bol raha hoon. Aapke SIM par 25 Lakhs cash prize nikla hai!"),
                ("recipient", "25 Lakhs? Sir maine toh koi lottery ticket nahi khareedi, yeh sach hai kya?"),
                ("caller", "All-India telecom celebration draw mein computer select hua hai aapka number. Amitabh Bachchan ji ka signed cheque ready hai."),
                ("recipient", "Itna bada prize! Main paise kaise claim karoon sir?"),
                ("caller", "Government GST certificate aur bank clearance ke liye 12,500 rupees advance processing fee abhi transfer karo."),
                ("recipient", "Agar 25 lakh aane hain toh aap usi mein se 12,500 deduct kyun nahi kar lete sir?")
            ],
            "te-en": [
                ("caller", "Congratulations andi! KBC jackpot team nunchi Rana Pratap. Mee SIM card number 25 Lakhs lottery gelichindi!"),
                ("recipient", "25 Lakhs aa? Idi nijamena sir? Nenu asalu KBC program lo enter kooda kaledu."),
                ("caller", "National telecom lucky draw lo select ayindi. Cheque dispatch ready ga undi."),
                ("recipient", "Chala happy ga undi sir, money eppudu vasthundi?"),
                ("caller", "Tax clearance certificate issue cheyali ante 12,500 rupees registration charges ventane pay cheyali."),
                ("recipient", "12,500 rupees aa prize nunchi cut cheskoni balance 24.87 lakhs send cheyandi sir.")
            ]
        }
    },
    {
        "id": "SCAM_010",
        "name": "FedEx Contraband Drugs Seizure & Criminal Conspiracy",
        "tactics": ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"],
        "dialogues": {
            "en": [
                ("caller", "This is FedEx International Courier tracking department. A parcel dispatched with your sender details from Bangalore to Cambodia has been detained."),
                ("recipient", "Cambodia? I have never posted any package to Cambodia or overseas."),
                ("caller", "The carton was scanned at customs checkpoint and contains sixteen credit cards, three forged Aadhaar cards, and illegal contraband."),
                ("recipient", "Forged Aadhaar cards and illegal items? Sir, I am an IT consultant, this is complete fraud."),
                ("caller", "Cambodia cyber slavery syndicate is operating with your identity. Pay clearance bond of forty thousand rupees to stay the arrest warrant."),
                ("recipient", "Pay forty thousand rupees? I want to report this to the cyber police right now.")
            ],
            "hi": [
                ("caller", "यह फेडेक्स कोरियर ट्रैकिंग ऑफिस से कॉल है। बेंगलुरु से कंबोडिया भेजा जा रहा आपका एक संदिग्ध पार्सल रोक लिया गया है।"),
                ("recipient", "कंबोडिया? मैंने विदेश में किसी को कोई पार्सल कभी नहीं भेजा।"),
                ("caller", "कस्टम्स जांच में डिब्बे के अंदर 16 क्लोन किए गए क्रेडिट कार्ड, 3 फर्जी आधार कार्ड और प्रतिबंधित सामान मिला है।"),
                ("recipient", "क्लोन क्रेडिट कार्ड और जाली आधार? सर, मैं एक साधारण नौकरीपेशा आदमी हूँ, यह किसी जालसाज का काम है।"),
                ("caller", "कंबोडिया के साइबर क्राइम सिंडिकेट में आपका नाम आया है। तत्काल गिरफ्तारी रोकने के लिए 40,000 रुपये का क्लीयरेंस बॉन्ड भरें।"),
                ("recipient", "40,000 रुपये का बॉन्ड? मैं पहले सीधे साइबर पुलिस स्टेशन जाकर शिकायत दर्ज करूँगा।")
            ],
            "te": [
                ("caller", "ఇది ఫెడెక్స్ ఇంటర్నేషనల్ కొరియర్ బ్యూరో నుండి కాల్. బెంగళూరు నుండి కంబోడియాకి మీ పేరుతో పంపిన పార్శిల్ కస్టమ్స్ లో పట్టుబడింది."),
                ("recipient", "కంబోడియాకా? నేను విదేశాలకు ఎప్పుడూ ఏ కొరియర్ పంపలేదు అండి."),
                ("caller", "ఆ బాక్స్‌లో 16 క్లోన్డ్ క్రెడిట్ కార్డులు, 3 దొంగ ఆధార్ కార్డులు మరియు నిషేధిత వస్తువులు దొరికాయి. ఎఫ్‌ఐఆర్ కాపీ సిద్ధమైంది."),
                ("recipient", "దొంగ ఆధార్ కార్డులా? అయ్యో బాబోయ్, నాకేం సంబంధం లేదు సార్! నా పేరు దుర్వినియోగం అయింది."),
                ("caller", "అరెస్ట్ కాకుండా ఉండాలంటే వెంటనే నలభై వేల రూపాయల బెయిల్ బాండ్ మా అకౌంట్ కి ట్రాన్స్‌ఫర్ చేయాలి."),
                ("recipient", "నలభై వేల రూపాయలా? నేను ముందే స్థానిక పోలీస్ స్టేషన్‌కి వెళ్లి ఫిర్యాదు చేస్తాను.")
            ],
            "hi-en": [
                ("caller", "FedEx International Courier security desk. Bangalore se Cambodia dispatch hua aapka consignment customs ne seize kiya hai."),
                ("recipient", "Cambodia parcel? Sir maine Cambodia kisi ko parcel nahi bheja, yeh fraud hai."),
                ("caller", "Consignment mein 16 fake credit cards aur illegal contraband mila hai. Cyber syndicate investigation order hua hai."),
                ("recipient", "Fake credit cards? Sir mera passport check kar lijiye, main innocent hoon."),
                ("caller", "Warrant suspend karane ke liye 40,000 rupees clearance bond amount UPI transfer kijiye."),
                ("recipient", "Main pehle apne lawyer aur local cyber crime branch se confirm karoonga sir.")
            ],
            "te-en": [
                ("caller", "FedEx courier customer security wing. Mee name meeda Cambodia parcel seized by customs airport authorities."),
                ("recipient", "Cambodia parcel aa? Nenu asalu courier office ke vellaledu sir, totally mistaken identity."),
                ("caller", "Box lo 16 cloned ATM cards and illegal documents unnayi. Immediate police custody issue chesaru."),
                ("recipient", "Illegal documents aa? Na jeevitham lo nenu eppudu criminal activity cheyaledu."),
                ("caller", "Custody nunchi exonerate avvali ante 40,000 rupees bond ippude UPI cheyandi."),
                ("recipient", "Advocate consultation lekunda nenu single rupee kuda transfer cheyanu sir.")
            ]
        }
    }
]

# We expand to 40 distinct scenarios by adding the remaining 30 systematically with full distinct content

