import { useParams, useSearchParams } from 'react-router-dom';
import { useEffect, useState, useRef } from 'react';
import { useApi } from '../hooks/useApi';
import { MessageBubble } from '../components/MessageBubble';
import { EnergyBar } from '../components/EnergyBar';

export const ChatRoom = () => {
  const { characterId } = useParams();
  const [searchParams] = useSearchParams();
  const scenarioId = searchParams.get('scenario');
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState('');
  const [energy, setEnergy] = useState(30);
  const [gems, setGems] = useState(0);
  const { sendMessage, getHistory, getUserBalance } = useApi();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getHistory(parseInt(characterId!)).then(res => setMessages(res.data));
    getUserBalance().then(res => {
      setEnergy(res.data.energy);
      setGems(res.data.gems);
    });
  }, []);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user', content: input, created_at: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    try {
      const res = await sendMessage(parseInt(characterId!), input, scenarioId ? parseInt(scenarioId) : undefined);
      const assistantMsg = { role: 'assistant', content: res.data.reply, created_at: new Date().toISOString() };
      setMessages(prev => [...prev, assistantMsg]);
      setEnergy(res.data.energy_left);
    } catch (err: any) {
      if (err.response?.status === 400) alert(err.response.data.detail);
    }
    setInput('');
  };

  const handleImageCommand = async (prompt: string) => {
    // OOC-генерация
    setInput(`!img ${prompt}`);
    await handleSend();
  };

  return (
    <div className="flex flex-col h-screen">
      <EnergyBar energy={energy} gems={gems} />
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-3 border-t border-gray-800 bg-card flex gap-2">
        <input
          className="flex-1 bg-gray-900 rounded-full px-4 py-2 text-white outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Сообщение... /img для генерации"
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend} className="bg-gradient-to-r from-neonPink to-neonPurple px-5 rounded-full font-bold">
          ➤
        </button>
      </div>
    </div>
  );
};