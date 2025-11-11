const API_BASE_URL = 'https://www.yidasoftware.xyz/jinhengtai/api/v1';

Page({
  data: {
    keyword: '',
    searchHistory: [],
    productList: [],
    pageSize: 10,
    pageNum: 1,
    isLoading: false,
    hasMore: true,
    showHistory: true,
    showEmpty: false,
    hotKeywords: ['手机', '电脑', '耳机', '相机', '手表', '平板'],
  },

  onLoad: function (options) {
    if (options.keyword) {
      this.setData({
        keyword: options.keyword
      });
      this.handleSearch();
    }
    this.loadSearchHistory();
  },

  loadSearchHistory() {
    const history = wx.getStorageSync('searchHistory') || [];
    this.setData({ searchHistory: history });
  },

  saveSearchHistory(keyword) {
    if (!keyword.trim()) return;
    let history = wx.getStorageSync('searchHistory') || [];
    history = history.filter(item => item !== keyword);
    history.unshift(keyword);
    if (history.length > 10) {
      history = history.slice(0, 10);
    }
    wx.setStorageSync('searchHistory', history);
    this.setData({ searchHistory: history });
  },

  clearSearchHistory() {
    wx.removeStorageSync('searchHistory');
    this.setData({ searchHistory: [] });
    wx.showToast({ title: '已清空历史', icon: 'success' });
  },

  onInputChange(e) {
    const keyword = e.detail.value;
    this.setData({ keyword, showHistory: keyword.length === 0 });
  },

  onInputFocus() {
    this.setData({ showHistory: this.data.keyword.length === 0 });
  },

  onClearInput() {
    this.setData({ keyword: '', showHistory: true });
  },

  handleSearch() {
    const { keyword } = this.data;
    if (!keyword.trim()) {
      wx.showToast({ title: '请输入搜索关键词', icon: 'none' });
      return;
    }
    this.saveSearchHistory(keyword);
    this.setData({ productList: [], pageNum: 1, hasMore: true, showHistory: false, showEmpty: false });
    this.loadSearchResults();
  },

  loadSearchResults(isLoadMore = false) {
    const { keyword, pageNum, pageSize, isLoading, hasMore } = this.data;
    if (isLoading || (isLoadMore && !hasMore)) return;

    this.setData({ isLoading: true });

    wx.request({
      url: `${API_BASE_URL}/products/`,
      method: 'GET',
      data: {
        keyword: keyword,
        page: pageNum,
        page_size: pageSize
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const products = res.data;
          const newList = isLoadMore ? [...this.data.productList, ...products] : products;
          this.setData({
            productList: newList,
            pageNum: pageNum + 1,
            hasMore: products.length === pageSize,
            showEmpty: newList.length === 0
          });
        } else {
          wx.showToast({ title: '搜索失败', icon: 'none' });
        }
      },
      fail: () => {
        wx.showToast({ title: '网络请求失败', icon: 'none' });
      },
      complete: () => {
        this.setData({ isLoading: false });
      }
    });
  },

  onHistoryItemTap(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({ keyword });
    this.handleSearch();
  },

  onHotKeywordTap(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({ keyword });
    this.handleSearch();
  },

  onProductTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/product/detail/detail?id=${id}` });
  },

  onReachBottom: function () {
    if (this.data.hasMore) {
      this.loadSearchResults(true);
    }
  },

  goBack() {
    wx.navigateBack();
  }
});
