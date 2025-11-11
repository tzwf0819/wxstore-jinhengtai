const API_BASE_URL = 'https://www.yidasoftware.xyz/jinhengtai/api/v1';

Page({
  data: {
    categories: [],
    products: [],
    activeCategory: null,
  },

  onLoad() {
    this.loadCategories();
  },

  loadCategories() {
    wx.request({
      url: `${API_BASE_URL}/categories/`,
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200 && res.data.length > 0) {
          this.setData({
            categories: res.data,
            activeCategory: res.data[0] // Set the first category as active by default
          });
          this.loadProductsForCategory();
        }
      },
      fail: (err) => {
        console.error('Failed to load categories', err);
      }
    });
  },

  loadProductsForCategory() {
    if (!this.data.activeCategory) return;

    wx.request({
      url: `${API_BASE_URL}/products/`,
      method: 'GET',
      data: {
        category_code: this.data.activeCategory.code,
        page_size: 50 // Load more products for category page
      },
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({
            products: res.data
          });
        }
      },
      fail: (err) => {
        console.error('Failed to load products for category', err);
      }
    });
  },

  switchCategory(e) {
    const categoryId = e.currentTarget.dataset.categoryId;
    const newActiveCategory = this.data.categories.find(cat => cat.id === categoryId);

    if (newActiveCategory && newActiveCategory.id !== this.data.activeCategory.id) {
      this.setData({
        activeCategory: newActiveCategory,
        products: [] // Clear previous products immediately for better UX
      });
      this.loadProductsForCategory();
    }
  }
});
