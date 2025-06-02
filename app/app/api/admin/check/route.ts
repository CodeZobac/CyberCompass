import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { supabase } from '@lib/supabase.js';

export async function GET() {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json({ isAdmin: false, isRootAdmin: false });
    }

    // Check if user is an admin
    const { data: adminUser, error } = await supabase
      .from('admin_users')
      .select('is_root_admin, can_manage_admins')
      .eq('user_id', session.user.id)
      .single();

    if (error || !adminUser) {
      return NextResponse.json({ isAdmin: false, isRootAdmin: false });
    }

    return NextResponse.json({ 
      isAdmin: true, 
      isRootAdmin: adminUser.is_root_admin,
      canManageAdmins: adminUser.can_manage_admins
    });

  } catch (error) {
    console.error('Error checking admin status:', error);
    return NextResponse.json({ isAdmin: false, isRootAdmin: false }, { status: 500 });
  }
}
