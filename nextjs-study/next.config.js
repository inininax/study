/** @type {import("next").NextConfig} */

const path = require("path");

const nextConfig = {
  // next 12.1: standalone은 experimental.outputStandalone (12.3+부터 output: "standalone").
  // Dockerfile의 .next/standalone 복사에 필요하다.
  experimental: {
    outputStandalone: true,
  },
  reactStrictMode: true,
  sassOptions: {
    includePaths: [path.join(__dirname, "styles")],
  },
  compiler: {
    styledComponents: true,
  },
  // airbnb/prettier 스타일 규칙은 `npm run lint`로 관리하고,
  // 빌드가 스타일 에러로 깨지지 않도록 한다.
  eslint: {
    ignoreDuringBuilds: true,
  },
};

module.exports = nextConfig;
