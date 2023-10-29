import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/'; // Your API base URL

// Reusable Axios GET request function
const fetchData = (endpoint) => {
  return axios.get(`${API_BASE_URL}${endpoint}`)
    .then(response => {
      if (response.status !== 200) {
        throw Error(response.statusText);
      }
      console.log(response.data)
      return response.data;
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      throw error; // You can choose to handle errors here or propagate them to the caller
    });
};

// Reusable Axios POST request function
const postData = (endpoint, data) => {
  return axios.post(`${API_BASE_URL}${endpoint}`, data)
    .then(response => response.data)
    .catch(error => {
      console.error('Error posting data:', error);
      throw error; // You can choose to handle errors here or propagate them to the caller
    });
};

export { fetchData, postData };
