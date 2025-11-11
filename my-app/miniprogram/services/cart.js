/**
 * 购物车服务
 */
import { request } from './request';

const CART_ENDPOINT = '/cart';

const resolveHeaders = () => {
  const app = getApp();
  const token = app?.getAuthToken?.();
  return token
    ? {
        Authorization: `Bearer ${token}`
      }
    : {};
};

/**
 * 添加商品到购物车
 */
export const addToCart = async (productId, count = 1, skuId = null) => {
  try {
    const payload = {
      product_id: productId,
      quantity: count,
      sku_id: skuId
    };
    const data = await request({
      url: CART_ENDPOINT,
      method: 'POST',
      data: payload,
      headers: resolveHeaders()
    });
    return data;
  } catch (error) {
    console.error('添加到购物车失败', error);
    throw error;
  }
};

/**
 * 获取购物车列表
 */
export const getCartList = async () => {
  try {
    const data = await request({
      url: CART_ENDPOINT,
      headers: resolveHeaders()
    });
    return data;
  } catch (error) {
    console.error('获取购物车列表失败', error);
    throw error;
  }
};

/**
 * 更新购物车商品数量
 */
export const updateCartItemCount = async (itemId, count) => {
  try {
    return await request({
      url: `${CART_ENDPOINT}/${itemId}`,
      method: 'PUT',
      data: { quantity: count },
      headers: resolveHeaders()
    });
  } catch (error) {
    console.error('更新购物车商品数量失败', error);
    throw error;
  }
};

/**
 * 删除购物车商品
 */
export const removeFromCart = async (itemId) => {
  try {
    return await request({
      url: `${CART_ENDPOINT}/${itemId}`,
      method: 'DELETE',
      headers: resolveHeaders()
    });
  } catch (error) {
    console.error('删除购物车商品失败', error);
    throw error;
  }
};

/**
 * 更新购物车商品选中状态
 */
export const updateCartItemSelected = async (itemId, selected) => {
  try {
    return await request({
      url: `${CART_ENDPOINT}/${itemId}/selection`,
      method: 'PATCH',
      data: { selected },
      headers: resolveHeaders()
    });
  } catch (error) {
    console.error('更新购物车商品选中状态失败', error);
    throw error;
  }
};