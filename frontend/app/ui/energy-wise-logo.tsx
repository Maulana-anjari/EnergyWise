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
        className='hidden md:block'
        alt="Logo"
      />
      <Image 
        src="/logo-energy-wise.png"
        width={60}
        height={60}
        className='block md:hidden'
        alt="Logo"
      />
      <p className="text-[36px] px-5 md:text-[36px]">Energy Wise</p>
    </div>
  );
}
