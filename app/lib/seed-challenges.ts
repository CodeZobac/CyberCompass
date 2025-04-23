import { supabase } from './supabase';

/**
 * Script to seed the database with initial challenge data
 */
async function seedChallenges() {
  try {
    console.log('Starting database seeding for challenges...');

    // We already have the categories from the schema.sql, so we'll only add challenges and options

    // Catfishing challenges
    const catfishingCategory = await supabase
      .from('challenge_categories')
      .select('id')
      .eq('slug', 'catfishing')
      .single();

    if (!catfishingCategory.data) {
      throw new Error('Catfishing category not found');
    }

    const catfishingChallenges = [
      {
        title: 'Identifying Fake Profiles',
        description: 'Which of the following is NOT a common sign of a catfishing attempt?',
        difficulty: 1,
        order_index: 1,
        category_id: catfishingCategory.data.id,
        options: [
          {
            content: 'Profile has very few photos',
            is_correct: false,
          },
          {
            content: 'Profile seems too perfect or idealized',
            is_correct: false,
          },
          {
            content: 'Profile has many tagged photos with friends and family',
            is_correct: true,
          },
          {
            content: 'They refuse or make excuses about video calls',
            is_correct: false,
          }
        ]
      },
      {
        title: 'When Someone Asks for Money',
        description: 'If someone you met online asks you for money, what is the best response?',
        difficulty: 1,
        order_index: 2,
        category_id: catfishingCategory.data.id,
        options: [
          {
            content: 'Send a small amount to see if they are genuine',
            is_correct: false,
          },
          {
            content: 'Never send money, regardless of the reason or emergency',
            is_correct: true,
          },
          {
            content: 'Ask them to provide more details about their emergency',
            is_correct: false,
          },
          {
            content: 'Only send money if they provide identification',
            is_correct: false,
          }
        ]
      }
    ];
    
    // Cyberbullying challenges
    const cyberbullyingCategory = await supabase
      .from('challenge_categories')
      .select('id')
      .eq('slug', 'cyberbullying')
      .single();

    if (!cyberbullyingCategory.data) {
      throw new Error('Cyberbullying category not found');
    }

    const cyberbullyingChallenges = [
      {
        title: 'Recognizing Cyberbullying',
        description: 'Which of these actions is NOT considered cyberbullying?',
        difficulty: 1,
        order_index: 1,
        category_id: cyberbullyingCategory.data.id,
        options: [
          {
            content: 'Sending threatening messages',
            is_correct: false,
          },
          {
            content: 'Tagging someone in a positive group photo',
            is_correct: true,
          },
          {
            content: 'Spreading rumors online',
            is_correct: false,
          },
          {
            content: 'Creating fake profiles to impersonate someone',
            is_correct: false,
          }
        ]
      },
      {
        title: 'Responding to Cyberbullying',
        description: 'What is the most appropriate first step if you witness someone being cyberbullied?',
        difficulty: 1,
        order_index: 2,
        category_id: cyberbullyingCategory.data.id,
        options: [
          {
            content: 'Message the bully and tell them to stop',
            is_correct: false,
          },
          {
            content: 'Ignore it as it\'s none of your business',
            is_correct: false,
          },
          {
            content: 'Report the content to the platform',
            is_correct: true,
          },
          {
            content: 'Post a public comment calling out the bully',
            is_correct: false,
          }
        ]
      }
    ];

    // Deepfakes challenges
    const deepfakesCategory = await supabase
      .from('challenge_categories')
      .select('id')
      .eq('slug', 'deepfakes')
      .single();

    if (!deepfakesCategory.data) {
      throw new Error('Deepfakes category not found');
    }

    const deepfakesChallenges = [
      {
        title: 'Identifying Deepfakes',
        description: 'Which of the following is most likely to indicate that a video is a deepfake?',
        difficulty: 1,
        order_index: 1,
        category_id: deepfakesCategory.data.id,
        options: [
          {
            content: 'The video was published by a verified news source',
            is_correct: false,
          },
          {
            content: 'The lighting on the subject\'s face changes unnaturally',
            is_correct: true,
          },
          {
            content: 'The video has high production quality',
            is_correct: false,
          },
          {
            content: 'The subject is someone you recognize',
            is_correct: false,
          }
        ]
      },
      {
        title: 'Responding to Suspicious Media',
        description: 'You receive a video of a celebrity making shocking claims. What should you do first?',
        difficulty: 1,
        order_index: 2,
        category_id: deepfakesCategory.data.id,
        options: [
          {
            content: 'Share it immediately to warn others',
            is_correct: false,
          },
          {
            content: 'Cross-check with reliable news sources',
            is_correct: true,
          },
          {
            content: 'Download the video before it gets taken down',
            is_correct: false,
          },
          {
            content: 'Forward it to friends to get their opinions',
            is_correct: false,
          }
        ]
      }
    ];

    // Disinformation challenges
    const disinformationCategory = await supabase
      .from('challenge_categories')
      .select('id')
      .eq('slug', 'disinformation')
      .single();

    if (!disinformationCategory.data) {
      throw new Error('Disinformation category not found');
    }

    const disinformationChallenges = [
      {
        title: 'Evaluating News Sources',
        description: 'Which of these is the MOST reliable indicator of a trustworthy news source?',
        difficulty: 1,
        order_index: 1,
        category_id: disinformationCategory.data.id,
        options: [
          {
            content: 'The website has a professional design',
            is_correct: false,
          },
          {
            content: 'The article has many shares on social media',
            is_correct: false,
          },
          {
            content: 'The source cites specific studies or documents',
            is_correct: true,
          },
          {
            content: 'The headline contains emotional language',
            is_correct: false,
          }
        ]
      },
      {
        title: 'Spotting Fake News',
        description: 'What is the best approach to verify if news is legitimate?',
        difficulty: 1,
        order_index: 2,
        category_id: disinformationCategory.data.id,
        options: [
          {
            content: 'Check if it aligns with your existing beliefs',
            is_correct: false,
          },
          {
            content: 'Look for the same story from multiple reputable sources',
            is_correct: true,
          },
          {
            content: 'See if many people are sharing it on social media',
            is_correct: false,
          },
          {
            content: 'Check if the article has many comments',
            is_correct: false,
          }
        ]
      }
    ];

    // Insert all challenges and their options
    const allChallenges = [
      ...catfishingChallenges,
      ...cyberbullyingChallenges,
      ...deepfakesChallenges,
      ...disinformationChallenges
    ];

    // For each challenge, insert it and then its options
    for (const challenge of allChallenges) {
      // Extract options and create a new challenge object without the options property
      const { options, ...challengeData } = challenge;
      
      // Insert the challenge
      const { data: createdChallenge, error: challengeError } = await supabase
        .from('challenges')
        .insert(challengeData)
        .select('id')
        .single();

      if (challengeError) {
        console.error('Error inserting challenge:', challengeError);
        continue;
      }

      // Insert the options for this challenge
      const optionsWithChallengeId = options.map(option => ({
        ...option,
        challenge_id: createdChallenge.id
      }));

      const { error: optionsError } = await supabase
        .from('challenge_options')
        .insert(optionsWithChallengeId);

      if (optionsError) {
        console.error('Error inserting challenge options:', optionsError);
      }
    }

    console.log('Database seeding completed successfully!');
    return { success: true };
  } catch (error) {
    console.error('Error seeding database:', error);
    return { error };
  }
}

export { seedChallenges };