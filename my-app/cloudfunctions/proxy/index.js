const axios = require('axios');

exports.main = async (event, context) => {
  const {
    url,
    method = 'GET',
    data = {},
    headers = {}
  } = event;

  const baseUrl = 'https://www.yidasoftware.xyz/jinhengtai/api/v1/';
  const finalUrl = baseUrl.replace(/\/$/, '') + '/' + url.replace(/^\//, '');

  const requestHeaders = {
    'Content-Type': 'application/json',
    ...headers
  };

  try {
    const response = await axios({
      url: finalUrl,
      method,
      data,
      headers: requestHeaders,
      responseType: 'json'
    });

    return {
      statusCode: response.status,
      headers: response.headers,
      body: response.data
    };
  } catch (error) {
    return {
      statusCode: error.response ? error.response.status : 500,
      body: error.response ? error.response.data : { message: 'Internal Server Error' }
    };
  }
};