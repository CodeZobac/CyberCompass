import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import ListChallenges from '@/components/ListChallenges';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

interface PageProps {
  params: {
    locale: string;
  };
}

async function CatfishingChallenges({ locale }: { locale: string }) {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('catfishing', locale);

  return (
    <main>
      <Header />
      <ListChallenges 
        challenges={challenges} 
        userId={session?.user?.id}
        categoryName="Catfishing" 
      />
      <Footer />
    </main>
  );
}

export default function CatfishingPage({ params: { locale } }: PageProps) {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <CatfishingChallenges locale={locale} />
    </Suspense>
  );
}
