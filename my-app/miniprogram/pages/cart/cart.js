const cartService = require('../../services/cartService.js');

Page({
  data: {
    cart: [],
    totalPrice: 0,
    totalItems: 0
  },

  onShow() {
    this.loadCartData();
  },

  loadCartData() {
    const cart = cartService.getCart();
    this.setData({ cart });
    this.calculateTotals();
  },

  calculateTotals() {
    const cart = this.data.cart;
    let totalPrice = 0;
    let totalItems = 0;
    cart.forEach(item => {
      totalPrice += item.price * item.quantity;
      totalItems += item.quantity;
    });
    this.setData({
      totalPrice: totalPrice.toFixed(2),
      totalItems
    });
  },

  changeQuantity(e) {
    const { id, amount } = e.currentTarget.dataset;
    const item = this.data.cart.find(i => i.id === id);
    if (item) {
      const newQuantity = item.quantity + amount;
      if (newQuantity > 0) {
        cartService.updateQuantity(id, newQuantity);
        this.loadCartData();
      }
    }
  },

  deleteItem(e) {
    const { id } = e.currentTarget.dataset;
    wx.showModal({
      title: '确认删除',
      content: '确定要从购物车中移除该商品吗？',
      success: (res) => {
        if (res.confirm) {
          cartService.removeFromCart(id);
          this.loadCartData();
        }
      }
    });
  },

  goShopping() {
    wx.switchTab({ url: '/pages/home/home' });
  },

  goToCheckout() {
    if (this.data.cart.length === 0) return;
    const cartData = JSON.stringify(this.data.cart);
    wx.navigateTo({ 
      url: `/pages/checkout/checkout?cart=${encodeURIComponent(cartData)}`
    });
  }
});
