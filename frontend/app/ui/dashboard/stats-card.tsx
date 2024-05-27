import React from 'react';

const StatsCard = ({ title, value}: {title: string, value: string}) => {
  return (
    <div className="bg-white shadow-lg rounded-lg p-4 flex-grow">
      <h3 className="text-gray-500 text-sm font-medium">{title}</h3>
      <p className="text-xl font-semibold text-gray-900">{value}</p>
    </div>
  );
};

export default StatsCard;
