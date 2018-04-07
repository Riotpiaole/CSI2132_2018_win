import requests  as req 

args ={ 
        'name':'Rock"s restaurant',
        'address': "HuntClub Rd",
        'city':'Ottawa',
        'post_code': 'K1N 7S3',
        'phone_number':3437773548}
name='Stephen Szabo Salon'

r = req.get("http://localhost:5000/restaurant/")

print ( r.json() )