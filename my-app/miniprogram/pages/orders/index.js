import { request } from '../../services/request';

Page({
  data: {
    orders: [],
  },

  onLoad(options) {
    this.loadOrders();
  },

  onShow() {
    this.loadOrders();
  },

  loadOrders: async function() {
    wx.showLoading({ title: '加载中...' });
    try {
      const orders = await request({ url: '/orders' });
      this.setData({ orders: orders || [] });
    } catch (error) {
      console.error("Failed to load orders:", error);
      wx.showToast({ title: '订单加载失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  },

  onRefund: function(e) {
    const orderId = e.currentTarget.dataset.id;
    wx.showModal({
      title: '确认退款',
      content: `您确定要为订单 ${orderId} 办理退款吗？此操作不可撤销。`,
      success: async (res) => {
        if (res.confirm) {
          wx.showLoading({ title: '正在处理...' });
          try {
            await request({ url: `/orders/${orderId}/delete`, method: 'POST' });
            wx.showToast({ title: '退款成功', icon: 'success' });
            this.loadOrders(); // Refresh the order list
          } catch (error) {
            console.error("Refund failed:", error);
            wx.showToast({ title: `退款失败: ${error.message}` || '请求失败', icon: 'none' });
          } finally {
            wx.hideLoading();
          }
        }
      }
    });
  }
});
