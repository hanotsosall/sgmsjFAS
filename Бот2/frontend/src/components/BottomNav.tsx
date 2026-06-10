import { NavLink } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export const BottomNav = () => {
  const { t } = useTranslation();
  const navItems = [
    { path: '/', icon: '🏠', label: t('chats') },
    { path: '/studio', icon: '✨', label: t('studio') },
    { path: '/profile', icon: '👤', label: t('profile') },
    { path: '/shop', icon: '🛒', label: t('shop') },
  ];
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-black/80 backdrop-blur-lg border-t border-gray-800 flex justify-around py-2">
      {navItems.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) => `flex flex-col items-center p-2 ${isActive ? 'text-neonPink' : 'text-gray-400'}`}
        >
          <span className="text-2xl">{item.icon}</span>
          <span className="text-xs mt-1">{item.label}</span>
        </NavLink>
      ))}
    </div>
  );
};