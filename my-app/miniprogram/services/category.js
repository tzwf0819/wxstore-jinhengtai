/**
 * 商品分类数据服务
 */
import { request } from './request';

const mapCategoryResponse = (data) => {
  if (!data) {
    return [];
  }

  if (Array.isArray(data.items)) {
    return data.items;
  }

  if (Array.isArray(data.results)) {
    return data.results;
  }

  if (data.list && Array.isArray(data.list)) {
    return data.list;
  }

  if (Array.isArray(data)) {
    return data;
  }

  return [];
};

// 获取分类列表
export const getCategoryList = async () => {
  try {
    const data = await request({
      url: '/categories'
    });
    return mapCategoryResponse(data);
  } catch (error) {
    console.error('获取分类列表数据失败', error);
    return [];
  }
};
