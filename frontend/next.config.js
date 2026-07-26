/**
 * Next.js configuration.
 * `output: "standalone"` produces a self-contained server bundle that the
 * Docker image can run without the full node_modules tree.
 */
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  reactStrictMode: true,
};

module.exports = nextConfig;
