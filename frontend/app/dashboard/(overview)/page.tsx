import { Card } from '@/app/ui/dashboard/cards';
import { lusitana } from '@/app/ui/fonts';
import StatsCard from '@/app/ui/dashboard/stats-card';
import RevenueChart from '@/app/ui/dashboard/revenue-chart';
import ConsumptionChart from '@/app/ui/dashboard/consumption-chart';

import ConsumptionTable from '@/app/ui/dashboard/consumption-table';
import { 
  fetchAllEnergyConsumptions,
  fetchRooms,
  fetchDevices,
  fetchTotalEnergyConsumptionsByMonth,
 } from '@/app/lib/data';
import { Suspense } from 'react';
import { RevenueChartSkeleton, CardSkeleton } from '@/app/ui/skeletons';

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
  const numberOfRooms = await fetchRooms();
  const numberOfDevices = await fetchDevices();

  const totalConsumptionThisMonth: number = consumptionThisMonth.reduce((total: number, current: any) => total + current.energy_consumption, 0);
  const totalAllEnergyUsage: number = allEnergyConsumption.reduce((total: number, item: any) => total + item.energy_consumption, 0);
  const stats = [
    { title: 'Total Energy Usage All of Time', value: `${totalAllEnergyUsage.toFixed(2)} kWh` }, // Replace with actual data
    { title: 'Total Energy Usage This Month', value: `${totalConsumptionThisMonth.toFixed(2)} kWh` }, // Replace with actual data
    { title: 'Number of Devices', value: numberOfRooms }, // Replace with actual data
    { title: 'Number of Rooms', value: numberOfDevices }, // Replace with actual data
  ];
  return (
    <main>
      <h1 className={`${lusitana.className} mb-4 text-xl md:text-2xl`}>
        Dashboard
      </h1>
      <div className="flex flex-wrap -mx-4">
        {stats.map((stat, index) => (
          <div key={index} className="px-4 py-2 w-full sm:w-1/2 lg:w-1/4">
            <Suspense fallback={<CardSkeleton />}>
              <StatsCard title={stat.title} value={stat.value} />
            </Suspense>
          </div>
        ))}
      </div>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        
      </div>
      <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-4 lg:grid-cols-8">
        <Suspense fallback={<RevenueChartSkeleton />}>
          < ConsumptionChart month={month} />
        </Suspense>
      </div>
      <div className="mt-6">
        {/* <RevenueChart/> */}
        {/* <ConsumptionTable data={allEnergyConsumption} /> */}
      </div>
    </main>
  );
}