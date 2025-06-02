import { getTranslations } from 'next-intl/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '../../../lib/auth';
import { redirect } from 'next/navigation';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { supabase } from '../../../lib/supabase.js';
import Header from '../../components/Header';

// Check admin status by querying the Supabase admin_users table
async function checkAdminStatus(userId: string) {
  try {
    console.log(`Checking admin status for user: ${userId}`);
    
    // Query the admin_users table to check if user is an admin
    const { data: adminUser, error } = await supabase
      .from('admin_users')
      .select('is_root_admin, can_manage_admins')
      .eq('user_id', userId)
      .single();

    if (error || !adminUser) {
      console.log('User is not an admin:', error?.message);
      return { isAdmin: false, isRootAdmin: false };
    }

    console.log('Admin status found:', adminUser);
    return { 
      isAdmin: true, 
      isRootAdmin: adminUser.is_root_admin,
      canManageAdmins: adminUser.can_manage_admins
    };
  } catch (error) {
    console.error('Error checking admin status:', error);
    return { isAdmin: false, isRootAdmin: false };
  }
}

export default async function AdminDashboard({
  params
}: {
  params: Promise<{ locale: string }>
}) {
  const { locale } = await params;
  const session = await getServerSession(authOptions);
  const t = await getTranslations({ locale, namespace: 'admin.dashboard' });
  const tActions = await getTranslations({ locale, namespace: 'admin.dashboard.actions' });
  const tStatus = await getTranslations({ locale, namespace: 'admin.status' });

  if (!session?.user?.id) {
    redirect('/auth/signin');
  }

  const adminStatus = await checkAdminStatus(session.user.id);
  
  if (!adminStatus.isAdmin) {
    redirect('/');
  }

  // Mock statistics - in production these would come from Supabase
  const stats = {
    pending: 5,
    approved: 42,
    rejected: 8
  };

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
      {/* Header Section */}
      <div className="bg-white border-b-4 border-black shadow-[0_4px_0_0_#000]">
        <div className="container mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-black text-gray-900 mb-2 tracking-tight">
                {t('title')}
              </h1>
              <p className="text-lg text-gray-600 max-w-2xl">
                {t('welcome')}
              </p>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              <div className="bg-green-100 border-2 border-green-600 rounded-lg px-4 py-2">
                <span className="text-green-800 font-semibold text-sm uppercase tracking-wider">
                  ✅ {tStatus('active')}
                </span>
              </div>
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full border-4 border-black shadow-[4px_4px_0_0_#000] flex items-center justify-center">
                <span className="text-white font-bold text-lg">👤</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-12">
        {/* Enhanced Statistics Dashboard */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            📊 {tStatus('overview')}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Pending Stats Card */}
            <div className="group relative">
              <Card className="p-8 bg-gradient-to-br from-orange-50 to-yellow-50 border-4 border-orange-400 shadow-[8px_8px_0_0_#fb923c] hover:shadow-[4px_4px_0_0_#fb923c] hover:translate-x-1 hover:translate-y-1 transition-all duration-200">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-orange-500 rounded-lg border-2 border-black flex items-center justify-center">
                    <span className="text-white text-xl font-bold">⏳</span>
                  </div>
                  <div className="bg-orange-200 border-2 border-orange-600 rounded-full px-3 py-1">
                    <span className="text-orange-800 font-bold text-xs uppercase tracking-wider">
                      {tStatus('urgent')}
                    </span>
                  </div>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2 uppercase tracking-wide">
                  {t('stats.pending')}
                </h3>
                <p className="text-4xl font-black text-orange-600 mb-2">{stats.pending}</p>
                <p className="text-sm text-orange-700 font-medium">
                  {tStatus('requireAttention')}
                </p>
              </Card>
            </div>

            {/* Approved Stats Card */}
            <div className="group relative">
              <Card className="p-8 bg-gradient-to-br from-green-50 to-emerald-50 border-4 border-green-400 shadow-[8px_8px_0_0_#4ade80] hover:shadow-[4px_4px_0_0_#4ade80] hover:translate-x-1 hover:translate-y-1 transition-all duration-200">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-green-500 rounded-lg border-2 border-black flex items-center justify-center">
                    <span className="text-white text-xl font-bold">✅</span>
                  </div>
                  <div className="bg-green-200 border-2 border-green-600 rounded-full px-3 py-1">
                    <span className="text-green-800 font-bold text-xs uppercase tracking-wider">
                      {tStatus('success')}
                    </span>
                  </div>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2 uppercase tracking-wide">
                  {t('stats.approved')}
                </h3>
                <p className="text-4xl font-black text-green-600 mb-2">{stats.approved}</p>
                <p className="text-sm text-green-700 font-medium">
                  {tStatus('publishedSuccessfully')}
                </p>
              </Card>
            </div>

            {/* Rejected Stats Card */}
            <div className="group relative">
              <Card className="p-8 bg-gradient-to-br from-red-50 to-pink-50 border-4 border-red-400 shadow-[8px_8px_0_0_#f87171] hover:shadow-[4px_4px_0_0_#f87171] hover:translate-x-1 hover:translate-y-1 transition-all duration-200">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-red-500 rounded-lg border-2 border-black flex items-center justify-center">
                    <span className="text-white text-xl font-bold">❌</span>
                  </div>
                  <div className="bg-red-200 border-2 border-red-600 rounded-full px-3 py-1">
                    <span className="text-red-800 font-bold text-xs uppercase tracking-wider">
                      {tStatus('rejected')}
                    </span>
                  </div>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2 uppercase tracking-wide">
                  {t('stats.rejected')}
                </h3>
                <p className="text-4xl font-black text-red-600 mb-2">{stats.rejected}</p>
                <p className="text-sm text-red-700 font-medium">
                  {tStatus('notApproved')}
                </p>
              </Card>
            </div>
          </div>
        </div>

        {/* Enhanced Quick Actions */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            🚀 {tStatus('quickActions')}
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Review Questions Action Card */}
            <div className="group relative">
              <Card className="p-8 bg-gradient-to-br from-blue-50 to-indigo-50 border-4 border-blue-400 shadow-[8px_8px_0_0_#3b82f6] hover:shadow-[12px_12px_0_0_#3b82f6] hover:translate-x-1 hover:translate-y-1 transition-all duration-300">
                <div className="flex items-start justify-between mb-6">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl border-4 border-black shadow-[4px_4px_0_0_#000] flex items-center justify-center">
                    <span className="text-white text-2xl font-bold">📝</span>
                  </div>
                  <div className="bg-blue-200 border-2 border-blue-600 rounded-full px-4 py-2">
                    <span className="text-blue-800 font-bold text-xs uppercase tracking-wider">
                      {stats.pending} {t('stats.pending')}
                    </span>
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3 uppercase tracking-wide">
                  {tActions('reviewQuestions')}
                </h3>
                <p className="text-gray-700 mb-6 text-lg leading-relaxed">
                  {tActions('reviewQuestionsDesc')}
                </p>
                <Button 
                  asChild 
                  variant="brutal" 
                  className="w-full text-lg font-bold tracking-wide uppercase"
                >
                  <a href={`/${locale}/admin/questions`}>
                    🔍 {tActions('reviewQuestions')}
                  </a>
                </Button>
              </Card>
            </div>

            {/* Manage Admins or Alternative Action Card */}
            {adminStatus.isRootAdmin || adminStatus.canManageAdmins ? (
              <div className="group relative">
                <Card className="p-8 bg-gradient-to-br from-purple-50 to-pink-50 border-4 border-purple-400 shadow-[8px_8px_0_0_#8b5cf6] hover:shadow-[12px_12px_0_0_#8b5cf6] hover:translate-x-1 hover:translate-y-1 transition-all duration-300">
                  <div className="flex items-start justify-between mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl border-4 border-black shadow-[4px_4px_0_0_#000] flex items-center justify-center">
                      <span className="text-white text-2xl font-bold">👥</span>
                    </div>
                    <div className="bg-purple-200 border-2 border-purple-600 rounded-full px-4 py-2">
                      <span className="text-purple-800 font-bold text-xs uppercase tracking-wider">
                        Admin
                      </span>
                    </div>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3 uppercase tracking-wide">
                    {tActions('manageAdmins')}
                  </h3>
                  <p className="text-gray-700 mb-6 text-lg leading-relaxed">
                    {tActions('manageAdminsDesc')}
                  </p>
                  <Button 
                    asChild 
                    variant="brutal" 
                    className="w-full text-lg font-bold tracking-wide uppercase bg-purple-500 hover:bg-purple-600"
                  >
                    <a href={`/${locale}/admin/users`}>
                      ⚙️ {tActions('manageAdmins')}
                    </a>
                  </Button>
                </Card>
              </div>
            ) : (
              <div className="group relative">
                <Card className="p-8 bg-gradient-to-br from-gray-50 to-slate-50 border-4 border-gray-400 shadow-[8px_8px_0_0_#6b7280] hover:shadow-[12px_12px_0_0_#6b7280] hover:translate-x-1 hover:translate-y-1 transition-all duration-300">
                  <div className="flex items-start justify-between mb-6">
                    <div className="w-16 h-16 bg-gradient-to-br from-gray-500 to-slate-600 rounded-xl border-4 border-black shadow-[4px_4px_0_0_#000] flex items-center justify-center">
                      <span className="text-white text-2xl font-bold">📊</span>
                    </div>
                    <div className="bg-gray-200 border-2 border-gray-600 rounded-full px-4 py-2">
                      <span className="text-gray-800 font-bold text-xs uppercase tracking-wider">
                        {tStatus('analytics')}
                      </span>
                    </div>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3 uppercase tracking-wide">
                    {tStatus('viewStatistics')}
                  </h3>
                  <p className="text-gray-700 mb-6 text-lg leading-relaxed">
                    {tStatus('detailedReports')}
                  </p>
                  <Button 
                    asChild 
                    variant="brutal-normal" 
                    className="w-full text-lg font-bold tracking-wide uppercase"
                  >
                    <a href="#statistics">
                      📈 {tStatus('viewStatistics')}
                    </a>
                  </Button>
                </Card>
              </div>
            )}
          </div>
        </div>

        {/* Recent Activity Section */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            📈 {tStatus('recentActivity')}
          </h2>
          <Card className="p-8 bg-gradient-to-br from-white to-gray-50 border-4 border-gray-300 shadow-[8px_8px_0_0_#9ca3af]">
            <div className="space-y-4">
              <div className="flex items-center space-x-4 p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
                <div className="w-10 h-10 bg-blue-500 rounded-full border-2 border-black flex items-center justify-center">
                  <span className="text-white font-bold">📝</span>
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-gray-900">
                    {tStatus('newQuestionSubmitted')}
                  </p>
                  <p className="text-sm text-gray-600">
                    há 2 {tStatus('minutesAgo')}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4 p-4 bg-green-50 border-l-4 border-green-500 rounded">
                <div className="w-10 h-10 bg-green-500 rounded-full border-2 border-black flex items-center justify-center">
                  <span className="text-white font-bold">✅</span>
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-gray-900">
                    {tStatus('questionApproved')}
                  </p>
                  <p className="text-sm text-gray-600">
                    há 15 {tStatus('minutesAgo')}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4 p-4 bg-orange-50 border-l-4 border-orange-500 rounded">
                <div className="w-10 h-10 bg-orange-500 rounded-full border-2 border-black flex items-center justify-center">
                  <span className="text-white font-bold">⏳</span>
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-gray-900">
                    {tStatus('pendingReview')}
                  </p>
                  <p className="text-sm text-gray-600">
                    há 1 {tStatus('hourAgo')}
                  </p>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
    </>
  );
}
