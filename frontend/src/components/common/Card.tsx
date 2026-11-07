import React from 'react';
import { clsx } from 'clsx';

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement> & { elevated?: boolean; interactive?: boolean }> = ({
  className = '',
  elevated = false,
  interactive = false,
  children,
  ...props
}) => {
  return (
    <div
      className={clsx(
        'rounded-xl border transition-all duration-150',
        elevated
          ? 'bg-[#131c31] border-slate-700/60 shadow-lg shadow-black/40'
          : 'bg-[#0d1424] border-slate-800/80 shadow-md shadow-black/30',
        interactive && 'hover:border-cyan-500/40 hover:bg-[#10192e] cursor-pointer',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className = '',
  children,
  ...props
}) => {
  return (
    <div className={clsx('p-5 border-b border-slate-800/60 flex flex-col gap-1', className)} {...props}>
      {children}
    </div>
  );
};

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({
  className = '',
  children,
  ...props
}) => {
  return (
    <h3 className={clsx('text-base font-semibold text-slate-100 tracking-tight flex items-center justify-between', className)} {...props}>
      {children}
    </h3>
  );
};

export const CardDescription: React.FC<React.HTMLAttributes<HTMLParagraphElement>> = ({
  className = '',
  children,
  ...props
}) => {
  return (
    <p className={clsx('text-xs text-slate-400 font-normal leading-relaxed', className)} {...props}>
      {children}
    </p>
  );
};

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className = '',
  children,
  ...props
}) => {
  return (
    <div className={clsx('p-5', className)} {...props}>
      {children}
    </div>
  );
};

export const CardFooter: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className = '',
  children,
  ...props
}) => {
  return (
    <div className={clsx('p-4 border-t border-slate-800/60 bg-slate-900/30 rounded-b-xl flex items-center justify-between', className)} {...props}>
      {children}
    </div>
  );
};

