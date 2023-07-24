import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BeatLoader } from 'react-spinners';
import Head from 'next/head';

interface Data {
  Hour: string[];
  Status: string[];
  Home: string[];
  'Home Score': string[];
  'Away Score': string[];
  Away: string[];
}

export default function Home() {
  const webUrl = process.env.NEXT_PUBLIC_WEB_URL;

  const [data, setData] = useState<Data | null>(null);
  const today = new Date();
  const date = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;

  useEffect(() => {
    if (webUrl) {
      axios.get(webUrl).then((res) => {
        setData(res.data);
      });
    }
  }, [webUrl]);

  return (
    <>
      <Head>
        <title>Hello Games</title>
      </Head>
      <main className="flex flex-col items-center justify-center h-screen bg-gray-100">
        <h1 className="text-4xl font-semibold mt-12 mb-12">Games of {date}</h1>
        {data ? (
          <div className="overflow-auto w-full md:w-2/3 lg:w-[50%]">
            <table className="table-auto w-full bg-white">
              <thead className="bg-blue-500 text-white sticky top-0">
                <tr className="text-center">
                  <th className="px-4 py-2">Status</th>
                  <th className="px-4 py-2">Hour</th>
                  <th className="px-4 py-2">Home</th>
                  <th className="px-4 py-2">Score</th>
                  <th className="px-4 py-2">Away</th>
                </tr>
              </thead>
              <tbody>
                {data.Status.map((status, index) => (
                  <tr
                    key={index}
                    className={index % 2 === 0 ? 'bg-gray-100 text-center' : 'text-center'}
                  >
                    <td
                      className={`border px-4 py-2 font-bold ${
                        status === 'Terminado'
                          ? 'text-red-500'
                          : status === 'Em breve'
                          ? 'text-yellow-600'
                          : 'text-green-600'
                      }`}
                    >
                      {status === 'Terminado'
                        ? 'Finished'
                        : status === 'Em breve'
                        ? 'Soon'
                        : 'Live'}
                    </td>
                    <td className="border px-4 py-2">{data.Hour[index]}</td>
                    <td className="border px-4 py-2">{data.Home[index]}</td>
                    <td className="border px-4 py-2">
                      {data['Home Score'][index]
                        ? `${data['Home Score'][index]} - ${data['Away Score'][index]}`
                        : 'VS'}
                    </td>
                    <td className="border px-4 py-2">{data.Away[index]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <BeatLoader color="#4A90E2" />
        )}
      </main>
    </>
  );
}
