import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { supabase } from '@lib/supabase.js';

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
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

    const body = await request.json();
    const {
      translatedTitleEn,
      translatedTitlePt,
      translatedDescriptionEn,
      translatedDescriptionPt,
      translatedOptions,
      difficulty,
      categoryId
    } = body;

    // Get the pending challenge
    const { data: pendingChallenge, error: fetchError } = await supabase
      .from('pending_challenges')
      .select('*')
      .eq('id', params.id)
      .eq('status', 'pending')
      .single();

    if (fetchError || !pendingChallenge) {
      return NextResponse.json({ error: 'Question not found' }, { status: 404 });
    }

    // Start transaction by creating the challenge
    const { data: challenge, error: challengeError } = await supabase
      .from('challenges')
      .insert({
        category_id: categoryId || pendingChallenge.assigned_category_id,
        title: pendingChallenge.submitted_language === 'en' ? pendingChallenge.title : translatedTitleEn,
        description: pendingChallenge.submitted_language === 'en' ? pendingChallenge.description : translatedDescriptionEn,
        difficulty: difficulty || 1,
        order_index: 0 // Will be updated later
      })
      .select()
      .single();

    if (challengeError) {
      console.error('Error creating challenge:', challengeError);
      return NextResponse.json({ error: 'Failed to create challenge' }, { status: 500 });
    }

    // Create internationalization records
    const titleEn = pendingChallenge.submitted_language === 'en' ? pendingChallenge.title : translatedTitleEn;
    const titlePt = pendingChallenge.submitted_language === 'pt' ? pendingChallenge.title : translatedTitlePt;
    const descEn = pendingChallenge.submitted_language === 'en' ? pendingChallenge.description : translatedDescriptionEn;
    const descPt = pendingChallenge.submitted_language === 'pt' ? pendingChallenge.description : translatedDescriptionPt;

    const { error: i18nError } = await supabase
      .from('challenges_i18n')
      .insert([
        {
          challenge_id: challenge.id,
          locale: 'en',
          title: titleEn,
          description: descEn
        },
        {
          challenge_id: challenge.id,
          locale: 'pt',
          title: titlePt,
          description: descPt
        }
      ]);

    if (i18nError) {
      console.error('Error creating challenge i18n:', i18nError);
      return NextResponse.json({ error: 'Failed to create challenge translations' }, { status: 500 });
    }

    // Create challenge options
    const options = pendingChallenge.options as Array<{content: string, is_correct: boolean}>;
    const optionInserts = options.map(option => ({
      challenge_id: challenge.id,
      content: option.content,
      is_correct: option.is_correct
    }));

    const { data: challengeOptions, error: optionsError } = await supabase
      .from('challenge_options')
      .insert(optionInserts)
      .select();

    if (optionsError) {
      console.error('Error creating challenge options:', optionsError);
      return NextResponse.json({ error: 'Failed to create challenge options' }, { status: 500 });
    }

    // Create options internationalization
    const optionsI18n = [];
    challengeOptions.forEach((dbOption, index) => {
      const originalOption = options[index];
      const optionEn = pendingChallenge.submitted_language === 'en' ? originalOption.content : translatedOptions?.en[index];
      const optionPt = pendingChallenge.submitted_language === 'pt' ? originalOption.content : translatedOptions?.pt[index];

      optionsI18n.push(
        {
          option_id: dbOption.id,
          locale: 'en',
          content: optionEn
        },
        {
          option_id: dbOption.id,
          locale: 'pt',
          content: optionPt
        }
      );
    });

    const { error: optionsI18nError } = await supabase
      .from('challenge_options_i18n')
      .insert(optionsI18n);

    if (optionsI18nError) {
      console.error('Error creating options i18n:', optionsI18nError);
      return NextResponse.json({ error: 'Failed to create option translations' }, { status: 500 });
    }

    // Update pending challenge status
    const { error: updateError } = await supabase
      .from('pending_challenges')
      .update({
        status: 'approved',
        reviewed_by_admin_id: adminUser.id,
        reviewed_at: new Date().toISOString(),
        translated_title_en: titleEn,
        translated_title_pt: titlePt,
        translated_description_en: descEn,
        translated_description_pt: descPt,
        translated_options: translatedOptions,
        assigned_difficulty: difficulty
      })
      .eq('id', params.id);

    if (updateError) {
      console.error('Error updating pending challenge:', updateError);
      return NextResponse.json({ error: 'Failed to update question status' }, { status: 500 });
    }

    return NextResponse.json({ 
      success: true, 
      challengeId: challenge.id,
      message: 'Question approved and challenge created successfully' 
    });

  } catch (error) {
    console.error('Error approving question:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
