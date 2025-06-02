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

// PUT: Update admin permissions
export async function PUT(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Check if user has permission to manage admins
    const permissions = await checkAdminPermissions(session.user.id);
    if (!permissions.hasPermission) {
      return NextResponse.json({ error: 'No permission to manage admins' }, { status: 403 });
    }

    const { isRootAdmin, canManageAdmins } = await request.json();

    // Only root admins can modify root admin status or manage admin permissions
    if (!permissions.isRootAdmin && (isRootAdmin !== undefined || canManageAdmins !== undefined)) {
      return NextResponse.json({ 
        error: 'Only root admins can modify administrative privileges' 
      }, { status: 403 });
    }

    // Get the target admin to check if they exist and prevent self-modification issues
    const { data: targetAdmin, error: targetError } = await supabase
      .from('admin_users')
      .select('user_id, is_root_admin')
      .eq('id', id)
      .single();

    if (targetError || !targetAdmin) {
      return NextResponse.json({ error: 'Admin not found' }, { status: 404 });
    }

    // Prevent removing the last root admin
    if (targetAdmin.is_root_admin && isRootAdmin === false) {
      const { data: rootAdmins, error: rootCheckError } = await supabase
        .from('admin_users')
        .select('id')
        .eq('is_root_admin', true);

      if (rootCheckError || !rootAdmins || rootAdmins.length <= 1) {
        return NextResponse.json({ 
          error: 'Cannot remove the last root admin' 
        }, { status: 400 });
      }
    }

    // Update admin permissions
    const updateData: { is_root_admin?: boolean; can_manage_admins?: boolean } = {};
    if (isRootAdmin !== undefined) updateData.is_root_admin = isRootAdmin;
    if (canManageAdmins !== undefined) updateData.can_manage_admins = canManageAdmins;

    const { data: updatedAdmin, error: updateError } = await supabase
      .from('admin_users')
      .update(updateData)
      .eq('id', id)
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

    if (updateError) {
      console.error('Error updating admin:', updateError);
      return NextResponse.json({ error: 'Failed to update admin' }, { status: 500 });
    }

    return NextResponse.json({ 
      message: 'Admin permissions updated successfully',
      admin: updatedAdmin
    });

  } catch (error) {
    console.error('Error in PUT /api/admin/users/[id]:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

// DELETE: Remove admin
export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Check if user has permission to manage admins
    const permissions = await checkAdminPermissions(session.user.id);
    if (!permissions.hasPermission) {
      return NextResponse.json({ error: 'No permission to manage admins' }, { status: 403 });
    }

    // Get the target admin to check if they exist
    const { data: targetAdmin, error: targetError } = await supabase
      .from('admin_users')
      .select('user_id, is_root_admin')
      .eq('id', id)
      .single();

    if (targetError || !targetAdmin) {
      return NextResponse.json({ error: 'Admin not found' }, { status: 404 });
    }

    // Prevent self-removal
    if (targetAdmin.user_id === session.user.id) {
      return NextResponse.json({ 
        error: 'Cannot remove yourself as admin' 
      }, { status: 400 });
    }

    // Only root admins can remove other root admins
    if (targetAdmin.is_root_admin && !permissions.isRootAdmin) {
      return NextResponse.json({ 
        error: 'Only root admins can remove other root admins' 
      }, { status: 403 });
    }

    // Prevent removing the last root admin
    if (targetAdmin.is_root_admin) {
      const { data: rootAdmins, error: rootCheckError } = await supabase
        .from('admin_users')
        .select('id')
        .eq('is_root_admin', true);

      if (rootCheckError || !rootAdmins || rootAdmins.length <= 1) {
        return NextResponse.json({ 
          error: 'Cannot remove the last root admin' 
        }, { status: 400 });
      }
    }

    // Remove admin
    const { error: deleteError } = await supabase
      .from('admin_users')
      .delete()
      .eq('id', id);

    if (deleteError) {
      console.error('Error removing admin:', deleteError);
      return NextResponse.json({ error: 'Failed to remove admin' }, { status: 500 });
    }

    return NextResponse.json({ 
      message: 'Admin removed successfully'
    });

  } catch (error) {
    console.error('Error in DELETE /api/admin/users/[id]:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
