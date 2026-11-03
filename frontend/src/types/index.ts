export interface ProviderStatus {
  name: string;
  status: string;
  version: string;
  languages?: string[];
}

export interface SystemProviders {
  gnani_prisma: ProviderStatus;
  gnani_timbre: ProviderStatus;
  gnani_evon: ProviderStatus;
}

export interface DashboardMetrics {
  total_analyzed_calls: number;
  total_incidents: number;
  high_risk_incidents: number;
  medium_risk_incidents: number;
  low_risk_incidents: number;
  safe_calls: number;
  average_risk_score: number;
  detection_rate: number;
  false_positive_rate: number;
  risk_distribution: {
    Critical: number;
    High: number;
    Medium: number;
    Guarded: number;
    Low: number;
  };
  language_distribution: Record<string, number>;
  threat_category_distribution: Record<string, number>;
  recent_incidents: IncidentSummary[];
}

export interface ThreatDetail {
  rule_id: string;
  category: string;
  matched_text: string;
  evidence_start?: number;
  evidence_end?: number;
  contribution: number;
  explanation: string;
  recommendation?: string;
}

export interface AnalysisResponse {
  analysis_id: string;
  transcript_id: string;
  risk_score: number;
  severity: 'Low' | 'Guarded' | 'Medium' | 'High' | 'Critical';
  threats: ThreatDetail[];
  categories: string[];
  recommendations: string[];
  context_suppressed?: boolean;
  context_note?: string;
  incident_id?: string;
  engine_version: string;
}

export interface TranscriptSegment {
  start: number;
  end: number;
  text: string;
  language: string;
}

export interface TranscriptResponse {
  transcript_id: string;
  audio_id?: string;
  language: string;
  detected_languages: string[];
  segments: TranscriptSegment[];
  full_text: string;
  provider: string;
  is_mock?: boolean;
}

export interface IncidentSummary {
  id: string;
  incident_number: string;
  title: string;
  severity: string;
  status: string;
  assigned_analyst?: string;
  risk_score: number;
  created_at: string;
  updated_at?: string;
}

export interface IncidentTimelineItem {
  event_type: string;
  description: string;
  event_time: string;
}

export interface IncidentDetail extends IncidentSummary {
  analysis_id: string;
  analyst_notes?: string;
  transcript_text: string;
  detected_language: string;
  audio_filename: string;
  audio_id?: string;
  threats: ThreatDetail[];
  timeline: IncidentTimelineItem[];
  report_id?: string;
}

export interface ReportItem {
  report_id: string;
  incident_id: string;
  incident_number: string;
  title: string;
  severity: string;
  generated_at: string;
  download_url: string;
}

export interface EvaluationMetrics {
  dataset_size: number;
  confusion_matrix: {
    true_positives: number;
    true_negatives: number;
    false_positives: number;
    false_negatives: number;
  };
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
  };
  per_language_accuracy: Record<string, number>;
  per_category_coverage: Record<string, number>;
  detailed_results: Array<{
    scenario_id: string;
    title: string;
    language: string;
    expected_classification: string;
    predicted_score: number;
    predicted_severity: string;
    detected_categories: string[];
    outcome: 'TP' | 'TN' | 'FP' | 'FN';
  }>;
}

export interface SystemSettings {
  preferred_language: string;
  warning_voice_language: string;
  audio_retention_days: number;
  max_upload_size_mb: number;
  demo_mode: boolean;
  gnani_prisma_connected: boolean;
  gnani_timbre_connected: boolean;
  gnani_evon_connected: boolean;
  app_version: string;
}
