import { useState } from 'react';
import { useApi } from '../hooks/useApi';

export const Studio = () => {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState('');
  const { getUserBalance } = useApi();

  const generate = async () => {
    if (!prompt) return;
    setLoading(true);
    // Отправляем команду через бот (прямой запрос к бекенду генерации)
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });
    const data = await res.json();
    if (data.url) setImageUrl(data.url);
    setLoading(false);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Студия генерации</h1>
      <textarea
        className="w-full bg-gray-900 rounded-xl p-3 mt-2 text-white"
        rows={3}
        placeholder="Опишите изображение..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        onClick={generate}
        disabled={loading}
        className="mt-3 w-full bg-gradient-to-r from-neonPink to-neonPurple py-2 rounded-full font-bold"
      >
        {loading ? 'Генерация...' : 'Сгенерировать (5 💎)'}
      </button>
      {imageUrl && <img src={imageUrl} className="mt-4 rounded-xl" />}
    </div>
  );
};