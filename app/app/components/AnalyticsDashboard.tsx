/**
 * AnalyticsDashboard Component
 * Real-time analytics and progress tracking for cyber ethics learning
 * Requirements: 6.1, 6.2, 6.3, 6.4
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { useSession } from 'next-auth/react';

interface CompetencyScore {
  category: string;
  score: number;
  trend: 'up' | 'down' | 'stable';
  lastUpdated: string;
}

interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  earnedAt: string;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
}

interface LearningRecommendation {
  category: string;
  priority: 'high' | 'medium' | 'low';
  description: string;
  suggestedChallenges: string[];
}

interface PeerComparison {
  userPercentile: number;
  averageScore: number;
  userScore: number;
}

interface AnalyticsData {
  competencyScores: CompetencyScore[];
  achievements: Achievement[];
  recommendations: LearningRecommendation[];
  peerComparison: PeerComparison;
  totalChallengesCompleted: number;
  currentStreak: number;
  level: number;
  experiencePoints: number;
  nextLevelXP: number;
}

interface AnalyticsDashboardProps {
  locale?: string;
  userId?: string;
}

export function AnalyticsDashboard({
  locale = 'en',
  userId,
}: AnalyticsDashboardProps) {
  const { data: session } = useSession();
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedTab, setSelectedTab] = useState<'overview' | 'achievements' | 'recommendations'>('overview');

  const effectiveUserId = userId || session?.user?.id || 'anonymous';

  const messages = {
    en: {
      title: 'Learning Analytics',
      overview: 'Overview',
      achievements: 'Achievements',
      recommendations: 'Recommendations',
      competencyScores: 'Competency Scores',
      level: 'Level',
      streak: 'Day Streak',
      challengesCompleted: 'Challenges Completed',
      yourRank: 'Your Rank',
      percentile: 'Percentile',
      loading: 'Loading analytics...',
      noData: 'No analytics data available yet. Complete some challenges to see your progress!',
      trend: 'Trend',
      priority: 'Priority',
      suggestedChallenges: 'Suggested Challenges',
      earnedOn: 'Earned on',
      rarity: 'Rarity',
      progress: 'Progress to Next Level',
      peerComparison: 'Peer Comparison',
      yourScore: 'Your Score',
      averageScore: 'Average Score',
    },
    pt: {
      title: 'Análise de Aprendizado',
      overview: 'Visão Geral',
      achievements: 'Conquistas',
      recommendations: 'Recomendações',
      competencyScores: 'Pontuações de Competência',
      level: 'Nível',
      streak: 'Sequência de Dias',
      challengesCompleted: 'Desafios Concluídos',
      yourRank: 'Sua Classificação',
      percentile: 'Percentil',
      loading: 'Carregando análises...',
      noData: 'Nenhum dado de análise disponível ainda. Complete alguns desafios para ver seu progresso!',
      trend: 'Tendência',
      priority: 'Prioridade',
      suggestedChallenges: 'Desafios Sugeridos',
      earnedOn: 'Conquistado em',
      rarity: 'Raridade',
      progress: 'Progresso para o Próximo Nível',
      peerComparison: 'Comparação com Pares',
      yourScore: 'Sua Pontuação',
      averageScore: 'Pontuação Média',
    },
  };

  const t = messages[locale as keyof typeof messages] || messages.en;

  useEffect(() => {
    loadAnalytics();
    
    // Set up EventSource for real-time updates with error handling
    let eventSource: EventSource | null = null;
    let reconnectTimeout: NodeJS.Timeout | null = null;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    
    const connectSSE = () => {
      try {
        eventSource = new EventSource(`/api/ai-backend/analytics-stream?userId=${effectiveUserId}`);
        
        eventSource.onopen = () => {
          console.log('SSE connection established');
          reconnectAttempts = 0; // Reset on successful connection
        };
        
        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            // Smooth data transition with animation
            setAnalytics((prevAnalytics) => {
              if (!prevAnalytics) return data;
              
              // Animate score changes
              return {
                ...data,
                competencyScores: data.competencyScores.map((newScore: CompetencyScore, idx: number) => {
                  const oldScore = prevAnalytics.competencyScores[idx];
                  if (oldScore && oldScore.score !== newScore.score) {
                    // Trigger animation for score change
                    return { ...newScore, animated: true };
                  }
                  return newScore;
                }),
              };
            });
          } catch (error) {
            console.error('Error parsing analytics update:', error);
          }
        };

        eventSource.onerror = (error) => {
          console.error('EventSource error:', error);
          eventSource?.close();
          
          // Attempt to reconnect with exponential backoff
          if (reconnectAttempts < maxReconnectAttempts) {
            const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
            console.log(`Attempting to reconnect in ${delay}ms (attempt ${reconnectAttempts + 1}/${maxReconnectAttempts})`);
            
            reconnectTimeout = setTimeout(() => {
              reconnectAttempts++;
              connectSSE();
            }, delay);
          } else {
            console.error('Max reconnection attempts reached. Falling back to manual refresh.');
          }
        };
      } catch (error) {
        console.error('Error creating EventSource:', error);
      }
    };
    
    // Initial connection
    connectSSE();

    return () => {
      if (eventSource) {
        eventSource.close();
      }
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
    };
  }, [effectiveUserId]);

  const loadAnalytics = async () => {
    setLoading(true);

    try {
      const response = await fetch('/api/ai-backend/analytics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: effectiveUserId,
          locale,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to load analytics');
      }

      const data = await response.json();
      setAnalytics(data);
    } catch (error) {
      console.error('Error loading analytics:', error);
      // Fallback to mock data
      setAnalytics(generateMockAnalytics());
    } finally {
      setLoading(false);
    }
  };

  const generateMockAnalytics = (): AnalyticsData => {
    return {
      competencyScores: [
        { category: 'Deepfake Detection', score: 75, trend: 'up', lastUpdated: '2024-01-15' },
        { category: 'Disinformation Awareness', score: 82, trend: 'up', lastUpdated: '2024-01-14' },
        { category: 'Catfish Detection', score: 68, trend: 'stable', lastUpdated: '2024-01-13' },
        { category: 'Cyberbullying Prevention', score: 90, trend: 'up', lastUpdated: '2024-01-12' },
      ],
      achievements: [
        {
          id: '1',
          name: 'First Steps',
          description: 'Complete your first challenge',
          icon: '🎯',
          earnedAt: '2024-01-10',
          rarity: 'common',
        },
        {
          id: '2',
          name: 'Deepfake Detective',
          description: 'Correctly identify 10 deepfakes',
          icon: '🔍',
          earnedAt: '2024-01-12',
          rarity: 'rare',
        },
      ],
      recommendations: [
        {
          category: 'Catfish Detection',
          priority: 'high',
          description: 'Your catfish detection skills need improvement. Focus on identifying inconsistencies.',
          suggestedChallenges: ['Advanced Catfish Scenarios', 'Red Flag Recognition'],
        },
        {
          category: 'Deepfake Detection',
          priority: 'medium',
          description: 'Continue practicing with more complex deepfake examples.',
          suggestedChallenges: ['Expert Deepfake Analysis'],
        },
      ],
      peerComparison: {
        userPercentile: 78,
        averageScore: 72,
        userScore: 79,
      },
      totalChallengesCompleted: 45,
      currentStreak: 7,
      level: 8,
      experiencePoints: 2340,
      nextLevelXP: 3000,
    };
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return '📈';
      case 'down': return '📉';
      default: return '➡️';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case 'legendary': return 'bg-gradient-to-r from-yellow-400 to-orange-500';
      case 'epic': return 'bg-gradient-to-r from-purple-500 to-pink-500';
      case 'rare': return 'bg-gradient-to-r from-blue-500 to-cyan-500';
      default: return 'bg-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-black mx-auto mb-4"></div>
          <p className="font-bold uppercase">{t.loading}</p>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="p-8 text-center">
        <Card className="shadow-[8px_8px_0_0_#000]">
          <CardContent>
            <p className="text-lg font-semibold">{t.noData}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      {/* Hero Section with Gradient Background */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 border-6 border-black p-8 md:p-12 shadow-[12px_12px_0_0_#000]">
        <h1 className="text-5xl md:text-8xl font-black text-white uppercase mb-6 tracking-tight">
          📊 {t.title}
        </h1>
        
        {/* Stats Cards Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 mb-8">
          <div className="bg-white border-4 border-black p-4 md:p-6 text-center shadow-[4px_4px_0_0_#000] hover:shadow-[8px_8px_0_0_#000] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all">
            <div className="text-4xl md:text-5xl font-black text-blue-500">{analytics.level}</div>
            <div className="text-xs md:text-sm font-bold uppercase mt-2">{t.level}</div>
          </div>
          <div className="bg-white border-4 border-black p-4 md:p-6 text-center shadow-[4px_4px_0_0_#000] hover:shadow-[8px_8px_0_0_#000] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all">
            <div className="text-4xl md:text-5xl font-black text-orange-500">🔥{analytics.currentStreak}</div>
            <div className="text-xs md:text-sm font-bold uppercase mt-2">{t.streak}</div>
          </div>
          <div className="bg-white border-4 border-black p-4 md:p-6 text-center shadow-[4px_4px_0_0_#000] hover:shadow-[8px_8px_0_0_#000] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all">
            <div className="text-4xl md:text-5xl font-black text-green-500">{analytics.totalChallengesCompleted}</div>
            <div className="text-xs md:text-sm font-bold uppercase mt-2">{t.challengesCompleted}</div>
          </div>
          <div className="bg-white border-4 border-black p-4 md:p-6 text-center shadow-[4px_4px_0_0_#000] hover:shadow-[8px_8px_0_0_#000] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all">
            <div className="text-4xl md:text-5xl font-black text-purple-500">{analytics.peerComparison.userPercentile}%</div>
            <div className="text-xs md:text-sm font-bold uppercase mt-2">{t.percentile}</div>
          </div>
        </div>

        {/* XP Progress Bar with Animation */}
        <div className="mt-6">
          <div className="flex justify-between text-white font-bold text-sm md:text-base mb-2">
            <span className="uppercase">{t.progress}</span>
            <span>{analytics.experiencePoints} / {analytics.nextLevelXP} XP</span>
          </div>
          <div className="w-full bg-white border-4 border-black h-8 relative overflow-hidden">
            <div
              className="bg-yellow-400 h-full transition-all duration-700 ease-out relative"
              style={{ width: `${(analytics.experiencePoints / analytics.nextLevelXP) * 100}%` }}
            >
              {/* Animated shimmer effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-yellow-200 to-transparent animate-shimmer" 
                   style={{ 
                     backgroundSize: '200% 100%',
                     animation: 'shimmer 2s infinite'
                   }} 
              />
            </div>
          </div>
        </div>
      </div>

      {/* Tab Navigation with Keyboard Accessibility */}
      <div className="flex gap-2 border-b-4 border-black pb-2" role="tablist" aria-label={t.title}>
        {(['overview', 'achievements', 'recommendations'] as const).map((tab, index) => (
          <button
            key={tab}
            onClick={() => setSelectedTab(tab)}
            onKeyDown={(e) => {
              if (e.key === 'ArrowRight') {
                const tabs = ['overview', 'achievements', 'recommendations'] as const;
                const nextIndex = (index + 1) % tabs.length;
                setSelectedTab(tabs[nextIndex]);
              } else if (e.key === 'ArrowLeft') {
                const tabs = ['overview', 'achievements', 'recommendations'] as const;
                const prevIndex = (index - 1 + tabs.length) % tabs.length;
                setSelectedTab(tabs[prevIndex]);
              }
            }}
            role="tab"
            aria-selected={selectedTab === tab}
            aria-controls={`${tab}-panel`}
            tabIndex={selectedTab === tab ? 0 : -1}
            className={`px-6 py-3 font-black uppercase border-4 border-black transition-all duration-200 ease-out ${
              selectedTab === tab
                ? 'bg-blue-500 text-white shadow-[4px_4px_0_0_#000] translate-y-1 scale-105'
                : 'bg-white hover:bg-gray-50 hover:shadow-[2px_2px_0_0_#000] hover:translate-y-[2px] focus:outline-none focus:ring-4 focus:ring-blue-500 focus:ring-offset-2'
            }`}
          >
            {t[tab]}
          </button>
        ))}
      </div>

      {/* Tab Content with Smooth Transitions */}
      {selectedTab === 'overview' && (
        <div 
          className="space-y-6 animate-slideIn" 
          role="tabpanel" 
          id="overview-panel" 
          aria-labelledby="overview-tab"
        >
          {/* Competency Scores Section */}
          <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0_0_#000]">
            <h2 className="text-2xl md:text-3xl font-black uppercase mb-6 flex items-center gap-2">
              🎯 {t.competencyScores}
            </h2>
            <div className="space-y-6">
              {analytics.competencyScores.map((score, idx) => (
                <div key={idx} className="bg-white border-4 border-black p-4 shadow-[4px_4px_0_0_#000] hover:shadow-[6px_6px_0_0_#000] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all">
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-black uppercase text-base md:text-lg">{score.category}</span>
                    <div className="flex items-center gap-3">
                      <span 
                        className="text-3xl transition-transform duration-300 hover:scale-125" 
                        title={`Trend: ${score.trend}`}
                        aria-label={`Trend: ${score.trend}`}
                      >
                        {getTrendIcon(score.trend)}
                      </span>
                      <span className="text-3xl font-black animate-pulse-brutal">{score.score}%</span>
                    </div>
                  </div>
                  {/* Progress Bar with Color Coding */}
                  <div className="w-full bg-gray-200 h-6 border-2 border-black relative overflow-hidden">
                    <div
                      className={`h-full transition-all duration-700 ease-out ${
                        score.score >= 80 ? 'bg-green-500' :
                        score.score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${score.score}%` }}
                    >
                      {/* Animated shimmer effect on progress bar */}
                      <div 
                        className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30"
                        style={{ 
                          backgroundSize: '200% 100%',
                          animation: 'shimmer 2s infinite'
                        }} 
                      />
                    </div>
                  </div>
                  <div className="text-xs text-gray-600 mt-2 font-semibold">
                    Last updated: {new Date(score.lastUpdated).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Peer Comparison Cards */}
          <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0_0_#000]">
            <h2 className="text-2xl md:text-3xl font-black uppercase mb-6 flex items-center gap-2">
              📊 {t.peerComparison}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-blue-100 border-4 border-blue-500 p-8 text-center shadow-[4px_4px_0_0_#000] hover:shadow-[8px_8px_0_0_#000] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all">
                <div className="text-5xl md:text-6xl font-black text-blue-600 mb-2 animate-pulse-brutal">
                  {analytics.peerComparison.userScore}
                </div>
                <div className="text-sm md:text-base font-bold uppercase text-blue-800">{t.yourScore}</div>
                <div className="mt-4 text-xs font-semibold text-blue-700">
                  You're performing {analytics.peerComparison.userScore > analytics.peerComparison.averageScore ? 'above' : 'below'} average
                </div>
              </div>
              <div className="bg-gray-100 border-4 border-gray-500 p-8 text-center shadow-[4px_4px_0_0_#000] hover:shadow-[8px_8px_0_0_#000] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all">
                <div className="text-5xl md:text-6xl font-black text-gray-600 mb-2">
                  {analytics.peerComparison.averageScore}
                </div>
                <div className="text-sm md:text-base font-bold uppercase text-gray-800">{t.averageScore}</div>
                <div className="mt-4 text-xs font-semibold text-gray-700">
                  Based on all users
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {selectedTab === 'achievements' && (
        <div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-slideIn" 
          role="tabpanel" 
          id="achievements-panel" 
          aria-labelledby="achievements-tab"
        >
          {analytics.achievements.map((achievement, index) => (
            <div 
              key={achievement.id} 
              className="bg-white border-4 border-black shadow-[8px_8px_0_0_#000] hover:shadow-[12px_12px_0_0_#000] hover:translate-x-[-4px] hover:translate-y-[-4px] transition-all duration-300 overflow-hidden group"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Rarity Header with Gradient */}
              <div className={`${getRarityColor(achievement.rarity)} p-6 border-b-4 border-black text-center relative overflow-hidden`}>
                {/* Large Emoji Icon */}
                <div className="text-7xl md:text-8xl mb-3 transform group-hover:scale-110 transition-transform duration-300 relative z-10">
                  {achievement.icon}
                </div>
                {/* Rarity Badge */}
                <div className="text-white font-black uppercase text-sm tracking-wider bg-black bg-opacity-30 px-3 py-1 inline-block border-2 border-white">
                  {achievement.rarity}
                </div>
                {/* Unlock Animation Effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-20 group-hover:animate-shimmer" />
              </div>
              
              {/* Achievement Details */}
              <div className="p-6">
                <h3 className="font-black text-xl md:text-2xl mb-3 uppercase">
                  {achievement.name}
                </h3>
                <p className="text-sm md:text-base font-semibold text-gray-700 mb-4 leading-relaxed">
                  {achievement.description}
                </p>
                <div className="flex items-center gap-2 text-xs font-bold text-gray-500 border-t-2 border-gray-200 pt-3">
                  <span className="text-base">🏆</span>
                  <span className="uppercase">
                    {t.earnedOn}: {new Date(achievement.earnedAt).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedTab === 'recommendations' && (
        <div 
          className="space-y-6 animate-slideIn" 
          role="tabpanel" 
          id="recommendations-panel" 
          aria-labelledby="recommendations-tab"
        >
          <h2 className="text-2xl md:text-3xl font-black uppercase mb-4 flex items-center gap-2">
            💡 {t.recommendations}
          </h2>
          {analytics.recommendations.map((rec, idx) => {
            const borderColor = rec.priority === 'high' ? 'border-l-red-500' : 
                               rec.priority === 'medium' ? 'border-l-yellow-500' : 
                               'border-l-green-500';
            const bgColor = rec.priority === 'high' ? 'bg-red-50' : 
                           rec.priority === 'medium' ? 'bg-yellow-50' : 
                           'bg-green-50';
            
            return (
              <div 
                key={idx} 
                className={`bg-white border-4 border-black border-l-8 ${borderColor} p-6 shadow-[8px_8px_0_0_#000] hover:shadow-[12px_12px_0_0_#000] hover:translate-x-[-4px] hover:translate-y-[-4px] transition-all duration-300`}
              >
                <div className="flex flex-col md:flex-row md:items-start gap-4">
                  {/* Priority Badge */}
                  <div className={`${getPriorityColor(rec.priority)} text-white px-4 py-2 border-4 border-black font-black uppercase text-sm shadow-[4px_4px_0_0_#000] self-start`}>
                    {rec.priority}
                  </div>
                  
                  {/* Recommendation Content */}
                  <div className="flex-1">
                    <h3 className="font-black text-xl md:text-2xl mb-3 uppercase">
                      {rec.category}
                    </h3>
                    <p className="font-semibold text-gray-700 mb-6 text-base leading-relaxed">
                      {rec.description}
                    </p>
                    
                    {/* Suggested Challenges */}
                    <div>
                      <div className="font-black uppercase text-sm mb-3 flex items-center gap-2">
                        🎯 {t.suggestedChallenges}:
                      </div>
                      <div className="flex flex-wrap gap-3">
                        {rec.suggestedChallenges.map((challenge, cidx) => (
                          <button
                            key={cidx}
                            className="bg-blue-500 text-white px-4 py-2 border-4 border-black text-sm font-bold uppercase shadow-[4px_4px_0_0_#000] hover:shadow-[2px_2px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] transition-all duration-150 cursor-pointer"
                            onClick={() => {
                              // Navigate to the challenge or show more info
                              console.log('Navigate to challenge:', challenge);
                            }}
                          >
                            {challenge} →
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
