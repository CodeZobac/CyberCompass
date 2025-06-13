'use client';

import { useState, useEffect } from 'react';
import { useTranslations } from 'next-intl';
import { motion } from 'framer-motion';
import type { ProfileAnalytics } from '@lib/types';
import { ProgressOverview } from '../../../components/ProgressOverview';
import { CategoryBreakdown } from '../../../components/CategoryBreakdown';
import { AchievementBadges } from '../../../components/AchievementBadges';
import { PerformanceCharts } from '../../../components/PerformanceCharts';
import { WeakAreasAnalysis } from '../../../components/WeakAreasAnalysis';
import { ChallengeHistory } from '../../../components/ChallengeHistory';

interface SharedProfileData {
  analytics: ProfileAnalytics;
  userInfo: {
    name?: string;
    joinDate: string;
  };
  shareInfo: {
    viewCount: number;
    expiresAt?: string;
    createdAt: string;
  };
}

interface SharedProfileDashboardProps {
  token: string;
}

export function SharedProfileDashboard({ token }: SharedProfileDashboardProps) {
  const [data, setData] = useState<SharedProfileData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const t = useTranslations('profile');

  useEffect(() => {
    async function fetchSharedProfile() {
      try {
        const response = await fetch(`/api/profile/shared/${token}`);
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to load shared profile');
        }

        const profileData = await response.json();
        setData(profileData);
      } catch (err) {
        console.error('Error fetching shared profile:', err);
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
      } finally {
        setIsLoading(false);
      }
    }

    fetchSharedProfile();
  }, [token]);

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white border-4 border-black shadow-brutal h-64 animate-pulse" />
          <div className="bg-white border-4 border-black shadow-brutal h-96 animate-pulse" />
        </div>
        <div className="space-y-6">
          <div className="bg-white border-4 border-black shadow-brutal h-32 animate-pulse" />
          <div className="bg-white border-4 border-black shadow-brutal h-48 animate-pulse" />
          <div className="bg-white border-4 border-black shadow-brutal h-64 animate-pulse" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-red-50 border-4 border-red-500 shadow-brutal p-6"
      >
        <div className="text-center">
          <span className="text-6xl mb-4 block">🚫</span>
          <h2 className="text-2xl font-bold text-red-800 mb-2">
            {t('sharedProfileError')}
          </h2>
          <p className="text-red-700 mb-4">{error}</p>
          <button
            onClick={() => window.history.back()}
            className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 border-4 border-black shadow-brutal transform transition-transform hover:scale-105"
          >
            {t('goBack')}
          </button>
        </div>
      </motion.div>
    );
  }

  if (!data) {
    return (
      <div className="bg-yellow-50 border-4 border-yellow-500 shadow-brutal p-6">
        <h2 className="text-2xl font-bold text-yellow-800 mb-2">No Data Available</h2>
        <p className="text-yellow-700">
          The shared profile data could not be loaded.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Share Info Banner */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-blue-50 border-4 border-blue-400 shadow-brutal p-4 rounded-lg"
      >
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h3 className="font-bold text-blue-800 mb-1">
              📊 {t('sharedProfileInfo')}
            </h3>
            <p className="text-sm text-blue-700">
              {t('profileSharedBy', { name: data.userInfo.name || 'User' })}
            </p>
          </div>
          <div className="text-right">
            <div className="text-sm text-blue-600 space-y-1">
              <div>👁️ {t('views')}: {data.shareInfo.viewCount}</div>
              {data.shareInfo.expiresAt && (
                <div>
                  ⏰ {t('expires')}: {new Date(data.shareInfo.expiresAt).toLocaleDateString()}
                </div>
              )}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Profile Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          <SharedProfileHeader 
            analytics={data.analytics}
            userInfo={data.userInfo}
          />
          
          <ProgressOverview analytics={data.analytics} />
          
          <PerformanceCharts analytics={data.analytics} />
          
          <ChallengeHistory analytics={data.analytics} />
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <CategoryBreakdown analytics={data.analytics} />
          
          <AchievementBadges 
            achievements={data.analytics.achievements || []} 
            isLoading={false}
          />
          
          <WeakAreasAnalysis analytics={data.analytics} />
        </div>
      </div>
    </div>
  );
}

interface SharedProfileHeaderProps {
  analytics: ProfileAnalytics;
  userInfo: {
    name?: string;
    joinDate: string;
  };
}

function SharedProfileHeader({ analytics, userInfo }: SharedProfileHeaderProps) {
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
              {userInfo.name?.charAt(0)?.toUpperCase() || 'U'}
            </span>
          </div>
          <div>
            <h2 className="text-2xl font-black text-black mb-1">
              {userInfo.name || 'User'}
            </h2>
            <p className="text-sm text-gray-600 font-medium">
              {t('memberSince')}: {new Date(userInfo.joinDate).toLocaleDateString()}
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
