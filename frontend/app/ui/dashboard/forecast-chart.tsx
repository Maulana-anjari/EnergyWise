import { generateYAxisConsumption } from '@/app/lib/utils';
import { CalendarIcon } from '@heroicons/react/24/outline';
import { lusitana } from '@/app/ui/fonts';
import { fetchForecast } from '@/app/lib/data';
import DropdownMonth from '@/app/ui/dashboard/dropdown-month';
import BarChart from '@/app/ui/dashboard/bar-chart';
import {Consumption} from "@/app/lib/definitions"
function getMonthName(monthNumber: number): string {
  // Array of month names indexed from 0 (January) to 11 (December)
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  // Check if the monthNumber is within the valid range (1 to 12)
  if (monthNumber < 1 || monthNumber > 12) {
    throw new Error('Invalid month number. Please provide a number between 1 and 12.');
  }

  // Return the month name (note: monthNumber - 1 to convert to 0-based index)
  return monthNames[monthNumber - 1];
}
export default async function ForecastChart(){
  const consumption: Consumption[] = await fetchForecast();
  let data: any
  if (!consumption || consumption.length === 0) {
    data = {
      labels: [0,0,0],
      datasets: [
        {
          label: 'Energy Usage',
          data: [0,0,0],
          backgroundColor: 'rgb(21 128 61)',
        },
      ],
    };
  } else {
    data = {
      labels: consumption.map(item => item.timestamp),
      datasets: [
        {
          label: 'Energy Usage in kWh',
          data: consumption.map(item => item.energy_consumption),
          backgroundColor: 'rgb(21 128 61)',
        },
      ],
    };
  }
  
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: `Energy Consumption Forecasting`,
      },
    },
  };
  return (
    <div className="w-full md:col-span-4">
      <div className="rounded-xl bg-gray-50 p-4">
        <BarChart data={data} options={options} />
      </div>
    </div>
  );
}
