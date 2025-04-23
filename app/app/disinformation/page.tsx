import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { ChallengeList } from '@/components/ChallengeList';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';

async function DisinformationChallenges() {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('disinformation');

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Disinformation Challenges</h1>
      <p className="mb-8 text-gray-700">
        Learn how to identify and combat disinformation - false information deliberately spread to deceive people.
        Complete these challenges to develop critical thinking skills for evaluating information online.
      </p>
      
      <ChallengeList 
        challenges={challenges} 
        userId={session?.user?.id} 
      />
    </div>
  );
}

export default function DisinformationPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <DisinformationChallenges />
    </Suspense>
  );
}