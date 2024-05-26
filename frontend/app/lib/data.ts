import { sql } from '@vercel/postgres';
import {
  CustomerField,
  CustomersTableType,
  InvoiceForm,
  InvoicesTable,
  LatestInvoiceRaw,
  User,
  Revenue,
  EnergyUsage,
  Consumption
} from './definitions';
import { formatCurrency } from './utils';
import { unstable_noStore as noStore } from 'next/cache';
const backend_url = process.env.BACKEND_URL || "http://127.0.0.1:5000"
const dummy_consumption = {
  "total_energy_usage": [
      {
          "energy_consumption": 568.0699999999999,
          "timestamp": "24-04-2024"
      },
      {
          "energy_consumption": 4359.340000000003,
          "timestamp": "25-04-2024"
      },
      {
          "energy_consumption": 4511.839999999999,
          "timestamp": "26-04-2024"
      },
      {
          "energy_consumption": 4633.669999999997,
          "timestamp": "27-04-2024"
      },
      {
          "energy_consumption": 4475.660000000004,
          "timestamp": "28-04-2024"
      },
      {
          "energy_consumption": 4461.489999999999,
          "timestamp": "29-04-2024"
      },
      {
          "energy_consumption": 4428.199999999999,
          "timestamp": "30-04-2024"
      }
  ]
}
function sliceTimestamps(consumption: Consumption[]): Consumption[] {
  return consumption.map(item => {
    if (item.timestamp && item.timestamp.length >= 2) {
      return { ...item, timestamp: item.timestamp.slice(0, 2) };
    }
    return item;
  });
}

export async function fetchTotalEnergyConsumptionsByMonth(month: number) {
  noStore();
  try {
    // uncomment kalau mau pake api
    const response = await fetch(`${backend_url}/api/energy/usage/total?month=${month}`);
    const data = await response.json();
    return data.energy_usage_month;

    // comment ini kalo mau pake api
    // const data = dummy_consumption;
    // const consumption: Consumption[] = data?.total_energy_usage;
    // const slicedConsumption = sliceTimestamps(consumption);
    
    // return slicedConsumption;
    // sampe sini
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch all energy consumption data.');
  }
}

export async function fetchAllEnergyConsumptions() {
  // ditampilin pake tabel
  noStore();
  const exampleData = {"energy_usage":[
    {
      "area": "100m2",
      "data_id": 1,
      "device_id": 1,
      "device_type": "energy_meter",
      "energy_consumption": 18.51,
      "floor": 1,
      "room_id": 1,
      "room_name": "Conference Room",
      "status": "active",
      "timestamp": "24-04-2024 21:13:40 GMT"
    },
    ,
    {
        "area": "20m2",
        "data_id": 8643,
        "device_id": 3,
        "device_type": "energy_meter",
        "energy_consumption": 12.12,
        "floor": 1,
        "room_id": 2,
        "room_name": "Office 101",
        "status": "active",
        "timestamp": "24-04-2024 21:13:40 GMT"
    },
    {
        "area": "100m2",
        "data_id": 4322,
        "device_id": 2,
        "device_type": "energy_meter",
        "energy_consumption": 6.6,
        "floor": 1,
        "room_id": 1,
        "room_name": "Conference Room",
        "status": "active",
        "timestamp": "24-04-2024 21:13:40 GMT"
    },

  ]};

  try {
    // uncomment kalo mau pake api
    const response = await fetch(`${backend_url}/api/energy/usage?type=all`);
    const data = await response.json();
    return data.energy_usage;
    // return exampleData.energy_usage;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch all energy consumption data.');
  }
}

export async function fetchEnergyConsumptionsByMonth(month: number) {
  noStore();
  try {
    const response = await fetch(`${backend_url}/api/energy/usage?type=month&month=${month}`);
    const data = await response.json();
    return data.energy_usage;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch all energy consumption data.');
  }
}

export async function fetchEnergyConsumptionsByDevice(device_id: number) {
  noStore();
  try {
    const response = await fetch(`${backend_url}/api/energy/usage?type=device&device_id=${device_id}`);
    const data = await response.json();
    return data.rows();
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch all energy consumption data.');
  }
}

export async function fetchEnergyConsumptionsByMonthDevice(month: number, device_id: number) {
  noStore();
  try {
    const response = await fetch(`${backend_url}/api/energy/usage?type=month-device&month=${month}&device_id=${device_id}`);
    const data = await response.json();
    return data.rows();
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch all energy consumption data.');
  }
}

export async function fetchRevenue() {
  // Add noStore() here to prevent the response from being cached.
  // This is equivalent to in fetch(..., {cache: 'no-store'}).
  noStore();
  try {
    const data = await sql<Revenue>`SELECT * FROM revenue`;
    return data.rows;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch revenue data.');
  }
}

export async function fetchLatestInvoices() {
  noStore();
  try {
    const data = await sql<LatestInvoiceRaw>`
      SELECT invoices.amount, customers.name, customers.image_url, customers.email, invoices.id
      FROM invoices
      JOIN customers ON invoices.customer_id = customers.id
      ORDER BY invoices.date DESC
      LIMIT 5`;

    const latestInvoices = data.rows.map((invoice) => ({
      ...invoice,
      amount: formatCurrency(invoice.amount),
    }));
    return latestInvoices;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch the latest invoices.');
  }
}

export async function fetchCardData() {
  noStore();
  try {
    // You can probably combine these into a single SQL query
    // However, we are intentionally splitting them to demonstrate
    // how to initialize multiple queries in parallel with JS.
    const invoiceCountPromise = sql`SELECT COUNT(*) FROM invoices`;
    const customerCountPromise = sql`SELECT COUNT(*) FROM customers`;
    const invoiceStatusPromise = sql`SELECT
         SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) AS "paid",
         SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END) AS "pending"
         FROM invoices`;

    const data = await Promise.all([
      invoiceCountPromise,
      customerCountPromise,
      invoiceStatusPromise,
    ]);

    const numberOfInvoices = Number(data[0].rows[0].count ?? '0');
    const numberOfCustomers = Number(data[1].rows[0].count ?? '0');
    const totalPaidInvoices = formatCurrency(data[2].rows[0].paid ?? '0');
    const totalPendingInvoices = formatCurrency(data[2].rows[0].pending ?? '0');

    return {
      numberOfCustomers,
      numberOfInvoices,
      totalPaidInvoices,
      totalPendingInvoices,
    };
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch card data.');
  }
}

const ITEMS_PER_PAGE = 6;
export async function fetchFilteredInvoices(
  query: string,
  currentPage: number,
) {
  noStore();
  const offset = (currentPage - 1) * ITEMS_PER_PAGE;

  try {
    const invoices = await sql<InvoicesTable>`
      SELECT
        invoices.id,
        invoices.amount,
        invoices.date,
        invoices.status,
        customers.name,
        customers.email,
        customers.image_url
      FROM invoices
      JOIN customers ON invoices.customer_id = customers.id
      WHERE
        customers.name ILIKE ${`%${query}%`} OR
        customers.email ILIKE ${`%${query}%`} OR
        invoices.amount::text ILIKE ${`%${query}%`} OR
        invoices.date::text ILIKE ${`%${query}%`} OR
        invoices.status ILIKE ${`%${query}%`}
      ORDER BY invoices.date DESC
      LIMIT ${ITEMS_PER_PAGE} OFFSET ${offset}
    `;

    return invoices.rows;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch invoices.');
  }
}

export async function fetchInvoicesPages(query: string) {
  noStore();
  try {
    const count = await sql`SELECT COUNT(*)
    FROM invoices
    JOIN customers ON invoices.customer_id = customers.id
    WHERE
      customers.name ILIKE ${`%${query}%`} OR
      customers.email ILIKE ${`%${query}%`} OR
      invoices.amount::text ILIKE ${`%${query}%`} OR
      invoices.date::text ILIKE ${`%${query}%`} OR
      invoices.status ILIKE ${`%${query}%`}
  `;

    const totalPages = Math.ceil(Number(count.rows[0].count) / ITEMS_PER_PAGE);
    return totalPages;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch total number of invoices.');
  }
}

export async function fetchInvoiceById(id: string) {
  noStore();
  try {
    const data = await sql<InvoiceForm>`
      SELECT
        invoices.id,
        invoices.customer_id,
        invoices.amount,
        invoices.status
      FROM invoices
      WHERE invoices.id = ${id};
    `;

    const invoice = data.rows.map((invoice) => ({
      ...invoice,
      // Convert amount from cents to dollars
      amount: invoice.amount / 100,
    }));

    return invoice[0];
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch invoice.');
  }
}

export async function fetchCustomers() {
  noStore();
  try {
    const data = await sql<CustomerField>`
      SELECT
        id,
        name
      FROM customers
      ORDER BY name ASC
    `;

    const customers = data.rows;
    return customers;
  } catch (err) {
    console.error('Database Error:', err);
    throw new Error('Failed to fetch all customers.');
  }
}

export async function fetchFilteredCustomers(query: string) {
  noStore();
  try {
    const data = await sql<CustomersTableType>`
		SELECT
		  customers.id,
		  customers.name,
		  customers.email,
		  customers.image_url,
		  COUNT(invoices.id) AS total_invoices,
		  SUM(CASE WHEN invoices.status = 'pending' THEN invoices.amount ELSE 0 END) AS total_pending,
		  SUM(CASE WHEN invoices.status = 'paid' THEN invoices.amount ELSE 0 END) AS total_paid
		FROM customers
		LEFT JOIN invoices ON customers.id = invoices.customer_id
		WHERE
		  customers.name ILIKE ${`%${query}%`} OR
        customers.email ILIKE ${`%${query}%`}
		GROUP BY customers.id, customers.name, customers.email, customers.image_url
		ORDER BY customers.name ASC
	  `;

    const customers = data.rows.map((customer) => ({
      ...customer,
      total_pending: formatCurrency(customer.total_pending),
      total_paid: formatCurrency(customer.total_paid),
    }));

    return customers;
  } catch (err) {
    console.error('Database Error:', err);
    throw new Error('Failed to fetch customer table.');
  }
}

export async function getUser(email: string) {
  noStore();
  try {
    const user = await sql`SELECT * FROM users WHERE email=${email}`;
    return user.rows[0] as User;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw new Error('Failed to fetch user.');
  }
}
