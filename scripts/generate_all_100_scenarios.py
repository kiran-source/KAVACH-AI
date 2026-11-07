# scripts/generate_all_100_scenarios.py
import json
from pathlib import Path

def get_all_100_conversations():
    conversations = []
    
    # -------------------------------------------------------------
    # 1. ENGLISH (20 Conversations: 8 Scam, 7 Legit, 5 Ambig)
    # -------------------------------------------------------------
    
    # KAV-SYNTH-001 (Pilot 1)
    conversations.append({
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

    # KAV-SYNTH-002
    conversations.append({
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

    # KAV-SYNTH-003
    conversations.append({
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
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/english/kav_synth_003.wav"
    })

    # KAV-SYNTH-004
    conversations.append({
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
        "review_status": "pending_review",
        "audio_sample": True,
        "audio_file": "audio/english/kav_synth_004.wav"
    })

    # Return conversations so far
    return conversations

if __name__ == "__main__":
    convos = get_all_100_conversations()
    print(f"Loaded {len(convos)} conversations.")

