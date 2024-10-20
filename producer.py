from kafka import KafkaProducer
from json import dumps
import time
import pandas as pd
import random
from faker import Faker
import random
import string

fake = Faker()

bootstrap_servers = '15.188.65.61:9092'
topic = 'Topic4CreditCard'  

producer = KafkaProducer(bootstrap_servers= bootstrap_servers,
              api_version=(0,11,5),
              value_serializer=lambda x: dumps(x).encode('utf-8'))


client_data = pd.read_csv('./ML_Model/data/simulation_data.csv')


print("Producer started...")
try :
          while True:
                    
                    random_row = client_data.sample(n=1)
                    random_row = random_row.to_dict(orient='records')[0]
                    random_row['UserID'] = 'static_id' # partition key
                    random_row['name'] = fake.name()
                    random_row['email'] = fake.email()
                    random_row['phone'] = fake.phone_number()
                    random_row['age'] = fake.random_int(min=18, max=80)
                    random_row['date'] = time.strftime('%Y-%m-%d %H:%M:%S') # sort key
                    # sleep_duration = random.uniform(2, 10)  
                    time.sleep(2)
                    producer.send(topic, value=random_row) 
                    print(f"message sent!")  
                    # print(random_row)    
except Exception as e:
          print(f'Error sending message: {e}')
finally:
          producer.close()
