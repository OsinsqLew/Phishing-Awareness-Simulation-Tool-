import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { loginUser } from "@/lib/api";

export default NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        try {
          const res = await loginUser(credentials!.email, credentials!.password);
          if (res.data && res.data.token) {
            return { id: res.data.id, email: credentials!.email, token: res.data.token };
          }
          return null;
        } catch {
          return null;
        }
      }
    })
  ],
  session: {
    strategy: "jwt"
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.token = user.token;
        token.email = user.email;
      }
      return token;
    },
    async session({ session, token }) {
      if (token?.token) {
        session.user.token = token.token;
        session.user.email = token.email;
      }
      return session;
    }
  },
  pages: {
    signIn: "/login"
  }
});