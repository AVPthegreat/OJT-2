'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import AudioVisualizer from '@/components/AudioVisualizer';
import ChatMessage from '@/components/ChatMessage';
import ScoreCard from '@/components/ScoreCard';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

interface Score {
    technical_accuracy: number;
    clarity: number;
    depth: number;
    confidence: number;
    communication: number;
    overall: number;
    feedback: string;
}

export default function InterviewPage() {
    const router = useRouter();
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [isAISpeaking, setIsAISpeaking] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [score, setScore] = useState<Score | null>(null);
    const [sessionEnded, setSessionEnded] = useState(false);
    const [time, setTime] = useState(0);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Timer
    useEffect(() => {
        if (sessionId && !sessionEnded) {
            const interval = setInterval(() => {
                setTime(t => t + 1);
            }, 1000);
            return () => clearInterval(interval);
        }
    }, [sessionId, sessionEnded]);

    // Scroll to bottom of messages
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Start session on mount
    useEffect(() => {
        startSession();
    }, []);

    const startSession = async () => {
        try {
            const res = await fetch('http://localhost:8000/api/interview/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ subject: 'DSA' })
            });

            if (res.ok) {
                const data = await res.json();
                setSessionId(data.session_id);

                // Add welcome message
                setMessages([{
                    id: '1',
                    role: 'assistant',
                    content: "Hello! Welcome to your DSA viva. I'll be evaluating your understanding of data structures and algorithms. Let's begin with a fundamental question: Can you explain what a linked list is and how it differs from an array?",
                    timestamp: new Date()
                }]);

                setIsAISpeaking(true);
                setTimeout(() => setIsAISpeaking(false), 3000);
            }
        } catch (error) {
            console.error('Failed to start session:', error);
            // Demo mode - continue without backend
            setSessionId('demo-session');
            setMessages([{
                id: '1',
                role: 'assistant',
                content: "Hello! Welcome to your DSA viva. I'll be evaluating your understanding of data structures and algorithms. Let's begin with a fundamental question: Can you explain what a linked list is and how it differs from an array?",
                timestamp: new Date()
            }]);
        }
    };

    const toggleRecording = () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    };

    const startRecording = () => {
        setIsRecording(true);
        // TODO: Implement actual audio recording
    };

    const stopRecording = () => {
        setIsRecording(false);
        setIsProcessing(true);

        // Simulate processing and AI response
        setTimeout(() => {
            setMessages(prev => [
                ...prev,
                {
                    id: String(prev.length + 1),
                    role: 'user',
                    content: "A linked list is a linear data structure where elements are stored in nodes. Each node contains data and a pointer to the next node. Unlike arrays, linked lists don't require contiguous memory allocation, which makes insertion and deletion more efficient at O(1) when you have the reference. However, accessing elements is O(n) compared to O(1) for arrays.",
                    timestamp: new Date()
                }
            ]);

            setIsProcessing(false);
            setIsAISpeaking(true);

            setTimeout(() => {
                setMessages(prev => [
                    ...prev,
                    {
                        id: String(prev.length + 1),
                        role: 'assistant',
                        content: "Good explanation! You've covered the key differences. Now, can you tell me about the different types of linked lists and when you might use each one?",
                        timestamp: new Date()
                    }
                ]);
                setIsAISpeaking(false);
            }, 2000);
        }, 1500);
    };

    const endSession = async () => {
        setSessionEnded(true);

        // Mock score for demo
        setScore({
            technical_accuracy: 8.5,
            clarity: 7.8,
            depth: 7.2,
            confidence: 8.0,
            communication: 8.3,
            overall: 7.9,
            feedback: "Strong understanding of fundamentals. Consider discussing time/space complexity trade-offs more explicitly. Good clear communication style."
        });
    };

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className="min-h-screen flex flex-col">
            {/* Header */}
            <header className="glass border-b border-[var(--glass-border)] px-6 py-4 flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => router.push('/')}
                        className="p-2 rounded-lg hover:bg-white/5 transition-colors"
                    >
                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                    </button>
                    <div>
                        <h1 className="text-lg font-semibold">DSA Interview</h1>
                        <p className="text-sm text-[var(--text-muted)]">Session ID: {sessionId?.slice(0, 8)}...</p>
                    </div>
                </div>

                <div className="flex items-center gap-6">
                    {/* Timer */}
                    <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5">
                        <div className={`w-2 h-2 rounded-full ${sessionEnded ? 'bg-gray-500' : 'bg-green-500 animate-pulse'}`} />
                        <span className="font-mono text-lg">{formatTime(time)}</span>
                    </div>

                    {/* End session button */}
                    {!sessionEnded && (
                        <button
                            onClick={endSession}
                            className="px-4 py-2 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-colors"
                        >
                            End Session
                        </button>
                    )}
                </div>
            </header>

            {/* Main content */}
            <div className="flex-1 flex">
                {/* Chat area */}
                <div className="flex-1 flex flex-col">
                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-6 space-y-4">
                        {messages.map((msg) => (
                            <ChatMessage key={msg.id} message={msg} />
                        ))}

                        {isProcessing && (
                            <div className="flex items-center gap-2 text-[var(--text-muted)]">
                                <div className="flex gap-1">
                                    <div className="w-2 h-2 bg-[var(--accent-primary)] rounded-full typing-dot" />
                                    <div className="w-2 h-2 bg-[var(--accent-primary)] rounded-full typing-dot" />
                                    <div className="w-2 h-2 bg-[var(--accent-primary)] rounded-full typing-dot" />
                                </div>
                                <span className="text-sm">Processing your response...</span>
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {/* Audio controls */}
                    {!sessionEnded && (
                        <div className="p-6 border-t border-[var(--glass-border)]">
                            <div className="flex flex-col items-center gap-4">
                                {/* Audio visualizer */}
                                <AudioVisualizer isActive={isRecording || isAISpeaking} />

                                {/* Record button */}
                                <button
                                    onClick={toggleRecording}
                                    disabled={isProcessing || isAISpeaking}
                                    className={`relative w-20 h-20 rounded-full transition-all ${isRecording
                                            ? 'bg-red-500 glow-error'
                                            : 'bg-gradient-to-br from-indigo-500 to-purple-600 glow-primary'
                                        } ${(isProcessing || isAISpeaking) ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105'}`}
                                >
                                    {isRecording && (
                                        <div className="absolute inset-0 rounded-full bg-red-500 pulse-ring" />
                                    )}
                                    <div className="relative flex items-center justify-center w-full h-full">
                                        {isRecording ? (
                                            <div className="w-6 h-6 bg-white rounded" />
                                        ) : (
                                            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                                                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                                                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                                            </svg>
                                        )}
                                    </div>
                                </button>

                                <p className="text-sm text-[var(--text-muted)]">
                                    {isRecording ? 'Recording... Click to stop' : isAISpeaking ? 'AI is speaking...' : 'Click to speak'}
                                </p>
                            </div>
                        </div>
                    )}
                </div>

                {/* Score panel (shows after session ends) */}
                {sessionEnded && score && (
                    <div className="w-96 border-l border-[var(--glass-border)] p-6 overflow-y-auto">
                        <ScoreCard score={score} />

                        <div className="mt-6 space-y-3">
                            <button
                                onClick={() => router.push('/dashboard')}
                                className="btn-primary w-full"
                            >
                                View Dashboard
                            </button>
                            <button
                                onClick={() => window.location.reload()}
                                className="btn-secondary w-full"
                            >
                                New Session
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
