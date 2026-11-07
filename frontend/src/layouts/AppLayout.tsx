import React, { useState, useEffect } from 'react';
import { NavLink, Outlet, useLocation, Link } from 'react-router-dom';
import {
  Shield, LayoutDashboard, Mic, Radio, ShieldAlert,
  FileText, Activity, Settings, Database,
  PhoneCall, ExternalLink, ChevronLeft, ChevronRight,
  Server, Cpu, Layers, Bell, CheckCircle2, AlertTriangle, UserCheck
} from 'lucide-react';
import { api } from '../services/api';
import { SystemProviders } from '../types';
import { StatusIndicator } from '../components/common/StatusIndicator';

interface NavGroup {
  groupName: string;
  items: {
    to: string;
    label: string;
    icon: React.ElementType;
    badge?: string;
  }[];
}

export const AppLayout: React.FC = () => {
  const [providers, setProviders] = useState<SystemProviders | null>(null);
  const [healthStatus, setHealthStatus] = useState<{ status: string; demo_mode: boolean } | null>(null);
  const [isCollapsed, setIsCollapsed] = useState<boolean>(false);
  const location = useLocation();

  useEffect(() => {
    api.getProviders().then(setProviders).catch(console.error);
    api.getHealth().then(setHealthStatus).catch(console.error);

    // Keyboard shortcut to toggle sidebar collapse '['
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === '[' && !['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) {
        setIsCollapsed((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const navGroups: NavGroup[] = [
    {
      groupName: 'OPERATIONS',
      items: [
        { to: '/dashboard', label: 'Overview', icon: LayoutDashboard },
        { to: '/analyze', label: 'Audio Analysis', icon: Mic, badge: 'Live STT' },
        { to: '/live', label: 'Live Chunk Scanner', icon: Radio },
      ],
    },
    {
      groupName: 'INTELLIGENCE & CASES',
      items: [
        { to: '/threats', label: 'Threat Intelligence', icon: Layers },
        { to: '/incidents', label: 'Security Incidents', icon: ShieldAlert },
        { to: '/evidence', label: 'Evidence Vault', icon: Database },
        { to: '/reports', label: 'Incident Reports', icon: FileText },
      ],
    },
    {
      groupName: 'GOVERNANCE & SYSTEM',
      items: [
        { to: '/evaluation', label: 'Synthetic Benchmark', icon: Activity },
        { to: '/settings', label: 'System Settings', icon: Settings },
      ],
    },
  ];

  // Dynamic breadcrumb calculation
  const getBreadcrumbTitle = (pathname: string) => {
    if (pathname.startsWith('/incidents/')) return 'Incident Investigation Dossier';
    switch (pathname) {
      case '/dashboard':
        return 'Executive SOC Overview';
      case '/analyze':
        return 'Forensic Audio Analysis Workstation';
      case '/live':
        return 'Near-Real-Time Microphone Stream Ingestion';
      case '/threats':
        return 'Voice Scam Tactic & Threat Repository';
      case '/incidents':
        return 'Security Incident Management Queue';
      case '/evidence':
        return 'Forensic Chain of Custody & Evidence Vault';
      case '/reports':
        return 'Formal Incident Dossiers & PDF Archives';
      case '/evaluation':
        return 'Synthetic Benchmark & Split Evaluation';
      case '/settings':
        return 'System Configuration & Security Boundaries';
      default:
        return 'Security Operations Console';
    }
  };

  return (
    <div className="flex h-screen bg-[#060911] text-slate-100 overflow-hidden font-sans">
      {/* Sidebar */}
      <aside
        className={`bg-[#0d1424] border-r border-slate-800/80 flex flex-col justify-between shrink-0 transition-all duration-200 ease-out z-20 ${
          isCollapsed ? 'w-20' : 'w-64'
        }`}
        aria-label="Main Navigation"
      >
        <div className="flex flex-col h-full overflow-hidden">
          {/* Brand Header */}
          <div className="p-4 border-b border-slate-800/80 flex items-center justify-between bg-[#090e1a]">
            <Link to="/dashboard" className="flex items-center space-x-3 overflow-hidden">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 via-cyan-500 to-teal-400 flex items-center justify-center shadow-md shadow-cyan-500/20 shrink-0">
                <Shield className="w-6 h-6 text-slate-950 stroke-[2.5]" />
              </div>
              {!isCollapsed && (
                <div className="truncate">
                  <div className="flex items-center space-x-1.5">
                    <span className="font-extrabold text-base tracking-wider text-white">KAVACH</span>
                    <span className="text-[10px] px-1.5 py-0.2 rounded bg-cyan-500/20 text-cyan-300 font-mono font-bold border border-cyan-500/30">
                      SOC
                    </span>
                  </div>
                  <p className="text-[10px] text-slate-400 font-mono tracking-tight truncate">VOICE DEFENSE PLATFORM</p>
                </div>
              )}
            </Link>

            <button
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="p-1 rounded-md text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition-colors"
              title={isCollapsed ? 'Expand sidebar ([)' : 'Collapse sidebar ([)'}
              aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
              {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>
          </div>

          {/* AI Providers Status Box */}
          {!isCollapsed && (
            <div className="px-4 py-2.5 bg-[#080d17] border-b border-slate-800/60 text-xs">
              <div className="text-[9px] uppercase font-mono tracking-wider text-slate-400 mb-1.5 flex items-center justify-between">
                <span>AI INFERENCE ENGINES</span>
                <span className="text-emerald-400 flex items-center text-[9px]">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1 animate-pulse" />
                  Connected
                </span>
              </div>
              <div className="space-y-1 text-[11px] font-mono">
                <div className="flex items-center justify-between">
                  <span className="text-slate-300 flex items-center gap-1">
                    <Cpu className="w-3 h-3 text-cyan-400" />
                    Gnani Prisma v3.0
                  </span>
                  <span className="text-[10px] text-cyan-400 bg-cyan-950/60 px-1.5 py-0.2 rounded border border-cyan-800/40">
                    STT
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-300 flex items-center gap-1">
                    <Server className="w-3 h-3 text-teal-400" />
                    Gnani Timbre v2.5
                  </span>
                  <span className="text-[10px] text-teal-400 bg-teal-950/60 px-1.5 py-0.2 rounded border border-teal-800/40">
                    TTS
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Nav Links */}
          <nav className="flex-1 overflow-y-auto px-3 py-3 space-y-4">
            {navGroups.map((group) => (
              <div key={group.groupName} className="space-y-1">
                {!isCollapsed && (
                  <h4 className="px-2 text-[10px] font-mono uppercase tracking-wider text-slate-400 font-semibold mb-1">
                    {group.groupName}
                  </h4>
                )}
                {group.items.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.to}
                      to={item.to}
                      title={isCollapsed ? item.label : undefined}
                      className={({ isActive }) =>
                        `flex items-center ${
                          isCollapsed ? 'justify-center py-2.5' : 'space-x-3 px-3 py-2'
                        } rounded-lg text-xs font-medium transition-all ${
                          isActive
                            ? 'bg-cyan-950/60 text-cyan-400 border border-cyan-800/50 shadow-sm shadow-cyan-950/40 font-semibold'
                            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                        }`
                      }
                    >
                      <Icon className="w-4 h-4 shrink-0" aria-hidden="true" />
                      {!isCollapsed && (
                        <div className="flex items-center justify-between w-full">
                          <span>{item.label}</span>
                          {item.badge && (
                            <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
                              {item.badge}
                            </span>
                          )}
                        </div>
                      )}
                    </NavLink>
                  );
                })}
              </div>
            ))}
          </nav>

          {/* Emergency Helpline Box */}
          {!isCollapsed ? (
            <div className="p-3 m-3 rounded-xl bg-red-950/20 border border-red-900/40 text-[11px]">
              <div className="flex items-center space-x-1.5 text-red-400 font-semibold mb-0.5">
                <PhoneCall className="w-3.5 h-3.5 shrink-0" />
                <span>National Cyber Helpline</span>
              </div>
              <p className="text-slate-200 font-mono font-bold text-sm">1930</p>
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
          ) : (
            <div className="p-2 m-2 flex justify-center" title="Helpline: 1930">
              <a
                href="tel:1930"
                className="w-10 h-10 rounded-lg bg-red-950/30 border border-red-800/40 flex items-center justify-center text-red-400 hover:bg-red-900/40 transition-colors"
                aria-label="National Cyber Helpline 1930"
              >
                <PhoneCall className="w-4 h-4" />
              </a>
            </div>
          )}
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Operational Bar */}
        <header className="h-14 bg-[#0d1424]/90 border-b border-slate-800/80 px-6 flex items-center justify-between shrink-0 backdrop-blur z-10">
          <div className="flex items-center space-x-3">
            <div>
              <span className="text-[10px] font-mono uppercase tracking-wider text-cyan-400 block">
                {getBreadcrumbTitle(location.pathname)}
              </span>
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="font-semibold text-slate-100">KAVACH SOC</span>
                <span className="text-slate-600">/</span>
                <span className="font-mono text-slate-400">{location.pathname.replace('/', '') || 'dashboard'}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Real-time Status Telemetry */}
            <div className="hidden sm:flex items-center space-x-2.5 px-2.5 py-1 rounded-lg bg-[#070b12] border border-slate-800">
              <StatusIndicator
                status={healthStatus?.status === 'healthy' ? 'online' : 'warning'}
                label={healthStatus?.demo_mode ? 'DEMO MODE' : 'HYBRID SOC ACTIVE'}
                pulse={true}
              />
              <span className="text-slate-700">|</span>
              <span className="text-[11px] font-mono text-slate-400">
                LID: <b className="text-cyan-400">TE</b> · <b className="text-teal-400">HI</b> · <b className="text-slate-200">EN</b>
              </span>
            </div>

            {/* Quick Actions */}
            <Link
              to="/analyze"
              className="hidden md:inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-slate-950 transition-all shadow-sm shadow-cyan-500/20 active:scale-[0.98]"
            >
              <Mic className="w-3.5 h-3.5" />
              <span>Ingest Audio</span>
            </Link>

            {/* User Profile */}
            <div className="flex items-center space-x-2 pl-2 border-l border-slate-800">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-cyan-950 to-slate-800 border border-cyan-800/40 flex items-center justify-center font-bold text-cyan-400 text-[11px]">
                SOC
              </div>
              <div className="hidden lg:block text-left">
                <div className="text-xs font-semibold text-slate-200 leading-tight">SecOps Analyst</div>
                <div className="text-[10px] text-emerald-400 font-mono flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  Active Duty
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Scrollable Page Body */}
        <main className="flex-1 overflow-y-auto p-6 bg-[#060911]" id="main-content">
          <Outlet />
        </main>

        {/* Footer Disclaimer */}
        <footer className="h-8 bg-[#090d16] border-t border-slate-800/80 px-6 flex items-center justify-between text-[11px] text-slate-500 font-mono shrink-0">
          <div className="flex items-center space-x-3">
            <span>KAVACH AI — Multilingual Voice Scam Intelligence Engine</span>
            <span className="text-slate-700">·</span>
            <span className="text-cyan-500/80">Great Indian AI Challenge</span>
          </div>
          <span className="hidden sm:inline text-amber-500/80">
            Automated AI decision support system · Dial 1930 for verified cybercrime emergencies
          </span>
        </footer>
      </div>
    </div>
  );
};
