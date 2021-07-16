#! /usr/bin/python3

from fastapi.encoders import jsonable_encoder
import pickle


def serialize(data):
    data = jsonable_encoder(data)
    with open("serialize.txt",'ab') as file:
        pickle.dump(data,file)
    
    return (200,{"data":data,"msg":"Data has been serialized!"})

def deserialize():
    file = open('serialize.txt','rb')
    data = pickle.load(file)
    print(data)
    file.close()
    return data


# deserialize("string")