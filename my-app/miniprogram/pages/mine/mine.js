Page({
  data: {
    userInfo: {
      avatar: '/images/default-avatar.png',
      nickName: '点击登录'
    },
    orderStats: {
      pendingPayment: 1,
      pendingDelivery: 2,
      pendingReceipt: 3,
      completed: 4,
    },
  },

  onShow() {
    // 在真实应用中，这里会加载用户信息和订单统计
  },

  getUserProfile() {
    // 模拟登录
    this.setData({
      userInfo: {
        avatar: 'https://placehold.co/120x120/6A5ACD/white?text=User',
        nickName: '微信用户',
        _id: 'user123'
      }
    });
  },

  navigateTo(e) {
    const url = e.currentTarget.dataset.url;
    wx.navigateTo({ url });
  },

  logout() {
    this.setData({
      userInfo: {
        avatar: '/images/default-avatar.png',
        nickName: '点击登录'
      }
    });
  },
});