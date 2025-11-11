const CART_KEY = 'mall_cart';

const getCart = () => {
  try {
    return wx.getStorageSync(CART_KEY) || [];
  } catch (e) {
    return [];
  }
};

const saveCart = (cart) => {
  try {
    wx.setStorageSync(CART_KEY, cart);
  } catch (e) {
    console.error('Failed to save cart', e);
  }
};

const addToCart = (product) => {
  const cart = getCart();
  const existingItem = cart.find(item => item.id === product.id);

  if (existingItem) {
    existingItem.quantity += 1;
  } else {
    cart.push({ ...product, quantity: 1 });
  }
  saveCart(cart);
};

const updateQuantity = (productId, quantity) => {
  let cart = getCart();
  const item = cart.find(item => item.id === productId);

  if (item) {
    if (quantity <= 0) {
      cart = cart.filter(item => item.id !== productId);
    } else {
      item.quantity = quantity;
    }
    saveCart(cart);
  }
};

const removeFromCart = (productId) => {
  const cart = getCart().filter(item => item.id !== productId);
  saveCart(cart);
};

module.exports = {
  getCart,
  addToCart,
  updateQuantity,
  removeFromCart
};
