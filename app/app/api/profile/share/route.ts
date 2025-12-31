import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { createClient } from '@supabase/supabase-js';
import { randomUUID } from 'crypto';

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );

    const userId = session.user.id;
    const { expiresInDays = 30 } = await request.json();

    // Generate a secure token
    const token = randomUUID().replace(/-/g, '');
    
    // Calculate expiration date
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + expiresInDays);

    // Deactivate any existing active share links for this user
    await supabase
      .from('profile_share_links')
      .update({ is_active: false })
      .eq('user_id', userId)
      .eq('is_active', true);

    // Create new share link
    const { data, error } = await supabase
      .from('profile_share_links')
      .insert({
        user_id: userId,
        token,
        expires_at: expiresAt.toISOString(),
        is_active: true,
      })
      .select()
      .single();

    if (error) {
      console.error('Error creating share link:', error);
      return NextResponse.json(
        { error: 'Failed to create share link' },
        { status: 500 }
      );
    }

    // Generate the shareable URL
    const baseUrl = process.env.NEXTAUTH_URL || 'http://localhost:3000';
    const shareUrl = `${baseUrl}/en/profile/shared/${token}`;

    return NextResponse.json({
      shareUrl,
      token,
      expiresAt: data.expires_at,
      viewCount: 0,
    });
  } catch (error) {
    console.error('Error in profile share API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET() {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );

    const userId = session.user.id;

    // Get active share links for the user
    const { data, error } = await supabase
      .from('profile_share_links')
      .select('*')
      .eq('user_id', userId)
      .eq('is_active', true)
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching share links:', error);
      return NextResponse.json(
        { error: 'Failed to fetch share links' },
        { status: 500 }
      );
    }

    const baseUrl = process.env.NEXTAUTH_URL || 'http://localhost:3000';
    const shareLinks = data.map(link => ({
      id: link.id,
      shareUrl: `${baseUrl}/en/profile/shared/${link.token}`,
      token: link.token,
      expiresAt: link.expires_at,
      viewCount: link.view_count,
      createdAt: link.created_at,
    }));

    return NextResponse.json(shareLinks);
  } catch (error) {
    console.error('Error in profile share API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );

    const userId = session.user.id;
    const { token } = await request.json();

    if (!token) {
      return NextResponse.json(
        { error: 'Token is required' },
        { status: 400 }
      );
    }

    // Deactivate the share link
    const { error } = await supabase
      .from('profile_share_links')
      .update({ is_active: false })
      .eq('user_id', userId)
      .eq('token', token);

    if (error) {
      console.error('Error deactivating share link:', error);
      return NextResponse.json(
        { error: 'Failed to deactivate share link' },
        { status: 500 }
      );
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error in profile share API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
