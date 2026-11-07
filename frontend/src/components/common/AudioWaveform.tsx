import React, { useEffect, useRef } from 'react';
import { clsx } from 'clsx';

interface AudioWaveformProps {
  progress?: number; // 0 to 1
  isRecording?: boolean;
  isPlaying?: boolean;
  barCount?: number;
  height?: number;
  className?: string;
  onSeek?: (ratio: number) => void;
}

export const AudioWaveform: React.FC<AudioWaveformProps> = ({
  progress = 0,
  isRecording = false,
  isPlaying = false,
  barCount = 48,
  height = 56,
  className = '',
  onSeek,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animFrameRef = useRef<number | null>(null);

  // Pre-generate pseudo-random baseline bar heights
  const barsRef = useRef<number[]>(
    Array.from({ length: barCount }, (_, i) => {
      // Natural speech envelope simulation: higher in middle, tapered at ends
      const pos = i / barCount;
      const envelope = Math.sin(pos * Math.PI);
      const jitter = 0.3 + 0.7 * Math.abs(Math.sin(i * 1.618));
      return Math.max(0.12, Math.min(1.0, envelope * jitter));
    })
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let tick = 0;

    const render = () => {
      tick += 0.05;
      const width = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, width, h);

      const barWidth = Math.max(2, Math.floor((width - (barCount - 1) * 3) / barCount));
      const gap = 3;

      for (let i = 0; i < barCount; i++) {
        const x = i * (barWidth + gap);
        let barHeightRatio = barsRef.current[i] || 0.2;

        if (isRecording) {
          // Dynamic live acoustic wave oscillation
          const wave = Math.sin(tick * 3 + i * 0.4) * 0.35 + Math.cos(tick * 2 + i * 0.8) * 0.2;
          barHeightRatio = Math.max(0.1, Math.min(1.0, barHeightRatio + wave));
        }

        const barHeight = Math.max(4, barHeightRatio * (h - 8));
        const y = (h - barHeight) / 2;
        const isPast = (i / barCount) <= progress;

        // Gradient coloring: past is bright cyan/teal, future is dark slate
        if (isRecording) {
          ctx.fillStyle = '#ef4444'; // Recording active red
        } else if (isPast) {
          const grad = ctx.createLinearGradient(0, y, 0, y + barHeight);
          grad.addColorStop(0, '#22d3ee');
          grad.addColorStop(1, '#06b6d4');
          ctx.fillStyle = grad;
        } else {
          ctx.fillStyle = '#1e293b';
        }

        // Rounded bar
        ctx.beginPath();
        ctx.roundRect(x, y, barWidth, barHeight, 2);
        ctx.fill();
      }

      if (isRecording || isPlaying) {
        animFrameRef.current = requestAnimationFrame(render);
      }
    };

    render();

    return () => {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    };
  }, [progress, isRecording, isPlaying, barCount]);

  const handleClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!onSeek) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const ratio = Math.max(0, Math.min(1, clickX / rect.width));
    onSeek(ratio);
  };

  return (
    <div
      className={clsx('relative flex items-center justify-center select-none w-full', className)}
      role="progressbar"
      aria-valuenow={Math.round(progress * 100)}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={isRecording ? 'Live recording audio waveform' : 'Audio playback progress waveform'}
    >
      <canvas
        ref={canvasRef}
        width={480}
        height={height}
        onClick={handleClick}
        className={clsx('w-full rounded-lg', onSeek && 'cursor-pointer hover:opacity-90')}
        style={{ height: `${height}px` }}
      />
    </div>
  );
};

