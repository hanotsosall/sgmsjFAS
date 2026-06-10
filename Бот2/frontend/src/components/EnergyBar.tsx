export const EnergyBar = ({ energy, gems }: { energy: number; gems: number }) => (
  <div className="bg-black/80 p-2 flex justify-between text-sm border-b border-gray-800">
    <span>⚡ {energy}</span>
    <span>💎 {gems}</span>
  </div>
);