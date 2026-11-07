"""
Generator for SCAM_DATA in KAVACH AI Synthetic Dataset v3.
Constructs 200 distinct, diverse SCAM scenario families across 17 categories.
"""

import json
from pathlib import Path

SCAM_CATEGORIES = [
    # 1. Digital Arrest & Fake Judiciary (18)
    ("DIGITAL_ARREST", 18, [
        ("CBI Headquarters New Delhi", "DSP Rakesh Asthana", "4.8 crore illegal Hawala laundering under Aadhaar", "Immediate non-bailable arrest warrant from Delhi High Court", "Transfer funds to RBI asset security clearing account", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"]),
        ("Supreme Court Judicial Cell", "Advocate Sanjay Mishra", "Contempt of court citation for non-appearance in money laundering case", "Immovable property sealing order execution", "Immediate bail deposit into court escrow portal", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"]),
        ("Enforcement Directorate Special Cell", "Assistant Director Vikram Solanki", "Unreported foreign currency transactions exceeding $65,000", "Freezing of all family bank accounts under PMLA Act", "Transfer to ED statutory verification vault", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("Mumbai Cyber Crime Special Branch", "Inspector Pradeep Sawant", "SIM card linked to Aadhaar found routing illegal offshore gambling funds", "Police remand team dispatched to current GPS coordinates", "Join continuous confidential Skype video surveillance", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),
        ("Delhi Police Special Cell", "Sub-Inspector Alok Varma", "Identity theft syndicate using your credentials for hawala routing", "Non-bailable digital custody detention order", "Deposit sovereign bond security to clear financial record", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("Telangana Cyber Crime Directorate", "ACP K. Srinivas Rao", "Aadhaar misuse in multi-crore investment scam operating in Hyderabad", "Immediate extradition warrant and bank account freeze", "Submit financial ledger to secure RBI clearing custody", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"]),
        ("Kolkata Police Cyber Police Station", "Inspector Debasish Roy", "Seizure of illicit SIM bank operating in Salt Lake under your Aadhaar", "Arrest warrant issuance by Chief Metropolitan Magistrate", "Transfer clearance guarantee to state treasury account", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("National Investigation Agency Liaison", "Inspector Amit Deshmukh", "Financial transaction flagged under terror financing surveillance", "Immediate national travel ban and physical detainment", "Provide comprehensive financial declaration and verification fee", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"]),
        ("Gujarat Crime Branch Cyber Cell", "DySP Hasmukh Patel", "Aadhaar number associated with illegal betting ring transaction", "Impounding of vehicle and residential property attachment", "Authorize instant asset verification transfer", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("Bangalore Central Crime Branch", "Inspector Harish Gowda", "Corporate identity fraud involving overseas illicit transfers", "Non-bailable warrant served to local police station", "Initiate immediate security clearance via RBI escrow", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"]),
        ("TRAI High Level Vigilance", "Officer Manoj Kulkarni", "SIM card sending 15,000 illegal phishing messages across country", "Immediate permanent blacklisting of all telecom services", "Verify Aadhaar on encrypted video call or face arrest", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "ACCOUNT_OR_KYC_THREAT"]),
        ("NCB Narcotics Control Bureau", "Zonal Director Rajesh Kaul", "Courier seized at courier cargo terminal with synthetic narcotics and your ID", "Narcotic Drugs and Psychotropic Substances Act detention", "Pay provisional customs exoneration fine", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "COURIER_CUSTOMS_FRAUD"]),
        ("Chennai Cyber Crime Cell", "Inspector R. Senthil", "Aadhaar card used in unauthorized overseas money transfer syndicate", "Immediate digital arrest and non-bailable custody", "Clear legal liability through government security deposit", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("Punjab Police Cyber Wing", "Inspector Gurpreet Singh", "Money laundering network operating through dummy accounts in your name", "State-level lookout circular issued at all airports", "Transfer surety bond to verified nodal account", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"]),
        ("Rajasthan Anti-Corruption Bureau", "Officer Surendra Rathore", "Government tender fraud kickback traced to your PAN card", "Vigilance raid scheduled at your residence within two hours", "Lodge immediate affidavit with electronic verification fee", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("Kerala Police Cyberdome", "Sub-Inspector Varghese Mathew", "Suspect financial communication detected across international border", "Immediate summons under Section 41A with arrest clause", "Verify net banking credentials via secure portal", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "OTP_PIN_CVV_THEFT"]),
        ("Madhya Pradesh Cyber Cell", "Inspector Vijay Chouhan", "Fraudulent call center raid discovered your identity documents", "Inclusion of name in primary FIR charge sheet", "Deposit temporary clearance security fund", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("Lucknow Cyber Crime Headquarters", "DSP Akhilesh Pandey", "High-value suspicious transactions violating RBI foreign exchange rules", "Immediate bank account freezing order by magistrate", "Execute swift sovereign clearance verification", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"])
    ]),
    
    # 2. Fake Law Enforcement & Police (15)
    ("FAKE_LAW_ENFORCEMENT", 15, [
        ("Delhi Cyber Police Station", "Sub-Inspector Sandeep Kumar", "IP address used to launch cyber attack on municipal servers", "Filing of non-bailable FIR 712/2026", "Provide remote device access for forensic inspection", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "REMOTE_ACCESS_MANIPULATION"]),
        ("Mumbai Crime Branch Unit 9", "Officer Santosh Jadhav", "Vehicle registered in your name involved in hit-and-run incident", "Impounding of vehicle and arrest of owner", "Pay spot settlement fine to police welfare trust", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
        ("Hyderabad Cyber Cell", "Inspector B. Madhusudhan", "Defamation complaint filed by political entity regarding social posts", "Immediate arrest summons to Begumpet police station", "Settle out-of-court administrative charge", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
        ("Income Tax Central Circle", "Commissioner R. K. Saxena", "Undisclosed gold jewelry and cash purchases exceeding 25 lakhs", "Tax evasion raid and bank locker attachment", "Immediate advance tax penalty deposit", ["AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Customs Air Cargo Clearance", "Superintendent George Verghese", "Undervalued electronic consignment held at Chennai airport", "Seizure and penalty under Customs Act 1962", "Transfer customs duties to official clearing agent account", ["AUTHORITY_IMPERSONATION", "COURIER_CUSTOMS_FRAUD", "FINANCIAL_REDIRECTION"]),
        ("Railway Protection Force", "Inspector D. K. Sharma", "Unauthorized commercial goods transportation on passenger ticket", "Confiscation of luggage and court prosecution", "Clear demurrage fine via instant UPI", ["AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("CBI Economic Offences Wing", "Officer Naveen Chawla", "Dummy firm registered using forged Aadhaar card for GST input credit fraud", "Immediate summons with potential detention", "Transfer audit clearance deposit", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
        ("Cyber Crime Cell Pune", "Inspector Yogesh More", "Obscene video call complaint registered against your phone number", "Public registry listing on sex offender portal", "Pay case expungement fee to police fund", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),
        ("Jaipur Police Commissionerate", "Sub-Inspector Kuldeep Bhati", "Stolen mobile phone IMEI traced using your secondary SIM", "Confiscation of device and criminal complaint", "Verify identity via instant digital bond", ["AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("Chandigarh Police Traffic Cell", "Sub-Inspector Ravinder Mann", "Multiple speed limit violations and pending court e-challan warrant", "License suspension and arrest warrant", "Pay overdue fine via provided third-party link", ["AUTHORITY_IMPERSONATION", "MALICIOUS_LINK_OR_APP", "URGENCY_OR_THREAT"]),
        ("Assam Police CID Cyber Wing", "Inspector Biswajit Das", "Unregistered transnational internet telephony call gateway usage", "Prosecution under Indian Telegraph Act", "Pay departmental compounding fee", ["AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("Goa Police Special Branch", "Inspector Anthony D'Souza", "Unregistered tourist villa rental financial dispute", "Magistrate notice and court summons", "Deposit arbitration settlement token", ["AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("Bhopal Crime Investigation Cell", "Officer Prakash Tiwari", "Suspicious transaction recorded during municipal election monitoring", "Election commission vigilance inquiry", "Provide comprehensive financial declaration code", ["AUTHORITY_IMPERSONATION", "OTP_PIN_CVV_THEFT"]),
        ("Surat Cyber Crime Cell", "Inspector Chetan Desai", "Cryptocurrency transaction traced to illegal diamond Hawala", "Direct freezing of bank accounts", "Provide exchange login credentials for audit", ["AUTHORITY_IMPERSONATION", "OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("Patna Cyber Cell", "Officer Shailesh Upadhyay", "Fake job portal operating using your residential WiFi connection", "Seizure of router and computer equipment", "Pay provisional clearance penalty", ["AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"])
    ]),

    # 3. Banking Fraud & Reversal (18)
    ("BANKING_FRAUD", 18, [
        ("SBI Fraud Monitoring Cell", "Executive Arvind Narang", "Suspicious transaction of 85,000 rupees initiated from unknown IP", "Immediate debit from savings account within 10 minutes", "Transfer funds to reserve safe vault account for protection", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT", "AUTHORITY_IMPERSONATION"]),
        ("HDFC Bank Card Services", "Manager Rajiv Sen", "International e-commerce transaction of $420 pending authorization", "Permanent charge to credit card balance", "Share 16-digit card number and OTP to cancel payment", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT", "URGENCY_OR_THREAT"]),
        ("ICICI Bank NetBanking Cell", "Officer Ananya Gupta", "Dual login attempt detected on your net banking portal from Russia", "Total compromise of bank deposits", "Confirm net banking password and OTP to freeze access", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT", "ACCOUNT_OR_KYC_THREAT"]),
        ("Axis Bank Dispute Unit", "Executive Rohit Singhal", "Erroneous credit of 45,000 rupees deposited into your savings account", "Legal notice for wrongful enrichment and asset freezing", "Reverse the amount immediately via UPI to provided VPA", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Punjab National Bank Support", "Officer Baldev Raj", "Cheque clearing error resulting in negative account balance penalty", "Cheque bounce criminal case under Section 138", "Transfer clearing penalty of 2,500 rupees", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
        ("Bank of Baroda Security Cell", "Officer Manoj Joshi", "Debit card magnetic strip damaged and requiring security reactivation", "Permanent card block tonight at 12 midnight", "Verify 4-digit ATM PIN and expiry date", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("Canara Bank Operations", "Executive K. V. Swamy", "Dormant account annual maintenance fee waiver opportunity", "Closure of account and transfer to unclaimed deposits", "Perform 1-rupee test debit with full credentials", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("Kotak Mahindra Bank Care", "Manager Vivek Oberoi", "Reward points worth 12,000 rupees expiring within 48 hours", "Forfeiture of cash equivalent rewards", "Enter credit card details and OTP on redemption link", ["MALICIOUS_LINK_OR_APP", "OTP_PIN_CVV_THEFT"]),
        ("IndusInd Bank Digital Desk", "Officer Shalini Kapoor", "Credit card limit increase from 1.5 lakhs to 5 lakhs pre-approved", "Lapse of complimentary credit limit offer", "Provide OTP received for limit enhancement", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("Federal Bank Card Division", "Executive George Thomas", "Unauthorized recurring subscription charge of 6,999 on debit card", "Recurring monthly deduction starting today", "Share CVV and cancellation OTP to revoke subscription", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Union Bank of India Support", "Officer Harish Chandra", "System upgrade requires mandatory debit card re-registration", "Block on ATM and online transactions", "Provide 16-digit card number and CVV", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("IDFC First Bank Card Cell", "Executive Sameer Khan", "Airport lounge access activation on credit card requires card re-authentication", "Loss of lifetime free lounge privilege", "Enter OTP sent to mobile for complimentary enrollment", ["OTP_PIN_CVV_THEFT"]),
        ("Standard Chartered Desk", "Officer David Miller", "International wire transfer held due to intermediary compliance code", "Cancellation and forfeiture of remittance funds", "Pay wire release tax via UPI immediately", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("RBL Bank Card Division", "Executive Shruti Nair", "Cashback of 4,500 rupees pending credit on recent retail swipe", "Cashback forfeiture within 24 hours", "Download reward APK app to claim cashback balance", ["MALICIOUS_LINK_OR_APP", "OTP_PIN_CVV_THEFT"]),
        ("Yes Bank Security Team", "Manager Tarun Bedi", "High-risk Merchant transaction attempted on international portal", "Permanent credit card blocking and replacement fee", "Verify cardholder identity by reciting SMS verification code", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Central Bank of India Care", "Officer Rameshwar Dayal", "Passbook printing and SMS alert service fee overdue", "Suspension of mobile banking alerts", "Transfer 150 rupees via payment link to reactivate alerts", ["MALICIOUS_LINK_OR_APP", "FINANCIAL_REDIRECTION"]),
        ("Indian Overseas Bank Helpdesk", "Officer Murugan", "Annual interest payout credited but held in suspense account", "Return of interest to central pool", "Verify savings account number and mobile OTP", ["OTP_PIN_CVV_THEFT"]),
        ("Bank of India Vigilance", "Inspector S. K. Pathak", "Card cloning attempt detected at outdoor highway ATM", "Immediate siphon of total account balance", "Move funds to temporary emergency escrow account", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"])
    ]),

    # 4. UPI & QR Fraud (18)
    ("UPI_FRAUD", 18, [
        ("PhonePe Merchant Desk", "Executive Rahul Verma", "Cashback coupon reward of 2,850 rupees won on grocery transaction", "Coupon expiration in 15 minutes", "Accept UPI collect request and enter UPI PIN to receive money", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
        ("Google Pay Rewards Cell", "Supervisor Aman Saxena", "Scratch card festival prize worth 5,000 rupees ready for credit", "Prize returned to merchant pool", "Scan QR code sent on WhatsApp and enter PIN", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
        ("Paytm Customer Care", "Executive Neha Sharma", "Paytm wallet KYC expired leading to pending cashback release", "Total freeze of wallet balance of 3,200", "Approve 1-rupee verification payment through custom UPI link", ["MALICIOUS_LINK_OR_APP", "ACCOUNT_OR_KYC_THREAT"]),
        ("OLX Buyer Representative", "Buyer Vikramaditya Singh", "Advance token payment for second-hand furniture listed online", "Cancellation of purchase order", "Scan QR code to receive advance payment directly into bank", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
        ("Zomato Delivery Refund", "Support Agent Imran", "Refund of 680 rupees for cancelled food order stuck in transit", "Forfeiture of order refund", "Click link to receive instant refund via Google Pay collect request", ["MALICIOUS_LINK_OR_APP", "OTP_PIN_CVV_THEFT"]),
        ("Swiggy Instamart Support", "Agent Karan Patel", "Double debit on grocery delivery order requiring instant reversal", "Long wait for 7-day bank statement refund", "Approve merchant refund request on PhonePe with PIN", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
        ("Amazon Pay Helpdesk", "Executive Divya Nair", "Gift voucher balance of 1,500 rupees expiring today", "Voucher balance lapse", "Enter UPI PIN on payment screen to claim cashback voucher", ["OTP_PIN_CVV_THEFT"]),
        ("Bhim UPI Support", "Officer Alok Ranjan", "Inter-bank UPI transaction pending settlement from morning", "Transaction failure and penalty debit", "Share 6-digit MPIN over call for manual reconciliation", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Uber Driver Payment Cell", "Executive Santosh Yadav", "Extra fare overcharged on cab ride refund processing", "Loss of travel fare compensation", "Scan driver refund QR code using phone camera", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
        ("Rapido Ride Refund Support", "Agent Manoj", "Helmet charge deducted erroneously on two-wheeler ride", "Fare refund lapse", "Enter UPI PIN to approve reverse credit into wallet", ["OTP_PIN_CVV_THEFT"]),
        ("Cred Cash Support", "Executive Priya Sen", "Pre-approved cashback of 3,750 on credit card bill payment", "Cashback allocation expiry", "Approve instant collect notification in UPI app", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
        ("Flipkart SuperCoin Desk", "Agent Rajesh", "SuperCoins converted to 2,000 rupees cash balance", "Conversion points lapse", "Scan barcode sent via SMS to transfer cash", ["MALICIOUS_LINK_OR_APP", "OTP_PIN_CVV_THEFT"]),
        ("BookMyShow Refund Helpdesk", "Agent Tanvi", "Movie show cancellation refund of 950 rupees pending approval", "Ticket refund non-refundable after 1 hour", "Click WhatsApp link and enter UPI PIN", ["MALICIOUS_LINK_OR_APP", "OTP_PIN_CVV_THEFT"]),
        ("MakeMyTrip Flight Support", "Executive Varun", "Airfare refund for cancelled flight requiring immediate UPI authorization", "Ticket cancellation fee forfeiture", "Enter UPI PIN on reversal collect screen", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Electricity Board Refund Desk", "Officer Suresh", "Overpaid power bill subsidy credit of 1,200 rupees ready", "Subsidy lapse to state revenue", "Accept UPI collect request in Google Pay", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
        ("Petrol Pump QR Refund Desk", "Manager Ravi", "Double payment debited at fuel pump terminal", "Delayed bank dispute process", "Scan payment terminal refund barcode with UPI app", ["OTP_PIN_CVV_THEFT"]),
        ("IRCTC UPI Payment Desk", "Helpdesk Agent Sunita", "Failed tatkal ticket reservation refund authorization", "Ticket refund cancellation", "Approve transaction collect request in Bhim app", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("DTH Recharge Cashback Cell", "Executive Deepak", "Recharge cashback of 450 rupees pending for DTH customer", "Loss of subscriber promotion", "Enter UPI MPIN on forwarded payment screen", ["OTP_PIN_CVV_THEFT"])
    ]),

    # 5. OTP & Credential Harvesting (18)
    ("OTP_HARVESTING", 18, [
        ("Airtel Telecom Verification", "Officer Naresh Goyal", "SIM card re-verification mandate issued by Telecom Ministry", "SIM card deactivation within 2 hours", "Provide 6-digit SMS verification code immediately", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT", "URGENCY_OR_THREAT"]),
        ("Jio Digital Security", "Supervisor Ankit Roy", "Aadhaar e-KYC mismatch causing outgoing call suspension", "Permanent disconnection of mobile number", "Recite OTP sent to alternate registered number", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT", "URGENCY_OR_THREAT"]),
        ("Vodafone Idea Regulatory Cell", "Officer Meenakshi Sundaram", "Mandatory 4G to 5G SIM conversion security code validation", "Complete signal outage starting tonight", "Share confirmation OTP to complete air-migration", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("UIDAI Aadhaar Security", "Officer Harish Hegde", "Aadhaar biometric lock bypass detected on regional authentication server", "Freezing of Aadhaar number across all banking services", "Provide Aadhaar authentication OTP to lock credentials", ["OTP_PIN_CVV_THEFT", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"]),
        ("Income Tax E-Filing Cell", "Officer Sunita Roy", "Income tax refund of 24,500 rupees approved for direct deposit", "Lapse of refund to central pool", "Share income tax portal validation OTP", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("NSDL PAN Card Services", "Executive Alok Mishra", "PAN card deactivation scheduled due to incomplete Aadhaar linkage", "Salary bank account freeze and 10,000 fine", "Verify PAN linkage authorization OTP code", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT", "URGENCY_OR_THREAT"]),
        ("HDFC NetBanking Security", "Officer Manish Arora", "New beneficiary addition attempted from an unknown device in Noida", "Unauthorized transfer of 95,000 rupees", "Provide cancellation OTP to revoke beneficiary registration", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT", "ACCOUNT_OR_KYC_THREAT"]),
        ("ICICI Security Alert", "Manager Smita Rao", "International roaming transaction attempted on debit card", "Complete debit of available account funds", "Read out card blocking authorization code", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Axis Bank Alerts Desk", "Executive Tarun Varma", "Card replacement dispatch verification required", "Card dispatch cancellation and penalty", "Provide security verification code sent via SMS", ["OTP_PIN_CVV_THEFT"]),
        ("SBI Card Anti-Fraud Unit", "Officer Vikramjit", "Card protection plan auto-renewal fee of 4,999 debited", "Recurring annual deduction from credit balance", "Share OTP to cancel card protection plan insurance", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("EPFO Member Portal", "Officer S. N. Joshi", "Universal Account Number (UAN) profile KYC update required", "Provident fund interest withdrawal suspension", "Share EPFO mobile validation code", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("Indian Post Office Savings", "Officer K. Ramanathan", "Postal savings account mobile linkage verification", "Account dormancy and withdrawal restriction", "Share postal verification OTP over phone", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("FASTag Toll Security", "Officer Deepak Chawla", "FASTag wallet low balance penalty fee dispute", "Vehicle blacklisting at national toll plazas", "Provide OTP to claim disputed toll reversal", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("LIC Pension Portal", "Officer R. K. Bhatt", "Life certificate annual submission verification code", "Suspension of monthly pension disbursement", "Recite OTP received from Jeevan Pramaan portal", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("WhatsApp Security Verification", "Technical Support James", "Two-step verification pin reset request from another phone", "Total account hijack and deletion of chat history", "Share 6-digit WhatsApp registration code", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Instagram Account Integrity", "Desk Officer Alex", "Copyright infringement notice on recent social media photo", "Permanent deletion of social media profile in 24 hours", "Enter two-factor security code on provided form", ["OTP_PIN_CVV_THEFT", "MALICIOUS_LINK_OR_APP"]),
        ("Google Account Security", "Support Lead Michael", "Password reset attempted from unknown browser in Russia", "Lockout from Gmail, Google Drive and Photos", "Confirm Google verification prompt or recite SMS code", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Microsoft Account Vigilance", "Senior Engineer David", "Windows enterprise license expiration and data encryption threat", "Loss of operating system access", "Provide Microsoft account verification code", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"])
    ]),

    # 6. Fake KYC Updates & Account Freeze (16)
    ("FAKE_KYC", 16, [
        ("SBI Central Operations", "Manager Ajay Saxena", "Mandatory RBI CKYC non-compliance block on savings account", "Account suspension and 5,000 unfreeze fine", "Upload PAN Aadhaar on urgent web-link", ["ACCOUNT_OR_KYC_THREAT", "MALICIOUS_LINK_OR_APP", "URGENCY_OR_THREAT"]),
        ("HDFC Bank Compliance Desk", "Officer Ritu Chopra", "Video KYC pending for high-value banking operations", "Suspension of outgoing IMPS and UPI", "Complete verification through custom mobile portal link", ["ACCOUNT_OR_KYC_THREAT", "MALICIOUS_LINK_OR_APP"]),
        ("ICICI KYC Support", "Executive Sandeep Das", "Aadhaar demographic mismatch with bank database", "Immediate account freeze tonight", "Share OTP and Aadhaar number to update profile", ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Axis Bank e-KYC Unit", "Officer Megha Tandon", "Form 60/PAN mandate non-submission penalty", "Freezing of debit card and net banking", "Download bank KYC update APK from link", ["ACCOUNT_OR_KYC_THREAT", "MALICIOUS_LINK_OR_APP"]),
        ("Kotak Mahindra KYC Cell", "Supervisor Rahul Roy", "Account classified as dormant due to overdue annual re-KYC", "Forfeiture of interest payout", "Transfer 10 rupees to verify active VPA", ["ACCOUNT_OR_KYC_THREAT", "FINANCIAL_REDIRECTION"]),
        ("Bank of Baroda KYC Bureau", "Officer S. K. Nair", "Periodic re-KYC deadline lapsed today at 5 PM", "Total transaction debit freeze", "Provide OTP to bypass branch visit", ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Punjab National Bank Desk", "Executive Jagjit Singh", "Biometric KYC update required at customer home desk", "Closure of government subsidy account", "Pay 350 rupees doorstep verification charge", ["ACCOUNT_OR_KYC_THREAT", "FINANCIAL_REDIRECTION"]),
        ("Canara Bank KYC Team", "Officer Savitri Rao", "Centralized KYC registry update mandate pending", "Account debit freeze within 3 hours", "Recite mobile validation code", ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT"]),
        ("Union Bank Compliance Cell", "Manager D. N. Pandey", "FATCA declaration pending for international transactions", "Account freezing under tax compliance laws", "Upload passport copy on third-party link", ["ACCOUNT_OR_KYC_THREAT", "MALICIOUS_LINK_OR_APP"]),
        ("Paytm Payments Bank KYC", "Agent Rohit Kumar", "Wallet balance freeze due to expired minimum KYC", "Loss of remaining wallet balance", "Enter UPI PIN on KYC approval screen", ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT"]),
        ("Airtel Payments Bank KYC", "Executive Priyanka", "Merchant payment account KYC expiration", "Account blacklisting", "Provide Aadhaar authentication code", ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT"]),
        ("Jio Payments Bank Support", "Agent Vishal", "Digital wallet regulatory compliance hold", "Permanent account deactivation", "Share verification code sent via SMS", ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT"]),
        ("FASTag KYC Helpline", "Officer Nitin", "FASTag NPCI compliance block", "Blacklisting of vehicle tag at toll plaza", "Verify FASTag wallet through payment link", ["ACCOUNT_OR_KYC_THREAT", "MALICIOUS_LINK_OR_APP"]),
        ("Zerodha Demat KYC Unit", "Executive Arjun", "SEBI mandatory Demat re-KYC compliance", "Freezing of stock trading portfolio", "Share trading portal OTP and password", ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT"]),
        ("Groww Mutual Fund KYC", "Officer Sneha", "Central KYC status showing on-hold for mutual funds", "Inability to redeem or sell investment units", "Update KYC through external verification app", ["ACCOUNT_OR_KYC_THREAT", "MALICIOUS_LINK_OR_APP"]),
        ("Upstox Brokerage KYC", "Agent Karthik", "Demat account annual compliance documents missing", "Suspension of equity trading account", "Provide Aadhaar OTP for instant paperless renewal", ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT"])
    ]),

    # 7. Phishing Links & Malicious APKs (14)
    ("PHISHING_LINKS", 14, [
        ("State Electricity Department", "Officer B. K. Shinde", "Unpaid electricity bill surcharge of 12 rupees pending", "Power supply disconnection tonight at 8 PM", "Install Bijli_Bill_Update.apk from SMS link", ["MALICIOUS_LINK_OR_APP", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
        ("Traffic Police E-Challan Cell", "Inspector Vinod Tyagi", "Pending traffic violation e-challan photo evidence", "Suspension of driving license and court warrant", "Click official e-challan SMS link to clear fine", ["MALICIOUS_LINK_OR_APP", "URGENCY_OR_THREAT", "AUTHORITY_IMPERSONATION"]),
        ("Income Tax Refund Processing", "Desk Officer M. L. Gupta", "Tax refund of 38,200 rupees credited to wrong account", "Refund cancellation if not confirmed within 24 hours", "Confirm bank details on IncomeTax_Refund_Portal.link", ["MALICIOUS_LINK_OR_APP", "ACCOUNT_OR_KYC_THREAT"]),
        ("PM Kisan Samman Nidhi", "Officer Ramadhar Singh", "Government farmer subsidy installment of 6,000 rupees pending", "Cancellation of subsidy allocation", "Download PM_Kisan_Yojana.apk to verify bank account", ["MALICIOUS_LINK_OR_APP", "FINANCIAL_REDIRECTION"]),
        ("LPG Gas Subsidy Desk", "Agent Rajeshwar", "Annual cooking gas subsidy credit verification", "Permanent loss of subsidized cylinder quota", "Submit bank details on Gas_Subsidy_Update.com", ["MALICIOUS_LINK_OR_APP", "ACCOUNT_OR_KYC_THREAT"]),
        ("India Post Consignment Track", "Helpdesk Agent Sunita", "Delivery address missing street number on parcel", "Parcel return to sender with return fee", "Update address and pay 5 rupees re-delivery fee on link", ["MALICIOUS_LINK_OR_APP", "COURIER_CUSTOMS_FRAUD", "FINANCIAL_REDIRECTION"]),
        ("Ration Card Digital Portal", "Officer Devendra", "Digital smart ration card mandatory e-KYC", "Ration quota suspension for entire family", "Install Smart_Ration_Card.apk to activate smart card", ["MALICIOUS_LINK_OR_APP", "ACCOUNT_OR_KYC_THREAT"]),
        ("Free Mobile Recharge Offer", "Executive Simran", "Government 3-month free internet recharge promotional link", "Offer expiration tonight", "Forward link to 10 WhatsApp groups and enter mobile number", ["MALICIOUS_LINK_OR_APP"]),
        ("Telecom 5G Tower Land Lease", "Officer Balwant", "Tower installation advance payment agreement link", "Cancellation of 50,000 monthly rent agreement", "Review contract on telecom-tower-agreement.net", ["MALICIOUS_LINK_OR_APP", "FINANCIAL_REDIRECTION"]),
        ("Voter ID Card Online Portal", "Desk Officer Anand", "Voter card address revision verification", "Removal of name from electoral roll", "Verify electoral roll on voter-id-revision.org", ["MALICIOUS_LINK_OR_APP", "ACCOUNT_OR_KYC_THREAT"]),
        ("Hospital Patient Portal", "Staff Sister Sunita", "Doctor prescription and pathology report download link", "Delay in treatment consultation", "Download City_Hospital_Patient.apk to view test results", ["MALICIOUS_LINK_OR_APP"]),
        ("School Examination Results", "Coordinator Mohan", "Quarterly board examination marksheet verification", "Withholding of student admit card", "Access student portal on dps-exam-board.info", ["MALICIOUS_LINK_OR_APP"]),
        ("Metro Smart Card Recharge", "Executive Preeti", "100% cashback promo on metro card recharge link", "Promo expiration in 30 minutes", "Recharge metro card on metro-recharge-bonus.app", ["MALICIOUS_LINK_OR_APP", "FINANCIAL_REDIRECTION"]),
        ("Water Board Bill Discount", "Officer Harish", "50% rebate on advance water utility bill payment", "Rebate expiration today", "Pay discounted bill on jalboard-online-bill.link", ["MALICIOUS_LINK_OR_APP", "FINANCIAL_REDIRECTION"])
    ]),

    # 8. Courier & International Customs (16)
    ("COURIER_CUSTOMS_FRAUD", 16, [
        ("FedEx Cargo Security", "Officer Deshmukh", "Consignment from Taiwan seized containing 140 grams MDMA narcotics", "Immediate NCB arrest warrant and interrogation", "Pay provisional customs exoneration clearance fee", ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "DIGITAL_ARREST"]),
        ("DHL Express International", "Superintendent George Verghese", "Undervalued electronic consignment from Dubai containing 5 gold bars", "Confiscation and criminal prosecution under Customs Act", "Transfer penalty deposit to customs clearance officer", ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("India Post International Hub", "Officer Ramanathan", "Foreign parcel with fake passport and high-value foreign currency", "FIR registered with airport police station", "Pay legal verification deposit through instant UPI", ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("BlueDart Security Operations", "Manager Amit Saxena", "Parcel returned twice due to incorrect address, contains confidential documents", "Parcel forfeiture and legal notice", "Install tracking APK to correct delivery address", ["COURIER_CUSTOMS_FRAUD", "MALICIOUS_LINK_OR_APP"]),
        ("Delhi Airport Cargo Customs", "Superintendent B. S. Hooda", "Overseas gift parcel containing undeclared luxury items from London", "Confiscation and heavy customs penalty", "Transfer import duty clearance fee to official agent", ["COURIER_CUSTOMS_FRAUD", "FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Mumbai Air Cargo Complex", "Officer Pradeep Mane", "Parcel addressed to your mobile number held under suspicion of smuggling", "Customs detention and court prosecution", "Deposit refundable customs clearance bond", ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
        ("DTDC International Security", "Helpdesk Agent Manish", "Express parcel detained at state border due to lack of e-way bill", "Auction of parcel contents", "Pay border clearance tax immediately", ["COURIER_CUSTOMS_FRAUD", "FINANCIAL_REDIRECTION"]),
        ("Aramex Logistics Hub", "Officer Tariq", "Consignment from UK awaiting customs import clearance duty", "Package return to origin at recipient cost", "Pay clearance fee through provided SMS gateway", ["COURIER_CUSTOMS_FRAUD", "MALICIOUS_LINK_OR_APP"]),
        ("Speed Post National Sorting", "Supervisor Jagdish", "Speed post package containing legal summons delayed", "Court penalty for non-acceptance", "Verify identity via mobile OTP", ["COURIER_CUSTOMS_FRAUD", "OTP_PIN_CVV_THEFT"]),
        ("Ekart Logistics Hub", "Executive Vinay", "High-value smartphone delivery verification code required", "Order cancellation and return fee deduction", "Share delivery confirmation OTP over phone", ["COURIER_CUSTOMS_FRAUD", "OTP_PIN_CVV_THEFT"]),
        ("Shadowfax Delivery Network", "Agent Santosh", "E-commerce cash-on-delivery order address mismatch", "Account blacklisting on e-commerce portal", "Pay 10 rupees address confirmation fee via UPI", ["COURIER_CUSTOMS_FRAUD", "FINANCIAL_REDIRECTION"]),
        ("Delhivery Security Wing", "Officer Rakesh", "Seizure of banned biological samples in parcel bearing your name", "CBI FIR registration", "Transfer clearance verification bond", ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "DIGITAL_ARREST"]),
        ("Gati KWE Logistics", "Supervisor Naresh", "Commercial consignment detained for state GST inspection", "Vehicle and goods impounding", "Pay GST clearance penalty", ["COURIER_CUSTOMS_FRAUD", "FINANCIAL_REDIRECTION"]),
        ("Trackon Couriers Hub", "Agent Suresh", "Damaged parcel containing electronic parts", "Forfeiture of transit insurance claim", "Provide OTP to approve insurance settlement", ["COURIER_CUSTOMS_FRAUD", "OTP_PIN_CVV_THEFT"]),
        ("Professional Couriers", "Executive Mahesh", "Confidential court affidavit parcel delivery confirmation", "Contempt notice for non-delivery", "Verify recipient Aadhaar over call", ["COURIER_CUSTOMS_FRAUD", "OTP_PIN_CVV_THEFT"]),
        ("First Flight Courier Desk", "Agent Anil", "International consignment duty surcharge", "Auction of goods", "Transfer customs fee to clearing agent", ["COURIER_CUSTOMS_FRAUD", "FINANCIAL_REDIRECTION"])
    ]),

    # 9. Job, Task & Internship Scams (16)
    ("JOB_SCAM", 16, [
        ("Global Media Reach", "Recruiter Sneha Kapoor", "Part-time YouTube video liking task paying 3,500 rupees daily", "Forfeiture of premium job allocation", "Pay 5,000 rupees VIP task security deposit", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Apex Digital Freelance", "HR Lead Rahul Verma", "Google Maps hotel rating review work paying 150 rupees per review", "Account deactivation on Telegram work channel", "Transfer 10,000 for elite commission tier upgrade", ["FINANCIAL_REDIRECTION"]),
        ("Indigo Airlines HR Desk", "Manager Priya Nambiar", "Airport ground staff job offer with 45,000 monthly salary", "Offer cancellation in favor of standby candidate", "Pay 8,500 rupees uniform and security badge clearance", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Amazon Web Services Tasks", "Supervisor David Chen", "Cloud data annotation and AI labeling remote freelance job", "Termination of freelancer contractor contract", "Deposit 12,000 cryptocurrency training fee", ["FINANCIAL_REDIRECTION"]),
        ("Tata Tech Global Careers", "HR Executive Tanvi", "Selection as Junior Systems Associate with 8.5 LPA package", "Cancellation of appointment letter", "Pay 6,200 rupees background verification agency fee", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Infosys BPM Recruitment", "Recruiter Amit", "Work from home voice process customer support specialist", "Loss of assigned work laptop dispatch", "Pay 4,500 rupees laptop courier insurance deposit", ["FINANCIAL_REDIRECTION"]),
        ("Wipro Talent Acquisition", "Executive Deepa", "Software engineer opening with signing bonus of 1 lakh", "Offer revoked today", "Transfer 9,000 document processing charge", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Reliance Retail HR Cell", "HR Officer Manoj", "Store inventory manager role with company accommodation", "Selection of waitlisted candidate", "Deposit 5,500 medical fitness test fee", ["FINANCIAL_REDIRECTION"]),
        ("Flipkart Logistics Careers", "Recruiter Sonu", "Delivery hub supervisor job opening with company bike", "Job offer forfeiture", "Pay 3,800 gate pass and identity card fee", ["FINANCIAL_REDIRECTION"]),
        ("Tech Mahindra BPO Hiring", "HR Executive Divya", "Chat support executive position with night shift allowance", "Cancellation of onboarding slot", "Pay 2,900 portal registration charge", ["FINANCIAL_REDIRECTION"]),
        ("Airtel Customer Service HR", "Agent Rohit", "Customer relationship officer work from home vacancy", "Loss of selected candidate seat", "Transfer 4,000 training software license fee", ["FINANCIAL_REDIRECTION"]),
        ("HCL Tech Campus Hiring", "Recruiter Neha", "Graduate trainee opening with joining bonus", "Revocation of campus offer", "Pay 7,500 aptitude test certification fee", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Apollo Pharmacy HR Desk", "Officer Suresh", "Pharmacy retail billing executive vacancy", "Passing offer to next applicant", "Deposit 3,200 uniform and badge charge", ["FINANCIAL_REDIRECTION"]),
        ("L&T Construction Careers", "HR Lead Vikram", "Site supervisor job with overseas deputation option", "Offer expiration in 24 hours", "Pay 11,000 visa documentation fee", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Maruti Suzuki Plant Hiring", "Recruiter Harish", "Assembly plant technician role with food and stay", "Cancellation of candidate file", "Deposit 4,800 safety gear deposit", ["FINANCIAL_REDIRECTION"]),
        ("Cognizant HR Operations", "Executive Shalini", "Junior developer vacancy with immediate joining", "Offer withdrawal", "Pay 6,500 background verification fee", ["FINANCIAL_REDIRECTION"])
    ]),

    # 10. Investment, Crypto & Forex Fraud (14)
    ("INVESTMENT_FRAUD", 14, [
        ("BitPro Wealth Advisory", "Trader Aryan Mehra", "Algorithmic Bitcoin arbitrage trading guaranteeing 250% weekly returns", "Closure of exclusive institutional trading window", "Deposit 25,000 rupees initial investment via crypto wallet", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("NSE Institutional Syndicate", "Chief Strategist R. K. Singhal", "Pre-IPO allotment of high-growth tech shares at 70% discount", "Allotment given to secondary institutional bidder", "Transfer 50,000 rupees to institutional clearing escrow", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Forex Matrix Automated Bot", "Advisor Alex Turner", "High-frequency EUR/USD currency trading yielding 15% daily profit", "Bot license expiration today", "Deposit 20,000 software activation token", ["FINANCIAL_REDIRECTION"]),
        ("SEBI Approved Wealth Desk", "Advisor Vikram Joshi", "Guaranteed upper circuit multibagger stock recommendations group", "Removal from VIP Telegram inner circle", "Pay 15,000 quarterly advisory subscription", ["FINANCIAL_REDIRECTION"]),
        ("Gold Bullion Trading Desk", "Trader Mohit", "International gold commodity future arbitrage profit split", "Loss of margin leverage bonus", "Transfer 30,000 margin collateral", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Crude Oil Commodities Hub", "Advisor Deepak", "Crude oil options contract yielding 300% on inventory release", "Contract expiry within 2 hours", "Deposit 35,000 premium to execute trade", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Binance VIP Arbitrage Group", "Manager Kevin", "Cross-exchange USDT flash loan arbitrage pool", "Pool full, slot reassigned", "Transfer 40,000 to shared liquidity pool", ["FINANCIAL_REDIRECTION"]),
        ("Ethereum Staking Foundation", "Lead Dev Lucas", "ETH 2.0 validator staking reward of 30% monthly APY", "Staking pool rewards forfeiture", "Send crypto to staking deposit smart contract", ["FINANCIAL_REDIRECTION"]),
        ("Mutual Fund Multibagger Cell", "Analyst Sanjay", "Unlisted pre-IPO private equity fund participation", "Opportunity closed to retail investors", "Transfer 60,000 minimum subscription capital", ["FINANCIAL_REDIRECTION"]),
        ("Stock Market Insider Desk", "Trader Tarun", "SEBI confidential earnings leak stock tip guarantee", "Removal from premium trading signal broadcast", "Pay 18,000 monthly insider commission", ["FINANCIAL_REDIRECTION"]),
        ("Penny Stock Pump Syndicate", "Advisor Vishal", "Guaranteed 10x micro-cap company merger surge", "Loss of entry price advantage", "Deposit 25,000 into trading syndicate account", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Green Energy Carbon Credits", "Manager David", "International carbon credit trading investment with high ROI", "Tax incentive quota expiration", "Transfer 45,000 carbon credit unit purchase", ["FINANCIAL_REDIRECTION"]),
        ("Agro Commodity Warehouse Desk", "Advisor Ramesh", "Soybean and mustard seed future hedging guaranteed return", "Hedging window close", "Deposit 30,000 seasonal commodity bond", ["FINANCIAL_REDIRECTION"]),
        ("Real Estate REIT Syndicate", "Officer Alok", "Fractional commercial real estate rental income 18% yield", "Slot allocation cancellation", "Transfer 50,000 token advance booking", ["FINANCIAL_REDIRECTION"])
    ]),

    # 11. Loan & Credit Card Scams (12)
    ("LOAN_SCAM", 12, [
        ("QuickFin Lending Solutions", "Loan Officer Agarwal", "Pre-approved paperless personal loan of 10 lakhs at 4.5% interest", "Cancellation of subsidized festive loan sanction", "Pay 9,800 rupees loan insurance stamp duty fee", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Pradhan Mantri Mudra Yojana", "Officer Surendra Yadav", "Government Mudra business loan subsidy of 5 lakhs sanctioned", "Lapse of government loan subsidy grant", "Deposit 12,500 refundable subsidy processing fee", ["FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION"]),
        ("Bajaj Finance Pre-Approved", "Executive Rohit Sen", "Zero percent interest consumer durable loan of 2.5 lakhs", "Cancellation of pre-approved loan credit line", "Pay 3,500 file processing charge via UPI", ["FINANCIAL_REDIRECTION"]),
        ("Tata Capital Easy Loans", "Loan Advisor Megha", "Instant collateral-free home renovation loan of 7 lakhs", "Rate of interest hike to 18%", "Transfer 8,200 legal verification fee", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("CIBIL Credit Score Repair", "Analyst Vivek", "Expungement of negative credit defaults and CIBIL score boost to 800+", "Inability to apply for banking loans for 3 years", "Pay 6,000 bureau data correction fee", ["FINANCIAL_REDIRECTION"]),
        ("Student Education Loan Desk", "Officer Ananya", "Subsidized abroad higher education loan sanction of 20 lakhs", "Cancellation of university tuition loan release", "Deposit 15,000 consular document fee", ["FINANCIAL_REDIRECTION"]),
        ("Emergency Medical Loan Hub", "Advisor Alok", "Instant hospital cash loan of 3 lakhs sanctioned without income proof", "Approval cancellation", "Pay 4,500 emergency disbursal commission", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("HassleFree Vehicle Loan", "Manager Vikram", "100% on-road financing for new vehicle at zero down payment", "Offer transferred to next buyer", "Transfer 5,500 vehicle hypothecation fee", ["FINANCIAL_REDIRECTION"]),
        ("Gold Loan Top-Up Solutions", "Officer Sunita", "Instant gold loan top-up of 1.5 lakhs without physical inspection", "Loss of gold loan interest discount", "Pay 2,800 appraisal fee via link", ["FINANCIAL_REDIRECTION"]),
        ("Payday Advance Credit Cell", "Executive Kunal", "Instant salary advance of 50,000 rupees credited in 5 minutes", "Credit line cancellation", "Pay 1,999 registration fee through payment link", ["MALICIOUS_LINK_OR_APP", "FINANCIAL_REDIRECTION"]),
        ("Rural Agriculture Loan Desk", "Officer Ramdas", "Kisan credit card limit enhancement to 4 lakhs without land audit", "Forfeiture of agricultural subsidy", "Deposit 4,200 revenue stamp fee", ["FINANCIAL_REDIRECTION"]),
        ("Overdraft Facility Care", "Manager Tanvi", "Lifetime free bank overdraft limit of 2 lakhs on savings account", "Facility cancellation", "Verify account with 2,500 activation deposit", ["FINANCIAL_REDIRECTION"])
    ]),

    # 12. Insurance & Policy Bonus Fraud (10)
    ("INSURANCE_SCAM", 10, [
        ("LIC Claims Settlement Cell", "Officer Tripathi", "Accumulated life insurance bonus of 3.8 lakhs ready for release", "Lapse of policy maturity bonus to government fund", "Pay 18,500 rupees GST processing charge", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("IRDAI Consumer Grievance", "Officer Manoj Sharma", "Refund of 1.2 lakhs recovered from mis-sold private insurance policy", "Closure of grievance complaint file", "Transfer 8,900 statutory court fee to release cheque", ["FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION"]),
        ("HDFC Life Maturity Division", "Manager Neha Verma", "Policy maturity payout credited but held in treasury pool", "Maturity funds forfeiture", "Verify bank details with netbanking OTP", ["OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
        ("Max Life Bonus Disbursement", "Officer Rajiv", "Unclaimed loyalty additions on lapsed life insurance policy", "Bonus return to insurer surplus pool", "Pay 6,500 clearance charge", ["FINANCIAL_REDIRECTION"]),
        ("Star Health Cashless Claim", "Agent Deepa", "Hospital cashless claim reimbursement clearance fee", "Rejection of medical insurance claim", "Transfer 4,800 processing fee", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("ICICI Prudential Rewards", "Officer Tarun", "Accumulated unit linked insurance portfolio cash dividend", "Dividend return to central reserve", "Share mobile verification code", ["OTP_PIN_CVV_THEFT"]),
        ("Bajaj Allianz Motor Claims", "Surveyor Alok", "Car accident insurance claim settlement release", "Claim repudiation", "Pay 3,500 salvage inspection charge", ["FINANCIAL_REDIRECTION"]),
        ("SBI General Insurance Cell", "Executive Divya", "Personal accident cover complimentary upgrade", "Loss of 25-lakh free cover", "Provide debit card expiry and CVV", ["OTP_PIN_CVV_THEFT"]),
        ("National Insurance Office", "Officer Balraj", "Mediclaim policy renewal with zero deduction benefit", "Policy lapse tonight", "Pay premium through third-party payment link", ["MALICIOUS_LINK_OR_APP", "FINANCIAL_REDIRECTION"]),
        ("Tata AIG Health Desk", "Advisor Pooja", "Critical illness rider payout ready for wire transfer", "Forfeiture of rider benefit", "Deposit 7,200 clearing tax", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"])
    ]),

    # 13. Lottery, Contest & Lucky Draw (8)
    ("LOTTERY_SCAM", 8, [
        ("Kaun Banega Crorepati Office", "Officer Rana Pratap", "Winner of 25 Lakhs cash prize in national SIM lucky draw", "Cancellation of prize cheque", "Pay 12,500 rupees government GST tax fee", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Amazon 25th Anniversary Draw", "Supervisor Aman Gupta", "Selected winner of Brand New Tata Safari SUV in customer sweepstake", "Prize passed to alternate contestant", "Deposit 24,000 vehicle registration and road tax", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Flipkart Big Billion Winner", "Executive Priya Sen", "Lucky winner of Apple iPhone 16 Pro Max for 1-rupee token", "Gift order cancellation", "Pay 2,499 customs duty and shipping insurance", ["FINANCIAL_REDIRECTION"]),
        ("Jio Consumer Jubilee Draw", "Officer Naresh", "SIM card selected for 10 Lakhs cash bonanza prize", "Prize money returned to company fund", "Transfer 8,500 RBI processing token", ["FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION"]),
        ("Samsung Electronics Mega Draw", "Manager Kevin", "Global customer appreciation prize of 5 Lakhs", "Forfeiture of award prize", "Pay 6,800 international bank wire fee", ["FINANCIAL_REDIRECTION"]),
        ("Dubai Shopping Festival Draw", "Officer David", "Raffle ticket winner of 100 grams gold bar", "Gold bullion auction by customs", "Deposit 15,000 customs clearance tax", ["FINANCIAL_REDIRECTION", "COURIER_CUSTOMS_FRAUD"]),
        ("Coca Cola Summer Mega Promo", "Agent Rohit", "Bottle crown code won 2 Lakhs cash voucher", "Voucher cancellation today", "Pay 3,500 commercial processing fee", ["FINANCIAL_REDIRECTION"]),
        ("Airtel Golden SIM Rewards", "Executive Meena", "Special subscriber reward of 1 Lakh shopping voucher", "Reward lapse in 1 hour", "Provide OTP to claim gift voucher", ["OTP_PIN_CVV_THEFT"])
    ]),

    # 14. Tech Support & Malware (10)
    ("TECH_SUPPORT", 10, [
        ("Microsoft Windows Security", "Senior Tech Lead Peter", "Critical Trojan virus detected attempting to broadcast passwords", "Complete hard drive encryption within 30 minutes", "Install remote tool to allow engineer to purge malware", ["REMOTE_ACCESS_MANIPULATION", "URGENCY_OR_THREAT"]),
        ("Global Cyber Defender Tech", "Supervisor Michael Ross", "Annual anti-virus subscription auto-renewed for 28,000 rupees", "Non-refundable debit from bank account", "Connect via TeamViewer to process instant refund", ["REMOTE_ACCESS_MANIPULATION", "FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
        ("Google Workspace Corporate", "Engineer Alex Turner", "Corporate email compromised and used in spam campaigns", "Immediate termination of Google Workspace domain", "Verify administrator password on remote session", ["REMOTE_ACCESS_MANIPULATION", "OTP_PIN_CVV_THEFT"]),
        ("Apple iCloud Security Desk", "Support Lead James", "iCloud photo library accessed from unknown IP in Beijing", "Complete data wipe and Apple ID permanent lock", "Provide two-factor Apple verification code", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("McAfee Anti-Virus Renewal", "Tech Agent David", "Auto-debit of 19,999 initiated for 3-year antivirus package", "Irreversible bank charge in 1 hour", "Allow screen share to cancel invoice", ["REMOTE_ACCESS_MANIPULATION", "FINANCIAL_REDIRECTION"]),
        ("Norton LifeLock Security", "Support Officer Chris", "Identity theft alert indicating Dark Web sale of Aadhaar", "Financial identity compromise", "Install Norton_Fix.apk to secure mobile device", ["MALICIOUS_LINK_OR_APP", "URGENCY_OR_THREAT"]),
        ("HP Printer Support Helpdesk", "Technician George", "Printer firmware virus infecting home WiFi router", "Network shutdown by ISP", "Pay 4,500 network cleaning fee", ["FINANCIAL_REDIRECTION"]),
        ("Broadband Router Firmware", "Engineer Anand", "Malicious malware attack on residential fiber optic modem", "Internet connection termination", "Provide router admin password and OTP", ["OTP_PIN_CVV_THEFT"]),
        ("Dell Service Security Desk", "Technician Suresh", "Hardware motherboard error transmitting system telemetry", "Motherboard failure", "Install remote diagnostic assistant", ["REMOTE_ACCESS_MANIPULATION"]),
        ("Kaspersky Anti-Hacking Cell", "Agent Roy", "Active ransomware beacon detected on local machine", "Files locked forever", "Purchase 5,000 decryption security key", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"])
    ]),

    # 15. Remote Access Application Manipulation (12)
    ("REMOTE_ACCESS", 12, [
        ("HDFC Digital Security Cell", "Supervisor Vikramaditya", "Unauthorized device logged into your mobile banking app", "Total siphon of savings balance", "Install AnyDesk and share 9-digit code for security audit", ["REMOTE_ACCESS_MANIPULATION", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("SBI YONO Technical Desk", "Executive Rajiv Sen", "YONO mobile app version update error causing payment freeze", "Permanent YONO portal deactivation", "Download QuickSupport and keep screen on", ["REMOTE_ACCESS_MANIPULATION", "ACCOUNT_OR_KYC_THREAT"]),
        ("ICICI iMobile Support Unit", "Officer Ananya Gupta", "Beneficiary limit enhancement requires remote screen verification", "Failure of fund transfer", "Install TeamViewer and grant accessibility permissions", ["REMOTE_ACCESS_MANIPULATION"]),
        ("Axis Mobile App Support", "Executive Rohit Singhal", "Mobile banking fingerprint sensor desynchronization", "Account lock", "Install RustDesk for remote sensor calibration", ["REMOTE_ACCESS_MANIPULATION"]),
        ("Paytm Technical Helpline", "Agent Neha Sharma", "Paytm wallet payment gateway error during merchant transaction", "Loss of pending payment", "Install AnyDesk to perform reverse payment routing", ["REMOTE_ACCESS_MANIPULATION", "FINANCIAL_REDIRECTION"]),
        ("PhonePe Resolution Team", "Executive Rahul Verma", "UPI server sync issue blocking incoming merchant refunds", "Refund return to bank", "Share screen via QuickSupport to resolve pending cash", ["REMOTE_ACCESS_MANIPULATION", "FINANCIAL_REDIRECTION"]),
        ("Google Pay Tech Helpdesk", "Supervisor Aman", "Virtual payment address conflict on multi-SIM phone", "Google Pay service ban", "Download ScreenShare APK from provided link", ["MALICIOUS_LINK_OR_APP", "REMOTE_ACCESS_MANIPULATION"]),
        ("Bank of Baroda M-Connect", "Officer Manoj", "Mobile banking passbook download error resolution", "Statement access suspended", "Install AnyDesk to download encrypted statement", ["REMOTE_ACCESS_MANIPULATION"]),
        ("Canara ai1 App Support", "Executive Swamy", "App crash during IMPS transaction requiring remote patch", "Transaction dispute failure", "Share TeamViewer access to clear cache", ["REMOTE_ACCESS_MANIPULATION"]),
        ("Kotak 811 Tech Desk", "Manager Vivek", "Zero-balance digital account biometric remote verification", "Account closure", "Install QuickSupport for live video screen capture", ["REMOTE_ACCESS_MANIPULATION", "ACCOUNT_OR_KYC_THREAT"]),
        ("Airtel Thanks App Care", "Agent Naresh", "Recharge transaction failure refund processing", "Loss of recharge balance", "Install AnyDesk to reverse recharge debit", ["REMOTE_ACCESS_MANIPULATION", "FINANCIAL_REDIRECTION"]),
        ("JioFiber Home Gateway Desk", "Engineer Ankit", "Set-top box software glitch causing streaming blackouts", "Hardware replacement fee", "Install remote control app on smartphone", ["REMOTE_ACCESS_MANIPULATION"])
    ]),

    # 16. Identity Theft & Impersonation of Relatives (8)
    ("IDENTITY_THEFT", 8, [
        ("City Police Station", "Sub-Inspector Pandey", "Nephew arrested in serious road accident collision with injuries", "Immediate transfer to central jail custody", "Send 35,000 cash bail to police welfare UPI handle", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),
        ("Corporate Executive Desk", "Director Rajiv Mehra", "Urgent corporate client meeting requiring immediate gift card codes", "Loss of multi-million dollar business contract", "Purchase 50,000 rupees Apple gift cards and send codes", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
        ("International Airport Transit", "Friend Siddharth", "Stuck at Dubai transit with stolen wallet and cancelled flight", "Detention by immigration authorities", "Transfer 40,000 rupees emergency cash for flight ticket", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),
        ("City Trauma Care Hospital", "Dr. Alok Verma", "Close family friend admitted unconscious following severe cardiac arrest", "Withholding of emergency ICU admission and medication", "Deposit 30,000 rupees emergency hospital admission fee", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),
        ("Overseas University Hostel", "Colleague Sameer", "Immediate payment of semester examination fee to prevent expulsion", "Cancellation of student visa", "Transfer 45,000 university registration fee", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
        ("Highway Police Checkpoint", "Officer Dinesh", "Brother caught carrying unaccounted cash at interstate border", "FIR registration and vehicle seizure", "Pay 25,000 spot compounding settlement", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION"]),
        ("Railway Station Parcel Office", "Relative Ramesh", "Urgent delivery of wedding jewelry box held at luggage counter", "Forfeiture of family jewelry parcel", "Transfer 15,000 luggage release charge", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
        ("Hotel Reception Goa", "Manager Fernandes", "Son booked in hotel unable to pay damages for broken glass table", "Filing of police property damage complaint", "Pay 18,000 hotel damage settlement", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"])
    ]),

    # 17. Fake Customer Support & Helplines (7)
    ("FAKE_CUSTOMER_SUPPORT", 7, [
        ("IndiGo Airlines Care Desk", "Executive Sonia Bhatia", "Domestic flight booking cancelled due to schedule rescheduling", "Total ticket refund forfeiture", "Install custom refund APK from WhatsApp to claim airfare", ["MALICIOUS_LINK_OR_APP", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Swiggy Customer Escalations", "Support Lead Tanmay", "Refund for undelivered party dinner order of 2,400 rupees", "Refund cancellation after 30 minutes", "Enter UPI PIN on reverse debit payment screen", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
        ("IRCTC Ticket Cancellation Desk", "Agent Rajeshwar", "Failed Tatkal ticket refund verification", "Forfeiture of train fare refund", "Share OTP received from IRCTC", ["OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
        ("Amazon Delivery Escalation", "Helpdesk Agent Priya", "Wrong product delivered, courier pickup executive arriving", "Pickup cancellation", "Pay 20 rupees return processing fee via payment link", ["MALICIOUS_LINK_OR_APP", "FINANCIAL_REDIRECTION"]),
        ("BookMyShow Support Helpline", "Agent Varun", "Concert ticket cancellation refund processing", "Ticket refund forfeiture", "Accept collect request in Google Pay", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
        ("MakeMyTrip Hotel Care", "Executive Shalini", "Hotel check-in rejection refund resolution", "Booking forfeiture", "Enter UPI MPIN to approve hotel refund", ["OTP_PIN_CVV_THEFT"]),
        ("Uber Support Resolution Desk", "Agent Manoj", "Overcharged cab route fare adjustment refund", "Refund lapse", "Scan refund QR code sent via WhatsApp", ["OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"])
    ])
]

TARGET_COUNTS = {
    "DIGITAL_ARREST": 15,
    "FAKE_LAW_ENFORCEMENT": 13,
    "BANKING_FRAUD": 14,
    "UPI_FRAUD": 14,
    "OTP_HARVESTING": 15,
    "FAKE_KYC": 14,
    "PHISHING_LINKS": 13,
    "COURIER_CUSTOMS_FRAUD": 14,
    "JOB_SCAM": 14,
    "INVESTMENT_FRAUD": 13,
    "LOAN_SCAM": 11,
    "INSURANCE_SCAM": 9,
    "LOTTERY_SCAM": 8,
    "TECH_SUPPORT": 9,
    "REMOTE_ACCESS": 11,
    "IDENTITY_THEFT": 7,
    "FAKE_CUSTOMER_SUPPORT": 6
}

# Flatten and assign sequential IDs from SCAM_V3_001 to SCAM_V3_200
scam_records = []
counter = 1

for cat_code, _, scenarios in SCAM_CATEGORIES:
    limit = TARGET_COUNTS[cat_code]
    for org, caller, hook, threat, demand, tactics in scenarios[:limit]:
        s_id = f"SCAM_V3_{counter:03d}"
        s_name = f"{org} - {hook[:45]}"
        turn_count = 4 if counter % 5 == 1 else 6 if counter % 5 == 2 else 8 if counter % 5 == 3 else 10 if counter % 5 == 4 else 12
        scam_records.append({
            "id": s_id,
            "name": s_name,
            "category": "SCAM",
            "sub_category": cat_code,
            "caller_org": org,
            "caller_name": caller,
            "hook": hook,
            "threat": threat,
            "demand": demand,
            "tactics": tactics,
            "turn_count": turn_count
        })
        counter += 1

print(f"Total SCAM scenario archetypes generated: {len(scam_records)}")
assert len(scam_records) == 200, f"Expected 200 scam records, got {len(scam_records)}"

out_path = Path(__file__).resolve().parent / "dataset_definitions_v3" / "scam_data.py"
with open(out_path, "w", encoding="utf-8") as f:
    f.write('"""Autogenerated 200 Distinct SCAM Scenario Archetypes for KAVACH AI v3"""\n\n')
    f.write("SCAM_DATA = " + json.dumps(scam_records, indent=2, ensure_ascii=False) + "\n")

print(f"Wrote {len(scam_records)} SCAM scenario records to {out_path}")

