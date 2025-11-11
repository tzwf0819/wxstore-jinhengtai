// app.js
App({
  onLaunch: function() {
    const token = wx.getStorageSync('authToken');
    const profile = wx.getStorageSync('userProfile');
    if (token) {
      this.globalData.token = token;
    }
    if (profile) {
      this.globalData.userProfile = profile;
    }
  },

  setAuthToken(token) {
    this.globalData.token = token;
    if (token) {
      wx.setStorageSync('authToken', token);
    } else {
      wx.removeStorageSync('authToken');
    }
  },

  getAuthToken() {
    if (this.globalData.token) {
      return this.globalData.token;
    }
    const token = wx.getStorageSync('authToken');
    if (token) {
      this.globalData.token = token;
    }
    return token;
  },

  setUserProfile(profile) {
    this.globalData.userProfile = profile;
    if (profile) {
      wx.setStorageSync('userProfile', profile);
    } else {
      wx.removeStorageSync('userProfile');
    }
  },

  getUserProfile() {
    if (this.globalData.userProfile) {
      return this.globalData.userProfile;
    }
    const profile = wx.getStorageSync('userProfile');
    if (profile) {
      this.globalData.userProfile = profile;
    }
    return profile;
  },

  globalData: {
    apiBaseUrl: 'http://192.168.1.242:8000/api/v1',
    userProfile: null,
    token: null
  }
}); 