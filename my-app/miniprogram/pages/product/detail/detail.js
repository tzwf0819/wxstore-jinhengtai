import { getProductDetail } from '../../../services/product';

Page({
  data: {
    product: null,
    activeTab: 0,
    quantity: 1, // Add quantity to data
  },

  onLoad(options) {
    const productId = options.id;
    if (productId) {
      this.loadProductDetail(productId);
    }
  },

  async loadProductDetail(productId) {
    wx.showLoading({ title: '加载中...' });
    try {
      const product = await getProductDetail(productId);
      if (product) {
        const serverBaseUrl = 'http://192.168.1.242:8000';
        product.image_url = product.image_url && (product.image_url.startsWith('http') ? product.image_url : serverBaseUrl + product.image_url);
        this.setData({ product });
      } else {
        wx.showToast({
          title: '商品不存在',
          icon: 'none'
        });
      }
    } catch (error) {
      console.error('Failed to load product detail', error);
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    } finally {
      wx.hideLoading();
    }
  },

  onTabChange(event) {
    this.setData({ activeTab: event.detail.name });
  },

  onQuantityChange(event) {
    this.setData({ quantity: event.detail });
  },

  onClickIcon() {
    wx.switchTab({
      url: '/pages/cart/cart'
    });
  },

  addToCart() {
    if (this.data.product) {
      const cart = wx.getStorageSync('cart') || [];
      const existingItem = cart.find(item => item.id === this.data.product.id);

      if (existingItem) {
        existingItem.quantity += this.data.quantity;
      } else {
        cart.push({ ...this.data.product, quantity: this.data.quantity });
      }

      wx.setStorageSync('cart', cart);
      wx.showToast({
        title: '已加入购物车',
        icon: 'success'
      });
    }
  },

  buyNow() {
    if (this.data.product) {
        const productToBuy = [{ ...this.data.product, quantity: this.data.quantity }];
        wx.navigateTo({ 
            url: `/pages/checkout/checkout?orderItems=${encodeURIComponent(JSON.stringify(productToBuy))}`
        });
    }
  }
});
