import React, { useState, useEffect } from 'react';
import {
  ShieldAlert, Key, Smartphone, Building2, Package, Lock,
  PhoneOff, Scale, Search, ExternalLink, ArrowRight, Activity, AlertTriangle
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/common/Card';
import { SeverityBadge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { DashboardMetrics } from '../types';

export const ThreatIntelligencePage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [selectedPillar, setSelectedPillar] = useState<string>('digital_arrest');
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    api.getDashboardMetrics().then(setMetrics).catch(console.error);
  }, []);

  const pillars = [
    {
      id: 'digital_arrest',
      name: 'Digital Arrest Patterns',
      category: 'Digital Arrest',
      severity: 'Critical',
      icon: Scale,
      tag: 'SEC-PIL-008',
      description: 'Coercive videoconference confinement claiming Supreme Court, CBI, or Cyber Police warrants. Perpetrators order continuous video surveillance and forbid call disconnection.',
      indicators: [
        'Continuous Skype / Zoom / WhatsApp video surveillance demands',
        'Claims of Supreme Court / CBI digital arrest warrants',
        'Forbidding call disconnection under penalty of physical arrest',
        'Demands to stay in a closed room with camera always turned on'
      ],
      sampleTriggers: {
        en: 'You are placed under digital arrest by Supreme Court. Turn on Skype camera right now.',
        hi: 'aap digital arrest ke tehat hain. turant skype video call par aaiye aur room lock kijiye.',
        te: 'meeru digital arrest lo unnaru. ventane video call disconnect cheyakandi.'
      },
      mitigation: 'Disconnect immediately. Indian law does NOT recognize digital arrest via video calls. Report to 1930 immediately.'
    },
    {
      id: 'credential_theft',
      name: 'Credential & OTP Harvesting',
      category: 'Credential Theft',
      severity: 'Critical',
      icon: Key,
      tag: 'SEC-PIL-003',
      description: 'Social engineering extraction of One-Time Passwords (OTPs), net banking credentials, UPI PINs, CVVs, and mobile banking passwords under false verification pretenses.',
      indicators: [
        'Urgent demands for 6-digit SMS verification code / OTP',
        'Requests for UPI PIN or ATM debit card CVV to "unblock" account',
        'Net banking login password or user ID verification pretext',
        'Claims that failure to disclose OTP will result in permanent account termination'
      ],
      sampleTriggers: {
        en: 'Read out the 6 digit OTP sent to your phone right now to stop account deactivation.',
        hi: 'aapke phone par 6 digit ka OTP aaya hoga, turant bataiye varna account block hoga.',
        te: 'mee mobile ki vachina 6 digit OTP ventane cheppandi.'
      },
      mitigation: 'Banks, telecom operators, and law enforcement NEVER request OTPs, CVVs, or UPI PINs. Never disclose codes over the phone.'
    },
    {
      id: 'remote_access',
      name: 'Remote Access Manipulation',
      category: 'Remote Access Manipulation',
      severity: 'Critical',
      icon: Smartphone,
      tag: 'SEC-PIL-004',
      description: 'Coercing victims into installing screen-sharing software (AnyDesk, TeamViewer, QuickSupport) or malicious APKs under the guise of technical support or security verification.',
      indicators: [
        'Directing victim to download AnyDesk, TeamViewer, or RustDesk',
        'Sideloading malicious Android APKs sent via WhatsApp or Telegram',
        'Demands to share 9-digit remote pairing access code',
        'Claims of technical diagnostic scan to "clean" fraudulent transactions'
      ],
      sampleTriggers: {
        en: 'Install AnyDesk app from Play Store and tell me the 9-digit pairing code to fix banking bug.',
        hi: 'Play Store se AnyDesk download kijiye aur 9 digit code bataiye.',
        te: 'Play Store nundi AnyDesk install chesi 9 digit code cheppandi.'
      },
      mitigation: 'Never install remote screen-sharing applications on instruction from callers. Sharing your code grants total device takeover.'
    },
    {
      id: 'authority_impersonation',
      name: 'Authority & Law Enforcement Impersonation',
      category: 'Authority Impersonation',
      severity: 'High',
      icon: Building2,
      tag: 'SEC-PIL-001',
      description: 'False pretenses claiming identity as CBI Officers, Cyber Crime Cells, Telecom Regulatory Authority of India (TRAI), Mumbai/Delhi Police, or Customs officials.',
      indicators: [
        'Fabricated badge numbers, police station names, and officer ranks',
        'Forged arrest orders with official government emblems',
        'Claims that victims Aadhaar card is tied to multi-crore money laundering or narcotics',
        'Threats of imminent local police raid if cooperation is withheld'
      ],
      sampleTriggers: {
        en: 'This is Inspector Vikram from Cyber Crime Cell. An FIR has been registered against your Aadhaar.',
        hi: 'Main Cyber Crime Cell se bol raha hoon, aapke naam par illegal narcotics parcel aaya hai.',
        te: 'Nenu Cyber Police station nundi matladuthunnanu, mee Aadhaar illegal transactions lo involve ayindi.'
      },
      mitigation: 'Official summons are served in writing, never issued as verbal threats over WhatsApp or voice calls. Contact local police station directly.'
    },
    {
      id: 'courier_narcotics',
      name: 'Courier & Customs Contraband Fraud',
      category: 'Courier & Customs Fraud',
      severity: 'High',
      icon: Package,
      tag: 'SEC-PIL-007',
      description: 'Fraudulent notifications alleging customs interception of parcels (FedEx, DHL, India Post) containing passports, synthetic narcotics (MDMA), or illegal currency in victims name.',
      indicators: [
        'Allegations of intercepted illegal parcel addressed to Taiwan, Thailand, or Dubai',
        'Claims that parcel contains forged passports and contraband substances',
        'Transferring call to "Customs Crime Division" or "Narcotics Control Bureau"',
        'Extortion demands for clearance fee or customs deposit'
      ],
      sampleTriggers: {
        en: 'FedEx customer service: Your parcel to Taiwan has been seized containing 140 grams of MDMA.',
        hi: 'FedEx courier se bol rahe hain, aapka parcel customs ne rok liya hai jisme drugs mile hain.',
        te: 'FedEx nundi call chestunnamu, mee parcel lo narcotics dorikinayi.'
      },
      mitigation: 'Courier companies do not transfer calls to police divisions. Verify tracking numbers on official carrier websites.'
    },
    {
      id: 'financial_redirection',
      name: 'Financial Redirection & Safe Accounts',
      category: 'Financial Redirection',
      severity: 'High',
      icon: Lock,
      tag: 'SEC-PIL-005',
      description: 'Coercing victims into transferring personal savings to "Reserve Bank of India Safe Verification Accounts" or government escrow to avoid asset seizure.',
      indicators: [
        'Instructions to transfer funds via RTGS/NEFT to third-party bank accounts for "verification"',
        'False promises that transferred funds will be refunded within 15 minutes after clearance',
        'Liquidating fixed deposits or mutual funds under regulatory intimidation',
        'Prohibiting disclosure of transfer purpose to branch bank managers'
      ],
      sampleTriggers: {
        en: 'Transfer your bank balance to the RBI Reserve Escrow account for safety clearance.',
        hi: 'Apne saare paise RBI ke safe government account mein transfer kijiye verification ke liye.',
        te: 'Mee money antha RBI safe account ki transfer cheyandi, verification taruvatha refund avthundi.'
      },
      mitigation: 'No government agency or RBI operates "safe accounts" for fund transfers. Any demand to transfer money is guaranteed fraud.'
    },
    {
      id: 'psychological_isolation',
      name: 'Psychological Isolation & Coercion',
      category: 'Psychological Isolation',
      severity: 'Medium',
      icon: PhoneOff,
      tag: 'SEC-PIL-006',
      description: 'Threats preventing victims from seeking advice from family, advocates, or bank managers to ensure uninterrupted cognitive manipulation.',
      indicators: [
        'Strict instructions not to tell spouse, parents, or colleagues',
        'Claims of Official Secrets Act violations if call details are shared',
        'Ordering victim to stay locked inside a private room without consulting anyone',
        'Rapid speech cadence and high-pressure artificial deadlines'
      ],
      sampleTriggers: {
        en: 'This is an official state secret inquiry. If you tell your family you will be charged with obstruction.',
        hi: 'Is baare mein kisi ko mat batana, ye national security ka matter hai.',
        te: 'Ee vishayam evariki cheppakandi, national security case idi.'
      },
      mitigation: 'Take a breath. Legitimate authorities never demand total secrecy from family or legal counsel. Immediately consult trusted contacts.'
    }
  ];

  const filteredPillars = pillars.filter(
    (p) =>
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const currentPillar = pillars.find((p) => p.id === selectedPillar) || pillars[0];
  const Icon = currentPillar.icon;

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 font-mono text-xs mb-1">
            <Activity className="w-4 h-4" />
            <span>KAVACH AI SOC THREAT INTELLIGENCE MATRIX</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100">
            Voice Scam & Vishing Tactic Repository
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Forensic analysis of the 8 primary voice social-engineering attack pillars monitored by the KAVACH AI Hybrid Detection Engine across regional Indian languages.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link to="/analyze">
            <Button variant="primary" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
              Test Live Audio
            </Button>
          </Link>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Tactic Selector (5 cols) */}
        <div className="lg:col-span-5 space-y-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Filter threat tactics..."
              className="w-full bg-[#0d1424] text-xs text-slate-200 placeholder:text-slate-500 rounded-lg pl-9 pr-4 py-2 border border-slate-800 focus:border-cyan-500 focus:outline-none"
            />
          </div>

          <div className="space-y-2 max-h-[640px] overflow-y-auto pr-1">
            {filteredPillars.map((pillar) => {
              const PIcon = pillar.icon;
              const isSelected = pillar.id === selectedPillar;
              const occurrenceCount = metrics?.threat_category_distribution?.[pillar.category] ?? 0;

              return (
                <div
                  key={pillar.id}
                  onClick={() => setSelectedPillar(pillar.id)}
                  className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-[#131c31] border-cyan-500/50 shadow-md shadow-cyan-950/30'
                      : 'bg-[#0d1424] border-slate-800/80 hover:border-slate-700 hover:bg-[#10192e]'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center space-x-2.5">
                      <div className={`p-2 rounded-lg ${isSelected ? 'bg-cyan-500/20 text-cyan-400' : 'bg-slate-800/60 text-slate-400'}`}>
                        <PIcon className="w-4 h-4" />
                      </div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="text-xs font-semibold text-slate-200">{pillar.name}</span>
                          <span className="font-mono text-[10px] text-slate-500">{pillar.tag}</span>
                        </div>
                        <p className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">{pillar.description}</p>
                      </div>
                    </div>
                    <SeverityBadge severity={pillar.severity} size="xs" />
                  </div>

                  <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-800/40 text-[10px] font-mono text-slate-400">
                    <span>Incidents Logged: <b className="text-slate-200">{occurrenceCount}</b></span>
                    <span className="text-cyan-400 flex items-center">Inspect <ArrowRight className="w-2.5 h-2.5 ml-0.5" /></span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Detail Dossier (7 cols) */}
        <div className="lg:col-span-7">
          <Card elevated className="h-full border-slate-700/60">
            <CardHeader className="bg-slate-900/40">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2.5 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                    <Icon className="w-6 h-6" />
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <CardTitle className="text-lg text-slate-100">{currentPillar.name}</CardTitle>
                      <SeverityBadge severity={currentPillar.severity} size="sm" />
                    </div>
                    <CardDescription className="font-mono text-cyan-400 text-xs">
                      Category: {currentPillar.category} · Reference: {currentPillar.tag}
                    </CardDescription>
                  </div>
                </div>
              </div>
            </CardHeader>

            <CardContent className="space-y-5 p-6">
              {/* Overview */}
              <div>
                <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">Tactic Threat Profile</h4>
                <p className="text-xs text-slate-200 leading-relaxed bg-[#0a0f1c] p-3.5 rounded-lg border border-slate-800">
                  {currentPillar.description}
                </p>
              </div>

              {/* Forensic Indicators */}
              <div>
                <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">Forensic Signatures & Indicators</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {currentPillar.indicators.map((ind, i) => (
                    <div key={i} className="flex items-start space-x-2 p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/80 text-xs text-slate-300">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                      <span>{ind}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Multilingual Speech Triggers */}
              <div>
                <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">Multilingual Speech Signatures</h4>
                <div className="space-y-2 font-mono text-xs">
                  <div className="p-3 rounded-lg bg-[#070b14] border border-slate-800">
                    <div className="text-[10px] text-cyan-400 mb-1 font-semibold">ENGLISH SIGNATURE:</div>
                    <p className="text-slate-200 italic">"{currentPillar.sampleTriggers.en}"</p>
                  </div>
                  <div className="p-3 rounded-lg bg-[#070b14] border border-slate-800">
                    <div className="text-[10px] text-teal-400 mb-1 font-semibold">HINDI SIGNATURE (हिंदी):</div>
                    <p className="text-slate-200 italic">"{currentPillar.sampleTriggers.hi}"</p>
                  </div>
                  <div className="p-3 rounded-lg bg-[#070b14] border border-slate-800">
                    <div className="text-[10px] text-purple-400 mb-1 font-semibold">TELUGU SIGNATURE (తెలుగు):</div>
                    <p className="text-slate-200 italic">"{currentPillar.sampleTriggers.te}"</p>
                  </div>
                </div>
              </div>

              {/* SOC Defense Advisory */}
              <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30">
                <h4 className="text-xs font-bold text-emerald-400 flex items-center space-x-1.5 mb-1.5">
                  <ShieldAlert className="w-4 h-4" />
                  <span>SOC Recommended Countermeasure</span>
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {currentPillar.mitigation}
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

