const API_BASE_URL = 'https://www.yidasoftware.xyz/jinhengtai/api/v1';
const cartService = require('../../services/cartService.js');

Page({
  data: {
    product: null,
  },

  onLoad(options) {
    const productId = options.id;
    if (productId) {
      this.loadProductDetail(productId);
    }
  },

  loadProductDetail(productId) {
    wx.request({
      url: `${API_BASE_URL}/products/${productId}`,
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({ product: res.data });
        } else {
          wx.showToast({
            title: '商品加载失败',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        console.error('Failed to load product detail', err);
        wx.showToast({
          title: '网络请求失败',
          icon: 'none'
        });
      }
    });
  },

  addToCart() {
    if (this.data.product) {
      cartService.addToCart(this.data.product);
      wx.showToast({
        title: '已加入购物车',
        icon: 'success'
      });
    }
  }
});
