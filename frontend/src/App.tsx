import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { BottomNav } from './components/BottomNav';
import { Home } from './pages/Home';
import { Chats } from './pages/Chats';
import { CharacterProfile } from './pages/CharacterProfile';
import { ChatRoom } from './pages/ChatRoom';
import { Studio } from './pages/Studio';
import { Profile } from './pages/Profile';
import { Shop } from './pages/Shop';

function App() {
  return (
    <BrowserRouter>
      <div className="bg-dark min-h-screen text-white pb-16">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chats" element={<Chats />} />
          <Route path="/character/:id" element={<CharacterProfile />} />
          <Route path="/chat/:characterId" element={<ChatRoom />} />
          <Route path="/studio" element={<Studio />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/shop" element={<Shop />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
        <BottomNav />
      </div>
    </BrowserRouter>
  );
}

export default App;