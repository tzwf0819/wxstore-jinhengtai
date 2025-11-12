
import { getBanners, getHotProducts } from '../../services/api';

Page({
  data: {
    banners: [],
    products: [],
    loading: true,
  },

  onLoad: function (options) {
    this.loadHomePageData();
  },

  onPullDownRefresh: function () {
    this.loadHomePageData();
  },

  loadHomePageData: async function () {
    this.setData({ loading: true });
    wx.showLoading({ title: '加载中...' });
    try {
      const [bannersRes, productsRes] = await Promise.all([
        getBanners(),
        getHotProducts(10) // 获取10个热门商品
      ]);

      this.setData({
        banners: bannersRes || [],
        products: productsRes || []
      });

    } catch (error) {
      console.error("Failed to load home page data:", error);
      wx.showToast({ title: '数据加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
      wx.hideLoading();
      wx.stopPullDownRefresh();
    }
  },

  goToProductDetail: function(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/product/detail/detail?id=${id}`
    });
  }
});