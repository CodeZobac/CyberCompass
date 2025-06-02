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

async function DisinformationChallenges({ locale }: { locale: string }) {
  const session = await getServerSession(authOptions);
  const challenges = await getChallengesByCategorySlug('disinformation', locale);

  return (
    <main>
      <Header />
      <ListChallenges 
        challenges={challenges} 
        userId={session?.user?.id}
        categoryName="Disinformation" 
      />
      <Footer />
    </main>
  );
}

export default function DisinformationPage({ params: { locale } }: PageProps) {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <DisinformationChallenges locale={locale} />
    </Suspense>
  );
}
