from flask import Blueprint, render_template, url_for, redirect
import pandas as pd
from flask_login import login_required, current_user
from .init_db import get_engine, get_connection
from sqlalchemy import text
from sqlalchemy.sql import select

# create cool graphics and charts with pandas and matplotlib
from pandas import DataFrame
import matplotlib.pyplot as plt

# mpld3 takes matplolib and creates html files
from mpld3 import *

# import species and observation tables
from .models import Species, Observations

# blueprint handles regular routes
dashboards = Blueprint('dashboards', __name__)
connection = get_connection()

# get route for dashboard
@dashboards.route('/dashboard')
def dashboard():
    # call the create table and graph functions
    create_dashboard()
    create_graph()

    # have to be logged in to see the dashboard
    if not current_user.is_authenticated:
        return redirect(url_for('auth.signIn'))

    return render_template('dashboard.html')

# create the dashbaord
def create_dashboard():
    observation = Observations()
    engine = get_engine()

    # select our dashboard view DATE, Name, Comment, Species
    s2 = select(text("o.id,o.date, n.name,o.comment,s.species from observations o, species s, nests n where o.species_id = s.id AND o.nest_id = n.id order by date DESC"))
    conn = engine.connect()
    result = conn.execute(s2)
    conn.close()

    # using pandas to make the query more usable
    df = pd.read_sql_query(s2, connection)
    observation_id = df['id']
    buttons=[]
    flags=[]

    # loop through the observation id and create the flags and buttons
    for x in observation_id:

        # select the current id
        s = select(text("id from observations where id=:n")).params(n=x)
        conn = engine.connect()
        result = conn.execute(s)

        # format the result for use with our chart
        observation_id = str(result.first()[0])
        conn.close()

        # select nest_flags and cow_birds and add together so if either exist we'll know
        s2 = select(text("SUM(cow_present + nest_flagged) from observations where id=:n")).params(n=x)
        conn = engine.connect()
        result = conn.execute(s2)
        flag = int(result.first()[0])
        conn.close()

        # if there is a flag mark it
        if flag > 0:
            flags.append("<i class='fas fa-flag text-danger'></i>")

        # otherwise leave it blank
        else:
            flags.append("")
        buttons.append("<a class='nav-link btn btn-warning mb-1 btn-small text-white' href='{{ url_for('nest_data.editObservation', id="+observation_id+")}}'>Edit</a><a class='nav-link btn btn-danger btn-small text-white' href='{{ url_for('nest_data.deleteObservation', id="+observation_id+") }}'>Delete</a>")

    # create our custom chart with flags and buttons
    df2 = df.drop(columns=['id']).assign(links = buttons).assign(flags=flags)

    # change to html with mpld3
    html = df2.to_html(index=False, escape=False)

    # write html to file
    text_file = open('src/templates/table.html', "w")
    text_file.write(html)
    text_file.close()

# create the graph on the dashboard
def create_graph():
    species = Species()
    engine = get_engine()

    # select everything useful for graph date,num_eggs_live_young, dead_young
    s = select(text("o.id,o.date,o.num_eggs,o.live_young,o.dead_young,s.species FROM observations o, species s WHERE o.species_id = s.id"))
    conn = engine.connect()
    result = conn.execute(s)
    conn.close()

    # read query with panda for easier use
    df = pd.read_sql_query(s, connection)

    # seperate all our columns for use
    observation_id_list = df['id']
    date_list = df['date']
    num_eggs_list = df['num_eggs']
    live_young_list = df['live_young']
    dead_young_list = df['dead_young']
    species_name_list = df['species']

    # setup variables for later use
    total_fledglings = 0
    total_fledglings_data = []
    total_fledglings_list = []

    # for how ever many observations there are
    for x in range(0,len(observation_id_list)):
        # total birds = egg birds + live birds - dead birds
        total_fledglings = num_eggs_list[x] + live_young_list[x] - dead_young_list[x]

        # setup our columns with the correct index
        total_fledglings_data.append(observation_id_list[x])
        total_fledglings_data.append(species_name_list[x])
        total_fledglings_data.append(date_list[x])

        # add our total
        total_fledglings_data.append(total_fledglings)
        total_fledglings_list.append(total_fledglings_data)

        # reset for loop
        total_fledglings_data=[]

    # create new pandas list with new appended data
    df2 = DataFrame(total_fledglings_list,columns=['id', 'species','date', 'total_fledglings'])
    observation_id_list = df2['id']
    date_list = df2['date']

    # how many unique species of birds do we have
    species_name_list = df.species.unique()
    total_fledglings_list = df2['total_fledglings']

    # matlabplots setup
    fig, ax = plt.subplots()

    # for every species of bird
    for x in range(len(species_name_list)):
        # our unique bird
        bird = species_name_list[x]
        # create a line plot for each unique bird
        df3 = df2[df2.species == bird]
        date_list = df3['date']
        total_fledglings_list = df3['total_fledglings']

        #setup our plot
        a = date_list
        b = total_fledglings_list
        # plot our code
        ax.plot(a,b, label=bird)
        ax.set(xlabel='Date', ylabel='total_fledglings',
               title='Total Fledglings over time')

    # setup grid and legend
    ax.grid()
    plt.legend()

    # conect to our text file
    text_file = open('src/templates/graph.html', "w")

    # write html to file
    save_html(fig,text_file, figid='graph')

    text_file.close()
