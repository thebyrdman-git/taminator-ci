// ESLint v9+ flat config format (CommonJS)
const js = require('@eslint/js');
const globals = require('globals');

module.exports = [
  // Base recommended rules
  js.configs.recommended,
  
  {
    files: ['**/*.js'],
    
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'commonjs',
      globals: {
        ...globals.browser,
        ...globals.node,
        // Electron-specific globals
        ipcRenderer: 'readonly',
      },
    },
    
    rules: {
      // Error prevention - would have caught our bugs!
      'no-unused-vars': ['warn', { 
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_'
      }],
      'no-console': 'off', // Allow console for logging
      
      // Async/Promise rules - CRITICAL (prevents Bug #2!)
      'require-await': 'warn',
      'no-async-promise-executor': 'error',
      'no-promise-executor-return': 'error',
      
      // Best practices
      'eqeqeq': ['error', 'always'], // Require === instead of ==
      'no-var': 'error', // Use let/const instead of var
      'prefer-const': 'warn',
      'no-throw-literal': 'error',
      
      // Code quality
      'no-trailing-spaces': 'warn',
      'semi': ['warn', 'always'],
      'quotes': ['warn', 'single', { 
        avoidEscape: true,
        allowTemplateLiterals: true 
      }],
      
      // Prevent bugs we just fixed
      'no-undef': 'error', // Catch undefined variables
      'no-unreachable': 'error',
      'no-dupe-keys': 'error',
      'no-duplicate-case': 'error',
      
      // Memory leak prevention (Bug #3)
      'no-unused-expressions': ['error', {
        allowShortCircuit: true,
        allowTernary: true
      }],
    },
  },
  
  // Ignore patterns
  {
    ignores: [
      'node_modules/**',
      'dist/**',
      '*.min.js',
      'build/**',
    ],
  },
];

