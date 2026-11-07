import React, { useState, useEffect } from 'react';
import {
  FileText, Mic, ShieldAlert, Key, Search, ExternalLink,
  Download, Clock, CheckCircle, Database, Filter, ArrowUpRight
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/common/Card';
import { SeverityBadge, StatusBadge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { SearchInput } from '../components/common/SearchInput';
import { EmptyState } from '../components/common/EmptyState';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { IncidentSummary, IncidentDetail } from '../types';

interface EvidenceItem {
  id: string;
  incidentId: string;
  incidentNumber: string;
  type: 'Audio Container' | 'Verbatim Transcript' | 'Forensic Threat Match' | 'Chain of Custody';
  source: string;
  summary: string;
  timestamp: string;
  severity: string;
  details: string;
  category?: string;
  hashOrRef?: string;
}

export const EvidencePage: React.FC = () => {
  const [incidents, setIncidents] = useState<IncidentSummary[]>([]);
  const [evidenceList, setEvidenceList] = useState<EvidenceItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [filterType, setFilterType] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceItem | null>(null);

  useEffect(() => {
    loadEvidence();
  }, []);

  const loadEvidence = async () => {
    try {
      setLoading(true);
      const incs = await api.listIncidents();
      setIncidents(incs);

      // Fetch top 10 incidents for detailed evidence reconstruction
      const items: EvidenceItem[] = [];
      const sampleIncidents = incs.slice(0, 12);

      await Promise.all(
        sampleIncidents.map(async (inc) => {
          try {
            const detail: IncidentDetail = await api.getIncident(inc.id);

            // 1. Audio Container Evidence
            if (detail.audio_filename) {
              items.push({
                id: `EVD-AUD-${detail.id.slice(0, 6)}`,
                incidentId: detail.id,
                incidentNumber: detail.incident_number,
                type: 'Audio Container',
                source: 'User Audio Ingestion / Webhook',
                summary: `Acoustic container file: ${detail.audio_filename}`,
                timestamp: detail.created_at,
                severity: detail.severity,
                details: `Authenticated audio recording ingested into forensic vault. Container: ${detail.audio_filename}. Audio ID: ${detail.audio_id || 'LOCAL-VAULT'}.`,
                hashOrRef: detail.audio_id || detail.audio_filename,
              });
            }

            // 2. Verbatim Transcript Evidence
            if (detail.transcript_text) {
              items.push({
                id: `EVD-TRS-${detail.id.slice(0, 6)}`,
                incidentId: detail.id,
                incidentNumber: detail.incident_number,
                type: 'Verbatim Transcript',
                source: 'Gnani Prisma v3.0 STT',
                summary: `Spoken dialogue transcript (${detail.detected_language?.toUpperCase() || 'MULTI'})`,
                timestamp: detail.created_at,
                severity: detail.severity,
                details: detail.transcript_text,
                category: detail.detected_language,
                hashOrRef: `LANG-${detail.detected_language}`,
              });
            }

            // 3. Matched Threat Indicators
            if (detail.threats && detail.threats.length > 0) {
              detail.threats.forEach((th, idx) => {
                items.push({
                  id: `EVD-THR-${detail.id.slice(0, 4)}-${idx + 1}`,
                  incidentId: detail.id,
                  incidentNumber: detail.incident_number,
                  type: 'Forensic Threat Match',
                  source: `Threat Engine [${th.rule_id}]`,
                  summary: `Matched: "${th.matched_text}" (${th.category})`,
                  timestamp: detail.created_at,
                  severity: detail.severity,
                  details: th.explanation,
                  category: th.category,
                  hashOrRef: th.rule_id,
                });
              });
            }
          } catch (err) {
            console.error(`Failed to load evidence for incident ${inc.id}`, err);
          }
        })
      );

      // Sort by creation time descending
      items.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      setEvidenceList(items);
      if (items.length > 0) setSelectedEvidence(items[0]);
    } catch (err) {
      console.error('Failed to load incidents', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredEvidence = evidenceList.filter((item) => {
    const matchesType = filterType === 'All' || item.type === filterType;
    const matchesSearch =
      item.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.incidentNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.details.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesType && matchesSearch;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 font-mono text-xs mb-1">
            <Database className="w-4 h-4" />
            <span>KAVACH AI FORENSIC EVIDENCE VAULT</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100">
            Chain of Custody & Evidence Explorer
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Verifiable repository of audio recordings, verbatim multilingual speech transcripts, forensic indicator matches, and timeline audit logs.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={loadEvidence} isLoading={loading}>
            Refresh Evidence
          </Button>
          <Link to="/reports">
            <Button variant="secondary" size="sm" rightIcon={<ArrowUpRight className="w-3.5 h-3.5" />}>
              View Reports
            </Button>
          </Link>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-3 bg-[#0d1424] p-3 rounded-xl border border-slate-800">
        <div className="w-full md:w-96">
          <SearchInput
            value={searchQuery}
            onChangeValue={setSearchQuery}
            placeholder="Search by Evidence ID, Incident #, or content..."
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto">
          {['All', 'Audio Container', 'Verbatim Transcript', 'Forensic Threat Match'].map((t) => (
            <button
              key={t}
              onClick={() => setFilterType(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                filterType === t
                  ? 'bg-cyan-500 text-slate-950 font-semibold shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid: List + Detail */}
      {filteredEvidence.length === 0 ? (
        <EmptyState
          icon={Database}
          title="No forensic evidence matches"
          description="No evidence records match the selected filter or query. Ingest audio files to generate forensic records."
          actionLabel="Clear Filters"
          onAction={() => {
            setFilterType('All');
            setSearchQuery('');
          }}
        />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Table / List (7 cols) */}
          <div className="lg:col-span-7 space-y-2">
            <div className="text-xs font-mono text-slate-500 flex justify-between px-1">
              <span>SHOWING {filteredEvidence.length} EVIDENCE RECORDS</span>
              <span>SORTED BY INGESTION UTC</span>
            </div>

            <div className="space-y-2 max-h-[640px] overflow-y-auto pr-1">
              {filteredEvidence.map((item) => {
                const isSelected = selectedEvidence?.id === item.id;
                return (
                  <div
                    key={item.id}
                    onClick={() => setSelectedEvidence(item)}
                    className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                      isSelected
                        ? 'bg-[#131c31] border-cyan-500/50 shadow-md shadow-cyan-950/20'
                        : 'bg-[#0d1424] border-slate-800/80 hover:border-slate-700 hover:bg-[#10192e]'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2 mb-1.5">
                      <div className="flex items-center space-x-2 font-mono text-xs">
                        <span className="font-bold text-cyan-400">{item.id}</span>
                        <span className="text-slate-500">·</span>
                        <span className="text-slate-300 font-semibold">{item.incidentNumber}</span>
                      </div>
                      <SeverityBadge severity={item.severity} size="xs" />
                    </div>

                    <p className="text-xs font-medium text-slate-200 line-clamp-1">{item.summary}</p>

                    <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-800/40 text-[10px] font-mono text-slate-400">
                      <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700/60">
                        {item.type}
                      </span>
                      <span>{new Date(item.timestamp).toLocaleString()}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right Detail Dossier (5 cols) */}
          <div className="lg:col-span-5">
            {selectedEvidence ? (
              <Card elevated className="h-full border-slate-700/60 sticky top-4">
                <CardHeader className="bg-slate-900/40">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="font-mono text-xs text-cyan-400 font-bold">{selectedEvidence.id}</span>
                      <CardTitle className="text-base text-slate-100 mt-0.5">
                        {selectedEvidence.type}
                      </CardTitle>
                    </div>
                    <SeverityBadge severity={selectedEvidence.severity} size="sm" />
                  </div>
                </CardHeader>

                <CardContent className="space-y-4 p-5">
                  <div>
                    <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
                      Associated Incident Reference
                    </span>
                    <Link
                      to={`/incidents/${selectedEvidence.incidentId}`}
                      className="inline-flex items-center space-x-1.5 text-xs font-mono font-semibold text-cyan-400 hover:text-cyan-300 bg-cyan-950/30 px-2.5 py-1.5 rounded-lg border border-cyan-800/40 transition-colors"
                    >
                      <span>{selectedEvidence.incidentNumber}</span>
                      <ArrowUpRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>

                  <div>
                    <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
                      Evidence Source & Provenance
                    </span>
                    <p className="text-xs text-slate-200 font-mono bg-[#070b14] p-2.5 rounded-lg border border-slate-800">
                      {selectedEvidence.source}
                    </p>
                  </div>

                  <div>
                    <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
                      Ingestion Timestamp (UTC)
                    </span>
                    <div className="flex items-center space-x-2 text-xs text-slate-300 font-mono">
                      <Clock className="w-3.5 h-3.5 text-slate-500" />
                      <span>{new Date(selectedEvidence.timestamp).toUTCString()}</span>
                    </div>
                  </div>

                  <div>
                    <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
                      Forensic Content Payload
                    </span>
                    <div className="p-3.5 rounded-lg bg-[#070b14] border border-slate-800 text-xs text-slate-200 font-mono max-h-60 overflow-y-auto leading-relaxed">
                      {selectedEvidence.details}
                    </div>
                  </div>

                  {selectedEvidence.hashOrRef && (
                    <div>
                      <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block mb-1">
                        Cryptographic Hash / Resource Key
                      </span>
                      <span className="text-[11px] font-mono text-slate-400 bg-slate-900 px-2 py-1 rounded block truncate border border-slate-800">
                        {selectedEvidence.hashOrRef}
                      </span>
                    </div>
                  )}

                  <div className="pt-2">
                    <Link to={`/incidents/${selectedEvidence.incidentId}`} className="block">
                      <Button variant="primary" size="sm" className="w-full" rightIcon={<ExternalLink className="w-3.5 h-3.5" />}>
                        Open Investigation Dossier
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <EmptyState
                icon={Database}
                title="Select an evidence item"
                description="Click on any evidence record on the left to inspect its cryptographic metadata, transcript payload, and chain of custody."
              />
            )}
          </div>
        </div>
      )}
    </div>
  );
};

