import { request } from './request';

/**
 * 获取轮播图数据
 */
export const getBanners = () => {
  return request({ url: '/banners' });
};

/**
 * 获取商品列表
 * @param {object} params - 查询参数
 */
export const getProducts = (params = {}) => {
  return request({
    url: '/products',
    data: params
  });
};

/**
 * 获取热门商品
 */
export const getHotProducts = (limit = 10) => {
  return getProducts({
    page: 1,
    page_size: limit,
    sort_by: 'sales',
    sort_order: 'desc'
  });
};


/**
 * 获取商品详情
 * @param {string} id - 商品ID
 */
export const getProductDetail = (id) => {
  return request({ url: `/products/${id}` });
};

/**
 * 获取分类列表
 */
export const getCategories = () => {
  return request({ url: '/categories' });
};

/**
 * 创建订单
 * @param {object} orderData - 订单数据
 */
export const createOrder = (orderData) => {
  return request({
    url: '/orders',
    method: 'POST',
    data: orderData
  });
};
