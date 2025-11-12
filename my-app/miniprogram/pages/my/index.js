
Page({
  data: {
    //  যেহেতু লগইন প্রয়োজন নেই, আমরা এখানে স্ট্যাটিক ডেটা ব্যবহার করব
    userInfo: {
      avatarUrl: '/static/images/avatar_placeholder.png',
      nickName: '微信用户'
    },
    menuItems: [
      { icon: '/static/images/orders.png', text: '我的订单', url: '/pages/orders/index' },
      { icon: '/static/images/address.png', text: '地址管理', url: '' },
      { icon: '/static/images/contact.png', text: '联系客服', action: 'contact' }
    ]
  },

  onMenuItemClick: function(e) {
    const { url, action } = e.currentTarget.dataset.item;
    if (url) {
      wx.navigateTo({ url });
    } else if (action === 'contact') {
      wx.makePhoneCall({
        phoneNumber: '10086' // 这里替换为实际的客服电话
      });
    } else {
      wx.showToast({ title: '功能暂未开放', icon: 'none' });
    }
  }
});