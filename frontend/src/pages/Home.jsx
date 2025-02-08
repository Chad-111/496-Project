import React from "react";

const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="p-4 bg-yellow-100 border-l-4 border-yellow-500 shadow-md rounded-lg max-w-md text-center">
        <h2 className="text-2xl font-bold text-yellow-800">🚧 Under Construction 🚧</h2>
        <p className="text-gray-700 mt-2">We're working hard to bring you an amazing experience. Stay tuned!</p>
        <div className="mt-4 flex justify-center">
          <img src="/assets/construction-animation.svg" alt="Under Construction" className="w-48" />
        </div>
      </div>
    </div>
  );
};

export default Home;
