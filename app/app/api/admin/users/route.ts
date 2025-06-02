import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { supabase } from '@lib/supabase.js';

// Check if user has permission to manage admins
async function checkAdminPermissions(userId: string) {
  const { data: adminUser, error } = await supabase
    .from('admin_users')
    .select('is_root_admin, can_manage_admins')
    .eq('user_id', userId)
    .single();

  if (error || !adminUser) {
    return { hasPermission: false, isRootAdmin: false };
  }

  return {
    hasPermission: adminUser.is_root_admin || adminUser.can_manage_admins,
    isRootAdmin: adminUser.is_root_admin
  };
}

// GET: List all admins
export async function GET() {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Check if user has permission to manage admins
    const permissions = await checkAdminPermissions(session.user.id);
    if (!permissions.hasPermission) {
      return NextResponse.json({ error: 'No permission to manage admins' }, { status: 403 });
    }

    // Get all admin users with their user details
    const { data: admins, error } = await supabase
      .from('admin_users')
      .select(`
        id,
        user_id,
        email,
        is_root_admin,
        can_manage_admins,
        created_at,
        added_by_admin_id,
        users:user_id (
          name,
          email
        ),
        added_by:added_by_admin_id (
          users:user_id (
            name,
            email
          )
        )
      `)
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching admins:', error);
      return NextResponse.json({ error: 'Failed to fetch admins' }, { status: 500 });
    }

    return NextResponse.json({ admins });

  } catch (error) {
    console.error('Error in GET /api/admin/users:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

// POST: Add new admin
export async function POST(request: Request) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Check if user has permission to manage admins
    const permissions = await checkAdminPermissions(session.user.id);
    if (!permissions.hasPermission) {
      return NextResponse.json({ error: 'No permission to manage admins' }, { status: 403 });
    }

    const { email, isRootAdmin = false, canManageAdmins = false } = await request.json();

    if (!email) {
      return NextResponse.json({ error: 'Email is required' }, { status: 400 });
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json({ error: 'Invalid email format' }, { status: 400 });
    }

    // Only root admins can create other root admins or admins with manage permissions
    if (!permissions.isRootAdmin && (isRootAdmin || canManageAdmins)) {
      return NextResponse.json({ 
        error: 'Only root admins can grant administrative privileges' 
      }, { status: 403 });
    }

    // Check if user exists in the users table
    const { data: existingUser, error: userError } = await supabase
      .from('users')
      .select('id, email')
      .eq('email', email)
      .single();

    if (userError || !existingUser) {
      return NextResponse.json({ error: 'User with this email not found' }, { status: 404 });
    }

    // Check if user is already an admin
    const { data: existingAdmin, error: adminCheckError } = await supabase
      .from('admin_users')
      .select('id')
      .eq('user_id', existingUser.id)
      .single();

    if (!adminCheckError && existingAdmin) {
      return NextResponse.json({ error: 'User is already an admin' }, { status: 400 });
    }

    // Get the current admin's admin_users record
    const { data: currentAdmin, error: currentAdminError } = await supabase
      .from('admin_users')
      .select('id')
      .eq('user_id', session.user.id)
      .single();

    if (currentAdminError || !currentAdmin) {
      return NextResponse.json({ error: 'Current admin record not found' }, { status: 500 });
    }

    // Add user as admin
    const { data: newAdmin, error: insertError } = await supabase
      .from('admin_users')
      .insert({
        user_id: existingUser.id,
        email: existingUser.email,
        is_root_admin: isRootAdmin,
        can_manage_admins: canManageAdmins,
        added_by_admin_id: currentAdmin.id
      })
      .select(`
        id,
        user_id,
        email,
        is_root_admin,
        can_manage_admins,
        created_at,
        users:user_id (
          name,
          email
        )
      `)
      .single();

    if (insertError) {
      console.error('Error inserting admin:', insertError);
      return NextResponse.json({ error: 'Failed to add admin' }, { status: 500 });
    }

    return NextResponse.json({ 
      message: 'Admin added successfully',
      admin: newAdmin
    });

  } catch (error) {
    console.error('Error in POST /api/admin/users:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
