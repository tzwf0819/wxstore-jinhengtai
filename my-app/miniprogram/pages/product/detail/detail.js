
import { getProductDetail } from '../../../services/api';
const app = getApp();

Page({
  data: {
    product: null,
    loading: true
  },

  onLoad: function (options) {
    if (options.id) {
      this.loadProductDetail(options.id);
    } else {
      wx.showToast({ title: '商品不存在', icon: 'none' });
      this.setData({ loading: false });
    }
  },

  loadProductDetail: async function (id) {
    this.setData({ loading: true });
    try {
      const product = await getProductDetail(id);
      this.setData({ product: product, loading: false });
    } catch (error) {
      console.error("Failed to load product detail:", error);
      wx.showToast({ title: '商品加载失败', icon: 'none' });
      this.setData({ loading: false });
    }
  },

  onAddToCart: function () {
    if (!this.data.product) return;
    app.addToCart(this.data.product);
    wx.showToast({
      title: '已添加到购物车',
      icon: 'success'
    });
  },

  onBuyNow: function() {
    if (!this.data.product) return;
    // 为了演示流程，直接将当前商品加入购物车并跳转到订单确认页
    app.addToCart(this.data.product);
    wx.navigateTo({
      url: '/pages/order-confirm/index'
    });
  },

  goToCart: function() {
    wx.switchTab({
      url: '/pages/cart/index'
    });
  }
});