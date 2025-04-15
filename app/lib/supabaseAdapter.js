import { supabase } from './supabase';

export function SupabaseAdapter() {
  return {
    // User operations
    async createUser(data) {
      const { data: user, error } = await supabase
        .from('users')
        .insert({
          name: data.name,
          email: data.email,
          email_verified: data.emailVerified,
          image: data.image,
        })
        .select()
        .single();

      if (error) throw error;
      return user;
    },

    async getUser(id) {
      const { data, error } = await supabase
        .from('users')
        .select('*')
        .eq('id', id)
        .single();

      if (error) return null;
      return data;
    },

    async getUserByEmail(email) {
      const { data, error } = await supabase
        .from('users')
        .select('*')
        .eq('email', email)
        .single();

      if (error) return null;
      return data;
    },

    async getUserByAccount({ provider, providerAccountId }) {
      const { data: account, error } = await supabase
        .from('accounts')
        .select('user_id')
        .eq('provider', provider)
        .eq('provider_account_id', providerAccountId)
        .single();

      if (error || !account) return null;

      const { data: user } = await supabase
        .from('users')
        .select('*')
        .eq('id', account.user_id)
        .single();

      return user || null;
    },

    async updateUser(user) {
      const { data, error } = await supabase
        .from('users')
        .update({
          name: user.name,
          email: user.email,
          email_verified: user.emailVerified,
          image: user.image,
          updated_at: new Date(),
        })
        .eq('id', user.id)
        .select()
        .single();

      if (error) throw error;
      return data;
    },

    async deleteUser(userId) {
      const { error } = await supabase
        .from('users')
        .delete()
        .eq('id', userId);

      if (error) throw error;
    },

    // Account operations
    async linkAccount(account) {
      const { data, error } = await supabase
        .from('accounts')
        .insert({
          user_id: account.userId,
          type: account.type,
          provider: account.provider,
          provider_account_id: account.providerAccountId,
          refresh_token: account.refresh_token,
          access_token: account.access_token,
          expires_at: account.expires_at,
          token_type: account.token_type,
          scope: account.scope,
          id_token: account.id_token,
          session_state: account.session_state,
          oauth_token_secret: account.oauth_token_secret,
          oauth_token: account.oauth_token,
        })
        .select()
        .single();

      if (error) throw error;
      return data;
    },

    async unlinkAccount({ provider, providerAccountId }) {
      const { error } = await supabase
        .from('accounts')
        .delete()
        .eq('provider', provider)
        .eq('provider_account_id', providerAccountId);

      if (error) throw error;
    },

    // Session operations
    async createSession(data) {
      const { data: session, error } = await supabase
        .from('sessions')
        .insert({
          user_id: data.userId,
          expires: new Date(data.expires).toISOString(),
          session_token: data.sessionToken,
        })
        .select()
        .single();

      if (error) throw error;
      return session;
    },

    async getSessionAndUser(sessionToken) {
      const { data: session, error } = await supabase
        .from('sessions')
        .select('*')
        .eq('session_token', sessionToken)
        .single();

      if (error || !session) return null;

      const { data: user } = await supabase
        .from('users')
        .select('*')
        .eq('id', session.user_id)
        .single();

      if (!user) return null;

      return {
        session,
        user,
      };
    },

    async updateSession(session) {
      const { data, error } = await supabase
        .from('sessions')
        .update({
          expires: session.expires,
        })
        .eq('session_token', session.sessionToken)
        .select()
        .single();

      if (error) throw error;
      return data;
    },

    async deleteSession(sessionToken) {
      const { error } = await supabase
        .from('sessions')
        .delete()
        .eq('session_token', sessionToken);

      if (error) throw error;
    },

    // Verification token operations
    async createVerificationToken(data) {
      const { data: verificationToken, error } = await supabase
        .from('verification_tokens')
        .insert({
          identifier: data.identifier,
          token: data.token,
          expires: data.expires,
        })
        .select()
        .single();

      if (error) throw error;
      return verificationToken;
    },

    async useVerificationToken({ identifier, token }) {
      const { data, error } = await supabase
        .from('verification_tokens')
        .delete()
        .match({ identifier, token })
        .select()
        .single();

      if (error) return null;
      return data;
    },
  };
}
