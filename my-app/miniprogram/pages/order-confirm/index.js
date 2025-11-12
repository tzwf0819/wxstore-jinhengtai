
import { createOrder } from '../../services/api';
const app = getApp();

Page({
  data: {
    orderItems: [],
    totalPrice: 0,
    shippingAddress: '河北省雄安新区易达软件', // 模拟地址
    shippingContact: '18131218660', // 模拟联系方式
    submitting: false,
  },

  onLoad: function (options) {
    const cart = app.globalData.cart;
    const orderItems = cart.filter(item => item.selected);
    const totalPrice = orderItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

    this.setData({
      orderItems,
      totalPrice: totalPrice.toFixed(2)
    });
  },

  onQuantityChange: function(e) {
    const { id, type } = e.currentTarget.dataset;
    const orderItems = this.data.orderItems;
    const item = orderItems.find(i => i.id === id);

    if (item) {
      if (type === 'INCREMENT') {
        item.quantity++;
      } else if (type === 'DECREMENT' && item.quantity > 1) {
        item.quantity--;
      }
    }

    const totalPrice = orderItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

    this.setData({
      orderItems,
      totalPrice: totalPrice.toFixed(2)
    });

    // Also update the global cart data
    app.updateCartItem(id, { type, quantity: item.quantity });
  },

  onAddressInput: function(e) {
    this.setData({ shippingAddress: e.detail.value });
  },

  onContactInput: function(e) {
    this.setData({ shippingContact: e.detail.value });
  },

  onSubmitOrder: async function() {
    if (!this.data.shippingAddress || !this.data.shippingContact) {
      wx.showToast({ title: '请填写完整的收货信息', icon: 'none' });
      return;
    }

    this.setData({ submitting: true });

    const orderData = {
      shipping_address: this.data.shippingAddress,
      shipping_contact: this.data.shippingContact,
      items: this.data.orderItems.map(item => ({
        product_id: item.id,
        quantity: item.quantity
      }))
    };

    try {
      const orderRes = await createOrder(orderData);
      // 下单成功
      app.clearCheckedCartItems(); // 清空购物车中已结算的商品
      wx.redirectTo({
        url: `/pages/order-result/index?success=true&orderId=${orderRes.id}`
      });
    } catch (error) {
      console.error('Failed to create order:', error);
      wx.redirectTo({
        url: `/pages/order-result/index?success=false&message=${error.message}`
      });
    } finally {
      this.setData({ submitting: false });
    }
  }
});