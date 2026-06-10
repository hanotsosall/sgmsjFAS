import { useEffect, useState } from 'react';

declare global {
  interface Window {
    Telegram: any;
  }
}

export function useTelegram() {
  const [tg, setTg] = useState<any>(null);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const telegram = window.Telegram?.WebApp;
    if (telegram) {
      telegram.expand();
      setTg(telegram);
      if (telegram.initDataUnsafe?.user) {
        setUser(telegram.initDataUnsafe.user);
      }
    }
  }, []);

  return { tg, user };
}