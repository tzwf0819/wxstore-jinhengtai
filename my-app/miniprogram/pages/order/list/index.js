import { getOrders } from '../../../services/order';

Page({
  data: {
    orders: [],
  },

  onShow() {
    this.loadOrders();
  },

  async loadOrders() {
    wx.showLoading({ title: '加载中...' });
    try {
      const orders = await getOrders();
      this.setData({ orders });
    } catch (error) {
      console.error('Failed to load orders', error);
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  },

  navigateToDetail(event) {
    const orderId = event.currentTarget.dataset.orderId;
    wx.navigateTo({ url: `/pages/order/detail/index?id=${orderId}` });
  },
});
