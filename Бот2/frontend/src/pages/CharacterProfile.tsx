import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';

export const CharacterProfile = () => {
  const { id } = useParams();
  const [character, setCharacter] = useState<any>(null);
  const { getCharacters } = useApi();
  const navigate = useNavigate();

  useEffect(() => {
    getCharacters().then(res => {
      const found = res.data.find((c: any) => c.id === parseInt(id!));
      setCharacter(found);
    });
  }, [id]);

  if (!character) return <div className="p-4">Загрузка...</div>;

  return (
    <div className="pb-20">
      <img src={character.large_art_url} className="w-full h-64 object-cover" />
      <div className="p-4">
        <h1 className="text-3xl font-bold">{character.name}</h1>
        <p className="text-gray-300 mt-2">{character.short_desc}</p>
        <div className="mt-4">
          <h2 className="text-xl font-semibold">О персонаже</h2>
          <p className="text-gray-400 mt-1">{character.lore}</p>
        </div>
        {character.scenarios?.length > 0 && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold">Сценарии</h2>
            <Swiper spaceBetween={12} slidesPerView={1.2} className="mt-2">
              {character.scenarios.map((sc: any) => (
                <SwiperSlide key={sc.id}>
                  <div className="bg-card rounded-xl p-3">
                    <img src={sc.cover} className="w-full h-32 object-cover rounded-lg" />
                    <h3 className="font-bold mt-2">{sc.title}</h3>
                    <p className="text-xs text-gray-400">{sc.intro}</p>
                    <button
                      onClick={() => navigate(`/chat/${character.id}?scenario=${sc.id}`)}
                      className="mt-2 bg-gradient-to-r from-neonPink to-neonPurple px-4 py-1 rounded-full text-sm"
                    >
                      ИГРАТЬ
                    </button>
                  </div>
                </SwiperSlide>
              ))}
            </Swiper>
          </div>
        )}
        <button
          onClick={() => navigate(`/chat/${character.id}`)}
          className="mt-6 w-full bg-gradient-to-r from-neonPink to-neonPurple py-3 rounded-full font-bold text-lg"
        >
          ИГРАТЬ
        </button>
      </div>
    </div>
  );
};