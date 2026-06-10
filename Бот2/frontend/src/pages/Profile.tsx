// Profile.tsx
import { useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';

export const Profile = () => {
  const [balance, setBalance] = useState({ energy: 0, gems: 0 });
  const { getUserBalance } = useApi();
  useEffect(() => {
    getUserBalance().then(res => setBalance(res.data));
  }, []);
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Профиль</h1>
      <div className="mt-4 bg-card rounded-xl p-4">
        <p>⚡ Энергия: {balance.energy}</p>
        <p>💎 Гемы: {balance.gems}</p>
      </div>
    </div>
  );
};