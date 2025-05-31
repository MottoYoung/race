module.exports = {
  root: true,
  env: {
    node: true
  },

  'extends': [
    'plugin:vue/vue3-essential',
    'eslint:recommended'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-unused-vars': 'off', // 将错误改为警告
    'vue/multi-word-component-names': 'off',
    'vue/require-v-for-key': 'off',
  }
}
