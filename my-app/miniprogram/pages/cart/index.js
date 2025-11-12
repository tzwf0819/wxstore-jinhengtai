
const app = getApp();

Page({
  data: {
    cart: [],
    totalPrice: 0,
    isAllSelected: true,
  },

  onShow: function () {
    this.updateCartData();
    app.updateCartBadge();
  },

  updateCartData: function() {
    const cart = app.globalData.cart;
    let totalPrice = 0;
    let isAllSelected = cart.length > 0;

    cart.forEach(item => {
      if (item.selected) {
        totalPrice += item.price * item.quantity;
      }
      if (!item.selected) {
        isAllSelected = false;
      }
    });

    this.setData({
      cart: cart,
      totalPrice: totalPrice.toFixed(2),
      isAllSelected: isAllSelected
    });
  },

  onQuantityChange: function(e) {
    const { id, type } = e.currentTarget.dataset;
    app.updateCartItem(id, { type });
    this.updateCartData();
  },

  onToggleSelect: function(e) {
    const { id } = e.currentTarget.dataset;
    app.updateCartItem(id, { type: 'TOGGLE_SELECT' });
    this.updateCartData();
  },

  onSelectAll: function() {
    const cart = app.globalData.cart;
    const currentIsAllSelected = this.data.isAllSelected;
    cart.forEach(item => {
      item.selected = !currentIsAllSelected;
    });
    app.syncCart();
    this.updateCartData();
  },

  onRemoveItem: function(e) {
    const { id } = e.currentTarget.dataset;
    wx.showModal({
      title: '提示',
      content: '确定要删除这个商品吗？',
      success: (res) => {
        if (res.confirm) {
          app.updateCartItem(id, { type: 'REMOVE' });
          this.updateCartData();
        }
      }
    });
  },

  onCheckout: function() {
    const hasSelectedItem = this.data.cart.some(item => item.selected);
    if (!hasSelectedItem) {
      wx.showToast({ title: '请选择要结算的商品', icon: 'none' });
      return;
    }
    wx.navigateTo({
      url: '/pages/order-confirm/index'
    });
  }
});