import { Card } from '@/app/ui/dashboard/cards';
import { lusitana } from '@/app/ui/fonts';
import ForecastChart from '@/app/ui/dashboard/forecast-chart';

export default async function Page() {
  return (
    <main>
      <h1 className={`${lusitana.className} mb-4 text-xl md:text-2xl`}>
        Energy Consumption Forecast H+1
      </h1>
      <div className="grid gap-6">
        < ForecastChart />
      </div>
      <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-4 lg:grid-cols-8">
        
      </div>
    </main>
  );
}