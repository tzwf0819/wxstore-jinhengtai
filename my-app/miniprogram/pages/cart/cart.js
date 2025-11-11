const cartService = require('../../services/cart.js');

Page({
  data: {
    cart: []
  },

  onShow() {
    this.setData({ cart: cartService.getCart() });
  },

  goToCheckout() {
    wx.navigateTo({ url: '/pages/checkout/checkout' });
  }
});