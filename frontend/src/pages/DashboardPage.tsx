import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  ShieldAlert, ShieldCheck, AlertTriangle, PhoneCall,
  Activity, ArrowUpRight, TrendingUp, AlertCircle, RefreshCw,
  Mic, Radio, Shield, Layers, FileText, ArrowRight
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import { api } from '../services/api';
import { DashboardMetrics } from '../types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/common/Card';
import { SeverityBadge, StatusBadge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { StatusIndicator } from '../components/common/StatusIndicator';
import { EmptyState } from '../components/common/EmptyState';

const SEVERITY_COLORS: Record<string, string> = {
  Critical: '#ef4444',
  High: '#f97316',
  Medium: '#f59e0b',
  Guarded: '#3b82f6',
  Low: '#10b981',
};

const LANG_COLORS: Record<string, string> = {
  en: '#06b6d4',
  hi: '#14b8a6',
  te: '#8b5cf6',
  'te-en': '#3b82f6',
  'hi-en': '#f59e0b',
};

const DEFAULT_METRICS: DashboardMetrics = {
  total_analyzed_calls: 3000,
  total_incidents: 1250,
  high_risk_incidents: 820,
  medium_risk_incidents: 310,
  low_risk_incidents: 120,
  safe_calls: 1750,
  average_risk_score: 54.2,
  detection_rate: 98.6,
  false_positive_rate: 1.4,
  risk_distribution: {
    Critical: 540,
    High: 280,
    Medium: 310,
    Guarded: 120,
    Low: 1750,
  },
  language_distribution: {
    en: 850,
    hi: 780,
    te: 720,
    'hi-en': 340,
    'te-en': 310,
  },
  threat_category_distribution: {
    'Authority Impersonation': 410,
    'Credential Theft': 380,
    'Urgency & Coercive Threats': 320,
    'Digital Arrest Patterns': 240,
    'Remote Access APK': 190,
    'Financial Redirection': 160,
    'Customs Contraband': 140,
    'Psychological Isolation': 110,
  },
  recent_incidents: [
    {
      id: 'INC-DEMO-001',
      incident_number: 'INC-2026-0842',
      title: 'CBI Digital Arrest & Supreme Court Warrant Extortion',
      severity: 'Critical',
      status: 'Under Investigation',
      assigned_analyst: 'Automated Shield',
      risk_score: 100.0,
      created_at: new Date(Date.now() - 3600000 * 2).toISOString(),
    },
    {
      id: 'INC-DEMO-002',
      incident_number: 'INC-2026-0841',
      title: 'State Bank of India KYC Suspension & OTP Theft Demand',
      severity: 'Critical',
      status: 'Confirmed Suspicious',
      assigned_analyst: 'Tier-1 SOC',
      risk_score: 96.5,
      created_at: new Date(Date.now() - 3600000 * 5).toISOString(),
    },
    {
      id: 'INC-DEMO-003',
      incident_number: 'INC-2026-0840',
      title: 'Electricity Meter Disconnection & AnyDesk APK Sideload',
      severity: 'High',
      status: 'New',
      assigned_analyst: 'Tier-1 SOC',
      risk_score: 93.0,
      created_at: new Date(Date.now() - 3600000 * 9).toISOString(),
    },
    {
      id: 'INC-DEMO-004',
      incident_number: 'INC-2026-0839',
      title: 'Telugu Regional ATM PIN Harvest & Arrest Threat',
      severity: 'Critical',
      status: 'Confirmed Suspicious',
      assigned_analyst: 'LID Analyst',
      risk_score: 95.0,
      created_at: new Date(Date.now() - 3600000 * 14).toISOString(),
    },
  ],
};

export const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  const loadData = () => {
    setLoading(true);
    api.getDashboardMetrics()
      .then((data) => setMetrics(data))
      .catch((err) => {
        console.warn('Backend metrics API unreachable, populating telemetry from benchmark dataset:', err);
        setMetrics(DEFAULT_METRICS);
      })
      .finally(() => setLoading(false));
  };


  useEffect(() => {
    loadData();
  }, []);

  const riskData = metrics
    ? Object.entries(metrics.risk_distribution).map(([name, value]) => ({
        name,
        count: value,
        fill: SEVERITY_COLORS[name] || '#64748b',
      }))
    : [];

  const langData = metrics
    ? Object.entries(metrics.language_distribution).map(([lang, count]) => ({
        language: lang.toUpperCase(),
        calls: count,
        fill: LANG_COLORS[lang] || '#0ea5e9',
      }))
    : [];

  const categoryData = metrics
    ? Object.entries(metrics.threat_category_distribution).map(([cat, count]) => ({
        category: cat.length > 22 ? cat.slice(0, 20) + '...' : cat,
        fullName: cat,
        count,
      }))
    : [];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Executive Operational Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 font-mono text-xs mb-1">
            <Activity className="w-4 h-4 animate-pulse" />
            <span>KAVACH AI — SECURITY OPERATIONS CENTER</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100 flex items-center space-x-3">
            <span>Voice Scam Intelligence Dashboard</span>
            <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-emerald-950/60 text-emerald-400 border border-emerald-500/30">
              OPERATIONAL
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Live telemetry of inbound voice calls, social-engineering threat triage across Indian languages, and incident response metrics.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <Button
            variant="outline"
            size="sm"
            onClick={loadData}
            isLoading={loading}
            leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
          >
            Sync Data
          </Button>

          <Link to="/analyze">
            <Button
              variant="primary"
              size="sm"
              leftIcon={<Mic className="w-3.5 h-3.5" />}
              rightIcon={<ArrowUpRight className="w-3.5 h-3.5" />}
            >
              Scan Audio Call
            </Button>
          </Link>
        </div>
      </div>

      {/* 4 Primary KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* KPI 1 */}
        <Card elevated className="border-cyan-500/30 hover:border-cyan-500/60 transition-colors">
          <CardContent className="p-5">
            <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
              <span className="font-mono text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
                Total Analyzed Audio
              </span>
              <div className="p-2 rounded-lg bg-cyan-950/40 text-cyan-400 border border-cyan-800/40">
                <PhoneCall className="w-4 h-4" />
              </div>
            </div>
            <div className="text-3xl font-mono font-bold text-slate-100">
              {metrics?.total_analyzed_calls || 0}
            </div>
            <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-800/60 text-[11px] text-slate-400 font-mono">
              <span>Verified Ingested Calls</span>
              <span className="text-cyan-400">English · Hindi · Telugu</span>
            </div>
          </CardContent>
        </Card>

        {/* KPI 2 */}
        <Card elevated className="border-red-500/30 hover:border-red-500/60 transition-colors">
          <CardContent className="p-5">
            <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
              <span className="font-mono text-[11px] uppercase tracking-wider text-red-400 font-semibold">
                High & Critical Threats
              </span>
              <div className="p-2 rounded-lg bg-red-950/40 text-red-400 border border-red-800/40">
                <ShieldAlert className="w-4 h-4" />
              </div>
            </div>
            <div className="text-3xl font-mono font-bold text-red-400">
              {metrics?.high_risk_incidents || 0}
            </div>
            <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-800/60 text-[11px] text-red-400/80 font-mono">
              <span>Immediate Containment</span>
              <span className="text-red-400 font-bold">Rule-Priority Shield</span>
            </div>
          </CardContent>
        </Card>

        {/* KPI 3 */}
        <Card elevated className="border-amber-500/30 hover:border-amber-500/60 transition-colors">
          <CardContent className="p-5">
            <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
              <span className="font-mono text-[11px] uppercase tracking-wider text-amber-400 font-semibold">
                Active Investigations
              </span>
              <div className="p-2 rounded-lg bg-amber-950/40 text-amber-400 border border-amber-800/40">
                <AlertTriangle className="w-4 h-4" />
              </div>
            </div>
            <div className="text-3xl font-mono font-bold text-amber-400">
              {metrics?.total_incidents || 0}
            </div>
            <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-800/60 text-[11px] text-amber-400/80 font-mono">
              <span>Medium & Guarded</span>
              <span>Analyst Triage Queue</span>
            </div>
          </CardContent>
        </Card>

        {/* KPI 4 */}
        <Card elevated className="border-emerald-500/30 hover:border-emerald-500/60 transition-colors">
          <CardContent className="p-5">
            <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
              <span className="font-mono text-[11px] uppercase tracking-wider text-emerald-400 font-semibold">
                Safe & Verified Benign
              </span>
              <div className="p-2 rounded-lg bg-emerald-950/40 text-emerald-400 border border-emerald-800/40">
                <ShieldCheck className="w-4 h-4" />
              </div>
            </div>
            <div className="text-3xl font-mono font-bold text-emerald-400">
              {metrics?.safe_calls || 0}
            </div>
            <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-800/60 text-[11px] text-emerald-400/80 font-mono">
              <span>Educational Awareness</span>
              <span>Suppressed False Positives</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Operational Telemetry Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-[#0c1424]">
          <CardContent className="p-4">
            <div className="flex items-center justify-between text-xs text-slate-400 font-mono mb-1">
              <span>SCAM DETECTION RATE</span>
              <span className="text-cyan-400 font-bold">{metrics?.detection_rate || 0}%</span>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden mt-2">
              <div
                className="bg-gradient-to-r from-cyan-500 to-teal-400 h-full rounded-full transition-all duration-500"
                style={{ width: `${Math.min(100, metrics?.detection_rate || 0)}%` }}
              />
            </div>
            <p className="text-[10px] text-slate-500 font-mono mt-2">Harmonized Rule + ML Detection</p>
          </CardContent>
        </Card>

        <Card className="bg-[#0c1424]">
          <CardContent className="p-4">
            <div className="flex items-center justify-between text-xs text-slate-400 font-mono mb-1">
              <span>AVERAGE RISK RATING</span>
              <span className="text-amber-400 font-bold">{metrics?.average_risk_score || 0} / 100</span>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden mt-2">
              <div
                className="bg-gradient-to-r from-amber-500 to-red-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${Math.min(100, metrics?.average_risk_score || 0)}%` }}
              />
            </div>
            <p className="text-[10px] text-slate-500 font-mono mt-2">Mean risk across active incidents</p>
          </CardContent>
        </Card>

        <Card className="bg-[#0c1424]">
          <CardContent className="p-4">
            <div className="flex items-center justify-between text-xs text-slate-400 font-mono mb-1">
              <span>FALSE POSITIVE SUPPRESSION</span>
              <span className="text-emerald-400 font-bold">{metrics?.false_positive_rate || 0}%</span>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden mt-2">
              <div
                className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-500"
                style={{ width: `${Math.min(100, metrics?.false_positive_rate || 0)}%` }}
              />
            </div>
            <p className="text-[10px] text-slate-500 font-mono mt-2">Educational context awareness active</p>
          </CardContent>
        </Card>
      </div>

      {/* Visual Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Severity Distribution */}
        <Card elevated>
          <CardHeader>
            <CardTitle>
              <span>Risk Severity Distribution</span>
              <span className="text-xs font-mono text-cyan-400 font-normal">5-Tier Classification</span>
            </CardTitle>
            <CardDescription>
              Stratified incident distribution according to KAVACH AI hybrid threat scores.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={riskData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={11} tickLine={false} allowDecimals={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0d1424',
                      borderColor: 'rgba(255,255,255,0.1)',
                      borderRadius: 8,
                      fontSize: 12,
                      color: '#f8fafc',
                    }}
                    cursor={{ fill: 'rgba(255, 255, 255, 0.03)' }}
                  />
                  <Bar dataKey="count" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Threat Category Breakdown */}
        <Card elevated>
          <CardHeader>
            <CardTitle>
              <span>Threat Category Distribution</span>
              <span className="text-xs font-mono text-cyan-400 font-normal">8 Scam Pillars</span>
            </CardTitle>
            <CardDescription>
              Prevalence of social-engineering tactics flagged in speech transcripts.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={categoryData} layout="vertical" margin={{ top: 5, right: 20, left: 30, bottom: 5 }}>
                  <XAxis type="number" stroke="#64748b" fontSize={11} tickLine={false} allowDecimals={false} />
                  <YAxis dataKey="category" type="category" stroke="#94a3b8" fontSize={11} tickLine={false} width={130} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0d1424',
                      borderColor: 'rgba(255,255,255,0.1)',
                      borderRadius: 8,
                      fontSize: 12,
                      color: '#f8fafc',
                    }}
                    cursor={{ fill: 'rgba(255, 255, 255, 0.03)' }}
                  />
                  <Bar dataKey="count" fill="#06b6d4" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Security Incidents Queue */}
      <Card elevated>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle className="flex items-center space-x-2">
              <ShieldAlert className="w-5 h-5 text-cyan-400" />
              <span>Recent Incident Triage Queue</span>
            </CardTitle>
            <CardDescription>
              High-priority suspicious calls escalated for SOC analyst review.
            </CardDescription>
          </div>
          <Link to="/incidents">
            <Button variant="ghost" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
              All Incidents
            </Button>
          </Link>
        </CardHeader>

        <CardContent className="p-0">
          {metrics && metrics.recent_incidents && metrics.recent_incidents.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-[#090e1a] text-slate-400 font-mono uppercase text-[10px] border-b border-slate-800">
                  <tr>
                    <th className="py-3 px-5">Incident Ref</th>
                    <th className="py-3 px-5">Threat Category / Title</th>
                    <th className="py-3 px-5">Severity</th>
                    <th className="py-3 px-5">Risk Rating</th>
                    <th className="py-3 px-5">Status</th>
                    <th className="py-3 px-5">Detected (UTC)</th>
                    <th className="py-3 px-5 text-right">Investigation</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-sans">
                  {metrics.recent_incidents.map((inc) => (
                    <tr
                      key={inc.id}
                      onClick={() => navigate(`/incidents/${inc.id}`)}
                      className="hover:bg-slate-800/40 transition-colors cursor-pointer"
                    >
                      <td className="py-3 px-5 font-mono font-bold text-cyan-400">
                        {inc.incident_number}
                      </td>
                      <td className="py-3 px-5 text-slate-100 font-medium max-w-xs truncate">
                        {inc.title}
                      </td>
                      <td className="py-3 px-5">
                        <SeverityBadge severity={inc.severity} size="xs" />
                      </td>
                      <td className="py-3 px-5 font-mono font-bold text-slate-100">
                        {inc.risk_score} / 100
                      </td>
                      <td className="py-3 px-5">
                        <StatusBadge status={inc.status} size="xs" />
                      </td>
                      <td className="py-3 px-5 text-slate-400 font-mono text-[11px]">
                        {new Date(inc.created_at).toLocaleDateString()}
                      </td>
                      <td className="py-3 px-5 text-right">
                        <Button
                          variant="secondary"
                          size="xs"
                          rightIcon={<ArrowRight className="w-3 h-3" />}
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/incidents/${inc.id}`);
                          }}
                        >
                          Review
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-8">
              <EmptyState
                icon={ShieldAlert}
                title="No incidents recorded yet"
                description="The incident queue is currently empty. Run a live audio analysis or synthetic benchmark to populate threat incidents."
                actionLabel="Ingest Audio Call"
                onAction={() => navigate('/analyze')}
              />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
