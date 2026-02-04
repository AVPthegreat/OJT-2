'use client';

interface AudioVisualizerProps {
    isActive: boolean;
}

export default function AudioVisualizer({ isActive }: AudioVisualizerProps) {
    return (
        <div className="flex items-center justify-center gap-1 h-12">
            {[...Array(5)].map((_, i) => (
                <div
                    key={i}
                    className={`w-1.5 rounded-full transition-all duration-150 ${isActive
                            ? 'bg-gradient-to-t from-indigo-500 to-purple-500 audio-bar'
                            : 'bg-[var(--glass-border)] h-2'
                        }`}
                    style={{
                        animationDelay: isActive ? `${i * 0.1}s` : '0s',
                        height: isActive ? undefined : '8px'
                    }}
                />
            ))}
        </div>
    );
}
