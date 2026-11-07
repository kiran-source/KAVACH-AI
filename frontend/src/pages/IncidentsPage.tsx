import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ShieldAlert, Filter, Search, ArrowUpRight,
  RefreshCw, CheckCircle, Clock, AlertTriangle, ShieldCheck,
  ChevronRight, ArrowRight
} from 'lucide-react';
import { api } from '../services/api';
import { IncidentSummary } from '../types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/common/Card';
import { SeverityBadge, StatusBadge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { SearchInput } from '../components/common/SearchInput';
import { EmptyState } from '../components/common/EmptyState';

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

  const criticalCount = incidents.filter((i) => i.severity === 'Critical').length;
  const highCount = incidents.filter((i) => i.severity === 'High').length;
  const underReviewCount = incidents.filter((i) => i.status === 'Under Review' || i.status === 'INVESTIGATING').length;
  const resolvedCount = incidents.filter((i) => i.status === 'Resolved' || i.status === 'RESOLVED').length;

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 font-mono text-xs mb-1">
            <ShieldAlert className="w-4 h-4" />
            <span>KAVACH AI INCIDENT MANAGEMENT CONSOLE</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100 flex items-center space-x-3">
            <span>Security Incidents Triage Queue</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Triage, investigate, and resolve voice scam security incidents with verified evidentiary audio transcripts and threat rule logs.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <Button
            variant="outline"
            size="sm"
            onClick={fetchIncidents}
            isLoading={loading}
            leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
          >
            Refresh Queue
          </Button>
        </div>
      </div>

      {/* Queue Stat Counters */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-[#0d1424] p-3.5 rounded-xl border border-slate-800">
          <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-1">Total Incidents</div>
          <div className="text-2xl font-mono font-bold text-slate-100">{incidents.length}</div>
        </div>
        <div className="bg-[#0d1424] p-3.5 rounded-xl border border-red-900/40">
          <div className="text-[10px] font-mono text-red-400 uppercase tracking-wider mb-1">Critical & High</div>
          <div className="text-2xl font-mono font-bold text-red-400">{criticalCount + highCount}</div>
        </div>
        <div className="bg-[#0d1424] p-3.5 rounded-xl border border-amber-900/40">
          <div className="text-[10px] font-mono text-amber-400 uppercase tracking-wider mb-1">Under Review</div>
          <div className="text-2xl font-mono font-bold text-amber-400">{underReviewCount}</div>
        </div>
        <div className="bg-[#0d1424] p-3.5 rounded-xl border border-emerald-900/40">
          <div className="text-[10px] font-mono text-emerald-400 uppercase tracking-wider mb-1">Resolved Cases</div>
          <div className="text-2xl font-mono font-bold text-emerald-400">{resolvedCount}</div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <Card className="bg-[#0d1424] p-4">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-4">
          <div className="w-full lg:w-96">
            <SearchInput
              value={searchQuery}
              onChangeValue={setSearchQuery}
              placeholder="Search by incident ref, threat keyword, analyst..."
            />
          </div>

          <div className="flex flex-wrap items-center gap-3 w-full lg:w-auto">
            {/* Status Selector */}
            <div className="flex items-center space-x-1.5 text-xs text-slate-400">
              <span className="font-mono text-[11px]">STATUS:</span>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="bg-[#070b14] border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-sans"
              >
                <option value="All">All Statuses</option>
                <option value="New">New</option>
                <option value="Under Review">Under Review</option>
                <option value="Confirmed Suspicious">Confirmed Suspicious</option>
                <option value="False Positive">False Positive</option>
                <option value="Resolved">Resolved</option>
              </select>
            </div>

            {/* Severity Selector */}
            <div className="flex items-center space-x-1.5 text-xs text-slate-400">
              <span className="font-mono text-[11px]">SEVERITY:</span>
              <select
                value={severityFilter}
                onChange={(e) => setSeverityFilter(e.target.value)}
                className="bg-[#070b14] border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-sans"
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
      </Card>

      {/* Incidents Table */}
      <Card elevated className="overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-xs text-cyan-400 font-mono flex items-center justify-center space-x-2">
            <RefreshCw className="w-4 h-4 animate-spin" />
            <span>Loading security incident queue...</span>
          </div>
        ) : filtered.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-[#090e1a] text-slate-400 font-mono uppercase text-[10px] border-b border-slate-800">
                <tr>
                  <th className="py-3.5 px-5">Incident ID</th>
                  <th className="py-3.5 px-5">Threat Category / Title</th>
                  <th className="py-3.5 px-5">Risk Score</th>
                  <th className="py-3.5 px-5">Severity</th>
                  <th className="py-3.5 px-5">Investigation Status</th>
                  <th className="py-3.5 px-5">Assigned Analyst</th>
                  <th className="py-3.5 px-5">Timestamp (UTC)</th>
                  <th className="py-3.5 px-5 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {filtered.map((inc) => (
                  <tr
                    key={inc.id}
                    onClick={() => navigate(`/incidents/${inc.id}`)}
                    className="hover:bg-slate-800/40 cursor-pointer transition-colors"
                  >
                    <td className="py-3.5 px-5 font-mono font-bold text-cyan-400">
                      {inc.incident_number}
                    </td>
                    <td className="py-3.5 px-5 text-slate-100 font-medium max-w-sm truncate">
                      {inc.title}
                    </td>
                    <td className="py-3.5 px-5 font-mono font-bold text-slate-100">
                      {inc.risk_score} / 100
                    </td>
                    <td className="py-3.5 px-5">
                      <SeverityBadge severity={inc.severity} size="xs" />
                    </td>
                    <td className="py-3.5 px-5">
                      <StatusBadge status={inc.status} size="xs" />
                    </td>
                    <td className="py-3.5 px-5 text-slate-300 font-mono text-[11px]">
                      {inc.assigned_analyst || 'SecOps Pool'}
                    </td>
                    <td className="py-3.5 px-5 text-slate-400 text-[11px] font-mono">
                      {new Date(inc.created_at).toLocaleString()}
                    </td>
                    <td className="py-3.5 px-5 text-right">
                      <Button
                        variant="secondary"
                        size="xs"
                        rightIcon={<ArrowRight className="w-3 h-3" />}
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/incidents/${inc.id}`);
                        }}
                      >
                        Inspect
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
              title="No incidents match filter"
              description="No security incidents match the selected severity, status, or search query. Reset filters to view all cases."
              actionLabel="Reset Filters"
              onAction={() => {
                setStatusFilter('All');
                setSeverityFilter('All');
                setSearchQuery('');
              }}
            />
          </div>
        )}
      </Card>
    </div>
  );
};
