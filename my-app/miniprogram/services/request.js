const API_BASE_URL = 'https://www.yidasoftware.xyz/jinhengtai/api/v1/';

export const request = ({ url, method = 'GET', data = {}, headers = {} }) => {
  const baseUrl = API_BASE_URL;

  if (!baseUrl) {
    console.error('API base URL not configured');
    return Promise.reject(new Error('API base URL not configured'));
  }

  // Create a robust final URL by ensuring there is exactly one slash between parts.
  console.log('Base URL:', baseUrl);
  const finalUrl = baseUrl.replace(/\/$/, '') + '/' + url.replace(/^\//, '');
  console.log('Final URL:', finalUrl);
  console.log('Request params:', { url, method, data, headers }); // 打印所有请求参数

  const requestHeaders = {
    'Content-Type': 'application/json',
    ...headers
  };
  console.log('Final URL:', finalUrl);
  console.log('Full Request:', {
    url: finalUrl,
    method,
    data,
    headers: requestHeaders
  });
  return new Promise((resolve, reject) => {
    wx.request({
      url: finalUrl,
      method,
      data,
      header: requestHeaders,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          // 处理图片URL，添加完整域名
          const processImageUrls = (data) => {
            if (!data) return data;
            
            if (Array.isArray(data)) {
              return data.map(item => processImageUrls(item));
            }
            
            if (typeof data === 'object') {
              return Object.keys(data).reduce((acc, key) => {
                const value = data[key];
                if (key.match(/(image|img|avatar|banner|photo)/i) && typeof value === 'string') {
                  // 如果已经是完整URL则跳过
                  if (value.startsWith('http')) {
                    acc[key] = value;
                  } else {
                    acc[key] = `${API_BASE_URL.split('/api/')[0]}${value.startsWith('/') ? '' : '/'}${value}`;
                  }
                } else {
                  acc[key] = processImageUrls(value);
                }
                return acc;
              }, {});
            }
            
            return data;
          };
          
          resolve(processImageUrls(res.data));
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