#! /usr/bin/python3

from pydantic import BaseModel
from typing import Optional

data_dict = {}


class Item(BaseModel):
    providerID : str 
    active : Optional[bool]=True
    name : str
    qualification:list
    speciality:list
    phone:int 
    department:Optional[str]=None
    organization:str
    location:Optional[str]=None
    address:str


class Update(BaseModel):
    providerID : str 
    active : Optional[bool]=None
    name : Optional[str]=None
    qualification:Optional[list]=None
    speciality:Optional[list]=None
    phone:Optional[int]=0 
    department:Optional[str]=None
    organization:Optional[str]=None
    location:Optional[str]=None
    address:Optional[str]=None
