'use client';

import { motion } from 'framer-motion';
import { useSession } from 'next-auth/react';
import { useTranslations } from 'next-intl';
import type { ProfileAnalytics } from '@lib/types';

interface ProfileHeaderProps {
  analytics: ProfileAnalytics;
  onExport: (format: 'json' | 'pdf') => void;
  isExporting: boolean;
}

export function ProfileHeader({ analytics, onExport, isExporting }: ProfileHeaderProps) {
  const { data: session } = useSession();
  const t = useTranslations('profile');

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white border-4 border-black shadow-brutal p-6"
    >
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 border-4 border-black shadow-brutal rounded-full flex items-center justify-center">
            <span className="text-2xl font-black text-white">
              {session?.user?.name?.charAt(0)?.toUpperCase() || 'U'}
            </span>
          </div>
          <div>
            <h2 className="text-2xl font-black text-black mb-1">
              {session?.user?.name || 'User'}
            </h2>
            <p className="text-sm text-gray-600 font-medium">
              {session?.user?.email}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-3xl font-black text-black mb-1">
              {analytics.ethicalDevelopmentScore}/100
            </div>
            <div className="text-sm font-bold text-gray-700 uppercase tracking-wide">
              {t('ethicalScore')}
            </div>
          </div>

          <motion.div
            className={`w-20 h-20 border-4 border-black shadow-brutal rounded-full flex items-center justify-center ${
              analytics.ethicalDevelopmentScore >= 80 
                ? 'bg-green-400' 
                : analytics.ethicalDevelopmentScore >= 60 
                ? 'bg-yellow-400' 
                : 'bg-red-400'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="text-2xl font-black text-black">
              {analytics.ethicalDevelopmentScore >= 80 
                ? '🏆' 
                : analytics.ethicalDevelopmentScore >= 60 
                ? '⭐' 
                : '📈'}
            </span>
          </motion.div>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6 pt-6 border-t-4 border-black">
        <div className="text-center">
          <div className="text-2xl font-black text-black">
            {analytics.completedChallenges}
          </div>
          <div className="text-sm font-bold text-gray-700 uppercase tracking-wide">
            {t('completed')}
          </div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-black text-black">
            {analytics.completionRate.toFixed(1)}%
          </div>
          <div className="text-sm font-bold text-gray-700 uppercase tracking-wide">
            {t('completion')}
          </div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-black text-black">
            {analytics.averageScore.toFixed(1)}%
          </div>
          <div className="text-sm font-bold text-gray-700 uppercase tracking-wide">
            {t('accuracy')}
          </div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-black text-black">
            {analytics.streakData.currentStreak}
          </div>
          <div className="text-sm font-bold text-gray-700 uppercase tracking-wide">
            {t('streak')}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
