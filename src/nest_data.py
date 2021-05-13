from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user
from sqlalchemy import text
from sqlalchemy.sql import select
# for converting dates
from datetime import datetime
# pandas for easy use with sql
import pandas as pd

# import our models
from .models import Nests, Species, Observations

from . import db
from .init_db import get_engine, get_connection

# setup global connection as needed
connection = get_connection()

# blueprint handles regular routes
nest_data = Blueprint('nest_data', __name__)

# add observation get route
@nest_data.route('/add-observation')
def addObservation ():
    # if user is not logged in return to sign in screen
    if not current_user.is_authenticated:
        return redirect(url_for('auth.signIn'))

    # setup models
    nests = Nests()
    species = Species()

    #select our nests so they can be used in our options input
    engine = get_engine()
    s = select([nests])
    conn = engine.connect()
    boxes = conn.execute(s)
    conn.close()

    # select our species so they can be used in our options input
    s2 = select([species])
    conn = engine.connect()
    species = conn.execute(s2)
    conn.close()

    # render template with our nests and species and user
    return render_template('add-observation.html', boxes=boxes, species=species, user_id=current_user.id)

# get route for edit observation
@nest_data.route('/edit-observation/<int:id>')
def editObservation(id):
    # if you're not logged in sends to sign in page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.signIn'))

    # setup models
    observations = Observations()
    nests = Nests()
    species = Species()

    # select our nests for our selection options
    engine = get_engine()
    s = select([nests])
    conn = engine.connect()
    boxes = conn.execute(s)
    conn.close()

    # select our species for our selection options
    s2 = select([species])
    conn = engine.connect()
    species = conn.execute(s2)
    conn.close()

    # query to select everything we need to populate our fields by the current id
    s3 = select(text("o.id, o.nest_id, o.species_id,o.date,o.comment,o.num_eggs,o.live_young,o.dead_young,o.nest_flagged,o.cow_present from observations o where o.id=:x")).params(x=id)
    conn = engine.connect()
    result = conn.execute(s2)
    df = pd.read_sql_query(s3, connection)

    # setup our panda data
    nest = df['nest_id']
    date = df['date']
    species_id = df['species_id']
    comment = df['comment']
    num_eggs = df['num_eggs']
    live_young = df['live_young']
    dead_young = df['dead_young']
    nest_flagged = df['nest_flagged']
    cow_present = df['cow_present']
    conn.close()

    # transform our data for use in our html
    nest = nest.to_string(index=False)
    nest = int(nest)
    species_id = species_id.to_string(index=False)
    species_id = int(species_id)
    date = date.to_string(index=False)
    date = pd.to_datetime(date,format="%Y-%m-%d")
    str_date = datetime.strftime(date, '%m/%d/%Y')
    num_eggs = num_eggs.to_string(index=False)
    live_young = live_young.to_string(index=False)
    dead_young = dead_young.to_string(index=False)
    comment = comment.to_string(index=False)
    nest_flagged = nest_flagged.to_string(index=False)
    cow_present = cow_present.to_string(index=False)
    nest_flagged= int(nest_flagged)
    cow_present=int(cow_present)

    # render our template with all fields filled out from what we used
    return render_template('edit-observation.html',id=id,nest=nest,date=str_date,species_name=species_id,comment=comment,num_eggs=num_eggs,live_young=live_young,dead_young=dead_young,nest_flagged=nest_flagged,cow_present=cow_present, boxes=boxes, species=species, user_id=current_user.id)

# delete get route for deleting an observation
@nest_data.route('/delete-observation/<int:id>')
def deleteObservation(id):

    # if your not logged in reutrn to the sign in page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.signIn'))
    engine = get_engine()
    observations = Observations()

    # delete the observation based on id
    result = (
        text("DELETE FROM observations where id=:n").params(n=id)
    )
    # connect to database
    conn = engine.connect()
    conn.execute(result)
    conn.close()

    # redirect back to dashboard
    return redirect(url_for('dashboards.dashboard'))


# add observation post
@nest_data.route('/add-observation', methods=['POST'])
def observation_post():
    # if you're not logged in go to sign in
    if not current_user.is_authenticated:
        return redirect(url_for('auth.signIn'))
    # setup our engine and models
    engine = get_engine()
    nests = Nests()
    species_tb = Species()
    observations = Observations()

    # get all rqeuest items
    user_id = request.form['user_id']
    nest_id = request.form['bird-box']
    date = request.form['date']
    species = request.form['species']

    # species is special because if they choose an other we need to know and add it to our database
    if species == 'other':
        # get other species request data
        species = request.form['other-species']

        # insert new into table
        ins = species_tb.insert().values(
            species=species
        )
        conn = engine.connect()
        result = conn.execute(ins)
        conn.close()

        # select the specific species id we just created so we can save it in the observation
        s = select(text("id from species where species=:n")).params(n=species)

        # connect and execute query and close
        conn = engine.connect()
        species = conn.execute(s)
        species = str(species.first()[0])
        conn.close()

    # more request forms
    eggs_present = request.form['eggs_present']
    live_young = request.form['live_young']
    dead_young = request.form['dead_young']
    comments = request.form['comments']

    # checkboxes are special
    cow_present = request.form.get('cow_present')
    nest_flagged = request.form.get('nest_flagged')

    # insert into observations the new observation data
    ins = observations.insert().values(
        user_id=user_id,
        nest_id=nest_id,
        date=datetime.strptime(date,'%m/%d/%Y'),
        species_id=species,
        num_eggs=int(eggs_present),
        live_young=int(live_young),
        dead_young=int(dead_young),
        comment=comments,
        cow_present=bool(cow_present),
        nest_flagged=bool(nest_flagged)
    )

    # connect to database and execute then close
    conn = engine.connect()
    result = conn.execute(ins)
    conn.close()

    # redirec tto the dashboard
    return redirect(url_for('dashboards.dashboard'))

# Post edit a specific observation
@nest_data.route('/edit-observation/<int:id>', methods=['POST'])
def edit_observation_post(id):

    # if you're not logged in log out
    if not current_user.is_authenticated:
        return redirect(url_for('auth.signIn'))

    # create models and engine
    engine = get_engine()
    nests = Nests()
    species_tb = Species()
    observations = Observations()

    # get all form requests
    user_id = request.form['user_id']
    nest_id = request.form['bird-box']
    date = request.form['date']
    species = request.form['species']

    # if species is other we need to add it to our species table
    if species == 'other':
        species = request.form['other-species']

        # insert other species into database
        ins = species_tb.insert().values(
            species=species
        )

        # connect to database and execute query
        conn = engine.connect()
        result = conn.execute(ins)
        conn.close()

        # select the id we will need it for the observeration
        s = select(text("id from species where species=:n")).params(n=species)

        # connect to database
        conn = engine.connect()
        species = conn.execute(s)
        species = str(species.first()[0])
        conn.close()

    # more database fields
    eggs_present = request.form['eggs_present']
    live_young = request.form['live_young']
    dead_young = request.form['dead_young']
    comments = request.form['comments']

    # checkboxes are special
    cow_present = request.form.get('cow_present')
    nest_flagged = request.form.get('nest_flagged')

    # datetime needs updated to work with the database
    datetime.strptime(date,'%m/%d/%Y')

    # update the observation based on it's observation.id
    update = text("UPDATE observations SET user_id = :user_id, nest_id = :nest_id, species_id = :species_id, num_eggs = :num_eggs, live_young = :live_young, dead_young = :dead_young, nest_flagged = :nest_flagged, cow_present = :cow_present, date = :date WHERE (id = :id)")
    conn = engine.connect()

    # execute update and replace the variables inside the query
    conn.execute(update,
            user_id=int(user_id),
            id=id,
            nest_id=int(nest_id),
            date=datetime.strptime(date,'%m/%d/%Y'),
            species_id=int(species),
            num_eggs=int(eggs_present),
            live_young=int(live_young),
            dead_young=int(dead_young),
            comment=comments,
            cow_present=bool(cow_present),
            nest_flagged=bool(nest_flagged)
     )
    conn.close()

    return redirect(url_for('dashboards.dashboard'))