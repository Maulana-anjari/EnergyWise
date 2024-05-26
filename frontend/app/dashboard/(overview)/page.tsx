import { Card } from '@/app/ui/dashboard/cards';
import { lusitana } from '@/app/ui/fonts';
import StatsCard from '@/app/ui/dashboard/stats-card';
import RevenueChart from '@/app/ui/dashboard/revenue-chart';
import ConsumptionChart from '@/app/ui/dashboard/consumption-chart';
import ConsumptionTable from '@/app/ui/dashboard/consumption-table';
import { 
  fetchAllEnergyConsumptions,
  fetchTotalEnergyConsumptionsByMonth,
 } from '@/app/lib/data';

export default async function Page({
  searchParams,
}: {
  searchParams?: {
    month?: number;
  };
}) { 
  const month = searchParams?.month || 1;
  const allEnergyConsumption = await fetchAllEnergyConsumptions();
  const currentDate = new Date();
  const currentMonth: number = currentDate.getMonth() + 1;
  const consumptionThisMonth = await fetchTotalEnergyConsumptionsByMonth(currentMonth);
  const totalConsumptionThisMonth: number = consumptionThisMonth.reduce((total: number, current: any) => total + current.energy_consumption, 0);
  const totalAllEnergyUsage: number = allEnergyConsumption.reduce((total: number, item: any) => total + item.energy_consumption, 0);
  const stats = [
    { title: 'Total Energy Usage All of Time', value: `${totalAllEnergyUsage.toFixed(2)} kWh` }, // Replace with actual data
    { title: 'Total Energy Usage This Month', value: `${totalConsumptionThisMonth.toFixed(2)} kWh` }, // Replace with actual data
    { title: 'Total Devices', value: '1' }, // Replace with actual data
  ];
  return (
    <main>
      <h1 className={`${lusitana.className} mb-4 text-xl md:text-2xl`}>
        Dashboard
      </h1>
      <div className="flex flex-wrap -mx-4">
        {stats.map((stat, index) => (
          <div key={index} className="px-4 py-2 w-full sm:w-1/2 lg:w-1/3">
            <StatsCard title={stat.title} value={stat.value} />
          </div>
        ))}
      </div>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        
      </div>
      <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-4 lg:grid-cols-8">
        {/* <RevenueChart/> */}
        < ConsumptionChart month={month} />
      </div>
      <div className="mt-6">
        {/* <RevenueChart/> */}
        <ConsumptionTable data={allEnergyConsumption} />
      </div>
    </main>
  );
}