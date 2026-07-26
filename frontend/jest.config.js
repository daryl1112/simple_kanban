/**
 * Jest configuration built on top of Next.js's SWC transform so TS/JSX and
 * path aliases work without extra Babel setup.
 *
 * react-markdown and remark-gfm are ESM-only; rather than transforming their
 * deep ESM dependency trees, we map them to lightweight mocks under __mocks__.
 * They are only mocked for tests — the real packages are used at build/runtime.
 */
const nextJest = require("next/jest");

const createJestConfig = nextJest({ dir: "./" });

/** @type {import('jest').Config} */
const customConfig = {
  testEnvironment: "jest-environment-jsdom",
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
  moduleNameMapper: {
    "^react-markdown$": "<rootDir>/__mocks__/react-markdown.tsx",
    "^remark-gfm$": "<rootDir>/__mocks__/remark-gfm.ts",
    "^@/(.*)$": "<rootDir>/$1",
  },
  testMatch: ["<rootDir>/__tests__/**/*.test.{ts,tsx}"],
};

module.exports = createJestConfig(customConfig);
