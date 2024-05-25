import logging
from flask import Flask, render_template, url_for
import ideation, meaning, validation
from database import mysql

app = Flask(__name__)
# initialize database
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'thesis_db'


mysql.init_app(app)  # Initialise with the new app


@app.context_processor
def inject_dict_for_all_templates():
    # build the navbar and pass it for every route
    # https://copyprogramming.com/howto/flask-nav-navigation-alternative-for-python-3-10#flask-nav-navigation-alternative-for-python-310
    nav = [
        {
            "text": "Ideation",
            "sublinks": [
                {"text": "Aim and Audience", "url": url_for('ideation.create_intent_aim')},
                {"text": "Media and Genre", "url": url_for('ideation.create_intent_media')},
                {"text": "Content Structure", "url": url_for('ideation.create_intent_content_structure')},
                {"text": "General Settings", "url": url_for('ideation.create_intent_general_settings')},
                {"text": "Visualize Intent Structure", "url": url_for('ideation.show_intent_structure')},

            ],
        },
        {
            "text": "Meaning Making",
            "sublinks": [
                {"text": "Narrative Design", "url": url_for('meaning.narrative_design')}
            ],
        },
        {
            "text": "Validation",
            "sublinks": [
                {"text": "Test the Narrative", "url": url_for('validation.test_the_narrative')},
            ],
        }
    ]
    return dict(navbar=nav)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    try:
        prepare_tables()
        return render_template("homepage.html", title="Home Page")
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


app.register_blueprint(ideation.bp)
app.register_blueprint(meaning.bp)
app.register_blueprint(validation.bp)


if __name__ == '__main__':
    app.run(debug=True)


def prepare_tables():
    cursor = mysql.get_db().cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS thesis_db")
    cursor.execute("use thesis_db")
    cursor.execute("DROP TABLE IF EXISTS ideation_content_structure_element_relationships")
    cursor.execute("DROP TABLE IF EXISTS ideation_content_structure_elements")
    cursor.execute("DROP TABLE IF EXISTS ideation_aim")
    cursor.execute("DROP TABLE IF EXISTS ideation_media")
    cursor.execute("DROP TABLE IF EXISTS ideation_general_settings")

    cursor.execute("DROP TABLE IF EXISTS ideation_meaning_making")
    cursor.execute("DROP TABLE IF EXISTS meaning_making_content_structure_elements")
    cursor.execute("DROP TABLE IF EXISTS meaning_making_content_structure_element_relationships")
    cursor.execute("DROP TABLE IF EXISTS meaning_making_content_structure_element_components")

    cursor.execute("CREATE TABLE ideation_content_structure_elements (ideation_id varchar (50),"
                   "element_id varchar(50),element_type varchar(50),element_name varchar(50),"
                   "element_desc varchar(500), element_inserted_ts datetime)")

    cursor.execute("CREATE TABLE ideation_content_structure_element_relationships (structure_id varchar(50),"
                   "relationship_id varchar(50), element_id varchar(50), related_element_id varchar(50),"
                   "inserted_ts datetime)")

    cursor.execute("CREATE TABLE ideation_aim (ideation_id varchar(50), topic varchar(50), title varchar(50),"
                   "goal varchar(50), audience varchar(500),inserted_ts datetime)")

    cursor.execute("CREATE TABLE ideation_media (ideation_id varchar(50),modality varchar(50),tool_text varchar(50),"
                   "tool_visual varchar(50),media varchar(50),type varchar(50),genre varchar(50),"
                   "plot_synopsis varchar(500),inserted_ts datetime)")

    cursor.execute("CREATE TABLE ideation_general_settings(ideation_id varchar(50),intent_interaction varchar(50),"
                   "intent_background_story varchar(1000),tools varchar(50),notes varchar (500),"
                   "inserted_ts datetime)")

    mysql.get_db().commit()
    cursor.close()

