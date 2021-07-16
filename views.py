#! /usr/bin/python3

from fastapi import HTTPException,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import pickle
from pydantic import BaseModel
from typing import Optional
from models import Item,Update,data_dict
from fastapi import FastAPI,Query
from functions import serialize,deserialize
from pathlib import Path


app = FastAPI()
try:
    data_dict = deserialize()
except:
    data_dict={}

app.mount("/static",StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory="templates")




@app.api_route('/',methods=['GET'])
async def index(req:Request):
    return templates.TemplateResponse('action.html',{'request':req,'msg':"Welcome to Hospital API UI"})


@app.api_route("/get-info/", methods=['GET','POST'],response_class=HTMLResponse)
async def get_info(req:Request):
    form = await req.form()
    if form:
        providerid = form.get("providerid")
        if data_dict.get(providerid,None):
            return templates.TemplateResponse('get_info.html',{"request":req,"items":data_dict[providerid],"pid":providerid})
        else:
            raise HTTPException(status_code=404,detail="Invalid ProviderID!")
    return templates.TemplateResponse('get_info.html',{"request":req,"items":None,"pid":""})


@app.api_route("/post-info",methods=['GET','POST'],response_class=HTMLResponse)
async def post_into_route(req:Request):
    form = await req.form()
    if form:
        if data_dict.get(form.get("provider"),None):
            raise HTTPException(status_code=300,detail="ProviderID exists!")
        data_dict[form.get("provider")] = {

                                         "name":form.get("name"),
                                         "active":form.get("active"),
                                         "qualification":list(form.get("qualification").split(";")),
                                         "speciality":list(form.get("speciality").split(";")),
                                         "phone":form.get("phone"),
                                         "department":form.get("department"),
                                         "organization":form.get("organization"),
                                         "location":form.get("location"),
                                         "address":form.get("address"),
                                         }
        return templates.TemplateResponse('action.html',{'request':req,'msg':'Information posted!'})
    return templates.TemplateResponse('post_info.html',{"request":req})


@app.api_route('/update',methods=['GET','PUT','POST'],response_class=HTMLResponse)
async def update_item(req:Request):

    form = await req.form()
    if form:
        if not data_dict.get(form.get('provider'),None):
            raise HTTPException(status_code=404,detail="Invalid ProviderID!")
        else:
            data=data_dict[form.get('provider')]

            data['name'] = form.get('name') if form.get('name') is not None else data['name']
            data['active'] = form.get('active') if form.get('active') is not None else data['active']
            data['qualification'] = list(form.get('qualification').split(";")) if form.get('qualification') is not None else data['qualification']
            data['speciality'] = list(form.get('speciality').split(";")) if form.get('speciality') is not None else data['qualification']
            data['phone'] = form.get('phone') if form.get('phone') is not None else data['phone']
            data['department'] = form.get('department') if form.get('department') is not None else data['department']
            data['organization'] = form.get('organization') if form.get('organization') is not None else data['organization']
            data['location'] = form.get('location') if form.get('location') is not None else data['location']
            data['address'] = form.get('address') if form.get('address') is not None else data['address']

            return templates.TemplateResponse('action.html',{'request':req,'msg':'Information Update!'})

    
    return templates.TemplateResponse('update.html',{'request':req})
    

@app.api_route('/delete',methods=['GET','DELETE','POST'],response_class=HTMLResponse)
async def delete_item(req:Request):
    form = await req.form()
    if form:
        providerID = form.get('provider')
        if not data_dict.get(providerID,None):
            raise HTTPException(404,detail="Invalid Provider ID!")
        else:
            data=data_dict[providerID]
            del data_dict[providerID]
            return templates.TemplateResponse('action.html',{'request':req,'msg':'Information Deleted!'})
    return templates.TemplateResponse('delete.html',{'request':req})

@app.api_route('/serialize',methods=['GET'])
async def serialize(req:Request):
    if not data_dict:
        raise HTTPException(305,"No data available to serialize!")
    print(data_dict)
    data = jsonable_encoder(data_dict)
    file =  open("serialize.txt",'ab')
    ret = await pickle.dump(data,file)
    
    return (200,{"data":data,"msg":"Data has been serialized!"})



