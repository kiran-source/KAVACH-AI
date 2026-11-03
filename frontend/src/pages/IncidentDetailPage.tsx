import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ShieldAlert, ArrowLeft, Download, FileText, Clock,
  Volume2, UserCheck, AlertTriangle, CheckCircle, RefreshCw,
  ExternalLink, Send
} from 'lucide-react';
import { api } from '../services/api';
import { IncidentDetail } from '../types';

export const IncidentDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [incident, setIncident] = useState<IncidentDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [newNote, setNewNote] = useState<string>('');
  const [statusUpdating, setStatusUpdating] = useState<boolean>(false);
  const [generatingReport, setGeneratingReport] = useState<boolean>(false);

  const fetchDetail = () => {
    if (!id) return;
    setLoading(true);
    api.getIncident(id)
      .then(setIncident)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDetail();
  }, [id]);

  const handleStatusChange = async (newStatus: string) => {
    if (!id) return;
    setStatusUpdating(true);
    try {
      await api.updateIncident(id, { status: newStatus });
      fetchDetail();
    } catch (err) {
      console.error(err);
    } finally {
      setStatusUpdating(false);
    }
  };

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !newNote.trim()) return;

    try {
      await api.addIncidentNote(id, newNote);
      setNewNote('');
      fetchDetail();
    } catch (err) {
      console.error(err);
    }
  };

  const handleGenerateReport = async () => {
    if (!id) return;
    setGeneratingReport(true);
    try {
      const res = await api.createReport(id);
      window.open(`/api/v1/reports/${res.report_id}/download`, '_blank');
      fetchDetail();
    } catch (err) {
      console.error(err);
      alert("Failed to generate PDF report.");
    } finally {
      setGeneratingReport(false);
    }
  };

  if (loading || !incident) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="flex items-center space-x-2 text-cyan-400 font-mono text-sm">
          <RefreshCw className="w-4 h-4 animate-spin" />
          <span>Loading Incident Dossier...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Back button & Action Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <button
          onClick={() => navigate('/incidents')}
          className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white transition font-mono self-start"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Incident Queue</span>
        </button>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleGenerateReport}
            disabled={generatingReport}
            className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-500 hover:to-teal-400 text-slate-950 font-bold text-xs rounded-lg shadow-md transition flex items-center space-x-2"
          >
            {generatingReport ? (
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <FileText className="w-3.5 h-3.5" />
            )}
            <span>Export Official SOC PDF Report</span>
          </button>
        </div>
      </div>

      {/* Incident Overview Card */}
      <div className="bg-[#0c1220] p-6 rounded-xl border border-slate-800 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div>
            <div className="flex items-center space-x-2 font-mono text-xs text-cyan-400 font-bold">
              <span>{incident.incident_number}</span>
              <span className="text-slate-600">•</span>
              <span className="text-slate-400">{new Date(incident.created_at).toUTCString()}</span>
            </div>
            <h1 className="text-xl font-bold text-white mt-1">{incident.title}</h1>
          </div>

          <div className="flex items-center space-x-3">
            <div className="text-right">
              <div className="text-[10px] font-mono text-slate-400">RISK ASSESSMENT</div>
              <div className="text-xl font-mono font-bold text-white">{incident.risk_score} / 100</div>
            </div>
            <div
              className={`px-3 py-1.5 rounded-lg text-xs font-bold font-mono border ${
                incident.severity === 'Critical' || incident.severity === 'High'
                  ? 'bg-red-500/20 text-red-400 border-red-500/40'
                  : 'bg-amber-500/20 text-amber-400 border-amber-500/40'
              }`}
            >
              {incident.severity}
            </div>
          </div>
        </div>

        {/* Status Transition Row */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 text-xs">
          <div>
            <span className="text-slate-400 block mb-1">Investigation Status:</span>
            <select
              value={incident.status}
              onChange={(e) => handleStatusChange(e.target.value)}
              disabled={statusUpdating}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-cyan-400 font-semibold w-full focus:outline-none"
            >
              <option value="New">New</option>
              <option value="Under Review">Under Review</option>
              <option value="Confirmed Suspicious">Confirmed Suspicious</option>
              <option value="False Positive">False Positive</option>
              <option value="Resolved">Resolved</option>
            </select>
          </div>

          <div>
            <span className="text-slate-400 block mb-1">Assigned SOC Analyst:</span>
            <div className="p-1.5 rounded bg-slate-900 border border-slate-800 text-slate-200 font-medium">
              {incident.assigned_analyst || 'SOC Analyst 1'}
            </div>
          </div>

          <div>
            <span className="text-slate-400 block mb-1">Audio Source File:</span>
            <div className="p-1.5 rounded bg-slate-900 border border-slate-800 text-slate-300 font-mono text-[11px] truncate">
              {incident.audio_filename}
            </div>
          </div>
        </div>
      </div>

      {/* Audio Playback & Transcript */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Full Transcript */}
        <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
            <span>Prisma v2.5 Audio Transcript</span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-cyan-400">
              LANG: {incident.detected_language.toUpperCase()}
            </span>
          </div>
          <div className="bg-[#070b14] p-4 rounded-lg border border-slate-800 text-xs text-slate-200 leading-relaxed max-h-56 overflow-y-auto italic font-sans">
            "{incident.transcript_text}"
          </div>
          {incident.audio_id && (
            <div className="pt-2 flex items-center justify-between text-xs text-slate-400">
              <span>Original Audio Stream:</span>
              <audio src={`/api/v1/audio/${incident.audio_id}`} controls className="h-7 w-56" />
            </div>
          )}
        </div>

        {/* Incident Timeline Audit Log */}
        <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 space-y-3">
          <div className="text-xs font-semibold text-slate-300 flex items-center space-x-1.5">
            <Clock className="w-3.5 h-3.5 text-cyan-400" />
            <span>Chronological Incident Audit Timeline</span>
          </div>
          <div className="bg-[#070b14] p-4 rounded-lg border border-slate-800 text-xs space-y-3 max-h-56 overflow-y-auto font-sans">
            {incident.timeline && incident.timeline.length > 0 ? (
              incident.timeline.map((tm, idx) => (
                <div key={idx} className="border-l-2 border-cyan-500/60 pl-3 space-y-0.5">
                  <div className="flex items-center space-x-2">
                    <span className="font-semibold text-cyan-300 text-[11px]">{tm.event_type}</span>
                    <span className="text-[10px] font-mono text-slate-500">
                      {new Date(tm.event_time).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-slate-300 text-[11px]">{tm.description}</p>
                </div>
              ))
            ) : (
              <p className="text-slate-500 italic">No timeline entries.</p>
            )}
          </div>
        </div>
      </div>

      {/* Threat Evidence Table */}
      <div className="bg-[#0c1220] rounded-xl border border-slate-800 overflow-hidden">
        <div className="p-4 border-b border-slate-800">
          <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span>Forensic Evidence & Triggered Scam Tactics</span>
          </h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-[#090d16] text-slate-400 font-mono uppercase text-[10px]">
              <tr>
                <th className="py-3 px-4">Threat Category</th>
                <th className="py-3 px-4">Matched Forensic Excerpt</th>
                <th className="py-3 px-4">Contribution</th>
                <th className="py-3 px-4">Detailed Rule Tactic Explanation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {incident.threats && incident.threats.length > 0 ? (
                incident.threats.map((th, i) => (
                  <tr key={i} className="hover:bg-slate-800/30">
                    <td className="py-3 px-4 font-semibold text-white">{th.category}</td>
                    <td className="py-3 px-4 font-mono text-cyan-300 text-[11px]">
                      <span className="bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-800/30">
                        "{th.matched_text}"
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-red-400">+{th.contribution}</td>
                    <td className="py-3 px-4 text-slate-300 text-[11px] leading-relaxed">{th.explanation}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={4} className="py-4 text-center text-slate-500">
                    No specific threat patterns flagged.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Analyst Investigation Notes Section */}
      <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 space-y-4">
        <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
          <UserCheck className="w-4 h-4 text-cyan-400" />
          <span>Analyst Case Notes & Investigation Journal</span>
        </h2>

        {incident.analyst_notes ? (
          <div className="bg-[#070b14] p-4 rounded-lg border border-slate-800 text-xs font-mono text-slate-300 whitespace-pre-wrap leading-relaxed">
            {incident.analyst_notes}
          </div>
        ) : (
          <p className="text-xs text-slate-500 italic">No notes recorded yet for this case.</p>
        )}

        {/* Append Note Form */}
        <form onSubmit={handleAddNote} className="flex gap-2">
          <input
            type="text"
            placeholder="Append observation (e.g., 'Checked caller CLI with TRAI database', 'Victim did not transfer funds')..."
            value={newNote}
            onChange={(e) => setNewNote(e.target.value)}
            className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-400 border border-cyan-800/40 font-semibold text-xs rounded-lg transition flex items-center space-x-1.5"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Add Note</span>
          </button>
        </form>
      </div>
    </div>
  );
};
