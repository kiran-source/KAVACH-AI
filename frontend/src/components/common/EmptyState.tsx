import React from 'react';
import { clsx } from 'clsx';
import { LucideIcon } from 'lucide-react';
import { Button } from './Button';

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  className = '',
}) => {
  return (
    <div
      className={clsx(
        'flex flex-col items-center justify-center p-8 rounded-xl border border-dashed border-slate-800 bg-[#0a0f1c]/50 text-center max-w-lg mx-auto',
        className
      )}
      role="region"
      aria-label={title}
    >
      <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700/60 flex items-center justify-center text-cyan-400 mb-4 shadow-sm">
        <Icon className="w-6 h-6 stroke-[1.75]" aria-hidden="true" />
      </div>
      <h3 className="text-base font-semibold text-slate-100 mb-1.5">{title}</h3>
      <p className="text-xs text-slate-400 leading-relaxed mb-5 max-w-sm">{description}</p>
      {actionLabel && onAction && (
        <Button variant="primary" size="sm" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
};

