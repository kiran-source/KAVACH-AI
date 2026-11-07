import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Shield, Lock, ArrowRight, CheckCircle2, AlertTriangle,
  Radio, PhoneCall, Cpu, Globe2, Sparkles, ShieldAlert,
  Terminal, Check
} from 'lucide-react';
import { Button } from '../components/common/Button';
import { StatusIndicator } from '../components/common/StatusIndicator';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState<string>('analyst');
  const [password, setPassword] = useState<string>('kavach2026');

  const handleDemoSignIn = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  const threatPillars = [
    { title: 'Digital Arrest Scams', desc: 'Simulated Supreme Court/CBI arrest warrants via Skype & WhatsApp' },
    { title: 'Law Enforcement Impersonation', desc: 'Fabricated narcotics courier allegations & fake police badge intimidation' },
    { title: 'Bank KYC & OTP Harvesting', desc: 'Urgent SIM deactivation warnings designed to extract UPI PINs & credentials' },
    { title: 'Remote Access Sideloading', desc: 'AnyDesk & TeamViewer APK installation orders targeting elderly victims' },
    { title: 'Customs & FedEx Contraband', desc: 'Unclaimed Taiwan package seizures with alleged illegal passports & MDMA' },
    { title: 'Multilingual & Code-Mixed', desc: 'Native triage in Telugu (తెలుగు), Hindi (हिंदी) & Indian English' }
  ];

  return (
    <div className="min-h-screen bg-navy-950 text-slate-100 flex flex-col justify-between selection:bg-cyan-500 selection:text-navy-950 relative overflow-hidden">
      {/* Background glow effects */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-teal-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* Top Header Bar */}
      <header className="border-b border-slate-800/80 px-6 sm:px-10 py-4 flex items-center justify-between bg-navy-950/80 backdrop-blur-xl relative z-10">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-teal-400 flex items-center justify-center shadow-glow-cyan">
            <Shield className="w-5 h-5 text-navy-950 stroke-[2.5]" />
          </div>
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-xl tracking-wider text-white">KAVACH</span>
            <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono font-bold border border-cyan-500/30">AI</span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <span className="text-xs font-mono text-slate-400 hidden md:inline">
            The Great Indian AI Challenge 2026
          </span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('/dashboard')}
            className="text-xs font-mono"
          >
            <span>Launch SOC Console</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
          </Button>
        </div>
      </header>

      {/* Main Hero & Console Login Section */}
      <main className="flex-1 flex items-center justify-center px-6 py-12 relative z-10">
        <div className="max-w-6xl w-full grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Column: Scope & Threat Vectors (7 cols) */}
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800/60 text-cyan-300 text-xs font-mono">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Next-Gen Voice Cyber Threat Neutralization Platform</span>
            </div>

            <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-[1.15]">
              Defending India from <br />
              <span className="bg-gradient-to-r from-cyan-400 via-teal-300 to-emerald-400 bg-clip-text text-transparent">
                Voice Scam Networks
              </span>
            </h1>

            <p className="text-sm text-slate-300 leading-relaxed max-w-xl">
              Enterprise SOC incident response, automated forensic transcription, and real-time social-engineering defense
              purpose-built for <b>Telugu, Hindi, and English</b> code-mixed telephony conversations.
            </p>

            {/* Genuine Gnani AI Stack */}
            <div className="p-4 rounded-xl bg-navy-900 border border-slate-800/80 space-y-2">
              <div className="text-xs font-mono text-cyan-400 font-semibold uppercase tracking-wider">
                Integrated with Genuine Gnani AI Engines
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-300 font-sans">
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
                  <span><b>Prisma v3:</b> Multilingual STT & Native LID</span>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
                  <span><b>Timbre v2.5:</b> Instant Acoustic Voice Advisories</span>
                </div>
              </div>
            </div>

            {/* 6 Key Threat Pillar Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              {threatPillars.map((p, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-navy-900/60 border border-slate-800/70 text-xs space-y-1">
                  <div className="font-bold text-white flex items-center space-x-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                    <span>{p.title}</span>
                  </div>
                  <p className="text-[11px] text-slate-400 leading-normal">{p.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column: Console Sign-in Card (5 cols) */}
          <div className="lg:col-span-5 bg-navy-900 p-8 rounded-2xl border border-slate-800/80 shadow-2xl space-y-6 relative">
            <div className="absolute top-0 right-0 -mr-8 -mt-8 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl pointer-events-none" />

            <div>
              <div className="flex items-center space-x-2 text-cyan-400 text-xs font-mono font-semibold uppercase tracking-wider">
                <Terminal className="w-4 h-4" />
                <span>SOC Analyst Workspace Access</span>
              </div>
              <h2 className="text-xl font-bold text-white mt-1.5">Sign in to KAVACH Console</h2>
              <p className="text-xs text-slate-400 mt-1">Pre-configured local session for evaluation.</p>
            </div>

            <form onSubmit={handleDemoSignIn} className="space-y-4 text-xs">
              <div>
                <label className="text-slate-300 font-medium block mb-1.5 font-mono text-[11px]">
                  OPERATOR IDENTIFIER
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-navy-950 border border-slate-700 rounded-lg px-3.5 py-2.5 text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
                />
              </div>

              <div>
                <label className="text-slate-300 font-medium block mb-1.5 font-mono text-[11px]">
                  PASSPHRASE
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-navy-950 border border-slate-700 rounded-lg px-3.5 py-2.5 text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
                />
              </div>

              <Button
                type="submit"
                variant="primary"
                size="lg"
                className="w-full shadow-glow-cyan text-xs font-bold"
              >
                <span>Launch Operational SOC Console</span>
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </form>

            <div className="pt-4 border-t border-slate-800/80 text-[11px] text-slate-500 space-y-2">
              <div className="flex items-center space-x-2 text-slate-400 font-mono">
                <span className="w-2 h-2 rounded-full bg-emerald-400" />
                <span>Localhost 127.0.0.1 Binding Active</span>
              </div>
              <p className="leading-relaxed">
                Zero external network requirements in local mode. 500-sample synthetic multilingual test suite pre-loaded.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 px-6 sm:px-10 py-4 bg-navy-950/80 text-center text-xs text-slate-500 font-mono relative z-10 flex flex-col sm:flex-row items-center justify-between gap-2">
        <span>KAVACH AI — Multilingual Voice Threat Intelligence Platform</span>
        <span className="text-cyan-400 font-semibold">National Cybercrime Helpline: 1930</span>
      </footer>
    </div>
  );
};
