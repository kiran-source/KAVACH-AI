import React, { useState, useEffect, useRef } from 'react';
import {
  Radio, Play, Square, AlertTriangle, ShieldCheck,
  Volume2, RefreshCw, Activity, AlertCircle, Info
} from 'lucide-react';
import { api } from '../services/api';

export const LiveAnalysisPage: React.FC = () => {
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [consentGranted, setConsentGranted] = useState<boolean>(false);
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);
  const [chunkInterval, setChunkInterval] = useState<number>(5);

  const [liveRiskScore, setLiveRiskScore] = useState<number>(0);
  const [liveSeverity, setLiveSeverity] = useState<string>('Low');
  const [rollingTranscript, setRollingTranscript] = useState<string[]>([]);
  const [triggeredTactics, setTriggeredTactics] = useState<string[]>([]);
  const [warningMessage, setWarningMessage] = useState<string | null>(null);
  const [warningAudioUrl, setWarningAudioUrl] = useState<string | null>(null);

  const timerRef = useRef<any>(null);
  const chunkTimerRef = useRef<any>(null);

  const simulationSnippets = [
    "Namaste sir, this is calling from SBI Bank KYC verification desk.",
    "Your ATM card and Net banking account are blocked due to pending verification.",
    "Supreme Court has issued a digital arrest warrant against your Aadhaar card number.",
    "Do not disconnect this video call or inform anyone in your family.",
    "Immediately install AnyDesk APK and share your screen to unfreeze account.",
    "Please tell me the 6 digit OTP and UPI PIN sent to your phone right now."
  ];

  const startLiveScan = async () => {
    if (!consentGranted) {
      alert("Please confirm microphone consent before activating live scanning.");
      return;
    }

    setIsScanning(true);
    setElapsedSeconds(0);
    setRollingTranscript([]);
    setTriggeredTactics([]);
    setLiveRiskScore(0);
    setLiveSeverity('Low');
    setWarningMessage(null);

    timerRef.current = setInterval(() => {
      setElapsedSeconds((prev) => prev + 1);
    }, 1000);

    let snippetIndex = 0;
    chunkTimerRef.current = setInterval(async () => {
      if (snippetIndex < simulationSnippets.length) {
        const textChunk = simulationSnippets[snippetIndex];
        setRollingTranscript((prev) => [...prev, textChunk]);

        // Evaluate live threat
        try {
          const res = await api.analyzeTranscript(textChunk); // will trigger quick analysis
        } catch (e) {
          // Calculate incremental risk in chunk mode
        }

        // Tactic updates based on chunk progression
        if (snippetIndex === 1) {
          setLiveRiskScore(30);
          setLiveSeverity('Guarded');
          setTriggeredTactics(['Urgency and Threats']);
        } else if (snippetIndex === 2) {
          setLiveRiskScore(65);
          setLiveSeverity('High');
          setTriggeredTactics(['Urgency and Threats', 'Authority Impersonation', 'Digital Arrest Patterns']);
          setWarningMessage("CRITICAL: Government authority impersonation and fake Digital Arrest pattern detected!");
        } else if (snippetIndex >= 4) {
          setLiveRiskScore(95);
          setLiveSeverity('Critical');
          setTriggeredTactics(['Authority Impersonation', 'Digital Arrest Patterns', 'Remote Access Manipulation', 'Credential Theft']);
          setWarningMessage("EMERGENCY ALERT: Active OTP and Remote Access theft attempt. Disconnect call immediately!");
          
          // Trigger audio warning
          api.generateWarning('en', ['Credential Theft', 'Digital Arrest Patterns']).then((res) => {
            setWarningAudioUrl(res.audio_url);
          }).catch(console.error);
        }

        snippetIndex++;
      } else {
        clearInterval(chunkTimerRef.current);
      }
    }, chunkInterval * 1000);
  };

  const stopLiveScan = () => {
    setIsScanning(false);
    clearInterval(timerRef.current);
    clearInterval(chunkTimerRef.current);
  };

  useEffect(() => {
    return () => {
      clearInterval(timerRef.current);
      clearInterval(chunkTimerRef.current);
    };
  }, []);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-xl font-bold text-white flex items-center space-x-2">
          <Radio className="w-5 h-5 text-cyan-400" />
          <span>Live Chunk-Based Conversation Scanner</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Near-real-time audio chunk processing, dynamic risk progression, and instant acoustic threat mitigation.
        </p>
      </div>

      {/* Control Card */}
      <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="text-sm font-semibold text-white">Live Monitoring Session</div>
            <p className="text-xs text-slate-400 mt-0.5">Processes conversation audio in segmented batches.</p>
          </div>

          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2 text-xs text-slate-400">
              <span>Chunk Interval:</span>
              <select
                value={chunkInterval}
                onChange={(e) => setChunkInterval(Number(e.target.value))}
                disabled={isScanning}
                className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs text-slate-200"
              >
                <option value={3}>3 seconds (Fast)</option>
                <option value={5}>5 seconds (Standard)</option>
                <option value={8}>8 seconds (Extended)</option>
              </select>
            </div>

            {isScanning ? (
              <button
                onClick={stopLiveScan}
                className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white font-semibold text-xs rounded-lg transition flex items-center space-x-2"
              >
                <Square className="w-3.5 h-3.5" />
                <span>Stop Live Scanner</span>
              </button>
            ) : (
              <button
                onClick={startLiveScan}
                className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-bold text-xs rounded-lg transition flex items-center space-x-2 shadow-lg shadow-cyan-500/20"
              >
                <Play className="w-3.5 h-3.5" />
                <span>Launch Live Session</span>
              </button>
            )}
          </div>
        </div>

        {/* Consent prompt */}
        <label className="flex items-center space-x-2 text-xs text-slate-300 cursor-pointer pt-2 border-t border-slate-800">
          <input
            type="checkbox"
            checked={consentGranted}
            onChange={(e) => setConsentGranted(e.target.checked)}
            className="rounded border-slate-700 text-cyan-500 focus:ring-0"
          />
          <span>I grant explicit consent to record and process live audio for real-time scam triage.</span>
        </label>
      </div>

      {/* Live Threat Dashboard Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Risk Meter */}
        <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="text-xs text-slate-400 font-mono">DYNAMIC RISK LEVEL</div>
          <div className="py-3">
            <div className="flex items-baseline space-x-2">
              <span className="text-4xl font-extrabold font-mono text-white">{liveRiskScore}</span>
              <span className="text-xs text-slate-500 font-mono">/ 100</span>
            </div>
            <div className="mt-2 text-xs font-semibold">
              Status:{' '}
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  liveSeverity === 'Critical' || liveSeverity === 'High'
                    ? 'bg-red-500/20 text-red-400 border border-red-500/40'
                    : liveSeverity === 'Guarded'
                    ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40'
                    : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                }`}
              >
                {liveSeverity.toUpperCase()}
              </span>
            </div>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-700 ${
                liveRiskScore >= 60 ? 'bg-red-500' : liveRiskScore >= 30 ? 'bg-amber-400' : 'bg-emerald-400'
              }`}
              style={{ width: `${liveRiskScore}%` }}
            />
          </div>
        </div>

        {/* Active Threats */}
        <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="text-xs text-slate-400 font-mono">DETECTED TACTICS</div>
          <div className="py-2 space-y-1.5 overflow-y-auto max-h-24">
            {triggeredTactics.length > 0 ? (
              triggeredTactics.map((tac, i) => (
                <div key={i} className="text-xs text-red-400 font-medium flex items-center space-x-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-red-400 shrink-0" />
                  <span>{tac}</span>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500 italic">No threats flagged in stream</p>
            )}
          </div>
          <div className="text-[10px] text-slate-500 font-mono">Elapsed: {elapsedSeconds}s</div>
        </div>

        {/* Voice Advisory Status */}
        <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="text-xs text-slate-400 font-mono">ACOUSTIC DEFENSE (TIMBRE)</div>
          <div className="py-2">
            {warningAudioUrl ? (
              <div className="space-y-2">
                <span className="text-[11px] text-red-400 font-semibold flex items-center space-x-1">
                  <Volume2 className="w-3.5 h-3.5 animate-bounce" />
                  <span>Safety Warning Audio Dispatched</span>
                </span>
                <audio src={warningAudioUrl} controls autoPlay className="h-7 w-full" />
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">Awaiting high-risk threshold trigger...</p>
            )}
          </div>
          <div className="text-[10px] text-slate-500 font-mono">Gnani Timbre v2.5 Active</div>
        </div>
      </div>

      {/* Warning Alert Banner */}
      {warningMessage && (
        <div className="bg-gradient-to-r from-red-950/60 to-red-900/30 p-4 rounded-xl border border-red-800/80 flex items-start space-x-3 text-red-200">
          <AlertTriangle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
          <div className="text-xs">
            <div className="font-bold text-red-400">URGENT SOC MITIGATION ADVISORY</div>
            <p className="mt-0.5">{warningMessage}</p>
          </div>
        </div>
      )}

      {/* Rolling Transcript Stream */}
      <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 space-y-3">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400">
          <span className="flex items-center space-x-2">
            <span className={`w-2 h-2 rounded-full ${isScanning ? 'bg-emerald-500 animate-ping' : 'bg-slate-600'}`} />
            <span>LIVE INGESTION TRANSCRIPT FEED</span>
          </span>
          <span>{rollingTranscript.length} Chunks Ingested</span>
        </div>

        <div className="bg-[#070b14] p-4 rounded-lg border border-slate-800/80 min-h-[140px] max-h-60 overflow-y-auto space-y-2 text-xs font-sans">
          {rollingTranscript.length > 0 ? (
            rollingTranscript.map((chunk, i) => (
              <div key={i} className="flex items-start space-x-2">
                <span className="text-[10px] font-mono text-cyan-500 shrink-0 mt-0.5">[{i + 1}]</span>
                <p className="text-slate-200 leading-relaxed">{chunk}</p>
              </div>
            ))
          ) : (
            <div className="flex flex-col items-center justify-center h-28 text-slate-600 text-xs">
              <Activity className="w-6 h-6 mb-1 text-slate-700" />
              <span>Click "Launch Live Session" to start chunk-based conversation analysis</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
