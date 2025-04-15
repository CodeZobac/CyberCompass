import type { NextAuthOptions } from "next-auth";
import { SupabaseAdapter } from "./supabaseAdapter";
import GoogleProvider from "next-auth/providers/google";

// Extend the next-auth Session type to include user.id
declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      name?: string | null;
      email?: string | null;
      image?: string | null;
    }
  }
}

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  adapter: SupabaseAdapter(),
  session: {
    strategy: "jwt",  // Changed from "database" to "jwt"
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  cookies: {
    sessionToken: {
      name: `next-auth.session-token`,
      options: {
        httpOnly: true,
        sameSite: "lax",
        path: "/",
        secure: process.env.NODE_ENV === "production",
      },
    },
  },
  callbacks: {
    async session({ session, token }) {
      // When using JWT strategy, we get token instead of user
      if (session?.user) {
        session.user.id = token.sub as string;
      }
      return session;
    },
  },
};
