import React, { useEffect, useState } from 'react';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { QueryCommand } from '@aws-sdk/lib-dynamodb';

// Configure AWS DynamoDB Client
const dynamoDBClient = new DynamoDBClient({
  region: 'eu-west-3',
  credentials: {
    accessKeyId: import.meta.env.VITE_REACT_APP_ACCESS_KEY_ID,
    secretAccessKey: import.meta.env.VITE_REACT_APP_SECRET_ACCESS_KEY,
  },
});

interface LastItem {
  UserID: string;
  name: string;
  email: string;
  phone: string;
  age: string;
  date: string;
  prediction: string;
}




const LastItemDisplay: React.FC = () => {
  const [lastItem, setLastItem] = useState<LastItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isFraud, setIsFraud] = useState<boolean>(false);

  useEffect(() => {
    const fetchLastItem = async () => {
      const params = {
        TableName: 'FraudDetection',
        KeyConditionExpression: 'UserID  = :id',
        ExpressionAttributeValues: {
          ':id': 'static_id',
        },
        ScanIndexForward: false, 
        Limit: 1,
      };

      try {
        const data = await dynamoDBClient.send(new QueryCommand(params));
        const item = data.Items && data.Items.length > 0 ? data.Items[0] : null;
        setLastItem(item as LastItem);
        if (item) {
          setIsFraud(item.prediction === 'Not Fraud');
        }
        console.log(item);

      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchLastItem();

    const intervalId = setInterval(fetchLastItem, 2000); // Adjust the interval as needed

    return () => clearInterval(intervalId);
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="w-screen h-screen bg-hero-bg bg-no-repeat bg-cover flex justify-start items-center p-52 ">
      <div className="w-[40%] ">
        {lastItem ? (
          <div className=" h-72 w-[100%] relative backdrop-blur-lg bg-white/30 shadow-lg rounded-xl flex flex-col justify-between text-black">
            <div className="flex-1 flex flex-col justify-center items-start p-4">
              <h3 className="text-2xl font-bold mb-2">Current User</h3>
              <p className="text-lg">
                Name: <span className="font-bold">{lastItem.name}</span>
              </p>
              <p className="text-lg">
                Email: <span className="font-bold">{lastItem.email}</span>
              </p>
              <p className="text-lg">
                Phone: <span className="font-bold">{lastItem.phone}</span>
              </p>
              <p className="text-lg">
                Age: <span className="font-bold">{lastItem.age}</span>
              </p>
              <p className="text-lg">
                Date: <span className="font-bold">{lastItem.date}</span>
              </p>
              <p className="text-lg">
                Transaction Type:{' '}
                <span
                  className={`font-bold text-2xl ${
                    isFraud ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {lastItem.prediction}
                </span>
              </p>
            </div>
          </div>
        ) : (
          <div>No items found.</div>
        )}
      </div>
    </div>
  );
};

export default LastItemDisplay;
