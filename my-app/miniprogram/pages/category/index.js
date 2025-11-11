import { getCategories, getProducts } from '../../services/product';
import { API_BASE_URL } from '../../utils/api';

Page({
  data: {
    categories: [],
    allProducts: [],
    activeCategory: null,
    filteredProducts: []
  },

  onLoad() {
    this.loadData();
  },

  async loadData() {
    wx.showLoading({ title: '加载中...' });
    try {
      const [categories, allProducts] = await Promise.all([
        getCategories(),
        getProducts({ page_size: 200 })
      ]);

      const serverBaseUrl = 'http://192.168.1.242:8000';
      const formattedProducts = allProducts.map(p => ({ ...p, image_url: p.image_url && (p.image_url.startsWith('http') ? p.image_url : serverBaseUrl + p.image_url) }));

      if (categories.length > 0) {
        const activeCategory = categories[0];
        this.setData({
          categories,
          allProducts: formattedProducts,
          activeCategory,
          filteredProducts: formattedProducts.filter(p => p.category === activeCategory.name)
        });
      }
    } catch (error) {
      console.error('Failed to load data', error);
    } finally {
      wx.hideLoading();
    }
  },

  switchCategory(e) {
    const categoryId = e.currentTarget.dataset.categoryId;
    const newActiveCategory = this.data.categories.find(cat => cat.id === categoryId);

    if (newActiveCategory && newActiveCategory.id !== this.data.activeCategory.id) {
      this.setData({
        activeCategory: newActiveCategory,
        filteredProducts: this.data.allProducts.filter(p => p.category === newActiveCategory.name)
      });
    }
  }
});
