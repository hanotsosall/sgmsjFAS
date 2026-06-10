import { useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';
import { CharacterCard } from '../components/CharacterCard';
import { motion } from 'framer-motion';

export const Home = () => {
  const [characters, setCharacters] = useState([]);
  const { getCharacters } = useApi();

  useEffect(() => {
    getCharacters().then(res => setCharacters(res.data));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold bg-gradient-to-r from-neonPink to-neonPurple bg-clip-text text-transparent mb-4">
        Veluna
      </h1>
      <div className="grid grid-cols-2 gap-4">
        {characters.map((char: any) => (
          <motion.div key={char.id} whileHover={{ scale: 1.02 }}>
            <CharacterCard character={char} />
          </motion.div>
        ))}
      </div>
    </div>
  );
};