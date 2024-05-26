'use client'
import React, { useState, useEffect } from 'react';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';

const months = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

const DropdownMonth: React.FC = () => {
  const [selectedMonth, setSelectedMonth] = useState<string>('');
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  useEffect(() => {
    const monthParam = searchParams.get('month');
    if (monthParam) {
      setSelectedMonth(monthParam);
    }
  }, [searchParams]);

  const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedMonth = event.target.value;
    setSelectedMonth(selectedMonth);
    handleSelectMonth(selectedMonth);
  };

  function handleSelectMonth(term: string) {
    const params = new URLSearchParams(searchParams.toString());
    if (term) {
      params.set('month', term);
    } else {
      params.delete('month');
    }
    replace(`${pathname}?${params.toString()}`);
  }

  return (
    <div className="relative inline-block">
      <select
        className="block w-50 appearance-none rounded-lg border border-gray-300 bg-white px-4 py-2 pr-8 leading-tight text-gray-700 shadow focus:border-blue-500 focus:outline-none focus:shadow-outline-blue"
        value={selectedMonth}
        onChange={handleSelectChange}
      >
        <option value="" disabled>
          Select a month
        </option>
        {months.map((month, index) => (
          <option key={index} value={index+1}>
            {month}
          </option>
        ))}
      </select>
    </div>
  );
};

export default DropdownMonth;
