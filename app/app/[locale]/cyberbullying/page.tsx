import { Suspense } from 'react';
import { getChallengesByCategorySlug } from '@lib/challenges';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import ListChallenges from '@/components/ListChallenges';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

// Force dynamic rendering to avoid build-time execution
export const dynamic = 'force-dynamic';

interface PageProps {
  params: Promise<{
    locale: string;
  }>;
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
      <Footer />
    </main>
  );
}

export default async function CyberbullyingPage({ params }: PageProps) {
  const { locale } = await params;
  
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading challenges...</div>}>
      <CyberbullyingChallenges locale={locale} />
    </Suspense>
  );
}
