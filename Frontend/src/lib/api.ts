import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function createUser(email: string, password: string) {
  return axios.post(`${API_URL}/create_user`, { email, password });
}

export async function loginUser(email: string, password: string) {
  return axios.post(`${API_URL}/login`, { email, password });
}

export async function getUserData(token: string) {
  return axios.get(`${API_URL}/get_user_data`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getUserStatistics(token: string) {
  return axios.get(`${API_URL}/user_statistics`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getStatistics(token: string) {
  return axios.get(`${API_URL}/statistics`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getHomePage(token: string) {
  return axios.get(`${API_URL}/home_page`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function trackReportPhishing() {
  return axios.get(`${API_URL}/track/report_phising.png`, {
    responseType: "arraybuffer",
  });
}