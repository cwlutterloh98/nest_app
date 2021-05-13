# Miami Valley Nesting App

An application I made to redesign the Miami Valley Audobon

## Installation

Clone this repository or download it.
CD to the folder where you cloned the repository.

## Important notes for getting started

Navigate to src/init.db.py
line 6 add connection="your_connection_here"

Navigate to _init_.py 
line 13 add app.config['SECRET_KEY'] = 'your-secret-key'

## Usage

To start
$ flask run app

Then visit _http://localhost:5000/ in your browser.

To close
Ctrl-C to terminate.

## Developer Notes

To use in Developer Mode
set FLASK_APP=app
set FLASK_ENV=development

### SCSS
To use SCSS
sass --watch scss:../static/css

To stop watching
Ctrl-C to terminate

## License
MIT for more information on MIT licensing visit https://opensource.org/licenses/MIT

## Diagram
USERS
-----
User_ID     primary_key     Int()
username    unique          String(100)
password    *hashed*        String(100)

Nests
------
Nests_ID    primary_key     Int()
Name                        String()

Species
-------
Species_ID  primary_key     Int()
Species                     String()

Observations
------------
Observation_ID  primary_key Int()
user_id     foreign_key     Int()
species_id  foreign_key     Int()
date                        DateTime()
comment                     String(500)
num_eggs                    Int()
live_young                  Int()  
dead_young                  Int()
nest_flagged                Tinyint()
cow_present                 Tinyint()