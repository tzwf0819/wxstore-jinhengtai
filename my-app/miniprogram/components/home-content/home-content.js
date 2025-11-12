import { getBanners } from '../../services/swiper';
import { getCategories } from '../../services/category';
import { getProducts } from '../../services/product';

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
    async loadInitialData() {
      wx.showLoading({ title: '加载中...' });
      try {
        await Promise.all([
          this.loadBanners(),
          this.loadCategories(),
          this.loadProducts(true), // 加载推荐商品
          this.loadProducts(false, true) // 首次加载全部商品
        ]);
      } catch (error) {
        console.error("Failed to load initial data", error);
        wx.showToast({ title: '数据加载失败', icon: 'none' });
      } finally {
        wx.hideLoading();
      }
    },

    async loadBanners() {
      try {
        const banners = await getBanners();
        this.setData({ swiperList: banners });
      } catch (error) {
        console.error("Failed to load banners", error);
      }
    },

    async loadCategories() {
      try {
        const categories = await getCategories();
        this.setData({ categoryList: categories });
      } catch (error) {
        console.error("Failed to load categories", error);
      }
    },

    async loadProducts(isRecommended, isInitialLoad = false) {
      if (!isRecommended && !this.data.hasMoreData && !isInitialLoad) {
        return;
      }

      const page = isRecommended ? 1 : this.data.page;
      const pageSize = isRecommended ? 4 : this.data.pageSize;
      const orderBy = isRecommended ? { field: 'sales', direction: 'desc' } : { field: 'created_at', direction: 'desc' };

      try {
        const products = await getProducts({
          pageNum: page,
          pageSize: pageSize,
          orderBy: orderBy
        });

        if (isRecommended) {
          this.setData({ recommendedProducts: products || [] });
        } else {
          this.setData({
            allProducts: isInitialLoad ? (products || []) : this.data.allProducts.concat(products || []),
            page: this.data.page + 1,
            hasMoreData: products && products.length === pageSize
          });
        }
      } catch (error) {
        console.error(`Failed to load ${isRecommended ? 'recommended' : 'all'} products`, error);
      }
    },

    loadMoreProducts() {
      this.loadProducts(false);
    },

    onSearch(e) {
      const keyword = e.detail.value;
      if (keyword) {
        wx.navigateTo({ url: `/pages/search/search?keyword=${keyword}` });
      }
    }
  }
});
