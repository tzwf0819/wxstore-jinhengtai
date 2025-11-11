const API_BASE_URL = 'https://www.yidasoftware.xyz/jinhengtai/api/v1';

Component({
  data: {
    swiperList: [],
    categoryList: [],
    recommendedProducts: [],
    allProducts: [],
    page: 1,
    pageSize: 10,
    hasMoreData: true
  },

  attached() {
    this.loadInitialData();
  },

  methods: {
    loadInitialData() {
      this.loadBanners();
      this.loadCategories();
      this.loadProducts(true);
      this.loadProducts(false);
    },

    loadBanners() {
      wx.request({
        url: `${API_BASE_URL}/banners/`,
        method: 'GET',
        success: (res) => {
          if (res.statusCode === 200) {
            this.setData({ swiperList: res.data });
          }
        }
      });
    },

    loadCategories() {
      wx.request({
        url: `${API_BASE_URL}/categories/`,
        method: 'GET',
        success: (res) => {
          if (res.statusCode === 200) {
            this.setData({ categoryList: res.data });
          }
        }
      });
    },

    loadProducts(isRecommended) {
      const page = isRecommended ? 1 : this.data.page;
      const pageSize = isRecommended ? 4 : this.data.pageSize;
      const sortBy = isRecommended ? 'sales' : 'created_at';

      wx.request({
        url: `${API_BASE_URL}/products/`,
        method: 'GET',
        data: { page, page_size: pageSize, sort_by: sortBy },
        success: (res) => {
          if (res.statusCode === 200) {
            const products = res.data;
            if (isRecommended) {
              this.setData({ recommendedProducts: products });
            } else {
              this.setData({
                allProducts: this.data.page === 1 ? products : this.data.allProducts.concat(products),
                page: this.data.page + 1,
                hasMoreData: products.length === pageSize
              });
            }
          }
        }
      });
    },

    loadMoreProducts() {
      if (this.data.hasMoreData) {
        this.loadProducts(false);
      }
    },

    onSearch(e) {
      const keyword = e.detail.value;
      if (keyword) {
        wx.navigateTo({ url: `/pages/search/search?keyword=${keyword}` });
      }
    }
  }
});
