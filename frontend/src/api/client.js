const BASE_URL = import.meta.env.VITE_API_URL || 'https://learning-mentor-app.onrender.com';

export const getToken = () => localStorage.getItem('access_token');

export const setTokens = (access, refresh) => {
  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
};

export const clearTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export const isLoggedIn = () => !!getToken();

const request = async (method, path, body = null) => {
  const headers = { 'Content-Type': 'application/json' };
  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 95000); // 95s timeout for sleeping server

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
      signal: controller.signal,
    });
    clearTimeout(timeout);

    if (res.status === 401) {
      clearTokens();
      window.location.href = '/login';
      return;
    }

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || data.detail || JSON.stringify(data));
    return data;
  } catch (err) {
    clearTimeout(timeout);
    if (err.name === 'AbortError') throw new Error('সার্ভার সাড়া দিচ্ছে না। পরে আবার চেষ্টা করো।');
    throw err;
  }
};

export const api = {
  login: (username, password) =>
    request('POST', '/api/auth/login/', { username, password }),

  getToday: () => request('GET', '/api/today/'),

  submitWork: (lessonId, code, explanation) =>
    request('POST', `/api/lessons/${lessonId}/submissions/`, { code, explanation }),

  submitFile: async (lessonId, file, explanation) => {
    const token = getToken();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('explanation', explanation);

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 180000); // 3 min for large files

    try {
      const res = await fetch(`${BASE_URL}/api/lessons/${lessonId}/file-submissions/`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData,
        signal: controller.signal,
      });
      clearTimeout(timeout);
      if (res.status === 401) { clearTokens(); window.location.href = '/login'; return; }
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || data.detail || JSON.stringify(data));
      return data;
    } catch (err) {
      clearTimeout(timeout);
      if (err.name === 'AbortError') throw new Error('সার্ভার সাড়া দিচ্ছে না। পরে আবার চেষ্টা করো।');
      throw err;
    }
  },

  getProgress: () => request('GET', '/api/progress/'),
  getLessons: () => request('GET', '/api/lessons/'),
  getLesson: (id) => request('GET', `/api/lessons/${id}/`),
  getStages: () => request('GET', '/api/stages/'),
};
