// Shop.tsx
export const Shop = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Магазин</h1>
      <div className="mt-4 space-y-3">
        <div className="bg-card rounded-xl p-3 flex justify-between">
          <span>💎 50 гемов</span>
          <button className="bg-neonPink px-4 py-1 rounded-full">25⭐</button>
        </div>
        <div className="bg-card rounded-xl p-3 flex justify-between">
          <span>⚡ +20 энергии</span>
          <button className="bg-neonPink px-4 py-1 rounded-full">10⭐</button>
        </div>
      </div>
    </div>
  );
};