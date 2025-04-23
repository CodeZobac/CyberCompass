'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Challenge } from '@lib/types';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { useChallenges } from '@lib/hooks/useChallenges';

interface ChallengeListProps {
  challenges: Challenge[];
  userId?: string;
}

export const ChallengeList: React.FC<ChallengeListProps> = ({ challenges, userId }) => {
  const router = useRouter();
  
  const {
    currentChallenge,
    progress,
    selectedOption,
    isAnswered,
    isCorrect,
    loading,
    isLastChallenge,
    handleOptionSelect,
    handleSubmit,
    handleNext,
    getOptionClassName
  } = useChallenges({
    challenges,
    userId,
    onComplete: () => router.push('/')
  });

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
      <div className="mb-4 text-sm text-gray-500">
        Challenge {progress.current} of {progress.total}
      </div>

      <Card className="mb-6 p-6">
        <h2 className="text-xl font-bold mb-4">{currentChallenge.title}</h2>
        {currentChallenge.description && (
          <p className="mb-6 text-gray-700">{currentChallenge.description}</p>
        )}       
        <div className="space-y-3">
          {currentChallenge.options?.map(option => (
            <div 
              key={option.id}
              className={`p-4 border rounded-lg cursor-pointer transition-all
                ${selectedOption === option.id ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-300'}
                ${getOptionClassName(option)}`}
              onClick={() => handleOptionSelect(option.id)}
            >
              <div className="flex items-start gap-3">
                <div 
                  className={`w-5 h-5 rounded-full flex items-center justify-center mt-0.5 border
                    ${selectedOption === option.id ? 'bg-blue-500 border-blue-500' : 'border-gray-400'}`}
                >
                  {selectedOption === option.id && (
                    <div className="w-2 h-2 rounded-full bg-white"></div>
                  )}
                </div>
                <div>{option.content}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 flex justify-end gap-3">
          {!isAnswered ? (
            <Button 
              onClick={handleSubmit}
              disabled={!selectedOption || loading}
            >
              {loading ? 'Submitting...' : 'Submit Answer'}
            </Button>
          ) : (
            <Button onClick={handleNext}>
              {isLastChallenge ? 'Finish' : 'Next Challenge'}
            </Button>
          )}
        </div>

        {isAnswered && (
          <div className={`mt-4 p-4 rounded-lg ${isCorrect ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
            <p className="font-medium">
              {isCorrect 
                ? 'Correct! Well done!' 
                : 'Incorrect. Try to understand why the correct answer is better.'}
            </p>
          </div>
        )}
      </Card>
    </div>
  );
};