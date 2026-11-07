import React from 'react';
import { clsx } from 'clsx';
import { ShieldAlert, AlertTriangle, AlertCircle, ShieldCheck, Info, CheckCircle2, Clock, XCircle } from 'lucide-react';

export type ThreatSeverity = 'Critical' | 'High' | 'Medium' | 'Guarded' | 'Low' | 'Informational';
export type IncidentStatus = 'New' | 'Under Review' | 'Confirmed Suspicious' | 'False Positive' | 'Resolved' | 'OPEN' | 'INVESTIGATING' | 'CONFIRMED_FRAUD' | 'FALSE_POSITIVE' | 'RESOLVED';

interface SeverityBadgeProps {
  severity: string;
  size?: 'xs' | 'sm' | 'md';
  showIcon?: boolean;
  className?: string;
}

export const SeverityBadge: React.FC<SeverityBadgeProps> = ({
  severity,
  size = 'sm',
  showIcon = true,
  className = '',
}) => {
  const norm = severity?.toLowerCase() || 'low';

  const configs: Record<string, { label: string; icon: React.ElementType; classes: string }> = {
    critical: {
      label: 'Critical',
      icon: ShieldAlert,
      classes: 'bg-red-950/40 text-red-400 border-red-500/40 shadow-sm shadow-red-950/50',
    },
    high: {
      label: 'High',
      icon: AlertTriangle,
      classes: 'bg-orange-950/40 text-orange-400 border-orange-500/40',
    },
    medium: {
      label: 'Medium',
      icon: AlertCircle,
      classes: 'bg-amber-950/40 text-amber-400 border-amber-500/40',
    },
    guarded: {
      label: 'Guarded',
      icon: Info,
      classes: 'bg-blue-950/40 text-blue-400 border-blue-500/40',
    },
    low: {
      label: 'Low / Safe',
      icon: ShieldCheck,
      classes: 'bg-emerald-950/40 text-emerald-400 border-emerald-500/40',
    },
    safe: {
      label: 'Safe',
      icon: ShieldCheck,
      classes: 'bg-emerald-950/40 text-emerald-400 border-emerald-500/40',
    },
  };

  const current = configs[norm] || {
    label: severity || 'Unknown',
    icon: Info,
    classes: 'bg-slate-800/60 text-slate-300 border-slate-700/60',
  };

  const Icon = current.icon;

  const sizeClasses = {
    xs: 'text-[10px] px-1.5 py-0.5 gap-1 font-mono',
    sm: 'text-xs px-2.5 py-1 gap-1.5 font-medium',
    md: 'text-sm px-3 py-1.5 gap-2 font-medium',
  };

  const iconSizes = {
    xs: 'w-2.5 h-2.5',
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-md border font-mono tracking-wide select-none',
        current.classes,
        sizeClasses[size],
        className
      )}
      role="status"
      aria-label={`Threat severity: ${current.label}`}
    >
      {showIcon && <Icon className={clsx(iconSizes[size], 'shrink-0')} aria-hidden="true" />}
      <span>{current.label}</span>
    </span>
  );
};

interface StatusBadgeProps {
  status: string;
  size?: 'xs' | 'sm';
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  size = 'sm',
  className = '',
}) => {
  const norm = status?.toLowerCase() || 'new';

  const configs: Record<string, { label: string; icon: React.ElementType; classes: string }> = {
    new: {
      label: 'New',
      icon: AlertCircle,
      classes: 'bg-cyan-950/40 text-cyan-400 border-cyan-500/30',
    },
    'under review': {
      label: 'Under Review',
      icon: Clock,
      classes: 'bg-amber-950/40 text-amber-400 border-amber-500/30',
    },
    investigating: {
      label: 'Investigating',
      icon: Clock,
      classes: 'bg-amber-950/40 text-amber-400 border-amber-500/30',
    },
    'confirmed suspicious': {
      label: 'Confirmed Suspicious',
      icon: ShieldAlert,
      classes: 'bg-red-950/40 text-red-400 border-red-500/40',
    },
    confirmed_fraud: {
      label: 'Confirmed Fraud',
      icon: ShieldAlert,
      classes: 'bg-red-950/40 text-red-400 border-red-500/40',
    },
    'false positive': {
      label: 'False Positive',
      icon: XCircle,
      classes: 'bg-slate-800/60 text-slate-400 border-slate-700/50',
    },
    false_positive: {
      label: 'False Positive',
      icon: XCircle,
      classes: 'bg-slate-800/60 text-slate-400 border-slate-700/50',
    },
    resolved: {
      label: 'Resolved',
      icon: CheckCircle2,
      classes: 'bg-emerald-950/40 text-emerald-400 border-emerald-500/30',
    },
  };

  const current = configs[norm] || {
    label: status || 'Unknown',
    icon: Info,
    classes: 'bg-slate-800 text-slate-400 border-slate-700',
  };

  const Icon = current.icon;
  const sizeClass = size === 'xs' ? 'text-[10px] px-1.5 py-0.5 gap-1' : 'text-xs px-2.5 py-0.5 gap-1.5';

  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full border font-mono tracking-tight font-medium',
        current.classes,
        sizeClass,
        className
      )}
      role="status"
    >
      <Icon className="w-3 h-3 shrink-0" aria-hidden="true" />
      <span>{current.label}</span>
    </span>
  );
};

