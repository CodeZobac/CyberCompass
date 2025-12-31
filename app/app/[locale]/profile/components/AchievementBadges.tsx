'use client';

import { motion } from 'framer-motion';
import { useTranslations } from 'next-intl';
import type { UserAchievement } from '@lib/types';

interface AchievementBadgesProps {
  achievements: UserAchievement[];
  isLoading: boolean;
}

export function AchievementBadges({ achievements, isLoading }: AchievementBadgesProps) {
  const t = useTranslations('profile');

  const getAchievementIcon = (type: string) => {
    switch (type) {
      case 'streak':
        return '🔥';
      case 'category_master':
        return '👑';
      case 'perfect_score':
        return '💯';
      case 'speed_demon':
        return '⚡';
      case 'consistency':
        return '📅';
      case 'milestone':
        return '🏆';
      default:
        return '⭐';
    }
  };

  const getAchievementColor = (type: string) => {
    switch (type) {
      case 'streak':
        return 'bg-red-400';
      case 'category_master':
        return 'bg-yellow-400';
      case 'perfect_score':
        return 'bg-green-400';
      case 'speed_demon':
        return 'bg-blue-400';
      case 'consistency':
        return 'bg-purple-400';
      case 'milestone':
        return 'bg-orange-400';
      default:
        return 'bg-gray-400';
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white border-4 border-black shadow-brutal p-6">
        <h3 className="text-xl font-black text-black mb-4 text-shadow-brutal">
          {t('achievements')}
        </h3>
        <div className="grid grid-cols-2 gap-3">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-gray-200 border-2 border-black h-20 animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.3 }}
      className="bg-white border-4 border-black shadow-brutal p-6"
    >
      <h3 className="text-xl font-black text-black mb-4 text-shadow-brutal">
        {t('achievements')}
      </h3>

      {achievements.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-6xl mb-4">🏆</div>
          <p className="text-gray-600 font-bold">
            {t('noAchievements')}
          </p>
          <p className="text-sm text-gray-500 mt-2">
            {t('keepLearning')}
          </p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 gap-3 mb-4">
            {achievements.slice(0, 6).map((achievement, index) => (
              <motion.div
                key={achievement.id}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.4 + index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                className={`${getAchievementColor(achievement.achievement_type)} border-2 border-black shadow-brutal p-3 text-center cursor-pointer group relative`}
              >
                <div className="text-2xl mb-1">
                  {getAchievementIcon(achievement.achievement_type)}
                </div>
                <div className="text-xs font-bold text-black uppercase tracking-wide leading-tight">
                  {achievement.achievement_name}
                </div>
                
                {/* Tooltip */}
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-10">
                  <div className="bg-black text-white text-xs p-2 rounded whitespace-nowrap max-w-48">
                    {achievement.achievement_description || achievement.achievement_name}
                    <div className="text-xs text-gray-300 mt-1">
                      {new Date(achievement.earned_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {achievements.length > 6 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1 }}
              className="text-center"
            >
              <div className="bg-gray-100 border-2 border-black p-2 text-sm font-bold text-gray-700">
                +{achievements.length - 6} {t('moreAchievements')}
              </div>
            </motion.div>
          )}

          {/* Recent Achievement Highlight */}
          {achievements.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.2 }}
              className="mt-4 pt-4 border-t-2 border-black"
            >
              <h4 className="text-sm font-bold text-black mb-2 uppercase">
                {t('latestAchievement')}
              </h4>
              <div className="flex items-center gap-3 bg-yellow-100 border-2 border-black p-3">
                <div className="text-3xl">
                  {getAchievementIcon(achievements[0].achievement_type)}
                </div>
                <div className="flex-1">
                  <div className="font-bold text-black text-sm">
                    {achievements[0].achievement_name}
                  </div>
                  <div className="text-xs text-gray-600">
                    {new Date(achievements[0].earned_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </>
      )}

      {/* Achievement Stats */}
      <div className="mt-6 pt-4 border-t-2 border-black">
        <div className="grid grid-cols-3 gap-2 text-center text-xs">
          <div className="bg-yellow-100 border border-black p-2">
            <div className="font-black text-yellow-800 text-lg">
              {achievements.length}
            </div>
            <div className="font-bold text-yellow-700 uppercase">
              {t('total')}
            </div>
          </div>
          <div className="bg-green-100 border border-black p-2">
            <div className="font-black text-green-800 text-lg">
              {achievements.filter(a => a.achievement_type === 'category_master').length}
            </div>
            <div className="font-bold text-green-700 uppercase">
              {t('mastery')}
            </div>
          </div>
          <div className="bg-red-100 border border-black p-2">
            <div className="font-black text-red-800 text-lg">
              {achievements.filter(a => a.achievement_type === 'streak').length}
            </div>
            <div className="font-bold text-red-700 uppercase">
              {t('streaks')}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
