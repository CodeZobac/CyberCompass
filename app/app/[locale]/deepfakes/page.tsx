/* eslint-disable react/no-unescaped-entities */
import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import ListChallenges from '@/components/ListChallenges';

async function DeepfakesChallenges() {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('deepfakes');

  return (
    <ListChallenges 
      challenges={challenges} 
      userId={session?.user?.id}
      categoryName="Deepfakes" 
    />
  );
}

export default function DeepfakesPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <DeepfakesChallenges />
    </Suspense>
  );
}