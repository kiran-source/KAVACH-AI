import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FileText, Download, Search, RefreshCw, ExternalLink,
  ShieldAlert, CheckCircle, FileCheck, Calendar, ArrowRight,
  Filter, FileSpreadsheet, Lock
} from 'lucide-react';
import { api } from '../services/api';
import { ReportItem } from '../types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/common/Card';
import { SeverityBadge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { SearchInput } from '../components/common/SearchInput';
import { EmptyState } from '../components/common/EmptyState';

export const ReportsPage: React.FC = () => {
  const navigate = useNavigate();
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [severityFilter, setSeverityFilter] = useState<string>('all');

  const fetchReports = () => {
    setLoading(true);
    api.listReports()
      .then(setReports)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const filtered = reports.filter((r) => {
    const matchesSearch =
      !searchQuery ||
      r.incident_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.severity.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesSeverity =
      severityFilter === 'all' ||
      r.severity.toLowerCase() === severityFilter.toLowerCase();

    return matchesSearch && matchesSeverity;
  });

  const criticalCount = reports.filter(r => r.severity === 'Critical' || r.severity === 'High').length;

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
              <FileText className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                Forensic Incident Reports Archive
              </h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Officially formatted PDF dossiers, chain of custody logs, and threat intelligence exports for law enforcement.
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <Button
            variant="outline"
            size="sm"
            onClick={fetchReports}
            isLoading={loading}
            className="text-xs"
          >
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
            <span>Refresh Archive</span>
          </Button>
        </div>
      </div>

      {/* KPI Overview Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="bg-navy-900/60">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Total PDF Dossiers</div>
              <div className="text-2xl font-extrabold font-mono text-white mt-1">{reports.length}</div>
              <div className="text-[11px] text-slate-500 mt-0.5">Stored in local vault</div>
            </div>
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
              <FileCheck className="w-5 h-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-navy-900/60">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Critical / High Severity</div>
              <div className="text-2xl font-extrabold font-mono text-red-400 mt-1">{criticalCount}</div>
              <div className="text-[11px] text-slate-500 mt-0.5">Mandatory escalation cases</div>
            </div>
            <div className="w-10 h-10 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-navy-900/60">
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Export Compliance</div>
              <div className="text-sm font-bold text-emerald-400 mt-1 flex items-center space-x-1">
                <CheckCircle className="w-4 h-4 mr-1 text-emerald-400" />
                <span>CERT-In & 1930 Portal</span>
              </div>
              <div className="text-[11px] text-slate-500 mt-0.5">Section 65B IT Act ready</div>
            </div>
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Lock className="w-5 h-5" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filter and Search Bar */}
      <Card className="p-3">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="w-full sm:w-96">
            <SearchInput
              value={searchQuery}
              onChangeValue={setSearchQuery}
              placeholder="Filter by report ID, incident #, or threat type..."
            />
          </div>

          <div className="flex items-center space-x-1.5 self-end sm:self-auto overflow-x-auto w-full sm:w-auto">
            {['all', 'critical', 'high', 'medium', 'low'].map((sev) => (
              <button
                key={sev}
                onClick={() => setSeverityFilter(sev)}
                className={`px-2.5 py-1 rounded-lg text-xs font-mono font-medium capitalize transition ${
                  severityFilter === sev
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                    : 'text-slate-400 hover:text-white bg-slate-900/40 border border-transparent'
                }`}
              >
                {sev}
              </button>
            ))}
          </div>
        </div>
      </Card>

      {/* Reports Data Table */}
      <Card className="overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-xs text-cyan-400 font-mono flex flex-col items-center justify-center space-y-3">
            <RefreshCw className="w-6 h-6 animate-spin text-cyan-400" />
            <span>Decrypting SOC reports repository...</span>
          </div>
        ) : filtered.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-navy-950 text-slate-400 font-mono uppercase text-[10px] border-b border-slate-800">
                <tr>
                  <th className="py-3.5 px-4 font-semibold">Report Reference</th>
                  <th className="py-3.5 px-4 font-semibold">Incident Identifier</th>
                  <th className="py-3.5 px-4 font-semibold">Incident Title / Scam Vector</th>
                  <th className="py-3.5 px-4 font-semibold">Severity</th>
                  <th className="py-3.5 px-4 font-semibold">Generated Timestamp</th>
                  <th className="py-3.5 px-4 text-right font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {filtered.map((rep) => (
                  <tr key={rep.report_id} className="hover:bg-slate-800/30 transition group">
                    <td className="py-3.5 px-4 font-mono font-medium text-slate-400 text-[11px]">
                      <span className="bg-slate-900 px-2 py-1 rounded border border-slate-800">
                        {rep.report_id.slice(0, 14)}...
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-mono font-bold text-cyan-400">
                      <button
                        onClick={() => navigate(`/incidents/${rep.incident_id}`)}
                        className="hover:text-cyan-300 hover:underline flex items-center space-x-1.5 focus:outline-none"
                      >
                        <span>{rep.incident_number}</span>
                        <ExternalLink className="w-3 h-3 text-slate-500 group-hover:text-cyan-400" />
                      </button>
                    </td>
                    <td className="py-3.5 px-4 text-white font-medium max-w-xs truncate">
                      {rep.title}
                    </td>
                    <td className="py-3.5 px-4">
                      <SeverityBadge severity={rep.severity} size="sm" />
                    </td>
                    <td className="py-3.5 px-4 text-slate-400 text-[11px] font-mono">
                      {new Date(rep.generated_at).toLocaleString()}
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <a
                        href={rep.download_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center space-x-1.5 px-3 py-1.5 bg-cyan-600/10 hover:bg-cyan-600/20 text-cyan-400 border border-cyan-500/30 hover:border-cyan-500/60 rounded-lg text-xs font-semibold transition active:scale-[0.98]"
                      >
                        <Download className="w-3.5 h-3.5" />
                        <span>Download PDF</span>
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState
            icon={FileText}
            title="No Incident Reports Found"
            description={
              searchQuery || severityFilter !== 'all'
                ? "No reports match your current filter parameters. Try resetting filters."
                : "No official PDF dossiers have been generated yet. Open any incident in the Triage Queue and click 'Export Official SOC PDF'."
            }
            actionLabel="View Incident Triage Queue"
            onAction={() => navigate('/incidents')}
          />
        )}
      </Card>
    </div>
  );
};
