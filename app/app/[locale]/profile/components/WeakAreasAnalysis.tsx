'use client';

import { motion } from 'framer-motion';
import { useTranslations } from 'next-intl';
import Link from 'next/link';
import type { ProfileAnalytics } from '@lib/types';

interface WeakAreasAnalysisProps {
  analytics: ProfileAnalytics;
}

export function WeakAreasAnalysis({ analytics }: WeakAreasAnalysisProps) {
  const t = useTranslations('profile');

  const getCategorySlug = (category: string) => {
    return category.toLowerCase().replace(/\s+/g, '-');
  };

  const getImprovementIcon = (accuracy: number) => {
    if (accuracy < 40) return '🚨';
    if (accuracy < 60) return '⚠️';
    if (accuracy < 80) return '📈';
    return '✅';
  };

  const getUrgencyColor = (accuracy: number) => {
    if (accuracy < 40) return 'bg-red-100 border-red-500 text-red-800';
    if (accuracy < 60) return 'bg-orange-100 border-orange-500 text-orange-800';
    if (accuracy < 80) return 'bg-yellow-100 border-yellow-500 text-yellow-800';
    return 'bg-green-100 border-green-500 text-green-800';
  };

  // Sort weak areas by accuracy (lowest first)
  const sortedWeakAreas = [...analytics.weakAreas].sort((a, b) => a.accuracy - b.accuracy);

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.5 }}
      className="bg-white border-4 border-black shadow-brutal p-6"
    >
      <h3 className="text-xl font-black text-black mb-4 text-shadow-brutal">
        {t('weakAreasAnalysis')}
      </h3>

      {sortedWeakAreas.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-6xl mb-4">🎯</div>
          <p className="text-gray-600 font-bold">
            {t('noWeakAreas')}
          </p>
          <p className="text-sm text-gray-500 mt-2">
            {t('excellentProgress')}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {sortedWeakAreas.slice(0, 3).map((area, index) => (
            <motion.div
              key={area.category}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 + index * 0.1 }}
              className={`border-2 p-4 ${getUrgencyColor(area.accuracy)}`}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{getImprovementIcon(area.accuracy)}</span>
                  <h4 className="font-bold text-sm uppercase tracking-wide">
                    {area.category}
                  </h4>
                </div>
                <div className="text-lg font-black">
                  {area.accuracy.toFixed(1)}%
                </div>
              </div>

              {/* Priority Level */}
              <div className="mb-3">
                <span className="text-xs font-bold uppercase px-2 py-1 bg-black text-white">
                  {area.accuracy < 40 ? t('critical') : 
                   area.accuracy < 60 ? t('high') : 
                   area.accuracy < 80 ? t('medium') : t('low')} {t('priority')}
                </span>
              </div>

              {/* Recommended Challenges */}
              {area.recommendedChallenges.length > 0 && (
                <div className="space-y-2">
                  <p className="text-xs font-bold uppercase">
                    {t('recommendedPractice')}:
                  </p>
                  <div className="text-xs">
                    {t('practiceMore', { count: area.recommendedChallenges.length })}
                  </div>
                </div>
              )}

              {/* Action Button */}
              <Link 
                href={`/${getCategorySlug(area.category)}`}
                className="inline-block mt-3"
              >
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="bg-black text-white px-4 py-2 border-2 border-black shadow-brutal text-xs font-bold uppercase tracking-wide hover:bg-gray-800 transition-colors"
                >
                  {t('practiceNow')} →
                </motion.button>
              </Link>
            </motion.div>
          ))}

          {/* Learning Tips */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
            className="mt-6 pt-4 border-t-2 border-black"
          >
            <h4 className="text-sm font-bold text-black mb-3 uppercase">
              {t('learningTips')}
            </h4>
            <div className="space-y-2 text-xs text-gray-700">
              <div className="flex items-start gap-2">
                <span className="text-blue-500">💡</span>
                <p>{t('tip1')}</p>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-green-500">🎯</span>
                <p>{t('tip2')}</p>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-purple-500">📚</span>
                <p>{t('tip3')}</p>
              </div>
            </div>
          </motion.div>

          {/* Overall Improvement Score */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2 }}
            className="mt-6 pt-4 border-t-2 border-black"
          >
            <div className="text-center">
              <div className="text-2xl font-black text-black mb-1">
                {((analytics.categoryBreakdown.reduce((acc, cat) => acc + cat.accuracy, 0) / analytics.categoryBreakdown.length) || 0).toFixed(1)}%
              </div>
              <div className="text-xs font-bold text-gray-700 uppercase">
                {t('overallImprovement')}
              </div>
              <div className="mt-2 text-xs text-gray-600">
                {analytics.categoryBreakdown.filter(cat => cat.accuracy >= 80).length > analytics.categoryBreakdown.filter(cat => cat.accuracy < 60).length 
                  ? t('goodProgress') 
                  : t('keepPracticing')}
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </motion.div>
  );
}
