import React from 'react';
import { clsx } from 'clsx';
import { Search, X } from 'lucide-react';

interface SearchInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  value: string;
  onChangeValue: (val: string) => void;
  placeholder?: string;
  className?: string;
}

export const SearchInput: React.FC<SearchInputProps> = ({
  value,
  onChangeValue,
  placeholder = 'Search incidents, transcripts, indicators...',
  className = '',
  ...props
}) => {
  return (
    <div className={clsx('relative flex items-center w-full', className)}>
      <Search className="w-4 h-4 text-slate-400 absolute left-3 pointer-events-none" aria-hidden="true" />
      <input
        type="search"
        value={value}
        onChange={(e) => onChangeValue(e.target.value)}
        placeholder={placeholder}
        aria-label={placeholder}
        className="w-full bg-[#0a0f1c] text-xs text-slate-100 placeholder:text-slate-500 rounded-lg pl-9 pr-8 py-2 border border-slate-700/80 focus:border-cyan-500/80 focus:outline-none focus:ring-1 focus:ring-cyan-500/50 transition-colors font-sans"
        {...props}
      />
      {value && (
        <button
          type="button"
          onClick={() => onChangeValue('')}
          className="absolute right-2.5 p-0.5 rounded text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          aria-label="Clear search query"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      )}
    </div>
  );
};

