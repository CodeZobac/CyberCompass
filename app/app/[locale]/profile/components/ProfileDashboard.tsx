'use client';

import { useProfileAnalytics } from '@lib/hooks/profile/useProfileAnalytics';
import { useAchievements } from '@lib/hooks/profile/useAchievements';
import { useExport } from '@lib/hooks/profile/useExport';
import { ProfileHeader } from './ProfileHeader';
import { ProgressOverview } from './ProgressOverview';
import { CategoryBreakdown } from './CategoryBreakdown';
import { AchievementBadges } from './AchievementBadges';
import { PerformanceCharts } from './PerformanceCharts';
import { WeakAreasAnalysis } from './WeakAreasAnalysis';
import { ChallengeHistory } from './ChallengeHistory';
import { ExportControls } from './ExportControls';

interface ProfileDashboardProps {
  userId: string;
}

export function ProfileDashboard({ userId }: ProfileDashboardProps) {
  const { data: analytics, isLoading: analyticsLoading, error: analyticsError } = useProfileAnalytics(userId);
  const { data: achievements, isLoading: achievementsLoading } = useAchievements(userId);
  const exportMutation = useExport();

  if (analyticsLoading) {
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

  if (analyticsError) {
    return (
      <div className="bg-red-50 border-4 border-red-500 shadow-brutal p-6">
        <h2 className="text-2xl font-bold text-red-800 mb-2">Error Loading Profile</h2>
        <p className="text-red-700">
          Failed to load your profile data. Please try refreshing the page.
        </p>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="bg-yellow-50 border-4 border-yellow-500 shadow-brutal p-6">
        <h2 className="text-2xl font-bold text-yellow-800 mb-2">No Data Available</h2>
        <p className="text-yellow-700">
          Start completing challenges to see your progress analytics!
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Main Content */}
      <div className="lg:col-span-2 space-y-6">
        <ProfileHeader analytics={analytics} />
        
        <ProgressOverview analytics={analytics} />
        
        <PerformanceCharts analytics={analytics} />
        
        <ChallengeHistory analytics={analytics} />
      </div>

      {/* Sidebar */}
      <div className="space-y-6">
        <CategoryBreakdown analytics={analytics} />
        
        <AchievementBadges 
          achievements={achievements || []} 
          isLoading={achievementsLoading}
        />
        
        <WeakAreasAnalysis analytics={analytics} />
        
        <ExportControls 
          onExport={exportMutation.mutate}
          isExporting={exportMutation.isPending}
        />
      </div>
    </div>
  );
}
