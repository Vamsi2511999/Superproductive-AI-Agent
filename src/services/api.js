import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Task APIs
export const taskService = {
  getAllTasks: async () => {
    const response = await api.get('/api/tasks');
    return response.data;
  },

  extractTasks: async () => {
    const response = await api.post('/api/tasks/extract');
    return response.data;
  },

  prioritizeTasks: async () => {
    const response = await api.post('/api/tasks/prioritize');
    return response.data;
  },

  filterTasks: async (filters) => {
    const params = new URLSearchParams();
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);
    if (filters.source_type) params.append('source_type', filters.source_type);
    if (filters.priority) params.append('priority', filters.priority);
    if (filters.status) params.append('status', filters.status);

    const response = await api.get(`/api/tasks/filter?${params.toString()}`);
    return response.data;
  },

  updateTaskStatus: async (taskId, status) => {
    const response = await api.put(`/api/tasks/${taskId}/status`, status, {
      params: { status },
    });
    return response.data;
  },

  deleteTask: async (taskId) => {
    const response = await api.delete(`/api/tasks/${taskId}`);
    return response.data;
  },
};

// Chat API
export const chatService = {
  sendMessage: async (message) => {
    const response = await api.post('/api/chat', { message });
    return response.data;
  },
};

// Insights API
export const insightsService = {
  getInsights: async () => {
    const response = await api.get('/api/insights');
    return response.data;
  },
};
