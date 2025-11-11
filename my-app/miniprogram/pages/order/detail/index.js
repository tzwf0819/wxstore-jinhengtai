Page({
  data: {
    status: 'success', // or 'fail'
    orderId: '123456789'
  },

  onLoad(options) {
    if (options.status) {
      this.setData({ status: options.status });
    }
  },

  goToHome() {
    wx.switchTab({ url: '/pages/home/home' });
  },

  viewOrder() {
    // 在实际应用中，这里会跳转到此订单的详情
    wx.showToast({ title: '查看订单功能待实现', icon: 'none' });
  }
});