module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'public/js/**/*.js',
    '*.js',
    '!public/js/**/*.test.js',
    '!**/*.test.js',
    '!jest.config.js',
    '!.eslintrc.js'
  ],
  testMatch: [
    '**/__tests__/**/*.js',
    '**/*.test.js'
  ],
  coverageThreshold: {
    global: {
      statements: 30,
      branches: 20,
      functions: 30,
      lines: 30
    }
  },
  testTimeout: 10000
};

