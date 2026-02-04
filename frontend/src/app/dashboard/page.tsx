'use client';

import { useState } from 'react';
import Link from 'next/link';

// Mock data for demo
const mockSessions = [
    {
        id: '1',
        date: new Date('2024-02-03T14:30:00'),
        duration: 1245,
        score: 8.2,
        topic: 'Linked Lists & Arrays'
    },
    {
        id: '2',
        date: new Date('2024-02-02T10:15:00'),
        duration: 1890,
        score: 7.5,
        topic: 'Binary Search Trees'
    },
    {
        id: '3',
        date: new Date('2024-02-01T16:45:00'),
        duration: 1520,
        score: 6.8,
        topic: 'Graph Traversals'
    },
];

const mockStats = {
    totalSessions: 12,
    avgScore: 7.6,
    totalTime: 18540,
    improvement: 15,
};

export default function DashboardPage() {
    const [activeTab, setActiveTab] = useState<'overview' | 'history'>('overview');

    const formatDuration = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}m ${secs}s`;
    };

    const formatDate = (date: Date) => {
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const getScoreColor = (score: number) => {
        if (score >= 8) return 'text-green-400';
        if (score >= 6) return 'text-yellow-400';
        return 'text-red-400';
    };

    return (
        <div className="min-h-screen">
            {/* Header */}
            <header className="glass border-b border-[var(--glass-border)] px-6 py-4">
                <div className="max-w-6xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Link href="/" className="p-2 rounded-lg hover:bg-white/5 transition-colors">
                            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                            </svg>
                        </Link>
                        <h1 className="text-xl font-semibold">Dashboard</h1>
                    </div>

                    <Link href="/interview">
                        <button className="btn-primary">
                            New Session
                        </button>
                    </Link>
                </div>
            </header>

            {/* Main content */}
            <main className="max-w-6xl mx-auto p-6">
                {/* Stats cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                    <div className="card-glass">
                        <p className="text-sm text-[var(--text-muted)] mb-1">Total Sessions</p>
                        <p className="text-3xl font-bold">{mockStats.totalSessions}</p>
                    </div>
                    <div className="card-glass">
                        <p className="text-sm text-[var(--text-muted)] mb-1">Average Score</p>
                        <p className={`text-3xl font-bold ${getScoreColor(mockStats.avgScore)}`}>
                            {mockStats.avgScore.toFixed(1)}
                        </p>
                    </div>
                    <div className="card-glass">
                        <p className="text-sm text-[var(--text-muted)] mb-1">Total Practice Time</p>
                        <p className="text-3xl font-bold">{Math.floor(mockStats.totalTime / 3600)}h</p>
                    </div>
                    <div className="card-glass">
                        <p className="text-sm text-[var(--text-muted)] mb-1">Improvement</p>
                        <p className="text-3xl font-bold text-green-400">+{mockStats.improvement}%</p>
                    </div>
                </div>

                {/* Tabs */}
                <div className="flex gap-4 mb-6 border-b border-[var(--glass-border)]">
                    <button
                        onClick={() => setActiveTab('overview')}
                        className={`pb-3 px-2 font-medium transition-colors ${activeTab === 'overview'
                                ? 'border-b-2 border-[var(--accent-primary)] text-white'
                                : 'text-[var(--text-muted)] hover:text-white'
                            }`}
                    >
                        Overview
                    </button>
                    <button
                        onClick={() => setActiveTab('history')}
                        className={`pb-3 px-2 font-medium transition-colors ${activeTab === 'history'
                                ? 'border-b-2 border-[var(--accent-primary)] text-white'
                                : 'text-[var(--text-muted)] hover:text-white'
                            }`}
                    >
                        Session History
                    </button>
                </div>

                {activeTab === 'overview' && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Performance chart placeholder */}
                        <div className="card">
                            <h3 className="text-lg font-semibold mb-4">Performance Trend</h3>
                            <div className="h-48 flex items-center justify-center text-[var(--text-muted)]">
                                <div className="text-center">
                                    <svg className="w-12 h-12 mx-auto mb-2 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                    </svg>
                                    <p className="text-sm">Complete more sessions to see trends</p>
                                </div>
                            </div>
                        </div>

                        {/* Skills breakdown */}
                        <div className="card">
                            <h3 className="text-lg font-semibold mb-4">Skills Breakdown</h3>
                            <div className="space-y-4">
                                {[
                                    { skill: 'Technical Accuracy', score: 7.8 },
                                    { skill: 'Clarity', score: 8.2 },
                                    { skill: 'Depth', score: 6.5 },
                                    { skill: 'Confidence', score: 7.5 },
                                    { skill: 'Communication', score: 8.0 },
                                ].map(item => (
                                    <div key={item.skill}>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span>{item.skill}</span>
                                            <span className={getScoreColor(item.score)}>{item.score}</span>
                                        </div>
                                        <div className="score-meter">
                                            <div
                                                className="score-meter-fill bg-gradient-to-r from-indigo-500 to-purple-500"
                                                style={{ width: `${(item.score / 10) * 100}%` }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Recent activity */}
                        <div className="card md:col-span-2">
                            <h3 className="text-lg font-semibold mb-4">Recent Sessions</h3>
                            <div className="space-y-3">
                                {mockSessions.slice(0, 3).map(session => (
                                    <div
                                        key={session.id}
                                        className="flex items-center justify-between p-4 rounded-xl bg-[var(--bg-tertiary)] hover:bg-white/5 transition-colors"
                                    >
                                        <div className="flex items-center gap-4">
                                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center">
                                                <span className="text-lg">📚</span>
                                            </div>
                                            <div>
                                                <p className="font-medium">{session.topic}</p>
                                                <p className="text-sm text-[var(--text-muted)]">{formatDate(session.date)}</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-6">
                                            <span className="text-sm text-[var(--text-muted)]">{formatDuration(session.duration)}</span>
                                            <span className={`font-bold ${getScoreColor(session.score)}`}>{session.score}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'history' && (
                    <div className="card">
                        <div className="space-y-3">
                            {mockSessions.map(session => (
                                <div
                                    key={session.id}
                                    className="flex items-center justify-between p-4 rounded-xl bg-[var(--bg-tertiary)] hover:bg-white/5 transition-colors cursor-pointer"
                                >
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center">
                                            <span className="text-xl">📚</span>
                                        </div>
                                        <div>
                                            <p className="font-medium">{session.topic}</p>
                                            <p className="text-sm text-[var(--text-muted)]">{formatDate(session.date)}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-8">
                                        <div className="text-right">
                                            <p className="text-sm text-[var(--text-muted)]">Duration</p>
                                            <p className="font-medium">{formatDuration(session.duration)}</p>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-sm text-[var(--text-muted)]">Score</p>
                                            <p className={`text-xl font-bold ${getScoreColor(session.score)}`}>{session.score}</p>
                                        </div>
                                        <svg className="w-5 h-5 text-[var(--text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                        </svg>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}
