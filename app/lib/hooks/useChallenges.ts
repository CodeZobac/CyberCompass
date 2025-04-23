'use client';

import { useState } from 'react';
import { Challenge, ChallengeOption } from '@lib/types';

export interface UseChallengesOptions {
  challenges: Challenge[];
  userId?: string;
  onComplete?: () => void;
}

export interface UseChallengesResult {
  currentChallenge: Challenge | null;
  currentChallengeIndex: number;
  isLastChallenge: boolean;
  selectedOption: string | null;
  isAnswered: boolean;
  isCorrect: boolean;
  loading: boolean;
  progress: {
    current: number;
    total: number;
    percentage: number;
  };
  handleOptionSelect: (optionId: string) => void;
  handleSubmit: () => Promise<void>;
  handleNext: () => void;
  isOptionCorrect: (option: ChallengeOption) => boolean | undefined;
  getOptionClassName: (option: ChallengeOption) => string;
}

export function useChallenges({
  challenges,
  userId,
  onComplete
}: UseChallengesOptions): UseChallengesResult {
  const [currentChallengeIndex, setCurrentChallengeIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const currentChallenge = challenges.length > 0 ? challenges[currentChallengeIndex] : null;
  const isLastChallenge = currentChallengeIndex === challenges.length - 1;

  const handleOptionSelect = (optionId: string) => {
    if (isAnswered) return;
    setSelectedOption(optionId);
  };

  const handleSubmit = async () => {
    if (!selectedOption || !userId || !currentChallenge) return;
    
    setLoading(true);
    
    try {
      // API call to submit answer
      const response = await fetch('/api/challenges', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          challengeId: currentChallenge.id,
          optionId: selectedOption,
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to submit answer');
      }
      
      const result = await response.json();
      setIsAnswered(true);
      setIsCorrect(result.isCorrect);
    } catch (error) {
      console.error('Error submitting challenge answer:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    if (isLastChallenge) {
      onComplete?.();
      return;
    }
    
    setCurrentChallengeIndex(prev => prev + 1);
    setSelectedOption(null);
    setIsAnswered(false);
    setIsCorrect(false);
  };

  const isOptionCorrect = (option: ChallengeOption): boolean | undefined => {
    if (!isAnswered) return undefined;
    return option.is_correct;
  };

  const getOptionClassName = (option: ChallengeOption): string => {
    if (!isAnswered) return '';
    if (option.id === selectedOption) {
      return option.is_correct ? 'bg-green-100 border-green-500' : 'bg-red-100 border-red-500';
    }
    return option.is_correct ? 'bg-green-50 border-green-300' : '';
  };

  // Calculate progress
  const progress = {
    current: currentChallengeIndex + 1,
    total: challenges.length,
    percentage: challenges.length > 0 
      ? Math.round(((currentChallengeIndex + 1) / challenges.length) * 100) 
      : 0
  };

  return {
    currentChallenge,
    currentChallengeIndex,
    isLastChallenge,
    selectedOption,
    isAnswered,
    isCorrect,
    loading,
    progress,
    handleOptionSelect,
    handleSubmit,
    handleNext,
    isOptionCorrect,
    getOptionClassName,
  };
}