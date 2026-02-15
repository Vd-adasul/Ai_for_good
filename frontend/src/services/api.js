import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_URL = `${API_BASE_URL}/dashboard`;

export const api = {
    getWeather: async (city) => {
        try {
            const response = await axios.get(`${API_URL}/weather`, { params: { city } });
            return response.data;
        } catch (error) {
            console.error("Error fetching weather:", error);
            return null;
        }
    },

    getPrices: async () => {
        try {
            const response = await axios.get(`${API_URL}/prices`);
            return response.data;
        } catch (error) {
            console.error("Error fetching prices:", error);
            return [];
        }
    },

    getSubsidies: async (category) => {
        try {
            const response = await axios.get(`${API_URL}/subsidies`, { params: { category } });
            return response.data;
        } catch (error) {
            console.error("Error fetching subsidies:", error);
            return [];
        }
    },

    chat: async (message, district, history = []) => {
        try {
            const response = await axios.post(`${API_URL}/chat`, { message, district, history });
            return response.data;
        } catch (error) {
            console.error("Error sending message:", error);
            throw error;
        }
    }
};
