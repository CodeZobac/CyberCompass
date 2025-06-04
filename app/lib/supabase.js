import { createClient } from '@supabase/supabase-js';

// Initialize Supabase client with SERVICE ROLE key instead of anon key
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY; // Use service role key

// During build time, use placeholder values to prevent build errors
const isDuringBuild = process.env.NODE_ENV === 'production' && !supabaseUrl;

if (!supabaseUrl || !supabaseServiceKey) {
  if (isDuringBuild) {
    // Use placeholder values during build
    console.warn('Using placeholder Supabase values during build');
  } else {
    throw new Error('Missing Supabase environment variables');
  }
}

// Service role bypasses RLS
const supabase = createClient(
  supabaseUrl || 'https://placeholder.supabase.co', 
  supabaseServiceKey || 'placeholder-key'
);

export { supabase };
