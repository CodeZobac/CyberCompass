import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { createClient } from '@supabase/supabase-js';
import type { ExportData } from '@lib/types';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(request: Request) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    const { format } = await request.json();

    // Fetch analytics data (reuse logic from analytics endpoint)
    const analyticsResponse = await fetch(
      `${process.env.NEXTAUTH_URL}/api/profile/analytics`,
      {
        headers: {
          'Cookie': request.headers.get('cookie') || '',
        },
      }
    );

    if (!analyticsResponse.ok) {
      return NextResponse.json(
        { error: 'Failed to fetch analytics data' },
        { status: 500 }
      );
    }

    const analytics = await analyticsResponse.json();

    // Fetch user data
    const { data: userData, error: userError } = await supabase
      .from('users')
      .select('name, email, created_at')
      .eq('id', session.user.id)
      .single();

    if (userError) {
      console.error('Error fetching user data:', userError);
      return NextResponse.json({ error: 'Failed to fetch user data' }, { status: 500 });
    }

    const exportData: ExportData = {
      userInfo: {
        name: userData?.name || session.user.name || 'Unknown User',
        email: userData?.email || session.user.email || '',
        joinDate: userData?.created_at || new Date().toISOString(),
      },
      analytics,
      generatedAt: new Date().toISOString(),
    };

    if (format === 'json') {
      // Return JSON data
      return NextResponse.json(exportData, {
        headers: {
          'Content-Type': 'application/json',
          'Content-Disposition': `attachment; filename="cyber-compass-profile-${new Date().toISOString().split('T')[0]}.json"`,
        },
      });
    }

    // For PDF format, return the data that will be used by client-side PDF generation
    return NextResponse.json({
      success: true,
      data: exportData,
      message: 'Export data prepared for PDF generation',
    });

  } catch (error) {
    console.error('Error in export API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
