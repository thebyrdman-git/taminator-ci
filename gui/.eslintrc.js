module.exports = {
  env: {
    browser: true,
    commonjs: true,
    es2021: true,
    node: true,
  },
  extends: 'eslint:recommended',
  parserOptions: {
    ecmaVersion: 'latest',
  },
  globals: {
    // Electron globals
    electron: 'readonly',
    // Custom globals from your app
    errorHandler: 'readonly',
    intelligenceClient: 'readonly',
    customerService: 'readonly',
    issueService: 'readonly',
    dashboardService: 'readonly',
    jiraClient: 'readonly',
    portalClient: 'readonly',
    settingsManager: 'readonly',
    rhcaseClient: 'readonly',
    TaminatorAPI: 'readonly',
    googleAuth: 'writable',
  },
  rules: {
    // Error Prevention (What caused your recent bugs)
    'no-async-promise-executor': 'error',
    'no-await-in-loop': 'warn',
    'no-console': 'off', // You use console.error/log for debugging
    'no-constant-condition': 'error',
    'no-promise-executor-return': 'error',
    'require-atomic-updates': 'error',
    
    // Async/Await Best Practices
    'no-return-await': 'error',
    'prefer-promise-reject-errors': 'error',
    
    // Error Handling
    'no-throw-literal': 'error',
    'no-unused-vars': ['warn', { 
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_'
    }],
    
    // Code Quality
    'eqeqeq': ['error', 'always'],
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-var': 'error',
    'prefer-const': 'warn',
    'prefer-arrow-callback': 'warn',
    
    // Memory Leak Prevention
    'no-unreachable': 'error',
    'no-unreachable-loop': 'error',
    
    // Debugging
    'no-debugger': 'warn',
    'no-alert': 'warn',
    
    // Best Practices
    'curly': ['error', 'all'],
    'default-case': 'warn',
    'default-case-last': 'error',
    'no-duplicate-imports': 'error',
    'no-self-compare': 'error',
    'no-unmodified-loop-condition': 'error',
    'no-unused-expressions': 'warn',
    'no-useless-concat': 'warn',
    'no-useless-return': 'warn',
    'require-await': 'warn',
    
    // Style (Keep consistent with your current code)
    'indent': ['error', 2, { SwitchCase: 1 }],
    'quotes': ['warn', 'single', { avoidEscape: true }],
    'semi': ['error', 'always'],
    'comma-dangle': ['warn', 'always-multiline'],
  },
  overrides: [
    {
      // Main process files (Electron)
      files: ['main.js', 'service-manager.js', 'preload.js'],
      env: {
        node: true,
        browser: false,
      },
      globals: {
        __dirname: 'readonly',
        __filename: 'readonly',
      },
    },
    {
      // Renderer process files (Browser)
      files: ['public/js/**/*.js', 'google-auth-handler.js'],
      env: {
        browser: true,
        node: false,
      },
      globals: {
        // IPC exposed by preload
        window: 'readonly',
        document: 'readonly',
      },
    },
  ],
};

