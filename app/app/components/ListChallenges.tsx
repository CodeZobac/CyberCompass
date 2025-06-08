'use client';

import React, { useState } from 'react';
import { Challenge } from '@lib/types';
import { useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { RenderChallenge } from '@/components/RenderChallenge';
import { useProgressPersistence, useProgressBroadcast } from '@lib/hooks/useProgressPersistence';
import { useRealtimeProgress, useRealtimeBroadcast } from '@lib/hooks/useRealtimeProgress';
import { useAutoMigration } from '@lib/hooks/useProgressMigration';
import { 
  ProgressIndicator, 
  OfflineIndicator, 
  SyncSpinner, 
  ConflictWarning,
  CollaborationIndicator 
} from './ui/progress-indicator';
import { useNetworkStatus } from '@lib/services/offline-sync';
import { useSession } from 'next-auth/react';

interface ListChallengesProps {
  challenges: Challenge[];
  userId?: string;
  categoryName: string;
}

export default function ListChallenges({ challenges, userId, categoryName }: ListChallengesProps) {
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const { data: session } = useSession();

  // Enhanced progress persistence
  const { 
    getCategoryProgress,
    isChallengeCompleted,
    isAuthenticated
  } = useProgressPersistence();

  // Real-time features
  useRealtimeProgress();
  useRealtimeBroadcast();
  useProgressBroadcast();

  // Auto-migration when user signs in
  const { triggerAutoMigration, isMigrating } = useAutoMigration();

  // Network status
  const { isOnline } = useNetworkStatus();

  // Trigger migration when user becomes authenticated
  React.useEffect(() => {
    if (session?.user?.id && !isAuthenticated) {
      triggerAutoMigration(session.user.id);
    }
  }, [session?.user?.id, isAuthenticated, triggerAutoMigration]);

  // Calculate category progress
  const challengeIds = challenges.map(c => c.id);
  const categoryProgress = getCategoryProgress(challengeIds);
  const completedCount = challengeIds.filter(id => isChallengeCompleted(id)).length;

  const handleSelectChallenge = (challenge: Challenge) => {
    setSelectedChallenge(challenge);
  };

  const handleBackToList = () => {
    setSelectedChallenge(null);
  };

  // Helper function to get difficulty-based colors
  const getDifficultyColors = (difficulty: number) => {
    switch(difficulty) {
      case 1: return {
        bg: 'bg-green-600',
        text: 'text-white',
        label: 'EASY'
      };
      case 2: return {
        bg: 'bg-yellow-600',
        text: 'text-black',
        label: 'MEDIUM'
      };
      case 3: return {
        bg: 'bg-red-600',
        text: 'text-white',
        label: 'HARD'
      };
      default: return {
        bg: 'bg-gray-600',
        text: 'text-white',
        label: 'UNKNOWN'
      };
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {selectedChallenge ? (
        // Selected Challenge View
        <div className="container mx-auto px-6 py-8">
          <Button 
            onClick={handleBackToList} 
            className="mb-8 bg-white text-black border-6 border-black hover:bg-black hover:text-white font-bold text-lg px-8 py-4 shadow-[8px_8px_0px_0px_#000000] hover:shadow-[4px_4px_0px_0px_#000000] transform hover:translate-x-1 hover:translate-y-1 transition-all duration-200"
          >
            ← BACK TO CHALLENGES
          </Button>
          <RenderChallenge 
            challenges={[selectedChallenge]} 
            userId={userId} 
          />
        </div>
      ) : (
        // Challenge Selection View
        <div>
          {/* Hero Section */}
          <div className="bg-white text-black py-16 border-b-6 border-black">
            <div className="container mx-auto px-6 text-center">
              <h1 className="text-6xl md:text-8xl font-black uppercase mb-6 text-red-500 text-shadow-[6px_6px_0px_#000000]">
                {categoryName}
              </h1>
              <h2 className="text-2xl md:text-4xl font-bold uppercase mb-4 text-black text-shadow-[3px_3px_0px_#ffffff]">
                CHALLENGES
              </h2>


              <div className="bg-black text-white p-6 inline-block border-4 border-black shadow-[12px_12px_0px_0px_#ff0000] mt-8">
                <p className="text-xl font-bold uppercase">
                  {challenges.length} CHALLENGE{challenges.length !== 1 ? 'S' : ''} AVAILABLE
                </p>
              </div>
            </div>
          </div>

          {/* Instructions Section */}
          <div className="bg-white py-16">
            <div className="container mx-auto px-6">
              <div className="max-w-4xl mx-auto text-center mb-16">
                <div className="bg-red-600 text-white p-8 border-6 border-black shadow-[12px_12px_0px_0px_#000000]">
                  <h3 className="text-3xl font-black uppercase mb-4">SELECT YOUR CHALLENGE</h3>
                  <p className="text-xl font-bold">
                    Choose a challenge below to test your cybersecurity knowledge and skills.
                    Each challenge is designed to strengthen your digital defense capabilities.
                  </p>
                </div>
              </div>

              {/* Dedicated Progress Panel - Less Intrusive */}
              <div className="max-w-4xl mx-auto mb-12">
                <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0_0_#000] rounded-sm">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="text-lg font-black uppercase tracking-wider">Your Progress</h4>
                    <div className="flex items-center gap-2">
                      {isMigrating && <SyncSpinner />}
                      {!isOnline && <OfflineIndicator />}
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
                    {/* Progress Indicator */}
                    <div className="md:col-span-2">
                      <ProgressIndicator 
                        progress={categoryProgress}
                        className="w-full"
                      />
                    </div>
                    
                    {/* Stats Summary */}
                    <div className="space-y-2">
                      <div className="bg-gray-50 border-2 border-black px-3 py-2 rounded-sm text-center">
                        <div className="text-2xl font-black">{completedCount}/{challenges.length}</div>
                        <div className="text-xs font-bold uppercase tracking-wider">Completed</div>
                      </div>
                      <div className="bg-gray-50 border-2 border-black px-3 py-2 rounded-sm text-center">
                        <div className="text-xs font-bold uppercase tracking-wider">
                          {isAuthenticated ? '🔐 Signed In' : '👤 Anonymous'}
                        </div>
                        <div className="text-xs font-bold">
                          {isOnline ? '🟢 Online' : '🔴 Offline'}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Migration Status */}
                  {isMigrating && (
                    <div className="mt-4 p-3 bg-yellow-100 border-2 border-yellow-500 rounded-sm">
                      <div className="flex items-center gap-2 text-sm">
                        <SyncSpinner />
                        <span className="font-bold uppercase tracking-wider">
                          Migrating your progress...
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Challenge Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
                {challenges.map((challenge) => {
                  const colors = getDifficultyColors(challenge.difficulty as number);
                  const isCompleted = isChallengeCompleted(challenge.id);
                  
                  return (
                    <Card 
                      key={challenge.id}
                      className={`bg-white border-6 border-black shadow-[12px_12px_0px_0px_#000000] hover:shadow-[6px_6px_0px_0px_#000000] transform hover:translate-x-2 hover:translate-y-2 transition-all duration-200 cursor-pointer p-0 overflow-hidden ${
                        isCompleted ? 'ring-4 ring-green-500' : ''
                      }`}
                      onClick={() => handleSelectChallenge(challenge)}
                    >
                      {/* Difficulty Badge */}
                      <div className={`${colors.bg} ${colors.text} p-4 border-b-4 border-black relative`}>
                        <div className="text-center">
                          <span className="text-lg font-black uppercase tracking-wider">
                            {colors.label}
                          </span>
                        </div>
                      </div>

                      {/* Challenge Content */}
                      <div className="p-6">
                        <h3 className="text-2xl font-black uppercase mb-4 text-black leading-tight">
                          {challenge.i18n?.[locale]?.title || challenge.title}
                        </h3>
                        
                        {challenge.i18n?.[locale]?.description && (
                          <p className="text-gray-700 font-semibold text-sm leading-relaxed">
                            {challenge.i18n[locale].description.slice(0, 120)}
                            {challenge.i18n[locale].description.length > 120 ? '...' : ''}
                          </p>
                        )}

                        {/* Action Indicator */}
                        <div className="mt-6 pt-4 border-t-2 border-black">
                          <div className={`px-4 py-2 inline-block font-bold uppercase text-sm ${
                            isCompleted 
                              ? 'bg-green-500 text-white border-2 border-green-700' 
                              : 'bg-black text-white'
                          }`}>
                            {isCompleted ? '✓ COMPLETED' : 'START CHALLENGE →'}
                          </div>
                        </div>
                      </div>
                    </Card>
                  );
                })}
              </div>

              {/* Bottom CTA */}
              {challenges.length === 0 && (
                <div className="text-center mt-16">
                  <div className="bg-gray-100 border-6 border-black p-8 inline-block shadow-[8px_8px_0px_0px_#000000]">
                    <h3 className="text-2xl font-black uppercase mb-2">NO CHALLENGES AVAILABLE</h3>
                    <p className="text-lg font-bold text-gray-700">
                      Check back soon for new cybersecurity challenges!
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
