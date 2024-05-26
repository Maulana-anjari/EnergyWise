import { lusitana } from '@/app/ui/fonts';
import Image from 'next/image';

export default function EnergyWiseLogo() {
  return (
    <div
      className={`${lusitana.className} flex flex-row items-center leading-none text-white`}
    >
      <Image 
            src="/logo-energy-wise.png"
            width={100}
            height={100}
            className=''
            alt="Logo"
          />
      <p className="text-[44px]">Energy Wise</p>
    </div>
  );
}
