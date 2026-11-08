import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  UploadCloud, Mic, Square, Play, Pause, AlertTriangle,
  ShieldCheck, Volume2, ArrowRight, CheckCircle2, RefreshCw,
  FileAudio, ShieldAlert, Sparkles, Layers, Info, ExternalLink, Activity
} from 'lucide-react';
import { api } from '../services/api';
import { AnalysisResponse, TranscriptResponse } from '../types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/common/Card';
import { SeverityBadge, StatusBadge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { AudioWaveform } from '../components/common/AudioWaveform';

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
  const [playbackProgress, setPlaybackProgress] = useState<number>(0);
  const [audioDuration, setAudioDuration] = useState<number>(0);
  const [audioCurrentTime, setAudioCurrentTime] = useState<number>(0);
  const audioPlayerRef = useRef<HTMLAudioElement | null>(null);

  // Analysis Pipeline Progress State
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [transcriptResult, setTranscriptResult] = useState<TranscriptResponse | null>(null);
  const [warningAudioUrl, setWarningAudioUrl] = useState<string | null>(null);
  const [warningText, setWarningText] = useState<string | null>(null);
  const [isDemoFallback, setIsDemoFallback] = useState<boolean>(false);

  // MediaRecorder refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<any>(null);

  const steps = [
    'Audio Ingestion & Magic-Byte Container Verification',
    'Gnani Prisma v3.0 Multilingual Speech-to-Text & LID',
    '8-Pillar Social Engineering Pattern & Coercion Scan',
    'Explainable Hybrid Risk Scoring & Rule-Priority Shield',
    'Gnani Timbre v2.5 Multilingual Safety Voice Advisory'
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setAudioUrl(URL.createObjectURL(file));
      setAnalysisResult(null);
      setTranscriptResult(null);
      setIsPlaying(false);
      setPlaybackProgress(0);
    }
  };

  // Audio player time updates
  const handleTimeUpdate = () => {
    if (audioPlayerRef.current) {
      const curr = audioPlayerRef.current.currentTime;
      const dur = audioPlayerRef.current.duration || 1;
      setAudioCurrentTime(curr);
      setAudioDuration(dur);
      setPlaybackProgress(curr / dur);
    }
  };

  const togglePlayback = () => {
    if (!audioPlayerRef.current || !audioUrl) return;
    if (isPlaying) {
      audioPlayerRef.current.pause();
      setIsPlaying(false);
    } else {
      audioPlayerRef.current.play().catch(console.error);
      setIsPlaying(true);
    }
  };

  const handleSeek = (ratio: number) => {
    if (audioPlayerRef.current && audioDuration > 0) {
      audioPlayerRef.current.currentTime = ratio * audioDuration;
      setPlaybackProgress(ratio);
    }
  };

  const startRecording = async () => {
    if (!consentGiven) {
      alert("Please confirm user consent for microphone recording first.");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
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

      const mediaRecorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const resolvedType = mediaRecorder.mimeType || mimeType;
        const audioBlob = new Blob(audioChunksRef.current, { type: resolvedType });
        const file = new File([audioBlob], `mic_recording_${Date.now()}.${extension}`, { type: resolvedType });
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
      alert("Unable to access microphone. Please ensure microphone permissions are granted in browser.");
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
      // Create a simulated test scenario file
      const sampleBlob = new Blob([new Uint8Array(44)], { type: 'audio/wav' });
      const file = new File([sampleBlob], filename, { type: 'audio/wav' });
      setSelectedFile(file);
      setLanguage(lang);
      setAudioUrl(null);
      setAnalysisResult(null);
      setTranscriptResult(null);
    } catch (e) {
      console.error(e);
    }
  };

  const getSimulatedData = (filename: string, requestedLang: string) => {
    const name = filename.toLowerCase();

    if (name.includes('cbi') || name.includes('digital_arrest') || name.includes('police')) {
      return {
        transcript: {
          transcript_id: `TR-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          language: 'hi',
          detected_languages: ['hi', 'en'],
          full_text: "Namaste. I am Inspector Sharma calling from Central Bureau of Investigation CBI headquarters New Delhi. A courier parcel containing fake passports and contraband narcotics was seized in Mumbai registered under your Aadhaar number. Supreme Court has issued an immediate non-bailable warrant. You are placed under Digital Arrest right now. Do not disconnect this video call or inform your family, otherwise a police team will arrest you within one hour.",
          provider: "Gnani Prisma v3.0 (Interactive Demo Mode)",
          is_mock: true,
          segments: [
            { start: 0.0, end: 5.2, text: "Namaste. I am Inspector Sharma calling from Central Bureau of Investigation CBI headquarters New Delhi.", language: "hi" },
            { start: 5.3, end: 12.8, text: "A courier parcel containing fake passports and contraband narcotics was seized in Mumbai registered under your Aadhaar number.", language: "en" },
            { start: 12.9, end: 22.0, text: "Supreme Court has issued an immediate non-bailable warrant. You are placed under Digital Arrest right now.", language: "en" },
            { start: 22.1, end: 32.4, text: "Do not disconnect this video call or inform your family, otherwise a police team will arrest you within one hour.", language: "en" }
          ]
        },
        analysis: {
          analysis_id: `AN-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          transcript_id: 'TR-SIM-DEMO',
          risk_score: 100.0,
          severity: 'Critical' as const,
          engine_version: 'Hybrid Intelligence v1.0 (Interactive Demo)',
          categories: ['Authority Impersonation', 'Urgency & Coercive Threats', 'Psychological Isolation', 'Digital Arrest Patterns'],
          recommendations: [
            'CRITICAL THREAT: Disconnect the call immediately. Law enforcement and courts never issue Digital Arrests over video calls.',
            'Never transfer money to any purported government verification or security escrow account.',
            'Report this cyber extortion attempt immediately to the National Cybercrime Helpline by dialing 1930 or visiting cybercrime.gov.in.'
          ],
          threats: [
            {
              rule_id: 'RULE-AUTH-01',
              category: 'Authority Impersonation',
              matched_text: 'Inspector Sharma from Central Bureau of Investigation CBI headquarters New Delhi',
              contribution: 45.0,
              explanation: 'Caller impersonates a federal law enforcement officer to establish false legal authority.'
            },
            {
              rule_id: 'RULE-URG-01',
              category: 'Urgency & Coercive Threats',
              matched_text: 'police team will arrest you within one hour',
              contribution: 35.0,
              explanation: 'Imposes an artificial panic deadline to prevent the victim from seeking outside counsel.'
            },
            {
              rule_id: 'RULE-DARR-01',
              category: 'Digital Arrest Patterns',
              matched_text: 'placed under Digital Arrest right now. Do not disconnect this video call',
              contribution: 40.0,
              explanation: 'Classic Digital Arrest coercion pattern forcing continuous video compliance.'
            },
            {
              rule_id: 'RULE-ISOL-01',
              category: 'Psychological Isolation',
              matched_text: 'Do not disconnect this video call or inform your family',
              contribution: 30.0,
              explanation: 'Deliberate tactic to cut the victim off from family and trusted advisors.'
            }
          ]
        },
        warning: {
          warning_text: "चेतावनी: यह एक डिजिटल अरेस्ट धोखाधड़ी कॉल है। सीबीआई या पुलिस कभी भी वीडियो कॉल पर गिरफ्तारी नहीं करती। तुरंत कॉल काटें और 1930 पर रिपोर्ट करें।"
        }
      };
    } else if (name.includes('kyc') || name.includes('otp') || name.includes('sbi') || name.includes('bank')) {
      return {
        transcript: {
          transcript_id: `TR-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          language: 'en',
          detected_languages: ['en'],
          full_text: "Good morning sir, this is Rajesh calling from State Bank of India KYC verification desk. Your net banking access and debit card are suspended due to pending biometric KYC update. To unfreeze your account immediately, share the six digit OTP received on your mobile and confirm your UPI PIN right now.",
          provider: "Gnani Prisma v3.0 (Interactive Demo Mode)",
          is_mock: true,
          segments: [
            { start: 0.0, end: 5.5, text: "Good morning sir, this is Rajesh calling from State Bank of India KYC verification desk.", language: "en" },
            { start: 5.6, end: 12.0, text: "Your net banking access and debit card are suspended due to pending biometric KYC update.", language: "en" },
            { start: 12.1, end: 21.5, text: "To unfreeze your account immediately, share the six digit OTP received on your mobile and confirm your UPI PIN right now.", language: "en" }
          ]
        },
        analysis: {
          analysis_id: `AN-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          transcript_id: 'TR-SIM-DEMO',
          risk_score: 96.5,
          severity: 'Critical' as const,
          engine_version: 'Hybrid Intelligence v1.0 (Interactive Demo)',
          categories: ['Credential Theft', 'Authority Impersonation', 'Urgency & Coercive Threats'],
          recommendations: [
            'NEVER share OTPs, UPI PINs, or card passwords. Legitimate bank staff will never request these over the phone.',
            'Immediately contact your bank via the official toll-free number printed on the back of your card to freeze credentials if shared.'
          ],
          threats: [
            {
              rule_id: 'RULE-CRED-01',
              category: 'Credential Theft',
              matched_text: 'share the six digit OTP received on your mobile and confirm your UPI PIN',
              contribution: 50.0,
              explanation: 'Direct solicitation of banking authentication credentials (OTP and UPI PIN).'
            },
            {
              rule_id: 'RULE-AUTH-02',
              category: 'Authority Impersonation',
              matched_text: 'State Bank of India KYC verification desk',
              contribution: 30.0,
              explanation: 'Impersonation of banking support personnel.'
            }
          ]
        },
        warning: {
          warning_text: "ALERT: This call is demanding confidential banking credentials. Bank staff never ask for OTP or UPI PIN. Do not share codes."
        }
      };
    } else if (name.includes('telugu') || name.includes('te')) {
      return {
        transcript: {
          transcript_id: `TR-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          language: 'te',
          detected_languages: ['te'],
          full_text: "నమస్కారం, మీ బ్యాంకు అకౌంట్ మరియు ఏటీఎం కార్డు వెంటనే బ్లాక్ అవుతుంది. వెంటనే మీ మొబైల్ కి వచ్చిన ఓటీపీ మరియు ఏటీఎం పిన్ నంబర్ చెప్పండి. లేదంటే మీ పై పోలీస్ స్టేషన్ లో కేసు ఫైల్ చేస్తాం, అరెస్ట్ చేస్తారు.",
          provider: "Gnani Prisma v3.0 (Interactive Demo Mode)",
          is_mock: true,
          segments: [
            { start: 0.0, end: 6.0, text: "నమస్కారం, మీ బ్యాంకు అకౌంట్ మరియు ఏటీఎం కార్డు వెంటనే బ్లాక్ అవుతుంది.", language: "te" },
            { start: 6.1, end: 12.0, text: "వెంటనే మీ మొబైల్ కి వచ్చిన ఓటీపీ మరియు ఏటీఎం పిన్ నంబర్ చెప్పండి.", language: "te" },
            { start: 12.1, end: 18.0, text: "లేదంటే మీ పై పోలీస్ స్టేషన్ లో కేసు ఫైల్ చేస్తాం, అరెస్ట్ చేస్తారు.", language: "te" }
          ]
        },
        analysis: {
          analysis_id: `AN-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          transcript_id: 'TR-SIM-DEMO',
          risk_score: 95.0,
          severity: 'Critical' as const,
          engine_version: 'Hybrid Intelligence v1.0 (Interactive Demo)',
          categories: ['Credential Theft', 'Urgency & Coercive Threats'],
          recommendations: [
            'హెచ్చరిక: బ్యాంకు అధికారులు ఎప్పుడూ ఫోన్ ద్వారా ఓటీపీ లేదా ఏటీఎం పిన్ అడగరు. వెంటనే కాల్ కట్ చేయండి.',
            'సైబర్ హెల్ప్‌లైన్ 1930 కి ఫిర్యాదు చేయండి.'
          ],
          threats: [
            {
              rule_id: 'RULE-CRED-TE',
              category: 'Credential Theft',
              matched_text: 'ఓటీపీ మరియు ఏటీఎం పిన్ నంబర్ చెప్పండి',
              contribution: 50.0,
              explanation: 'Direct demand for OTP and ATM PIN credentials in Telugu.'
            }
          ]
        },
        warning: {
          warning_text: "హెచ్చరిక: ఇది బ్యాంకు మోసపూరిత కాల్. మీ ఓటీపీ లేదా ఏటీఎం పిన్ ఎవరికీ చెప్పకండి."
        }
      };
    } else if (name.includes('safe') || name.includes('legit') || name.includes('support')) {
      return {
        transcript: {
          transcript_id: `TR-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          language: 'en',
          detected_languages: ['en'],
          full_text: "Hello, thank you for reaching out to customer care regarding your fiber broadband speed issue. Our technician has resolved the fiber line attenuation at your local node, and ticket number 4819 is now closed. Please let us know if your internet connection is working smoothly. Have a pleasant day.",
          provider: "Gnani Prisma v3.0 (Interactive Demo Mode)",
          is_mock: true,
          segments: [
            { start: 0.0, end: 8.0, text: "Hello, thank you for reaching out to customer care regarding your fiber broadband speed issue.", language: "en" },
            { start: 8.1, end: 16.0, text: "Our technician has resolved the fiber line attenuation at your local node, and ticket number 4819 is now closed.", language: "en" },
            { start: 16.1, end: 23.0, text: "Please let us know if your internet connection is working smoothly. Have a pleasant day.", language: "en" }
          ]
        },
        analysis: {
          analysis_id: `AN-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          transcript_id: 'TR-SIM-DEMO',
          risk_score: 0.6,
          severity: 'Low' as const,
          engine_version: 'Hybrid Intelligence v1.0 (Interactive Demo)',
          categories: [],
          recommendations: ['Routine business dialogue. No coercion, credential demands, or extortion detected.'],
          threats: []
        },
        warning: {
          warning_text: "Call verified safe. No social engineering threat patterns detected."
        }
      };
    } else {
      return {
        transcript: {
          transcript_id: `TR-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          language: requestedLang === 'auto' ? 'en' : requestedLang,
          detected_languages: [requestedLang === 'auto' ? 'en' : requestedLang],
          full_text: `Audio stream ingested successfully (${filename}). Evaluated against KAVACH AI 8-pillar threat detection rules.`,
          provider: "Gnani Prisma v3.0 (Interactive Demo Mode)",
          is_mock: true,
          segments: [
            { start: 0.0, end: 10.0, text: `Audio analysis stream ingested. File: ${filename}`, language: requestedLang === 'auto' ? 'en' : requestedLang }
          ]
        },
        analysis: {
          analysis_id: `AN-SIM-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
          transcript_id: 'TR-SIM-DEMO',
          risk_score: 12.0,
          severity: 'Low' as const,
          engine_version: 'Hybrid Intelligence v1.0 (Interactive Demo)',
          categories: [],
          recommendations: ['Audio processed under simulated demo conditions.'],
          threats: []
        },
        warning: {
          warning_text: "Audio scanned. Connect live backend for full neural transformer inference."
        }
      };
    }
  };

  const runAnalysisPipeline = async () => {
    if (!selectedFile) return;

    setAnalyzing(true);
    setIsDemoFallback(false);
    setCurrentStep(1);

    try {
      // Step 1: Upload
      const uploadRes = await api.uploadAudio(selectedFile);
      const audioId = uploadRes.audio_id;
      setCurrentStep(2);

      // Step 2: Transcribe via Gnani Prisma v3.0
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
      console.warn("Analysis pipeline live API request failed:", err);
      // If backend is offline or Vercel VITE_API_URL is unconfigured, gracefully fallback to interactive simulation
      const isNetworkIssue = !err.response || err.message === 'Network Error' || err.code === 'ERR_NETWORK';

      if (isNetworkIssue) {
        setIsDemoFallback(true);

        // Step 1: Ingestion
        await new Promise((r) => setTimeout(r, 350));
        setCurrentStep(2);

        // Step 2: Speech-to-Text
        await new Promise((r) => setTimeout(r, 450));
        const sim = getSimulatedData(selectedFile.name, language);
        setTranscriptResult(sim.transcript);
        setCurrentStep(3);

        // Step 3 & 4: Threat Pattern & Scoring
        await new Promise((r) => setTimeout(r, 500));
        setAnalysisResult(sim.analysis);
        setCurrentStep(5);

        // Step 5: Voice Warning
        await new Promise((r) => setTimeout(r, 350));
        setWarningText(sim.warning.warning_text);
        setCurrentStep(6);
      } else {
        alert(`Analysis failed: ${err.response?.data?.detail || err.message}`);
      }
    } finally {
      setAnalyzing(false);
    }
  };


  const formatSeconds = (sec: number) => {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Hidden audio element for playback */}
      {audioUrl && (
        <audio
          ref={audioPlayerRef}
          src={audioUrl}
          onTimeUpdate={handleTimeUpdate}
          onEnded={() => setIsPlaying(false)}
          className="hidden"
        />
      )}

      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 font-mono text-xs mb-1">
            <Activity className="w-4 h-4" />
            <span>KAVACH AI FORENSIC ANALYSIS WORKSTATION</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100 flex items-center space-x-3">
            <span>Audio Ingestion & Multilingual Threat Triage</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Accepts audio recordings and live microphone streams. Transcribes Indian languages via Gnani Prisma v3.0 and scans for social-engineering coercion.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <Link to="/threats">
            <Button variant="outline" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
              Explore 8 Threat Pillars
            </Button>
          </Link>
        </div>
      </div>

      {/* Preset Test Scenarios */}
      <Card className="bg-[#0a0f1c]/80 border-slate-800/80">
        <CardHeader className="py-3 px-4 flex flex-row items-center justify-between border-b border-slate-800/50">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-semibold text-slate-200">Demonstration Archetypes</span>
          </div>
          <span className="text-[10px] font-mono text-slate-400">Click to quickly evaluate detection logic</span>
        </CardHeader>
        <CardContent className="p-3">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
            <button
              onClick={() => selectScenario('cbi_digital_arrest_sample.wav', 'hi')}
              className="p-3 bg-[#0d1424] hover:bg-[#131c31] text-left rounded-lg border border-slate-800 hover:border-red-500/40 text-xs transition group"
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-red-400 group-hover:text-red-300">🚨 CBI Digital Arrest</span>
                <span className="text-[9px] font-mono text-slate-500">HI</span>
              </div>
              <p className="text-[10px] text-slate-400 mt-1 line-clamp-1">Hindi coercion · Fake Supreme Court warrant</p>
            </button>

            <button
              onClick={() => selectScenario('sbi_bank_kyc_otp_sample.wav', 'en')}
              className="p-3 bg-[#0d1424] hover:bg-[#131c31] text-left rounded-lg border border-slate-800 hover:border-amber-500/40 text-xs transition group"
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-amber-400 group-hover:text-amber-300">💳 Bank KYC & OTP Theft</span>
                <span className="text-[9px] font-mono text-slate-500">EN</span>
              </div>
              <p className="text-[10px] text-slate-400 mt-1 line-clamp-1">English banking fraud · 6-digit code demand</p>
            </button>

            <button
              onClick={() => selectScenario('telugu_bank_block_pin.wav', 'te')}
              className="p-3 bg-[#0d1424] hover:bg-[#131c31] text-left rounded-lg border border-slate-800 hover:border-purple-500/40 text-xs transition group"
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-purple-400 group-hover:text-purple-300">⚠️ Telugu Account Freeze</span>
                <span className="text-[9px] font-mono text-slate-500">TE</span>
              </div>
              <p className="text-[10px] text-slate-400 mt-1 line-clamp-1">తెలుగు భాషలో ATM PIN కోరిన బెదిరింపు</p>
            </button>

            <button
              onClick={() => selectScenario('safe_customer_service_legit.wav', 'en')}
              className="p-3 bg-[#0d1424] hover:bg-[#131c31] text-left rounded-lg border border-slate-800 hover:border-emerald-500/40 text-xs transition group"
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-emerald-400 group-hover:text-emerald-300">✅ Legitimate Support Call</span>
                <span className="text-[9px] font-mono text-slate-500">EN</span>
              </div>
              <p className="text-[10px] text-slate-400 mt-1 line-clamp-1">Routine broadband resolution · Safe context</p>
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Main Forensic Ingestion Vault (Dual-Input Grid) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Method 1: File Drop Zone (6 cols) */}
        <div className="lg:col-span-6">
          <Card elevated className="h-full flex flex-col justify-between">
            <CardHeader>
              <CardTitle className="text-sm">
                <span className="flex items-center space-x-2">
                  <UploadCloud className="w-4 h-4 text-cyan-400" />
                  <span>Acoustic File Ingestion</span>
                </span>
                <span className="text-[10px] font-mono text-slate-400 uppercase">Max 25 MB</span>
              </CardTitle>
              <CardDescription>
                Validates WAV, MP3, M4A, FLAC, and WebM containers with magic-byte verification.
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              <div
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-slate-700/80 hover:border-cyan-500/80 rounded-xl p-8 text-center cursor-pointer transition-all bg-[#090d18]/60 hover:bg-[#0c1424] flex flex-col items-center justify-center group"
                role="button"
                tabIndex={0}
                aria-label="Upload audio file"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') fileInputRef.current?.click();
                }}
              >
                <div className="w-12 h-12 rounded-xl bg-slate-800/80 group-hover:bg-cyan-950/40 border border-slate-700 group-hover:border-cyan-700 flex items-center justify-center text-slate-400 group-hover:text-cyan-400 mb-3 transition-colors">
                  <FileAudio className="w-6 h-6 stroke-[1.75]" />
                </div>
                <p className="text-xs font-semibold text-slate-200">
                  {selectedFile ? selectedFile.name : 'Click to select audio file or drag & drop'}
                </p>
                <p className="text-[10px] font-mono text-slate-400 mt-1">
                  16 kHz / 8 kHz Mono or Stereo · RIFF/WAVE compliant
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".wav,.mp3,.m4a,.flac,.ogg,.webm"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </div>

              {selectedFile && (
                <div className="p-3 rounded-lg bg-[#070b14] border border-slate-800 text-xs flex items-center justify-between font-mono">
                  <span className="text-slate-400">Payload Name:</span>
                  <span className="text-cyan-400 font-bold truncate max-w-xs">{selectedFile.name}</span>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Method 2: Live Microphone Vault (6 cols) */}
        <div className="lg:col-span-6">
          <Card elevated className="h-full flex flex-col justify-between">
            <CardHeader>
              <CardTitle className="text-sm">
                <span className="flex items-center space-x-2">
                  <Mic className="w-4 h-4 text-cyan-400" />
                  <span>Browser Microphone Capture</span>
                </span>
                <span className="text-[10px] font-mono text-amber-400 uppercase">Consent Required</span>
              </CardTitle>
              <CardDescription>
                Near-real-time speech capture for demonstration and analyst verification.
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              {/* Mandatory Consent Checkbox */}
              <label className="flex items-start space-x-2.5 p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={consentGiven}
                  onChange={(e) => setConsentGiven(e.target.checked)}
                  className="mt-0.5 rounded border-slate-700 text-cyan-500 focus:ring-0 bg-[#070b14]"
                />
                <span className="text-[11px] leading-relaxed">
                  I explicitly consent to microphone capture and local audio processing for scam and vishing detection evaluation.
                </span>
              </label>

              {/* Recording Control & Waveform Display */}
              <div className="p-4 rounded-xl bg-[#090d18] border border-slate-800 text-center space-y-3">
                <AudioWaveform isRecording={isRecording} height={44} barCount={40} />

                {isRecording ? (
                  <div className="space-y-2">
                    <div className="flex items-center justify-center space-x-2 text-red-400 font-mono text-xs font-bold animate-pulse">
                      <span className="w-2.5 h-2.5 rounded-full bg-red-500" />
                      <span>STREAM RECORDING: {formatSeconds(recordDuration)}</span>
                    </div>
                    <Button variant="destructive" size="sm" onClick={stopRecording} leftIcon={<Square className="w-3.5 h-3.5" />}>
                      Stop Recording
                    </Button>
                  </div>
                ) : (
                  <Button
                    variant={consentGiven ? 'primary' : 'secondary'}
                    size="sm"
                    onClick={startRecording}
                    disabled={!consentGiven}
                    leftIcon={<Mic className="w-4 h-4" />}
                  >
                    Start Microphone Ingestion
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Audio Playback Workstation Bar */}
      {audioUrl && (
        <Card className="bg-[#090e1a] border-cyan-800/40 p-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center space-x-3 w-full sm:w-auto">
              <Button
                variant="primary"
                size="sm"
                onClick={togglePlayback}
                leftIcon={isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              >
                {isPlaying ? 'Pause' : 'Play Audio'}
              </Button>
              <div className="font-mono text-xs text-slate-300">
                <span>{formatSeconds(audioCurrentTime)}</span>
                <span className="text-slate-500"> / </span>
                <span>{formatSeconds(audioDuration)}</span>
              </div>
            </div>

            <div className="w-full sm:flex-1 max-w-lg">
              <AudioWaveform
                progress={playbackProgress}
                isPlaying={isPlaying}
                height={36}
                barCount={52}
                onSeek={handleSeek}
              />
            </div>
          </div>
        </Card>
      )}

      {/* Language Selector & Scan Action */}
      <div className="bg-[#0d1424] p-4 rounded-xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <label className="text-xs font-mono text-slate-400 whitespace-nowrap">Transcription Language:</label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-[#070b14] border border-slate-700/80 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-sans"
          >
            <option value="auto">Auto-Detect (Prisma LID)</option>
            <option value="te">Telugu (తెలుగు / Code-mixed)</option>
            <option value="hi">Hindi (हिंदी / Hinglish)</option>
            <option value="en">English (Indian Telephony Accent)</option>
          </select>
        </div>

        <Button
          variant="primary"
          size="md"
          onClick={runAnalysisPipeline}
          disabled={!selectedFile || analyzing}
          isLoading={analyzing}
          rightIcon={!analyzing ? <ArrowRight className="w-4 h-4" /> : undefined}
          className="w-full sm:w-auto font-mono uppercase tracking-wider text-xs"
        >
          {analyzing ? 'RUNNING HYBRID PIPELINE...' : 'EXECUTE KAVACH THREAT SCAN'}
        </Button>
      </div>

      {/* Pipeline Progress Stages */}
      {analyzing && (
        <Card elevated className="border-cyan-500/40 p-5 space-y-3 bg-[#090e1a]">
          <div className="flex items-center justify-between text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider">
            <span className="flex items-center space-x-2">
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Pipeline Stage Execution Active</span>
            </span>
            <span>Stage {currentStep} of 5</span>
          </div>

          <div className="space-y-2 pt-1">
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
                  <span
                    className={
                      isCurrent
                        ? 'text-cyan-300 font-semibold'
                        : isDone
                        ? 'text-slate-300'
                        : 'text-slate-500'
                    }
                  >
                    {step}
                  </span>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* Forensic Threat Analysis Results */}
      {analysisResult && (
        <Card elevated className="border-slate-700/80 p-6 space-y-6">
          {/* Offline / Demo Fallback Notice */}
          {isDemoFallback && (
            <div className="p-3.5 bg-amber-950/40 border border-amber-500/40 rounded-xl text-xs text-amber-300 flex items-start space-x-3">
              <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
              <div className="space-y-1">
                <div className="font-semibold text-amber-200">
                  Interactive Demonstration Mode Active
                </div>
                <div className="text-[11px] text-amber-300/90 leading-relaxed">
                  Live backend is currently unreachable at <code className="bg-black/40 px-1 py-0.5 rounded font-mono text-[10px]">VITE_API_URL</code>. 
                  Demonstration archetype results, 8-pillar threat scoring, and warning advisories are simulated client-side. To enable live neural transformer inference, launch the backend and set <code className="bg-black/40 px-1 py-0.5 rounded font-mono text-[10px]">VITE_API_URL</code> in Vercel.
                </div>
              </div>
            </div>
          )}

          {/* Header Verdict Banner */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-800 gap-4">
            <div>
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                THREAT ASSESSMENT VERDICT
              </span>
              <div className="flex items-center space-x-3 mt-1.5">
                <SeverityBadge severity={analysisResult.severity} size="md" />
                <span className="text-2xl font-bold font-mono text-slate-100">
                  Risk Score: {analysisResult.risk_score} / 100
                </span>
              </div>
            </div>

            {analysisResult.incident_id && (
              <Button
                variant="destructive"
                size="sm"
                onClick={() => navigate(`/incidents/${analysisResult.incident_id}`)}
                rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
              >
                Open Investigation Dossier
              </Button>
            )}
          </div>

          {/* Side-by-Side: Speech Transcript + Matched Tactics */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Transcript (6 cols) */}
            <div className="lg:col-span-6 space-y-4">
              <h3 className="text-xs font-mono font-semibold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                <span>PRISMA v3.0 TRANSCRIPT ({transcriptResult?.language?.toUpperCase() || 'MULTI'})</span>
                <span className="text-cyan-400 font-normal">Acoustic Confidence Verified</span>
              </h3>

              <div className="p-4 rounded-xl bg-[#070b14] border border-slate-800 text-xs text-slate-200 leading-relaxed font-sans max-h-80 overflow-y-auto">
                <p className="italic text-slate-300">"{transcriptResult?.full_text || 'No text extracted.'}"</p>
              </div>

              {/* Synthesized Voice Warning (Gnani Timbre) */}
              {warningText && (
                <div className="p-4 rounded-xl bg-gradient-to-r from-red-950/30 to-[#0d1424] border border-red-900/50 space-y-2.5">
                  <div className="flex items-center justify-between text-xs font-bold text-red-400">
                    <span className="flex items-center space-x-1.5">
                      <Volume2 className="w-4 h-4" />
                      <span>Gnani Timbre v2.5 Voice Advisory</span>
                    </span>
                    <span className="text-[10px] font-mono text-slate-400 uppercase">
                      Voice: {transcriptResult?.language === 'te' ? 'Chitra' : 'Nalini'}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 font-medium">{warningText}</p>
                  {warningAudioUrl && (
                    <audio src={warningAudioUrl} controls autoPlay className="h-8 w-full pt-1" />
                  )}
                </div>
              )}
            </div>

            {/* Matched Tactics & Rule Breakdown (6 cols) */}
            <div className="lg:col-span-6 space-y-3">
              <h3 className="text-xs font-mono font-semibold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                <span>TRIGGERED SOCIAL ENGINEERING TACTICS ({analysisResult.threats.length})</span>
                <span className="text-red-400 font-normal">Rule-Priority Shield</span>
              </h3>

              {analysisResult.threats && analysisResult.threats.length > 0 ? (
                <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                  {analysisResult.threats.map((th, i) => (
                    <div
                      key={i}
                      className="p-3.5 rounded-xl bg-[#070b14] border border-slate-800 hover:border-slate-700 text-xs space-y-1.5"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <span className="font-semibold text-slate-100">{th.category}</span>
                          <span className="font-mono text-[10px] text-slate-500">[{th.rule_id}]</span>
                        </div>
                        <span className="font-mono font-bold text-red-400 bg-red-950/40 px-2 py-0.5 rounded border border-red-900/40 text-[11px]">
                          +{th.contribution}
                        </span>
                      </div>

                      <p className="text-[11px] text-slate-400 leading-relaxed">{th.explanation}</p>

                      <div className="text-[11px] font-mono text-cyan-300 bg-cyan-950/30 px-2 py-1 rounded border border-cyan-800/30 break-all">
                        Evidence: "{th.matched_text}"
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center text-slate-500 text-xs bg-[#070b14] rounded-xl border border-slate-800">
                  <ShieldCheck className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
                  <p className="font-semibold text-slate-300">Clean Dialogue Verified</p>
                  <p className="text-[11px] text-slate-500 mt-1">No actionable extortion or credential extraction signatures detected.</p>
                </div>
              )}
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
