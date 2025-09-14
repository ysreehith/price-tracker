import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { PriceHistory } from '../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface PriceChartProps {
  productName: string;
  priceHistory: PriceHistory[];
  onClose: () => void;
}

const PriceChart: React.FC<PriceChartProps> = ({
  productName,
  priceHistory,
  onClose,
}) => {
  // Sort price history by timestamp
  const sortedHistory = [...priceHistory].sort(
    (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  );

  const data = {
    labels: sortedHistory.map((entry) =>
      new Date(entry.timestamp).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    ),
    datasets: [
      {
        label: 'Price',
        data: sortedHistory.map((entry) => entry.price),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.1,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: `Price History - ${productName}`,
      },
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function (value: any) {
            return '$' + value.toFixed(2);
          },
        },
      },
    },
  };

  if (priceHistory.length === 0) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Price History - {productName}
          </h3>
          <p className="text-gray-500 mb-4">No price history available for this product.</p>
          <button
            onClick={onClose}
            className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-4xl w-full mx-4 max-h-[90vh] overflow-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-800">
            Price History - {productName}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>
        
        <div className="mb-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-600">Total Data Points:</span>
              <span className="ml-2 text-gray-800">{priceHistory.length}</span>
            </div>
            <div>
              <span className="font-medium text-gray-600">Date Range:</span>
              <span className="ml-2 text-gray-800">
                {new Date(sortedHistory[0].timestamp).toLocaleDateString()} -{' '}
                {new Date(sortedHistory[sortedHistory.length - 1].timestamp).toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>

        <div className="h-96">
          <Line data={data} options={options} />
        </div>

        <div className="mt-4 flex justify-end">
          <button
            onClick={onClose}
            className="bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default PriceChart;

