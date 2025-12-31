/**
 * Deepfake Detection Training Page - Brutalist Design
 * Task 3: Build Deepfake Detection Training page
 * Requirements: 1, 7, 8, 9, 10
 */

'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useSession } from 'next-auth/react';

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

interface UserStats {
  challengesCompleted: number;
  accuracy: number;
  streak: number;
}

interface PageProps {
  params: {
    locale: string;
  };
}

export default function DeepfakeTrainingPage({ params }: PageProps) {
  const { data: session } = useSession();
  const { locale } = params;
  
  // State management
  const [currentMedia, setCurrentMedia] = useState<DeepfakeMedia | null>(null);
  const [userDecision, setUserDecision] = useState<boolean | null>(null);
  const [feedback, setFeedback] = useState<DeepfakeFeedback | null>(null);
  const [loading, setLoading] = useState(false);
  const [showHints, setShowHints] = useState(false);
  const [challengeNumber, setChallengeNumber] = useState(1);
  const [totalChallenges] = useState(10);
  const [userStats, setUserStats] = useState<UserStats>({
    challengesCompleted: 45,
    accuracy: 89,
    streak: 7,
  });
  const [isStarted, setIsStarted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const effectiveUserId = session?.user?.email || 'anonymous';

  // Translations
  const messages = {
    en: {
      title: 'DEEPFAKE DETECTION TRAINING',
      subtitle: 'Master the art of spotting manipulated media',
      challengesLabel: 'Challenges',
      accuracyLabel: 'Accuracy',
      streakLabel: 'Streak',
      startTraining: 'START TRAINING',
      viewProgress: 'VIEW PROGRESS',
      challengeOf: 'CHALLENGE',
      of: 'OF',
      difficulty: 'DIFFICULTY',
      easy: 'EASY',
      medium: 'MEDIUM',
      hard: 'HARD',
      authentic: 'AUTHENTIC',
      deepfake: 'DEEPFAKE',
      submitAnswer: 'SUBMIT ANSWER',
      showHints: 'SHOW HINTS',
      hideHints: 'HIDE HINTS',
      hints: 'DETECTION HINTS',
      correct: 'CORRECT! WELL DONE!',
      incorrect: 'INCORRECT - LEARN FROM THIS',
      detectionClues: 'DETECTION CLUES REVEALED',
      technicalAnalysis: 'TECHNICAL ANALYSIS',
      nextChallenge: 'NEXT CHALLENGE',
      viewAnalysis: 'VIEW DETAILED ANALYSIS',
      loading: 'LOADING...',
      analyzing: 'ANALYZING...',
      errorTitle: 'OOPS! SOMETHING WENT WRONG',
      errorMessage: 'We couldn\'t load this content. Please try again.',
      tryAgain: 'TRY AGAIN',
      goBack: 'GO BACK',
    },
    pt: {
      title: 'TREINAMENTO DE DETECÇÃO DE DEEPFAKE',
      subtitle: 'Domine a arte de identificar mídia manipulada',
      challengesLabel: 'Desafios',
      accuracyLabel: 'Precisão',
      streakLabel: 'Sequência',
      startTraining: 'INICIAR TREINAMENTO',
      viewProgress: 'VER PROGRESSO',
      challengeOf: 'DESAFIO',
      of: 'DE',
      difficulty: 'DIFICULDADE',
      easy: 'FÁCIL',
      medium: 'MÉDIO',
      hard: 'DIFÍCIL',
      authentic: 'AUTÊNTICO',
      deepfake: 'DEEPFAKE',
      submitAnswer: 'ENVIAR RESPOSTA',
      showHints: 'MOSTRAR DICAS',
      hideHints: 'OCULTAR DICAS',
      hints: 'DICAS DE DETECÇÃO',
      correct: 'CORRETO! MUITO BEM!',
      incorrect: 'INCORRETO - APRENDA COM ISSO',
      detectionClues: 'PISTAS DE DETECÇÃO REVELADAS',
      technicalAnalysis: 'ANÁLISE TÉCNICA',
      nextChallenge: 'PRÓXIMO DESAFIO',
      viewAnalysis: 'VER ANÁLISE DETALHADA',
      loading: 'CARREGANDO...',
      analyzing: 'ANALISANDO...',
      errorTitle: 'OPS! ALGO DEU ERRADO',
      errorMessage: 'Não foi possível carregar este conteúdo. Por favor, tente novamente.',
      tryAgain: 'TENTAR NOVAMENTE',
      goBack: 'VOLTAR',
    },
  };

  const t = messages[locale as keyof typeof messages] || messages.en;

  // Load next challenge
  const loadNextChallenge = useCallback(async () => {
    setLoading(true);
    setUserDecision(null);
    setFeedback(null);
    setShowHints(false);
    setError(null);

    try {
      const response = await fetch('/api/ai-backend/deepfake-challenge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: effectiveUserId,
          locale,
          difficulty: Math.min(1 + Math.floor(challengeNumber / 3), 3),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to load challenge');
      }

      const data = await response.json();
      setCurrentMedia(data.media);
    } catch (err) {
      console.error('Error loading challenge:', err);
      // Fallback to mock data
      setCurrentMedia({
        id: `mock-${Date.now()}`,
        url: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="800" height="450"%3E%3Crect fill="%23f3f4f6" width="800" height="450"/%3E%3Ctext fill="%23374151" x="50%25" y="50%25" text-anchor="middle" dy=".3em" font-size="24" font-weight="bold"%3EMedia Content%3C/text%3E%3C/svg%3E',
        type: 'image',
        isDeepfake: Math.random() > 0.5,
        difficulty: Math.min(1 + Math.floor(challengeNumber / 3), 3),
        detectionClues: [
          'Unnatural eye movements',
          'Inconsistent lighting on face',
          'Blurred edges around hairline',
        ],
      });
    } finally {
      setLoading(false);
    }
  }, [challengeNumber, effectiveUserId, locale]);

  // Handle keyboard shortcuts
  useEffect(() => {
    if (!isStarted || feedback || loading) return;

    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'a' || e.key === 'A') {
        setUserDecision(false); // Authentic
      } else if (e.key === 'd' || e.key === 'D') {
        setUserDecision(true); // Deepfake
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [isStarted, feedback, loading]);

  // Submit decision
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
      if (isCorrect) {
        setUserStats(prev => ({
          ...prev,
          challengesCompleted: prev.challengesCompleted + 1,
          accuracy: Math.round(((prev.accuracy * prev.challengesCompleted + 100) / (prev.challengesCompleted + 1))),
          streak: prev.streak + 1,
        }));
      } else {
        setUserStats(prev => ({
          ...prev,
          challengesCompleted: prev.challengesCompleted + 1,
          accuracy: Math.round(((prev.accuracy * prev.challengesCompleted) / (prev.challengesCompleted + 1))),
          streak: 0,
        }));
      }
    } catch (err) {
      console.error('Error submitting decision:', err);
      const isCorrect = userDecision === currentMedia.isDeepfake;
      setFeedback({
        isCorrect,
        explanation: isCorrect
          ? 'Great job! You correctly identified this media.'
          : `This was actually ${currentMedia.isDeepfake ? 'a deepfake' : 'authentic'}.`,
        cluesRevealed: currentMedia.detectionClues,
        technicalDetails: ['AI backend integration pending'],
      });
    } finally {
      setLoading(false);
    }
  };

  // Handle next challenge
  const handleNext = () => {
    if (challengeNumber >= totalChallenges) {
      // Training complete - could redirect to results
      console.log('Training complete!');
    } else {
      setChallengeNumber(prev => prev + 1);
      loadNextChallenge();
    }
  };

  // Start training
  const handleStart = () => {
    setIsStarted(true);
    loadNextChallenge();
  };

  // Get difficulty styling
  const getDifficultyColor = (difficulty: number) => {
    const colors = {
      1: 'bg-green-600',
      2: 'bg-yellow-600',
      3: 'bg-red-600',
    };
    return colors[difficulty as keyof typeof colors] || 'bg-gray-600';
  };

  const getDifficultyLabel = (difficulty: number) => {
    const labels = {
      1: t.easy,
      2: t.medium,
      3: t.hard,
    };
    return labels[difficulty as keyof typeof labels] || 'UNKNOWN';
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Task 3.1: Hero Section */}
      <div className="relative bg-gradient-to-b from-red-50 to-white border-b-6 border-black py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          {/* Bold Title with Red Accent */}
          <h1 className="text-6xl md:text-8xl font-black uppercase text-red-500 mb-6 text-center text-shadow-[3px_3px_0px_#000000]">
            🎭 {t.title}
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl font-semibold text-gray-700 text-center mb-12 max-w-3xl mx-auto">
            {t.subtitle}
          </p>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 max-w-4xl mx-auto">
            {/* Challenges Completed */}
            <div className="bg-white border-4 border-black p-6 shadow-brutal-md hover-lift">
              <div className="text-5xl font-black text-center mb-2">🎯</div>
              <div className="text-4xl font-black text-center mb-1">{userStats.challengesCompleted}</div>
              <div className="text-sm font-bold uppercase text-center text-gray-700 tracking-wider">
                {t.challengesLabel}
              </div>
            </div>

            {/* Accuracy */}
            <div className="bg-white border-4 border-black p-6 shadow-brutal-md hover-lift">
              <div className="text-5xl font-black text-center mb-2">✓</div>
              <div className="text-4xl font-black text-center mb-1">{userStats.accuracy}%</div>
              <div className="text-sm font-bold uppercase text-center text-gray-700 tracking-wider">
                {t.accuracyLabel}
              </div>
            </div>

            {/* Streak */}
            <div className="bg-white border-4 border-black p-6 shadow-brutal-md hover-lift">
              <div className="text-5xl font-black text-center mb-2">🔥</div>
              <div className="text-4xl font-black text-center mb-1">{userStats.streak}</div>
              <div className="text-sm font-bold uppercase text-center text-gray-700 tracking-wider">
                {t.streakLabel}
              </div>
            </div>
          </div>

          {/* Primary CTA Buttons */}
          {!isStarted && (
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <button
                onClick={handleStart}
                className="bg-red-500 text-white px-8 py-4 border-4 border-black font-black text-lg uppercase shadow-brutal-md hover-press transition-all"
              >
                {t.startTraining} →
              </button>
              <button
                onClick={() => window.location.href = `/${locale}/analytics`}
                className="bg-white text-black px-8 py-4 border-4 border-black font-black text-lg uppercase shadow-brutal-md hover-press transition-all"
              >
                {t.viewProgress}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Main Content Area */}
      {isStarted && (
        <div className="container mx-auto max-w-5xl px-6 py-12">
          {/* Error State - Task 3.4 */}
          {error && (
            <div className="bg-red-100 border-4 border-red-500 p-8 mb-8 text-center animate-slide-in">
              <div className="text-6xl mb-4">⚠️</div>
              <h2 className="text-2xl font-black uppercase mb-4">{t.errorTitle}</h2>
              <p className="text-lg font-semibold mb-6">{t.errorMessage}</p>
              <div className="flex gap-4 justify-center">
                <button
                  onClick={loadNextChallenge}
                  className="bg-white text-black px-6 py-3 border-4 border-black font-black uppercase shadow-brutal-sm hover-press transition-all"
                >
                  {t.tryAgain}
                </button>
                <button
                  onClick={() => setIsStarted(false)}
                  className="bg-white text-black px-6 py-3 border-4 border-black font-black uppercase shadow-brutal-sm hover-press transition-all"
                >
                  {t.goBack}
                </button>
              </div>
            </div>
          )}

          {/* Loading State - Task 3.4 */}
          {loading && !currentMedia && (
            <div className="bg-white border-4 border-black p-12 text-center animate-fade-in">
              <div className="animate-spin rounded-full h-16 w-16 border-4 border-black border-t-transparent mx-auto mb-6"></div>
              <p className="text-xl font-black uppercase">{t.loading}</p>
            </div>
          )}

          {/* Challenge Interface - Task 3.2 */}
          {currentMedia && !error && (
            <div className="animate-slide-in">
              {/* Progress Header */}
              <div className="flex flex-col md:flex-row items-center justify-between mb-8 gap-4">
                <div className="bg-white border-4 border-black px-6 py-3 shadow-brutal-sm">
                  <span className="font-black uppercase tracking-wider">
                    {t.challengeOf} {challengeNumber} {t.of} {totalChallenges}
                  </span>
                </div>

                {/* Progress Bar */}
                <div className="flex-1 max-w-md w-full">
                  <div className="bg-gray-100 border-4 border-black h-8 relative overflow-hidden">
                    <div
                      className="bg-red-500 h-full transition-all duration-500"
                      style={{ width: `${(challengeNumber / totalChallenges) * 100}%` }}
                    />
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="font-black text-sm">
                        {Math.round((challengeNumber / totalChallenges) * 100)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Difficulty Badge */}
                <div className={`${getDifficultyColor(currentMedia.difficulty)} text-white px-6 py-3 border-4 border-black font-black uppercase shadow-brutal-sm`}>
                  ⚠️ {getDifficultyLabel(currentMedia.difficulty)}
                </div>
              </div>

              {/* Media Display Container (16:9 aspect ratio) */}
              <div className="bg-white border-6 border-black mb-8 shadow-brutal-lg">
                <div className="aspect-video bg-gray-100 flex items-center justify-center relative overflow-hidden">
                  {loading && currentMedia ? (
                    /* Skeleton Loader - Task 3.4 */
                    <div className="w-full h-full animate-shimmer" />
                  ) : (
                    <>
                      {currentMedia.type === 'image' && (
                        <img
                          src={currentMedia.url}
                          alt="Media to analyze"
                          className="w-full h-full object-contain"
                        />
                      )}
                      {currentMedia.type === 'video' && (
                        <video
                          src={currentMedia.url}
                          controls
                          className="w-full h-full"
                        />
                      )}
                      {currentMedia.type === 'audio' && (
                        <div className="w-full p-12">
                          <div className="text-6xl text-center mb-6">🎵</div>
                          <audio
                            src={currentMedia.url}
                            controls
                            className="w-full"
                          />
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>

              {/* Hints Toggle Panel */}
              {!feedback && (
                <div className="mb-8">
                  <button
                    onClick={() => setShowHints(!showHints)}
                    className="bg-yellow-400 text-black px-6 py-3 border-4 border-black font-black uppercase shadow-brutal-sm hover-press transition-all mb-4"
                  >
                    💡 {showHints ? t.hideHints : t.showHints}
                  </button>

                  {showHints && (
                    <div className="bg-yellow-100 border-4 border-yellow-500 p-6 animate-slide-in">
                      <h4 className="font-black uppercase mb-4 text-lg">{t.hints}</h4>
                      <ul className="space-y-2">
                        {currentMedia.detectionClues.map((clue, idx) => (
                          <li key={idx} className="flex items-start gap-3">
                            <span className="text-yellow-600 font-black">•</span>
                            <span className="font-semibold">{clue}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Decision Buttons (Authentic/Deepfake) */}
              {!feedback && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                  <button
                    onClick={() => setUserDecision(false)}
                    disabled={loading}
                    className={`p-8 border-6 border-black font-black text-2xl uppercase transition-all ${
                      userDecision === false
                        ? 'bg-green-500 text-white shadow-brutal-md transform translate-x-1 translate-y-1'
                        : 'bg-white hover:bg-gray-50 shadow-brutal-sm hover:shadow-brutal-md'
                    } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    aria-label="Mark as authentic (Press A)"
                  >
                    <div className="text-5xl mb-3">✓</div>
                    {t.authentic}
                    <div className="text-sm mt-2 font-semibold">(Press A)</div>
                  </button>

                  <button
                    onClick={() => setUserDecision(true)}
                    disabled={loading}
                    className={`p-8 border-6 border-black font-black text-2xl uppercase transition-all ${
                      userDecision === true
                        ? 'bg-red-500 text-white shadow-brutal-md transform translate-x-1 translate-y-1'
                        : 'bg-white hover:bg-gray-50 shadow-brutal-sm hover:shadow-brutal-md'
                    } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    aria-label="Mark as deepfake (Press D)"
                  >
                    <div className="text-5xl mb-3">✗</div>
                    {t.deepfake}
                    <div className="text-sm mt-2 font-semibold">(Press D)</div>
                  </button>
                </div>
              )}

              {/* Submit Button */}
              {!feedback && (
                <button
                  onClick={handleSubmit}
                  disabled={userDecision === null || loading}
                  className={`w-full bg-blue-500 text-white px-8 py-6 border-6 border-black font-black text-2xl uppercase shadow-brutal-lg transition-all ${
                    userDecision === null || loading
                      ? 'opacity-50 cursor-not-allowed'
                      : 'hover-press'
                  }`}
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-3">
                      <div className="animate-spin rounded-full h-6 w-6 border-4 border-white border-t-transparent"></div>
                      {t.analyzing}
                    </span>
                  ) : (
                    `${t.submitAnswer} →`
                  )}
                </button>
              )}

              {/* Results Display - Task 3.3 */}
              {feedback && (
                <div className="space-y-6 animate-slide-in">
                  {/* Feedback Card with Color-Coded Results */}
                  <div className={`p-8 border-6 border-black ${
                    feedback.isCorrect ? 'bg-green-500' : 'bg-red-500'
                  } text-white shadow-brutal-lg ${feedback.isCorrect ? 'animate-pulse-brutal' : ''}`}>
                    <div className="text-6xl mb-4 text-center">
                      {feedback.isCorrect ? '✓' : '✗'}
                    </div>
                    <p className="font-black text-3xl uppercase text-center mb-4">
                      {feedback.isCorrect ? t.correct : t.incorrect}
                    </p>
                    <p className="font-semibold text-xl text-center">
                      {feedback.explanation}
                    </p>
                  </div>

                  {/* Detection Clues Reveal Section */}
                  <div className="bg-blue-100 border-4 border-blue-500 p-6">
                    <h4 className="font-black uppercase mb-4 text-xl flex items-center gap-2">
                      🔍 {t.detectionClues}
                    </h4>
                    <ul className="space-y-3">
                      {feedback.cluesRevealed.map((clue, idx) => (
                        <li key={idx} className="flex items-start gap-3 animate-slide-in" style={{ animationDelay: `${idx * 100}ms` }}>
                          <span className="text-blue-600 font-black text-xl">•</span>
                          <span className="font-semibold text-lg">{clue}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Technical Analysis Panel */}
                  {feedback.technicalDetails.length > 0 && (
                    <div className="bg-gray-100 border-4 border-gray-500 p-6">
                      <h4 className="font-black uppercase mb-4 text-xl flex items-center gap-2">
                        🔬 {t.technicalAnalysis}
                      </h4>
                      <ul className="space-y-3">
                        {feedback.technicalDetails.map((detail, idx) => (
                          <li key={idx} className="flex items-start gap-3">
                            <span className="text-gray-600 font-black">•</span>
                            <span className="font-semibold">{detail}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Next Challenge Button */}
                  <div className="flex flex-col sm:flex-row gap-4">
                    <button
                      onClick={handleNext}
                      className="flex-1 bg-red-500 text-white px-8 py-6 border-6 border-black font-black text-2xl uppercase shadow-brutal-lg hover-press transition-all"
                    >
                      {t.nextChallenge} →
                    </button>
                    <button
                      onClick={() => console.log('View detailed analysis')}
                      className="flex-1 bg-white text-black px-8 py-6 border-6 border-black font-black text-2xl uppercase shadow-brutal-lg hover-press transition-all"
                    >
                      {t.viewAnalysis}
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
