/**
 * 轮播图数据服务
 */
import { request } from './request';

// 获取轮播图列表
export const getSwiperList = async () => {
  try {
    const data = await request({
      url: '/banners'
    });
    return data;
  } catch (error) {
    console.error('获取轮播图数据失败', error);
    return [];
  }
};