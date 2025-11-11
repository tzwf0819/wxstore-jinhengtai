module.exports = {
  testEnvironment: 'jsdom',
  testMatch: ['**/__tests__/**/*.spec.js'],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  transform: {},
  globals: {
    wx: true,
    Page: true,
    Component: true,
    getApp: true,
  },
};
