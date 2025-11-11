Page({
  data: {
    cart: [],
    totalPrice: 0,
  },

  onShow() {
    this.loadCartData();
  },

  loadCartData() {
    const cart = wx.getStorageSync('cart') || [];
    this.setData({ cart });
    this.calculateTotalPrice();
  },

  calculateTotalPrice() {
    const totalPrice = this.data.cart.reduce((sum, item) => {
      return sum + item.price * item.quantity;
    }, 0);
    this.setData({ totalPrice: totalPrice * 100 }); // Van submit-bar expects price in cents
  },

  onQuantityChange(event) {
    const itemId = event.currentTarget.dataset.itemId;
    const newQuantity = event.detail;
    const cart = this.data.cart.map(item => {
      if (item.id === itemId) {
        item.quantity = newQuantity;
      }
      return item;
    });

    this.setData({ cart });
    wx.setStorageSync('cart', cart);
    this.calculateTotalPrice();
  },

  onDeleteItem(event) {
    const itemId = event.currentTarget.dataset.itemId;
    const cart = this.data.cart.filter(item => item.id !== itemId);

    this.setData({ cart });
    wx.setStorageSync('cart', cart);
    this.calculateTotalPrice();
  },

  onSubmit() {
    if (this.data.cart.length > 0) {
      wx.navigateTo({
        url: `/pages/checkout/checkout?orderItems=${encodeURIComponent(JSON.stringify(this.data.cart))}`,
      });
    }
  },
});
