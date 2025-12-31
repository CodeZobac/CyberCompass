/**
 * SocialMediaSimulation Component
 * Interactive social media disinformation detection training
 * Requirements: 5.1, 5.2, 5.3, 5.4
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { useSession } from 'next-auth/react';

interface SocialMediaPost {
  id: string;
  author: {
    name: string;
    avatar: string;
    verified: boolean;
  };
  content: string;
  image?: string;
  timestamp: string;
  likes: number;
  shares: number;
  comments: number;
  isDisinformation: boolean;
  category: 'health' | 'politics' | 'conspiracy' | 'authentic';
  redFlags: string[];
}

interface PostInteraction {
  postId: string;
  action: 'like' | 'share' | 'report' | 'ignore';
  timestamp: Date;
}

interface SimulationFeedback {
  correctIdentifications: number;
  missedDisinformation: number;
  falsePositives: number;
  engagementImpact: string;
  recommendations: string[];
}

interface SocialMediaSimulationProps {
  locale?: string;
  userId?: string;
  onComplete?: (feedback: SimulationFeedback) => void;
}

export function SocialMediaSimulation({
  locale = 'en',
  userId,
  onComplete,
}: SocialMediaSimulationProps) {
  const { data: session } = useSession();
  const [posts, setPosts] = useState<SocialMediaPost[]>([]);
  const [interactions, setInteractions] = useState<PostInteraction[]>([]);
  const [loading, setLoading] = useState(false);
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedback, setFeedback] = useState<SimulationFeedback | null>(null);
  const [currentPostIndex, setCurrentPostIndex] = useState(0);
  
  // Touch/swipe state for mobile
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);

  const effectiveUserId = userId || session?.user?.email || 'anonymous';

  // Minimum swipe distance (in px)
  const minSwipeDistance = 50;

  const messages = {
    en: {
      title: 'Social Media Simulation',
      description: 'Navigate this simulated social media feed and identify disinformation.',
      like: 'Like',
      share: 'Share',
      report: 'Report',
      skip: 'Skip',
      loading: 'Loading feed...',
      endSimulation: 'End Simulation',
      viewResults: 'View Results',
      verified: 'Verified',
      hoursAgo: 'hours ago',
      minutesAgo: 'minutes ago',
      likes: 'likes',
      shares: 'shares',
      comments: 'comments',
      feedbackTitle: 'Simulation Results',
      correctIdentifications: 'Correct Identifications',
      missedDisinformation: 'Missed Disinformation',
      falsePositives: 'False Reports',
      engagementImpact: 'Engagement Impact',
      recommendations: 'Recommendations',
      tryAgain: 'Try Again',
    },
    pt: {
      title: 'Simulação de Mídia Social',
      description: 'Navegue por este feed simulado de mídia social e identifique desinformação.',
      like: 'Curtir',
      share: 'Compartilhar',
      report: 'Denunciar',
      skip: 'Pular',
      loading: 'Carregando feed...',
      endSimulation: 'Encerrar Simulação',
      viewResults: 'Ver Resultados',
      verified: 'Verificado',
      hoursAgo: 'horas atrás',
      minutesAgo: 'minutos atrás',
      likes: 'curtidas',
      shares: 'compartilhamentos',
      comments: 'comentários',
      feedbackTitle: 'Resultados da Simulação',
      correctIdentifications: 'Identificações Corretas',
      missedDisinformation: 'Desinformação Perdida',
      falsePositives: 'Denúncias Falsas',
      engagementImpact: 'Impacto do Engajamento',
      recommendations: 'Recomendações',
      tryAgain: 'Tentar Novamente',
    },
  };

  const t = messages[locale as keyof typeof messages] || messages.en;

  useEffect(() => {
    loadFeed();
  }, []);

  const loadFeed = async () => {
    setLoading(true);

    try {
      const response = await fetch('/api/ai-backend/social-media-feed', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: effectiveUserId,
          locale,
          postCount: 10,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to load feed');
      }

      const data = await response.json();
      setPosts(data.posts);
    } catch (error) {
      console.error('Error loading feed:', error);
      // Fallback to mock data
      setPosts(generateMockPosts());
    } finally {
      setLoading(false);
    }
  };

  const generateMockPosts = (): SocialMediaPost[] => {
    return [
      {
        id: '1',
        author: { name: 'Health News Daily', avatar: '👨‍⚕️', verified: false },
        content: 'BREAKING: New study shows miracle cure for all diseases! Doctors hate this one simple trick!',
        timestamp: '2 hours ago',
        likes: 15234,
        shares: 8932,
        comments: 456,
        isDisinformation: true,
        category: 'health',
        redFlags: ['Sensational claims', 'No credible source', 'Too good to be true'],
      },
      {
        id: '2',
        author: { name: 'Science Journal', avatar: '🔬', verified: true },
        content: 'New research published in Nature shows promising results in cancer treatment trials.',
        timestamp: '5 hours ago',
        likes: 3421,
        shares: 892,
        comments: 156,
        isDisinformation: false,
        category: 'authentic',
        redFlags: [],
      },
    ];
  };

  const handleInteraction = async (postId: string, action: 'like' | 'share' | 'report' | 'ignore') => {
    const interaction: PostInteraction = {
      postId,
      action,
      timestamp: new Date(),
    };

    setInteractions(prev => [...prev, interaction]);

    // Move to next post
    if (currentPostIndex < posts.length - 1) {
      setCurrentPostIndex(prev => prev + 1);
    } else {
      // End simulation
      await endSimulation();
    }
  };

  // Touch handlers for swipe gestures on mobile
  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe) {
      // Swipe left = Skip to next post
      handleInteraction(currentPost.id, 'ignore');
    }
    // Right swipe could be used for going back, but we'll keep it simple for now
  };

  const endSimulation = async () => {
    setLoading(true);

    try {
      const response = await fetch('/api/ai-backend/social-media-feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: effectiveUserId,
          posts,
          interactions,
          locale,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get feedback');
      }

      const feedbackData = await response.json();
      setFeedback(feedbackData);
    } catch (error) {
      console.error('Error getting feedback:', error);
      // Generate fallback feedback
      const correctReports = interactions.filter(
        i => i.action === 'report' && posts.find(p => p.id === i.postId)?.isDisinformation
      ).length;
      const missedDisinfo = posts.filter(
        p => p.isDisinformation && !interactions.find(i => i.postId === p.id && i.action === 'report')
      ).length;
      const falseReports = interactions.filter(
        i => i.action === 'report' && !posts.find(p => p.id === i.postId)?.isDisinformation
      ).length;

      setFeedback({
        correctIdentifications: correctReports,
        missedDisinformation: missedDisinfo,
        falsePositives: falseReports,
        engagementImpact: 'Your engagement patterns show room for improvement.',
        recommendations: [
          'Look for credible sources',
          'Check for verification badges',
          'Be skeptical of sensational claims',
        ],
      });
    } finally {
      setLoading(false);
      setShowFeedback(true);
    }
  };

  const currentPost = posts[currentPostIndex];

  if (loading && posts.length === 0) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-black mx-auto mb-4"></div>
          <p className="font-bold uppercase">{t.loading}</p>
        </div>
      </div>
    );
  }

  if (showFeedback && feedback) {
    const totalPosts = posts.length;
    const accuracy = totalPosts > 0 
      ? Math.round((feedback.correctIdentifications / totalPosts) * 100) 
      : 0;

    return (
      <div className="w-full max-w-4xl mx-auto animate-[fadeIn_400ms_ease-out]">
        {/* Results Header */}
        <div className="text-center mb-8">
          <h2 className="text-5xl sm:text-6xl font-black uppercase text-blue-500 mb-4 drop-shadow-[4px_4px_0_rgba(0,0,0,1)]">
            📊 {t.feedbackTitle}
          </h2>
          <p className="text-xl font-semibold text-gray-700">
            {locale === 'pt' 
              ? 'Veja como você se saiu na simulação' 
              : 'See how you performed in the simulation'}
          </p>
        </div>

        <Card className="shadow-[8px_8px_0_0_#000] border-4 border-black">
          <CardContent className="p-8">
            <div className="space-y-8">
              {/* Stats Cards (correct, missed, false positives) */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6">
                <div className="bg-green-100 border-2 sm:border-4 border-green-500 p-4 sm:p-6 text-center shadow-[4px_4px_0_0_#000] hover:shadow-[6px_6px_0_0_#000] transition-all">
                  <div className="text-4xl sm:text-5xl font-black text-green-700 mb-2">
                    {feedback.correctIdentifications}
                  </div>
                  <div className="text-xs font-black uppercase text-green-800 mb-1">
                    {t.correctIdentifications}
                  </div>
                  <div className="text-xl sm:text-2xl">✓</div>
                </div>
                <div className="bg-red-100 border-2 sm:border-4 border-red-500 p-4 sm:p-6 text-center shadow-[4px_4px_0_0_#000] hover:shadow-[6px_6px_0_0_#000] transition-all">
                  <div className="text-4xl sm:text-5xl font-black text-red-700 mb-2">
                    {feedback.missedDisinformation}
                  </div>
                  <div className="text-xs font-black uppercase text-red-800 mb-1">
                    {t.missedDisinformation}
                  </div>
                  <div className="text-xl sm:text-2xl">✗</div>
                </div>
                <div className="bg-yellow-100 border-2 sm:border-4 border-yellow-500 p-4 sm:p-6 text-center shadow-[4px_4px_0_0_#000] hover:shadow-[6px_6px_0_0_#000] transition-all">
                  <div className="text-4xl sm:text-5xl font-black text-yellow-700 mb-2">
                    {feedback.falsePositives}
                  </div>
                  <div className="text-xs font-black uppercase text-yellow-800 mb-1">
                    {t.falsePositives}
                  </div>
                  <div className="text-xl sm:text-2xl">⚠️</div>
                </div>
              </div>

              {/* Data Visualization - Accuracy Bar */}
              <div className="bg-white border-4 border-black p-6 shadow-[4px_4px_0_0_#000]">
                <h4 className="font-black uppercase mb-4 text-lg">
                  {locale === 'pt' ? 'Taxa de Precisão' : 'Accuracy Rate'}
                </h4>
                <div className="relative">
                  <div className="w-full bg-gray-200 h-8 border-4 border-black">
                    <div
                      className={`h-full transition-all duration-1000 ease-out ${
                        accuracy >= 70 ? 'bg-green-500' : accuracy >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${accuracy}%` }}
                    />
                  </div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="font-black text-xl drop-shadow-[2px_2px_0_rgba(255,255,255,1)]">
                      {accuracy}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Engagement Impact Section */}
              <div className="bg-blue-100 border-4 border-blue-500 p-6 shadow-[4px_4px_0_0_#000]">
                <div className="flex items-start gap-3">
                  <span className="text-3xl">💡</span>
                  <div className="flex-1">
                    <h4 className="font-black uppercase mb-3 text-lg text-blue-900">
                      {t.engagementImpact}
                    </h4>
                    <p className="font-semibold text-blue-900 leading-relaxed">
                      {feedback.engagementImpact}
                    </p>
                  </div>
                </div>
              </div>

              {/* Recommendations List */}
              <div className="bg-purple-50 border-4 border-purple-500 p-6 shadow-[4px_4px_0_0_#000]">
                <div className="flex items-start gap-3 mb-4">
                  <span className="text-3xl">🎯</span>
                  <h4 className="font-black uppercase text-lg text-purple-900">
                    {t.recommendations}
                  </h4>
                </div>
                <ul className="space-y-3">
                  {feedback.recommendations.map((rec, idx) => (
                    <li 
                      key={idx} 
                      className="flex items-start gap-3 bg-white border-2 border-purple-300 p-3 shadow-[2px_2px_0_0_rgba(0,0,0,0.1)]"
                    >
                      <span className="text-purple-600 font-black text-lg">•</span>
                      <span className="font-semibold text-gray-800 flex-1">{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Try Again and Detailed Analysis Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <button
                  onClick={() => {
                    setShowFeedback(false);
                    setInteractions([]);
                    setCurrentPostIndex(0);
                    loadFeed();
                  }}
                  className="flex-1 p-4 bg-blue-500 text-white border-4 border-black font-black uppercase text-lg hover:bg-blue-600 shadow-[4px_4px_0_0_#000] hover:shadow-[2px_2px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] transition-all duration-150"
                >
                  🔄 {t.tryAgain}
                </button>
                <button
                  onClick={() => onComplete?.(feedback)}
                  className="flex-1 p-4 bg-white border-4 border-black font-black uppercase text-lg hover:bg-gray-50 shadow-[4px_4px_0_0_#000] hover:shadow-[2px_2px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] transition-all duration-150"
                >
                  📈 {locale === 'pt' ? 'Análise Detalhada' : 'Detailed Analysis'}
                </button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Add keyframe animation */}
        <style jsx>{`
          @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
          }
        `}</style>
      </div>
    );
  }

  if (!currentPost) {
    return null;
  }

  return (
    <div className="w-full max-w-2xl mx-auto px-4 sm:px-0">
      {/* Progress Indicator */}
      <div className="mb-4 sm:mb-6 bg-white border-2 sm:border-4 border-black p-3 sm:p-4 shadow-[4px_4px_0_0_#000]">
        <div className="flex items-center justify-between mb-3">
          <span className="font-black uppercase text-sm">
            Post {currentPostIndex + 1} of {posts.length}
          </span>
          <button
            onClick={endSimulation}
            className="px-4 py-2 bg-gray-300 border-4 border-black font-black uppercase text-xs hover:bg-gray-400 shadow-[2px_2px_0_0_#000] hover:shadow-[1px_1px_0_0_#000] transition-all"
          >
            {t.endSimulation}
          </button>
        </div>
        <div className="w-full bg-gray-200 h-3 border-2 border-black">
          <div
            className="bg-blue-500 h-full transition-all duration-500 ease-out"
            style={{ width: `${((currentPostIndex + 1) / posts.length) * 100}%` }}
          />
        </div>
        <div className="mt-2 text-xs font-bold text-gray-600 text-right">
          {Math.round(((currentPostIndex + 1) / posts.length) * 100)}% Complete
        </div>
      </div>

      {/* Social Media Post Card with smooth transitions and swipe support */}
      <div 
        key={currentPost.id}
        className="animate-[slideIn_300ms_ease-out]"
        style={{
          animation: 'slideIn 300ms ease-out'
        }}
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
      >
        <Card className="shadow-[8px_8px_0_0_#000] hover:shadow-[12px_12px_0_0_#000] transition-all duration-200 touch-pan-y">
          {/* Post Header with author profile */}
          <div className="p-5 border-b-4 border-black flex items-center gap-4 bg-gray-50">
            <div className="w-14 h-14 flex items-center justify-center text-4xl bg-white border-4 border-black shadow-[2px_2px_0_0_#000]">
              {currentPost.author.avatar}
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="font-black text-lg">{currentPost.author.name}</span>
                {/* Verification badge */}
                {currentPost.author.verified && (
                  <span className="bg-blue-500 text-white text-xs px-2 py-1 font-black border-2 border-black shadow-[2px_2px_0_0_#000]">
                    ✓ {t.verified}
                  </span>
                )}
                {!currentPost.author.verified && (
                  <span className="bg-gray-300 text-gray-700 text-xs px-2 py-1 font-black border-2 border-black">
                    Not Verified
                  </span>
                )}
              </div>
              <span className="text-sm font-semibold text-gray-600">{currentPost.timestamp}</span>
            </div>
          </div>

          {/* Post Content */}
          <div className="p-6 bg-white">
            <p className="text-lg font-semibold mb-6 leading-relaxed">{currentPost.content}</p>
            {currentPost.image && (
              <div className="border-4 border-black mb-6 shadow-[4px_4px_0_0_#000]">
                <img
                  src={currentPost.image}
                  alt="Post content"
                  className="w-full"
                />
              </div>
            )}

            {/* Engagement Metrics Display */}
            <div className="flex gap-8 text-sm font-bold text-gray-700 mb-6 pb-6 border-b-4 border-gray-200">
              <div className="flex items-center gap-2">
                <span className="text-xl">❤️</span>
                <span>{currentPost.likes.toLocaleString()}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xl">🔄</span>
                <span>{currentPost.shares.toLocaleString()}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xl">💬</span>
                <span>{currentPost.comments.toLocaleString()}</span>
              </div>
            </div>

            {/* Action Buttons Grid (2x2) - Optimized touch targets for mobile (min 44x44px) */}
            <div className="grid grid-cols-2 gap-3 sm:gap-4">
              <button
                onClick={() => handleInteraction(currentPost.id, 'like')}
                className="min-h-[44px] p-3 sm:p-4 bg-white border-4 border-black font-black uppercase text-xs sm:text-sm hover:bg-gray-50 shadow-[4px_4px_0_0_#000] hover:shadow-[2px_2px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] transition-all duration-150 active:shadow-none active:translate-x-[4px] active:translate-y-[4px] touch-manipulation"
              >
                <span className="text-xl mr-1 sm:mr-2">❤️</span>
                <span className="hidden xs:inline">{t.like}</span>
              </button>
              <button
                onClick={() => handleInteraction(currentPost.id, 'share')}
                className="min-h-[44px] p-3 sm:p-4 bg-white border-4 border-black font-black uppercase text-xs sm:text-sm hover:bg-gray-50 shadow-[4px_4px_0_0_#000] hover:shadow-[2px_2px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] transition-all duration-150 active:shadow-none active:translate-x-[4px] active:translate-y-[4px] touch-manipulation"
              >
                <span className="text-xl mr-1 sm:mr-2">🔄</span>
                <span className="hidden xs:inline">{t.share}</span>
              </button>
              <button
                onClick={() => handleInteraction(currentPost.id, 'report')}
                className="min-h-[44px] p-3 sm:p-4 bg-red-500 text-white border-4 border-black font-black uppercase text-xs sm:text-sm hover:bg-red-600 shadow-[4px_4px_0_0_#000] hover:shadow-[2px_2px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] transition-all duration-150 active:shadow-none active:translate-x-[4px] active:translate-y-[4px] touch-manipulation"
              >
                <span className="text-xl mr-1 sm:mr-2">🚩</span>
                <span className="hidden xs:inline">{t.report}</span>
              </button>
              <button
                onClick={() => handleInteraction(currentPost.id, 'ignore')}
                className="min-h-[44px] p-3 sm:p-4 bg-gray-300 border-4 border-black font-black uppercase text-xs sm:text-sm hover:bg-gray-400 shadow-[4px_4px_0_0_#000] hover:shadow-[2px_2px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] transition-all duration-150 active:shadow-none active:translate-x-[4px] active:translate-y-[4px] touch-manipulation"
              >
                <span className="text-xl mr-1 sm:mr-2">⏭️</span>
                <span className="hidden xs:inline">{t.skip}</span>
              </button>
            </div>
            
            {/* Swipe hint for mobile */}
            <div className="mt-4 text-center text-xs font-semibold text-gray-500 sm:hidden">
              💡 {locale === 'pt' ? 'Dica: Deslize para a esquerda para pular' : 'Tip: Swipe left to skip'}
            </div>
          </div>
        </Card>
      </div>

      {/* Add keyframe animation */}
      <style jsx>{`
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}
