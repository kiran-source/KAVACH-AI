import json
import os
from pathlib import Path

DATA_DIR = Path("data/kavach_synthetic_v1")

def build_catalog():
    items = []
    
    # =========================================================================
    # 1. ENGLISH (20 Conversations: 8 Scam, 7 Legit, 5 Ambig)
    # =========================================================================
    # EN-SCAM-01 (Pilot 1)
    items.append({
        "conversation_id": "KAV-SYNTH-001",
        "pilot_id": "KAV-SYNTH-PILOT-001",
        "language": "en",
        "primary_label": "SCAM",
        "scenario": "International Courier Narcotics Seizure & Extortion Scam",
        "dialogue": [
            {"speaker": "caller", "text": "Good afternoon, this is Officer Vikram Rathore from DHL Customs clearance department, Mumbai Cargo terminal."},
            {"speaker": "recipient", "text": "Hello? Why are you calling me? I didn't send any package."},
            {"speaker": "caller", "text": "A consignment containing five fake passports, expired credit cards, and 140 grams of narcotics was booked under your Aadhaar details to Singapore."},
            {"speaker": "recipient", "text": "What? That is completely false! Someone must have stolen my identity."},
            {"speaker": "caller", "text": "The narcotics control bureau has initiated an arrest warrant. To establish your innocence, you must immediately connect to our confidential Skype channel."},
            {"speaker": "recipient", "text": "I will contact my local police station in Bangalore first."},
            {"speaker": "caller", "text": "If you disconnect this call, a police squad will be dispatched to your residence within thirty minutes. You must immediately transfer the verification fee to our RBI clearing account."},
            {"speaker": "recipient", "text": "No, this sounds like extortion. I am hanging up and filing a cybercrime report."}
        ],
        "scam_tactics": ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"],
        "risk_indicators": ["narcotics seizure allegation", "arrest warrant threat", "prohibition on disconnecting call", "unauthorized payment demand"],
        "explanation": "Fraudulent caller poses as customs and police official alleging drug contraband to coerce emergency money transfer under threat of immediate arrest.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/english/kav-synth-pilot-001.wav"
    })

    # EN-SCAM-02
    items.append({
        "conversation_id": "KAV-SYNTH-002",
        "language": "en",
        "primary_label": "SCAM",
        "scenario": "SBI Netbanking Credential Harvesting & KYC Lock Threat",
        "dialogue": [
            {"speaker": "caller", "text": "Good morning sir, I am calling from State Bank of India regulatory compliance cell."},
            {"speaker": "recipient", "text": "Yes, what is the matter?"},
            {"speaker": "caller", "text": "Your savings account KYC documents have expired as per RBI guidelines. Your debit card and UPI will be blocked in two hours."},
            {"speaker": "recipient", "text": "I visited my home branch last month and submitted my PAN card."},
            {"speaker": "caller", "text": "Our central database shows pending digital verification. Please open the SMS link sent to your phone and enter your netbanking username and password."},
            {"speaker": "recipient", "text": "Why should I enter my login password on a link sent via SMS?"},
            {"speaker": "caller", "text": "It is an encrypted portal sir. If you delay, your funds will be frozen and you will face a penalty of five thousand rupees."},
            {"speaker": "recipient", "text": "No legitimate bank asks for passwords over phone or SMS. I will report this number."}
        ],
        "scam_tactics": ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT", "MALICIOUS_LINK_OR_APP", "URGENCY_OR_THREAT"],
        "risk_indicators": ["kyc expiration threat", "netbanking password solicitation", "fake sms link", "financial penalty threat"],
        "explanation": "Impersonates bank compliance officer claiming pending KYC to solicit online banking credentials through a phishing link under threat of account freeze.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/english/kav_synth_002.wav"
    })

    # EN-SCAM-03
    items.append({
        "conversation_id": "KAV-SYNTH-003",
        "language": "en",
        "primary_label": "SCAM",
        "scenario": "Supreme Court Warrant & Continuous Surveillance Threat",
        "dialogue": [
            {"speaker": "caller", "text": "This is Advocate Suresh Menon calling from the Supreme Court e-Courts administrative cell."},
            {"speaker": "recipient", "text": "Supreme Court? Why are you contacting me?"},
            {"speaker": "caller", "text": "A non-bailable arrest warrant has been signed by the bench regarding an unpaid loan fraud committed with your identity credentials."},
            {"speaker": "recipient", "text": "I have never taken any such loan! This must be identity theft."},
            {"speaker": "caller", "text": "To obtain an emergency stay order before police dispatch, you must remain on this line under virtual court custody."},
            {"speaker": "recipient", "text": "I need to call my family lawyer right now."},
            {"speaker": "caller", "text": "Any external call is a violation of judicial secrecy and will trigger immediate seizure of all your family bank accounts."},
            {"speaker": "recipient", "text": "This is completely absurd. Courts do not conduct virtual custody over phone calls. I am hanging up."}
        ],
        "scam_tactics": ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE", "URGENCY_OR_THREAT"],
        "risk_indicators": ["supreme court warrant claim", "virtual custody demand", "isolation from legal counsel", "asset seizure threat"],
        "explanation": "Threatens judicial arrest warrant and asset seizure to coerce emotional isolation and compliance.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-SCAM-04
    items.append({
        "conversation_id": "KAV-SYNTH-004",
        "language": "en",
        "primary_label": "SCAM",
        "scenario": "High-Yield Crypto Trading Telegram Investment Fraud",
        "dialogue": [
            {"speaker": "caller", "text": "Hello madam, I am Priya from Apex Global Wealth Advisory. Are you looking for high return passive income?"},
            {"speaker": "recipient", "text": "Where did you get my contact number?"},
            {"speaker": "caller", "text": "You registered on our financial portal. We are offering exclusive VIP access to an automated algorithmic crypto trading group."},
            {"speaker": "recipient", "text": "I am not interested in cryptocurrency investments."},
            {"speaker": "caller", "text": "Madam, our members earn guaranteed daily returns of thirty percent. You just need to start with an initial deposit of ten thousand rupees."},
            {"speaker": "recipient", "text": "Guaranteed thirty percent daily is mathematically impossible."},
            {"speaker": "caller", "text": "We have SEBI authorized certificates madam. Transfer five thousand right now to our manager's private UPI to lock your introductory slot."},
            {"speaker": "recipient", "text": "SEBI does not authorize private UPI crypto transfers. Please remove me from your list."}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"],
        "risk_indicators": ["guaranteed impossible returns", "private upi transfer solicitation", "fake regulatory authorization", "limited slot urgency"],
        "explanation": "Fraudulent investment scheme promising guaranteed high daily returns and soliciting immediate private UPI transfer.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-SCAM-05
    items.append({
        "conversation_id": "KAV-SYNTH-005",
        "language": "en",
        "primary_label": "SCAM",
        "scenario": "Work-From-Home YouTube Rating Advance Fee Scam",
        "dialogue": [
            {"speaker": "caller", "text": "Hi, I am HR executive Natasha from Global Digital Media Solutions. We saw your resume on Shine.com."},
            {"speaker": "recipient", "text": "Okay, which role is this regarding?"},
            {"speaker": "caller", "text": "Part-time digital rating evaluator. You only need to like and subscribe to travel videos. Daily payout is three thousand rupees."},
            {"speaker": "recipient", "text": "Sounds very easy. How does payment work?"},
            {"speaker": "caller", "text": "We already sent three hundred rupees trial bonus. To activate the VIP payroll gateway, you need to pay a refundable security deposit of two thousand rupees."},
            {"speaker": "recipient", "text": "Why should an employee pay money to start work?"},
            {"caller": "caller", "speaker": "caller", "text": "It is standard company registration compliance. Once you transfer, your account will be activated instantly with your first salary."},
            {"speaker": "recipient", "text": "Legitimate employers never ask for registration fees. This is a task scam."}
        ],
        "scam_tactics": ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"],
        "risk_indicators": ["advance security fee for job", "too good to be true daily payout", "vip payroll activation fee"],
        "explanation": "Employment task scam offering trivial tasks for unrealistic payouts to extort upfront registration fees.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-SCAM-06
    items.append({
        "conversation_id": "KAV-SYNTH-006",
        "language": "en",
        "primary_label": "SCAM",
        "scenario": "Electricity Meter Tampering Penalty Threat & Remote APK",
        "dialogue": [
            {"speaker": "caller", "text": "Alert notice from State Electricity Board. Your smart meter has shown an irregular bypass signal today."},
            {"speaker": "recipient", "text": "Bypass signal? What does that mean?"},
            {"speaker": "caller", "text": "It indicates power theft. A field inspection officer has been assigned to disconnect your line at seven PM tonight."},
            {"speaker": "recipient", "text": "We never touched the meter! It is sealed by the board."},
            {"speaker": "caller", "text": "You can resolve it by installing our diagnostic app from this direct link to submit your digital meter photograph."},
            {"speaker": "recipient", "text": "Can I submit the photo on the official utility website?"},
            {"speaker": "caller", "text": "No, web server is under maintenance. If you don't install the APK within twenty minutes, line will be disconnected."},
            {"speaker": "recipient", "text": "Installing unknown APK files gives remote control. I will contact the substation manager directly."}
        ],
        "scam_tactics": ["REMOTE_ACCESS_MANIPULATION", "MALICIOUS_LINK_OR_APP", "URGENCY_OR_THREAT", "AUTHORITY_IMPERSONATION"],
        "risk_indicators": ["immediate power cut threat", "demand to install apk from link", "fake server maintenance excuse"],
        "explanation": "Impersonates electricity utility alleging meter bypass to force installation of remote access APK.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-SCAM-07
    items.append({
        "conversation_id": "KAV-SYNTH-007",
        "language": "en",
        "primary_label": "SCAM",
        "scenario": "Income Tax Refund Notice with Debit Card CVV Solicitation",
        "dialogue": [
            {"speaker": "caller", "text": "Hello, I am calling from the Central Board of Direct Taxes refund processing division."},
            {"speaker": "recipient", "text": "Yes, I was waiting for my assessment refund."},
            {"speaker": "caller", "text": "Your tax refund of thirty-four thousand rupees was processed, but the electronic mandate failed due to an outdated IFSC code."},
            {"speaker": "recipient", "text": "I can update my bank details on the e-filing portal."},
            {"speaker": "caller", "text": "Portal changes take ninety days. We can credit the amount directly to your debit card within ten minutes over our direct gateway."},
            {"speaker": "recipient", "text": "How do you credit to a debit card?"},
            {"speaker": "caller", "text": "Please provide your sixteen digit card number, expiry date, and three digit CVV code on the back for authentication."},
            {"speaker": "recipient", "text": "CVV is only used for payments, never for receiving refunds. You are trying to steal my card details."}
        ],
        "scam_tactics": ["OTP_PIN_CVV_THEFT", "AUTHORITY_IMPERSONATION", "ACCOUNT_OR_KYC_THREAT"],
        "risk_indicators": ["income tax refund lure", "debit card cvv demand", "false claim that cvv is needed for refund"],
        "explanation": "Impersonates tax department offering fast-track refund to harvest card credentials and CVV.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-SCAM-08
    items.append({
        "conversation_id": "KAV-SYNTH-008",
        "language": "en",
        "primary_label": "SCAM",
        "scenario": "Telecom Authority SIM Card Block Threat & Verification Charge",
        "dialogue": [
            {"speaker": "caller", "text": "Automated notification from Department of Telecommunications. All services on your primary mobile number will be terminated within two hours."},
            {"speaker": "recipient", "text": "Terminated? What is the reason?"},
            {"speaker": "caller", "text": "Thirteen complaints of harassment and illegal financial SMS broadcasting have been lodged against this SIM card in New Delhi."},
            {"speaker": "recipient", "text": "I live in Chennai! I have never sent any illegal SMS."},
            {"speaker": "caller", "text": "Your Aadhaar has been duplicated. To prevent a permanent national telecom blacklist, pay a security bond of nine thousand rupees via UPI."},
            {"speaker": "recipient", "text": "Why should I pay a security bond to stop telecom disconnection?"},
            {"speaker": "caller", "text": "This is refundable bail money sir. If you refuse, telecom enforcement and Delhi police will arrest you tomorrow."},
            {"speaker": "recipient", "text": "DoT never collects bail money via UPI. I am lodging an official fraud complaint on Chakshu portal."}
        ],
        "scam_tactics": ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"],
        "risk_indicators": ["telecom authority impersonation", "sim termination urgency", "refundable bail payment via upi"],
        "explanation": "Impersonates telecom ministry threatening national SIM cancellation and arrest to coerce UPI payment.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-LEGIT-01
    items.append({
        "conversation_id": "KAV-SYNTH-009",
        "language": "en",
        "primary_label": "LEGITIMATE",
        "scenario": "Broadband Internet Plan Speed Upgrade Confirmation",
        "dialogue": [
            {"speaker": "caller", "text": "Good afternoon, calling from ACT Fibernet customer relationship desk. Am I speaking with Mr. Arvind?"},
            {"speaker": "recipient", "text": "Yes, Arvind speaking. How can I help you?"},
            {"speaker": "caller", "text": "We noticed your fiber connection has completed two years. We have an annual loyalty upgrade offering two hundred megabits per second at your current bill amount."},
            {"speaker": "recipient", "text": "Will there be any hidden installation or router charges?"},
            {"speaker": "caller", "text": "No extra charges sir. Your existing dual-band router supports this speed automatically. It simply updates your profile on your next billing cycle."},
            {"speaker": "recipient", "text": "That sounds great. Do I need to fill out any form?"},
            {"speaker": "caller", "text": "No forms or documents needed. I have updated your account request. You will receive an official confirmation SMS on your registered number."},
            {"speaker": "recipient", "text": "Thank you for the prompt assistance."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["no credential solicitation", "transparent loyalty offer", "official sms confirmation without link"],
        "explanation": "Routine customer loyalty call from internet service provider confirming plan speed upgrade with zero financial or credential requests.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/english/kav_synth_009.wav"
    })
    items.append({
        "conversation_id": "KAV-SYNTH-010",
        "language": "en",
        "primary_label": "LEGITIMATE",
        "scenario": "Diagnostic Laboratory Blood Test Appointment Booking",
        "dialogue": [
            {"speaker": "caller", "text": "Good morning, this is Priya from SRL Diagnostics customer care. I am following up on your online health checkup booking."},
            {"speaker": "recipient", "text": "Yes, I booked a home sample collection for tomorrow morning."},
            {"speaker": "caller", "text": "Our phlebotomist Ramesh will visit your residence between seven thirty and eight AM. Please ensure ten hours of fasting before the test."},
            {"speaker": "recipient", "text": "Understood. Can I drink water during fasting?"},
            {"speaker": "caller", "text": "Plain water is perfectly fine sir. How would you prefer to receive the test results?"},
            {"speaker": "recipient", "text": "Please send the soft copy report to my registered email address."},
            {"speaker": "caller", "text": "Sure, your reports will be emailed within twenty-four hours. You can pay the standard fee directly to the technician by cash or card upon arrival."},
            {"speaker": "recipient", "text": "Perfect, thank you for confirming."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["standard medical appointment", "transparent payment upon arrival", "medical preparation instructions"],
        "explanation": "Legitimate diagnostic healthcare appointment confirmation with routine medical fasting instructions and safe on-site payment.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-LEGIT-03
    items.append({
        "conversation_id": "KAV-SYNTH-011",
        "language": "en",
        "primary_label": "LEGITIMATE",
        "scenario": "Airline Flight Delay Rescheduling Assistance",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Mr. Sen, this is IndiGo special assistance desk regarding your flight 6E-204 from Delhi to Mumbai tomorrow."},
            {"speaker": "recipient", "text": "Yes, is there any schedule change?"},
            {"speaker": "caller", "text": "Due to runway maintenance at Mumbai airport, your departure time has been moved from two PM to four fifteen PM."},
            {"speaker": "recipient", "text": "That might affect my evening meeting. Are there earlier options available?"},
            {"speaker": "caller", "text": "Yes sir, we have a flight departing at eleven thirty AM with available seats. We can transfer you at zero rescheduling charge."},
            {"speaker": "recipient", "text": "Eleven thirty AM works much better for me. Please change it to that flight."},
            {"speaker": "caller", "text": "Done sir. Your new boarding pass has been issued and sent to your airline mobile app and registered email."},
            {"speaker": "recipient", "text": "Thank you so much for the proactive assistance."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["official airline reschedule", "no fee charged", "official app confirmation"],
        "explanation": "Authentic airline operations desk assisting passenger with flight reschedule at zero charge.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-LEGIT-04
    items.append({
        "conversation_id": "KAV-SYNTH-012",
        "language": "en",
        "primary_label": "LEGITIMATE",
        "scenario": "Life Insurance Annual Policy Renewal Reminder",
        "dialogue": [
            {"speaker": "caller", "text": "Good day, calling from HDFC Life Insurance service desk. Am I speaking with Mrs. Mehra?"},
            {"speaker": "recipient", "text": "Yes speaking. What is this regarding?"},
            {"speaker": "caller", "text": "This is a courtesy reminder that your Click 2 Protect life insurance policy annual premium is due on the twenty-fifth of this month."},
            {"speaker": "recipient", "text": "Right, I remember. Can I pay it through netbanking?"},
            {"speaker": "caller", "text": "Yes madam, you can log in directly to our official portal at hdfclife.com or use your bank auto-debit facility."},
            {"speaker": "recipient", "text": "Is there any change in the premium amount this year?"},
            {"speaker": "caller", "text": "No change madam, it remains exactly the same as last year. We advise customers to never share policy login OTPs with anyone over the phone."},
            {"speaker": "recipient", "text": "Thank you for the security advice. I will pay it on the official portal tonight."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["proactive anti-fraud warning", "direction to official website", "standard insurance renewal notice"],
        "explanation": "Legitimate insurance premium reminder that includes standard anti-phishing warnings directing customer to official portal.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-LEGIT-05
    items.append({
        "conversation_id": "KAV-SYNTH-013",
        "language": "en",
        "primary_label": "LEGITIMATE",
        "scenario": "Bank Credit Card International Roaming Activation",
        "dialogue": [
            {"speaker": "caller", "text": "Good afternoon, calling from ICICI Bank credit card customer support. Am I speaking with Dr. Nair?"},
            {"speaker": "recipient", "text": "Yes, I requested international usage enablement on my card yesterday."},
            {"speaker": "caller", "text": "I am confirming your service request for your upcoming travel to the United Kingdom from tenth to twenty-fifth."},
            {"speaker": "recipient", "text": "Yes, that is accurate. Will contactless chip transactions work at London terminals?"},
            {"speaker": "caller", "text": "Yes sir, international contactless and POS limits are now activated as per your requested ten day window."},
            {"speaker": "recipient", "text": "Do you need my card details to finalize the activation?"},
            {"speaker": "caller", "text": "No sir, we never ask for your card number, CVV or OTP. Your request was already authenticated via your mobile banking app."},
            {"speaker": "recipient", "text": "Excellent, thank you for confirming."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["explicit refusal of sensitive credentials", "authentication verified via official app", "service confirmation"],
        "explanation": "Legitimate bank travel service follow-up confirming international card settings while explicitly refusing sensitive credentials.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-LEGIT-06
    items.append({
        "conversation_id": "KAV-SYNTH-014",
        "language": "en",
        "primary_label": "LEGITIMATE",
        "scenario": "Laptop Service Center Repair Status Update",
        "dialogue": [
            {"speaker": "caller", "text": "Hello, calling from Dell Authorized Service Center, Koramangala. Is this Mr. Joseph?"},
            {"speaker": "recipient", "text": "Yes, I dropped off my XPS laptop yesterday for display diagnostic."},
            {"speaker": "caller", "text": "Our hardware team inspected the unit. The display cable had come loose, but the LCD panel is completely undamaged."},
            {"speaker": "recipient", "text": "Oh, that is a relief! Will it be covered under my active warranty?"},
            {"speaker": "caller", "text": "Yes sir, it is fully covered under your accidental damage protection. There is zero service charge."},
            {"speaker": "recipient", "text": "When will it be ready for pickup?"},
            {"caller": "caller", "speaker": "caller", "text": "The laptop has passed quality calibration and is ready at the front desk. Please bring your job sheet acknowledgment slip when visiting."},
            {"speaker": "recipient", "text": "I will drop by this evening. Thank you."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["warranty coverage confirmation", "zero service charge", "physical pickup verification"],
        "explanation": "Authentic computer repair center providing diagnostic status under active warranty with zero charge.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-LEGIT-07
    items.append({
        "conversation_id": "KAV-SYNTH-015",
        "language": "en",
        "primary_label": "LEGITIMATE",
        "scenario": "University Alumni Meetup Registration Confirmation",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Ananya, this is Divya from the BITS Pilani Alumni Relations office."},
            {"speaker": "recipient", "text": "Hi Divya, nice to hear from the alumni team!"},
            {"speaker": "caller", "text": "Calling to confirm your attendance for the Bangalore chapter annual reunion next Saturday at five PM."},
            {"speaker": "recipient", "text": "Yes, I registered on the alumni portal last week."},
            {"speaker": "caller", "text": "Great! Entry badge will be available at the registration desk. Dinner is sponsored by the association."},
            {"speaker": "recipient", "text": "Are plus ones permitted for the dinner session?"},
            {"speaker": "caller", "text": "Yes, spouses are welcome. You can add guest details on the official alumni website anytime before Thursday."},
            {"speaker": "recipient", "text": "Wonderful, looking forward to meeting everyone."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["college alumni coordination", "no financial solicitation", "official website self-service"],
        "explanation": "Benign educational alumni event coordination confirming meetup attendance with zero commercial solicitation.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-AMBIG-01
    items.append({
        "conversation_id": "KAV-SYNTH-016",
        "language": "en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Bank Security Advisory on Phishing Links (Negative Context)",
        "dialogue": [
            {"speaker": "caller", "text": "Important advisory from Axis Bank security operations. This is an informational customer announcement."},
            {"speaker": "recipient", "text": "Has there been any fraudulent attempt on my account?"},
            {"speaker": "caller", "text": "No sir, your account is secure. We are informing all customers regarding fake APK links and lottery fraud SMS."},
            {"speaker": "recipient", "text": "What precautions should I take?"},
            {"speaker": "caller", "text": "Never enter your OTP, password or debit card CVV on any link sent via SMS or WhatsApp, even if the sender claims to be a bank officer."},
            {"speaker": "recipient", "text": "Do you need me to verify any security questions?"},
            {"speaker": "caller", "text": "No verification is required. This is purely an advisory notification. Stay vigilant against cybercrime."},
            {"speaker": "recipient", "text": "Thank you for the security advisory."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["negative context suppression", "security advisory containing threat keywords without scam intent"],
        "explanation": "Bank cybersecurity awareness advisory warning against phishing links; contains threat keywords without fraudulent coercion.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/english/kav_synth_016.wav"
    })

    # EN-AMBIG-02
    items.append({
        "conversation_id": "KAV-SYNTH-017",
        "language": "en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Emergency Hospital Admission Inquiry from Unknown Number",
        "dialogue": [
            {"speaker": "caller", "text": "Hello? Is this Rajesh? I am calling from Apollo Hospital casualty reception."},
            {"speaker": "recipient", "text": "Yes, who is this? Why are you calling from the hospital?"},
            {"speaker": "caller", "text": "A person named Mr. K. Sharma was admitted after a road accident near Silk Board. Your contact number was listed in his emergency diary."},
            {"speaker": "recipient", "text": "Mr. Sharma? My former colleague! How is he now?"},
            {"speaker": "caller", "text": "He is conscious but needs emergency CT scanning. The billing desk needs someone to sign the guardian admission consent."},
            {"speaker": "recipient", "text": "Do you need me to transfer any admission deposit right now?"},
            {"speaker": "caller", "text": "We cannot accept remote payments over phone. Please reach the hospital emergency ward immediately with his identity copy."},
            {"speaker": "recipient", "text": "I am on my way to the hospital right now."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["high emotional urgency", "medical emergency context", "refusal of remote payments"],
        "explanation": "High-urgency medical emergency situation from an unverified caller, but caller explicitly refuses remote financial transfers.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-AMBIG-03
    items.append({
        "conversation_id": "KAV-SYNTH-018",
        "language": "en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Property Maintenance Dues Notice with Unverified Payment Portal",
        "dialogue": [
            {"speaker": "caller", "text": "Good evening, calling from Prestige Falcon Ridge Residents Association management committee."},
            {"speaker": "recipient", "text": "Hello, is this regarding the quarterly maintenance?"},
            {"speaker": "caller", "text": "Yes sir. The audited accounts show an outstanding water surcharge of three thousand rupees against Flat 402."},
            {"speaker": "recipient", "text": "I already cleared the full annual society dues in April via MyGate app."},
            {"speaker": "caller", "text": "The committee migrated to a new billing vendor last month. We have sent a direct payment link on your mobile."},
            {"speaker": "recipient", "text": "I will not click any unverified link. Why was this not announced in the resident AGM?"},
            {"speaker": "caller", "text": "It was discussed in the circular. You may also pay by cheque directly to the estate office on Monday."},
            {"speaker": "recipient", "text": "I will drop by the estate office in person on Monday with my receipt."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["unverified billing link", "contested dues", "alternative physical resolution offered"],
        "explanation": "Ambiguous residential association billing dispute involving an unverified payment link, but with legitimate offline cheque option provided.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-AMBIG-04
    items.append({
        "conversation_id": "KAV-SYNTH-019",
        "language": "en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Credit Score Improvement Consultation Inquiry",
        "dialogue": [
            {"speaker": "caller", "text": "Hello Mr. Das, I am calling from CreditKarma Financial Advisory services."},
            {"speaker": "recipient", "text": "Yes, what service are you offering?"},
            {"speaker": "caller", "text": "We offer credit score restoration for customers whose CIBIL score is below seven hundred due to past loan settlement remarks."},
            {"speaker": "recipient", "text": "How do you improve a CIBIL score? Can you remove settlement flags?"},
            {"caller": "caller", "speaker": "caller", "text": "We file legal representation with credit bureaus under the Fair Credit Reporting framework to dispute inaccurate negative entries."},
            {"speaker": "recipient", "text": "Do you need any banking passwords or advance fees?"},
            {"speaker": "caller", "text": "We only charge a consultancy retainer of twelve hundred rupees after sending you a preliminary legal assessment report."},
            {"speaker": "recipient", "text": "Send the assessment details to my email first. I will verify your company credentials before deciding."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["credit repair fee consultation", "unsolicited financial marketing", "no credential solicitation"],
        "explanation": "Aggressive financial credit restoration marketing call; borderline legitimacy requiring caution but lacking explicit coercion or credential theft.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    # EN-AMBIG-05
    items.append({
        "conversation_id": "KAV-SYNTH-020",
        "language": "en",
        "primary_label": "AMBIGUOUS",
        "scenario": "Pre-Approved Personal Loan Offer with Incomplete Verification",
        "dialogue": [
            {"speaker": "caller", "text": "Congratulations sir, you have been shortlisted for an instant pre-approved personal loan of five lakh rupees from Bajaj Finserv."},
            {"speaker": "recipient", "text": "I did not apply for any personal loan."},
            {"speaker": "caller", "text": "It is based on your healthy banking transactions. Interest rate is only nine point five percent with zero documentation."},
            {"speaker": "recipient", "text": "Nine point five percent for personal loan is unusually low. What are the terms?"},
            {"speaker": "caller", "text": "We just need your verbal confirmation to generate the e-mandate agreement letter."},
            {"speaker": "recipient", "text": "Do you need my debit card or netbanking details?"},
            {"speaker": "caller", "text": "Our backend executive will call you tomorrow for formal verification. No passwords will be requested."},
            {"speaker": "recipient", "text": "Do not generate any agreement without sending the terms and conditions to my email first."}
        ],
        "scam_tactics": ["NONE"],
        "risk_indicators": ["pre-approved loan telemarketing", "promotional interest rate", "incomplete verification details"],
        "explanation": "High-pressure unsolicited loan marketing with incomplete details; requires verification against official channels.",
        "synthetic_source": "KAVACH-AI Domain-Curated Dataset Engine",
        "generation_model": "domain-curated-expert-v1",
        "review_status": "pending_review"
    })

    return items

if __name__ == "__main__":
    catalog = build_catalog()
    print(f"Built {len(catalog)} English conversations.")
