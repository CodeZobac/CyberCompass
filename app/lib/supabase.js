import { createClient } from '@supabase/supabase-js';

// Initialize Supabase client with SERVICE ROLE key instead of anon key
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY; // Use service role key

if (!supabaseUrl || !supabaseServiceKey) {
  throw new Error('Missing Supabase environment variables');
}

// Service role bypasses RLS
const supabase = createClient(supabaseUrl, supabaseServiceKey);

export { supabase };