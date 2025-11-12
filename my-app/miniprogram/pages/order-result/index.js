
Page({
  data: {
    success: false,
    message: '',
    orderId: null,
  },

  onLoad: function (options) {
    this.setData({
      success: options.success === 'true',
      message: options.message || (options.success === 'true' ? '订单支付成功' : '订单创建失败'),
      orderId: options.orderId || null,
    });
  },

  goToHome: function() {
    wx.switchTab({
      url: '/pages/home/home'
    });
  },

  viewOrder: function() {
    if (this.data.orderId) {
      // 实际项目中应跳转到订单详情页
      wx.showToast({ title: `查看订单 ${this.data.orderId}`, icon: 'none' });
      wx.switchTab({
        url: '/pages/my/index'
      });
    }
  }
});