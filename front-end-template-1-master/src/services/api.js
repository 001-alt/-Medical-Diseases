import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // 注意这里使用代理前缀
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
});

export default {
  getPredictions() {
    return apiClient.get('/getPredictions'); // 完整URL将是 /api/getPredictions
  }
};
