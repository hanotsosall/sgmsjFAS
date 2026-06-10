export const MessageBubble = ({ message }: { message: any }) => {
  const isUser = message.role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[80%] rounded-2xl p-3 ${isUser ? 'bg-neonPurple text-white' : 'bg-gray-800 text-gray-100'}`}>
        {message.is_generated_image && message.image_url ? (
          <img src={message.image_url} className="rounded-lg max-w-full" />
        ) : (
          <p>{message.content}</p>
        )}
        <span className="text-xs opacity-50 block mt-1">
          {new Date(message.created_at).toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
};