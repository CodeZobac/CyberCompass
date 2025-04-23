import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { ChallengeList } from '@/components/ChallengeList';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';

async function CatfishingChallenges() {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('catfishing');

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Catfishing Challenges</h1>
      <p className="mb-8 text-gray-700">
        Learn how to identify and avoid catfishing scams by completing these challenges.
        Catfishing is when someone creates a false online identity to deceive others.
      </p>
      
      <ChallengeList 
        challenges={challenges} 
        userId={session?.user?.id} 
      />
    </div>
  );
}

export default function CatfishingPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <CatfishingChallenges />
    </Suspense>
  );
}