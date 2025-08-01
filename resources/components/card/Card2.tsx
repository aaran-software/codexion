type Card2Item = {
  title: string;
  body: string;
};

type Card2Props = {
  items: Card2Item[];
  containerStyle?:string;
};

export default function Card2({ items, containerStyle }: Card2Props) {
  return (
    <div className={`grid pt-10 gap-8 ${containerStyle}`}>
      {items.map((item, idx) => (
        <div
          key={idx}
          className="flex items-start gap-4 p-4 rounded-lg shadow-md bg-gray-50"
        >
          {/* Optional icon placeholder */}
          <div className="w-2 h-8 bg-green-600 rounded" aria-hidden="true" />
          <div className="flex flex-col gap-3">
            <p className="text-lg font-medium text-gray-700">{item.title}</p>
            <p className="text-sm font-medium text-gray-700">{item.body}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
