import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
    async rewrites() {  // proxy for backend server
        return [
          {
            source: '/proxy/:path*',
            destination: `${process.env.INTERNAL_API_URL || 'http://localhost:5000'}/:path*`,
          },
        ];
      },
};

export default nextConfig;
