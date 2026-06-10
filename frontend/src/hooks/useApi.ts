import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

export const useApi = () => {
  const getCharacters = () => api.get('/characters');
  const sendMessage = (characterId: number, text: string, scenarioId?: number) =>
    api.post('/chat/send', { character_id: characterId, text, scenario_id: scenarioId });
  const getHistory = (characterId: number) => api.get(`/chat/history/${characterId}`);
  const getUserBalance = () => api.get('/user/balance');
  const buyGems = (gems: number, stars: number) => api.post('/shop/buy_gems', { gems, stars_cost: stars });
  const completeTask = (taskId: string) => api.post(`/tasks/complete/${taskId}`);
  
  return { getCharacters, sendMessage, getHistory, getUserBalance, buyGems, completeTask };
};