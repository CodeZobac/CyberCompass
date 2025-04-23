import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { ChallengeList } from '@/components/ChallengeList';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';

async function CyberbullyingChallenges() {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('cyberbullying');

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Cyberbullying Challenges</h1>
      <p className="mb-8 text-gray-700">
        Learn about cyberbullying, how to recognize it, and what to do if you or someone you know is being cyberbullied.
        Complete these challenges to understand how to create safer online environments.
      </p>
      
      <ChallengeList 
        challenges={challenges} 
        userId={session?.user?.id} 
      />
    </div>
  );
}

export default function CyberbullyingPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <CyberbullyingChallenges />
    </Suspense>
  );
}