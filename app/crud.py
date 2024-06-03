import json
import re

from sqlmodel import Session

from database import engine
from models import AttractionBase as Attraction, Image

def add_attraction(name,category,description,address,transport,mrt,lat,lng,images):
    with Session(engine) as session:
        new_attraction = Attraction(
            name=name,
            category=category,
            description=description,
            address=address,
            transport=transport,
            mrt=mrt if mrt else 'mrt-not-exist',
            lat=lat,
            lng=lng,
        )
        try:
            session.add(new_attraction)
            session.flush() 
            if True in (img is None for img in images):
                print(images)
                raise Exception("Image URL cannot be null")
            session.add_all((
                Image(url=img, attraction_id=new_attraction.id) 
                for img in images
            ))
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise e
       

def add_attraction_from_json(json_file):
    with open(json_file,'r') as file:
        data = json.load(file)
        attractions_data = data['result']['results']
        for _,attraction_data in enumerate(attractions_data):
            pattern = r'https:\/\/[^"]+?\.(?:jpg|JPG|png|PNG)'
            images = re.findall(pattern, attraction_data['file'])
            add_attraction(
                attraction_data['name'],
                attraction_data['CAT'],
                attraction_data['description'],
                attraction_data['address'],
                attraction_data['direction'],
                attraction_data['MRT'],
                attraction_data['latitude'],
                attraction_data['longitude'],
                images
            )



