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

async function DeepfakesChallenges({ locale }: { locale: string }) {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('deepfakes', locale);

  return (
    <main>
      <Header />
      <ListChallenges 
        challenges={challenges} 
        userId={session?.user?.id}
        categoryName="Deepfakes" 
      />
      <Footer />
    </main>
  );
}

export default function DeepfakesPage({ params: { locale } }: PageProps) {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <DeepfakesChallenges locale={locale} />
    </Suspense>
  );
}
