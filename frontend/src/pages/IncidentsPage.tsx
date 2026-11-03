import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ShieldAlert, Filter, Search, ArrowUpRight,
  RefreshCw, CheckCircle, Clock, AlertTriangle
} from 'lucide-react';
import { api } from '../services/api';
import { IncidentSummary } from '../types';

const SEVERITY_BADGES: Record<string, string> = {
  Critical: 'bg-red-500/20 text-red-400 border-red-500/40',
  High: 'bg-orange-500/20 text-orange-400 border-orange-500/40',
  Medium: 'bg-amber-500/20 text-amber-400 border-amber-500/40',
  Guarded: 'bg-blue-500/20 text-blue-400 border-blue-500/40',
  Low: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40',
};

const STATUS_BADGES: Record<string, string> = {
  New: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
  'Under Review': 'bg-amber-500/10 text-amber-400 border-amber-500/30',
  'Confirmed Suspicious': 'bg-red-500/10 text-red-400 border-red-500/30',
  'False Positive': 'bg-slate-700/40 text-slate-400 border-slate-600',
  Resolved: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
};

export const IncidentsPage: React.FC = () => {
  const navigate = useNavigate();
  const [incidents, setIncidents] = useState<IncidentSummary[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Filters
  const [statusFilter, setStatusFilter] = useState<string>('All');
  const [severityFilter, setSeverityFilter] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const fetchIncidents = () => {
    setLoading(true);
    api.listIncidents(statusFilter, severityFilter)
      .then(setIncidents)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchIncidents();
  }, [statusFilter, severityFilter]);

  const filtered = incidents.filter((inc) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      inc.incident_number.toLowerCase().includes(q) ||
      inc.title.toLowerCase().includes(q) ||
      (inc.assigned_analyst && inc.assigned_analyst.toLowerCase().includes(q))
    );
  });

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5 text-red-400" />
            <span>Security Incident Triage & Management</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Investigate, review and manage voice scam detections with full evidentiary audit trails.
          </p>
        </div>

        <button
          onClick={fetchIncidents}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-lg border border-slate-700 flex items-center space-x-1.5 self-start sm:self-auto"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Queue</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-2 flex-1 min-w-[240px]">
          <Search className="w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search by incident #, tactic, analyst..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="bg-slate-900 border border-slate-700/80 rounded-lg px-3 py-1.5 text-xs text-slate-200 w-full focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1.5 text-xs text-slate-400">
            <Filter className="w-3.5 h-3.5 text-slate-500" />
            <span>Status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-slate-200"
            >
              <option value="All">All Statuses</option>
              <option value="New">New</option>
              <option value="Under Review">Under Review</option>
              <option value="Confirmed Suspicious">Confirmed Suspicious</option>
              <option value="False Positive">False Positive</option>
              <option value="Resolved">Resolved</option>
            </select>
          </div>

          <div className="flex items-center space-x-1.5 text-xs text-slate-400">
            <span>Severity:</span>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-slate-200"
            >
              <option value="All">All Severities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
        </div>
      </div>

      {/* Incidents Table */}
      <div className="bg-[#0c1220] rounded-xl border border-slate-800 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-xs text-cyan-400 font-mono flex items-center justify-center space-x-2">
            <RefreshCw className="w-4 h-4 animate-spin" />
            <span>Loading security incident queue...</span>
          </div>
        ) : filtered.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-[#090d16] text-slate-400 font-mono uppercase text-[10px]">
                <tr>
                  <th className="py-3 px-4">Incident ID</th>
                  <th className="py-3 px-4">Title / Primary Threat</th>
                  <th className="py-3 px-4">Risk Score</th>
                  <th className="py-3 px-4">Severity</th>
                  <th className="py-3 px-4">Investigation Status</th>
                  <th className="py-3 px-4">Assigned SOC Analyst</th>
                  <th className="py-3 px-4">Created Time</th>
                  <th className="py-3 px-4 text-right">Inspect</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {filtered.map((inc) => (
                  <tr
                    key={inc.id}
                    onClick={() => navigate(`/incidents/${inc.id}`)}
                    className="hover:bg-slate-800/40 cursor-pointer transition"
                  >
                    <td className="py-3 px-4 font-mono font-bold text-cyan-400">{inc.incident_number}</td>
                    <td className="py-3 px-4 text-white font-medium">{inc.title}</td>
                    <td className="py-3 px-4 font-mono font-bold text-white">{inc.risk_score} / 100</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${SEVERITY_BADGES[inc.severity] || 'bg-slate-800 text-slate-400'}`}>
                        {inc.severity}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${STATUS_BADGES[inc.status] || 'bg-slate-800 text-slate-300'}`}>
                        {inc.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-300">{inc.assigned_analyst || 'Unassigned'}</td>
                    <td className="py-3 px-4 text-slate-400 text-[11px] font-mono">
                      {new Date(inc.created_at).toLocaleString()}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <ArrowUpRight className="w-4 h-4 text-slate-400 hover:text-cyan-400 inline" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center text-slate-500 text-xs">
            <p>No incidents match the active filter criteria.</p>
          </div>
        )}
      </div>
    </div>
  );
};
