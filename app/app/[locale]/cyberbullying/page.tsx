import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import ListChallenges from '@/components/ListChallenges';

async function CyberbullyingChallenges() {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('cyberbullying');

  return (
    <ListChallenges 
      challenges={challenges} 
      userId={session?.user?.id}
      categoryName="Cyberbullying" 
    />
  );
}

export default function CyberbullyingPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <CyberbullyingChallenges />
    </Suspense>
  );
}