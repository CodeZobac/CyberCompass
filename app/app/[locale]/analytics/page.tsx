/**
 * Analytics Dashboard Page
 * Comprehensive learning analytics and progress tracking
 */

import { AnalyticsDashboard } from '@/components/AnalyticsDashboard';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { redirect } from 'next/navigation';

interface PageProps {
  params: Promise<{
    locale: string;
  }>;
}

export default async function AnalyticsPage({ params }: PageProps) {
  const session = await getServerSession(authOptions);
  const { locale } = await params;

  // Redirect to sign-in if not authenticated
  if (!session?.user) {
    redirect(`/${locale}/auth/signin?callbackUrl=/${locale}/analytics`);
  }

  return (
    <div className="min-h-screen bg-white py-12 px-4">
      <div className="container mx-auto">
        {/* Analytics Dashboard Component */}
        <AnalyticsDashboard
          locale={locale}
          userId={session.user.id}
        />
      </div>
    </div>
  );
}
