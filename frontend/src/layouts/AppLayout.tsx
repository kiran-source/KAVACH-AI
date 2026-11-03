import React, { useState, useEffect } from 'react';
import { NavLink, Outlet, useLocation } from 'react-router-dom';
import {
  Shield, LayoutDashboard, Mic, Radio, ShieldAlert,
  FileText, Activity, Settings, AlertTriangle, CheckCircle,
  ExternalLink, PhoneCall
} from 'lucide-react';
import { api } from '../services/api';
import { SystemProviders } from '../types';

export const AppLayout: React.FC = () => {
  const [providers, setProviders] = useState<SystemProviders | null>(null);
  const location = useLocation();

  useEffect(() => {
    api.getProviders().then(setProviders).catch(console.error);
  }, []);

  const navItems = [
    { to: '/dashboard', label: 'SOC Dashboard', icon: LayoutDashboard },
    { to: '/analyze', label: 'Audio Ingestion & Scan', icon: Mic },
    { to: '/live', label: 'Live Chunk Scanner', icon: Radio },
    { to: '/incidents', label: 'Security Incidents', icon: ShieldAlert },
    { to: '/reports', label: 'Incident Reports', icon: FileText },
    { to: '/evaluation', label: 'Synthetic Benchmark', icon: Activity },
    { to: '/settings', label: 'System Settings', icon: Settings },
  ];

  return (
    <div className="flex h-screen bg-[#070b12] text-slate-100 overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-[#0c1220] border-r border-slate-800 flex flex-col justify-between shrink-0">
        <div>
          {/* Brand */}
          <div className="p-5 border-b border-slate-800/80 flex items-center space-x-3 bg-[#0a0f1c]">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-tr from-cyan-600 to-teal-400 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Shield className="w-6 h-6 text-slate-950 stroke-[2.5]" />
            </div>
            <div>
              <div className="flex items-center space-x-1.5">
                <span className="font-extrabold text-base tracking-wider text-white">KAVACH</span>
                <span className="text-xs px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono font-semibold border border-cyan-500/30">AI</span>
              </div>
              <p className="text-[10px] text-slate-400 font-mono">VOICE SOC DEFENSE</p>
            </div>
          </div>

          {/* AI Providers Status */}
          <div className="px-4 py-3 bg-[#080d17] border-b border-slate-800/60 text-xs">
            <div className="text-[10px] uppercase font-mono tracking-wider text-slate-500 mb-2">INTEGRATED AI ENGINES</div>
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-slate-300 font-mono text-[11px]">Gnani Prisma v2.5</span>
                <span className="flex items-center text-[10px] text-teal-400 bg-teal-500/10 px-1.5 py-0.5 rounded border border-teal-500/20">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mr-1 animate-pulse"></span>
                  Active
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-300 font-mono text-[11px]">Gnani Timbre v2.5</span>
                <span className="flex items-center text-[10px] text-teal-400 bg-teal-500/10 px-1.5 py-0.5 rounded border border-teal-500/20">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-400 mr-1"></span>
                  TTS Ready
                </span>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="p-3 space-y-1 mt-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center space-x-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                      isActive
                        ? 'bg-gradient-to-r from-cyan-950/60 to-slate-900 text-cyan-400 border border-cyan-800/40 shadow-sm'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Helpline Notice */}
        <div className="p-3.5 m-3 rounded-lg bg-red-950/20 border border-red-900/40 text-[11px]">
          <div className="flex items-center space-x-1.5 text-red-400 font-semibold mb-1">
            <PhoneCall className="w-3.5 h-3.5" />
            <span>National Cyber Helpline</span>
          </div>
          <p className="text-slate-300 font-mono font-bold text-sm">1930</p>
          <a
            href="https://cybercrime.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[10px] text-cyan-400 hover:underline flex items-center space-x-0.5 mt-1"
          >
            <span>cybercrime.gov.in</span>
            <ExternalLink className="w-2.5 h-2.5" />
          </a>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Operational Bar */}
        <header className="h-14 bg-[#0c1220]/90 border-b border-slate-800 px-6 flex items-center justify-between shrink-0 backdrop-blur">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              <span>SOC MONITORING ACTIVE</span>
            </div>
            <span className="text-slate-700">|</span>
            <span className="text-xs text-slate-400 font-mono">
              LANGUAGES: <b className="text-slate-200">TE (తెలుగు)</b> · <b className="text-slate-200">HI (हिंदी)</b> · <b className="text-slate-200">EN</b>
            </span>
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/30">
              DEMO & EVALUATION MODE
            </span>
            <div className="flex items-center space-x-2 text-xs text-slate-300">
              <span className="w-7 h-7 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-cyan-400 text-[11px]">
                SOC
              </span>
              <span>Analyst 1</span>
            </div>
          </div>
        </header>

        {/* Scrollable Page Body */}
        <main className="flex-1 overflow-y-auto p-6 bg-[#070b12]">
          <Outlet />
        </main>

        {/* Footer Disclaimer */}
        <footer className="h-8 bg-[#090d16] border-t border-slate-800/80 px-6 flex items-center justify-between text-[11px] text-slate-500 font-mono">
          <span>KAVACH AI — Multilingual Voice Scam SOC Response Engine (Great Indian AI Challenge)</span>
          <span className="text-amber-500/80">AI-assisted decision-support system, not a guaranteed fraud detector.</span>
        </footer>
      </div>
    </div>
  );
};
