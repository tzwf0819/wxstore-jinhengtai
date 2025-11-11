/**
 * 商品分类数据服务
 */
import { request } from './request';

// 获取分类列表
export const getCategoryList = async () => {
  try {
    const data = await request({
      url: '/categories'
    });
    return data;
  } catch (error) {
    console.error('获取分类列表数据失败', error);
    return [];
  }
};
