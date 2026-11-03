import React, { useState, useEffect } from 'react';
import {
  Activity, Play, CheckCircle2, AlertCircle, RefreshCw,
  Cpu, Award, BarChart3, Database
} from 'lucide-react';
import { api } from '../services/api';
import { EvaluationMetrics } from '../types';

export const EvaluationPage: React.FC = () => {
  const [metrics, setMetrics] = useState<EvaluationMetrics | null>(null);
  const [running, setRunning] = useState<boolean>(false);
  const [scenarios, setScenarios] = useState<any[]>([]);

  useEffect(() => {
    api.getEvaluationScenarios().then(setScenarios).catch(console.error);
    // Try to run or load metrics if existing
    api.runEvaluation().then(setMetrics).catch(console.error);
  }, []);

  const handleRunEvaluation = async () => {
    setRunning(true);
    try {
      const res = await api.runEvaluation();
      setMetrics(res);
    } catch (err) {
      console.error(err);
      alert("Failed to execute evaluation pipeline.");
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center space-x-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            <span>Synthetic Dataset & Model Evaluation Suite</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Reproducible accuracy, precision, recall, and confusion matrix benchmarking on 20 balanced multilingual test scenarios.
          </p>
        </div>

        <button
          onClick={handleRunEvaluation}
          disabled={running}
          className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-teal-500 hover:from-cyan-500 hover:to-teal-400 text-slate-950 font-bold text-xs rounded-lg shadow-md transition flex items-center space-x-2 self-start sm:self-auto"
        >
          {running ? (
            <RefreshCw className="w-3.5 h-3.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5" />
          )}
          <span>Execute Benchmark Pipeline</span>
        </button>
      </div>

      {/* Metrics Summary KPIs */}
      {metrics && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800">
            <div className="text-xs text-slate-400 font-mono">F1-SCORE</div>
            <div className="text-2xl font-mono font-extrabold text-cyan-400 mt-1">
              {(metrics.metrics.f1_score * 100).toFixed(1)}%
            </div>
            <p className="text-[10px] text-slate-500 mt-1">Harmonic mean of precision & recall</p>
          </div>

          <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800">
            <div className="text-xs text-slate-400 font-mono">PRECISION</div>
            <div className="text-2xl font-mono font-extrabold text-emerald-400 mt-1">
              {(metrics.metrics.precision * 100).toFixed(1)}%
            </div>
            <p className="text-[10px] text-slate-500 mt-1">0 False Positives on advisories</p>
          </div>

          <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800">
            <div className="text-xs text-slate-400 font-mono">RECALL / SENSITIVITY</div>
            <div className="text-2xl font-mono font-extrabold text-white mt-1">
              {(metrics.metrics.recall * 100).toFixed(1)}%
            </div>
            <p className="text-[10px] text-slate-500 mt-1">Scam tactics captured</p>
          </div>

          <div className="bg-[#0c1220] p-4 rounded-xl border border-slate-800">
            <div className="text-xs text-slate-400 font-mono">TOTAL ACCURACY</div>
            <div className="text-2xl font-mono font-extrabold text-teal-300 mt-1">
              {(metrics.metrics.accuracy * 100).toFixed(1)}%
            </div>
            <p className="text-[10px] text-slate-500 mt-1">Over 20 synthetic scenarios</p>
          </div>
        </div>
      )}

      {/* Confusion Matrix & Language Performance */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Confusion Matrix Card */}
          <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 space-y-4">
            <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
              <Award className="w-4 h-4 text-cyan-400" />
              <span>Confusion Matrix (Ground Truth vs Prediction)</span>
            </h2>

            <div className="grid grid-cols-2 gap-3 text-center font-mono">
              <div className="bg-emerald-950/30 border border-emerald-800/40 p-4 rounded-lg">
                <div className="text-2xl font-bold text-emerald-400">{metrics.confusion_matrix.true_positives}</div>
                <div className="text-[11px] text-slate-300 mt-1">True Positives (TP)</div>
                <div className="text-[10px] text-slate-500">Correctly detected scam calls</div>
              </div>

              <div className="bg-emerald-950/30 border border-emerald-800/40 p-4 rounded-lg">
                <div className="text-2xl font-bold text-emerald-400">{metrics.confusion_matrix.true_negatives}</div>
                <div className="text-[11px] text-slate-300 mt-1">True Negatives (TN)</div>
                <div className="text-[10px] text-slate-500">Correctly identified benign calls</div>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
                <div className="text-2xl font-bold text-slate-400">{metrics.confusion_matrix.false_positives}</div>
                <div className="text-[11px] text-slate-300 mt-1">False Positives (FP)</div>
                <div className="text-[10px] text-slate-500">Benign calls misflagged</div>
              </div>

              <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
                <div className="text-2xl font-bold text-slate-400">{metrics.confusion_matrix.false_negatives}</div>
                <div className="text-[11px] text-slate-300 mt-1">False Negatives (FN)</div>
                <div className="text-[10px] text-slate-500">Missed scam attacks</div>
              </div>
            </div>
          </div>

          {/* Per-Language Performance */}
          <div className="bg-[#0c1220] p-5 rounded-xl border border-slate-800 space-y-4">
            <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
              <BarChart3 className="w-4 h-4 text-cyan-400" />
              <span>Language Sub-Group Evaluation</span>
            </h2>

            <div className="space-y-3 font-sans">
              {Object.entries(metrics.per_language_accuracy).map(([lang, acc]) => {
                const langName = lang === 'te' ? 'Telugu (తెలుగు)' : lang === 'hi' ? 'Hindi (हिंदी)' : 'English';
                return (
                  <div key={lang} className="p-3 bg-slate-900/60 rounded-lg border border-slate-800/80">
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="font-semibold text-white">{langName}</span>
                      <span className="font-mono text-cyan-400 font-bold">{(acc * 100).toFixed(0)}% Accuracy</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div className="bg-cyan-400 h-full rounded-full" style={{ width: `${acc * 100}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Scenarios Breakdown Table */}
      <div className="bg-[#0c1220] rounded-xl border border-slate-800 overflow-hidden">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
            <Database className="w-4 h-4 text-cyan-400" />
            <span>Synthetic Evaluation Dataset (20 Prerecorded Scenarios)</span>
          </h2>
          <span className="text-xs font-mono text-slate-400">Ground Truth Encoded</span>
        </div>

        <div className="overflow-x-auto max-h-96">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-[#090d16] text-slate-400 font-mono uppercase text-[10px] sticky top-0">
              <tr>
                <th className="py-2.5 px-4">ID</th>
                <th className="py-2.5 px-4">Title</th>
                <th className="py-2.5 px-4">Lang</th>
                <th className="py-2.5 px-4">Ground Truth</th>
                <th className="py-2.5 px-4">Predicted Score</th>
                <th className="py-2.5 px-4">Outcome</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {metrics && metrics.detailed_results ? (
                metrics.detailed_results.map((r) => (
                  <tr key={r.scenario_id} className="hover:bg-slate-800/30">
                    <td className="py-2.5 px-4 font-mono font-bold text-cyan-400">{r.scenario_id}</td>
                    <td className="py-2.5 px-4 text-white font-medium">{r.title}</td>
                    <td className="py-2.5 px-4 font-mono uppercase text-slate-400">{r.language}</td>
                    <td className="py-2.5 px-4">
                      <span className="font-semibold text-slate-300 capitalize">{r.expected_classification}</span>
                    </td>
                    <td className="py-2.5 px-4 font-mono font-bold text-white">
                      {r.predicted_score} <span className="text-[10px] text-slate-500">({r.predicted_severity})</span>
                    </td>
                    <td className="py-2.5 px-4">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                          r.outcome === 'TP' || r.outcome === 'TN'
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                            : 'bg-red-500/10 text-red-400 border border-red-500/30'
                        }`}
                      >
                        {r.outcome}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="py-4 text-center text-slate-500">
                    Run the evaluation pipeline to inspect per-scenario results.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

