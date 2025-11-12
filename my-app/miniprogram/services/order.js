import request from '../utils/request';

const API_BASE_URL = 'https://www.yidasoftware.xyz/jinhengtai/api/v1'; // Make sure this matches your backend URL

export function createOrder(data) {
  return request(`${API_BASE_URL}/orders/`, {
    method: 'POST',
    data,
  });
}

export function getOrders() {
  return request(`${API_BASE_URL}/orders/`);
}

export function getOrderDetail(orderId) {
  return request(`${API_BASE_URL}/orders/${orderId}`);
}
