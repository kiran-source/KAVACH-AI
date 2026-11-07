import React, { useState, useEffect, useRef } from 'react';
import {
  Radio, Play, Square, AlertTriangle, ShieldCheck,
  Volume2, RefreshCw, Activity, AlertCircle, Info, Mic,
  VolumeX, ShieldAlert, Sparkles, Check, Headphones
} from 'lucide-react';
import { api } from '../services/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/common/Card';
import { SeverityBadge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { StatusIndicator } from '../components/common/StatusIndicator';
import { AudioWaveform } from '../components/common/AudioWaveform';

export const LiveAnalysisPage: React.FC = () => {
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [consentGranted, setConsentGranted] = useState<boolean>(false);
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);
  const [chunkInterval, setChunkInterval] = useState<number>(5);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('auto');

  // Real-time calculated threat state
  const [liveRiskScore, setLiveRiskScore] = useState<number>(0);
  const [liveSeverity, setLiveSeverity] = useState<string>('Low');
  const [rollingTranscript, setRollingTranscript] = useState<{ id: number; text: string; time: string }[]>([]);
  const [triggeredTactics, setTriggeredTactics] = useState<string[]>([]);
  const [warningMessage, setWarningMessage] = useState<string | null>(null);
  const [warningAudioUrl, setWarningAudioUrl] = useState<string | null>(null);
  const [chunkStatus, setChunkStatus] = useState<string>('Idle');

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const timerRef = useRef<any>(null);
  const cumulativeTextRef = useRef<string>('');
  const chunkCountRef = useRef<number>(0);

  const startLiveScan = async () => {
    if (!consentGranted) {
      alert("Please check and confirm microphone consent before activating live chunk scanning.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      let mimeType = 'audio/webm';
      let extension = 'webm';
      if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
        mimeType = 'audio/webm;codecs=opus';
        extension = 'webm';
      } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
        mimeType = 'audio/mp4';
        extension = 'm4a';
      } else if (MediaRecorder.isTypeSupported('audio/wav')) {
        mimeType = 'audio/wav';
        extension = 'wav';
      }

      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      mediaRecorderRef.current = recorder;

      setIsScanning(true);
      setElapsedSeconds(0);
      setRollingTranscript([]);
      setTriggeredTactics([]);
      setLiveRiskScore(0);
      setLiveSeverity('Low');
      setWarningMessage(null);
      setWarningAudioUrl(null);
      cumulativeTextRef.current = '';
      chunkCountRef.current = 0;
      setChunkStatus('Actively listening...');

      timerRef.current = setInterval(() => {
        setElapsedSeconds((prev) => prev + 1);
      }, 1000);

      recorder.ondataavailable = async (e: BlobEvent) => {
        if (e.data && e.data.size > 100) {
          chunkCountRef.current += 1;
          const currentChunkNum = chunkCountRef.current;
          setChunkStatus(`Processing buffer #${currentChunkNum}...`);

          try {
            const chunkBlob = new Blob([e.data], { type: recorder.mimeType || mimeType });
            const chunkFile = new File([chunkBlob], `live_chunk_${Date.now()}.${extension}`, {
              type: recorder.mimeType || mimeType
            });

            // 1. Upload chunk
            const uploadRes = await api.uploadAudio(chunkFile);

            // 2. Transcribe chunk via Prisma
            const transRes = await api.transcribeAudio(uploadRes.audio_id, selectedLanguage);
            const chunkText = (transRes.full_text || '').trim();

            if (chunkText) {
              const timestamp = new Date().toLocaleTimeString();
              setRollingTranscript((prev) => [
                ...prev,
                { id: currentChunkNum, text: chunkText, time: timestamp }
              ]);

              // 3. Accumulate context & evaluate incremental threat
              cumulativeTextRef.current = `${cumulativeTextRef.current} ${chunkText}`.trim();
              const analysisRes = await api.analyzeText(cumulativeTextRef.current, transRes.language || 'en');

              setLiveRiskScore(analysisRes.risk_score);
              setLiveSeverity(analysisRes.severity);
              setTriggeredTactics(analysisRes.categories || []);

              // 4. Trigger acoustic safety alert if high risk
              if (analysisRes.risk_score >= 65 && !warningAudioUrl) {
                setWarningMessage(
                  `URGENT: Social engineering detected (${(analysisRes.categories || []).join(', ')}). Advise victim not to share credentials!`
                );
                try {
                  const warnRes = await api.generateWarning(
                    transRes.language?.split('-')[0] || 'en',
                    analysisRes.categories || ['Credential Theft']
                  );
                  if (warnRes.audio_url) {
                    setWarningAudioUrl(warnRes.audio_url);
                  }
                } catch (warnErr) {
                  console.error("Warning audio generation error:", warnErr);
                }
              }
            } else {
              setChunkStatus(`Buffer #${currentChunkNum}: Silence / low audio detected`);
            }
          } catch (err) {
            console.error("Live chunk processing error:", err);
            setChunkStatus(`Buffer #${currentChunkNum}: Awaiting audible speech`);
          }
        }
      };

      recorder.start(chunkInterval * 1000);
    } catch (err) {
      console.error("Microphone access failed:", err);
      alert("Microphone permission denied or audio device unavailable.");
      setIsScanning(false);
    }
  };

  const stopLiveScan = () => {
    setIsScanning(false);
    setChunkStatus('Session Terminated');

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
    }
    clearInterval(timerRef.current);
  };

  useEffect(() => {
    return () => {
      clearInterval(timerRef.current);
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
              <Radio className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                Real-Time Audio Stream Triage (Mic Ingestion)
              </h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Ingests live microphone buffers, performs streaming LID & Prisma STT, and executes incremental threat detection.
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <StatusIndicator
            status={isScanning ? 'online' : 'offline'}
            label={isScanning ? `LIVE SCANNING (${elapsedSeconds}s)` : 'STANDBY'}
            pulse={isScanning}
          />
        </div>
      </div>

      {/* Control Card with Waveform */}
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <CardTitle>Microphone Buffer Capture Controller</CardTitle>
              <CardDescription>
                Continuous chunk ingestion configured for low-latency scam triage.
              </CardDescription>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              {/* Language selection */}
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                disabled={isScanning}
                className="bg-navy-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
              >
                <option value="auto">Auto Detect Language</option>
                <option value="te">Telugu (తెలుగు)</option>
                <option value="hi">Hindi (हिन्दी)</option>
                <option value="en">English</option>
              </select>

              {/* Buffer Size */}
              <select
                value={chunkInterval}
                onChange={(e) => setChunkInterval(Number(e.target.value))}
                disabled={isScanning}
                className="bg-navy-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
              >
                <option value={3}>3s Buffers (Fast)</option>
                <option value={5}>5s Buffers (Standard)</option>
                <option value={8}>8s Buffers (Contextual)</option>
              </select>

              {isScanning ? (
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={stopLiveScan}
                  className="shadow-glow-crimson text-xs"
                >
                  <Square className="w-3.5 h-3.5 mr-1.5" />
                  <span>Stop Capture</span>
                </Button>
              ) : (
                <Button
                  variant="primary"
                  size="sm"
                  onClick={startLiveScan}
                  className="shadow-glow-cyan text-xs"
                >
                  <Play className="w-3.5 h-3.5 mr-1.5" />
                  <span>Start Live Stream</span>
                </Button>
              )}
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Dynamic Audio Visualizer */}
          <div className="p-4 rounded-xl bg-navy-950 border border-slate-800/80 space-y-2">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span className="flex items-center space-x-2">
                <Mic className={`w-3.5 h-3.5 ${isScanning ? 'text-cyan-400 animate-pulse' : 'text-slate-500'}`} />
                <span>ACOUSTIC STREAM ACTIVITY</span>
              </span>
              <span className="text-cyan-400">{chunkStatus}</span>
            </div>
            <AudioWaveform isRecording={isScanning} height={56} />
          </div>

          {/* Consent Checkbox */}
          <label className="flex items-start space-x-2.5 text-xs text-slate-300 cursor-pointer pt-2 border-t border-slate-800/80">
            <input
              type="checkbox"
              checked={consentGranted}
              onChange={(e) => setConsentGranted(e.target.checked)}
              className="mt-0.5 w-4 h-4 rounded border-slate-700 text-cyan-500 focus:ring-0 bg-navy-950"
            />
            <span className="leading-relaxed">
              I grant explicit consent to capture local microphone audio for automated social-engineering triage.
              No audio is transmitted outside localhost during evaluation mode.
            </span>
          </label>
        </CardContent>
      </Card>

      {/* Real-Time Live Threat Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Risk Gauge */}
        <Card className="bg-navy-900/70 border-slate-800">
          <CardContent className="p-5 flex flex-col justify-between h-full">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono text-slate-400 uppercase">CALCULATED THREAT SCORE</span>
                <SeverityBadge severity={liveSeverity} size="sm" />
              </div>
              <div className="flex items-baseline space-x-2 mt-2">
                <span className="text-4xl font-extrabold font-mono text-white">{liveRiskScore}</span>
                <span className="text-xs text-slate-500 font-mono">/ 100</span>
              </div>
            </div>

            <div className="mt-4">
              <div className="w-full bg-navy-950 h-2 rounded-full overflow-hidden border border-slate-800">
                <div
                  className={`h-full transition-all duration-700 ${
                    liveRiskScore >= 60 ? 'bg-red-500' : liveRiskScore >= 30 ? 'bg-amber-400' : 'bg-emerald-400'
                  }`}
                  style={{ width: `${liveRiskScore}%` }}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Active Detected Tactics */}
        <Card className="bg-navy-900/70 border-slate-800">
          <CardContent className="p-5 flex flex-col justify-between h-full">
            <div>
              <span className="text-[11px] font-mono text-slate-400 uppercase">IDENTIFIED ATTACK TACTICS</span>
              <div className="mt-2.5 space-y-1.5 max-h-24 overflow-y-auto">
                {triggeredTactics.length > 0 ? (
                  triggeredTactics.map((tac, i) => (
                    <div key={i} className="text-xs text-red-400 font-medium flex items-center space-x-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-red-400 shrink-0" />
                      <span>{tac}</span>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-500 italic">No suspicious tactics detected in speech</p>
                )}
              </div>
            </div>
            <div className="text-[10px] text-slate-500 font-mono mt-2">Elapsed: {elapsedSeconds}s</div>
          </CardContent>
        </Card>

        {/* Timbre Voice Warning */}
        <Card className="bg-navy-900/70 border-slate-800">
          <CardContent className="p-5 flex flex-col justify-between h-full">
            <div>
              <span className="text-[11px] font-mono text-slate-400 uppercase">TIMBRE ACOUSTIC DEFENSE</span>
              <div className="mt-2">
                {warningAudioUrl ? (
                  <div className="space-y-2">
                    <span className="text-xs text-red-400 font-semibold flex items-center space-x-1.5">
                      <Volume2 className="w-4 h-4 animate-bounce" />
                      <span>Safety Warning Audio Synthesized</span>
                    </span>
                    <audio src={warningAudioUrl} controls autoPlay className="h-7 w-full filter invert-[0.85] hue-rotate-180" />
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 italic">
                    Armed — synthesized intervention triggers immediately upon Critical threat threshold.
                  </p>
                )}
              </div>
            </div>
            <div className="text-[10px] text-slate-500 font-mono mt-2">Gnani Timbre v2.5 Online</div>
          </CardContent>
        </Card>
      </div>

      {/* Warning Alert Banner */}
      {warningMessage && (
        <div className="p-4 rounded-xl bg-gradient-to-r from-red-950/80 to-navy-900 border border-red-800/80 flex items-start space-x-3 text-red-200 shadow-glow-crimson">
          <AlertTriangle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
          <div className="text-xs">
            <div className="font-bold text-red-400 uppercase font-mono tracking-wider">
              CRITICAL SOC DEFENSE MITIGATION ADVISORY
            </div>
            <p className="mt-1 leading-relaxed">{warningMessage}</p>
          </div>
        </div>
      )}

      {/* Rolling Ingestion Transcript Feed */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              <CardTitle>Continuous Speech Ingestion Transcript</CardTitle>
            </div>
            <span className="text-xs font-mono text-slate-400">
              {rollingTranscript.length} Buffer Windows Processed
            </span>
          </div>
          <CardDescription>
            Chronological speech buffer transcription streamed from Gnani Prisma.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="p-4 rounded-xl bg-navy-950 border border-slate-800/90 min-h-[160px] max-h-72 overflow-y-auto space-y-2.5 font-sans">
            {rollingTranscript.length > 0 ? (
              rollingTranscript.map((chunk) => (
                <div key={chunk.id} className="flex items-start space-x-2.5 border-b border-slate-800/40 pb-2">
                  <span className="text-[10px] font-mono text-cyan-400 shrink-0 mt-0.5 bg-navy-900 px-1.5 py-0.5 rounded border border-slate-800">
                    [{chunk.time}]
                  </span>
                  <p className="text-xs text-slate-200 leading-relaxed font-sans">{chunk.text}</p>
                </div>
              ))
            ) : (
              <div className="flex flex-col items-center justify-center h-32 text-slate-500 text-xs space-y-2">
                <Mic className="w-6 h-6 text-slate-600" />
                <span>Click "Start Live Stream" and speak to observe live speech recognition and threat scoring.</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
