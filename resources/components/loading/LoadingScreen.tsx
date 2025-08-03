
interface LoadingScreenProps {
  image: string;
}

function LoadingScreen({ image }: LoadingScreenProps) {
  return (
    <div className="flex flex-col justify-center items-center h-screen bg-white text-gray-700">
      <img
        src={image}
        alt="Loading Logo"
        className="w-72 h-72 animate-pulse mb-4"
      />
      <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-2" />
      {/* <p className="text-lg font-medium animate-pulse">Loading your experience...</p> */}
    </div>
  );
}

export default LoadingScreen;
