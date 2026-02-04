"""
Evaluation Service - ML model for scoring viva responses
"""

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class EvaluationScore:
    """Evaluation scores for a viva response"""
    technical_accuracy: float  # 0-10
    clarity: float  # 0-10
    depth: float  # 0-10
    confidence: float  # 0-10
    communication: float  # 0-10
    overall: float  # 0-10
    feedback: str


class EvalService:
    """
    Evaluation service for scoring student responses during viva.
    Uses fine-tuned BERT models for text analysis and audio features for confidence.
    """
    
    def __init__(
        self,
        model_name: str = "microsoft/deberta-v3-base"
    ):
        """
        Initialize the evaluation model.
        
        Args:
            model_name: Base model for fine-tuning/evaluation
        """
        self.model_name = model_name
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[AutoModelForSequenceClassification] = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Load the evaluation model"""
        print(f"📊 Loading evaluation model...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # For MVP, we'll use a zero-shot approach
        # In Phase 2, this will be fine-tuned on interview data
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=5  # Our 5 scoring dimensions
        )
        self.model.to(self.device)
        self.model.eval()
        
        print("✅ Evaluation model loaded!")
        
    def evaluate_response(
        self,
        question: str,
        student_response: str,
        expected_concepts: List[str] = None,
        audio_features: Dict = None
    ) -> EvaluationScore:
        """
        Evaluate a student's response.
        
        Args:
            question: The interviewer's question
            student_response: The student's transcribed answer
            expected_concepts: Key concepts expected in the answer
            audio_features: Features extracted from audio (hesitation, pace, etc.)
            
        Returns:
            EvaluationScore with detailed breakdown
        """
        # MVP: Rule-based + heuristic scoring
        # Will be replaced with ML model after collecting training data
        
        scores = self._heuristic_scoring(
            question=question,
            response=student_response,
            expected_concepts=expected_concepts or []
        )
        
        # Incorporate audio features if available
        if audio_features:
            scores["confidence"] = self._score_confidence(audio_features)
            
        # Calculate overall score
        overall = np.mean([
            scores["technical_accuracy"],
            scores["clarity"],
            scores["depth"],
            scores["confidence"],
            scores["communication"]
        ])
        
        # Generate feedback
        feedback = self._generate_feedback(scores)
        
        return EvaluationScore(
            technical_accuracy=scores["technical_accuracy"],
            clarity=scores["clarity"],
            depth=scores["depth"],
            confidence=scores["confidence"],
            communication=scores["communication"],
            overall=round(overall, 1),
            feedback=feedback
        )
        
    def _heuristic_scoring(
        self,
        question: str,
        response: str,
        expected_concepts: List[str]
    ) -> Dict[str, float]:
        """
        Heuristic-based scoring for MVP.
        Will be replaced with ML model.
        """
        scores = {
            "technical_accuracy": 5.0,
            "clarity": 5.0,
            "depth": 5.0,
            "confidence": 5.0,
            "communication": 5.0
        }
        
        response_lower = response.lower()
        words = response.split()
        
        # Technical accuracy: Check for expected concepts
        if expected_concepts:
            concept_matches = sum(
                1 for concept in expected_concepts 
                if concept.lower() in response_lower
            )
            scores["technical_accuracy"] = min(10, 5 + (concept_matches / len(expected_concepts)) * 5)
            
        # Clarity: Response length and structure
        if len(words) > 20:
            scores["clarity"] += 1
        if len(words) > 50:
            scores["clarity"] += 1
        if any(word in response_lower for word in ["first", "second", "finally", "therefore"]):
            scores["clarity"] += 1
        scores["clarity"] = min(10, scores["clarity"])
        
        # Depth: Mentions of complexity, edge cases, trade-offs
        depth_indicators = [
            "time complexity", "space complexity", "O(n)", "O(log n)",
            "edge case", "trade-off", "optimize", "however", "depends on"
        ]
        depth_matches = sum(1 for ind in depth_indicators if ind in response_lower)
        scores["depth"] = min(10, 5 + depth_matches)
        
        # Communication: Grammar and articulation (basic check)
        if response[0].isupper() and response[-1] in ".!?":
            scores["communication"] += 1
        if len(set(words)) / len(words) > 0.7:  # Vocabulary variety
            scores["communication"] += 1
        scores["communication"] = min(10, scores["communication"])
        
        return scores
    
    def _score_confidence(self, audio_features: Dict) -> float:
        """Score confidence based on audio features"""
        # Features expected: speaking_rate, pause_ratio, volume_consistency
        base_score = 5.0
        
        if "speaking_rate" in audio_features:
            # Optimal speaking rate is ~130-170 words per minute
            rate = audio_features["speaking_rate"]
            if 130 <= rate <= 170:
                base_score += 2
            elif 100 <= rate < 130 or 170 < rate <= 200:
                base_score += 1
                
        if "pause_ratio" in audio_features:
            # Some pauses are good (thinking), too many indicate uncertainty
            ratio = audio_features["pause_ratio"]
            if ratio < 0.2:
                base_score += 2
            elif ratio < 0.4:
                base_score += 1
            else:
                base_score -= 1
                
        return min(10, max(0, base_score))
    
    def _generate_feedback(self, scores: Dict[str, float]) -> str:
        """Generate constructive feedback based on scores"""
        feedback_parts = []
        
        if scores["technical_accuracy"] >= 7:
            feedback_parts.append("Good technical understanding demonstrated.")
        elif scores["technical_accuracy"] < 5:
            feedback_parts.append("Review the core concepts for better accuracy.")
            
        if scores["clarity"] >= 7:
            feedback_parts.append("Clear and well-structured explanation.")
        elif scores["clarity"] < 5:
            feedback_parts.append("Try to organize your answer more clearly.")
            
        if scores["depth"] >= 7:
            feedback_parts.append("Excellent depth with complexity analysis.")
        elif scores["depth"] < 5:
            feedback_parts.append("Consider discussing time/space complexity and edge cases.")
            
        if scores["confidence"] < 5:
            feedback_parts.append("Practice speaking at a steady pace.")
            
        return " ".join(feedback_parts)
    
    def evaluate_session(
        self,
        conversation_history: List[Dict[str, str]]
    ) -> EvaluationScore:
        """
        Evaluate an entire interview session.
        
        Args:
            conversation_history: List of {"question": ..., "response": ...} dicts
            
        Returns:
            Overall session evaluation
        """
        if not conversation_history:
            return EvaluationScore(0, 0, 0, 0, 0, 0, "No responses to evaluate")
            
        all_scores = []
        
        for exchange in conversation_history:
            score = self.evaluate_response(
                question=exchange.get("question", ""),
                student_response=exchange.get("response", "")
            )
            all_scores.append(score)
            
        # Average all scores
        avg_scores = {
            "technical_accuracy": np.mean([s.technical_accuracy for s in all_scores]),
            "clarity": np.mean([s.clarity for s in all_scores]),
            "depth": np.mean([s.depth for s in all_scores]),
            "confidence": np.mean([s.confidence for s in all_scores]),
            "communication": np.mean([s.communication for s in all_scores])
        }
        
        overall = np.mean(list(avg_scores.values()))
        
        return EvaluationScore(
            technical_accuracy=round(avg_scores["technical_accuracy"], 1),
            clarity=round(avg_scores["clarity"], 1),
            depth=round(avg_scores["depth"], 1),
            confidence=round(avg_scores["confidence"], 1),
            communication=round(avg_scores["communication"], 1),
            overall=round(overall, 1),
            feedback=self._generate_feedback(avg_scores)
        )
