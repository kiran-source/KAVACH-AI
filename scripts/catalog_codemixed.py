# scripts/catalog_codemixed.py
import json

def get_telugu_english_conversations():
    items = []

    # KAV-SYNTH-061
    items.append({
        "conversation_id": "KAV-SYNTH-061",
        "language": "te-en",
        "primary_label": "SCAM",
        "scenario": "Fake IT MNC Job Offer Letter & Security Deposit Scam",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Vinay, I am calling from TCS Talent Acquisition team, Hyderabad campus."},
            {"speaker": "recipient", "text": "Hi madam! Is this regarding my application for Associate Software Engineer role?"},
            {"speaker": "caller", "text": "Yes Vinay, మీ profile shortlist అయింది. Direct technical package offers nine lakhs per annum."},
            {"speaker": "recipient", "text": "Nine lakhs! That is great! Interview schedule eppudu untundi madam?"},
            {"speaker": "caller", "text": "No formal interview needed. Direct corporate project assignment. But document verification fee and laptop security deposit ga twenty thousand pay cheyali."},
            {"speaker": "recipient", "text": "Deposit TCS company official portal lo pay cheyala madam?"},
            {"speaker": "caller", "text": "No, HR clearance team private UPI handle కి transfer cheyali before five PM today, లేదంటే offer cancel avtundi."},
            {"speaker": "recipient", "text": "MNC companies eppudu deposit adagavu. This is a clear job scam. I will not pay."}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["advance security deposit for job", "private upi transfer demand", "unrealistic direct salary offer without interview"],
        "explanation": "IT recruiter impersonation offering direct job appointment to extort advance laptop and documentation fees via private UPI.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/telugu_english/kav_synth_061.wav"
    })

    # KAV-SYNTH-062
    items.append({
        "conversation_id": "KAV-SYNTH-062",
        "language": "te-en",
        "primary_label": "SCAM",
        "scenario": "Aadhaar Card Linked SIM Misuse Digital Arrest",
        "dialogue": [
            {"speaker": "caller", "text": "This is Inspector Rajesh from Telecom Regulatory Authority and Delhi Police Crime Branch."},
            {"speaker": "recipient", "text": "Yes sir, cheppandi. Enti vishayam?"},
            {"speaker": "caller", "text": "Mee Aadhaar number tho link aina BSNL SIM card dwaara illegal financial extortion jarigindi."},
            {"speaker": "recipient", "text": "Sir, na daggara BSNL SIM eppudu ledu sir, someone must have forged my ID."},
            {"speaker": "caller", "text": "Already Non-Bailable Warrant issue aindi. Meeru immediately Skype video call lo join avvali under digital arrest."},
            {"speaker": "recipient", "text": "Digital arrest enti sir? Can I call my advocate?"},
            {"speaker": "caller", "text": "Advocate ki call cheste case national security kindaki veltundi. Ee call disconnect cheste squad mee intiki vastundi."},
            {"speaker": "recipient", "text": "Police phone lo digital arrest cheyaru. I know this is a scam, I am filing a complaint on 1930."}
        ],
        "scam_tactics": ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE", "URGENCY_OR_THREAT"],
        "risk_indicators": ["digital arrest demand", "prohibition on calling advocate", "threat of police squad dispatch"],
        "explanation": "Law enforcement impersonation claiming SIM card linkage to cybercrime to enforce digital arrest and compliance.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/telugu_english/kav_synth_062.wav"
    })

    # KAV-SYNTH-063
    items.append({
        "conversation_id": "KAV-SYNTH-063",
        "language": "te-en",
        "primary_label": "SCAM",
        "scenario": "Fake Credit Card Limit Enhancement OTP Theft",
        "dialogue": [
            {"speaker": "caller", "text": "Good morning sir, calling from HDFC Bank credit card operations department."},
            {"speaker": "recipient", "text": "Hello, yes tell me."},
            {"speaker": "caller", "text": "Sir, mee Regalia credit card limit two lakhs nundi five lakhs ki upgrade cheyadaniki approval vachindi."},
            {"speaker": "recipient", "text": "Any additional annual charges for limit increase?"},
            {"speaker": "caller", "text": "Zero annual charges sir, it is a lifetime free upgrade. Just card verification process complete cheyali."},
            {"speaker": "recipient", "text": "Okay, process enti?"},
            {"speaker": "caller", "text": "Mee registered mobile number ki six digit OTP send chesamu, limit upgrade kosam aa code cheppandi."},
            {"speaker": "recipient", "text": "Message lo transaction OTP ani undi! Bank credit limit ki OTP adagadu. You are trying to steal my money."}
        ],
        "scam_tactics": ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["credit card limit upgrade lure", "transaction otp misrepresentation", "urgent verbal code demand"],
        "explanation": "Posing as bank representative offering credit limit enhancement to harvest authentication OTP.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-064
    items.append({
        "conversation_id": "KAV-SYNTH-064",
        "language": "te-en",
        "primary_label": "SCAM",
        "scenario": "WhatsApp Hotel Rating Part-Time Task Scam",
        "dialogue": [
            {"speaker": "caller", "text": "Hi sir, this is Anitha from Global Marketing Partners. Are you interested in part-time online tasks?"},
            {"speaker": "recipient", "text": "What kind of tasks? How much time does it take?"},
            {"speaker": "caller", "text": "Daily one hour work sir. Google maps lo 5 star hotel reviews submit cheyali. Daily payout three thousand rupees."},
            {"speaker": "recipient", "text": "Is this genuine? How will you transfer money?"},
            {"speaker": "caller", "text": "First two tasks sample bonus five hundred rupees alreadymee Google Pay ki pampam. But next high profit tasks unlock cheyadaniki five thousand deposit cheyali."},
            {"speaker": "recipient", "text": "Why should I deposit money for doing review work?"},
            {"caller": "caller", "speaker": "caller", "text": "It is prepaid investment task sir. If you deposit five thousand, you will receive seven thousand five hundred within twenty minutes."},
            {"speaker": "recipient", "text": "This is a classic task investment fraud. Stop calling me."}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"],
        "risk_indicators": ["small initial trial bonus bait", "prepaid task investment demand", "guaranteed immediate profit return"],
        "explanation": "Hotel review task scam using small initial payouts to bait victims into depositing larger non-refundable amounts.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-065
    items.append({
        "conversation_id": "KAV-SYNTH-065",
        "language": "te-en",
        "primary_label": "SCAM",
        "scenario": "VIP Stock Market Trading WhatsApp Group Fraud",
        "dialogue": [
            {"speaker": "caller", "text": "Hello sir, Angel One VIP Institutional Trading desk nundi call chestunnamu."},
            {"speaker": "recipient", "text": "Yes, I have an active demat account. What is this about?"},
            {"speaker": "caller", "text": "Mee portfolio returns double cheyadaniki ma institutional block trades WhatsApp channel lo exclusive access istunnamu."},
            {"speaker": "recipient", "text": "Which stocks do you recommend?"},
            {"speaker": "caller", "text": "Pre-IPO shares and circuit stocks sir. Minimum twenty percent profit per trade guarantee."},
            {"speaker": "recipient", "text": "SEBI does not allow guaranteed stock returns."},
            {"caller": "caller", "speaker": "caller", "text": "Idi private institutional allocation sir. Fifty thousand ma manager personal account ki transfer chesi account open cheyandi."},
            {"speaker": "recipient", "text": "Brokers never ask money to personal bank accounts. You are running a fake trading scam."}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["guaranteed stock market returns", "unregistered vip whatsapp channel", "transfer to personal bank account"],
        "explanation": "Investment fraud promising guaranteed market returns via WhatsApp channel and soliciting direct personal funds.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-066
    items.append({
        "conversation_id": "KAV-SYNTH-066",
        "language": "te-en",
        "primary_label": "SCAM",
        "scenario": "Overseas Student Visa Processing Urgent Fee Fraud",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Sumanth, calling from Canadian Immigration Consulate and Global Visa Desk, Hyderabad."},
            {"speaker": "recipient", "text": "Yes madam, na student visa application stage enti?"},
            {"speaker": "caller", "text": "Mee visa file biometric review lo hold lo pettaru due to university tuition fee verification mismatch."},
            {"recipient": "recipient", "speaker": "recipient", "text": "University lo fee already pay chesanu kadandi, GIC account kuda active ga undi."},
            {"speaker": "caller", "text": "Ottawa embassy high commission nundi notice vachindi. Ee roju evening lopu verification bond pay cheyakapothe visa reject avtundi."},
            {"speaker": "recipient", "text": "How much is the verification bond?"},
            {"caller": "caller", "speaker": "caller", "text": "Forty-five thousand rupees immediately ma official immigration officer UPI handle ki transfer cheyandi."},
            {"speaker": "recipient", "text": "Canadian embassy eppudu UPI dwara fees tiskodu. Everything goes through VFS Global portal. This is fake."}
        ],
        "scam_tactics": ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"],
        "risk_indicators": ["embassy visa rejection threat", "urgent verification bond demand", "private upi payment request"],
        "explanation": "Impersonation of immigration authority threatening visa cancellation to coerce urgent UPI wire.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-067
    items.append({
        "conversation_id": "KAV-SYNTH-067",
        "language": "te-en",
        "primary_label": "SCAM",
        "scenario": "Fake UPI Scratch Card Cashback Claim Link",
        "dialogue": [
            {"speaker": "caller", "text": "Congratulations sir, PhonePe festive season reward program lo meeku three thousand nine hundred cashback vachindi."},
            {"speaker": "recipient", "text": "Cashback na PhonePe wallet lo direct ga credit avtunda?"},
            {"speaker": "caller", "text": "Yes sir, kani meeru scratch card claim cheyali. Nenu mee WhatsApp ki official link send chesanu."},
            {"speaker": "recipient", "text": "Link click cheste em cheyali?"},
            {"speaker": "caller", "text": "Link open chesi mee bank select chesi, pay button click chesi mee UPI PIN enter cheyandi, money credit avtundi."},
            {"speaker": "recipient", "text": "Pay button nokki PIN kodithe naku dabbu raadu, na account nundi debit avtundi!"},
            {"caller": "caller", "speaker": "caller", "text": "No sir, idi receiving gateway reverse protocol. PIN enter cheyakapothe cashback bounce avtundi."},
            {"speaker": "recipient", "text": "UPI lo receive cheskodaniki PIN avasaram ledu. Stop trying to scam me."}
        ],
        "scam_tactics": ["OTP_PIN_CVV_THEFT", "MALICIOUS_LINK_OR_APP", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["cashback scratch card lure", "upi pin requested to receive money", "reverse protocol deception"],
        "explanation": "Deceptive scheme claiming UPI PIN is required to receive rewards, attempting to execute an outbound fund transfer.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-068
    items.append({
        "conversation_id": "KAV-SYNTH-068",
        "language": "te-en",
        "primary_label": "SCAM",
        "scenario": "Federal Express Customs Clearance Verification Threat",
        "dialogue": [
            {"speaker": "caller", "text": "Federal Express international cargo clearance department. Am I speaking with Karthik?"},
            {"speaker": "recipient", "text": "Yes, Karthik speaking."},
            {"speaker": "caller", "text": "Mee name and PAN card tho Taipei nundi Hyderabad ki vachina courier box lo military-grade communication chips unnai."},
            {"speaker": "recipient", "text": "Military chips? I work in sales, naaku hardware import tho em relation ledu."},
            {"caller": "caller", "speaker": "caller", "text": "Customs enforcement team FIR lodge chesindi. To prevent immediate blacklisting and passport seizure, video interrogation attend avvali."},
            {"speaker": "recipient", "text": "Can I visit Hyderabad airport customs office directly?"},
            {"caller": "caller", "speaker": "caller", "text": "Airport ki velthe arrest chestharu. Just pay thirty thousand clearance clearance guarantee right now on our portal."},
            {"speaker": "recipient", "text": "Customs never demands online bail guarantees over calls. I am contacting cybercrime division."}
        ],
        "scam_tactics": ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"],
        "risk_indicators": ["customs contraband extortion", "passport seizure threat", "online clearance bail guarantee"],
        "explanation": "Courier customs fraud alleging military equipment import to demand immediate online clearance deposit.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-069 (Legit 1)
    items.append({
        "conversation_id": "KAV-SYNTH-069",
        "language": "te-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Software Engineer Onboarding Laptop Courier Tracking",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Sravani, I am calling from Infosys IT Logistics desk, Bangalore campus."},
            {"speaker": "recipient", "text": "Hi sir! Regarding my work-from-home onboarding kit?"},
            {"speaker": "caller", "text": "Yes Sravani, mee company laptop and welcome kit BlueDart courier dwaara dispatch chesamu."},
            {"speaker": "recipient", "text": "Tracking number generate ainda sir?"},
            {"speaker": "caller", "text": "Yes, tracking AWB number mee personal email ki share chesamu. Expected delivery is tomorrow by two PM."},
            {"speaker": "recipient", "text": "Do I need to sign any document during delivery?"},
            {"speaker": "caller", "text": "Yes, package unbox chesi external damage ledu ani acknowledgment slip sign cheyali. No payment is required."},
            {"speaker": "recipient", "text": "Sure sir, I will receive it and inform the onboarding team. Thank you."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["corporate onboarding logistics", "no payment requirement", "official company email tracking"],
        "explanation": "Authentic corporate IT department coordinating work laptop courier delivery with zero financial demands.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/telugu_english/kav_synth_069.wav"
    })

    # KAV-SYNTH-070
    items.append({
        "conversation_id": "KAV-SYNTH-070",
        "language": "te-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Tech Conference Registration & Delegate Badging Details",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Aditya, this is Divya from PyData Hyderabad organizing committee."},
            {"speaker": "recipient", "text": "Hi Divya, thanks for calling!"},
            {"speaker": "caller", "text": "Calling to confirm your delegate registration for PyData conference at HICC Novotel this Friday."},
            {"speaker": "recipient", "text": "Yes, I registered under early bird pass."},
            {"speaker": "caller", "text": "Great! Entry badge will be available at gate registration desk. Please carry any government photo ID."},
            {"speaker": "recipient", "text": "Are workshop seats reserved or first-come-first-serve?"},
            {"speaker": "caller", "text": "Hands-on workshops are first-come-first-serve basis, so early ga arrive avvadam better."},
            {"speaker": "recipient", "text": "Understood Divya, see you at the venue on Friday."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["technical conference registration", "no financial demands", "physical venue badging"],
        "explanation": "Legitimate tech community conference coordination confirming delegate entry protocols.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-071
    items.append({
        "conversation_id": "KAV-SYNTH-071",
        "language": "te-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Apartment Fiber Broadband Installation Schedule",
        "dialogue": [
            {"speaker": "caller", "text": "Hello, calling from Airtel Xstream Fiber installation team. Am I speaking with Mr. Charan?"},
            {"speaker": "recipient", "text": "Yes Charan speaking."},
            {"speaker": "caller", "text": "Sir, mee apartment My Home Bhooja lo new fiber optic connection installation kosam engineer allocate ayyaru."},
            {"speaker": "recipient", "text": "Eppudu vastaru engineer?"},
            {"speaker": "caller", "text": "Today evening four to six PM slot lo visit chestharu. Router and optical terminal unit free of cost deliver avtundi."},
            {"speaker": "recipient", "text": "Installation fee evarikaina cash ga ivvala?"},
            {"speaker": "caller", "text": "No cash payments sir. Any advance charges your first monthly bill lo Airtel Thanks app lo direct ga pay cheskovachu."},
            {"speaker": "recipient", "text": "Perfect, evening four PM ki intlo untanu, send the engineer."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["standard telecom broadband installation", "no cash or private payments", "official app billing"],
        "explanation": "Authentic broadband installation scheduling with explicit direction to pay only via official mobile app.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-072
    items.append({
        "conversation_id": "KAV-SYNTH-072",
        "language": "te-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Gym Membership Annual Plan Renewal",
        "dialogue": [
            {"speaker": "caller", "text": "Hi Varun, this is Sneha from Cult.fit Kondapur center."},
            {"speaker": "recipient", "text": "Hi Sneha, what is this regarding?"},
            {"speaker": "caller", "text": "Mee Cult Elite annual membership next week expire avtundi. We have an anniversary renewal offer."},
            {"speaker": "recipient", "text": "What is the offer discount?"},
            {"speaker": "caller", "text": "Renewal chesthe additional two months extension at zero cost. Offer is applied automatically in your Cult mobile app."},
            {"speaker": "recipient", "text": "Can I renew through the app directly?"},
            {"speaker": "caller", "text": "Yes, app open chesi 'Renew Membership' click cheyandi, no phone payments needed."},
            {"speaker": "recipient", "text": "Great, I will renew it tonight in the app."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["routine fitness renewal", "self-service app payment", "no phone credential collection"],
        "explanation": "Standard fitness center membership renewal notification directing customer to official self-service app.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-073
    items.append({
        "conversation_id": "KAV-SYNTH-073",
        "language": "te-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Passport Seva Kendra Document Checklist Inquiry",
        "dialogue": [
            {"speaker": "caller", "text": "Good afternoon, calling from Passport Seva Kendra enquiry desk, Begumpet."},
            {"speaker": "recipient", "text": "Yes sir, regarding my appointment tomorrow morning?"},
            {"speaker": "caller", "text": "Yes, mee appointment slot tomorrow ten fifteen AM ki undి. Document checklist remind cheyadaniki call chesamu."},
            {"speaker": "recipient", "text": "Which original documents should I carry?"},
            {"speaker": "caller", "text": "Original Aadhaar card, matriculation certificate, and current address proof utility bill compulsory ga carry cheyali."},
            {"speaker": "recipient", "text": "Are photocopies accepted?"},
            {"caller": "caller", "speaker": "caller", "text": "One set of self-attested photocopies tho patu original documents verify chestaru. No agent payments are entertained."},
            {"speaker": "recipient", "text": "Understood sir, I have all the originals ready. Thank you."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["official passport seva kendra support", "in-person verification instructions", "anti-agent disclaimer"],
        "explanation": "Legitimate passport service customer support confirming appointment checklist and warning against unauthorized agents.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-074
    items.append({
        "conversation_id": "KAV-SYNTH-074",
        "language": "te-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Medical Diagnostic Sample Pickup Coordination",
        "dialogue": [
            {"speaker": "caller", "text": "Hello madam, Vijaya Diagnostic home collection technician Raju calling."},
            {"speaker": "recipient", "text": "Hello Raju, when will you arrive for blood sample collection?"},
            {"speaker": "caller", "text": "Madam, I am ten minutes away from your apartment in Madhapur."},
            {"speaker": "recipient", "text": "My father is fasting as instructed. Will thyroid panel reports come today?"},
            {"speaker": "caller", "text": "Yes madam, thyroid and lipid profile reports evening six PM lopu email and SMS link dwaara download cheskovachu."},
            {"speaker": "recipient", "text": "Can I pay via UPI scan at home?"},
            {"caller": "caller", "speaker": "caller", "text": "Yes madam, company barcode scanner undi, sample sealed pack chesaka you can pay."},
            {"speaker": "recipient", "text": "Very good, gate security ki cheppi unchanu, come directly to flat 302."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["healthcare home sample collection", "authorized company qr payment upon service", "routine medical protocols"],
        "explanation": "Authentic medical laboratory home collection service coordinating sample pickup securely.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-075
    items.append({
        "conversation_id": "KAV-SYNTH-075",
        "language": "te-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Pet Veterinary Clinic Vaccination Reminder",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Swathi, this is Dr. Rao's Pet Clinic reception calling regarding your Golden Retriever, Bruno."},
            {"speaker": "recipient", "text": "Hi! Is Bruno's annual rabies booster vaccination due?"},
            {"speaker": "caller", "text": "Yes Swathi, annual anti-rabies and DHPP booster vaccine due date is day after tomorrow."},
            {"speaker": "recipient", "text": "Can I book a Saturday morning appointment slot?"},
            {"speaker": "caller", "text": "Saturday eleven AM slot is available. General health checkup and weight monitoring kuda untundi."},
            {"speaker": "recipient", "text": "Does he need any fasting before vaccination?"},
            {"caller": "caller", "speaker": "caller", "text": "No fasting needed. Just bring Bruno's vaccination booklet with you. Payment can be made at clinic desk."},
            {"speaker": "recipient", "text": "Perfect, please confirm the Saturday eleven AM slot. Thanks!"}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["routine veterinary appointment", "payment at clinic desk", "no advance money requests"],
        "explanation": "Benign pet healthcare clinic routine booster vaccination reminder.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-076 (Pilot 4)
    items.append({
        "conversation_id": "KAV-SYNTH-076",
        "pilot_id": "KAV-SYNTH-PILOT-004",
        "language": "te-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Unverified University Semester Fee Clarification",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Srinivas garu, నేను university accounts section నుండి రమేష్ మాట్లాడుతున్నాను."},
            {"speaker": "recipient", "text": "Yes Ramesh garu, చెప్పండి, ఏంటి విషయం?"},
            {"speaker": "caller", "text": "మీ third semester tuition fee payment transaction portal లో reconcile అవ్వలేదు."},
            {"speaker": "recipient", "text": "Portal లో success అని వచ్చింది కదా? Bank account లో కూడా debit అయింది."},
            {"speaker": "caller", "text": "UTR number match అవ్వడం లేదు. మీ fee receipt copy ని admin office email కి forward చేయగలరా?"},
            {"speaker": "recipient", "text": "Sure, ఏ email address కి పంపించాలి? WhatsApp లో పంపించమంటారా?"},
            {"speaker": "caller", "text": "No WhatsApp. కేవలం official university portal లోని accounts@university.edu.in కి మాత్రమే పంపించండి."},
            {"speaker": "recipient", "text": "Okay, transaction reference number తో ఇప్పుడే email చేస్తాను, verify చేయండి."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["unreconciled fee notice", "payment record ambiguity", "official channel direction"],
        "explanation": "Ambiguous administrative notification regarding fee payment mismatch directing to official verified channels without threat or credential extortion.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/telugu_english/kav-synth-pilot-004.wav"
    })

    # KAV-SYNTH-077
    items.append({
        "conversation_id": "KAV-SYNTH-077",
        "language": "te-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Bank Fraud Department Suspicious Transaction Verification",
        "dialogue": [
            {"speaker": "caller", "text": "Good evening, calling from HDFC Bank Central Fraud Monitoring Cell. Am I speaking with Mr. Teja?"},
            {"speaker": "recipient", "text": "Yes, Teja speaking. Is everything alright with my account?"},
            {"speaker": "caller", "text": "Sir, just now forty-eight thousand rupees international e-commerce transaction initiate aindi on UK merchant website. Did you authorize this?"},
            {"speaker": "recipient", "text": "No! I did not make any UK transaction! Please stop it immediately!"},
            {"speaker": "caller", "text": "We have temporarily blocked the transaction at our gateway. Card security verify cheyadaniki card details confirm chestara?"},
            {"speaker": "recipient", "text": "What details do you need? Will you ask for OTP or CVV?"},
            {"caller": "caller", "speaker": "caller", "text": "Never share OTP or CVV with anyone. We only need you to confirm your mother's maiden name or you can open mobile banking app and press 'Block Card'."},
            {"speaker": "recipient", "text": "I am opening my official mobile banking app right now and blocking the card directly from settings."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["fraud alert urgency", "suspicious international transaction context", "prohibition on sharing otp and self-service blocking advised"],
        "explanation": "High-urgency bank fraud monitoring call regarding unauthorized overseas transaction, with explicit instruction to use official app.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-078
    items.append({
        "conversation_id": "KAV-SYNTH-078",
        "language": "te-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Coworking Space Dedicated Seat Deposit Clarification",
        "dialogue": [
            {"speaker": "caller", "text": "Hi Sandeep, calling from WeWork Gachibowli community management team."},
            {"speaker": "recipient", "text": "Hi, regarding our four-seater dedicated desk agreement?"},
            {"speaker": "caller", "text": "Yes Sandeep, lease agreement signed kani two months refundable security deposit payment gateway lo pending chupistundi."},
            {"speaker": "recipient", "text": "We already transferred via RTGS from our company account on Tuesday."},
            {"speaker": "caller", "text": "Bank statement lo UTR update kaledu. Can you share payment screenshot to our manager personal WhatsApp?"},
            {"speaker": "recipient", "text": "Why personal WhatsApp? Isn't there an official billing ticket portal?"},
            {"caller": "caller", "speaker": "caller", "text": "You can upload on WeWork portal also, WhatsApp was suggested just for immediate desk activation today."},
            {"speaker": "recipient", "text": "I will stick to official billing portal and upload the RTGS counterfoil there."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["corporate deposit reconciliation", "informal channel requested for speed", "official portal alternative retained"],
        "explanation": "Commercial lease billing coordination with informal shortcut suggested but standard portal available.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-079
    items.append({
        "conversation_id": "KAV-SYNTH-079",
        "language": "te-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Freelance Web Development Project Advance Dispute",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Pradeep, this is Client Services Manager John from CloudScale Technologies."},
            {"speaker": "recipient", "text": "Yes John, react frontend project milestones gurincha?"},
            {"speaker": "caller", "text": "Mee code pull request quality audit lo test cases fail ayyayi. Second milestone milestone payout thirty thousand release cheyadam hold lo pettam."},
            {"speaker": "recipient", "text": "Scope of work lo automated unit test coverage mention cheyaledu kadandi."},
            {"speaker": "caller", "text": "Standard delivery terms lo code coverage mandatory. Advance payout unlock cheyadaniki security escrow deposit ten thousand pay cheyali."},
            {"speaker": "recipient", "text": "Developer advance escrow enduku pay cheyali? This sounds very suspicious."},
            {"caller": "caller", "speaker": "caller", "text": "Contract clause 4.2 review cheyandi. If not comfortable, we can do a joint Zoom meeting with management on Monday."},
            {"speaker": "recipient", "text": "Yes, let us schedule the formal Zoom meeting with the contract copy."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["commercial contractual dispute", "unusual escrow payment request", "formal meeting agreed"],
        "explanation": "Contractual freelance scope dispute involving an unconventional escrow request, with formal meeting scheduled to review contract.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-080
    items.append({
        "conversation_id": "KAV-SYNTH-080",
        "language": "te-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Cloud Infrastructure Subscription Auto-Renewal Notice",
        "dialogue": [
            {"speaker": "caller", "text": "Hello, AWS billing support desk representative calling. Is this Mr. Nikhil?"},
            {"speaker": "recipient", "text": "Yes Nikhil speaking."},
            {"speaker": "caller", "text": "Mee EC2 compute instances auto-renewal monthly charge one hundred and twenty dollars credit card failure chupistundi."},
            {"speaker": "recipient", "text": "My card was renewed last month, so old card might have failed."},
            {"speaker": "caller", "text": "If payment is not cleared in twelve hours, your production cloud database snapshot will be permanently purged."},
            {"speaker": "recipient", "text": "Permanent purge in twelve hours? That is extremely abrupt. AWS usually provides fifteen days grace period."},
            {"caller": "caller", "speaker": "caller", "text": "System policy rules sir. You can update your payment method directly inside your AWS root console."},
            {"speaker": "recipient", "text": "I am logging into my official AWS console directly to inspect the billing tab."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["service termination urgency", "cloud billing payment dispute", "direction to official cloud console"],
        "explanation": "High-urgency cloud infrastructure payment warning directing customer to official root console.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    return items

def get_hindi_english_conversations():
    items = []

    # KAV-SYNTH-081
    items.append({
        "conversation_id": "KAV-SYNTH-081",
        "language": "hi-en",
        "primary_label": "SCAM",
        "scenario": "Google Maps Hotel Review Work-From-Home Task Scam",
        "dialogue": [
            {"speaker": "caller", "text": "Hello sir, I am Tina from Digital Boost India. Are you interested in part-time flexible online earning?"},
            {"speaker": "recipient", "text": "Kis tarah ka kaam hai? Office aana hoga kya?"},
            {"speaker": "caller", "text": "No office needed, daily one to two hours work from home. Sirf Google Maps par luxury hotels ko 5-star rating aur reviews dena hai."},
            {"speaker": "recipient", "text": "Per review kitna payment milega?"},
            {"speaker": "caller", "text": "One review fifty rupees. Daily minimum two thousand guaranteed payout directly into your UPI account."},
            {"speaker": "recipient", "text": "Kaam shuru karne ke liye kya karna hoga?"},
            {"speaker": "caller", "text": "Aapko pehle humare Telegram VIP task group mein do hazar rupaye security deposit transfer karna padega for verification."},
            {"speaker": "recipient", "text": "Kaam karne ke liye paise mang rahe ho? Yeh fake rating task scam hai."}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"],
        "risk_indicators": ["task rating job lure", "unrealistic daily payout", "upfront telegram security deposit"],
        "explanation": "Fraudulent online task scheme offering easy review earnings to extort advance enrollment deposit via Telegram.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/hindi_english/kav_synth_081.wav"
    })

    # KAV-SYNTH-082
    items.append({
        "conversation_id": "KAV-SYNTH-082",
        "language": "hi-en",
        "primary_label": "SCAM",
        "scenario": "Enforcement Directorate Money Laundering Digital Arrest Skype Threat",
        "dialogue": [
            {"speaker": "caller", "text": "This is Joint Director R.K. Singhal from Enforcement Directorate, New Delhi headquarters."},
            {"speaker": "recipient", "text": "ED office? Maine kya kiya hai sir?"},
            {"speaker": "caller", "text": "Aapke Aadhaar aur ICICI account ke through Naresh Goyal money laundering scam mein five crore transactions trace huye hain."},
            {"speaker": "recipient", "text": "Mera aisa koi transaction nahi hai sir, my income is completely tax paid."},
            {"speaker": "caller", "text": "Non-bailable arrest warrant ready hai. Aapko twenty-four hours digital arrest mein rehna hoga under Skype continuous camera surveillance."},
            {"speaker": "recipient", "text": "Main apne family advocate ko call karke inform kar doon?"},
            {"speaker": "caller", "text": "Strictly confidential investigation hai. Kisi ko bataya toh immediate family members ko bhi arrest kar liya jayega."},
            {"speaker": "recipient", "text": "Courts aur ED Skype par digital arrest nahi karte. Main police station jaakar cybercrime complaint karunga."}
        ],
        "scam_tactics": ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE", "URGENCY_OR_THREAT"],
        "risk_indicators": ["enforcement directorate impersonation", "digital arrest assertion", "continuous camera surveillance threat", "isolation from family"],
        "explanation": "High-pressure digital arrest coercion claiming high-profile money laundering to induce psychological fear and compliance.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/hindi_english/kav_synth_082.wav"
    })

    # KAV-SYNTH-083
    items.append({
        "conversation_id": "KAV-SYNTH-083",
        "language": "hi-en",
        "primary_label": "SCAM",
        "scenario": "Fake Electricity Bill Penalty APK Download Threat",
        "dialogue": [
            {"speaker": "caller", "text": "Discom customer care service alert. Sir, aapka power supply tonight at ten PM disconnect ho jayega."},
            {"speaker": "recipient", "text": "Disconnect kyu hoga? Maine regular bill pay kiya hai through Cred app."},
            {"speaker": "caller", "text": "Third party payment app ka server error tha sir, unka reconciliation hamare electricity board mein pending hai."},
            {"speaker": "recipient", "text": "Toh main subah bill receipt electricity office dikha dunga."},
            {"speaker": "caller", "text": "Night line maintenance squad already on the way hai. Line chalu rakhne ke liye hamara quick utility APK update install kijiye."},
            {"speaker": "recipient", "text": "APK file kahan se milegi?"},
            {"speaker": "caller", "text": "Hum WhatsApp par direct link bhej rahe hain. Install karke bank details fill karke one rupee verification payment kijiye."},
            {"speaker": "recipient", "text": "Third-party APK se phone control lene ka scam hai yeh. Main direct discom substation call karunga."}
        ],
        "scam_tactics": ["REMOTE_ACCESS_MANIPULATION", "MALICIOUS_LINK_OR_APP", "URGENCY_OR_THREAT", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["immediate power supply cut urgency", "whatsapp utility apk file", "one rupee verification lure"],
        "explanation": "Electricity discom impersonation threatening nighttime disconnection to distribute malicious APK and extract bank details.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-084
    items.append({
        "conversation_id": "KAV-SYNTH-084",
        "language": "hi-en",
        "primary_label": "SCAM",
        "scenario": "SBI YONO Account Deactivation Phishing Link Fraud",
        "dialogue": [
            {"speaker": "caller", "text": "State Bank of India YONO digital cell. Sir aapka YONO banking app account permanently expire ho gaya hai."},
            {"speaker": "recipient", "text": "YONO expire ho gaya? Par main toh kal hi use kar raha tha."},
            {"speaker": "caller", "text": "Mandatory PAN card re-verification mandate launch hua hai. Agar update nahi karenge toh accounts freeze ho jayenge."},
            {"speaker": "recipient", "text": "Kahan se update karna hai?"},
            {"speaker": "caller", "text": "Humne aapko SMS par link bheja hai 'sbi-kyc-update.online'. Uspar click karke netbanking password aur profile password enter kijiye."},
            {"speaker": "recipient", "text": "Yeh link official onlinesbi.com toh nahi hai!"},
            {"caller": "caller", "speaker": "caller", "text": "High traffic server load ki wajah se temporary fast-track portal banaya gaya hai. Jaldi kijiye warna card block ho jayega."},
            {"speaker": "recipient", "text": "Bank kabhi unofficial domain par password nahi mangta. Phishing link hai yeh."}
        ],
        "scam_tactics": ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT", "MALICIOUS_LINK_OR_APP"],
        "risk_indicators": ["yono app expiration threat", "fake non-bank domain link", "netbanking password solicitation"],
        "explanation": "Banking phishing attack using urgent YONO deactivation threat to collect online banking credentials on fake domain.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-085
    items.append({
        "conversation_id": "KAV-SYNTH-085",
        "language": "hi-en",
        "primary_label": "SCAM",
        "scenario": "Customs Duty Fee Demand for International Gift Parcel",
        "dialogue": [
            {"speaker": "caller", "text": "Hello, this is Custom Clearance Officer Neha calling from Indira Gandhi International Airport cargo facility."},
            {"speaker": "recipient", "text": "Yes, kaun bol rahe hain?"},
            {"speaker": "caller", "text": "Aapke name par London se ek diplomatic gift parcel arrive hua hai containing gold watch, iPhone 16 and twenty thousand UK pounds."},
            {"speaker": "recipient", "text": "Mujhe London se koi gift nahi bhejta. Yeh kisi aur ka hoga."},
            {"speaker": "caller", "text": "Box par aapka mobile number aur address clearly printed hai. Foreign currency illegal undeclared smuggling hai under FEMA Act."},
            {"speaker": "recipient", "text": "Maine koi parcel order nahi kiya!"},
            {"caller": "caller", "speaker": "caller", "text": "FIR avoid karne ke liye custom clearance tax of thirty-eight thousand rupees transfer kijiye hamare RBI officer ke Google Pay par."},
            {"speaker": "recipient", "text": "Customs tax kabhi Google Pay par personal account mein nahi liya jata. Fraud call hai yeh."}
        ],
        "scam_tactics": ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"],
        "risk_indicators": ["foreign gift parcel with cash and gold lure", "fema act smuggling threat", "customs tax demanded via google pay"],
        "explanation": "Diplomatic gift parcel extortion pretending customs seizure of foreign cash and gold to demand payment via Google Pay.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-086
    items.append({
        "conversation_id": "KAV-SYNTH-086",
        "language": "hi-en",
        "primary_label": "SCAM",
        "scenario": "Urgent Hospital Accident Extortion Impersonating Family Relative",
        "dialogue": [
            {"speaker": "caller", "text": "Uncle namaste! Main Rohit bol raha hoon, aapka nephew. Bohot bada emergency ho gaya hai."},
            {"speaker": "recipient", "text": "Rohit? Kya hua beta? Awaz aisi kyu lag rahi hai?"},
            {"speaker": "caller", "text": "Mera car accident ho gaya hai highway par. Do log seriously injure ho gaye hain, police mujhe arrest kar rahi hai."},
            {"speaker": "recipient", "text": "Arrey baap re! Tumhare mummy papa ko pata hai kya?"},
            {"speaker": "caller", "text": "Nahi uncle, mummy heart patient hain, unko pata chala toh unki tabiyat bigad jayegi. Please unko mat batana."},
            {"speaker": "recipient", "text": "Abhi tum kahan par ho?"},
            {"caller": "caller", "speaker": "caller", "text": "Police station ke inspector compromise karne ko ready hain agar fifty thousand compensation abhi transfer kar dein unke number par."},
            {"speaker": "recipient", "text": "Main pehle tumhare papa se baat karunga, bina verify kiye kisi police ko phone par paise nahi dunga."}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"],
        "risk_indicators": ["fake nephew accident pretext", "demand not to inform parents", "urgent police compromise bribe demand"],
        "explanation": "Emotional extortion impersonating nephew claiming car accident to extract emergency settlement funds.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-087
    items.append({
        "conversation_id": "KAV-SYNTH-087",
        "language": "hi-en",
        "primary_label": "SCAM",
        "scenario": "Credit Card Reward Points Expiry Redemption Scam",
        "dialogue": [
            {"speaker": "caller", "text": "Good afternoon, calling from HDFC credit card reward redemption loyalty department."},
            {"speaker": "recipient", "text": "Yes, reward points ke baare mein?"},
            {"speaker": "caller", "text": "Sir aapke card par twelve thousand reward points expire hone wale hain tonight at midnight. Unka cash value six thousand rupees banta hai."},
            {"speaker": "recipient", "text": "Cash value statement mein adjust ho sakta hai kya?"},
            {"speaker": "caller", "text": "Yes sir, direct bank credit ho jayega. Bas card details verify karwa dijiye."},
            {"speaker": "recipient", "text": "Aapke paas toh card details already hongi?"},
            {"caller": "caller", "speaker": "caller", "text": "Security policy ke according aapka sixteen digit card number, expiry date aur card ke peeche likha CVV code batana hoga to initiate credit."},
            {"speaker": "recipient", "text": "CVV sirf payment ke liye hota hai, credit ke liye nahi. Card details chori karne ka tareeka hai yeh."}
        ],
        "scam_tactics": ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"],
        "risk_indicators": ["reward points midnight expiry urgency", "cash conversion lure", "card cvv requested for credit"],
        "explanation": "Reward points expiry urgency used to deceive cardholder into disclosing 16-digit card number and CVV.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-088
    items.append({
        "conversation_id": "KAV-SYNTH-088",
        "language": "hi-en",
        "primary_label": "SCAM",
        "scenario": "Fake Police Cyber Cell FIR Cancellation Bribe Fraud",
        "dialogue": [
            {"speaker": "caller", "text": "This is Sub-Inspector Verma from Delhi Police Special Cyber Cell unit, Lodhi Colony."},
            {"speaker": "recipient", "text": "Ji inspector sahab, kis baare mein phone hai?"},
            {"speaker": "caller", "text": "Aapke IP address se illegal darknet website browsing aur financial fraud complaints register hui hain under Section 66D IT Act."},
            {"speaker": "recipient", "text": "Main IT company mein software engineer hoon sir, maine aisi koi darknet site nahi kholi."},
            {"speaker": "caller", "text": "Server logs prove kar rahe hain. FIR draft ho chuki hai, shaam tak media mein release ho jayegi aur company HR ko inform karenge."},
            {"speaker": "recipient", "text": "Company HR ko kyu inform karenge? Meri job risk mein aa jayegi!"},
            {"caller": "caller", "speaker": "caller", "text": "Agar naam clean rakhna hai aur FIR cancel karwani hai toh informal settlement charge of forty thousand transfer kijiye."},
            {"speaker": "recipient", "text": "Police officer phone par settlement bribe nahi mangte. Main lawyer ke sath seedha ACP cybercrime office aa raha hoon."}
        ],
        "scam_tactics": ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"],
        "risk_indicators": ["cyber cell fir threat", "threat to inform corporate employer", "settlement bribe demand"],
        "explanation": "Cyber cell police impersonation threatening defamation and employer notification to extort cancellation bribe.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-089 (Pilot 5)
    items.append({
        "conversation_id": "KAV-SYNTH-089",
        "pilot_id": "KAV-SYNTH-PILOT-005",
        "language": "hi-en",
        "primary_label": "LEGITIMATE",
        "scenario": "E-Commerce Delivery Address Clarification & Safe Delivery PIN",
        "dialogue": [
            {"speaker": "caller", "text": "Hello sir, main BlueDart courier delivery executive bol raha hoon. Aapka Amazon parcel deliver karna hai."},
            {"speaker": "recipient", "text": "Haan bhaiya, aap kahan par pahunche hain?"},
            {"speaker": "caller", "text": "Main aapke apartment ke main gate par hoon, lekin building number 4 clear nahi dikh raha hai."},
            {"speaker": "recipient", "text": "Main security cabin ke paas khada hoon, lift ke left side aayiye."},
            {"speaker": "caller", "text": "Theek hai sir, main lift ke paas aa gaya hoon. Box par physical damage check kar lijiye."},
            {"speaker": "recipient", "text": "Haan package sealed hai. Payment already UPI se ho chuka tha na?"},
            {"speaker": "caller", "text": "Ji sir, pre-paid order hai. Handover complete karne ke liye delivery code bata dijiye jo app par aaya hai."},
            {"speaker": "recipient", "text": "Delivery code hai 4821. Thank you bhaiya."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["standard delivery pin", "physical handover verification", "no financial solicitation"],
        "explanation": "Benign routine delivery confirmation verifying package condition and standard delivery completion code.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/hindi_english/kav-synth-pilot-005.wav"
    })

    # KAV-SYNTH-090
    items.append({
        "conversation_id": "KAV-SYNTH-090",
        "language": "hi-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Food Delivery App Order Location Coordination",
        "dialogue": [
            {"speaker": "caller", "text": "Bhaiya namaste, Swiggy delivery partner bol raha hoon. Aapka food order pick kar liya hai."},
            {"speaker": "recipient", "text": "Haan bhaiya, location sahi dikh raha hai na GPS par?"},
            {"speaker": "caller", "text": "Sir aapke society ke main gate par security guard entry nahi de rahe hain without visitor pass."},
            {"speaker": "recipient", "text": "Main MyGate app par entry approve kar deta hoon, do minute rukiye."},
            {"speaker": "caller", "text": "Theek hai sir, entry milte hi main C-block lift se 4th floor aa raha hoon."},
            {"speaker": "recipient", "text": "Haan flat 404 hai. Doorbell baja dena."},
            {"caller": "caller", "speaker": "caller", "text": "Ji sir, order bag hot-case mein sealed hai. Main five minutes mein deliver kar raha hoon."},
            {"speaker": "recipient", "text": "Okay thank you bhaiya."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["food delivery logistics", "society visitor pass coordination", "no payment or credential inquiry"],
        "explanation": "Everyday food delivery logistics call coordinating residential entry without financial transaction.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-091
    items.append({
        "conversation_id": "KAV-SYNTH-091",
        "language": "hi-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Authorized Car Servicing Center Estimate & Pickup Time",
        "dialogue": [
            {"speaker": "caller", "text": "Good afternoon Mr. Kapoor, Hyundai authorized service center Okhla se Service Advisor Amit bol raha hoon."},
            {"recipient": "recipient", "speaker": "recipient", "text": "Haan Amit ji, meri Creta car ki 30,000 km regular servicing complete ho gayi kya?"},
            {"speaker": "caller", "text": "Sir engine oil replacement, brake pad cleaning aur wheel alignment sab complete ho gaya hai."},
            {"speaker": "recipient", "text": "Total billing amount kitna hua?"},
            {"speaker": "caller", "text": "Estimate bill tax mila kar six thousand four hundred bana hai sir. Invoice aapke WhatsApp aur email par bhej di hai."},
            {"speaker": "recipient", "text": "Car pickup ke liye kab aa sakta hoon?"},
            {"caller": "caller", "speaker": "caller", "text": "Washing aur vacuuming chal rahi hai, six PM tak vehicle ready ho jayegi. Payment aap bill desk par card ya cash se kar sakte hain."},
            {"speaker": "recipient", "text": "Theek hai, main six thirty par aakar test drive leke bill clear kar dunga."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["authorized vehicle service coordination", "transparent invoice breakdown", "on-site counter payment"],
        "explanation": "Authentic car dealership service center update with itemized bill and physical pickup arrangement.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-092
    items.append({
        "conversation_id": "KAV-SYNTH-092",
        "language": "hi-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Co-Working Desk Monthly Membership Confirmation",
        "dialogue": [
            {"speaker": "caller", "text": "Hi Rahul, this is Tanya from Innov8 Coworking community team, Cyber City Gurgaon."},
            {"speaker": "recipient", "text": "Hi Tanya! Regarding our dedicated hot desk renewal?"},
            {"speaker": "caller", "text": "Yes Rahul, aapka monthly dedicated desk pass renew ho gaya hai for next month. Access card validity update ho chuki hai."},
            {"speaker": "recipient", "text": "Does this plan include meeting room credits?"},
            {"speaker": "caller", "text": "Yes, ten hours of conference room credits aapke app wallet mein credit ho gaye hain. You can book directly via app."},
            {"speaker": "recipient", "text": "Tax invoice GST portal par kab reflect karegi?"},
            {"caller": "caller", "speaker": "caller", "text": "Accounts team within forty-eight hours B2B GST invoice aapke registered GSTIN par upload kar degi."},
            {"speaker": "recipient", "text": "Perfect Tanya, thanks for the quick update."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["coworking membership administration", "automated system update", "official app self-service"],
        "explanation": "Standard shared workspace membership confirmation with routine amenity and invoice details.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-093
    items.append({
        "conversation_id": "KAV-SYNTH-093",
        "language": "hi-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Diagnostic Health Package Report Delivery Notification",
        "dialogue": [
            {"speaker": "caller", "text": "Namaste Mr. Saxena, Lal PathLabs customer care team se baat kar rahi hoon."},
            {"speaker": "recipient", "text": "Haan, mere annual health checkup ke reports ready ho gaye kya?"},
            {"speaker": "caller", "text": "Yes sir, aapka complete blood count, HbA1c aur lipid profile reports verify hokar ready hain."},
            {"speaker": "recipient", "text": "Reports kaise milengi?"},
            {"speaker": "caller", "text": "Soft copy PDF aapke registered email par password-protected format mein send kar diya gaya hai. Password aapka birth year hai."},
            {"speaker": "recipient", "text": "Hard copy collect karne lab aana padega kya?"},
            {"caller": "caller", "speaker": "caller", "text": "Agar hard copy chahiye toh lab reception par lab ID bata kar collect kar sakte hain. No extra charges."},
            {"speaker": "recipient", "text": "Email par mil gaya hai toh hard copy ki zarurat nahi. Thank you."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["diagnostic health report delivery", "encrypted pdf format", "no unsolicited payment request"],
        "explanation": "Authentic diagnostic pathology center delivering patient test results via secure encrypted email.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-094
    items.append({
        "conversation_id": "KAV-SYNTH-094",
        "language": "hi-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Bank Home Loan Document Verification In-Person Visit Schedule",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Mr. Malhotra, ICICI Bank retail home loan processing team se loan officer Deepak bol raha hoon."},
            {"speaker": "recipient", "text": "Haan Deepak ji, hamare home loan application ka kya status hai?"},
            {"speaker": "caller", "text": "Sir aapki property legal title search clear ho chuki hai. Final sanction se pehle mandatory physical residence verification karna hai."},
            {"speaker": "recipient", "text": "Verification ke liye kab aana chahte hain?"},
            {"speaker": "caller", "text": "Tomorrow afternoon three PM ka time convenient rahega kya sir?"},
            {"speaker": "recipient", "text": "Haan, main aur meri wife dono ghar par rahenge. Kya documents check karenge?"},
            {"caller": "caller", "speaker": "caller", "text": "Bas original salary slip aur electricity bill physical copy check karenge. Kisi bhi officer ko cash ya processing fees bilkul nahi deni hai."},
            {"speaker": "recipient", "text": "Theek hai Deepak ji, kal 3 PM par milte hain."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["official banking home loan verification", "explicit warning against giving cash to officers", "in-person visit coordination"],
        "explanation": "Standard home loan physical verification scheduling with bank's anti-corruption disclaimers.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-095
    items.append({
        "conversation_id": "KAV-SYNTH-095",
        "language": "hi-en",
        "primary_label": "LEGITIMATE",
        "scenario": "Fitness Club Personal Trainer Session Reschedule",
        "dialogue": [
            {"speaker": "caller", "text": "Hi Rohit, Gold's Gym se trainer Vikram baat kar raha hoon."},
            {"speaker": "recipient", "text": "Haan Vikram, bolo. Aaj shaam ka personal training session hai na?"},
            {"speaker": "caller", "text": "Bhaiya aaj shaam ko gym floor par maintenance work chal raha hai, can we reschedule our session to tomorrow morning seven AM?"},
            {"speaker": "recipient", "text": "Tomorrow morning seven AM works fine for me. Leg workout karenge kal?"},
            {"speaker": "caller", "text": "Yes bhaiya, tomorrow we will do squat and mobility session. Post-workout protein shake ready rakhna."},
            {"speaker": "recipient", "text": "Sure Vikram. Package sessions count update ho gaya tha na system mein?"},
            {"caller": "caller", "speaker": "caller", "text": "Haan, twelve sessions balance hain gym mobile app dashboard par. Kal subah seven AM sharp milte hain."},
            {"speaker": "recipient", "text": "Done Vikram, see you tomorrow morning."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["fitness trainer personal coordination", "no financial demands", "gym app dashboard tracking"],
        "explanation": "Informal routine fitness trainer workout session reschedule between gym member and personal trainer.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-096 (Ambig 1)
    items.append({
        "conversation_id": "KAV-SYNTH-096",
        "language": "hi-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Bank Anti-Fraud Safety Campaign Warning Against Sharing OTP",
        "dialogue": [
            {"speaker": "caller", "text": "HDFC Bank cyber security awareness unit. Customer safety broadcast message."},
            {"speaker": "recipient", "text": "Hello, mere account mein koi unauthorized access hua hai kya?"},
            {"speaker": "caller", "text": "No sir, your account is completely safe. Yeh ek proactive public advisory hai regarding digital arrest and credit card points fraud."},
            {"speaker": "recipient", "text": "Mujhe kya precautions lene chahiye?"},
            {"speaker": "caller", "text": "Never share your netbanking password, OTP or card CVV on phone calls or WhatsApp links. Bank staff never asks for authentication secrets."},
            {"speaker": "recipient", "text": "Kya mujhe abhi koi confirmation button press karna hai?"},
            {"caller": "caller", "speaker": "caller", "text": "No input is required from your side. Sirf alert rahiye and report any suspicious calls on 1930 portal."},
            {"speaker": "recipient", "text": "Okay, thank you for the security advisory."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["negative context suppression", "security warning containing threat keywords without malicious intent"],
        "explanation": "Bank cybersecurity awareness broadcast advising customers not to share OTPs; contains threat keywords without fraudulent intent.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/hindi_english/kav_synth_096.wav"
    })

    # KAV-SYNTH-097
    items.append({
        "conversation_id": "KAV-SYNTH-097",
        "language": "hi-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "College Friend Requesting Emergency Travel Fare via UPI",
        "dialogue": [
            {"speaker": "caller", "text": "Bhai Rohan, main Aman bol raha hoon, IIT Roorkee wala. Pehchan liya?"},
            {"speaker": "recipient", "text": "Aman! Haan bhai, bohot time baad phone kiya. Kahan hai tu?"},
            {"speaker": "caller", "text": "Bhai main Delhi airport par phansa hua hoon. Mera wallet aur debit card bag ke sath cab mein chhoot gaya hai."},
            {"speaker": "recipient", "text": "Arey teri flight thi kya kahin ki?"},
            {"speaker": "caller", "text": "Haan, Bangalore ki connecting flight hai. Boarding pass nikalna hai par cab driver ka fare pay karne ke liye three thousand rupaye urgently chahiye."},
            {"speaker": "recipient", "text": "Tu cab driver ka Google Pay number bhej de ya apna number bhej."},
            {"caller": "caller", "speaker": "caller", "text": "Mera phone battery low hai bhai, cab driver ke scanner par abhi three thousand transfer kar de na, flight land karte hi return kar dunga."},
            {"speaker": "recipient", "text": "Ruk, main pehle tere room partner Varun ko call karke verify karta hoon fir bhejta hoon."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["distress call from old acquaintance", "unverified emergency upi payment to third-party scanner", "time pressure"],
        "explanation": "Ambiguous emergency borrowing call from college classmate; potential voice impersonation or genuine travel crisis.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-098
    items.append({
        "conversation_id": "KAV-SYNTH-098",
        "language": "hi-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Incomplete Credit Card Dispute Chargeback Call",
        "dialogue": [
            {"speaker": "caller", "text": "Good evening, calling from CitiBank card dispute operations. Am I speaking with Mr. Ankit?"},
            {"speaker": "recipient", "text": "Yes Ankit speaking. Maine ek fraudulent online transaction par chargeback raise kiya tha."},
            {"speaker": "caller", "text": "Yes sir, fourteen thousand rupees transaction on gaming merchant portal. Uska merchant dispute resolution status update hai."},
            {"speaker": "recipient", "text": "Paisa mere account mein kab reverse hoga?"},
            {"speaker": "caller", "text": "Merchant claims the goods were delivered digitally to your registered email. Verification ke liye transaction acknowledgment sign karke bhejna hoga."},
            {"speaker": "recipient", "text": "Maine koi digital goods receive nahi kiye!"},
            {"caller": "caller", "speaker": "caller", "text": "Aap dispute declaration form sign karke dispute@citi.com par mail kijiye with your police complaint copy. Phone par koi sensitive details mat share kijiye."},
            {"speaker": "recipient", "text": "Theek hai, main formal affidavit attach karke bank ke official email par bhej deta hoon."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["contested credit dispute", "chargeback declaration requirement", "refusal of phone credentials"],
        "explanation": "Legitimate banking dispute escalation clarifying documentation requirements for chargeback dispute.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-099
    items.append({
        "conversation_id": "KAV-SYNTH-099",
        "language": "hi-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Real Estate Property Rental Agreement Advance Terms Dispute",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Mr. Gupta, main property consultant Harish baat kar raha hoon from DLF Phase 5 brokerage."},
            {"speaker": "recipient", "text": "Haan Harish ji, apartment rental agreement finalize hua kya landlord ke sath?"},
            {"speaker": "caller", "text": "Landlord agrees on sixty thousand monthly rent, par unka kehna hai ki security deposit two months ke badle three months upfront dena hoga."},
            {"speaker": "recipient", "text": "Pehle toh two months deposit agree hua tha verbally!"},
            {"speaker": "caller", "text": "Society maintenance charges hike hue hain sir. Agreement draft lock karne ke liye unko fifty thousand token money transfer karna padega today."},
            {"speaker": "recipient", "text": "Token money direct landlord ke bank account mein RTGS karunga, aapko nahi."},
            {"caller": "caller", "speaker": "caller", "text": "Bilkul sir, landlord ka account detail lease draft agreement ke sath aayega. Aap lawyer ke presence mein signing par hi pay kijiye."},
            {"speaker": "recipient", "text": "Theek hai, agreement draft bhej dijiye, signing ke waqt hi payment hogi."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["rental lease deposit dispute", "advance token pressure", "lawyer signing protocol offered"],
        "explanation": "Commercial tenancy negotiation with shifting deposit terms; resolved through formal legal execution.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # KAV-SYNTH-100
    items.append({
        "conversation_id": "KAV-SYNTH-100",
        "language": "hi-en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Freelance Web Design Client Scope Clarification & Payment Delay",
        "dialogue": [
            {"speaker": "caller", "text": "Hi Varun, this is Siddharth from FinTech Ventures. Regarding our corporate landing page project."},
            {"speaker": "recipient", "text": "Hi Siddharth, maine final Figma designs deliver kar diye the on Friday."},
            {"speaker": "caller", "text": "Figma design looks clean, but our marketing team wants responsive dark mode and animation effects also included."},
            {"speaker": "recipient", "text": "Dark mode original milestone scope mein included nahi tha. Uske liye extra billing hours lagenge."},
            {"speaker": "caller", "text": "Agar extra budget chahiye toh hamare finance portal par scope amendment form submit kijiye with Revised Invoice."},
            {"speaker": "recipient", "text": "Current milestone ka payment kab release hoga?"},
            {"caller": "caller", "speaker": "caller", "text": "Current milestone fifty thousand approved hai, Friday tak bank transfer ho jayega as per standard net-7 payment cycle."},
            {"speaker": "recipient", "text": "Okay Siddharth, main updated scope document aur invoice email par share kar deta hoon."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["commercial client scope negotiation", "payment delay under standard contract", "formal invoicing required"],
        "explanation": "Routine corporate freelance contract discussion resolving scope expansion and milestone payout schedule.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    return items

