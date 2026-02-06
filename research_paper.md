# Research Paper: Personalized AI-Driven Viva Examination

**Title:** Real-Time Personalized Academic Assessment: Integrating Voice Cloning and Retrieval-Augmented Generation for Automated Viva Examinations  
**Author:** Anant Vardhan Pandey (NexusCode)  
**Date:** February 2026

---

## Abstract

Traditional academic viva examinations (oral exams) are often subject to interviewer bias, lack of consistency, and significant time constraints for faculty. This paper proposes a novel framework for an automated AI-driven viva platform that simulates a specific educator's intellectual and vocal persona. By integrating **Retrieval-Augmented Generation (RAG)** for domain-specific knowledge grounding and **Cross-Language Text-To-Speech (XTTS)** for high-fidelity voice cloning, the system provides a realistic, low-latency, and personalized interview experience. Furthermore, we implement a multi-parametric evaluation engine that analyzes both semantic accuracy and behavioral confidence to provide objective academic scoring.

## 1. Introduction

The oral examination remains a cornerstone of academic evaluation, particularly in technical fields like Data Structures and Algorithms (DSA). However, scaling this process for large student cohorts is challenging. Current AI solutions often lack the "human touch" and domain depth required for rigorous academic assessment. This project aims to bridge the gap by creating a digital twin of a professor capable of:

1. Conducting natural voice-to-voice technical interviews.
2. Maintaining a specific persona and pedagogical style.
3. Automatically grading students based on faculty-defined rubrics.

## 2. Technical Methodology

### 2.1 System Architecture

The architecture follows a modular piped-line approach to minimize latency, ensuring an end-to-end response time of less than 2.0 seconds.

#### 2.1.1 Speech Acquisition and Transcription (STT)

We utilize **faster-whisper**, a quantized C++ implementation of OpenAI's Whisper model. This enables real-time transcription of student responses with high noise immunity.

#### 2.1.2 Knowledge Grounding (RAG)

To prevent hallucinations common in generic LLMs, we implement **RAG** using **ChromaDB** as a vector store. Domain-specific documents (lecture notes, textbooks) are broken into semantic chunks and embedded using `all-MiniLM-L6-v2`. This ensures that the AI's follow-up questions and evaluations are strictly grounded in the professor’s curriculum.

#### 2.1.3 Linguistic Intelligence (LLM)

A local deployment of **Mistral 7B** or **LLaMA 3 8B** (via Ollama) serves as the core reasoning engine. A custom "Persona Module" is injected via system prompting to mirror the professor's specific questioning style and rigor.

#### 2.1.4 Personalized Synthesis (TTS)

We employ **XTTS v2** for voice synthesis. By processing a 2-3 minute audio sample of the target professor, the model extracts acoustic characteristics to generate natural-sounding responses in the professor’s actual voice.

### 2.2 Evaluation Engine

The system employs a dual-model scoring approach:

- **Semantic Accuracy (BERT/DeBERTa):** Analyzes the student's transcript against a gold-standard knowledge base to assign a technical score (0-10).
- **Behavioral Confidence (Wav2Vec 2.0):** Analyzes audio features such as speaking rate, pause frequency, and filler word count to measure student confidence.

## 3. Implementation Details

The platform is built using a "Technically Savage" stack:

- **Backend:** FastAPI (Python) for asynchronous orchestration.
- **Frontend:** Next.js 15 for a premium, low-latency UI.
- **Real-time Comms:** WebSockets for full-duplex audio streaming.
- **Environment:** Multi-stage Docker containers with NVIDIA GPU acceleration.

## 4. Challenges and Latency Optimization

The primary technical challenge is the **Inference Bottleneck**. To solve this, we implement:

1. **Audio Chunking:** TTS generation starts as soon as the first sentence is produced by the LLM.
2. **Model Quantization:** Running LLMs and STT models in INT8 format to reduce memory footprint and increase speed.
3. **GPU Offloading:** Distributing VRAM usage across multiple local GPUs using Docker resources.

## 5. Potential Impact

This platform democratizes high-quality interview preparation for students while providing faculty with a scalable tool for preliminary assessments. The integration of a specific professor's voice and thinking style increases student engagement and reduces the "AI friction" often found in automated systems.

## 6. Conclusion and Future Work

We have demonstrated a framework for personalized academic assessment that is both technically rigorous and user-centric. Future work will focus on **multimodal analysis** (analyzing student facial expressions via webcam during the viva) and **fine-tuning** models on actual professor-student interaction datasets to further refine the persona.

---

## References

1. Vaswani, et al. "Attention is All You Need" - Transformer architecture foundation.
2. Lewis, et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks."
3. Radford, et al. "Robust Speech Recognition via Large-Scale Weak Supervision" (Whisper).
4. Coqui AI XTTS v2 Documentation.
