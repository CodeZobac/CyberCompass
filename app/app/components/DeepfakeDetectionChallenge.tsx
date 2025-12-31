/**
 * DeepfakeDetectionChallenge Component
 * Interactive deepfake detection training interface
 * Requirements: 3.1, 3.2, 3.3, 3.4
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { useSession } from 'next-auth/react';
import { AriaLive, SROnly } from './ui/aria-live';

interface DeepfakeMedia {
  id: string;
  url: string;
  type: 'audio' | 'video' | 'image';
  isDeepfake: boolean;
  difficulty: number;
  detectionClues: string[];
}

interface DeepfakeFeedback {
  isCorrect: boolean;
  explanation: string;
  cluesRevealed: string[];
  technicalDetails: string[];
}

interface DeepfakeDetectionChallengeProps {
  locale?: string;
  userId?: string;
  onComplete?: (result: any) => void;
}

export function DeepfakeDetectionChallenge({
  locale = 'en',
  userId,
  onComplete,
}: DeepfakeDetectionChallengeProps) {
  const { data: session } = useSession();
  const [currentMedia, setCurrentMedia] = useState<DeepfakeMedia | null>(null);
  const [userDecision, setUserDecision] = useState<boolean | null>(null);
  const [feedback, setFeedback] = useState<DeepfakeFeedback | null>(null);
  const [loading, setLoading] = useState(false);
  const [showHints, setShowHints] = useState(false);
  const [challengeCount, setChallengeCount] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);

  const effectiveUserId = userId || session?.user?.email || 'anonymous';

  const messages = {
    en: {
      title: 'Deepfake Detection Challenge',
      description: 'Analyze the media content below and determine if it\'s authentic or a deepfake.',
      authentic: 'Authentic',
      deepfake: 'Deepfake',
      submit: 'Submit Decision',
      showHints: 'Show Hints',
      hideHints: 'Hide Hints',
      hints: 'Detection Hints',
      loading: 'Analyzing...',
      correct: 'Correct! Well Done!',
      incorrect: 'Incorrect - Learn from this',
      nextChallenge: 'Next Challenge',
      finish: 'Finish Training',
      score: 'Score',
      difficulty: 'Difficulty',
      technicalDetails: 'Technical Details',
      clues: 'Detection Clues',
    },
    pt: {
      title: 'Desafio de Detecção de Deepfake',
      description: 'Analise o conteúdo de mídia abaixo e determine se é autêntico ou um deepfake.',
      authentic: 'Autêntico',
      deepfake: 'Deepfake',
      submit: 'Enviar Decisão',
      showHints: 'Mostrar Dicas',
      hideHints: 'Ocultar Dicas',
      hints: 'Dicas de Detecção',
      loading: 'Analisando...',
      correct: 'Correto! Muito Bem!',
      incorrect: 'Incorreto - Aprenda com isso',
      nextChallenge: 'Próximo Desafio',
      finish: 'Finalizar Treinamento',
      score: 'Pontuação',
      difficulty: 'Dificuldade',
      technicalDetails: 'Detalhes Técnicos',
      clues: 'Pistas de Detecção',
    },
  };

  const t = messages[locale as keyof typeof messages] || messages.en;

  useEffect(() => {
    loadNextChallenge();
  }, []);

  const loadNextChallenge = async () => {
    setLoading(true);
    setUserDecision(null);
    setFeedback(null);
    setShowHints(false);

    try {
      // Call AI backend to get next deepfake challenge
      const response = await fetch('/api/ai-backend/deepfake-challenge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: effectiveUserId,
          locale,
          difficulty: Math.min(1 + Math.floor(challengeCount / 3), 3),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to load challenge');
      }

      const data = await response.json();
      setCurrentMedia(data.media);
    } catch (error) {
      console.error('Error loading challenge:', error);
      // Fallback to mock data for development
      setCurrentMedia({
        id: `mock-${Date.now()}`,
        url: '/placeholder-media.jpg',
        type: 'image',
        isDeepfake: Math.random() > 0.5,
        difficulty: 1,
        detectionClues: [
          'Check facial symmetry',
          'Look for unnatural lighting',
          'Examine edge artifacts',
        ],
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (userDecision === null || !currentMedia) return;

    setLoading(true);

    try {
      const response = await fetch('/api/ai-backend/deepfake-feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: effectiveUserId,
          mediaId: currentMedia.id,
          userDecision,
          correctAnswer: currentMedia.isDeepfake,
          locale,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get feedback');
      }

      const feedbackData = await response.json();
      setFeedback(feedbackData);

      const isCorrect = userDecision === currentMedia.isDeepfake;
      setChallengeCount(prev => prev + 1);
      if (isCorrect) {
        setCorrectCount(prev => prev + 1);
      }
    } catch (error) {
      console.error('Error submitting decision:', error);
      // Fallback feedback
      const isCorrect = userDecision === currentMedia.isDeepfake;
      setFeedback({
        isCorrect,
        explanation: isCorrect
          ? 'Great job! You correctly identified this media.'
          : 'This was actually ' + (currentMedia.isDeepfake ? 'a deepfake' : 'authentic') + '.',
        cluesRevealed: currentMedia.detectionClues,
        technicalDetails: ['AI backend integration pending'],
      });
      setChallengeCount(prev => prev + 1);
      if (isCorrect) {
        setCorrectCount(prev => prev + 1);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    if (challengeCount >= 5) {
      onComplete?.({
        totalChallenges: challengeCount,
        correctAnswers: correctCount,
        accuracy: (correctCount / challengeCount) * 100,
      });
    } else {
      loadNextChallenge();
    }
  };

  const getDifficultyLabel = (difficulty: number) => {
    const labels = { 1: 'EASY', 2: 'MEDIUM', 3: 'HARD' };
    return labels[difficulty as keyof typeof labels] || 'UNKNOWN';
  };

  const getDifficultyColor = (difficulty: number) => {
    const colors = {
      1: 'bg-green-600',
      2: 'bg-yellow-600',
      3: 'bg-red-600',
    };
    return colors[difficulty as keyof typeof colors] || 'bg-gray-600';
  };

  if (!currentMedia) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-black mx-auto mb-4"></div>
          <p className="font-bold uppercase">{t.loading}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto px-4 sm:px-0">
      {/* ARIA Live Region for Score Updates */}
      <AriaLive 
        message={feedback ? (feedback.isCorrect ? t.correct : t.incorrect) : ''} 
        politeness="assertive" 
      />
      
      {/* Header with Score */}
      <div className="mb-4 sm:mb-6 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 sm:gap-0">
        <div 
          className="bg-white border-2 sm:border-4 border-black p-3 sm:p-4 shadow-[4px_4px_0_0_#000] text-center sm:text-left"
          role="status"
          aria-label={`${t.score}: ${correctCount} out of ${challengeCount}`}
        >
          <span className="font-bold uppercase tracking-wider text-sm sm:text-base">
            {t.score}: {correctCount}/{challengeCount}
          </span>
        </div>
        <div 
          className={`${getDifficultyColor(currentMedia.difficulty)} text-white px-4 sm:px-6 py-2 sm:py-3 border-2 sm:border-4 border-black font-black uppercase shadow-[4px_4px_0_0_#000] text-center text-sm sm:text-base`}
          role="status"
          aria-label={`${t.difficulty}: ${getDifficultyLabel(currentMedia.difficulty)}`}
        >
          {t.difficulty}: {getDifficultyLabel(currentMedia.difficulty)}
        </div>
      </div>

      <Card className="shadow-[6px_6px_0_0_#000] sm:shadow-[8px_8px_0_0_#000]" role="article" aria-labelledby="challenge-title">
        <CardHeader>
          <CardTitle id="challenge-title" className="text-red-500 text-xl sm:text-2xl">{t.title}</CardTitle>
          <p className="text-gray-700 font-semibold mt-2 text-sm sm:text-base">{t.description}</p>
        </CardHeader>

        <CardContent>
          {/* Media Display */}
          <figure className="mb-4 sm:mb-6 border-2 sm:border-4 border-black bg-gray-100 aspect-video flex items-center justify-center">
            {currentMedia.type === 'image' && (
              <img
                src={currentMedia.url}
                alt={`Media content for deepfake detection challenge. Analyze this ${currentMedia.type} to determine if it is authentic or a deepfake.`}
                className="w-full h-full object-contain"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%23ddd" width="400" height="300"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" text-anchor="middle" dy=".3em"%3EMedia Content%3C/text%3E%3C/svg%3E';
                }}
              />
            )}
            {currentMedia.type === 'video' && (
              <video
                src={currentMedia.url}
                controls
                className="w-full h-full"
                aria-label={`Video content for deepfake detection challenge. Analyze this video to determine if it is authentic or a deepfake.`}
              >
                <SROnly>Video player for deepfake detection challenge</SROnly>
              </video>
            )}
            {currentMedia.type === 'audio' && (
              <audio
                src={currentMedia.url}
                controls
                className="w-full"
                aria-label={`Audio content for deepfake detection challenge. Listen to this audio to determine if it is authentic or a deepfake.`}
              >
                <SROnly>Audio player for deepfake detection challenge</SROnly>
              </audio>
            )}
          </figure>

          {/* Hints Section */}
          {!feedback && (
            <section className="mb-4 sm:mb-6" aria-labelledby="hints-section">
              <Button
                onClick={() => setShowHints(!showHints)}
                variant="brutal-normal"
                className="mb-3 sm:mb-4 w-full sm:w-auto min-h-[44px]"
                aria-expanded={showHints}
                aria-controls="hints-content"
              >
                <span aria-hidden="true">💡</span> {showHints ? t.hideHints : t.showHints}
              </Button>

              {showHints && (
                <div 
                  id="hints-content"
                  className="bg-yellow-100 border-2 sm:border-4 border-yellow-500 p-3 sm:p-4"
                  role="region"
                  aria-live="polite"
                >
                  <h4 id="hints-section" className="font-black uppercase mb-2 text-sm sm:text-base">{t.hints}</h4>
                  <ul className="list-disc list-inside space-y-1" role="list">
                    {currentMedia.detectionClues.map((clue, idx) => (
                      <li key={idx} className="font-semibold text-sm sm:text-base" role="listitem">{clue}</li>
                    ))}
                  </ul>
                </div>
              )}
            </section>
          )}

          {/* Decision Buttons */}
          {!feedback && (
            <fieldset className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mb-4 sm:mb-6">
              <legend className="sr-only">Choose whether the media is authentic or a deepfake</legend>
              <button
                onClick={() => setUserDecision(false)}
                role="radio"
                aria-checked={userDecision === false}
                aria-label="Mark as authentic"
                className={`p-4 sm:p-6 border-2 sm:border-4 border-black font-black text-base sm:text-lg uppercase transition-all min-h-[44px] ${
                  userDecision === false
                    ? 'bg-green-500 text-white shadow-[6px_6px_0_0_#000] transform translate-x-1 translate-y-1'
                    : 'bg-white hover:bg-gray-50 shadow-[4px_4px_0_0_#000] hover:shadow-[6px_6px_0_0_#000]'
                }`}
              >
                <span aria-hidden="true">✓</span> {t.authentic}
              </button>
              <button
                onClick={() => setUserDecision(true)}
                role="radio"
                aria-checked={userDecision === true}
                aria-label="Mark as deepfake"
                className={`p-4 sm:p-6 border-2 sm:border-4 border-black font-black text-base sm:text-lg uppercase transition-all min-h-[44px] ${
                  userDecision === true
                    ? 'bg-red-500 text-white shadow-[6px_6px_0_0_#000] transform translate-x-1 translate-y-1'
                    : 'bg-white hover:bg-gray-50 shadow-[4px_4px_0_0_#000] hover:shadow-[6px_6px_0_0_#000]'
                }`}
              >
                <span aria-hidden="true">✗</span> {t.deepfake}
              </button>
            </fieldset>
          )}

          {/* Submit Button */}
          {!feedback && (
            <Button
              onClick={handleSubmit}
              disabled={userDecision === null || loading}
              variant="brutal"
              className="w-full"
            >
              {loading ? t.loading : t.submit}
            </Button>
          )}

          {/* Feedback Section */}
          {feedback && (
            <section className="space-y-3 sm:space-y-4" aria-labelledby="feedback-section" role="region" aria-live="polite">
              <div className={`p-3 sm:p-4 border-2 sm:border-4 border-black ${
                feedback.isCorrect ? 'bg-green-500' : 'bg-red-500'
              } text-white`} role="alert">
                <p className="font-black text-base sm:text-lg uppercase">
                  <span aria-hidden="true">{feedback.isCorrect ? '✓' : '✗'}</span> {feedback.isCorrect ? t.correct : t.incorrect}
                </p>
                <p className="font-semibold mt-2 text-sm sm:text-base">{feedback.explanation}</p>
              </div>

              {/* Detection Clues */}
              <aside className="bg-blue-100 border-2 sm:border-4 border-blue-500 p-3 sm:p-4" aria-labelledby="clues-heading">
                <h4 id="clues-heading" className="font-black uppercase mb-2 text-sm sm:text-base">
                  <span aria-hidden="true">🔍</span> {t.clues}
                </h4>
                <ul className="list-disc list-inside space-y-1" role="list">
                  {feedback.cluesRevealed.map((clue, idx) => (
                    <li key={idx} className="font-semibold text-sm sm:text-base" role="listitem">{clue}</li>
                  ))}
                </ul>
              </aside>

              {/* Technical Details */}
              {feedback.technicalDetails.length > 0 && (
                <aside className="bg-gray-100 border-2 sm:border-4 border-gray-500 p-3 sm:p-4" aria-labelledby="technical-heading">
                  <h4 id="technical-heading" className="font-black uppercase mb-2 text-sm sm:text-base">
                    <span aria-hidden="true">🔬</span> {t.technicalDetails}
                  </h4>
                  <ul className="list-disc list-inside space-y-1" role="list">
                    {feedback.technicalDetails.map((detail, idx) => (
                      <li key={idx} className="font-semibold text-xs sm:text-sm" role="listitem">{detail}</li>
                    ))}
                  </ul>
                </aside>
              )}

              {/* Next Button */}
              <Button
                onClick={handleNext}
                variant="brutal"
                className="w-full min-h-[44px]"
                aria-label={challengeCount >= 5 ? t.finish : t.nextChallenge}
              >
                {challengeCount >= 5 ? t.finish : t.nextChallenge}
              </Button>
            </section>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
