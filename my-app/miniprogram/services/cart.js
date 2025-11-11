const CART_KEY = 'cart';

const getCart = () => {
  return wx.getStorageSync(CART_KEY) || [];
};

const saveCart = (cart) => {
  wx.setStorageSync(CART_KEY, cart);
};

const addToCart = (product, selectedSpec) => {
  const cart = getCart();
  const existingProductIndex = cart.findIndex(item => item.id === product.id && JSON.stringify(item.selectedSpec) === JSON.stringify(selectedSpec));

  if (existingProductIndex > -1) {
    cart[existingProductIndex].quantity += 1;
  } else {
    cart.push({ ...product, selectedSpec, quantity: 1 });
  }

  saveCart(cart);
};

module.exports = {
  getCart,
  addToCart
};