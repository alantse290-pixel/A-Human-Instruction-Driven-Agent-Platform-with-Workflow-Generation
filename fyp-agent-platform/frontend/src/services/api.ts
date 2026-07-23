// API 調用封裝
import axios from 'axios';


const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export async function sendMessage(message: string): Promise<string> {
  // 發送消息到後端 API
  const response = await api.post('/chat/send', { message });
  return response.data.reply;
}

export default api;