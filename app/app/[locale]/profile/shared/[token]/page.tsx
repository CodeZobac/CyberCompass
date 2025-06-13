import { Suspense } from 'react';
import { getTranslations } from 'next-intl/server';
import { redirect } from 'next/navigation';
import { getServerSession } from 'next-auth';
import { authOptions } from '../../../../../lib/auth';
import { SharedProfileDashboard } from './components/SharedProfileDashboard';

interface SharedProfilePageProps {
  params: {
    token: string;
    locale: string;
  };
}

export default async function SharedProfilePage({ params }: SharedProfilePageProps) {
  const session = await getServerSession(authOptions);
  const t = await getTranslations('profile');

  if (!session?.user) {
    redirect('/auth/signin');
  }

  const { token } = params;

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-4">
            <div className="bg-blue-100 border-4 border-black shadow-brutal p-3 rounded-lg">
              <span className="text-2xl">🔗</span>
            </div>
            <div>
              <h1 className="text-4xl font-black text-black mb-2 text-shadow-brutal">
                {t('sharedProfile')}
              </h1>
              <p className="text-lg text-gray-700 font-medium">
                {t('sharedProfileSubtitle')}
              </p>
            </div>
          </div>
          <div className="bg-yellow-50 border-4 border-yellow-400 shadow-brutal p-4 rounded-lg">
            <p className="text-sm font-bold text-yellow-800">
              📋 {t('sharedProfileNotice')}
            </p>
          </div>
        </div>
        
        <Suspense fallback={
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Loading skeleton */}
            <div className="lg:col-span-2 space-y-6">
              <div className="bg-white border-4 border-black shadow-brutal h-64 animate-pulse" />
              <div className="bg-white border-4 border-black shadow-brutal h-96 animate-pulse" />
            </div>
            <div className="space-y-6">
              <div className="bg-white border-4 border-black shadow-brutal h-32 animate-pulse" />
              <div className="bg-white border-4 border-black shadow-brutal h-48 animate-pulse" />
              <div className="bg-white border-4 border-black shadow-brutal h-64 animate-pulse" />
            </div>
          </div>
        }>
          <SharedProfileDashboard token={token} />
        </Suspense>
      </div>
    </div>
  );
}
