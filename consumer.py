# Create a Kafka consumer
from kafka import KafkaConsumer
import json
import pickle
import warnings
import boto3 
from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning)

dynamodb = boto3.resource('dynamodb' , region_name='eu-west-3')# paris
table = dynamodb.Table('FraudDetection')


consumer = KafkaConsumer(
    'Topic4CreditCard',
    bootstrap_servers='15.188.65.61:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Avoid decoding empty messages
)

with open('./ML_model/model.pkl', 'rb') as file:
          model = pickle.load(file)    




print("Consumer started...")
for i , message in enumerate(consumer) :
          model_input = message.value
          model_input = [model_input['V1'], model_input['V2'], model_input['V3'], model_input['V4'], model_input['V5'], model_input['V6'], model_input['V7'], model_input['V8'], model_input['V9'], model_input['V10'], model_input['V11'], model_input['V12'], model_input['V13'], model_input['V14'], model_input['V15'], model_input['V16'], model_input['V17'], model_input['V18'], model_input['V19'], model_input['V20'], model_input['V21'], model_input['V22'], model_input['V23'], model_input['V24'], model_input['V25'], model_input['V26'], model_input['V27'], model_input['V28'], model_input['Amount']]
          prediction = model.predict([model_input])
          prediction = prediction[0]
          print(prediction)
          prediction = 'Fraud' if prediction == -1 else 'Not Fraud'
          print(f"Prediction: {prediction}")
          print(f'real value: {message.value["Class"]}') 
          
          response = table.put_item(
          Item={
            'UserID': message.value['UserID'],  
            'name': message.value['name'],
            'email': message.value['email'],
            'phone': message.value['phone'],
            'age': message.value['age'],
            'date': message.value['date'], 
            'prediction': prediction,

          })
          print(f"getting Response")

          
          

#     print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
#                                           message.offset, message.key,
#                                           message.value))

          # print(f"Received message: {message.value}")
        
