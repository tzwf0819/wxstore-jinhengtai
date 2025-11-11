/**
 * 通用请求封装
 */

const defaultHeaders = {
  'Content-Type': 'application/json'
};

const getAppInstance = () => {
  try {
    return getApp();
  } catch (error) {
    console.error('获取全局应用实例失败', error);
    return null;
  }
};

export const request = ({ url, method = 'GET', data = {}, headers = {} }) => {
  const app = getAppInstance();
  const baseUrl = app?.globalData?.apiBaseUrl;
  if (!baseUrl) {
    console.error('后端地址未配置');
    return Promise.reject(new Error('后端地址未配置'));
  }

  const requestHeaders = {
    ...defaultHeaders,
    ...headers
  };

  return new Promise((resolve, reject) => {
    wx.request({
      url: `${baseUrl}${url}`,
      method,
      data,
      header: requestHeaders,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else if (res.statusCode === 401) {
          app?.setAuthToken?.(null);
          app?.setUserProfile?.(null);
          wx.showToast({
            title: '请重新登录',
            icon: 'none'
          });
          reject(new Error('未授权'));
        } else {
          console.error('请求失败', res);
          wx.showToast({
            title: res.data?.message || '请求失败',
            icon: 'none'
          });
          reject(new Error(res.data?.message || '请求失败'));
        }
      },
      fail: (error) => {
        console.error('网络请求失败', error);
        wx.showToast({
          title: '网络异常，请稍后重试',
          icon: 'none'
        });
        reject(error);
      }
    });
  });
};
