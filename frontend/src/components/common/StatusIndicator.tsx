import React from 'react';
import { clsx } from 'clsx';

interface StatusIndicatorProps {
  status: 'online' | 'active' | 'warning' | 'offline' | 'busy';
  label?: string;
  size?: 'sm' | 'md';
  pulse?: boolean;
  className?: string;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  status,
  label,
  size = 'sm',
  pulse = false,
  className = '',
}) => {
  const configs = {
    online: {
      dot: 'bg-emerald-400',
      ping: 'bg-emerald-400',
      text: 'text-emerald-400',
      defaultLabel: 'Online',
    },
    active: {
      dot: 'bg-cyan-400',
      ping: 'bg-cyan-400',
      text: 'text-cyan-400',
      defaultLabel: 'Active',
    },
    warning: {
      dot: 'bg-amber-400',
      ping: 'bg-amber-400',
      text: 'text-amber-400',
      defaultLabel: 'Degraded',
    },
    busy: {
      dot: 'bg-purple-400',
      ping: 'bg-purple-400',
      text: 'text-purple-400',
      defaultLabel: 'Processing',
    },
    offline: {
      dot: 'bg-slate-500',
      ping: 'bg-slate-500',
      text: 'text-slate-400',
      defaultLabel: 'Offline',
    },
  };

  const current = configs[status] || configs.offline;
  const dotSize = size === 'sm' ? 'w-2 h-2' : 'w-2.5 h-2.5';

  return (
    <div className={clsx('inline-flex items-center gap-2 select-none', className)}>
      <span className="relative flex shrink-0">
        {pulse && (
          <span
            className={clsx(
              'animate-ping absolute inline-flex h-full w-full rounded-full opacity-75',
              current.ping
            )}
            aria-hidden="true"
          />
        )}
        <span className={clsx('relative inline-flex rounded-full', dotSize, current.dot)} />
      </span>
      {label !== undefined ? (
        <span className={clsx('font-mono text-xs font-medium', current.text)}>{label}</span>
      ) : (
        <span className={clsx('font-mono text-xs font-medium', current.text)}>{current.defaultLabel}</span>
      )}
    </div>
  );
};

