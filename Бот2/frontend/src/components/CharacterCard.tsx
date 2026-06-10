import { Link } from 'react-router-dom';

export const CharacterCard = ({ character }: { character: any }) => (
  <Link to={`/character/${character.id}`}>
    <div className="bg-card rounded-2xl overflow-hidden shadow-lg">
      <img src={character.avatar_url} alt={character.name} className="w-full h-40 object-cover" />
      <div className="p-2">
        <h3 className="font-bold text-center">{character.name}</h3>
        <p className="text-xs text-gray-400 text-center truncate">{character.short_desc}</p>
      </div>
    </div>
  </Link>
);