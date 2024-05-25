from datetime import datetime
from bokeh.embed import components
from bokeh.transform import transform
import networkx as nx
import uuid
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool, ResetTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool, Scatter,
                          CustomJS, ColumnDataSource, BoxZoomTool, Div, Select,OpenURL, LabelSet, CustomJSTransform)
from bokeh.plotting import from_networkx
from bokeh.plotting import figure, show, save, output_file


from database import mysql

bp = Blueprint('ideation', __name__, url_prefix='/ideation')


@bp.route('/create_intent_aim', methods=('GET', 'POST'))
def create_intent_aim():
    #https: // www.w3schools.com / howto / howto_js_form_steps.asp
    if request.method == "GET":
        intent_id = request.args.get("intent_id")
    if request.method == "POST":
        # For the test we have 2 intent_id's (one with minimal, one with not...)
        if 'topic' in request.form:
            # recreate all the tables
            topic = request.form['topic']
            title = request.form['title']
            intent_id = uuid.uuid1()
            goal = request.form['goal']
            audience = request.form['audience']
            intent_inserted_dt = datetime.now()
            cursor = mysql.get_db().cursor()
            response = cursor.execute("INSERT INTO ideation_aim(ideation_id, topic, title, goal, audience, inserted_ts) "
                                    "VALUES(%s,%s,%s,%s,%s,%s)", (intent_id, topic, title, goal, audience, intent_inserted_dt))
            mysql.get_db().commit()
            cursor.close()
            return redirect(url_for('ideation.create_intent_media', intent_id=intent_id))
    return render_template("ideation/create_intent_aim.html", title="Aim and Audience")


@bp.route('/create_intent_media', methods=('GET', 'POST'))
def create_intent_media():

    #https: // www.w3schools.com / howto / howto_js_form_steps.asp
    if request.method == "GET":
        intent_id = request.args.get("intent_id")
    if request.method == "POST": # check to see if all data is filled in
        if 'modality' in request.form:
            # prepopulate the database with initial content structure elements for the current ideation_id
            prepopulate_database()
            cursor = mysql.get_db().cursor()
            cursor.execute("select ideation_id from ideation_aim "
                                         "where inserted_ts=(select max(inserted_ts) from ideation_aim); ")
            intent_id = cursor.fetchone()[0]
            modality = request.form['modality']
            tool_text = ""
            tool_visual = ""
            if modality == "2.text":
                tool_text = request.form['tool_text']
            if modality == "3.text+visual":
                tool_text = request.form['tool_text_2']
                tool_visual = request.form['tool_visual']
            media = request.form['media']
            type = ""
            genre = ""
            if media == "3.fiction":
                type = request.form['type']
                if type == "2.short_story":
                    genre = request.form['genre']
            plot_synopsis = request.form['plot_synopsis']
            inserted_ts = datetime.now()


            response = cursor.execute("INSERT INTO ideation_media(ideation_id, modality, tool_text, "
                                      "tool_visual, media, type, genre, plot_synopsis, inserted_ts) "
                                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (intent_id, modality, tool_text, tool_visual,
                                                                           media, type, genre, plot_synopsis, inserted_ts))
            mysql.get_db().commit()
            cursor.close()
            return redirect(url_for('ideation.create_intent_content_structure', intent_id=intent_id))
    return render_template("ideation/create_intent_media.html", title="Media and Genre")


@bp.route('/create_intent_content_structure', methods=('GET', 'POST'))
def create_intent_content_structure():
    # create variable for cursor
    cursor = mysql.get_db().cursor()
    #update the prepopulated elements to the record that is being created
    cursor.execute("select ideation_id from ideation_aim "
                   "where inserted_ts=(select max(inserted_ts) from ideation_aim); ")
    intent_id = cursor.fetchone()[0]
    cursor.execute("update ideation_content_structure_elements set ideation_id= %s; ", intent_id)
    mysql.get_db().commit()
    if request.method == "GET":
        intent_id = request.args.get("intent_id")
    existing_event_id = ''
    if request.method == "POST":
        # fetch form data
        if request.form['action'] == 'submit':
            ideation_id = intent_id
            element_id = uuid.uuid1()
            element_details = request.form
            element_type = element_details['element_type']
            element_name = element_details['element_name']
            element_desc = element_details['element_desc']
            element_inserted_dt = datetime.now()
            element_inserted_dt.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO ideation_content_structure_elements(ideation_id, element_id, "
                                      "element_type, element_name, element_desc, element_inserted_ts) "
                                      "VALUES(%s,%s,%s,%s,%s,%s)",
                                      (ideation_id, element_id, element_type, element_name, element_desc,
                                       element_inserted_dt))
            mysql.get_db().commit()
            cursor.close()
            return redirect(url_for('ideation.create_intent_content_structure'))
        if request.form['action'] == 'submit_2':
            return redirect(url_for('ideation.create_intent_general_settings'))

    cursor.execute("select * from ideation_content_structure_elements")
    content_structure_data = cursor.fetchall()

    column_names = [i[0] for i in cursor.description]


    # reindex the dataframe and get the right information
    #cursor.execute("select * from ideation_content_structure_elements")
    #content_structure = pd.DataFrame(cursor.fetchall())
    #content_structure.reindex(columns=content_structure.columns.tolist() + ['Edit'] + ['Delete'])


    return render_template("ideation/create_intent_content_structure.html", title="Content Structure",
                           content_structure_data=content_structure_data, column_names=column_names)


@bp.route('/content_element_delete', methods=['GET', 'POST'])
def content_element_delete():
    element_id = request.args.get("element_id")
    print(str(element_id))
    cursor = mysql.get_db().cursor()  # creating variable for connection
    cursor.execute("delete from ideation_content_structure_elements where element_id = %s ", element_id)
    # delete relationships
    cursor.execute("delete from ideation_content_structure_element_relationships "
                   "where element_id=%s or related_element_id=%s ", (element_id, element_id))
    print(cursor)
    mysql.get_db().commit()
    cursor.close()
    return redirect(url_for('ideation.create_intent_content_structure'))


@bp.route('/create_intent_general_settings', methods=('GET', 'POST'))
def create_intent_general_settings():
    # create variable for cursor
    cursor = mysql.get_db().cursor()
    cursor.execute("select ideation_id from ideation_aim "
                   "where inserted_ts=(select max(inserted_ts) from ideation_aim); ")
    intent_id = cursor.fetchone()[0]
    if request.method == "POST":
        if 'interaction' in request.form:
            print(request.form)
            intent_interaction = request.form['interaction']
            background_story = ''
            if request.form['background'] == 'Yes':
                background_story = request.form['background-story']
            tools = ",".join(request.form.getlist('tools'))  # Join selected tools into a comma-separated string
            notes = request.form['notes']
            inserted_ts = datetime.now()
            inserted_ts.strftime('%Y-%m-%d %H:%M:%S')

            response = cursor.execute("INSERT INTO ideation_general_settings(ideation_id, intent_interaction, "
                                      "intent_background_story, tools, notes, inserted_ts) "
                                     "VALUES(%s,%s,%s,%s,%s,%s)",
                                      (intent_id, intent_interaction, background_story, tools, notes, inserted_ts))
            mysql.get_db().commit()
            cursor.close()
            return redirect(url_for('ideation.show_intent_structure'))
    return render_template("ideation/create_intent_general_settings.html", title="General Settings")


@bp.route('/show_intent_structure', methods=('GET', 'POST'))
def show_intent_structure():

    # Create a Bokeh plot (network graph example)
    plot = create_network_graph_ideation()

    # Embed the Bokeh plot into the HTML template
    script, div = components(plot)

    #prepare database with meaning-making data
    prepare_database()
    return render_template("ideation/show_intent_structure.html", script=script, div=div, title="Visualize Intent Structure")



def prepopulate_database():
    cursor = mysql.get_db().cursor()
    # for now run the script to truncate and repopulate manually
    cursor = mysql.get_db().cursor()
    cursor.execute("select ideation_id from ideation_aim "
                   "where inserted_ts=(select max(inserted_ts) from ideation_aim); ")
    intent_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO ideation_content_structure_elements "
                   "(ideation_id, element_id, element_type, element_name, element_desc, element_inserted_ts) values"
                   "('1','1','Character','Gregor Samsa',"
                   "'Main character who works as a traveling salesman in order to provide money for his sister and parents.', now()),"
                   "('1','2','Character','The Family','His family', now()),"
                   "('1','5','Location','Bedroom','Main place where things happen',now()),"
                   "('1','8','Event','Transformation','One morning the character realises that he has transformed into a bug',now()),"
                   "('1','10','Event','Neglect','At first others tried to acommodate the transformed protagonist, but then gradually they started neglecting him',now()),"
                   "('1','11','Event','Death','After months of exhaustion and mistreat the death happens to Gregor',now())")

    cursor.execute("INSERT INTO ideation_content_structure_element_relationships(structure_id, relationship_id,"
                   "element_id, related_element_id, inserted_ts) values"
                   "('1','1','8','1',now()),"
                   "('1','1','8','5',now()),"
                   "('1','1','8','10',now()),"
                   "('1','1','10','1',now()),"
                   "('1','1','10','5',now()),"
                   "('1','1','10','2',now()),"
                   "('1','1','10','11',now()),"
                   "('1','1','11','1',now()),"
                   "('1','1','11','5',now())")

    cursor.execute("update ideation_content_structure_elements set ideation_id= %s", intent_id)
    cursor.execute("update ideation_content_structure_element_relationships set structure_id= %s", intent_id)

    mysql.get_db().commit()
    cursor.close()


def create_network_graph_ideation():
    # Prepare Data
    # G = nx.gnr_graph(5, 0.4)
    # G = nx.complete_graph(6)
    G = nx.Graph()
    # Retrieve data from ideation_content_structure_elements table
    cursor = mysql.get_db().cursor()
    # for now run the script to truncate and repopulate manually
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT element_id, element_type, element_name FROM ideation_content_structure_elements")
    elements = cursor.fetchall()
    # Populate nodes in the graph based on the retrieved data
    for element_id, element_type, element_name in elements:
        # Assign marker based on element type
        if element_type == 'Character':
            marker = 'circle'
        elif element_type == 'Location':
            marker = 'triangle'
        elif element_type == 'Event':
            marker = 'square'
        else:
            marker = 'unknown'

        # Add node to the graph with attributes
        G.add_node(element_id, marker=marker, index=element_id, type=element_type, name=element_name)
    # Retrieve data from ideation_content_structure_element_relationships table
    cursor.execute("SELECT element_id, related_element_id FROM ideation_content_structure_element_relationships")
    relationships = cursor.fetchall()

    # Populate edges in the graph based on the retrieved relationships
    for element_id, related_element_id in relationships:
        G.add_edge(element_id, related_element_id)


    # Print nodes and edges
    print("Nodes:", G.nodes(data=True))
    print("Edges:", G.edges())

    for i, j in G.edges():
        G[i][j]['weight'] = 1

    # Show with Bokeh
    cursor.execute("select title from ideation_aim; ")
    title = cursor.fetchone()[0]
    # Close the database connection
    cursor.close()

    plot = Plot(x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1), toolbar_location="below",
                title=title,
                tools=[BoxZoomTool(), ResetTool(), HoverTool()])
    plot.add_tools(HoverTool(tooltips=None), BoxSelectTool())
    plot.toolbar.autohide = True
    plot.sizing_mode = 'stretch_both'
    plot.background_fill_color = "#77B0AA"

    weight_labels = nx.get_edge_attributes(G, 'weight')
    # Render the plot
    # spring_layout is also possible
    graph_renderer = from_networkx(G, nx.circular_layout, scale=0.95, center=(0, 0))

    graph_renderer.node_renderer.glyph = Scatter(marker="marker", size=40, fill_color="#003C43")
    graph_renderer.node_renderer.selection_glyph = Scatter(marker="marker", size=40, fill_color="#E3FEF7")

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#003C43", line_alpha=1, line_width=1)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color="#E3FEF7", line_width=1)
    # graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color="#135D66", line_width=1)

    # graph_renderer.selection_policy = NodesAndLinkedEdges()
    # graph_renderer.inspection_policy = EdgesAndLinkedNodes()
    plot.renderers.append(graph_renderer)

    # Add permanent labels on nodes

    # add the labels to the node renderer data source
    source = graph_renderer.node_renderer.data_source

    # create a transform that can extract the actual x,y positions
    code = """
        var result = new Float64Array(xs.length)
        for (var i = 0; i < xs.length; i++) {
            result[i] = provider.graph_layout[xs[i]][%s]
        }
        return result
    """
    xcoord = CustomJSTransform(v_func=code % "0", args=dict(provider=graph_renderer.layout_provider))
    ycoord = CustomJSTransform(v_func=code % "1", args=dict(provider=graph_renderer.layout_provider))
    # Use the transforms to supply coords to a LabelSet
    labels = LabelSet(x=transform('index', xcoord),
                      y=transform('index', ycoord),
                      text='name', text_font_size="12px",
                      x_offset=0, y_offset=-35,
                      source=source)
    plot.add_layout(labels)

    layout = graph_renderer.layout_provider.graph_layout
    x_coords = [layout[node][0] for node in layout]
    y_coords = [layout[node][1] for node in layout]

    source.data['x'] = [x for x in x_coords]
    source.data['y'] = [x for x in y_coords]
    print("source is ")

    print(source.data)
    # Define JavaScript callback to handle node clicks
    node_indices = list(G.nodes)
    node_data = dict(x=source.data['x'],
                     y=source.data['y'],
                     index=source.data['index'], names=source.data['name'], type=source.data['type'])

    print("node_data is ")
    print(node_data)
    node_source = ColumnDataSource(data=node_data)

    # Save the plot as an HTML file
    output_file(filename="static/bokeh_plot.html", title="Static HTML file")
    save(plot)

    return plot


def prepare_database():
    # copy the current intent structure to meaning making structure

    cursor = mysql.get_db().cursor()
    meaning_making_id = uuid.uuid1()
    cursor.execute("select ideation_id from ideation_aim "
                   "where inserted_ts=(select max(inserted_ts) from ideation_aim); ")
    intent_id = cursor.fetchone()[0]
    inserted_ts = datetime.now()
    inserted_ts.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("CREATE TABLE IF NOT EXISTS ideation_meaning_making (ideation_id varchar(50), "
                   "meaning_making_id varchar(50), inserted_ts datetime) ")
    cursor.execute("INSERT into ideation_meaning_making(ideation_id, meaning_making_id, inserted_ts) "
                   "VALUES (%s,%s,%s)", (intent_id, meaning_making_id, inserted_ts))
    mysql.get_db().commit()

    # copy the elements from ideation, and then add more
    cursor.execute("CREATE TABLE IF NOT EXISTS meaning_making_content_structure_elements as select * from "
                   "ideation_content_structure_elements ")
    cursor.execute("CREATE TABLE IF NOT EXISTS meaning_making_content_structure_element_relationships as select * from "
                   "ideation_content_structure_element_relationships ")

    # update the meaning_making_id where needed
    cursor.execute("select meaning_making_id from ideation_meaning_making "
                   "where inserted_ts=(select max(inserted_ts) from ideation_meaning_making) ")
    meaning_making_id = cursor.fetchone()[0]
    cursor.execute("alter table meaning_making_content_structure_elements rename column ideation_id to meaning_making_id")
    # add what needed
    cursor.execute("INSERT into meaning_making_content_structure_elements(meaning_making_id, element_id, element_type,"
                   "element_name, element_desc, element_inserted_ts) values "
                   "('1','3','Character', 'The Office Manager','His boss', now()), "
                   "('1','4','Character', 'Charwoman','Is an old widowed lady who is employed to take care of the household duties', now())")
    cursor.execute("INSERT into meaning_making_content_structure_elements(meaning_making_id, element_id, element_type,"
                   "element_name, element_desc, element_inserted_ts) values "
                   "('1','6','Location', 'Living room','Living room of the family Samsa', now()),"
                   "('1','7','Location', 'Countryside','Beautiful place outside the city', now())")
    cursor.execute("INSERT into meaning_making_content_structure_elements(meaning_making_id, element_id, element_type,"
                   "element_name, element_desc, element_inserted_ts) values "
                   "('1','9','Event', 'Revelation','Others come to know about what happened to the protagonist.', now()),"
                   "('1','12','Event', 'Relief','Getting rid of the strange creature makes the family reunite and breathe easier.', now())")
    # update relationships that are needed
    cursor.execute("DELETE from meaning_making_content_structure_element_relationships where element_id='8' and related_element_id='10'")

    cursor.execute("INSERT into meaning_making_content_structure_element_relationships(structure_id, relationship_id, "
                   "element_id, related_element_id, inserted_ts) values "
                   "('2','1','8','9',now()),"
                   "('2','1','9','1',now()),"
                   "('2','1','9','2',now()),"
                   "('2','1','9','3',now()),"
                   "('2','1','9','6',now()),"
                   "('2','1','9','10',now()),"
                   "('2','1','10','4',now()),"
                   "('2','1','10','6',now()),"
                   "('2','1','11','4',now()),"
                   "('2','1','11','12',now()),"
                   "('2','1','12','2',now()),"
                   "('2','1','12','6',now()),"
                   "('2','1','12','7',now())")

    cursor.execute("update meaning_making_content_structure_element_relationships set structure_id=%s",meaning_making_id)
    cursor.execute("update meaning_making_content_structure_elements set meaning_making_id= %s", meaning_making_id)
    # delete default stuff from meaning-making considering that some things might have been deleted during ideation
    cursor.execute("DELETE FROM meaning_making_content_structure_element_relationships "
                   "WHERE element_id NOT IN (SELECT element_id FROM meaning_making_content_structure_elements) "
                   "OR related_element_id NOT IN (SELECT element_id FROM meaning_making_content_structure_elements)")

    mysql.get_db().commit()
    cursor.close()