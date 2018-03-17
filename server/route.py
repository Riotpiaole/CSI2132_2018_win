from flask import Flask
import os 

template_dir = os.path.abspath( "../template/" )

app = Flask( "Server" , template_folder = template_dir )

from flask import render_template

# Adding routes over here 

@app.route( "/" )
@app.route( "/main" )
def main():
    user = {'username': 'Miguel'}
    return render_template( 'index.html' 
        , user=user )

    