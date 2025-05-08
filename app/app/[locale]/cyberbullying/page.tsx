import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import ListChallenges from '@/components/ListChallenges';
import Header from '@/components/Header';

async function CyberbullyingChallenges() {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('cyberbullying');

  return (
    <main>
      <Header />
      <ListChallenges 
        challenges={challenges} 
        userId={session?.user?.id}
        categoryName="Cyberbullying" 
      />
    </main>
  );
}

export default function CyberbullyingPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <CyberbullyingChallenges />
    </Suspense>
  );
}