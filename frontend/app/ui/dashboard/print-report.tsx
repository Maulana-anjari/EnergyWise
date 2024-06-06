import { fetchReportByMonth } from '@/app/lib/data';

const PrintReport: React.FC<{ month: number }> = ({ month }) => {
    const handlePrint = async () => {
        const response = await fetchReportByMonth(month); 
        window.print();
    }
    return (
        <div className="relative inline-block">
            <button
                className="px-4 py-2 bg-green-900 text-white rounded hover:bg-green-600"
                // onClick={handlePrint}
            >
                Print Report
            </button>
        </div>
    );
};

export default PrintReport;
