'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useParams } from 'next/navigation';
import { Challenge } from '@lib/types';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { useChallenges } from '@lib/hooks/useChallenges';
import { AIFeedback } from './AIFeedback';
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

interface ChallengeListProps {
  challenges: Challenge[];
  userId?: string;
}

export const RenderChallenge: React.FC<ChallengeListProps> = ({ challenges, userId }) => {
  const router = useRouter();
  const params = useParams();
  const locale = (params?.locale as string) || 'en';
  const { data: session } = useSession();
  
  // Enhanced progress persistence
  const { 
    progress: persistedProgress,
    isLoadingProgress,
    submitProgress,
    isSubmitting,
    getCategoryProgress,
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

  const {
    currentChallenge,
    progress,
    selectedOption,
    isAnswered,
    isCorrect,
    loading,
    isLastChallenge,
    handleOptionSelect,
    handleSubmit: originalHandleSubmit,
    handleNext,
    getOptionClassName
  } = useChallenges({
    challenges,
    userId,
    onComplete: () => router.push('/')
  });

  // Enhanced submit handler using new persistence system
  const handleSubmit = async () => {
    if (!selectedOption || !currentChallenge) return;

    try {
      await submitProgress.mutateAsync({
        challengeId: currentChallenge.id,
        optionId: selectedOption,
        isCompleted: true,
      });
      
      // Continue with original submit logic for UI updates
      await originalHandleSubmit();
    } catch (error) {
      console.error('Enhanced submit failed, falling back to original:', error);
      // Fallback to original submit if enhanced version fails
      await originalHandleSubmit();
    }
  };

  // Calculate category progress
  const categoryProgress = React.useMemo(() => {
    const challengeIds = challenges.map(c => c.id);
    return getCategoryProgress(challengeIds);
  }, [challenges, getCategoryProgress]);

  // Find the selected option object
  const selectedOptionObject = currentChallenge?.options?.find(
    option => option.id === selectedOption
  ) || null;
  
  // Find the correct option object
  const correctOptionObject = currentChallenge?.options?.find(
    option => option.is_correct
  ) || null;

  if (!currentChallenge) {
    return (
      <div className="p-6 text-center">
        <h2 className="text-xl font-bold mb-4">No challenges available</h2>
        <p>Check back later for new challenges!</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-3xl mx-auto">
      {/* Simple Challenge Counter */}
      <div className="mb-4 p-3 bg-white border-4 border-black rounded-sm shadow-[4px_4px_0_0_#000]">
        <span className="font-bold text-sm uppercase tracking-wider">
          Challenge {progress.current} of {progress.total}
        </span>
      </div>

      <Card className="mb-6 p-6">
        <h2 className="text-xl font-bold mb-4">
          {currentChallenge.i18n?.[locale]?.title || currentChallenge.title}
        </h2>
        {(currentChallenge.i18n?.[locale]?.description || currentChallenge.description) && (
          <p className="mb-6 text-gray-700">
            {currentChallenge.i18n?.[locale]?.description || currentChallenge.description}
          </p>
        )}       
        <div className="space-y-4">
          {currentChallenge.options?.map(option => (
            <div 
              key={option.id}
              className={`p-4 border-4 border-black cursor-pointer transition-all duration-200 font-semibold
                ${selectedOption === option.id 
                  ? 'bg-blue-500 text-white shadow-[6px_6px_0px_0px_#000000] transform translate-x-1 translate-y-1' 
                  : 'bg-white hover:bg-gray-50 shadow-[4px_4px_0px_0px_#000000] hover:shadow-[6px_6px_0px_0px_#000000] hover:transform hover:translate-x-1 hover:translate-y-1'
                }
                ${getOptionClassName(option)}`}
              onClick={() => handleOptionSelect(option.id)}
            >
              <div className="flex items-start gap-4">
                <div 
                  className={`w-6 h-6 border-4 border-black flex items-center justify-center mt-0.5 font-black text-lg
                    ${selectedOption === option.id ? 'bg-white text-blue-500' : 'bg-gray-100'}`}
                >
                  {selectedOption === option.id && '✓'}
                </div>
                <div className="flex-1 text-lg leading-relaxed">
                  {option.i18n?.[locale]?.content || option.content}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 flex justify-end gap-3">
          {!isAnswered ? (
            <button 
              onClick={handleSubmit}
              disabled={!selectedOption || loading}
              className={`px-8 py-4 font-black text-lg uppercase tracking-wider border-4 border-black shadow-[8px_8px_0px_0px_#000000] hover:shadow-[4px_4px_0px_0px_#000000] transform hover:translate-x-1 hover:translate-y-1 transition-all duration-200 ${
                !selectedOption || loading 
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              }`}
            >
              {loading ? 'SUBMITTING...' : 'SUBMIT ANSWER'}
            </button>
          ) : (
            <button 
              onClick={handleNext}
              className="px-8 py-4 font-black text-lg uppercase tracking-wider bg-green-500 text-white border-4 border-black shadow-[8px_8px_0px_0px_#000000] hover:shadow-[4px_4px_0px_0px_#000000] transform hover:translate-x-1 hover:translate-y-1 transition-all duration-200 hover:bg-green-600"
            >
              {isLastChallenge ? 'FINISH' : 'NEXT CHALLENGE'}
            </button>
          )}
        </div>

        {isAnswered && (
          <div className={`mt-6 p-4 border-4 border-black shadow-[4px_4px_0px_0px_#000000] ${
            isCorrect 
              ? 'bg-green-500 text-white' 
              : 'bg-red-500 text-white'
          }`}>
            <p className="font-black text-lg uppercase tracking-wider">
              {isCorrect 
                ? '✓ CORRECT! WELL DONE!' 
                : '✗ INCORRECT - LEARN FROM THIS!'}
            </p>
            {!isCorrect && (
              <p className="font-semibold text-sm mt-2 normal-case tracking-normal">
                Try to understand why the correct answer is better.
              </p>
            )}
          </div>
        )}
      </Card>
      
      {/* AIFeedback component */}
      {isAnswered && selectedOptionObject && correctOptionObject && (
        <AIFeedback
          challenge={currentChallenge}
          selectedOption={selectedOptionObject}
          correctOption={correctOptionObject}
          isAnswered={isAnswered}
        />
      )}
    </div>
  );
};
