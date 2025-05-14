import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import ListChallenges from '@/components/ListChallenges';
import Header from '@/components/Header';

interface PageProps {
  params: {
    locale: string;
  };
}

async function CyberbullyingChallenges({ locale }: { locale: string }) {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('cyberbullying', locale);

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

export default function CyberbullyingPage({ params: { locale } }: PageProps) {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <CyberbullyingChallenges locale={locale} />
    </Suspense>
  );
}
