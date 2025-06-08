'use client';

import { motion } from 'framer-motion';
import { useTranslations } from 'next-intl';
import type { ProfileAnalytics } from '@lib/types';

interface CategoryBreakdownProps {
  analytics: ProfileAnalytics;
}

export function CategoryBreakdown({ analytics }: CategoryBreakdownProps) {
  const t = useTranslations('profile');

  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'catfishing':
        return '🎣';
      case 'cyberbullying':
        return '🛡️';
      case 'deepfakes':
        return '🎭';
      case 'disinformation':
        return '📰';
      default:
        return '🔒';
    }
  };

  const getAccuracyColor = (accuracy: number) => {
    if (accuracy >= 80) return 'bg-green-400';
    if (accuracy >= 60) return 'bg-yellow-400';
    return 'bg-red-400';
  };

  const getProgressBarColor = (accuracy: number) => {
    if (accuracy >= 80) return 'bg-green-500';
    if (accuracy >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.2 }}
      className="bg-white border-4 border-black shadow-brutal p-6"
    >
      <h3 className="text-xl font-black text-black mb-4 text-shadow-brutal">
        {t('categoryBreakdown')}
      </h3>

      <div className="space-y-4">
        {analytics.categoryBreakdown.map((category, index) => (
          <motion.div
            key={category.categoryId}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 + index * 0.1 }}
            className="border-2 border-black p-4 bg-gray-50"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className="text-2xl">{getCategoryIcon(category.category)}</span>
                <h4 className="font-bold text-black text-sm uppercase tracking-wide">
                  {category.category}
                </h4>
              </div>
              <div className={`px-2 py-1 border-2 border-black ${getAccuracyColor(category.accuracy)} font-bold text-xs`}>
                {category.accuracy.toFixed(1)}%
              </div>
            </div>

            {/* Progress Bar */}
            <div className="mb-3">
              <div className="flex justify-between text-xs font-bold text-gray-700 mb-1">
                <span>{t('progress')}</span>
                <span>{category.completed}/{category.total}</span>
              </div>
              <div className="w-full bg-gray-300 border-2 border-black h-4">
                <motion.div
                  className={`h-full border-r-2 border-black ${getProgressBarColor(category.accuracy)}`}
                  initial={{ width: 0 }}
                  animate={{ width: `${(category.completed / category.total) * 100}%` }}
                  transition={{ duration: 1, delay: 0.5 + index * 0.1 }}
                />
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="text-center bg-white border border-black p-2">
                <div className="font-black text-black">
                  {((category.completed / category.total) * 100).toFixed(0)}%
                </div>
                <div className="font-bold text-gray-600 uppercase">
                  {t('complete')}
                </div>
              </div>
              <div className="text-center bg-white border border-black p-2">
                <div className="font-black text-black">
                  {category.averageDifficulty.toFixed(1)}
                </div>
                <div className="font-bold text-gray-600 uppercase">
                  {t('difficulty')}
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Summary Stats */}
      <div className="mt-6 pt-4 border-t-2 border-black">
        <div className="grid grid-cols-2 gap-2 text-center">
          <div className="bg-blue-100 border-2 border-black p-3">
            <div className="text-lg font-black text-blue-800">
              {analytics.categoryBreakdown.length}
            </div>
            <div className="text-xs font-bold text-blue-700 uppercase">
              {t('categories')}
            </div>
          </div>
          <div className="bg-green-100 border-2 border-black p-3">
            <div className="text-lg font-black text-green-800">
              {analytics.categoryBreakdown.filter(cat => cat.accuracy >= 80).length}
            </div>
            <div className="text-xs font-bold text-green-700 uppercase">
              {t('mastered')}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
