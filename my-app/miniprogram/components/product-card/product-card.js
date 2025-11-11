Component({
  properties: {
    product: {
      type: Object,
      value: {}
    }
  },
  data: {},
  methods: {
    goToDetail() {
      wx.navigateTo({
        url: `/pages/product/detail/detail?id=${this.data.product.id}`
      });
    }
  }
});