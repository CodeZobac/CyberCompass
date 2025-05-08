import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import ListChallenges from '@/components/ListChallenges';

async function DisinformationChallenges() {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('disinformation');

  return (
    <ListChallenges 
      challenges={challenges} 
      userId={session?.user?.id}
      categoryName="Disinformation" 
    />
  );
}

export default function DisinformationPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <DisinformationChallenges />
    </Suspense>
  );
}