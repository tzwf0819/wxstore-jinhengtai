/**
 * 轮播图数据服务
 */
import { request } from './request';

const mapBannerResponse = (data) => {
  if (!data) {
    return [];
  }
  if (Array.isArray(data.results)) {
    return data.results;
  }
  if (Array.isArray(data.items)) {
    return data.items;
  }
  if (Array.isArray(data)) {
    return data;
  }
  return [];
};

// 获取轮播图列表
export const getSwiperList = async () => {
  try {
    const data = await request({
      url: '/banners'
    });
    return mapBannerResponse(data);
  } catch (error) {
    console.error('获取轮播图数据失败', error);
    return [];
  }
};