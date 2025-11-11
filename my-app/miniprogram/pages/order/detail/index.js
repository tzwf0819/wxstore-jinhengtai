import { getOrderDetail } from '../../../services/order';

Page({
  data: {
    order: null,
  },

  onLoad(options) {
    if (options.id) {
      this.loadOrderDetail(options.id);
    }
  },

  async loadOrderDetail(orderId) {
    wx.showLoading({ title: '加载中...' });
    try {
      const order = await getOrderDetail(orderId);
      this.setData({ order });
    } catch (error) {
      console.error('Failed to load order detail', error);
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  },
});
