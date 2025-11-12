import { API_BASE_URL } from '../config';

export const request = ({ url, method = 'GET', data = {}, headers = {} }) => {
  const baseUrl = API_BASE_URL;

  if (!baseUrl) {
    console.error('API base URL not configured');
    return Promise.reject(new Error('API base URL not configured'));
  }

  // Create a robust final URL by ensuring there is exactly one slash between parts.
  const finalUrl = baseUrl.replace(/\/$/, '') + '/' + url.replace(/^\//, '');

  const requestHeaders = {
    'Content-Type': 'application/json',
    ...headers
  };

  return new Promise((resolve, reject) => {
    wx.request({
      url: finalUrl,
      method,
      data,
      header: requestHeaders,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          console.error('Request failed:', res);
          const errorMessage = res.data?.detail || res.data?.message || '请求失败';
          wx.showToast({
            title: errorMessage,
            icon: 'none'
          });
          reject(new Error(errorMessage));
        }
      },
      fail: (error) => {
        console.error('Network request failed:', error);
        wx.showToast({
          title: '网络异常，请稍后重试',
          icon: 'none'
        });
        reject(error);
      }
    });
  });
};