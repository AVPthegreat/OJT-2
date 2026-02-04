'use client';

interface Score {
    technical_accuracy: number;
    clarity: number;
    depth: number;
    confidence: number;
    communication: number;
    overall: number;
    feedback: string;
}

interface ScoreCardProps {
    score: Score;
}

const getScoreColor = (value: number) => {
    if (value >= 8) return 'from-green-500 to-emerald-500';
    if (value >= 6) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
};

const getScoreLabel = (value: number) => {
    if (value >= 8) return 'Excellent';
    if (value >= 6) return 'Good';
    if (value >= 4) return 'Needs Work';
    return 'Poor';
};

export default function ScoreCard({ score }: ScoreCardProps) {
    const metrics = [
        { key: 'technical_accuracy', label: 'Technical Accuracy', icon: '🎯' },
        { key: 'clarity', label: 'Clarity', icon: '💡' },
        { key: 'depth', label: 'Depth', icon: '📚' },
        { key: 'confidence', label: 'Confidence', icon: '💪' },
        { key: 'communication', label: 'Communication', icon: '🗣️' },
    ];

    return (
        <div className="space-y-6">
            {/* Overall score */}
            <div className="text-center">
                <h2 className="text-lg font-semibold text-[var(--text-secondary)] mb-4">Session Complete</h2>
                <div className="relative inline-flex items-center justify-center">
                    <svg className="w-32 h-32 transform -rotate-90">
                        <circle
                            cx="64"
                            cy="64"
                            r="56"
                            stroke="currentColor"
                            strokeWidth="8"
                            fill="none"
                            className="text-[var(--bg-tertiary)]"
                        />
                        <circle
                            cx="64"
                            cy="64"
                            r="56"
                            stroke="url(#scoreGradient)"
                            strokeWidth="8"
                            fill="none"
                            strokeLinecap="round"
                            strokeDasharray={`${(score.overall / 10) * 352} 352`}
                        />
                        <defs>
                            <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stopColor="#6366f1" />
                                <stop offset="100%" stopColor="#8b5cf6" />
                            </linearGradient>
                        </defs>
                    </svg>
                    <div className="absolute flex flex-col items-center">
                        <span className="text-4xl font-bold gradient-text">{score.overall.toFixed(1)}</span>
                        <span className="text-sm text-[var(--text-muted)]">/ 10</span>
                    </div>
                </div>
                <p className={`mt-2 font-medium ${score.overall >= 8 ? 'text-green-400' : score.overall >= 6 ? 'text-yellow-400' : 'text-red-400'}`}>
                    {getScoreLabel(score.overall)}
                </p>
            </div>

            {/* Individual metrics */}
            <div className="space-y-3">
                {metrics.map(({ key, label, icon }) => {
                    const value = score[key as keyof Score] as number;
                    return (
                        <div key={key}>
                            <div className="flex items-center justify-between mb-1">
                                <span className="text-sm flex items-center gap-2">
                                    <span>{icon}</span>
                                    <span>{label}</span>
                                </span>
                                <span className="text-sm font-medium">{value.toFixed(1)}</span>
                            </div>
                            <div className="score-meter">
                                <div
                                    className={`score-meter-fill bg-gradient-to-r ${getScoreColor(value)}`}
                                    style={{ width: `${(value / 10) * 100}%` }}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Feedback */}
            <div className="card-glass">
                <h3 className="text-sm font-medium mb-2 flex items-center gap-2">
                    <span>📝</span>
                    <span>AI Feedback</span>
                </h3>
                <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
                    {score.feedback}
                </p>
            </div>
        </div>
    );
}
