import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import ListChallenges from '@/components/ListChallenges';
import Header from '@/components/Header';

async function CatfishingChallenges() {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('catfishing');

  return (
    <main>
		<Header />
		<ListChallenges 
		challenges={challenges} 
		userId={session?.user?.id}
		categoryName="Catfishing" 
		/>
	</main>
  );
}

export default function CatfishingPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <CatfishingChallenges />
    </Suspense>
  );
}