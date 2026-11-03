import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Download, Search, RefreshCw, ExternalLink } from 'lucide-react';
import { api } from '../services/api';
import { ReportItem } from '../types';

export const ReportsPage: React.FC = () => {
  const navigate = useNavigate();
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>('');

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
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      r.incident_number.toLowerCase().includes(q) ||
      r.title.toLowerCase().includes(q) ||
      r.severity.toLowerCase().includes(q)
    );
  });

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center space-x-2">
            <FileText className="w-5 h-5 text-cyan-400" />
            <span>Generated SOC Incident Reports (PDF Archive)</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Downloadable official security incident dossiers formatted for legal and cybersecurity forensic handoff.
          </p>
        </div>

        <button
          onClick={fetchReports}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-lg border border-slate-700 flex items-center space-x-1.5 self-start sm:self-auto"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Reports</span>
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800 flex items-center space-x-2">
        <Search className="w-4 h-4 text-slate-500" />
        <input
          type="text"
          placeholder="Filter reports by incident #, title, or severity..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="bg-transparent text-xs text-slate-200 w-full focus:outline-none"
        />
      </div>

      {/* Reports List */}
      <div className="bg-[#0c1220] rounded-xl border border-slate-800 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-xs text-cyan-400 font-mono flex items-center justify-center space-x-2">
            <RefreshCw className="w-4 h-4 animate-spin" />
            <span>Retrieving SOC reports repository...</span>
          </div>
        ) : filtered.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-[#090d16] text-slate-400 font-mono uppercase text-[10px]">
                <tr>
                  <th className="py-3 px-4">Report Reference</th>
                  <th className="py-3 px-4">Incident Number</th>
                  <th className="py-3 px-4">Title / Threat</th>
                  <th className="py-3 px-4">Severity</th>
                  <th className="py-3 px-4">Generated Time</th>
                  <th className="py-3 px-4 text-right">Download PDF</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {filtered.map((rep) => (
                  <tr key={rep.report_id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3 px-4 font-mono font-medium text-slate-400 text-[11px]">
                      {rep.report_id.slice(0, 16)}...
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-cyan-400">
                      <button
                        onClick={() => navigate(`/incidents/${rep.incident_id}`)}
                        className="hover:underline flex items-center space-x-1"
                      >
                        <span>{rep.incident_number}</span>
                        <ExternalLink className="w-3 h-3 text-slate-500" />
                      </button>
                    </td>
                    <td className="py-3 px-4 text-white font-medium">{rep.title}</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-amber-400 border border-slate-700">
                        {rep.severity}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400 text-[11px] font-mono">
                      {new Date(rep.generated_at).toLocaleString()}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <a
                        href={rep.download_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center space-x-1 px-3 py-1 bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-400 border border-cyan-500/40 rounded text-xs font-semibold transition"
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
          <div className="p-8 text-center text-slate-500 text-xs">
            <p>No PDF reports generated yet.</p>
            <p className="mt-1">Go to any incident dossier and click "Export Official SOC PDF Report".</p>
          </div>
        )}
      </div>
    </div>
  );
};

