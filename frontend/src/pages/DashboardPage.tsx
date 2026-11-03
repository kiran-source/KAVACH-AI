import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ShieldAlert, ShieldCheck, AlertTriangle, PhoneCall,
  Activity, ArrowUpRight, TrendingUp, AlertCircle, RefreshCw
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import { api } from '../services/api';
import { DashboardMetrics } from '../types';

const SEVERITY_COLORS: Record<string, string> = {
  Critical: '#ef4444',
  High: '#f97316',
  Medium: '#f59e0b',
  Guarded: '#3b82f6',
  Low: '#10b981'
};

const LANG_COLORS: Record<string, string> = {
  en: '#06b6d4',
  hi: '#8b5cf6',
  te: '#f43f5e'
};

export const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  const loadData = () => {
    setLoading(true);
    api.getDashboardMetrics()
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading && !metrics) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="flex items-center space-x-3 text-cyan-400 font-mono text-sm">
          <RefreshCw className="w-5 h-5 animate-spin" />
          <span>Synchronizing live SOC telemetry...</span>
        </div>
      </div>
    );
  }

  const riskData = metrics ? Object.entries(metrics.risk_distribution).map(([name, value]) => ({
    name,
    count: value,
    fill: SEVERITY_COLORS[name] || '#64748b'
  })) : [];

  const langData = metrics ? Object.entries(metrics.language_distribution).map(([lang, count]) => ({
    language: lang.toUpperCase(),
    calls: count,
    fill: LANG_COLORS[lang] || '#0ea5e9'
  })) : [];

  const categoryData = metrics ? Object.entries(metrics.threat_category_distribution).map(([cat, count]) => ({
    category: cat.length > 20 ? cat.slice(0, 18) + '...' : cat,
    fullName: cat,
    count
  })) : [];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-[#0c1424] to-[#0f172a] p-5 rounded-xl border border-slate-800">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <span>SOC Telemetry & Threat Surveillance</span>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800/60">
              LIVE DATABASE
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time voice social engineering analytics, multilingual tactic triage, and incident indicators.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={loadData}
            className="px-3 py-2 bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-lg border border-slate-700 flex items-center space-x-1.5 transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </button>
          <button
            onClick={() => navigate('/analyze')}
            className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-500 hover:to-teal-400 text-slate-950 font-semibold text-xs rounded-lg shadow-lg shadow-cyan-500/20 transition flex items-center space-x-1.5"
          >
            <span>Scan Audio File</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* KPI Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800/80">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Total Calls Analysed</span>
            <PhoneCall className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-mono font-bold text-white">{metrics?.total_analyzed_calls || 0}</div>
          <p className="text-[10px] text-slate-500 mt-1">Across English, Hindi & Telugu</p>
        </div>

        <div className="bg-[#0c1220] p-4 rounded-xl border border-red-950/40">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>High & Critical Threats</span>
            <ShieldAlert className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-2xl font-mono font-bold text-red-400">{metrics?.high_risk_incidents || 0}</div>
          <p className="text-[10px] text-red-400/70 mt-1">Requiring immediate containment</p>
        </div>

        <div className="bg-[#0c1220] p-4 rounded-xl border border-amber-950/40">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Medium / Guarded Risk</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-mono font-bold text-amber-400">{metrics?.medium_risk_incidents || 0}</div>
          <p className="text-[10px] text-amber-400/70 mt-1">Under analyst surveillance</p>
        </div>

        <div className="bg-[#0c1220] p-4 rounded-xl border border-emerald-950/40">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Safe / Benign Calls</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-mono font-bold text-emerald-400">{metrics?.safe_calls || 0}</div>
          <p className="text-[10px] text-emerald-400/70 mt-1">Low risk, verified normal</p>
        </div>
      </div>

      {/* Operational Ratios */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 mb-1">Scam Detection Rate</div>
          <div className="text-xl font-mono font-bold text-cyan-400">{metrics?.detection_rate || 0}%</div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
            <div
              className="bg-cyan-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, metrics?.detection_rate || 0)}%` }}
            />
          </div>
        </div>

        <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 mb-1">Average Risk Score</div>
          <div className="text-xl font-mono font-bold text-white">
            {metrics?.average_risk_score || 0} <span className="text-xs font-normal text-slate-400">/ 100</span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
            <div
              className="bg-amber-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, metrics?.average_risk_score || 0)}%` }}
            />
          </div>
        </div>

        <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800">
          <div className="text-xs text-slate-400 mb-1">Reported False Positive Rate</div>
          <div className="text-xl font-mono font-bold text-emerald-400">{metrics?.false_positive_rate || 0}%</div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
            <div
              className="bg-emerald-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, metrics?.false_positive_rate || 0)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Distribution Chart */}
        <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800">
          <h2 className="text-sm font-semibold text-white mb-4 flex items-center justify-between">
            <span>Risk Severity Distribution</span>
            <span className="text-[11px] font-mono text-slate-400">5 Tiers</span>
          </h2>
          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} allowDecimals={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: 8, fontSize: 12 }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Language Breakdown Chart */}
        <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800">
          <h2 className="text-sm font-semibold text-white mb-4 flex items-center justify-between">
            <span>Language Ingestion Volume</span>
            <span className="text-[11px] font-mono text-slate-400">Multilingual Ingestion</span>
          </h2>
          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={langData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="language" stroke="#64748b" fontSize={11} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} allowDecimals={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: 8, fontSize: 12 }}
                />
                <Bar dataKey="calls" radius={[4, 4, 0, 0]} fill="#06b6d4" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Incidents Table */}
      <div className="bg-[#0c1220] rounded-xl border border-slate-800 overflow-hidden">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
            <ShieldAlert className="w-4 h-4 text-cyan-400" />
            <span>Recent High-Priority Security Incidents</span>
          </h2>
          <button
            onClick={() => navigate('/incidents')}
            className="text-xs text-cyan-400 hover:text-cyan-300 font-mono flex items-center space-x-1"
          >
            <span>View All Incidents</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {metrics && metrics.recent_incidents.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-[#090d16] text-slate-400 font-mono uppercase text-[10px]">
                <tr>
                  <th className="py-3 px-4">Incident Ref</th>
                  <th className="py-3 px-4">Title / Threat</th>
                  <th className="py-3 px-4">Severity</th>
                  <th className="py-3 px-4">Risk Score</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Detected</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {metrics.recent_incidents.map((inc) => (
                  <tr key={inc.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3 px-4 font-mono font-medium text-cyan-400">{inc.incident_number}</td>
                    <td className="py-3 px-4 text-white font-medium">{inc.title}</td>
                    <td className="py-3 px-4">
                      <span
                        className="px-2 py-0.5 rounded text-[10px] font-semibold border"
                        style={{
                          backgroundColor: `${SEVERITY_COLORS[inc.severity] || '#64748b'}20`,
                          color: SEVERITY_COLORS[inc.severity] || '#64748b',
                          borderColor: `${SEVERITY_COLORS[inc.severity] || '#64748b'}40`
                        }}
                      >
                        {inc.severity}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-white">{inc.risk_score} / 100</td>
                    <td className="py-3 px-4">
                      <span className="text-[11px] font-medium text-slate-300 bg-slate-800 px-2 py-0.5 rounded">
                        {inc.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400 text-[11px]">
                      {new Date(inc.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => navigate(`/incidents/${inc.id}`)}
                        className="text-cyan-400 hover:text-cyan-300 font-medium underline"
                      >
                        Review
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center text-slate-500 text-xs">
            <p>No security incidents recorded yet in database.</p>
            <p className="mt-1">Upload a call recording or run synthetic scenarios to populate live data.</p>
            <button
              onClick={() => navigate('/analyze')}
              className="mt-3 px-3 py-1.5 bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-400 rounded border border-cyan-500/30 font-medium"
            >
              Analyze First Audio Call
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
