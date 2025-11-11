import { createOrder } from '../../services/order';

Page({
  data: {
    orderItems: [],
    totalPrice: 0,
    shipping_address: '',
    shipping_contact: '',
  },

  onLoad(options) {
    if (options.orderItems) {
      const orderItems = JSON.parse(decodeURIComponent(options.orderItems));
      this.setData({ orderItems });
      this.calculateTotalPrice(orderItems);
    }
  },

  calculateTotalPrice(items) {
    const totalPrice = items.reduce((sum, item) => {
      return sum + item.price * item.quantity;
    }, 0);
    this.setData({ totalPrice: totalPrice * 100 });
  },

  onAddressInput(event) {
    this.setData({ shipping_address: event.detail });
  },

  onContactInput(event) {
    this.setData({ shipping_contact: event.detail });
  },

  async onSubmitOrder() {
    if (!this.data.shipping_address || !this.data.shipping_contact) {
      wx.showToast({ title: '请填写收货信息', icon: 'none' });
      return;
    }

    const orderData = {
      items: this.data.orderItems.map(item => ({ product_id: item.id, quantity: item.quantity })),
      shipping_address: this.data.shipping_address,
      shipping_contact: this.data.shipping_contact,
    };

    wx.showLoading({ title: '正在提交订单...' });
    try {
      const order = await createOrder(orderData);
      wx.hideLoading();
      
      // Clear cart and navigate to order detail page
      wx.removeStorageSync('cart');
      wx.redirectTo({ url: `/pages/order/detail/index?id=${order.id}` });

    } catch (error) {
      wx.hideLoading();
      wx.showToast({ title: '订单创建失败', icon: 'none' });
      console.error('Failed to create order', error);
    }
  },
});
