
App({
  onLaunch: function () {
    // 尝试从本地缓存中加载购物车数据
    const cart = wx.getStorageSync('cart') || [];
    this.globalData.cart = cart;
    this.updateCartBadge();
  },

  globalData: {
    cart: [] // { id, name, price, image_url, quantity, selected }
  },

  // 添加商品到购物车
  addToCart: function(product) {
    const cart = this.globalData.cart;
    const existingProduct = cart.find(item => item.id === product.id);

    if (existingProduct) {
      existingProduct.quantity += 1;
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image_url: product.image_url,
        quantity: 1,
        selected: true // 默认选中
      });
    }
    this.syncCart();
  },

  // 更新购物车（例如：修改数量、选中状态）
  updateCartItem: function(productId, action) {
    const cart = this.globalData.cart;
    const productIndex = cart.findIndex(item => item.id === productId);
    if (productIndex === -1) return;

    const product = cart[productIndex];

    switch (action.type) {
      case 'INCREMENT':
        product.quantity += 1;
        break;
      case 'DECREMENT':
        if (product.quantity > 1) {
          product.quantity -= 1;
        } else {
          // 数量为1时再减则删除
          cart.splice(productIndex, 1);
        }
        break;
      case 'TOGGLE_SELECT':
        product.selected = !product.selected;
        break;
      case 'REMOVE':
        cart.splice(productIndex, 1);
        break;
    }
    this.syncCart();
  },

  // 清空已结算的商品
  clearCheckedCartItems: function() {
    this.globalData.cart = this.globalData.cart.filter(item => !item.selected);
    this.syncCart();
  },

  // 同步购物车数据到缓存并更新角标
  syncCart: function() {
    wx.setStorageSync('cart', this.globalData.cart);
    this.updateCartBadge();
  },

  // 更新购物车角标
  updateCartBadge: function() {
    const totalQuantity = this.globalData.cart.reduce((sum, item) => sum + item.quantity, 0);
    if (totalQuantity > 0) {
      wx.setTabBarBadge({
        index: 2, // 对应 tabBar 的购物车页面索引
        text: String(totalQuantity)
      });
    } else {
      wx.removeTabBarBadge({
        index: 2
      });
    }
  }
});