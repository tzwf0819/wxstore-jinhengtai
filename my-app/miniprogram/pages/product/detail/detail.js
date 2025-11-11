const allProducts = [
  {
    id: 1,
    name: '商品1',
    price: '100.00',
    image: 'https://placehold.co/600x600/6A5ACD/white?text=商品1',
    specs: [
      { name: '颜色', options: ['红色', '蓝色'] },
      { name: '尺寸', options: ['S', 'M', 'L'] }
    ]
  },
  {
    id: 2,
    name: '商品2',
    price: '200.00',
    image: 'https://placehold.co/600x600/6A5ACD/white?text=商品2',
    specs: [
      { name: '颜色', options: ['黑色', '白色'] },
      { name: '尺寸', options: ['M', 'L', 'XL'] }
    ]
  },
  {
    id: 3,
    name: '商品3',
    price: '300.00',
    image: 'https://placehold.co/600x600/cccccc/white?text=商品3',
    specs: []
  },
  {
    id: 4,
    name: '商品4',
    price: '400.00',
    image: 'https://placehold.co/600x600/cccccc/white?text=商品4',
    specs: []
  },
  {
    id: 5,
    name: '商品5',
    price: '500.00',
    image: 'https://placehold.co/600x600/cccccc/white?text=商品5',
    specs: []
  },
  {
    id: 6,
    name: '商品6',
    price: '600.00',
    image: 'https://placehold.co/600x600/cccccc/white?text=商品6',
    specs: []
  }
];

const cartService = require('../../services/cart.js');

Page({
  data: {
    product: null,
    selectedSpec: {}
  },

  onLoad(options) {
    const productId = parseInt(options.id, 10);
    const product = allProducts.find(p => p.id === productId);
    this.setData({ product });
  },

  selectSpec(e) {
    const { specName, option } = e.currentTarget.dataset;
    this.setData({
      [`selectedSpec.${specName}`]: option
    });
  },

  addToCart() {
    for (const spec of this.data.product.specs) {
      if (!this.data.selectedSpec[spec.name]) {
        wx.showToast({ title: `请选择${spec.name}`, icon: 'none' });
        return;
      }
    }

    cartService.addToCart(this.data.product, this.data.selectedSpec);
    wx.showToast({ title: '已加入购物车' });
  }
});