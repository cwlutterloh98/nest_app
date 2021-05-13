from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, text, select
from datetime import datetime

# hard coded connection!
def get_connection():
    connection = 'mysql+pymysql://root:root@127.0.0.1/nest_app'
    return connection

# engine is the starting point for SQLalchemy requires connection
def get_engine():
    connection = get_connection()
    engine = create_engine(connection, echo=True)
    return engine

# metadatadata is a collection of different features
def setup_db():
    meta = MetaData()
    return meta

# quick way to create your tables for data except users
def create_table():
    from .models import Nests, Species, Users_Setup, Observations
    meta = setup_db()
    nests = Nests()
    species = Species()
    users_setup = Users_Setup()
    observation = Observations()
    engine = get_engine()
    meta.create_all(engine)
    #insert_default()

# quick way to insert data into all tables
def insert_default():
    # import models of tables
    from .models import Nests, Species,Observations
    nests = Nests()
    species = Species()
    observations = Observations()

    # start engine
    engine = get_engine()

    # species lists
    def_species = ['Eastern Blue Bird',
                   'Tree Swallow',
                   'House Wren',
                   'Brown-Headed Cowbird',
                   'Unknown']

    # for every species insert it into the species table
    for num in def_species:
        ins = species.insert().values(
            species=num
        )

        # connect to database and execute and close
        conn = engine.connect()
        result = conn.execute(ins)
        conn.close()

    # for every bird nes insert it into the nests table
    def_nests = ['Bird House 1',
                 'Bird House 2',
                 'Bird House 3',
                 'Bird House 4',
                 'Bird House 5',
                 'Bird House 6',
                 'Bird House 7',
                 'Bird House 8',
                 'Bird House 9',
                 'Bird House 10',
                 'Bird House 11',
                 'Bird House 12',
                 'Bird House 13']

    # for every bird nest insert it into the nests table
    for num in def_nests:
        ins = nests.insert().values(
            name=num
        )
        conn = engine.connect()
        result = conn.execute(ins)
        conn.close()

    # set defaults for non specified data
    def_user_id = [1,1,1,1,1,1,1,1,1,1,1,1]
    def_nest_id = [1,1,1,1,1,1,1,1,1,1,1,1]

    # date lists got from client
    def_date = ['01/01/2017',
                '01/01/2017',
                '01/01/2017',
                '01/01/2018',
                '01/01/2018',
                '01/01/2018',
                '01/01/2019',
                '01/01/2019',
                '01/01/2019',
                '01/01/2020',
                '01/01/2020',
                '01/01/2020']

    # species 1 is Eastern Blue  2 is tree swallow 3 house wren 4 cow bird
    def_species_id = [1,2,3,1,2,3,1,2,3,1,2,3]

    # choose live_young since other stats weren't kept
    def_num_eggs = [0,0,0,0,0,0,0,0,0,0,0,0]
    def_live_young = [91,41,125,49,121,76,88,94,51,58,99,60]
    def_dead_young = [0,0,0,0,0,0,0,0,0,0,0,0]

    # initial load because it's previous data
    def_comment = ["initial load",
                   "initial load",
                   "initial load",
                   "initial load",
                   "initial load",
                   "initial load",
                   "initial load",
                   "initial load",
                   "initial load",
                   "initial load",
                   "initial load",
                   "initial load",]

    # cow and nest flag are binary 0 or 1
    def_cow_present = [0,0,0,0,0,0,0,0,0,0,0,0]
    def_nest_flagged = [0,0,0,0,0,0,0,0,0,0,0,0]

    # insert into the observation table
    x = range(12)
    for n in x:
        ins = observations.insert().values(
            user_id=def_user_id[n],
            nest_id=def_nest_id[n],
            species_id=def_species_id[n],
            date=datetime.strptime(def_date[n],'%m/%d/%Y'),
            comment=def_comment[n],
            num_eggs=def_num_eggs[n],
            live_young=def_live_young[n],
            dead_young=def_dead_young[n],
            nest_flagged=def_nest_flagged[n],
            cow_present=def_cow_present[n]
        )
        # connect and execute and close database
        conn = engine.connect()
        result = conn.execute(ins)
        conn.close()

