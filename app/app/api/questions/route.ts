import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '../../../lib/auth';
import { supabase } from '../../../lib/supabase.js';

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const {
      title,
      description,
      category,
      options,
      correctAnswer,
      language
    } = body;

    // Validate required fields
    if (!title || !description || !category || !options || correctAnswer === undefined || !language) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }

    // Validate options array
    if (!Array.isArray(options) || options.length !== 4) {
      return NextResponse.json({ error: 'Must provide exactly 4 options' }, { status: 400 });
    }

    // Validate correct answer index
    if (correctAnswer < 0 || correctAnswer >= 4) {
      return NextResponse.json({ error: 'Invalid correct answer index' }, { status: 400 });
    }

    // Get category ID
    const { data: categoryData, error: categoryError } = await supabase
      .from('challenge_categories')
      .select('id')
      .eq('slug', category)
      .single();

    if (categoryError || !categoryData) {
      return NextResponse.json({ error: 'Invalid category' }, { status: 400 });
    }

    // Create options object with correct answer marked
    const optionsWithCorrect = options.map((option: string, index: number) => ({
      content: option,
      is_correct: index === correctAnswer
    }));

    // Insert pending challenge
    const { data, error } = await supabase
      .from('pending_challenges')
      .insert({
        title,
        description,
        submitted_by_user_id: session.user.id,
        submitted_language: language,
        options: optionsWithCorrect,
        assigned_category_id: categoryData.id
      })
      .select()
      .single();

    if (error) {
      console.error('Error inserting pending challenge:', error);
      return NextResponse.json({ error: 'Failed to submit question' }, { status: 500 });
    }

    return NextResponse.json({ 
      success: true, 
      id: data.id,
      message: 'Question submitted successfully' 
    });

  } catch (error) {
    console.error('Error submitting question:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
