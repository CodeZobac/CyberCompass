import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { createClient } from '@supabase/supabase-js';
import type { UserAchievement } from '@lib/types';

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

    const { data: achievements, error } = await supabase
      .from('user_achievements')
      .select('*')
      .eq('user_id', session.user.id)
      .order('earned_at', { ascending: false });

    if (error) {
      console.error('Error fetching achievements:', error);
      return NextResponse.json({ error: 'Failed to fetch achievements' }, { status: 500 });
    }

    return NextResponse.json(achievements || []);
  } catch (error) {
    console.error('Error in achievements API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
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

    const body = await request.json();
    const { achievement_type, achievement_name, achievement_description, metadata } = body;

    // Check if achievement already exists
    const { data: existingAchievement } = await supabase
      .from('user_achievements')
      .select('id')
      .eq('user_id', session.user.id)
      .eq('achievement_type', achievement_type)
      .eq('achievement_name', achievement_name)
      .single();

    if (existingAchievement) {
      return NextResponse.json(
        { error: 'Achievement already earned' },
        { status: 409 }
      );
    }

    const { data: newAchievement, error } = await supabase
      .from('user_achievements')
      .insert({
        user_id: session.user.id,
        achievement_type,
        achievement_name,
        achievement_description,
        metadata: metadata || {},
      })
      .select()
      .single();

    if (error) {
      console.error('Error creating achievement:', error);
      return NextResponse.json({ error: 'Failed to create achievement' }, { status: 500 });
    }

    return NextResponse.json(newAchievement, { status: 201 });
  } catch (error) {
    console.error('Error in achievements POST API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
