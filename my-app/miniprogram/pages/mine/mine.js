const USER_INFO_KEY = 'mall_user_info';

Page({
  data: {
    userInfo: null, // Default to null, indicating not logged in
    // Mock order stats, in a real app, this would be fetched from a server
    orderStats: {
      pendingPayment: 1,
      pendingDelivery: 2,
      pendingReceipt: 3,
      completed: 4,
    },
  },

  onShow() {
    // Try to load user info from storage on page show
    this.loadUserInfoFromStorage();
  },

  loadUserInfoFromStorage() {
    try {
      const userInfo = wx.getStorageSync(USER_INFO_KEY);
      if (userInfo) {
        this.setData({ userInfo });
      }
    } catch (e) {
      console.error('Failed to load user info from storage', e);
    }
  },

  handleLogin() {
    wx.getUserProfile({
      desc: '用于完善会员资料', // This description will be shown to the user
      success: (res) => {
        const userInfo = res.userInfo;
        try {
          wx.setStorageSync(USER_INFO_KEY, userInfo);
          this.setData({ userInfo });
          wx.showToast({ title: '登录成功', icon: 'success' });
        } catch (e) {
          wx.showToast({ title: '登录失败', icon: 'none' });
        }
      },
      fail: (err) => {
        console.error('Failed to get user profile', err);
        wx.showToast({ title: '授权已取消', icon: 'none' });
      }
    });
  },

  logout() {
    wx.showModal({
      title: '确认退出',
      content: '您确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          try {
            wx.removeStorageSync(USER_INFO_KEY);
            this.setData({ userInfo: null });
            wx.showToast({ title: '已退出' });
          } catch (e) {
            wx.showToast({ title: '退出失败', icon: 'none' });
          }
        }
      }
    });
  },

  navigateTo(e) {
    const { url } = e.currentTarget.dataset;
    if (url) {
      wx.navigateTo({ url });
    }
  },
});
