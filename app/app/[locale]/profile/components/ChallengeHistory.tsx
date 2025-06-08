'use client';

import { motion } from 'framer-motion';
import { useTranslations } from 'next-intl';
import type { ProfileAnalytics } from '@lib/types';

interface ChallengeHistoryProps {
  analytics: ProfileAnalytics;
}

export function ChallengeHistory({ analytics }: ChallengeHistoryProps) {
  const t = useTranslations('profile');

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 90) return '🌟';
    if (score >= 80) return '🎯';
    if (score >= 60) return '👍';
    return '📈';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const getDaysAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return t('yesterday');
    if (diffDays < 7) return t('daysAgo', { days: diffDays });
    if (diffDays < 30) return t('weeksAgo', { weeks: Math.floor(diffDays / 7) });
    return t('monthsAgo', { months: Math.floor(diffDays / 30) });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6 }}
      className="bg-white border-4 border-black shadow-brutal p-6"
    >
      <h3 className="text-2xl font-black text-black mb-6 text-shadow-brutal">
        {t('challengeHistory')}
      </h3>

      {analytics.recentActivity.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📚</div>
          <p className="text-gray-600 font-bold">
            {t('noActivityYet')}
          </p>
          <p className="text-sm text-gray-500 mt-2">
            {t('startLearning')}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Activity Timeline */}
          <div className="relative">
            {analytics.recentActivity.map((activity, index) => (
              <motion.div
                key={`${activity.date}-${index}`}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                className="relative pl-8 pb-6 last:pb-0"
              >
                {/* Timeline Line */}
                {index < analytics.recentActivity.length - 1 && (
                  <div className="absolute left-3 top-8 w-0.5 h-full bg-gray-300" />
                )}
                
                {/* Timeline Dot */}
                <div className={`absolute left-0 top-2 w-6 h-6 border-2 border-black shadow-brutal rounded-full flex items-center justify-center text-xs ${getScoreColor(activity.score)}`}>
                  {getScoreIcon(activity.score)}
                </div>

                {/* Activity Card */}
                <div className="bg-gray-50 border-2 border-black p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <div className="text-sm font-bold text-black">
                        {formatDate(activity.date)}
                      </div>
                      <div className="text-xs text-gray-500">
                        {getDaysAgo(activity.date)}
                      </div>
                    </div>
                    <div className={`px-2 py-1 border border-black text-xs font-bold ${getScoreColor(activity.score)}`}>
                      {activity.score.toFixed(1)}%
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="text-sm text-gray-700">
                      {t('completedChallenges', { count: activity.challengesCompleted })}
                    </div>
                    <div className="flex items-center gap-1 text-xs text-gray-500">
                      <span>🎯</span>
                      <span>{activity.challengesCompleted}</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Summary Statistics */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2 }}
            className="mt-8 pt-6 border-t-4 border-black"
          >
            <h4 className="text-lg font-bold text-black mb-4">{t('activitySummary')}</h4>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-blue-100 border-2 border-black p-3 text-center">
                <div className="text-xl font-black text-blue-800">
                  {analytics.recentActivity.length}
                </div>
                <div className="text-xs font-bold text-blue-700 uppercase">
                  {t('activeDays')}
                </div>
              </div>

              <div className="bg-green-100 border-2 border-black p-3 text-center">
                <div className="text-xl font-black text-green-800">
                  {analytics.recentActivity.reduce((sum, activity) => sum + activity.challengesCompleted, 0)}
                </div>
                <div className="text-xs font-bold text-green-700 uppercase">
                  {t('totalCompleted')}
                </div>
              </div>

              <div className="bg-yellow-100 border-2 border-black p-3 text-center">
                <div className="text-xl font-black text-yellow-800">
                  {analytics.recentActivity.length > 0 
                    ? (analytics.recentActivity.reduce((sum, activity) => sum + activity.score, 0) / analytics.recentActivity.length).toFixed(1)
                    : '0.0'}%
                </div>
                <div className="text-xs font-bold text-yellow-700 uppercase">
                  {t('avgScore')}
                </div>
              </div>

              <div className="bg-purple-100 border-2 border-black p-3 text-center">
                <div className="text-xl font-black text-purple-800">
                  {analytics.recentActivity.filter(activity => activity.score >= 80).length}
                </div>
                <div className="text-xs font-bold text-purple-700 uppercase">
                  {t('excellentDays')}
                </div>
              </div>
            </div>
          </motion.div>

          {/* Motivational Message */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.4 }}
            className="mt-6 bg-gradient-to-r from-blue-100 to-purple-100 border-2 border-black p-4 text-center"
          >
            <div className="text-2xl mb-2">
              {analytics.streakData.currentStreak >= 7 ? '🔥' : 
               analytics.streakData.currentStreak >= 3 ? '⭐' : '💪'}
            </div>
            <p className="text-sm font-bold text-gray-800">
              {analytics.streakData.currentStreak >= 7 
                ? t('onFireMessage')
                : analytics.streakData.currentStreak >= 3 
                ? t('goodStreakMessage') 
                : t('keepGoingMessage')}
            </p>
          </motion.div>
        </div>
      )}
    </motion.div>
  );
}
