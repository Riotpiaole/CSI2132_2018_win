import requests  as req 

args ={ 
        'name':'Rock"s restaurant',
        'address': "HuntClub Rd",
        'city':'Ottawa',
        'post_code': 'K1N 7S3',
        'phone_number':3437773548}
name='Stephen Szabo Salon'

r = req.post("http://localhost:5050/restaurants/Rock's restaurant", 
            params=args)
