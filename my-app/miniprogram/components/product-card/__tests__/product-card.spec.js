const simulate = require('miniprogram-simulate');
const path = require('path');

describe('ProductCard', () => {
  it('should render product info correctly', () => {
    const componentId = simulate.load(path.resolve(__dirname, '../product-card'));
    const component = simulate.render(componentId, {
      product: {
        name: '测试商品',
        price: '99.99',
        image: 'test.jpg'
      }
    });

    const productName = component.querySelector('.product-name');
    const productPrice = component.querySelector('.product-price');

    expect(productName.dom.textContent).toBe('测试商品');
    expect(productPrice.dom.textContent).toBe('¥99.99');
  });
});
