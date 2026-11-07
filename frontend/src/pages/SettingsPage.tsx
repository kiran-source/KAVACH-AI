import React, { useState, useEffect } from 'react';
import {
  Settings, ShieldCheck, Database, HardDrive,
  Cpu, Lock, RefreshCw, CheckCircle, Save, AlertTriangle,
  Globe, Volume2, Shield, Info, Check
} from 'lucide-react';
import { api } from '../services/api';
import { SystemSettings, SystemProviders } from '../types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { StatusIndicator } from '../components/common/StatusIndicator';

export const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<SystemSettings | null>(null);
  const [providers, setProviders] = useState<SystemProviders | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
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
    setSaving(true);
    try {
      await api.updateSettings({ demo_mode: demoMode, retention_days: retentionDays });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
      loadSettings();
    } catch (err) {
      console.error(err);
      alert("Failed to update settings.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
              <Settings className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                Platform Settings, AI Providers & Compliance
              </h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Configure Gnani AI models, acoustic voice warning languages, data retention policies, and SOC operational preferences.
              </p>
            </div>
          </div>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={loadSettings}
          isLoading={loading}
          className="text-xs self-start sm:self-auto"
        >
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
          <span>Refresh Telemetry</span>
        </Button>
      </div>

      {savedSuccess && (
        <div className="p-4 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-xs text-emerald-300 flex items-center space-x-2">
          <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>Configuration saved successfully. System policy updated.</span>
        </div>
      )}

      {/* Provider Connectivity Hub */}
      <Card>
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <CardTitle>Gnani AI Integration Hub & Telemetry</CardTitle>
          </div>
          <CardDescription>
            Real-time status of foundational speech recognition, acoustic synthesis, and reasoning engines.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Prisma v3 */}
            <div className="p-4 rounded-xl bg-navy-950 border border-slate-800/80 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white text-xs">Gnani Prisma</span>
                <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800/50">
                  v3 STT
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                Multilingual Speech Recognition & Native LID (Telugu, Hindi, English).
              </p>
              <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-xs">
                <span className="text-slate-500 font-mono text-[10px]">STATUS</span>
                <StatusIndicator
                  status={providers?.gnani_prisma.status === 'connected' || providers?.gnani_prisma.status === 'verified_in_session' ? 'online' : 'active'}
                  label={providers?.gnani_prisma.status === 'connected' || providers?.gnani_prisma.status === 'verified_in_session' ? 'Live API Active' : 'Local Synthetic Mode'}
                />
              </div>
            </div>

            {/* Timbre v2.5 */}
            <div className="p-4 rounded-xl bg-navy-950 border border-slate-800/80 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white text-xs">Gnani Timbre</span>
                <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800/50">
                  v2.5 TTS
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                Acoustic Voice Synthesis for immediate real-time victim intervention.
              </p>
              <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-xs">
                <span className="text-slate-500 font-mono text-[10px]">STATUS</span>
                <StatusIndicator
                  status={providers?.gnani_timbre.status === 'connected' || providers?.gnani_timbre.status === 'verified_in_session' ? 'online' : 'active'}
                  label={providers?.gnani_timbre.status === 'connected' || providers?.gnani_timbre.status === 'verified_in_session' ? 'Live API Active' : 'Local TTS Active'}
                />
              </div>
            </div>

            {/* Gnani Evon */}
            <div className="p-4 rounded-xl bg-navy-950 border border-slate-800/80 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white text-xs">Gnani Evon</span>
                <span className="text-[10px] font-mono text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800/40">
                  v3.3 Text Gen
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                API probe returned <code className="text-amber-300 font-mono text-[10px]">403 SCOPE_NOT_ALLOWED</code> under current credentials. Multilingual scenarios synthesized via local Domain-Curated Engine.
              </p>
              <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-xs">
                <span className="text-slate-500 font-mono text-[10px]">STATUS</span>
                <StatusIndicator
                  status="warning"
                  label="Not Provisioned"
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Configuration Form */}
      <form onSubmit={handleSave}>
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <HardDrive className="w-4 h-4 text-cyan-400" />
              <CardTitle>Operational Preferences & Data Retention Policy</CardTitle>
            </div>
            <CardDescription>
              Governance configurations enforcing zero unauthorized telemetry and GDPR / DPDP-aligned data minimization.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
              <div>
                <label className="text-slate-300 font-medium block mb-1.5">
                  Audio Evidence Retention Window (Days):
                </label>
                <input
                  type="number"
                  min="1"
                  max="90"
                  value={retentionDays}
                  onChange={(e) => setRetentionDays(Number(e.target.value))}
                  className="bg-navy-950 border border-slate-700 rounded-lg px-3.5 py-2 text-slate-200 w-full focus:outline-none focus:border-cyan-500 font-mono"
                />
                <p className="text-[11px] text-slate-500 mt-1">
                  Raw acoustic files are automatically purged from disk after expiration.
                </p>
              </div>

              <div>
                <label className="text-slate-300 font-medium block mb-1.5">
                  Maximum Audio Upload Payload (MB):
                </label>
                <input
                  type="number"
                  value={settings?.max_upload_size_mb || 25}
                  disabled
                  className="bg-navy-950/50 border border-slate-800 rounded-lg px-3.5 py-2 text-slate-500 w-full font-mono cursor-not-allowed"
                />
                <p className="text-[11px] text-slate-500 mt-1">
                  Hard memory ceiling to prevent OOM on 16GB CPU evaluation environments.
                </p>
              </div>

              <div>
                <label className="text-slate-300 font-medium block mb-1.5">
                  Default Warning Voice Language:
                </label>
                <select
                  value={warningVoiceLang}
                  onChange={(e) => setWarningVoiceLang(e.target.value)}
                  className="bg-navy-950 border border-slate-700 rounded-lg px-3.5 py-2 text-slate-200 w-full focus:outline-none focus:border-cyan-500"
                >
                  <option value="en">English (Official Warning)</option>
                  <option value="te">Telugu (తెలుగు హెచ్చరిక)</option>
                  <option value="hi">Hindi (हिंदी सुरक्षा चेतावनी)</option>
                </select>
                <p className="text-[11px] text-slate-500 mt-1">
                  Language chosen for synthetic acoustic intervention warnings.
                </p>
              </div>

              <div className="flex items-center space-x-3 pt-4">
                <input
                  type="checkbox"
                  id="demoToggle"
                  checked={demoMode}
                  onChange={(e) => setDemoMode(e.target.checked)}
                  className="w-4 h-4 rounded border-slate-700 text-cyan-500 focus:ring-0 bg-navy-950 cursor-pointer"
                />
                <label htmlFor="demoToggle" className="text-slate-300 cursor-pointer">
                  <span className="font-semibold block text-xs text-white">Enable Local Demo Mode</span>
                  <span className="text-slate-500 text-[11px] block">
                    Permits 100% offline testing with realistic speech recognition when external Gnani keys are not present.
                  </span>
                </label>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-800/80 flex justify-end">
              <Button
                type="submit"
                variant="primary"
                size="md"
                isLoading={saving}
                className="shadow-glow-cyan text-xs"
              >
                <Save className="w-3.5 h-3.5 mr-1.5" />
                <span>Save Configuration</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>

      {/* Target Hardware Architecture Constraints */}
      <Card>
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <CardTitle>Evaluator Runtime Environment Specification</CardTitle>
          </div>
          <CardDescription>
            Optimized exclusively for commodity laptop execution without GPU requirements.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
            <div className="p-3 rounded-xl bg-navy-950 border border-slate-800">
              <span className="text-[10px] text-slate-500 block uppercase">MEMORY LIMIT</span>
              <span className="text-white font-bold">16 GB RAM Limit</span>
            </div>
            <div className="p-3 rounded-xl bg-navy-950 border border-slate-800">
              <span className="text-[10px] text-slate-500 block uppercase">PROCESSOR</span>
              <span className="text-white font-bold">Intel i5 / Ryzen 5</span>
            </div>
            <div className="p-3 rounded-xl bg-navy-950 border border-slate-800">
              <span className="text-[10px] text-slate-500 block uppercase">ACCELERATION</span>
              <span className="text-emerald-400 font-bold">CPU Only (No GPU)</span>
            </div>
            <div className="p-3 rounded-xl bg-navy-950 border border-slate-800">
              <span className="text-[10px] text-slate-500 block uppercase">DATABASE</span>
              <span className="text-cyan-400 font-bold">SQLite Local Storage</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Statutory Disclosures */}
      <div className="p-4 rounded-xl bg-navy-900/60 border border-slate-800/80 text-xs text-slate-500 space-y-2">
        <div className="flex items-center space-x-2 text-slate-400 font-mono font-semibold uppercase text-[11px]">
          <Shield className="w-4 h-4 text-cyan-400" />
          <span>Statutory & Regulatory Disclosures</span>
        </div>
        <p className="text-[11px] leading-relaxed">
          KAVACH AI operates in compliance with the Digital Personal Data Protection Act (DPDPA 2023) and Section 65B of the Indian Evidence Act.
          All live microphone captures mandate explicit user consent prior to buffer creation.
          In case of imminent financial fraud, contact the National Cybercrime Reporting Portal at <b>1930</b> or visit <b>cybercrime.gov.in</b>.
        </p>
      </div>
    </div>
  );
};
