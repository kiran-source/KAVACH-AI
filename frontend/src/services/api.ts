import axios from 'axios';
import {
  DashboardMetrics,
  SystemProviders,
  AnalysisResponse,
  TranscriptResponse,
  IncidentSummary,
  IncidentDetail,
  ReportItem,
  EvaluationMetrics,
  SystemSettings
} from '../types';

const API_BASE = '/api/v1';

export const api = {
  // Health
  getHealth: async () => {
    const res = await axios.get(`${API_BASE}/health`);
    return res.data;
  },
  getProviders: async (): Promise<SystemProviders> => {
    const res = await axios.get(`${API_BASE}/health/providers`);
    return res.data;
  },

  // Dashboard
  getDashboardMetrics: async (): Promise<DashboardMetrics> => {
    const res = await axios.get(`${API_BASE}/dashboard/metrics`);
    return res.data;
  },

  // Audio Upload & Processing
  uploadAudio: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await axios.post(`${API_BASE}/audio/upload`, formData);
    return res.data;
  },
  uploadRecording: async (blob: Blob, durationEstimate: number) => {
    const formData = new FormData();
    formData.append('audio_blob', blob, 'mic_recording.wav');
    formData.append('duration_estimate', durationEstimate.toString());
    const res = await axios.post(`${API_BASE}/audio/recording`, formData);
    return res.data;
  },
  deleteAudio: async (audioId: string) => {
    const res = await axios.delete(`${API_BASE}/audio/${audioId}`);
    return res.data;
  },

  // Transcription
  transcribeAudio: async (audioId: string, language: string = 'auto'): Promise<TranscriptResponse> => {
    const formData = new FormData();
    formData.append('language', language);
    const res = await axios.post(`${API_BASE}/transcription/${audioId}`, formData);
    return res.data;
  },
  getTranscript: async (transcriptId: string): Promise<TranscriptResponse> => {
    const res = await axios.get(`${API_BASE}/transcription/${transcriptId}`);
    return res.data;
  },

  // Threat Analysis
  analyzeTranscript: async (transcriptId: string): Promise<AnalysisResponse> => {
    const res = await axios.post(`${API_BASE}/analysis/${transcriptId}`);
    return res.data;
  },
  getAnalysis: async (analysisId: string) => {
    const res = await axios.get(`${API_BASE}/analysis/${analysisId}`);
    return res.data;
  },
  listAnalyses: async () => {
    const res = await axios.get(`${API_BASE}/analysis`);
    return res.data;
  },

  // Voice Warning
  generateWarning: async (language: string, categories: string[], customText?: string) => {
    const formData = new FormData();
    formData.append('language', language);
    formData.append('categories', categories.join(','));
    if (customText) formData.append('custom_text', customText);
    const res = await axios.post(`${API_BASE}/warnings/generate`, formData);
    return res.data;
  },

  // Incidents
  listIncidents: async (status?: string, severity?: string): Promise<IncidentSummary[]> => {
    const params: any = {};
    if (status && status !== 'All') params.status = status;
    if (severity && severity !== 'All') params.severity = severity;
    const res = await axios.get(`${API_BASE}/incidents`, { params });
    return res.data;
  },
  getIncident: async (incidentId: string): Promise<IncidentDetail> => {
    const res = await axios.get(`${API_BASE}/incidents/${incidentId}`);
    return res.data;
  },
  updateIncident: async (incidentId: string, data: { status?: string; assigned_analyst?: string; analyst_notes?: string }) => {
    const formData = new FormData();
    if (data.status) formData.append('status', data.status);
    if (data.assigned_analyst) formData.append('assigned_analyst', data.assigned_analyst);
    if (data.analyst_notes !== undefined) formData.append('analyst_notes', data.analyst_notes);
    const res = await axios.patch(`${API_BASE}/incidents/${incidentId}`, formData);
    return res.data;
  },
  addIncidentNote: async (incidentId: string, notes: string) => {
    const formData = new FormData();
    formData.append('notes', notes);
    const res = await axios.post(`${API_BASE}/incidents/${incidentId}/notes`, formData);
    return res.data;
  },

  // Reports
  createReport: async (incidentId: string) => {
    const res = await axios.post(`${API_BASE}/reports/${incidentId}`);
    return res.data;
  },
  listReports: async (): Promise<ReportItem[]> => {
    const res = await axios.get(`${API_BASE}/reports`);
    return res.data;
  },

  // Evaluation
  getEvaluationScenarios: async () => {
    const res = await axios.get(`${API_BASE}/evaluation/scenarios`);
    return res.data;
  },
  runEvaluation: async (): Promise<EvaluationMetrics> => {
    const res = await axios.post(`${API_BASE}/evaluation/run`);
    return res.data;
  },

  // Settings
  getSettings: async (): Promise<SystemSettings> => {
    const res = await axios.get(`${API_BASE}/settings`);
    return res.data;
  },
  updateSettings: async (settings: { demo_mode?: boolean; retention_days?: number }) => {
    const formData = new FormData();
    if (settings.demo_mode !== undefined) formData.append('demo_mode', settings.demo_mode.toString());
    if (settings.retention_days !== undefined) formData.append('retention_days', settings.retention_days.toString());
    const res = await axios.patch(`${API_BASE}/settings`, formData);
    return res.data;
  },

  // Feedback
  submitFeedback: async (analysisId: string, feedbackType: string, comments?: string) => {
    const formData = new FormData();
    formData.append('analysis_id', analysisId);
    formData.append('feedback_type', feedbackType);
    if (comments) formData.append('comments', comments);
    const res = await axios.post(`${API_BASE}/feedback`, formData);
    return res.data;
  }
};
