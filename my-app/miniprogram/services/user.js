/**
 * 用户服务
 */
import { request } from './request';

const AUTH_ENDPOINT = '/auth';
const USER_ENDPOINT = '/users/me';
const ORDER_STATS_ENDPOINT = '/orders/stats';

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
 * 登录并获取 Token
 */
export const loginWithCode = async (code, userInfo = {}) => {
  const payload = {
    code,
    avatar: userInfo.avatarUrl,
    nickname: userInfo.nickName,
    gender: userInfo.gender,
    city: userInfo.city,
    province: userInfo.province,
    country: userInfo.country,
    language: userInfo.language
  };

  const data = await request({
    url: `${AUTH_ENDPOINT}/wx-login`,
    method: 'POST',
    data: payload
  });

  const app = getApp();
  app?.setAuthToken?.(data.token);
  app?.setUserProfile?.(data.user);

  return data;
};

/**
 * 获取用户信息
 */
export const getUserInfo = async () => {
  try {
    const data = await request({
      url: USER_ENDPOINT,
      headers: resolveHeaders()
    });

    const app = getApp();
    app?.setUserProfile?.(data);
    return data;
  } catch (error) {
    console.error('获取用户信息失败：', error);
    return null;
  }
};

/**
 * 更新用户信息
 */
export const updateUserInfo = async (profile) => {
  try {
    const data = await request({
      url: USER_ENDPOINT,
      method: 'PUT',
      data: profile,
      headers: resolveHeaders()
    });

    const app = getApp();
    app?.setUserProfile?.(data);
    return data;
  } catch (error) {
    console.error('更新用户信息失败：', error);
    throw error;
  }
};

/**
 * 获取用户订单统计
 */
export const getOrderStats = async () => {
  try {
    const data = await request({
      url: ORDER_STATS_ENDPOINT,
      headers: resolveHeaders()
    });

    return data;
  } catch (error) {
    console.error('获取订单统计失败：', error);
    return {
      pendingPayment: 0,
      pendingDelivery: 0,
      pendingReceipt: 0,
      completed: 0
    };
  }
};
