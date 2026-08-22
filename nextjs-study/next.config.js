/** @type {import("next").NextConfig} */

const path = require("path");

const nextConfig = {
  output: "standalone",
  reactStrictMode: true,
  sassOptions: {
    includePaths: [path.join(__dirname, "styles")],
  },
  compiler: {
    styledComponents: true,
  },
};

module.exports = nextConfig;
