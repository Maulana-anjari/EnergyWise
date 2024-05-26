import { generateYAxisConsumption } from '@/app/lib/utils';
import { CalendarIcon } from '@heroicons/react/24/outline';
import { lusitana } from '@/app/ui/fonts';
import { fetchTotalEnergyConsumptionsByMonth } from '@/app/lib/data';
import DropdownMonth from '@/app/ui/dashboard/dropdown-month';

export default async function ConsumptionChart({month}:{month: any}){
  const consumption = await fetchTotalEnergyConsumptionsByMonth(month);
  const chartHeight = 250;
  const totalConsumption: number = consumption.reduce((total, current) => total + current.energy_consumption, 0);
  
  const { yAxisLabels, topLabel } = generateYAxisConsumption(consumption);

  if (!consumption || consumption.length === 0) {
    return <p className="mt-4 text-gray-400">No data available.</p>;
  }

  return (
    <div className="w-full md:col-span-4">
      <h2 className={`${lusitana.className} mb-4 text-xl md:text-2xl`}>
        Total Energy Consumptions day-by-day
      </h2>
      {/* NOTE: comment in this code when you get to this point in the course */}
      <div className="flex items-center justify-end mb-4">
          <DropdownMonth />
      </div>
      <div className="rounded-xl bg-gray-50 p-4">
        <div className="sm:grid-cols-13 mt-0 grid grid-cols-12 items-end gap-2 rounded-md bg-white p-4 md:gap-4">
          <div
            className="mb-6 hidden flex-col justify-between text-sm text-gray-400 sm:flex mr-4"
            style={{ height: `${chartHeight}px` }}
          >
            {yAxisLabels.map((label) => (
              <p key={label}>{label}</p>
            ))}
          </div>

          {consumption.map((item: any) => (
            <div key={item.timestamp} className="flex flex-col items-center gap-2">
              <div
                className="w-full rounded-md bg-green-300"
                style={{
                  height: `${(chartHeight / topLabel) * item.energy_consumption}px`,
                }}
              ></div>
              <p className="-rotate-90 text-sm text-gray-400 sm:rotate-0">
                {item.timestamp}
              </p>
            </div>
          ))}
        </div>
        <div className="flex items-center pb-2 pt-6">
          <CalendarIcon className="h-5 w-5 text-gray-500" />
          <h3 className="ml-2 text-sm text-gray-500 ">Total consumption in one month <span className='font-bold'>{totalConsumption.toFixed(2)} kWh</span></h3>
        </div>
      </div>
    </div>
  );
}
