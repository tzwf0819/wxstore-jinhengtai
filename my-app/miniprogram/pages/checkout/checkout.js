const cartService = require('../../services/cart.js');

Page({
  data: {
    cart: [],
    totalPrice: 0,
    addresses: [
      { id: 1, name: '张三', phone: '13800138000', address: '广东省深圳市南山区xx街道xx号' },
      { id: 2, name: '李四', phone: '13800138001', address: '广东省广州市天河区xx街道xx号' }
    ],
    selectedAddress: null
  },

  onLoad() {
    const cart = cartService.getCart();
    const totalPrice = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    this.setData({ 
      cart, 
      totalPrice: totalPrice.toFixed(2),
      selectedAddress: this.data.addresses[0] // 默认选择第一个地址
    });
  },

  selectAddress() {
    // 在实际应用中，这里会弹出一个地址选择列表
    wx.showToast({ title: '选择地址功能待实现', icon: 'none' });
  },

  submitOrder() {
    // 模拟订单提交和支付
    wx.showLoading({ title: '正在提交...' });
    setTimeout(() => {
      wx.hideLoading();
      // 清空购物车
      wx.removeStorageSync('cart');
      // 跳转到订单结果页
      wx.redirectTo({ url: '/pages/order/detail/index?status=success' });
    }, 1500);
  }
});