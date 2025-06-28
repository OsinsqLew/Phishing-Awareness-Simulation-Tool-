import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function createUser(email: string, password: string, firstName: string, lastName: string, tags?: string) {
  return axios.post(
    `${API_URL}/create_user`,
    {
      email_address: email,
      password,
      first_name: firstName,
      last_name: lastName,
      tags: tags || ""
    }
  );
}

export async function loginUser(email: string, password: string) {

  return axios.post(`${API_URL}/login`, null, {
    params: { email, password }
  });
}

export async function getUserData(token: string, userId: number) {
  return axios.get(`${API_URL}/get_user_data`, {
    params: { user_id: userId, token }
  });
}

export async function getUserStatistics(token: string, userId: number) {
  return axios.get(`${API_URL}/user_statistics`, {
    params: { user_id: userId, token }
  });
}

export async function getStatistics() {
  return axios.get(`${API_URL}/statistics`);
}

export async function getHomePage(reference: string) {
  return axios.get(`${API_URL}/home_page`, {
    params: { reference }
  });
}

export async function trackReportPhishing(reference: string) {
  return axios.get(`${API_URL}/track/report_phising.png`, {
    params: { reference },
    responseType: "arraybuffer"
  });
}