import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: { translation: { "chats": "Chats", "studio": "Studio", "profile": "Profile", "shop": "Shop" } },
  ru: { translation: { "chats": "Чаты", "studio": "Студия", "profile": "Профиль", "shop": "Магазин" } },
  ja: { translation: { "chats": "チャット", "studio": "スタジオ", "profile": "プロフィール", "shop": "ショップ" } },
  zh: { translation: { "chats": "聊天", "studio": "工作室", "profile": "个人资料", "shop": "商店" } },
  ko: { translation: { "chats": "채팅", "studio": "스튜디오", "profile": "프로필", "shop": "상점" } },
  tr: { translation: { "chats": "Sohbetler", "studio": "Stüdyo", "profile": "Profil", "shop": "Mağaza" } }
};

i18n.use(initReactI18next).init({
  resources,
  lng: "en",
  fallbackLng: "en",
  interpolation: { escapeValue: false }
});

export default i18n;