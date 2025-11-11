/**
 * 商品数据服务
 */
import { request } from './request';
import { getSwiperList as getBanners } from './swiper'; // Assuming getBanners is in swiper.js
import { getCategoryList as getCategories } from './category'; // Assuming getCategories is in category.js

const buildSortQuery = (orderBy) => {
  if (!orderBy) {
    return { sort_by: 'sales', sort_order: 'desc' };
  }
  const { field = 'sales', direction = 'desc' } = orderBy;
  return { sort_by: field, sort_order: direction };
};

// 获取商品列表
export const getProducts = async (options = {}) => {
  try {
    const {
      pageNum = 1,
      pageSize = 10,
      category = null,
      orderBy = { field: 'sales', direction: 'desc' }
    } = options;

    const query = {
      page: pageNum,
      page_size: pageSize,
      ...buildSortQuery(orderBy)
    };

    if (category) {
      query.category_code = category;
    }

    const data = await request({
      url: '/products',
      data: query
    });

    return data || [];
  } catch (error) {
    console.error('获取商品列表失败', error);
    return [];
  }
};

// 获取商品详情
export const getProductDetail = async (id) => {
  try {
    const data = await request({
      url: `/products/${id}`
    });
    return data;
  } catch (error) {
    console.error('获取商品详情失败', error);
    return null;
  }
};

// 获取热门商品
export const getHotProducts = async (limit = 6) => {
  try {
    const data = await request({
      url: '/products',
      data: {
        page: 1,
        page_size: limit,
        sort_by: 'sales',
        sort_order: 'desc'
      }
    });
    return data || [];
  } catch (error) {
    console.error('获取热门商品失败', error);
    return [];
  }
};

// 获取新品
export const getNewProducts = async (limit = 6) => {
  try {
    const data = await request({
      url: '/products',
      data: {
        page: 1,
        page_size: limit,
        sort_by: 'created_at',
        sort_order: 'desc'
      }
    });
    return data || [];
  } catch (error) {
    console.error('获取新品失败', error);
    return [];
  }
};

// 搜索商品
export const searchProducts = async (keyword, options = {}) => {
  try {
    const {
      page = 1,
      pageSize = 10,
      orderBy = { field: 'sales', direction: 'desc' }
    } = options;

    const data = await request({
      url: '/products',
      data: {
        page,
        page_size: pageSize,
        keyword,
        ...buildSortQuery(orderBy)
      }
    });

    return data || [];
  } catch (error) {
    console.error('搜索商品失败', error);
    return [];
  }
};

export { getBanners, getCategories };

