'use client';

import { useState, useEffect, useCallback } from 'react'; // Import useCallback
import * as React from 'react'; // Import React for React.useCallback
import { useParams } from 'next/navigation'; // Import useParams
import { Challenge, ChallengeOption } from '@lib/types';

interface AIFeedbackProps {
  challenge: Challenge | null;
  selectedOption: ChallengeOption | null;
  correctOption: ChallengeOption | null;
  isAnswered: boolean;
}

export function AIFeedback({ 
  challenge, 
  selectedOption, 
  correctOption, 
  isAnswered 
}: AIFeedbackProps) {
  const [feedback, setFeedback] = useState<string>('');
  const [displayedFeedback, setDisplayedFeedback] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState<number>(0);
  const params = useParams(); // Get URL parameters

  // Define generateFallbackFeedback before the useEffect that uses it
  const generateFallbackFeedback = useCallback(() => {
    const isCorrectAnswer = selectedOption?.is_correct;
    
    if (isCorrectAnswer) {
      setFeedback(`Great job! You correctly selected "${selectedOption?.content}". This demonstrates your understanding of this cybersecurity concept.`);
    } else {
      setFeedback(`The correct answer is "${correctOption?.content}". Understanding the difference between your selected answer and the correct one will help deepen your cybersecurity knowledge.`);
    }
  }, [selectedOption, correctOption, setFeedback]);

  // Only fetch feedback when the question has been answered
  useEffect(() => {
    if (!isAnswered || !selectedOption || !correctOption || !challenge) {
      return;
    }

    const fetchFeedback = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await fetch('/api/ai-feedback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            selectedOption: selectedOption.content,
            correctOption: correctOption.content,
            challengeTitle: challenge.title,
            challengeDescription: challenge.description,
            locale: params.locale // Add locale to the request body
          }),
          // Add timeout to prevent long-hanging requests
          signal: AbortSignal.timeout(10000)
        });

        if (!response.ok) {
          throw new Error('Failed to fetch AI feedback');
        }

        const data = await response.json();
        setFeedback(data.feedback || 'No feedback available at this time.');
      } catch (err) {
        console.error('Error fetching AI feedback:', err);
        const errorMessage = err instanceof Error ? err.message : 'Unknown error';
        
        // Specifically check for timeout or server unreachable issues
        if (errorMessage.includes('timeout') || errorMessage.includes('Failed to fetch')) {
          setError('Could not connect to the AI service. It may not be running.');
        } else {
          setError('Could not generate feedback at this time. Please try again later.');
        }
        
        // Generate fallback feedback
        generateFallbackFeedback();
      } finally {
        setLoading(false);
      }
    };

    fetchFeedback();
  }, [isAnswered, selectedOption, correctOption, challenge, retryCount, params.locale, generateFallbackFeedback]);

  // Retry button handler
  const handleRetry = () => {
    setRetryCount(prev => prev + 1);
  };

  // Generative text effect
  useEffect(() => {
    if (!feedback || loading) {
      return;
    }

    let index = 0;
    setDisplayedFeedback('');
    const interval = setInterval(() => {
      if (index <= feedback.length) {
        setDisplayedFeedback(feedback.substring(0, index));
        index++;
      } else {
        clearInterval(interval);
      }
    }, 20); // Adjust speed as needed

    return () => clearInterval(interval);
  }, [feedback, loading]);

  if (!isAnswered) {
    return null;
  }

  return (
    <div className="mt-6 p-5 border-2 border-black rounded-lg bg-white">
      <h3 className="text-lg font-bold mb-2 flex items-center">
        <span className="mr-2">🤖</span>
        AI Assistant Feedback
      </h3>
      
      {loading && (
        <div className="flex items-center space-x-2">
          <div className="animate-pulse h-3 w-3 rounded-full bg-black"></div>
          <div className="animate-pulse h-3 w-3 rounded-full bg-black" style={{ animationDelay: '0.2s' }}></div>
          <div className="animate-pulse h-3 w-3 rounded-full bg-black" style={{ animationDelay: '0.4s' }}></div>
          <span className="ml-2">Generating feedback...</span>
        </div>
      )}
      
      {error && !loading && (
        <div className="text-red-600 mb-3">
          {error}
          <button 
            onClick={handleRetry}
            className="ml-3 px-3 py-1 text-sm bg-black text-white rounded-md hover:bg-gray-800"
          >
            Retry
          </button>
        </div>
      )}
      
      {!loading && (
        <div className="prose max-w-none min-h-[60px]">
          {displayedFeedback || ' '} 
          {displayedFeedback !== feedback && !loading && (
            <span className="animate-pulse">|</span>
          )}
        </div>
      )}
    </div>
  );
}
