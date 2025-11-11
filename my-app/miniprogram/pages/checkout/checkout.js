const API_BASE_URL = 'https://www.yidasoftware.xyz/jinhengtai/api/v1';
const cartService = require('../../services/cartService.js');

Page({
  data: {
    cartItems: [],
    totalPrice: 0,
    shippingAddress: null
  },

  onLoad(options) {
    if (options.cart) {
      const cartItems = JSON.parse(decodeURIComponent(options.cart));
      this.setData({ cartItems });
      this.calculateTotal(cartItems);
    }
  },

  calculateTotal(cartItems) {
    const totalPrice = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
    this.setData({ totalPrice: totalPrice.toFixed(2) });
  },

  chooseAddress() {
    wx.chooseAddress({
      success: (res) => {
        this.setData({ shippingAddress: res });
      },
      fail: (err) => {
        if (err.errMsg.includes('cancel')) return;
        wx.showToast({ title: '获取地址失败', icon: 'none' });
      }
    });
  },

  submitOrder() {
    if (!this.data.shippingAddress) {
      wx.showToast({ title: '请选择收货地址', icon: 'none' });
      return;
    }

    // In a real app, you would get a real user ID after login.
    // Here we use a placeholder. You need to replace it with your user management logic.
    const userId = '1'; // Placeholder, replace with actual user ID

    const orderItems = this.data.cartItems.map(item => ({
      product_id: item.id,
      quantity: item.quantity
    }));

    const orderData = {
      items: orderItems,
      shipping_address: `${this.data.shippingAddress.provinceName}${this.data.shippingAddress.cityName}${this.data.shippingAddress.countyName}${this.data.shippingAddress.detailInfo}`,
      shipping_contact: `${this.data.shippingAddress.userName} ${this.data.shippingAddress.telNumber}`
    };

    wx.showLoading({ title: '正在提交订单...' });

    wx.request({
      url: `${API_BASE_URL}/orders/`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'X-User-Id': userId // Pass user ID in header as defined in deps.py
      },
      data: orderData,
      success: (res) => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          cartService.saveCart([]); // Clear cart
          wx.hideLoading();
          
          // Simulate payment success
          wx.showToast({ title: '支付成功', icon: 'success' });

          // Redirect to order list page
          setTimeout(() => {
            wx.redirectTo({ url: '/pages/order/list/index' });
          }, 1500);

        } else {
          wx.hideLoading();
          wx.showToast({ title: res.data.detail || '订单创建失败', icon: 'none' });
        }
      },
      fail: (err) => {
        wx.hideLoading();
        console.error('Failed to create order', err);
        wx.showToast({ title: '网络请求失败', icon: 'none' });
      }
    });
  }
});
