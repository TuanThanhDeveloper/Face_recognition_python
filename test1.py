import requests
import csv
from datetime import datetime
URL = "http://127.0.0.1:5000/"
print(datetime.now().strftime("%d/%m/%Y"))
print(datetime.now().strftime("%X"))
for i in range(1,20):
    response = requests.post(URL + f"log/{i}", data={"id_user": i})
    # response = requests.put(URL + f"user/{i}", data={"id": i, "name": f"thanh-{i}", "age": 21, "sex": "male"} )
    # response = requests.post(URL + f"log/{i}", data={"id_user": i, "day": "28/11/2021", "time": f'{datetime.now().strftime("%X")}'})
    print(response.json())

# with open("data.csv", encoding="utf-8", ) as f:
#     read = csv.reader(f, delimiter=',')
#     i = 1
#     for row in read:
#         response = requests.put(URL + f"user/{i}", data={"id": i, "name": f"{row[0]}", "age": f'{row[2]}', "sex": f"{row[1]}"})
#         print(response.json())
#         i+=1