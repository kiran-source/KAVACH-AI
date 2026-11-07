"""
Generator for LEGIT_DATA in KAVACH AI Synthetic Dataset v3.
Constructs 145 distinct, diverse LEGITIMATE scenario families across 10 categories.
Includes benign conversations that discuss banking, OTPs, police, deliveries, and account security.
"""

import json
from pathlib import Path

LEGIT_CATEGORIES = [
    # 1. Normal Banking Enquiries & Service Notifications (22)
    ("BANKING_SERVICE", 22, [
        ("HDFC Bank MG Road", "Priya", "Annual KYC document verification at branch", "Bring original Aadhaar and PAN to branch counter"),
        ("State Bank of India", "Branch Manager Ramesh", "Fixed deposit maturity renewal options advisory", "Visit nearest branch or renew online via official YONO portal"),
        ("ICICI Home Finance", "Officer Kavita", "Home loan interest rate benchmark reduction notification", "Review revised EMI amortization schedule in netbanking"),
        ("Axis Bank Card Operations", "Executive Amit", "New EMV contactless debit card courier dispatch tracking", "Card dispatched via speed post, set ATM PIN via mobile app"),
        ("Bank of Baroda", "Locker Incharge Neha", "Annual physical verification of safe deposit locker", "Visit branch during banking hours with primary locker key"),
        ("Canara Bank Operations", "Helpdesk Divya", "New chequebook request processed and dispatched", "Track registered speed post parcel using sent tracking ID"),
        ("Punjab National Bank", "Officer Baldev", "Senior citizen savings scheme interest credit confirmation", "Interest credited directly to linked savings account"),
        ("Kotak Mahindra Bank", "Advisor Nikhil", "Mutual fund annual systematic investment portfolio review", "Visit branch at your convenience for mutual fund advisory"),
        ("Union Bank of India", "Helpdesk Pooja", "Dormant account reactivation guidance", "Submit basic identity proof at home branch to reactivate"),
        ("IndusInd Bank", "Officer Shalini", "Complimentary airport lounge access feature update on credit card", "Terms updated on bank website, no fee charged"),
        ("Federal Bank", "Manager Thomas", "NRE account annual foreign currency remittance tax advisory", "Consult registered chartered accountant or bank foreign exchange desk"),
        ("IDFC First Bank", "Executive Sameer", "Monthly savings account interest payout statement dispatched", "Check digital bank statement received on registered email"),
        ("Indian Bank", "Officer Senthil", "Agricultural crop loan subsidy documentation checklist", "Submit harvest verification certificate at rural branch"),
        ("Central Bank of India", "Cashier Mohan", "Demand draft collection notification for university fee", "Collect physical draft from branch counter during business hours"),
        ("Bank of India", "Executive Rajesh", "Savings account branch transfer confirmation to new city", "Branch code updated successfully in core banking system"),
        ("RBL Bank", "Advisor Tanvi", "Credit card annual renewal fee reversal confirmation", "Annual fee reversed on account of qualifying annual spend"),
        ("Yes Bank", "Officer Tarun", "Fixed deposit interest certificate dispatched for tax filing", "Download digital TDS certificate from secure portal"),
        ("UCO Bank", "Manager Ghosh", "Pension disbursement date advisory for national holiday week", "Pension will be credited two business days in advance"),
        ("Standard Chartered", "Relationship Manager David", "Priority banking relationship officer introduction", "Available on branch direct line for banking assistance"),
        ("South Indian Bank", "Helpdesk Varghese", "Mobile banking alert activation confirmation", "Daily SMS transaction alerts successfully activated"),
        ("Karnataka Bank", "Officer Prasad", "Term deposit nomination update acknowledgment", "Nominee name updated in bank central records"),
        ("City Union Bank", "Cashier Raman", "Passbook replacement completed at counter", "Old passbook cancelled and new magnetic strip passbook issued")
    ]),

    # 2. Genuine Account Security & Fraud Awareness Calls (18)
    ("FRAUD_AWARENESS", 18, [
        ("State Bank of India Cyber Cell", "Advisory Voice", "RBI national cybersecurity awareness campaign notice", "Bank never requests OTP, PIN, or CVV over voice calls or SMS"),
        ("HDFC Bank Fraud Prevention Unit", "Officer Vikram", "Verification inquiry regarding recent high-value card transaction", "If not initiated, immediately block card in mobile app; do not share card details"),
        ("ICICI Bank Security Monitoring", "Supervisor Sneha", "Automated alert regarding login attempt from alternate browser", "If unauthorized, reset netbanking password on official website"),
        ("Axis Bank Vigilance Wing", "Officer Alok", "Educational reminder on recent electricity bill APK phishing scams", "Never download APK files from unknown WhatsApp or SMS links"),
        ("Punjab National Bank Security", "Officer Jagjit", "Advisory on avoiding unauthorized biometric Aadhaar sharing", "Lock Aadhaar biometrics using official UIDAI mAadhaar application"),
        ("Bank of Baroda Anti-Fraud Cell", "Manager Joshi", "Notice regarding fake lottery and prize call rackets", "Report unsolicited lottery winning calls to cybercrime portal 1930"),
        ("Canara Bank Security Desk", "Helpdesk Swamy", "Educational advisory regarding AnyDesk and remote screen scam methods", "Never install remote screen sharing apps on caller instructions"),
        ("Kotak Mahindra Fraud Desk", "Officer Vivek", "Notification of suspicious merchant transaction block", "Card automatically blocked by system, replacement dispatched to address"),
        ("Union Bank Security Cell", "Officer Pandey", "Advisory on fake customer support helpline numbers on Google Search", "Always verify official bank telephone numbers from printed passbook"),
        ("Airtel Telecom Vigilance", "Officer Goyal", "Educational reminder on fake SIM deactivation threat calls", "Telecom companies never threaten 2-hour disconnection over voice call"),
        ("Jio Security Advisory", "Supervisor Roy", "National consumer advisory on WhatsApp video call blackmail tactics", "Block and report unknown video calls demanding money to police"),
        ("Paytm Consumer Trust", "Executive Sharma", "Wallet security reminder regarding fake KYC unfreeze calls", "Paytm agents will never ask you to transfer money to keep wallet active"),
        ("PhonePe Trust & Safety", "Helpdesk Rahul", "Educational broadcast explaining UPI collect request mechanics", "Entering UPI PIN always deducts money; never enter PIN to receive funds"),
        ("Google Pay Security Desk", "Advisor Aman", "Advisory on QR code scam tactics", "Scanning a QR code is only for paying, never for receiving cashback prizes"),
        ("Cyber Crime Prevention Cell", "Inspector Ramanathan", "Public awareness initiative on digital arrest extortion techniques", "No law enforcement agency conducts digital arrest or court trials over Skype"),
        ("Income Tax Department Outreach", "Officer Saxena", "Public clarification regarding fraudulent tax refund email links", "Check legitimate refund status solely on official e-filing portal incometax.gov.in"),
        ("TRAI Consumer Advisory", "Director Kulkarni", "Advisory on unsolicited calls threatening telecom blacklisting", "TRAI does not disconnect individual consumer mobile connections"),
        ("National Cyber Crime Reporting", "Helpdesk Officer", "Consumer guidance on using national helpline 1930", "Report cyber financial fraud within the golden hour to freeze stolen funds")
    ]),

    # 3. Genuine Customer Support & Field Technician Visits (20)
    ("CUSTOMER_SUPPORT", 20, [
        ("ACT Fibernet Tech Desk", "Technician Santosh", "Scheduled fiber optic cable upgrade and router speed check", "Technician carrying official company badge will visit on Saturday"),
        ("Lenovo Authorized Service", "Engineer Deepak", "Warranty replacement laptop motherboard arrived at service hub", "Bring original job-sheet receipt to collect repaired device"),
        ("Tata Motors Service Center", "Advisor Sunil", "Vehicle periodic maintenance service completed", "Vehicle ready for pickup at showroom service bay"),
        ("Indraprastha Gas Limited", "Technician Amit", "Routine annual kitchen piped natural gas safety inspection", "Technician in uniform will inspect pipe valves for gas leaks"),
        ("Samsung Electronics Service", "Technician George", "Washing machine water inlet valve warranty replacement", "Technician arriving between 2 PM and 4 PM at residence"),
        ("LG Customer Care Support", "Coordinator Anita", "Air conditioner seasonal preventive service appointment booking", "Confirm date and time slot for technician visit"),
        ("Urban Company Home Services", "Service Partner Ravi", "Booked bathroom cleaning service arrival notification", "Service partner is at the apartment security gate"),
        ("Airtel Broadband Technical", "Engineer Manoj", "Broadband internet latency report resolution confirmation", "Speed restored to 200 Mbps, rate service quality on mobile app"),
        ("Whirlpool Appliance Care", "Technician Suresh", "Refrigerator compressor routine warranty inspection", "Visit scheduled for tomorrow morning"),
        ("Sony Service Center", "Executive Tanvi", "Television wall-mount bracket re-installation visit confirmation", "Confirm availability at registered residence address"),
        ("Voltas AC Service Hub", "Supervisor Alok", "Summer AC cooling tune-up scheduled visit confirmation", "Technician carrying company identification ID card"),
        ("Blue Star Commercial Coolers", "Technician Dinesh", "Water dispenser filter cartridge replacement visit", "Replacement parts covered under annual maintenance contract"),
        ("Eureka Forbes Aquaguard", "Engineer Naresh", "RO water purifier annual filter cartridge replacement", "Filter membrane replaced under annual service contract"),
        ("Carrier Midea Service", "Technician Jagdish", "Inverter AC gas pressure check and filter wash", "Technician will arrive with official service docket"),
        ("Bosch Appliance Support", "Advisor Shalini", "Dishwasher rinse aid dispenser replacement parts readiness", "Schedule technician visit for part fitting"),
        ("HP Service Hub", "Engineer Rohit", "Printer laser toner replacement delivered at front desk", "Collect toner cartridge from authorized center"),
        ("Godrej Security Solutions", "Technician Harish", "Electronic home digital safe battery replacement check", "Free periodic warranty check of digital locking mechanism"),
        ("Kent RO Water Systems", "Technician Prakash", "TDS mineral level water quality testing visit", "Complimentary water quality testing for residential customer"),
        ("Daikin Air Conditioning", "Engineer Kevin", "VRV indoor unit air filter cleaning scheduled appointment", "Technician visit confirmed for Monday 11 AM"),
        ("Hitachi Home Appliances", "Advisor Megha", "Refrigerator door gasket seal replacement appointment", "Technician carrying genuine spare replacement seal")
    ]),

    # 4. Routine Courier & Package Delivery Updates (18)
    ("COURIER_DELIVERY", 18, [
        ("BlueDart Logistics", "Courier Ramesh", "Amazon package out for delivery today", "Confirm if parcel can be handed to apartment building security guard"),
        ("DTDC Courier Service", "Delivery Agent Imran", "Clarification of apartment building wing name for envelope", "Confirm landmark near residential entrance gate"),
        ("Amazon Delivery Network", "Associate Vinod", "Delivery package arrival window notification", "Arriving in 15 minutes at registered home address"),
        ("Flipkart Ekart Logistics", "Associate Sonu", "Cash-on-delivery package arrival confirmation", "Keep exact change of 480 rupees ready for package receipt"),
        ("India Post Speed Post", "Postman Jagdish", "Registered speed post document delivery notification", "Postman at door, recipient signature required on delivery sheet"),
        ("Swiggy Delivery Network", "Delivery Partner Sonu", "Food delivery partner inquiring on apartment tower number", "Partner at main security gate seeking directions to tower 4"),
        ("Zomato Delivery Fleet", "Partner Imran", "Restaurant food parcel arrived at gate", "Food order delivered to building lobby reception as requested"),
        ("Blinkit Quick Commerce", "Rider Manoj", "Grocery grocery order delivery in 8 minutes", "Rider reaching residential entrance gate"),
        ("Zepto Delivery Fleet", "Rider Deepak", "Morning fresh milk and vegetable delivery notification", "Order placed on doorstep basket as per delivery note"),
        ("BigBasket Logistics", "Van Driver Santosh", "Scheduled grocery slot delivery van arriving", "Van parked near visitor parking area"),
        ("Shadowfax Express", "Agent Rajesh", "E-commerce fashion apparel return pickup", "Keep packaged return parcel ready with return barcode slip"),
        ("Delhivery Courier Hub", "Driver Mukesh", "Consignment re-attempt delivery window update", "Delivery re-attempted between 4 PM and 6 PM today"),
        ("Professional Couriers", "Agent Murugan", "Legal notice parcel available for self-collection", "Consignment held at neighborhood branch office for 3 days"),
        ("Trackon Couriers Hub", "Agent Anil", "Corporate documents envelope arrival confirmation", "Handed over to authorized corporate mailroom desk"),
        ("Dunzo Delivery Express", "Rider Suresh", "Medicines delivery from local pharmacy store", "Medicines parcel handed to family member at door"),
        ("InstaCart Delivery", "Partner Vinay", "Stationery and office supply delivery confirmation", "Delivered to security desk as instructed in delivery note"),
        ("Gati Logistics", "Driver Balwant", "Heavy furniture carton delivery vehicle arrival", "Unloading furniture package at residential parking area"),
        ("FedEx Express India", "Courier David", "International commercial sample envelope delivery", "Signature obtained from corporate reception desk")
    ]),

    # 5. Normal Educational & Academic Communications (12)
    ("EDUCATION", 12, [
        ("Osmania University Admissions", "Coordinator Lakshmi", "Verification of postgraduate application marksheets", "Report to administrative building counter 4 with original certificates"),
        ("Kendriya Vidyalaya School", "Class Teacher Sharma", "Quarterly parent-teacher meeting regarding academic progress", "Ten-minute interaction slot on Saturday at 11 AM"),
        ("Delhi University Registry", "Helpdesk Officer", "Undergraduate degree certificate collection schedule", "Collect original convocation degree certificate from examination hall"),
        ("Indian Institute of Technology", "Academic Cell Rao", "Graduate seminar registration and schedule confirmation", "Orientation program begins Monday 9 AM at main auditorium"),
        ("Central Library", "Librarian Murthy", "Two borrowed reference books due for return on Friday", "Option to renew borrowing online via official library web portal"),
        ("State Education Board", "Desk Officer Prasad", "Verification of college scholarship eligibility records", "Submit bonafide student certificate to college principal office"),
        ("Coaching Institute Hub", "Advisor Alok", "Weekend mock entrance examination timings announcement", "Mock test commences Sunday at 10 AM; bring admit card"),
        ("Pre-School Daycare Center", "Director Geetha", "Annual kindergarten sports day and costume circular", "Event scheduled for next Friday morning in school grounds"),
        ("Music & Arts Academy", "Instructor Swathi", "Classical vocal music quarterly grading examination slot", "Performance exam slot scheduled for Sunday afternoon"),
        ("Foreign Language Institute", "Coordinator David", "German language B1 certification class schedule confirmation", "Classes will be conducted in online audio-visual classroom"),
        ("IGNOU Regional Study Center", "Assistant Manoj", "Distance learning term-end assignment submission reminder", "Submit handwritten assignments before month-end deadline"),
        ("School Bus Transport Wing", "Supervisor Ramesh", "School bus morning pickup route timing adjustment", "Bus will arrive five minutes earlier starting Monday due to road work")
    ]),

    # 6. Genuine Job Recruitment & HR Outreach (15)
    ("JOB_RECRUITMENT", 15, [
        ("Infosys HR Operations", "Talent Lead Ananya", "Joining date scheduled for first week of next month", "Complete background verification documents upload on official corporate portal"),
        ("Tata Consultancy Services", "Recruiter Arvind", "Preliminary 20-minute telephonic technical screening interview", "Discussion on current tech stack, notice period, and CTC expectations"),
        ("Wipro Talent Acquisition", "Executive Deepa", "Scheduling second round system design interview with engineering manager", "Interview scheduled on Microsoft Teams with sent calendar invite"),
        ("Accenture HR Operations", "Recruiter Manish", "Offer letter acceptance acknowledgment and onboarding checklist", "Review official employment terms sent from accenture.com domain"),
        ("HCL Tech Recruitment", "HR Partner Sneha", "Discussion regarding joining location preference and relocation assistance", "Indicate preferred base location among Bangalore, Pune, or Noida"),
        ("Tech Mahindra Careers", "Recruiter Rohit", "Reference check coordinator reaching out for past manager contacts", "Provide official email address of previous supervisor for verification"),
        ("L&T Technology Services", "HR Lead Vikram", "Candidate document verification for engineering consultant vacancy", "Upload educational degree certificates on corporate career portal"),
        ("Cognizant HR Staffing", "Talent Advisor Priya", "Clarification regarding notice period duration and buyout feasibility", "Confirm if current employer allows 30-day notice buyout"),
        ("Mindtree Talent Team", "Recruiter Suresh", "Annual performance review and campus onboarding date confirmation", "Joining batch scheduled for mid-July at corporate campus"),
        ("Capgemini India HR", "Executive Tanvi", "Discussion on compensation breakdown and variable pay structure", "Review formal compensation annexure dispatched to candidate email"),
        ("Deloitte Advisory Recruitment", "Talent Lead Alex", "Partner round interview invitation for management consulting role", "Confirm availability for in-person interview at regional office"),
        ("EY Global Delivery Services", "Recruiter Divya", "Confirmation of candidate application for senior tax analyst vacancy", "Shortlisted candidate interview scheduled for Thursday afternoon"),
        ("Amazon Development Center", "Technical Recruiter Peter", "Coding assessment completion confirmation and onsite loop scheduling", "Onsite technical interview loop scheduled across two half-days"),
        ("Microsoft India R&D", "Staffing Lead Priya", "Initial recruiter connect regarding software engineer opening in Azure", "Discuss technical background and project experience over phone"),
        ("Google India Operations", "Recruiter Sonia", "Scheduling technical phone screen with staff software engineer", "Google Meet link dispatched to candidate personal email")
    ]),

    # 7. Routine Government & Municipal Information (12)
    ("GOVERNMENT_MUNICIPAL", 12, [
        ("Passport Seva Kendra", "Helpdesk Officer", "Appointment tomorrow at 9:15 AM at Regional Passport Office", "Carry original birth certificate, Aadhaar, and education proof"),
        ("Greater Hyderabad Municipal Corp", "Inspector Rao", "Confirmation of annual property tax assessment receipt", "Download official payment receipt from municipal web portal"),
        ("Income Tax Department", "E-Filing Desk", "Acknowledgment of assessment year income tax electronic return", "Return successfully verified; refund processed to registered bank account"),
        ("Water Supply & Sewerage Board", "Officer Reddy", "Temporary water supply shutdown on Thursday for valve repair", "Store necessary drinking water for one day during maintenance"),
        ("Regional Transport Office", "Automated Notice", "Pollution under control certificate expiring next week", "Visit any authorized vehicular emission testing booth for renewal"),
        ("Aadhaar Seva Kendra", "Supervisor Hegde", "Aadhaar address update appointment confirmation", "Report to Seva Kendra counter at 11:30 AM with original utility bill"),
        ("State Electricity Board", "Public Relations Desk", "Scheduled daytime power maintenance in residential sector", "Power supply shutdown from 10 AM to 2 PM for transformer upkeep"),
        ("Election Commission of India", "Booth Level Officer", "Routine residential verification for electoral roll revision", "Officer will visit residential colony to check voter register names"),
        ("Municipal Health Department", "Inspector Deshmukh", "Neighborhood mosquito fogging and dengue prevention drive", "Keep apartment windows closed during fogging spray in evening"),
        ("Department of Posts", "Postal Assistant Sunita", "Public Provident Fund annual statement printed and ready", "Collect stamped physical passbook from local sub-post office"),
        ("Civil Supplies Department", "Inspector Patil", "Fair price ration shop monthly distribution schedule", "Ration distribution counter open daily from 9 AM to 6 PM"),
        ("State Transport Corporation", "Helpdesk Officer", "Intercity express bus schedule revision notice", "Morning bus departure moved 15 minutes earlier due to expressway work")
    ]),

    # 8. Normal Family, Personal & Social Calls (12)
    ("PERSONAL_FAMILY", 12, [
        ("Family Relative", "Uncle Raghunath", "Family wedding travel coordination and hotel reservations", "Coordinating arrival times at railway station for family marriage"),
        ("Parents at Hometown", "Mother Shanta", "Weekly health checkup update and grocery coordination", "Mother asking about office work, health, and festival vacation dates"),
        ("College Alumni Network", "Friend Harish", "Planning weekend college reunion dinner get-together", "Confirming restaurant table booking for ten batchmates"),
        ("Sibling Coordination", "Brother Rajesh", "Discussing festival train ticket reservations and return dates", "Coordinating festival travel arrangements and gift purchases"),
        ("Residential Neighbor", "Neighbor Sharma", "Borrowing ladder for balcony plant pruning", "Asking if spare ladder can be borrowed for one hour"),
        ("Apartment Housing Society", "Secretary Manoj", "Annual society general body meeting this Sunday at 10 AM", "Agenda copies available at residential security gate office"),
        ("School Friend", "Friend Anjali", "Catching up on recent career transition and newborn child", "Sharing life updates and planning casual coffee meetup"),
        ("Cousin from Abroad", "Cousin Siddharth", "Inquiring about tourist spots to visit during upcoming India vacation", "Recommending historical monuments and pleasant hill station trip"),
        ("Family Doctor", "Dr. George", "Routine blood pressure checkup follow-up call", "Doctor advising to continue prescribed morning walk and dietary care"),
        ("Local Book Club", "Organizer Gautam", "Monthly book discussion meetup topic announcement", "This month's novel discussion scheduled for Saturday afternoon"),
        ("Sports Badminton Club", "Partner Rohit", "Booking indoor wooden court for Saturday morning badminton match", "Confirming 7 AM court reservation at sports complex"),
        ("Building Resident Welfare", "Member Kavita", "Arranging residential society Diwali festival decorations", "Volunteers gathering at society clubhouse on Saturday evening")
    ]),

    # 9. Genuine Business, B2B & Merchant Interactions (10)
    ("BUSINESS_B2B", 10, [
        ("Commercial Vendor Supply", "Vendor Sunil", "Formal commercial project quotation follow-up", "Checking if technical specification document was received"),
        ("Chartered Accountancy Firm", "CA Alok Mehra", "Quarterly GST return filing deadline courtesy reminder", "Send input tax credit invoices before 20th of the month"),
        ("Freelance Web Studio", "Designer Tanvi", "Discussion regarding client feedback on website homepage draft mockups", "Implementing revised color scheme and logo layout as requested"),
        ("Logistics Freight Partner", "Manager Balwant", "Industrial raw material pallet shipment arrival date confirmation", "Consignment dispatched by container truck, arriving Wednesday"),
        ("Corporate Travel Agency", "Travel Agent Deepa", "Flight and hotel itinerary dispatch for executive business trip", "E-tickets and hotel reservation vouchers emailed to travel desk"),
        ("Legal Advisory Chambers", "Advocate Tandon", "Draft commercial lease agreement ready for mutual review", "Review lease terms before scheduled notarization meeting"),
        ("Printing Press Works", "Printer Mahesh", "Corporate annual report brochures printed and ready for pickup", "Delivery vehicle dispatching printed copies to corporate office"),
        ("Office Stationery Supplier", "Supplier Suresh", "Quarterly office printing paper and stationery dispatch confirmation", "Items delivered to ground floor corporate loading bay"),
        ("Hardware Equipment Rental", "Vendor Dinesh", "Audio-visual projector rental confirmation for corporate townhall", "Technician will set up projector screen in conference hall"),
        ("Commercial Pest Control", "Supervisor Naresh", "Quarterly office premises sanitization and pest management visit", "Service team scheduled to arrive Saturday after office hours")
    ]),

    # 10. Healthcare & Diagnostic Center Follow-ups (6)
    ("HEALTHCARE", 6, [
        ("Apollo Clinic Diagnostic", "Sister Mary", "Scheduled routine preventive health checkup reminder", "Fasting 8 hours prior to morning blood sample collection"),
        ("Dr. Lal PathLabs", "Coordinator Swathi", "Home blood sample collection technician arrival window", "Phlebotomist arriving between 7:30 AM and 8:30 AM at home"),
        ("Dental Care Clinic", "Dr. Alok Verma", "Six-month routine dental cleaning and scaling appointment", "Confirming appointment slot for tomorrow afternoon at 4 PM"),
        ("Red Cross Blood Center", "Coordinator Lakshmi", "Shortage of O-negative blood group for scheduled emergency surgeries", "Voluntary blood donation at clinic if healthy and available"),
        ("City Eye Care Institute", "Coordinator Geetha", "Annual eye vision screening and spectacle power checkup reminder", "Routine annual vision test reminder for contact lens user"),
        ("Orthopedic Physiotherapy Center", "Physiotherapist Priya", "Post-fracture rehabilitation exercise progress review", "Confirming slot for weekly strengthening therapy session")
    ])
]

# Assign sequential IDs from LEGIT_V3_001 to LEGIT_V3_145
legit_records = []
counter = 1

for cat_code, expected_count, scenarios in LEGIT_CATEGORIES:
    for org, caller, topic, resolution in scenarios[:expected_count]:
        l_id = f"LEGIT_V3_{counter:03d}"
        l_name = f"{org} - {topic[:45]}"
        turn_count = 4 if counter % 5 == 1 else 6 if counter % 5 == 2 else 8 if counter % 5 == 3 else 10 if counter % 5 == 4 else 12
        legit_records.append({
            "id": l_id,
            "name": l_name,
            "category": "LEGITIMATE",
            "sub_category": cat_code,
            "caller_org": org,
            "caller_name": caller,
            "topic": topic,
            "resolution": resolution,
            "turn_count": turn_count
        })
        counter += 1

print(f"Total LEGIT scenario archetypes generated: {len(legit_records)}")
assert len(legit_records) == 145, f"Expected 145 legit records, got {len(legit_records)}"

out_path = Path(__file__).resolve().parent / "dataset_definitions_v3" / "legit_data.py"
with open(out_path, "w", encoding="utf-8") as f:
    f.write('"""Autogenerated 145 Distinct LEGITIMATE Scenario Archetypes for KAVACH AI v3"""\n\n')
    f.write("LEGIT_DATA = " + json.dumps(legit_records, indent=2, ensure_ascii=False) + "\n")

print(f"Wrote {len(legit_records)} LEGITIMATE scenario records to {out_path}")

