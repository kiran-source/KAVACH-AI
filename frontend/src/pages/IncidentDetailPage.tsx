import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ShieldAlert, ArrowLeft, Download, FileText, Clock,
  Volume2, UserCheck, AlertTriangle, CheckCircle, RefreshCw,
  ExternalLink, Send, Shield, Copy, Check, Headphones,
  AlertOctagon, Info
} from 'lucide-react';
import { api } from '../services/api';
import { IncidentDetail } from '../types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/common/Card';
import { SeverityBadge, StatusBadge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { StatusIndicator } from '../components/common/StatusIndicator';
import { AudioWaveform } from '../components/common/AudioWaveform';

export const IncidentDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [incident, setIncident] = useState<IncidentDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [newNote, setNewNote] = useState<string>('');
  const [statusUpdating, setStatusUpdating] = useState<boolean>(false);
  const [generatingReport, setGeneratingReport] = useState<boolean>(false);
  const [copiedId, setCopiedId] = useState<boolean>(false);
  const [copiedTranscript, setCopiedTranscript] = useState<boolean>(false);

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

  const copyIncidentId = () => {
    if (incident?.incident_number) {
      navigator.clipboard.writeText(incident.incident_number);
      setCopiedId(true);
      setTimeout(() => setCopiedId(false), 2000);
    }
  };

  const copyTranscriptText = () => {
    if (incident?.transcript_text) {
      navigator.clipboard.writeText(incident.transcript_text);
      setCopiedTranscript(true);
      setTimeout(() => setCopiedTranscript(false), 2000);
    }
  };

  if (loading || !incident) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center animate-pulse">
          <RefreshCw className="w-6 h-6 text-cyan-400 animate-spin" />
        </div>
        <div className="text-center">
          <p className="text-sm font-semibold text-white">Loading Incident Dossier</p>
          <p className="text-xs text-slate-500 font-mono mt-1">Retrieving forensic transcript and evidence logs...</p>
        </div>
      </div>
    );
  }

  const getLanguageName = (lang: string) => {
    const l = lang.toLowerCase();
    if (l === 'te') return 'Telugu (తెలుగు)';
    if (l === 'hi') return 'Hindi (हिंदी)';
    return 'English';
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Top Breadcrumb & Action Navigation */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <button
          onClick={() => navigate('/incidents')}
          className="inline-flex items-center space-x-2 text-xs font-mono text-slate-400 hover:text-cyan-400 transition-colors focus:outline-none"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Triage Queue</span>
        </button>

        <div className="flex items-center space-x-3">
          <Button
            variant="outline"
            size="sm"
            onClick={copyIncidentId}
            className="font-mono text-xs"
          >
            {copiedId ? <Check className="w-3.5 h-3.5 text-emerald-400 mr-1.5" /> : <Copy className="w-3.5 h-3.5 mr-1.5" />}
            <span>{copiedId ? 'Copied ID' : 'Copy Incident ID'}</span>
          </Button>

          <Button
            variant="primary"
            size="sm"
            onClick={handleGenerateReport}
            isLoading={generatingReport}
            className="shadow-glow-cyan text-xs"
          >
            <FileText className="w-4 h-4 mr-1.5" />
            <span>Export Official SOC PDF</span>
          </Button>
        </div>
      </div>

      {/* Main Dossier Header Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-navy-900 border border-slate-800/80 p-6 shadow-2xl backdrop-blur-xl">
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />
        
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-mono font-bold text-sm text-cyan-400 bg-cyan-950/80 border border-cyan-800/60 px-2.5 py-0.5 rounded-md">
                {incident.incident_number}
              </span>
              <SeverityBadge severity={incident.severity} size="sm" />
              <StatusBadge status={incident.status} size="sm" />
              <span className="text-xs font-mono text-slate-500 hidden sm:inline">
                Logged: {new Date(incident.created_at).toUTCString()}
              </span>
            </div>

            <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              {incident.title}
            </h1>
            <p className="text-xs text-slate-400 max-w-3xl leading-relaxed">
              Forensic audio incident analyzed by KAVACH hybrid engine. Preserving chain of custody,
              acoustic metadata, and explainable rule trigger proofs.
            </p>
          </div>

          {/* Quick Threat Score Pill */}
          <div className="flex items-center space-x-4 p-4 rounded-xl bg-navy-950/80 border border-slate-800/90 shrink-0">
            <div className="text-right">
              <div className="text-[10px] font-mono uppercase tracking-wider text-slate-400">Hybrid Risk Score</div>
              <div className="flex items-baseline justify-end space-x-1 mt-0.5">
                <span className={`text-3xl font-black font-mono tracking-tight ${
                  incident.risk_score >= 80 ? 'text-red-400' :
                  incident.risk_score >= 60 ? 'text-amber-400' :
                  incident.risk_score >= 30 ? 'text-cyan-400' : 'text-emerald-400'
                }`}>
                  {incident.risk_score}
                </span>
                <span className="text-xs text-slate-500 font-mono">/ 100</span>
              </div>
            </div>
            <div className="w-12 h-12 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center">
              <ShieldAlert className={`w-6 h-6 ${
                incident.risk_score >= 80 ? 'text-red-400' :
                incident.risk_score >= 60 ? 'text-amber-400' : 'text-emerald-400'
              }`} />
            </div>
          </div>
        </div>

        {/* Operational Metadata Bar */}
        <div className="mt-6 pt-4 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs font-sans">
          <div>
            <span className="text-slate-500 block mb-1 font-mono uppercase text-[10px]">Triage Workflow Status</span>
            <select
              value={incident.status}
              onChange={(e) => handleStatusChange(e.target.value)}
              disabled={statusUpdating}
              className="w-full bg-navy-950 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-cyan-300 font-semibold focus:outline-none focus:border-cyan-500"
            >
              <option value="New">New (Pending Triage)</option>
              <option value="Under Review">Under Review</option>
              <option value="Confirmed Suspicious">Confirmed Suspicious</option>
              <option value="False Positive">False Positive</option>
              <option value="Resolved">Resolved & Closed</option>
            </select>
          </div>

          <div>
            <span className="text-slate-500 block mb-1 font-mono uppercase text-[10px]">Assigned SOC Analyst</span>
            <div className="px-3 py-1.5 rounded-lg bg-navy-950 border border-slate-800 text-slate-200 font-medium truncate flex items-center space-x-1.5">
              <UserCheck className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
              <span>{incident.assigned_analyst || 'SOC Analyst 1'}</span>
            </div>
          </div>

          <div>
            <span className="text-slate-500 block mb-1 font-mono uppercase text-[10px]">Audio Ingestion File</span>
            <div className="px-3 py-1.5 rounded-lg bg-navy-950 border border-slate-800 text-slate-300 font-mono text-[11px] truncate flex items-center space-x-1.5">
              <Headphones className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
              <span title={incident.audio_filename}>{incident.audio_filename}</span>
            </div>
          </div>

          <div>
            <span className="text-slate-500 block mb-1 font-mono uppercase text-[10px]">Language Detected</span>
            <div className="px-3 py-1.5 rounded-lg bg-navy-950 border border-slate-800 text-cyan-400 font-mono text-[11px] font-bold">
              {getLanguageName(incident.detected_language)}
            </div>
          </div>
        </div>
      </div>

      {/* Two Column Investigation Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Audio & Transcript (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Audio Evidence Container with Waveform */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Headphones className="w-4 h-4 text-cyan-400" />
                  <CardTitle>Acoustic Forensics & Audio Playback</CardTitle>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  {incident.audio_filename.split('.').pop()?.toUpperCase() || 'WAV'} • RAW STREAM
                </span>
              </div>
              <CardDescription>
                Synchronized acoustic stream preserved under continuous SHA-256 chain of custody.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-4 rounded-xl bg-navy-950 border border-slate-800/80 space-y-3">
                <AudioWaveform isRecording={false} height={64} />
                {incident.audio_id && (
                  <div className="pt-2 flex items-center justify-between gap-4">
                    <audio
                      src={`/api/v1/audio/${incident.audio_id}`}
                      controls
                      className="w-full h-8 rounded-lg filter invert-[0.85] hue-rotate-180"
                    />
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Verbatim Transcript with Threat Highlighting */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <FileText className="w-4 h-4 text-cyan-400" />
                  <CardTitle>Prisma v3 Verbatim Speech Transcript</CardTitle>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={copyTranscriptText}
                  className="text-xs font-mono h-7 px-2"
                >
                  {copiedTranscript ? <Check className="w-3.5 h-3.5 text-emerald-400 mr-1" /> : <Copy className="w-3.5 h-3.5 mr-1" />}
                  <span>{copiedTranscript ? 'Copied' : 'Copy'}</span>
                </Button>
              </div>
              <CardDescription>
                High-fidelity automatic speech recognition with native code-mixed Indian accent support.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="p-4 rounded-xl bg-navy-950 border border-slate-800/90 max-h-72 overflow-y-auto">
                <p className="text-xs text-slate-200 leading-relaxed font-sans whitespace-pre-wrap selection:bg-cyan-500 selection:text-navy-950">
                  "{incident.transcript_text}"
                </p>
              </div>
              <div className="mt-3 flex items-center justify-between text-[11px] text-slate-500 font-mono">
                <span>Recognized by Gnani Prisma v3</span>
                <span>Language: {incident.detected_language.toUpperCase()}</span>
              </div>
            </CardContent>
          </Card>

          {/* Chronological Audit Timeline */}
          <Card>
            <CardHeader>
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-cyan-400" />
                <CardTitle>Chronological Incident Audit Timeline</CardTitle>
              </div>
              <CardDescription>
                Immutable chronological event trail from ingestion to analyst disposition.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {incident.timeline && incident.timeline.length > 0 ? (
                  <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
                    {incident.timeline.map((tm, idx) => (
                      <div key={idx} className="relative">
                        <div className="absolute -left-6 top-1 w-2.5 h-2.5 rounded-full bg-cyan-400 ring-4 ring-navy-900" />
                        <div className="flex items-center space-x-2">
                          <span className="text-xs font-bold text-white">{tm.event_type}</span>
                          <span className="text-[10px] font-mono text-slate-500">
                            {new Date(tm.event_time).toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 mt-1">{tm.description}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 italic">No timeline entries recorded.</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Threats & Notes (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          {/* Matched Threat Tactics & Evidence */}
          <Card>
            <CardHeader>
              <div className="flex items-center space-x-2">
                <AlertOctagon className="w-4 h-4 text-red-400" />
                <CardTitle>Triggered Scam Tactics & Evidence</CardTitle>
              </div>
              <CardDescription>
                Deterministic rule matches and weighted threat contribution breakdown.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {incident.threats && incident.threats.length > 0 ? (
                incident.threats.map((th, i) => (
                  <div
                    key={i}
                    className="p-3.5 rounded-xl bg-navy-950 border border-slate-800/80 hover:border-slate-700 transition space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-white flex items-center space-x-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-red-400" />
                        <span>{th.category}</span>
                      </span>
                      <span className="font-mono text-xs font-bold text-red-400 bg-red-950/60 border border-red-800/40 px-2 py-0.5 rounded">
                        +{th.contribution} pts
                      </span>
                    </div>

                    <div className="p-2 rounded bg-navy-900 border border-slate-800/60 font-mono text-[11px] text-cyan-300">
                      "{th.matched_text}"
                    </div>

                    <p className="text-[11px] text-slate-400 leading-relaxed">
                      {th.explanation}
                    </p>
                  </div>
                ))
              ) : (
                <div className="p-6 text-center text-slate-500 text-xs">
                  <Shield className="w-8 h-8 text-emerald-500/40 mx-auto mb-2" />
                  <p>No deterministic scam patterns violated.</p>
                  <p className="text-[11px] text-slate-600 mt-1">Classified as benign or below risk threshold.</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Analyst Case Notes & Journal */}
          <Card>
            <CardHeader>
              <div className="flex items-center space-x-2">
                <UserCheck className="w-4 h-4 text-cyan-400" />
                <CardTitle>Analyst Notes & Case Journal</CardTitle>
              </div>
              <CardDescription>
                Record investigation findings, caller CLI lookups, and mitigation steps taken.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {incident.analyst_notes ? (
                <div className="p-3.5 rounded-xl bg-navy-950 border border-slate-800/80 text-xs font-mono text-slate-300 whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">
                  {incident.analyst_notes}
                </div>
              ) : (
                <div className="p-4 rounded-xl bg-navy-950/50 border border-slate-800/50 text-center text-slate-500 text-xs">
                  No analyst notes logged for this incident yet.
                </div>
              )}

              {/* Add Note Input */}
              <form onSubmit={handleAddNote} className="space-y-2">
                <div className="relative">
                  <textarea
                    rows={3}
                    placeholder="Append observation (e.g., 'Checked caller number with TRAI DND database; victim advised to report on 1930 portal')..."
                    value={newNote}
                    onChange={(e) => setNewNote(e.target.value)}
                    className="w-full bg-navy-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 font-sans resize-none"
                  />
                </div>
                <div className="flex justify-end">
                  <Button
                    type="submit"
                    variant="secondary"
                    size="sm"
                    disabled={!newNote.trim()}
                    className="text-xs"
                  >
                    <Send className="w-3.5 h-3.5 mr-1.5" />
                    <span>Add Note</span>
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};
