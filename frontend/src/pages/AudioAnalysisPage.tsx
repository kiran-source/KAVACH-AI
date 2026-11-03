import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  UploadCloud, Mic, Square, Play, Pause, AlertTriangle,
  ShieldCheck, Volume2, ArrowRight, CheckCircle2, RefreshCw, FileAudio
} from 'lucide-react';
import { api } from '../services/api';
import { AnalysisResponse, TranscriptResponse } from '../types';

export const AudioAnalysisPage: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [language, setLanguage] = useState<string>('auto');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [recordDuration, setRecordDuration] = useState<number>(0);
  const [consentGiven, setConsentGiven] = useState<boolean>(false);

  // Audio Player state
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const audioPlayerRef = useRef<HTMLAudioElement | null>(null);

  // Analysis Pipeline Progress State
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [transcriptResult, setTranscriptResult] = useState<TranscriptResponse | null>(null);
  const [warningAudioUrl, setWarningAudioUrl] = useState<string | null>(null);
  const [warningText, setWarningText] = useState<string | null>(null);

  // MediaRecorder refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<any>(null);

  const steps = [
    'Audio Ingestion & Metadata Validation',
    'Gnani Prisma v2.5 Multilingual Transcription',
    'Multilingual Social Engineering Pattern Scan',
    'Explainable Risk Scoring & Threat Triage',
    'Gnani Timbre Multilingual Safety Voice Synthesis'
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setAudioUrl(URL.createObjectURL(file));
      setAnalysisResult(null);
    }
  };

  const startRecording = async () => {
    if (!consentGiven) {
      alert("Please confirm user consent for microphone recording first.");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const file = new File([audioBlob], `mic_recording_${Date.now()}.wav`, { type: 'audio/wav' });
        setSelectedFile(file);
        setAudioUrl(URL.createObjectURL(audioBlob));
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordDuration(0);
      timerRef.current = setInterval(() => {
        setRecordDuration((prev) => prev + 1);
      }, 1000);
    } catch (err) {
      console.error("Microphone access error:", err);
      alert("Unable to access microphone. Please ensure microphone permissions are granted.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach((track) => track.stop());
      setIsRecording(false);
      clearInterval(timerRef.current);
    }
  };

  const selectScenario = async (filename: string, lang: string) => {
    try {
      // Create a dummy WAV file for test scenario
      const sampleBlob = new Blob([new Uint8Array(44)], { type: 'audio/wav' });
      const file = new File([sampleBlob], filename, { type: 'audio/wav' });
      setSelectedFile(file);
      setLanguage(lang);
      setAudioUrl(null);
      setAnalysisResult(null);
    } catch (e) {
      console.error(e);
    }
  };

  const runAnalysisPipeline = async () => {
    if (!selectedFile) return;

    setAnalyzing(true);
    setCurrentStep(1);

    try {
      // Step 1: Upload
      const uploadRes = await api.uploadAudio(selectedFile);
      const audioId = uploadRes.audio_id;
      setCurrentStep(2);

      // Step 2: Transcribe via Gnani Prisma v2.5
      const trRes = await api.transcribeAudio(audioId, language);
      setTranscriptResult(trRes);
      setCurrentStep(3);

      // Step 3 & 4: Detection & Scoring
      const anRes = await api.analyzeTranscript(trRes.transcript_id);
      setAnalysisResult(anRes);
      setCurrentStep(5);

      // Step 5: Generate safety voice warning via Gnani Timbre
      const preferredLang = trRes.language || 'en';
      const warnRes = await api.generateWarning(preferredLang, anRes.categories);
      setWarningAudioUrl(warnRes.audio_url);
      setWarningText(warnRes.warning_text);

      setCurrentStep(6);
    } catch (err: any) {
      console.error("Analysis pipeline error:", err);
      alert(`Analysis failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-xl font-bold text-white flex items-center space-x-2">
          <FileAudio className="w-5 h-5 text-cyan-400" />
          <span>Audio Ingestion & Threat Analysis Engine</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Upload calls or record voice samples to detect social-engineering tactics across Telugu, Hindi, and English.
        </p>
      </div>

      {/* Synthetic Scenario Quick Select */}
      <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800">
        <div className="text-xs font-semibold text-slate-300 mb-2 flex items-center justify-between">
          <span>Preset Test Scenarios (Demonstration & Evaluation)</span>
          <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/40">
            Click to Auto-load
          </span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
          <button
            onClick={() => selectScenario('cbi_digital_arrest_sample.wav', 'hi')}
            className="p-2.5 bg-slate-800/60 hover:bg-slate-700/60 text-left rounded-lg border border-slate-700/80 text-xs transition"
          >
            <div className="font-semibold text-red-400">🚨 CBI Digital Arrest</div>
            <div className="text-[10px] text-slate-400 mt-0.5">Hindi / Code-mixed threat</div>
          </button>
          <button
            onClick={() => selectScenario('sbi_bank_kyc_otp_sample.wav', 'en')}
            className="p-2.5 bg-slate-800/60 hover:bg-slate-700/60 text-left rounded-lg border border-slate-700/80 text-xs transition"
          >
            <div className="font-semibold text-amber-400">💳 Bank KYC & OTP Theft</div>
            <div className="text-[10px] text-slate-400 mt-0.5">English banking fraud</div>
          </button>
          <button
            onClick={() => selectScenario('telugu_bank_block_pin.wav', 'te')}
            className="p-2.5 bg-slate-800/60 hover:bg-slate-700/60 text-left rounded-lg border border-slate-700/80 text-xs transition"
          >
            <div className="font-semibold text-red-400">⚠️ Telugu Account Freeze</div>
            <div className="text-[10px] text-slate-400 mt-0.5">తెలుగు ATM PIN డిమాండ్</div>
          </button>
          <button
            onClick={() => selectScenario('safe_customer_service_legit.wav', 'en')}
            className="p-2.5 bg-slate-800/60 hover:bg-slate-700/60 text-left rounded-lg border border-slate-700/80 text-xs transition"
          >
            <div className="font-semibold text-emerald-400">✅ Legitimate Support Call</div>
            <div className="text-[10px] text-slate-400 mt-0.5">Benign broadband resolution</div>
          </button>
        </div>
      </div>

      {/* Main Ingestion Card */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Method 1: File Upload */}
        <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-semibold text-white mb-2 flex items-center space-x-2">
              <UploadCloud className="w-4 h-4 text-cyan-400" />
              <span>Audio File Upload</span>
            </h2>
            <p className="text-xs text-slate-400 mb-4">
              Supported formats: WAV, MP3, M4A, FLAC, OGG (Max 25MB)
            </p>

            <div
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-slate-700 hover:border-cyan-500 rounded-xl p-6 text-center cursor-pointer transition bg-slate-900/40"
            >
              <UploadCloud className="w-8 h-8 text-slate-500 mx-auto mb-2" />
              <p className="text-xs font-medium text-slate-300">
                {selectedFile ? selectedFile.name : 'Click to select audio file or drag & drop'}
              </p>
              <p className="text-[10px] text-slate-500 mt-1">Safe temporary quarantine storage</p>
              <input
                ref={fileInputRef}
                type="file"
                accept=".wav,.mp3,.m4a,.flac,.ogg,.webm"
                onChange={handleFileChange}
                className="hidden"
              />
            </div>
          </div>

          <div className="mt-4 flex items-center justify-between text-xs text-slate-400">
            <span>Selected File:</span>
            <span className="font-mono text-cyan-400 font-semibold">{selectedFile?.name || 'None'}</span>
          </div>
        </div>

        {/* Method 2: Microphone Recording */}
        <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div>
            <h2 className="text-sm font-semibold text-white mb-2 flex items-center space-x-2">
              <Mic className="w-4 h-4 text-cyan-400" />
              <span>Direct Microphone Recording</span>
            </h2>
            <p className="text-xs text-slate-400 mb-3">
              Record voice interactions locally with explicit consent.
            </p>

            {/* Consent Checkbox */}
            <label className="flex items-start space-x-2 p-2.5 rounded bg-slate-900/60 border border-slate-800 text-[11px] text-slate-300 cursor-pointer mb-4">
              <input
                type="checkbox"
                checked={consentGiven}
                onChange={(e) => setConsentGiven(e.target.checked)}
                className="mt-0.5 rounded border-slate-700 text-cyan-500 focus:ring-0"
              />
              <span>I confirm that audio is recorded with user awareness for cyber threat evaluation.</span>
            </label>

            <div className="text-center py-3">
              {isRecording ? (
                <div className="space-y-3">
                  <div className="flex items-center justify-center space-x-2 text-red-400 font-mono text-sm animate-pulse">
                    <span className="w-3 h-3 rounded-full bg-red-500"></span>
                    <span>RECORDING ACTIVE: {recordDuration}s</span>
                  </div>
                  <button
                    onClick={stopRecording}
                    className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white font-semibold text-xs rounded-lg transition inline-flex items-center space-x-2 shadow-lg shadow-red-500/20"
                  >
                    <Square className="w-3.5 h-3.5" />
                    <span>Stop Recording</span>
                  </button>
                </div>
              ) : (
                <button
                  onClick={startRecording}
                  disabled={!consentGiven}
                  className={`px-4 py-2 rounded-lg font-semibold text-xs inline-flex items-center space-x-2 transition ${
                    consentGiven
                      ? 'bg-slate-800 hover:bg-slate-700 text-cyan-400 border border-cyan-800/40 shadow-sm'
                      : 'bg-slate-800/40 text-slate-600 border border-slate-800 cursor-not-allowed'
                  }`}
                >
                  <Mic className="w-4 h-4" />
                  <span>Start Microphone Record</span>
                </button>
              )}
            </div>
          </div>

          <div className="mt-4 flex items-center justify-between text-xs text-slate-400">
            <span>Audio Preview:</span>
            {audioUrl ? (
              <audio src={audioUrl} controls className="h-7 w-48" />
            ) : (
              <span className="text-[11px] text-slate-500 italic">No audio loaded</span>
            )}
          </div>
        </div>
      </div>

      {/* Language Selector & Scan Action */}
      <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <label className="text-xs font-mono text-slate-400 whitespace-nowrap">Transcription Language:</label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
          >
            <option value="auto">Auto-Detect (Prisma LID)</option>
            <option value="te">Telugu (తెలుగు / Code-mixed)</option>
            <option value="hi">Hindi (हिंदी / Code-mixed)</option>
            <option value="en">English (Indian Accent)</option>
          </select>
        </div>

        <button
          onClick={runAnalysisPipeline}
          disabled={!selectedFile || analyzing}
          className={`w-full sm:w-auto px-6 py-2.5 rounded-lg text-xs font-bold font-mono tracking-wider transition flex items-center justify-center space-x-2 shadow-lg ${
            selectedFile && !analyzing
              ? 'bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-500 hover:to-teal-400 text-slate-950 shadow-cyan-500/20'
              : 'bg-slate-800 text-slate-500 border border-slate-700 cursor-not-allowed'
          }`}
        >
          {analyzing ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>ANALYSING THREAT ENGINE...</span>
            </>
          ) : (
            <>
              <span>EXECUTE KAVACH SCAN</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>

      {/* Progress Steps Card */}
      {analyzing && (
        <div className="bg-[#0c1220] p-5 rounded-xl border border-cyan-800/40 space-y-3">
          <div className="text-xs font-mono text-cyan-400 font-semibold uppercase tracking-wider">
            Execution Pipeline in Progress
          </div>
          <div className="space-y-2">
            {steps.map((step, idx) => {
              const stepNum = idx + 1;
              const isDone = currentStep > stepNum;
              const isCurrent = currentStep === stepNum;
              return (
                <div key={idx} className="flex items-center space-x-3 text-xs">
                  <div
                    className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold font-mono ${
                      isDone
                        ? 'bg-emerald-500 text-slate-950'
                        : isCurrent
                        ? 'bg-cyan-500 text-slate-950 animate-pulse'
                        : 'bg-slate-800 text-slate-500'
                    }`}
                  >
                    {isDone ? '✓' : stepNum}
                  </div>
                  <span className={isCurrent ? 'text-cyan-300 font-semibold' : isDone ? 'text-slate-300' : 'text-slate-500'}>
                    {step}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Analysis Results Display */}
      {analysisResult && (
        <div className="bg-[#0c1220] rounded-xl border border-slate-800 p-6 space-y-6">
          {/* Header Result */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-4">
            <div>
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">THREAT ASSESSMENT VERDICT</span>
              <div className="flex items-center space-x-3 mt-1">
                <span
                  className={`px-3 py-1 rounded text-sm font-bold font-mono border ${
                    analysisResult.severity === 'Critical' || analysisResult.severity === 'High'
                      ? 'bg-red-500/20 text-red-400 border-red-500/40'
                      : analysisResult.severity === 'Medium'
                      ? 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                      : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                  }`}
                >
                  {analysisResult.severity.toUpperCase()} RISK
                </span>
                <span className="text-xl font-bold font-mono text-white">
                  Score: {analysisResult.risk_score} / 100
                </span>
              </div>
            </div>

            {analysisResult.incident_id && (
              <button
                onClick={() => navigate(`/incidents/${analysisResult.incident_id}`)}
                className="px-4 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 border border-red-500/40 rounded-lg text-xs font-semibold flex items-center space-x-2 transition"
              >
                <span>Open Incident Investigation</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Transcript Preview */}
          {transcriptResult && (
            <div className="bg-[#090d16] p-4 rounded-lg border border-slate-800">
              <div className="flex items-center justify-between text-xs text-slate-400 font-mono mb-2">
                <span>PRISMA v2.5 TRANSCRIPT ({transcriptResult.language.toUpperCase()})</span>
                <span className="text-[10px] text-cyan-400">Confidence Verified</span>
              </div>
              <p className="text-xs text-slate-200 leading-relaxed font-sans italic">
                "{transcriptResult.full_text}"
              </p>
            </div>
          )}

          {/* Voice Warning Synthesizer (Gnani Timbre) */}
          {warningText && (
            <div className="bg-gradient-to-r from-red-950/30 to-[#0c1220] p-4 rounded-lg border border-red-900/40 space-y-2">
              <div className="flex items-center space-x-2 text-xs font-semibold text-red-400">
                <Volume2 className="w-4 h-4" />
                <span>Gnani Timbre v2.5 Voice Safety Advisory</span>
              </div>
              <p className="text-xs text-slate-300 font-medium">{warningText}</p>
              {warningAudioUrl && (
                <div className="pt-2">
                  <audio src={warningAudioUrl} controls autoPlay className="h-8 w-full max-w-md" />
                </div>
              )}
            </div>
          )}

          {/* Detected Tactics List */}
          <div>
            <h3 className="text-xs font-mono font-semibold text-slate-400 uppercase tracking-wider mb-3">
              Triggered Social Engineering Tactics ({analysisResult.threats.length})
            </h3>
            {analysisResult.threats.length > 0 ? (
              <div className="space-y-2">
                {analysisResult.threats.map((th, i) => (
                  <div key={i} className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex items-start justify-between text-xs">
                    <div>
                      <div className="font-semibold text-white flex items-center space-x-2">
                        <span>{th.category}</span>
                        <span className="font-mono text-[10px] text-slate-500">({th.rule_id})</span>
                      </div>
                      <p className="text-slate-400 mt-1 text-[11px]">{th.explanation}</p>
                      <div className="mt-2 text-[11px] text-cyan-300 font-mono bg-cyan-950/30 px-2 py-0.5 rounded inline-block border border-cyan-800/30">
                        Evidence: "{th.matched_text}"
                      </div>
                    </div>
                    <div className="font-mono font-bold text-red-400 bg-red-950/40 px-2 py-1 rounded border border-red-900/40">
                      +{th.contribution}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">No suspicious social engineering tactics identified in transcript.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
