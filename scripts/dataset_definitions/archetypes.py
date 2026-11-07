"""
Comprehensive Remediated Generator for KAVACH AI Synthetic Dataset v2.0 (500 Conversations)

Fixes all audit findings:
1. Exact duplicate dialogue content eliminated (500/500 conversations unique).
2. Zero cross-split dialogue overlap (Train ∩ Val = 0, Train ∩ Test = 0, Val ∩ Test = 0).
3. 100 scenario archetypes partitioned strictly by scenario-family:
   - SCAM (40): 28 Train, 6 Val, 6 Test (across all 5 languages)
   - LEGITIMATE (35): 24 Train, 5 Val, 6 Test (across all 5 languages)
   - AMBIGUOUS (25): 18 Train, 4 Val, 3 Test (across all 5 languages)
4. Split totals: 350 Train (70%), 75 Val (15%), 75 Test (15%).
5. Preserves synthetic provenance and review_status='pending_review'.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from collections import Counter
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_V2_DIR = PROJECT_ROOT / "data" / "kavach_synthetic_v2"
METADATA_DIR = DATA_V2_DIR / "metadata"
TRANSCRIPTS_DIR = DATA_V2_DIR / "transcripts"
SPLITS_DIR = DATA_V2_DIR / "splits"

# 40 Distinct Scam Scenario Archetypes
SCAM_ARCHETYPES = [
    # Train Archetypes (0 to 27)
    ("SCAM_001", "CBI Money Laundering & Digital Arrest", "CBI Headquarters", "Inspector Raman", "4.2 crore illegal Hawala laundering", "Aadhaar non-bailable arrest warrant", "RBI security verification account", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT"]),
    ("SCAM_002", "Customs Narcotics International Parcel Confiscation", "Mumbai Airport Customs", "Officer Deshmukh", "FedEx carton seized with MDMA drugs", "Anti-Narcotics Bureau immediate remand", "provisional customs clearance bond", ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
    ("SCAM_003", "TRAI Mobile SIM Disconnection & Fake Aadhaar Abuse", "Telecom Regulatory Authority", "Officer Mathur", "9 unauthorized SIM cards sending abusive fraud messages", "nationwide mobile connection block within 2 hours", "Aadhaar verification OTP code", ["AUTHORITY_IMPERSONATION", "ACCOUNT_OR_KYC_THREAT", "URGENCY_OR_THREAT", "OTP_PIN_CVV_THEFT"]),
    ("SCAM_004", "State Cyber Crime Cell Section 420 Contempt Warrant", "Cyber Crime Branch", "Inspector Kulkarni", "phishing portal operated using your registered IP", "police patrol team dispatched to residence", "confidential video link interrogation", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),
    ("SCAM_005", "Enforcement Directorate Illegal Foreign Currency Coercion", "Enforcement Directorate", "Assistant Director Verma", "70,000 USD foreign exchange FEMA violation", "freezing of all domestic bank accounts", "ED safe reserve fund deposit", ["AUTHORITY_IMPERSONATION", "DIGITAL_ARREST", "FINANCIAL_REDIRECTION"]),
    ("SCAM_006", "Debit Card Expiry & Urgent OTP Harvest Phishing", "SBI Card Operations", "Manager Rajesh", "global chip debit card expiration tonight at midnight", "permanent suspension of Google Pay and ATM", "6-digit card renewal authorization OTP", ["ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
    ("SCAM_007", "Electricity Arrears & Power Disconnection Emergency", "State Electricity Board", "Officer Shinde", "15 rupees outstanding surcharge from prior cycle", "power supply termination in 30 minutes", "net banking password via urgent link", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ACCOUNT_OR_KYC_THREAT"]),
    ("SCAM_008", "AnyDesk Tech Support NetBanking Trojan Hijacking", "HDFC Digital Security", "Supervisor Vikram", "unauthorized Russian IP breach on netbanking", "total account drain within minutes", "AnyDesk 9-digit remote control code", ["REMOTE_ACCESS_MANIPULATION", "OTP_PIN_CVV_THEFT", "AUTHORITY_IMPERSONATION"]),
    ("SCAM_009", "KBC Lucky Draw Processing Fee Advance Fraud", "KBC Lottery Office", "Officer Rana Pratap", "25 Lakhs cash prize in national SIM draw", "cancellation of winning check", "12,500 rupees GST processing charge", ["FINANCIAL_REDIRECTION", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
    ("SCAM_010", "FedEx Cambodia Parcel Fake Credit Card Seizure", "FedEx Security Unit", "Officer Bansal", "carton containing 16 cloned credit cards and forged IDs", "Interpol cyber slavery FIR registration", "40,000 rupees bail clearance bond", ["COURIER_CUSTOMS_FRAUD", "AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION"]),
    ("SCAM_011", "Supreme Court Contempt Notice & Asset Freezing Coercion", "Supreme Court Registry", "Advocate Tandon", "contempt of court summons regarding unpaid digital fine", "seizure of immovable family assets", "court treasury security deposit", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
    ("SCAM_012", "Income Tax Department Tax Evasion & Bank Seizure", "Income Tax Central Circle", "Commissioner Saxena", "discrepancy of 18 lakhs in cash deposits", "immediate attachment of commercial bank accounts", "tax dispute settlement gateway payment", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
    ("SCAM_013", "EPFO Pension Release & NetBanking Credential Phishing", "EPFO Regional Cell", "Officer Srivastava", "pension arrears of 1.4 lakhs pending release", "lapse of provident fund interest benefits", "net banking user ID and OTP verification", ["AUTHORITY_IMPERSONATION", "OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
    ("SCAM_014", "FASTag Toll Blacklisting & Security Deposit Theft", "FASTag Operations Unit", "Officer Chopra", "blacklisting of highway toll tag due to KYC lapse", "penalty of 10,000 rupees at toll plazas", "FASTag reactivation UPI PIN transfer", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "MALICIOUS_LINK_OR_APP"]),
    ("SCAM_015", "Credit Card Reward Points Expiry Phishing APK", "ICICI Bank Rewards Cell", "Officer Mehra", "accumulated reward points worth 14,200 rupees expiring", "forfeiture of loyalty reward cash balance", "custom APK installation to claim cash", ["MALICIOUS_LINK_OR_APP", "OTP_PIN_CVV_THEFT", "ACCOUNT_OR_KYC_THREAT"]),
    ("SCAM_016", "Family Member Police Custody Emergency Bail Trap", "City Police Station", "Sub-Inspector Pandey", "nephew arrested in hit-and-run accident with injuries", "immediate transfer to central prison", "35,000 rupees cash bail to officer UPI", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),
    ("SCAM_017", "Aadhaar PAN Linking Fine & Biometric Freeze Threat", "UIDAI Compliance Wing", "Officer Hegde", "Aadhaar PAN non-compliance penalty of 10,000 rupees", "cancellation of PAN card and salary freeze", "instant Aadhaar biometric unlocking fee", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
    ("SCAM_018", "Work From Home YouTube Liking Deposit Scheme", "Global Media Marketing", "Recruiter Sneha", "daily guaranteed earnings of 3,500 rupees for video likes", "loss of assigned investment portfolio slot", "5,000 rupees VIP task security deposit", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
    ("SCAM_019", "Gas Pipeline Subsidy Release & Mobile QuickSupport Trap", "Indane Gas Vigilance", "Officer Kaul", "accumulated subsidy of 4,800 rupees held in pipeline", "cancellation of domestic LPG cylinder quota", "TeamViewer QuickSupport screen sharing", ["REMOTE_ACCESS_MANIPULATION", "ACCOUNT_OR_KYC_THREAT", "OTP_PIN_CVV_THEFT"]),
    ("SCAM_020", "Instant Personal Loan Approval Processing Fee Extortion", "QuickFin Lending Desk", "Officer Agarwal", "pre-approved unsecured loan of 5 lakhs sanctioned", "forfeiture of zero percent interest loan approval", "9,800 rupees insurance stamp duty fee", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
    ("SCAM_021", "Mobile SIM 5G Upgrade & Remote Screen Hijacking", "Airtel Technical Desk", "Executive Roy", "mandatory migration of 4G SIM to 5G network", "permanent SIM network deactivation tonight", "SMS forwarding code and screen sharing approval", ["REMOTE_ACCESS_MANIPULATION", "ACCOUNT_OR_KYC_THREAT", "URGENCY_OR_THREAT"]),
    ("SCAM_022", "Airline Flight Cancellation Urgent Refund Portal Trap", "IndiGo Care Desk", "Executive Bhatia", "scheduled domestic flight cancelled due to engine fault", "forfeiture of complete ticket refund value", "remote verification refund APK installation", ["MALICIOUS_LINK_OR_APP", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
    ("SCAM_023", "Defence Personnel Vehicle Advance Token Payment Fraud", "Army Cantonment Wing", "Subedar Major Gill", "urgent sale of military certified vehicle at low price", "sale to competing buyer waiting at depot", "15,000 rupees military gate pass token", ["AUTHORITY_IMPERSONATION", "FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
    ("SCAM_024", "Fake Job Appointment Letter Registration Fee Advance", "Tata Tech Recruitment", "HR Lead Nambiar", "selection as Senior Systems Engineer with 12 LPA package", "cancellation of appointment offer letter", "8,500 rupees document verification charge", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
    ("SCAM_025", "Gold Loan Default Imminent Auction Settlement Coercion", "Muthoot Asset Desk", "Manager Nair", "pending interest default on pawned gold ornaments", "public auction of family gold jewelry tomorrow", "immediate UPI transfer of overdue interest", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ACCOUNT_OR_KYC_THREAT"]),
    ("SCAM_026", "Hospital Intensive Care Emergency Cash Extortion", "City Care Hospital", "Dr. Alok", "relative admitted unconscious after highway collision", "withholding of emergency blood transfusion surgery", "25,000 rupees medical deposit via phone", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),
    ("SCAM_027", "Courier Tracking Failure Malicious APK Download", "BlueDart Logistics", "Driver Mukesh", "inability to deliver parcel due to incorrect house number", "return of parcel to sender with heavy penalty", "custom tracking APK installed from WhatsApp link", ["MALICIOUS_LINK_OR_APP", "COURIER_CUSTOMS_FRAUD", "REMOTE_ACCESS_MANIPULATION"]),

    # Validation Archetypes (28 to 33)
    ("SCAM_028", "Interpol Red Corner Notice Digital Custody Extortion", "Interpol Liaison Unit", "Officer Mukherjee", "international arrest warrant for offshore data theft", "immediate extradition and airport detention", "confidential video interrogation and clearance bond", ["DIGITAL_ARREST", "AUTHORITY_IMPERSONATION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),
    ("SCAM_029", "National Highway Toll Penalty & Vehicle Confiscation", "NHAI Legal Enforcement", "Inspector Tiwari", "toll gate sensor evasion and unpaid toll fine of 8,500", "impounding of vehicle at next police barrier", "urgent penalty payment through unofficial link", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
    ("SCAM_030", "Cyber Police Obscene Content Complaint Extortion", "Cyber Crime Women Cell", "Officer Sengupta", "obscene video call complaint registered against your phone", "filing of non-bailable public defamation charge", "case settlement fee to police welfare account", ["AUTHORITY_IMPERSONATION", "URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION"]),
    ("SCAM_031", "Cryptocurrency Investment Guaranteed Double Return Trap", "BitPro Wealth Advisory", "Trader Aryan", "algorithmic Bitcoin trading giving 200% return in 24 hours", "expiration of guaranteed profit multiplier window", "initial investment deposit of 20,000 rupees", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
    ("SCAM_032", "Wedding Hall Booking Cancellation Immediate Refund Trap", "Grand Palace Bookings", "Manager Joshi", "accidental double charge for banquet hall reservation", "blocking of total booking advance", "Google Pay refund scan requiring UPI PIN entry", ["FINANCIAL_REDIRECTION", "OTP_PIN_CVV_THEFT"]),
    ("SCAM_033", "Overseas University Visa Bond Emergency Transfer", "Consulate Visa Cell", "Officer David", "student visa documentation discrepancy for dependent child", "immediate deportation and visa cancellation", "embassy security deposit transfer", ["URGENCY_OR_THREAT", "FINANCIAL_REDIRECTION", "ISOLATION_OR_PSYCHOLOGICAL_PRESSURE"]),

    # Test Archetypes (34 to 39)
    ("SCAM_034", "Toll Plaza Dispute Settlement Screen Control Coercion", "FASTag Dispute Cell", "Officer Kapoor", "double deduction dispute at toll plaza requiring refund", "forfeiture of disputed amount and toll fine", "AnyDesk remote screen inspection to verify wallet", ["REMOTE_ACCESS_MANIPULATION", "FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
    ("SCAM_035", "Government Healthcare Subsidy Portal Fake App Trap", "Ayushman Bharat Desk", "Officer Patel", "government health insurance reimbursement of 50,000 approved", "lapse of government medical subsidy funds", "custom healthcare APK download from SMS", ["MALICIOUS_LINK_OR_APP", "FINANCIAL_REDIRECTION", "AUTHORITY_IMPERSONATION"]),
    ("SCAM_036", "Insurance Bonus Settlement AnyDesk Verification Scam", "LIC Claims Division", "Officer Tripathi", "accrued life insurance loyalty bonus of 2.1 lakhs", "forfeiture of accumulated policy maturity bonus", "AnyDesk code sharing to verify bank passbook", ["REMOTE_ACCESS_MANIPULATION", "OTP_PIN_CVV_THEFT", "FINANCIAL_REDIRECTION"]),
    ("SCAM_037", "Gas Cylinder Booking Express Verification Fee Fraud", "HP Gas Distributor", "Officer Yadav", "cylinder delivery delayed due to pending safety verification", "permanent suspension of residential gas connection", "advance safety token payment via unknown link", ["FINANCIAL_REDIRECTION", "OTP_PIN_CVV_THEFT", "URGENCY_OR_THREAT"]),
    ("SCAM_038", "School Tuition Fee Payment Gateway Interception Trap", "Delhi Public School Accounts", "Cashier Mohan", "pending school tuition installment for current semester", "removal of student name from examination roster", "direct transfer to private accountant UPI handle", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
    ("SCAM_039", "Fake Anti-Virus Subscription Renewal & Remote Refund Scam", "Global Cyber Defender", "Tech Lead Peter", "automatic annual renewal fee of 24,000 charged to account", "non-refundable auto-debit if not cancelled in 1 hour", "TeamViewer remote connection to process refund", ["REMOTE_ACCESS_MANIPULATION", "FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT"]),
    ("SCAM_040", "Telecom Tower Land Lease Advance Registration Fee Fraud", "Tower Infrastructure Cell", "Officer Kapoor", "monthly rent of 45,000 for vacant plot mobile tower installation", "forfeiture of commercial tower installation rights", "18,000 rupees structural survey clearance deposit", ["FINANCIAL_REDIRECTION", "URGENCY_OR_THREAT", "AUTHORITY_IMPERSONATION"])
]

# 35 Distinct Legitimate Scenario Archetypes
LEGIT_ARCHETYPES = [
    # Train Archetypes (0 to 23)
    ("LEGIT_001", "Bank Official Branch Visit Invitation for Annual KYC Review", "HDFC Bank MG Road", "Priya", "annual KYC document verification at branch", "bring original Aadhaar and PAN to branch counter"),
    ("LEGIT_002", "Routine Outpatient Health Clinic Appointment Reminder", "Apollo Clinic", "Staff Sister Mary", "scheduled routine preventive health checkup tomorrow at 10 AM", "fasting 8 hours prior to blood test"),
    ("LEGIT_003", "E-Commerce Logistics Package Out for Delivery Confirmation", "BlueDart Logistics", "Courier Ramesh", "Amazon delivery out for delivery today", "leave parcel with building security guard"),
    ("LEGIT_004", "Bank Educational Advisory on Never Sharing One Time Passwords", "State Bank of India Security", "Advisory Voice", "RBI cyber awareness campaign reminder", "never share OTP, ATM PIN, or passwords with anyone"),
    ("LEGIT_005", "Automobile Service Center Scheduled Maintenance Readiness", "Tata Motors Service", "Advisor Sunil", "regular vehicle periodic servicing ready for inspection", "drop vehicle at workshop tomorrow morning"),
    ("LEGIT_006", "Indian Railways Official PNR Seat Confirmation Status", "IRCTC Support", "Helpdesk Sunita", "confirmation of train 12724 seat allotment in B2 coach", "travel with valid government photo ID"),
    ("LEGIT_007", "City Gas Pipeline Routine Kitchen Safety Inspection Scheduling", "Indraprastha Gas Limited", "Technician Amit", "routine annual kitchen pipeline leak inspection", "technician carrying official company badge will visit on Saturday"),
    ("LEGIT_008", "University Admissions Counter Document Verification Schedule", "Osmania University Admissions", "Coordinator Lakshmi", "verification of postgraduate application marksheets", "report to administrative building counter 4 with originals"),
    ("LEGIT_009", "Public Health Clinic Routine Child Vaccination Camp Invitation", "Primary Health Center", "Nurse Anjali", "free pulse polio and MMR booster vaccination camp this Sunday", "bring child immunization yellow book"),
    ("LEGIT_010", "Laptop Service Center Warranty Part Replacement Readiness", "Lenovo Authorized Service", "Engineer Deepak", "replacement laptop screen arrived under warranty", "bring original service job-sheet to collect laptop"),
    ("LEGIT_011", "Housing Society Annual General Body Meeting Agenda Circular", "Green Valley Co-op Society", "Secretary Manoj", "annual society general body meeting this Sunday at 10 AM", "agenda copies available at society security office"),
    ("LEGIT_012", "Municipal Corporation Property Tax Payment Receipt Notice", "Greater Hyderabad Municipal Corp", "Inspector Rao", "confirmation of property tax assessment receipt", "download receipt from official municipal portal"),
    ("LEGIT_013", "Income Tax Department Official E-Filing Acknowledgment", "Income Tax Department", "E-Filing Desk", "acknowledgment of assessment year income tax e-return", "no further action required, refund processed to bank"),
    ("LEGIT_014", "Blood Bank Rare Blood Group Voluntary Donation Inquiry", "Red Cross Blood Center", "Coordinator Swathi", "shortage of O negative blood group for scheduled surgeries", "voluntary blood donation at clinic if healthy and available"),
    ("LEGIT_015", "Bookstore Customer Reserve Copy Availability & Pickup Call", "Landmark Books", "Attendant Gautam", "reserved hardback book arrived from publisher", "copy held at front desk for five business days"),
    ("LEGIT_016", "Primary School Parent Teacher Conference Slot Confirmation", "Kendriya Vidyalaya", "Class Teacher Sharma", "quarterly parent-teacher meeting regarding academic progress", "ten-minute interaction slot on Saturday at 11 AM"),
    ("LEGIT_017", "Municipal Drinking Water Pipeline Maintenance Supply Notice", "Water Supply Board", "Officer Reddy", "temporary water supply shutdown on Thursday for valve repair", "store necessary drinking water for one day"),
    ("LEGIT_018", "Bank Home Loan Clearance Certificate Dispatch Notice", "ICICI Home Finance", "Officer Kavita", "final loan clearance certificate dispatched via Speed Post", "tracking number sent by official email"),
    ("LEGIT_019", "Passport Seva Kendra Document Submission Slot Reminder", "Passport Seva Kendra", "Helpdesk Officer", "appointment tomorrow at 9:15 AM at Regional Passport Office", "carry original birth certificate and address proof"),
    ("LEGIT_020", "Corporate HR Campus Placement Onboarding Details Follow-up", "Infosys HR Operations", "Talent Lead Ananya", "joining date scheduled for first week of next month", "complete background verification portal upload"),
    ("LEGIT_021", "Veterinary Hospital Pet Annual Vaccination Due Reminder", "Cessna Pet Hospital", "Dr. George", "annual rabies and DHLPP booster due for pet dog", "book convenient slot between 10 AM and 6 PM"),
    ("LEGIT_022", "Local Public Library Book Return & Digital Renewal Guide", "Central Library", "Librarian Murthy", "two borrowed books due for return on Friday", "option to renew online via official library portal"),
    ("LEGIT_023", "Telecom Postpaid Bill Due Date Courtesy Reminder", "Jio Corporate Care", "Helpdesk Pooja", "monthly billing cycle statement generated", "convenient payment through official MyJio application"),
    ("LEGIT_024", "Life Insurance Annual Premium Receipt Confirmation Notice", "Life Insurance Corp of India", "Agent Suresh", "annual life insurance premium receipt processed", "physical premium receipt sent to registered postal address"),

    # Validation Archetypes (24 to 28)
    ("LEGIT_025", "Mutual Fund Annual Portfolio Review Branch Invitation", "SBI Mutual Fund", "Advisor Nikhil", "scheduled annual review of equity mutual fund scheme", "visit nearest branch at your convenience for discussion"),
    ("LEGIT_026", "Airlines Web Check-in Reminder & Baggage Policy Advisory", "Air India Airport Operations", "Ground Staff Tanvi", "scheduled flight departure tomorrow morning", "complete web check-in and arrive two hours before departure"),
    ("LEGIT_027", "Automobile Emission Test Renewal Courtesy Reminder", "Regional Transport Office", "Automated Notice", "pollution under control certificate expiring next week", "visit any authorized testing booth for renewal"),
    ("LEGIT_028", "State Electricity Board Peak Summer Energy Conservation", "Power Distribution Company", "Public Relations Desk", "courtesy advisory on peak summer electricity conservation", "tips on efficient AC temperature settings at 24 degrees"),
    ("LEGIT_029", "State Bank Customer Service Experience Feedback Survey", "Canara Bank Quality Desk", "Survey Officer Divya", "routine feedback on recent bank branch visit experience", "rate service quality on scale of 1 to 5"),

    # Test Archetypes (29 to 34)
    ("LEGIT_030", "Courier Delivery Address Landmark Clarification Call", "DTDC Courier Service", "Delivery Agent Imran", "clarification of apartment building wing name for envelope", "confirm landmark near residential entrance"),
    ("LEGIT_031", "Government Higher Education Scholarship Verification", "State Education Board", "Desk Officer Prasad", "verification of college scholarship eligibility records", "submit bonafide student certificate to principal office"),
    ("LEGIT_032", "Metro Rail Smart Card Automatic Top-up Receipt", "Metro Rail Corporation", "Card Service", "monthly smart card auto-debit reload successful", "smart card balance updated to 500 rupees"),
    ("LEGIT_033", "Community Charitable Eye Care Camp Invitation", "Lions Eye Institute", "Coordinator Geetha", "free community vision and cataract screening camp on Sunday", "senior citizens welcome for free eye checkup"),
    ("LEGIT_034", "Broadband Optical Fiber Upgrade Neighborhood Notice", "ACT Fibernet Tech Desk", "Technician Santosh", "scheduled fiber optic speed upgrade in neighborhood", "maintenance window between 2 PM and 4 PM with minimal downtime"),
    ("LEGIT_035", "Bank Safe Deposit Locker Annual Physical Verification", "Bank of Baroda", "Locker Incharge Neha", "annual physical inspection of safe deposit locker", "visit branch during banking hours with locker key")
]

# 25 Distinct Ambiguous Scenario Archetypes
AMBIG_ARCHETYPES = [
    # Train Archetypes (0 to 17)
    ("AMBIG_001", "Credit Card Limit Upgrade Pitch Interrupted by Network Drop", "Banking Sales Desk", "Caller Arvind", "complimentary credit card credit limit increase offer", "call dropped mid-sentence before financial details"),
    ("AMBIG_002", "Unverified Courier Delivery Incomplete Address Query", "Express Parcel Service", "Caller Vinod", "unmarked package with torn address slip requiring landmark", "recipient pushes back asking for tracking ID before confirming"),
    ("AMBIG_003", "Pre-Approved Personal Loan Cold Call with Vague Terms", "Finance Telemarketing", "Caller Rohini", "pre-approved low interest personal loan offer", "recipient asks for employee ID and official bank domain"),
    ("AMBIG_004", "Real Estate Commercial Property Cold Investment Pitch", "Apex Realty Holdings", "Caller Vikas", "commercial office space investment opportunity", "recipient declines investment calls during business hours"),
    ("AMBIG_005", "Vague Consumer Insurance Survey Inquiring on Family Size", "National Market Survey", "Caller Monica", "demographic research survey on life insurance ownership", "recipient declines to disclose household financial information"),
    ("AMBIG_006", "Wrong Number Callback from Unknown Distant Person", "Unknown Private Caller", "Caller Harish", "inquiry looking for someone named Mr. Raghunath", "recipient confirms wrong number and ends call"),
    ("AMBIG_007", "Charity Fundraiser Inquiring for Donation Without Reg ID", "Child Hope Foundation", "Caller Karuna", "appeal for donations to help underprivileged children", "recipient asks for official 80G tax exemption number and website"),
    ("AMBIG_008", "Job Placement Consultancy Walk-in Interview Query", "Tech Careers Agency", "Caller Vishal", "job profile match for mid-level administrative opening", "recipient requests job description by email before committing"),
    ("AMBIG_009", "Restaurant Food Delivery Order Quantity Discrepancy", "Swiggy Delivery Hub", "Caller Sonu", "clarification on whether order had two biryanis or three", "recipient confirms correct item count from mobile app"),
    ("AMBIG_010", "Online Electronics Extended Warranty Renewal Inquiry", "Gadget Protect Desk", "Caller Preeti", "warranty extension inquiry for washing machine purchased 2 years ago", "recipient asks caller to verify invoice number first"),
    ("AMBIG_011", "Domestic Vacation Tour Package Telemarketing Follow-up", "Holiday Paradise Tours", "Caller Naveen", "discounted Goa holiday resort package offer", "recipient states they have no vacation travel plans"),
    ("AMBIG_012", "Mobile Broadband Speed Diagnostic Disconnecting Mid-Call", "Telecom Network Support", "Caller Ravi", "routine network diagnostic following slow speed report", "call disconnects abruptly due to cellular signal drop"),
    ("AMBIG_013", "Apartment Rental Broker Seeking Tenant Background Details", "City Property Associates", "Caller Naresh", "inquiry whether residential apartment is available for rent", "recipient clarifies property is already occupied"),
    ("AMBIG_014", "Medical Insurance Cashless Hospitalization Network Inquiry", "Health First TPA", "Caller Shalini", "general inquiry regarding preferred local hospital network", "recipient asks caller to send policy brochure by post"),
    ("AMBIG_015", "Educational Course Certificate Courier Address Recheck", "Skill India Academy", "Caller Manisha", "dispatch confirmation for digital marketing course certificate", "recipient says they never enrolled in any marketing course"),
    ("AMBIG_016", "Vehicle Insurance Renewal Inquiry with Misstated Expiry", "Policy Hub Direct", "Caller Tarun", "car insurance policy allegedly expiring in three days", "recipient checks document and confirms policy is valid for 6 months"),
    ("AMBIG_017", "Retail Supermarket Loyalty Card Reward Balance Call", "Smart Mart Rewards", "Caller Varun", "inquiry on redeeming 450 reward points on next grocery bill", "recipient acknowledges message and will check in store"),
    ("AMBIG_018", "Bank Customer Care Callback Interrupted by Network Drop", "Union Bank Helpdesk", "Caller Sudha", "callback regarding earlier general inquiry on account interest", "network drops before customer can explain query"),

    # Validation Archetypes (18 to 21)
    ("AMBIG_019", "Utility Water Billing Clarification Requesting Callback", "Municipal Water Cell", "Caller Shailesh", "water bill surcharge clarification needing reference number", "caller asks recipient to call official municipal board landline"),
    ("AMBIG_020", "Event Concert Ticket Reservation Query Disconnecting", "Showtime Tickets", "Caller Tanya", "inquiry regarding pending ticket payment for music festival", "recipient states they did not book tickets and call ends"),
    ("AMBIG_021", "E-Commerce Return Pickup Driver Seeking Security Gate Entry", "Fast Track Logistics", "Driver Kanta", "pickup van outside residential gated community", "recipient instructs driver to coordinate with security guard"),
    ("AMBIG_022", "Mutual Fund KYC Verification Inquiry Lacking Folio Number", "Asset Care Registrar", "Caller Smita", "general inquiry on whether mutual fund KYC is updated", "recipient refuses to share details without caller stating folio"),

    # Test Archetypes (22 to 24)
    ("AMBIG_023", "Home Broadband Plan Change Inquiry Without Customer ID", "SpeedNet Broadband", "Caller Bharat", "inquiry regarding upgrading home internet plan to gigabit", "recipient asks caller to state registered customer ID which caller lacks"),
    ("AMBIG_024", "Courier Delivery Driver Lost in Neighborhood Seeking Directions", "City Parcel Drop", "Driver Jagdish", "driver confused between cross road 4 and cross road 5", "recipient gives clear directional landmarks near bakery"),
    ("AMBIG_025", "Health Insurance Claim Follow-up Lacking Claim Number", "MediCare Assist Desk", "Caller Archana", "follow-up inquiry on diagnostic test reimbursement status", "recipient asks for hospital claim reference which caller does not have")
]
