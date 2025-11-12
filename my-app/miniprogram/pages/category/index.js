
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
        this.onCategoryClick({ currentTarget: { dataset: { id: categories[0].id } } });
      }
    } catch (error) {
      console.error("Failed to load categories:", error);
      wx.showToast({ title: '分类加载失败', icon: 'none' });
    }
  },

  onCategoryClick: function (e) {
    const id = e.currentTarget.dataset.id;
    if (this.data.activeCategoryId === id) {
      return;
    }
    this.setData({ activeCategoryId: id, products: [] });
    this.loadProducts(id);
  },

  loadProducts: async function (categoryId) {
    this.setData({ loading: true });
    try {
      const products = await getProducts({ category_id: categoryId, page_size: 50 });
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