import React, { useState, useEffect } from 'react';
import {
  Settings, ShieldCheck, Database, HardDrive,
  Cpu, Lock, RefreshCw, CheckCircle, Save
} from 'lucide-react';
import { api } from '../services/api';
import { SystemSettings, SystemProviders } from '../types';

export const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<SystemSettings | null>(null);
  const [providers, setProviders] = useState<SystemProviders | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [savedSuccess, setSavedSuccess] = useState<boolean>(false);

  // Form states
  const [demoMode, setDemoMode] = useState<boolean>(true);
  const [retentionDays, setRetentionDays] = useState<number>(7);
  const [preferredLang, setPreferredLang] = useState<string>('en');
  const [warningVoiceLang, setWarningVoiceLang] = useState<string>('en');

  const loadSettings = () => {
    setLoading(true);
    Promise.all([api.getSettings(), api.getProviders()])
      .then(([s, p]) => {
        setSettings(s);
        setProviders(p);
        setDemoMode(s.demo_mode);
        setRetentionDays(s.audio_retention_days);
        setPreferredLang(s.preferred_language);
        setWarningVoiceLang(s.warning_voice_language);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadSettings();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.updateSettings({ demo_mode: demoMode, retention_days: retentionDays });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
      loadSettings();
    } catch (err) {
      console.error(err);
      alert("Failed to update settings.");
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-white flex items-center space-x-2">
          <Settings className="w-5 h-5 text-cyan-400" />
          <span>Platform Settings, AI Providers & Privacy</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Configure Gnani AI models, acoustic voice warning languages, data retention policies, and SOC operational preferences.
        </p>
      </div>

      {savedSuccess && (
        <div className="bg-emerald-950/40 border border-emerald-800/60 p-3 rounded-lg text-xs text-emerald-300 flex items-center space-x-2">
          <CheckCircle className="w-4 h-4 text-emerald-400" />
          <span>Configuration saved successfully.</span>
        </div>
      )}

      {/* Provider Connectivity Status */}
      <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 space-y-4">
        <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <span>Gnani AI Integration Hub & Status</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800">
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="font-semibold text-white">Gnani Prisma</span>
              <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950 px-1.5 py-0.5 rounded border border-cyan-800/40">
                v2.5 STT
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">Multilingual Speech-to-Text</p>
            <div className="mt-3 flex items-center space-x-1.5 text-xs text-teal-400">
              <span className="w-2 h-2 rounded-full bg-teal-400 animate-pulse" />
              <span>{providers?.gnani_prisma.status === 'connected' ? 'Connected (Live API)' : 'Simulated / Demo Mode'}</span>
            </div>
          </div>

          <div className="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800">
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="font-semibold text-white">Gnani Timbre</span>
              <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950 px-1.5 py-0.5 rounded border border-cyan-800/40">
                v2.5 TTS
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">Multilingual Voice Warning</p>
            <div className="mt-3 flex items-center space-x-1.5 text-xs text-teal-400">
              <span className="w-2 h-2 rounded-full bg-teal-400" />
              <span>{providers?.gnani_timbre.status === 'connected' ? 'Connected (Live API)' : 'Local TTS Active'}</span>
            </div>
          </div>

          <div className="bg-slate-900/60 p-3.5 rounded-lg border border-slate-800">
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="font-semibold text-white">Gnani Evon</span>
              <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-1.5 py-0.5 rounded border border-slate-700">
                v3.3 Reasoning
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">Contextual Ambiguity Arbiter</p>
            <div className="mt-3 flex items-center space-x-1.5 text-xs text-slate-500">
              <span className="w-2 h-2 rounded-full bg-slate-600" />
              <span>Optional Standby</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Configuration Form */}
      <form onSubmit={handleSave} className="bg-[#0c1220] p-6 rounded-xl border border-slate-800 space-y-6">
        <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
          <HardDrive className="w-4 h-4 text-cyan-400" />
          <span>Operational Preferences & Privacy Controls</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
          <div>
            <label className="text-slate-300 font-medium block mb-1.5">Audio Retention Window (Days):</label>
            <input
              type="number"
              min="1"
              max="90"
              value={retentionDays}
              onChange={(e) => setRetentionDays(Number(e.target.value))}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 w-full focus:outline-none focus:border-cyan-500 font-mono"
            />
            <p className="text-[11px] text-slate-500 mt-1">Raw audio files are purged automatically after expiration.</p>
          </div>

          <div>
            <label className="text-slate-300 font-medium block mb-1.5">Maximum Upload Size (MB):</label>
            <input
              type="number"
              value={settings?.max_upload_size_mb || 25}
              disabled
              className="bg-slate-900/50 border border-slate-800 rounded-lg px-3 py-2 text-slate-500 w-full font-mono cursor-not-allowed"
            />
            <p className="text-[11px] text-slate-500 mt-1">Fixed limit to prevent RAM exhaustion on target 16GB laptop.</p>
          </div>

          <div>
            <label className="text-slate-300 font-medium block mb-1.5">Default Warning Voice Language:</label>
            <select
              value={warningVoiceLang}
              onChange={(e) => setWarningVoiceLang(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 w-full focus:outline-none focus:border-cyan-500"
            >
              <option value="en">English (Official Warning)</option>
              <option value="te">Telugu (తెలుగు హెచ్చరిక)</option>
              <option value="hi">Hindi (हिंदी सुरक्षा चेतावनी)</option>
            </select>
          </div>

          <div className="flex items-center space-x-3 pt-4">
            <input
              type="checkbox"
              id="demoToggle"
              checked={demoMode}
              onChange={(e) => setDemoMode(e.target.checked)}
              className="rounded border-slate-700 text-cyan-500 focus:ring-0"
            />
            <label htmlFor="demoToggle" className="text-slate-300 cursor-pointer">
              <span className="font-semibold block">Enable Local Demo Mode</span>
              <span className="text-slate-500 text-[11px] block">
                Permits full offline testing with realistic synthetic speech recognition.
              </span>
            </label>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-800 flex justify-end">
          <button
            type="submit"
            className="px-5 py-2 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-500 hover:to-teal-400 text-slate-950 font-bold text-xs rounded-lg shadow-md transition flex items-center space-x-1.5"
          >
            <Save className="w-3.5 h-3.5" />
            <span>Save Settings</span>
          </button>
        </div>
      </form>

      {/* Technical Specifications */}
      <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 space-y-3 text-xs text-slate-400">
        <h3 className="text-xs font-semibold text-slate-300 font-mono uppercase">Target Hardware & Runtime Constraints</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-[11px]">
          <div className="p-2.5 rounded bg-slate-900 border border-slate-800">
            <span className="text-slate-500 block">MEMORY</span>
            <span className="text-white font-bold">16 GB RAM Limit</span>
          </div>
          <div className="p-2.5 rounded bg-slate-900 border border-slate-800">
            <span className="text-slate-500 block">PROCESSOR</span>
            <span className="text-white font-bold">Intel i5 / Ryzen 5</span>
          </div>
          <div className="p-2.5 rounded bg-slate-900 border border-slate-800">
            <span className="text-slate-500 block">ACCELERATION</span>
            <span className="text-white font-bold">CPU Only (No GPU)</span>
          </div>
          <div className="p-2.5 rounded bg-slate-900 border border-slate-800">
            <span className="text-slate-500 block">DATABASE</span>
            <span className="text-white font-bold">SQLite Local Storage</span>
          </div>
        </div>
      </div>
    </div>
  );
};

