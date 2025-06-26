import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export default NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        // Zwróć przykładowego użytkownika na potrzeby testów
        return { id: 1, email: credentials?.email, token: "FAKE_TOKEN" };
      }
    })
  ],
  session: { strategy: "jwt" },
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