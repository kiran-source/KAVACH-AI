import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Shield, Lock, ArrowRight, CheckCircle2, AlertTriangle,
  Radio, PhoneCall, Cpu, Globe2, Sparkles
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState<string>('analyst');
  const [password, setPassword] = useState<string>('kavach2026');

  const handleDemoSignIn = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  const threatPillars = [
    { title: 'Digital Arrest Scams', desc: 'Continuous video interrogation & simulated custody threats' },
    { title: 'CBI & Police Impersonation', desc: 'Fake badges, manufactured narcotics warrants & legal panic' },
    { title: 'Bank KYC & OTP Theft', desc: 'Account blocking ultimatums to extract UPI PINs & CVV numbers' },
    { title: 'Remote Access APK Sideloading', desc: 'AnyDesk & TeamViewer installation commands targeting elderly' },
    { title: 'Courier & Customs Contraband', desc: 'Fake drug seizure allegations by alleged FedEx / Customs officials' },
    { title: 'Multilingual & Code-Mixed', desc: 'Native triage in Telugu (తెలుగు), Hindi (हिंदी) & English' }
  ];

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 flex flex-col justify-between selection:bg-cyan-500 selection:text-white">
      {/* Top Bar */}
      <header className="border-b border-slate-800/80 px-8 py-4 flex items-center justify-between bg-[#0a0f1d]/80 backdrop-blur">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-cyan-600 to-teal-400 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Shield className="w-5 h-5 text-slate-950 stroke-[2.5]" />
          </div>
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-lg tracking-wider text-white">KAVACH</span>
            <span className="text-xs px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono font-bold border border-cyan-500/30">AI</span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <span className="text-xs font-mono text-slate-400 hidden sm:inline">
            Organised for <b>Gnani AI Great Indian AI Challenge</b>
          </span>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-400 border border-cyan-800/40 text-xs font-semibold rounded-lg transition"
          >
            Direct Console Access
          </button>
        </div>
      </header>

      {/* Hero & Login Section */}
      <main className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="max-w-5xl w-full grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Column: Mission & Tactic Scope */}
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-800/50 text-cyan-300 text-xs font-mono">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Next-Gen Voice Cyber Threat Neutralization</span>
            </div>

            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight leading-tight">
              Multilingual Voice Scam Detection & Incident Response
            </h1>

            <p className="text-sm text-slate-300 leading-relaxed max-w-xl">
              Engineered to protect Indian citizens against digital arrest rackets, official impersonation,
              and banking credential theft across <b>Telugu, Hindi, and English</b> code-mixed voice conversations.
            </p>

            {/* AI Architecture highlight */}
            <div className="p-4 rounded-xl bg-[#0c1324] border border-slate-800/80 space-y-2">
              <div className="text-xs font-mono text-cyan-400 font-semibold uppercase">
                Powered by Genuine Gnani AI Technologies
              </div>
              <div className="grid grid-cols-2 gap-3 text-xs text-slate-300 font-sans">
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
                  <span><b>Prisma v2.5:</b> Multilingual Speech-to-Text & LID</span>
                </div>
                <div className="flex items-start space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
                  <span><b>Timbre v2.5:</b> Immediate Voice Safety Warnings</span>
                </div>
              </div>
            </div>

            {/* 6 Key Threat Pillars */}
            <div className="grid grid-cols-2 gap-3 pt-2">
              {threatPillars.map((p, idx) => (
                <div key={idx} className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/60 text-xs">
                  <div className="font-semibold text-white">{p.title}</div>
                  <p className="text-[11px] text-slate-400 mt-0.5">{p.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column: Local Demo Authentication Card */}
          <div className="lg:col-span-5 bg-[#0c1220] p-7 rounded-2xl border border-slate-800 shadow-2xl space-y-6">
            <div>
              <div className="flex items-center space-x-2 text-cyan-400 text-xs font-mono font-semibold uppercase tracking-wider">
                <Lock className="w-4 h-4" />
                <span>SOC Analyst Workspace Access</span>
              </div>
              <h2 className="text-lg font-bold text-white mt-1">Sign in to KAVACH Console</h2>
              <p className="text-xs text-slate-400 mt-1">Single-user local demo session configured for evaluation.</p>
            </div>

            <form onSubmit={handleDemoSignIn} className="space-y-4 text-xs">
              <div>
                <label className="text-slate-300 font-medium block mb-1">Operator Identifier:</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
                />
              </div>

              <div>
                <label className="text-slate-300 font-medium block mb-1">Passphrase:</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2.5 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-500 hover:to-teal-400 text-slate-950 font-bold text-xs rounded-lg shadow-lg shadow-cyan-500/20 transition flex items-center justify-center space-x-2"
              >
                <span>Launch Operational SOC Dashboard</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>

            <div className="pt-4 border-t border-slate-800/80 text-[11px] text-slate-500 space-y-2">
              <div className="flex items-center space-x-2 text-slate-400 font-mono">
                <span className="w-2 h-2 rounded-full bg-emerald-400" />
                <span>Localhost 127.0.0.1 Binding Active</span>
              </div>
              <p>Demo mode uses synthetic audio scenarios with 0 external network dependencies.</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 px-8 py-4 bg-[#0a0f1d] text-center text-xs text-slate-500 font-mono">
        KAVACH AI — AI-assisted decision-support system, not a guaranteed fraud detector. National Cyber Helpline: 1930.
      </footer>
    </div>
  );
};
