import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '../../../../lib/auth';
import { supabase } from '../../../../lib/supabase.js';

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Check if user is admin
    const { data: adminUser, error: adminError } = await supabase
      .from('admin_users')
      .select('id')
      .eq('user_id', session.user.id)
      .single();

    if (adminError || !adminUser) {
      return NextResponse.json({ error: 'Access denied' }, { status: 403 });
    }

    const url = new URL(request.url);
    const status = url.searchParams.get('status') || 'pending';

    // Get pending challenges with user and category information
    const { data: pendingChallenges, error } = await supabase
      .from('pending_challenges')
      .select(`
        *,
        submitted_by_user:users!pending_challenges_submitted_by_user_id_fkey(name, email),
        assigned_category:challenge_categories!pending_challenges_assigned_category_id_fkey(name, slug)
      `)
      .eq('status', status)
      .order('submitted_at', { ascending: false });

    if (error) {
      console.error('Error fetching pending challenges:', error);
      return NextResponse.json({ error: 'Failed to fetch questions' }, { status: 500 });
    }

    return NextResponse.json({ questions: pendingChallenges });

  } catch (error) {
    console.error('Error in admin questions API:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
