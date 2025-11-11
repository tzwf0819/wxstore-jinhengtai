const simulate = require('miniprogram-simulate');
const path = require('path');

describe('HomeContent Component', () => {
  it('should render the basic structure', () => {
    // Manually load the dependent component first
    simulate.load(path.resolve(__dirname, '../../product-card/product-card'));

    // Load the target component
    const componentId = simulate.load(path.resolve(__dirname, '../home-content'));
    const component = simulate.render(componentId);

    // Verify structure
    const searchBar = component.querySelector('.search-bar');
    expect(searchBar).toBeTruthy();

    const swiper = component.querySelector('.swiper-container');
    expect(swiper).toBeTruthy();

    const categories = component.querySelector('.categories');
    expect(categories).toBeTruthy();
  });
});
