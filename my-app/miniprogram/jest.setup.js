// jest.setup.js

// This makes Page an alias for Component, so we can test pages as components.
Object.defineProperty(global, 'Page', {
  get() {
    return global.Component;
  },
});

global.getApp = jest.fn(() => ({}));
global.wx = {};
