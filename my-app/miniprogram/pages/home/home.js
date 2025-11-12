import { getBanners, getHotProducts } from '../../services/product';

Page({
  data: {
    banners: [],
    products: []
  },

  onLoad: function () {
    this.loadHomePageData();
  },

  async loadHomePageData() {
    wx.showLoading({ title: '加载中...' });
    try {
      const [banners, products] = await Promise.all([
        getBanners(),
        getHotProducts(10) // Fetch 10 hot products
      ]);

      // Add full URL to images
      const serverBaseUrl = 'https://www.yidasoftware.xyz/jinhengtai';
      const formattedBanners = banners.map(b => ({ ...b, image_url: b.image_url && (b.image_url.startsWith('http') ? b.image_url : serverBaseUrl + b.image_url) }));
      const formattedProducts = products.map(p => ({ ...p, image_url: p.image_url && (p.image_url.startsWith('http') ? p.image_url : serverBaseUrl + p.image_url) }));

      this.setData({
        banners: formattedBanners,
        products: formattedProducts
      });

    } catch (error) {
      console.error("Failed to load home page data:", error);
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  }
});