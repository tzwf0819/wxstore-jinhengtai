
import { getCategories, getProducts } from '../../services/api';

Page({
  data: {
    categories: [],
    products: [],
    activeCategoryId: null,
    loading: false,
  },

  onLoad: function (options) {
    this.loadCategories();
  },

  loadCategories: async function () {
    try {
      const categories = await getCategories();
      this.setData({ categories: categories || [] });
      if (categories && categories.length > 0) {
        const firstCategory = categories[0];
        // Pass both id and name for the initial load
        this.onCategoryClick({ currentTarget: { dataset: { id: firstCategory.id, name: firstCategory.name } } });
      }
    } catch (error) {
      console.error("Failed to load categories:", error);
      wx.showToast({ title: '分类加载失败', icon: 'none' });
    }
  },

  onCategoryClick: function (e) {
    // Get both id and name from the dataset
    const { id, name } = e.currentTarget.dataset;
    if (this.data.activeCategoryId === id) {
      return;
    }
    this.setData({ activeCategoryId: id, products: [] });
    // Pass the category NAME to loadProducts
    this.loadProducts(name);
  },

  loadProducts: async function (categoryName) {
    this.setData({ loading: true });
    try {
      // Use 'category' and pass the name
      const products = await getProducts({ category: categoryName, page_size: 50 });
      this.setData({ products: products || [] });
    } catch (error) {
      console.error("Failed to load products:", error);
      wx.showToast({ title: '商品加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
    }
  },

  goToProductDetail: function(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/product/detail/detail?id=${id}`
    });
  }
});