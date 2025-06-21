import axios from "axios";


const axiosInsatnce = axios.create({
    baseURL:'http://localhost:8080/api',
    timeout:10000,
})

axiosInsatnce.interceptors.request.use(
    (config) =>{
        return config;
    },
    (error) =>{
        return Promise.reject(error);
    }
);
axiosInsatnce.interceptors.response.use(
    (response) =>{
        return response.data;
    },
    (error) =>{
        return Promise.reject(error);
    }
);

export default axiosInsatnce;