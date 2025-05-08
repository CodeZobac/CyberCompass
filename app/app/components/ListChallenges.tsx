'use client';

import React, { useState } from 'react';
import { Challenge } from '@lib/types';
import { useRouter } from 'next/navigation';
import { 
  ResizablePanelGroup, 
  ResizablePanel, 
  ResizableHandle 
} from '@/components/ui/resizable';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { RenderChallenge } from '@/components/RenderChallenge';

interface ListChallengesProps {
  challenges: Challenge[];
  userId?: string;
  categoryName: string;
}

export default function ListChallenges({ challenges, userId, categoryName }: ListChallengesProps) {
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);
  const router = useRouter();

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
        bg: 'bg-green-100',
        text: 'text-green-800',
        hoverBg: 'hover:bg-green-50'
      };
      case 2: return {
        bg: 'bg-yellow-100',
        text: 'text-yellow-800',
        hoverBg: 'hover:bg-yellow-50'
      };
      case 3: return {
        bg: 'bg-red-100',
        text: 'text-red-800',
        hoverBg: 'hover:bg-red-50'
      };
      default: return {
        bg: 'bg-gray-100',
        text: 'text-gray-800',
        hoverBg: 'hover:bg-gray-50'
      };
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">{categoryName} Challenges</h1>
      
      {selectedChallenge ? (
        <>
          <Button 
            variant="outline" 
            onClick={handleBackToList} 
            className="mb-4 border-2 border-black"
          >
            ← Back to Challenge List
          </Button>
          <RenderChallenge 
            challenges={[selectedChallenge]} 
            userId={userId} 
          />
        </>
      ) : (
        <div className="max-w-5xl mx-auto">
          <div className="p-6 mb-6 bg-black text-white rounded-lg shadow-md border-2 border-black">
            <h2 className="text-2xl font-bold mb-2">Select a Challenge</h2>
            <p className="text-gray-300">
              Choose a challenge from the list below to begin your learning journey.
              Each challenge is designed to test and strengthen your knowledge.
            </p>
          </div>

          <ResizablePanelGroup 
            direction="vertical" 
            className="min-h-[500px] max-h-[700px] border-2 border-black rounded-lg overflow-hidden"
          >
            <ResizablePanel defaultSize={30} minSize={20}>
              <div className="p-4 h-full overflow-auto bg-bg align-center">
                <h2 className="text-xl font-semibold mb-4 border-b-2 border-black pb-2">Available Challenges</h2>
                <div className="space-y-3">
                  {challenges.map((challenge) => {
                    const colors = getDifficultyColors(challenge.difficulty as number);
                    return (
                      <Card 
                        key={challenge.id}
                        className={`p-5 cursor-pointer border-2 border-black 
                          transition-colors ${colors.hoverBg} mb-4`}
                        onClick={() => handleSelectChallenge(challenge)}
                      >
                        <h3 className="font-bold text-lg">{challenge.title}</h3>
                        {challenge.difficulty && (
                          <div className="mt-3 text-sm">
                            <span className={`
                              px-3 py-1.5 rounded-full ${colors.bg} ${colors.text}
                            `}>
                              {challenge.difficulty === 1 ? 'Easy' : 
                              challenge.difficulty === 2 ? 'Medium' : 
                              challenge.difficulty === 3 ? 'Hard' : 'Unknown'}
                            </span>
                          </div>
                        )}
                      </Card>
                    )}
                  )}
                </div>
              </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        </div>
      )}
    </div>
  );
}