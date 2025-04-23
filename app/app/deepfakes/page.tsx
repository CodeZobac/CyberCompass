/* eslint-disable react/no-unescaped-entities */
import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { ChallengeList } from '@/components/ChallengeList';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';

async function DeepfakesChallenges() {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('deepfakes');

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Deepfakes Challenges</h1>
      <p className="mb-8 text-gray-700">
        Learn how to identify and respond to deepfakes - manipulated media that uses AI to replace 
        someone's likeness or voice with someone else's. Complete these challenges to protect yourself 
        and others from this evolving threat.
      </p>
      
      <ChallengeList 
        challenges={challenges} 
        userId={session?.user?.id} 
      />
    </div>
  );
}

export default function DeepfakesPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <DeepfakesChallenges />
    </Suspense>
  );
}