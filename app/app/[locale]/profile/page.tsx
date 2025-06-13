import { Suspense } from 'react';
import { getTranslations } from 'next-intl/server';
import { redirect } from 'next/navigation';
import { getServerSession } from 'next-auth';
import { authOptions } from '../../../lib/auth';
import { ProfileDashboard } from './components/ProfileDashboard';

export default async function ProfilePage() {
  const session = await getServerSession(authOptions);
  const t = await getTranslations('profile');

  if (!session?.user) {
    redirect('/auth/signin');
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-black text-black mb-2 text-shadow-brutal">
            {t('title', { name: session.user.name?.split(' ')[0] || 'User' })}
          </h1>
          <p className="text-lg text-gray-700 font-medium">
            {t('subtitle')}
          </p>
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
          <ProfileDashboard userId={session.user.id} />
        </Suspense>
      </div>
    </div>
  );
}
