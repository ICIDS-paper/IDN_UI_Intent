
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)
from bokeh.embed import components
from bokeh.transform import transform
import networkx as nx
import uuid
from datetime import datetime
from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool, ResetTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool, Scatter,
                          CustomJS, ColumnDataSource, BoxZoomTool, Div, Select,OpenURL, LabelSet, CustomJSTransform)
from bokeh.plotting import from_networkx
from bokeh.plotting import figure, show, save, output_file

from database import mysql

bp = Blueprint('meaning', __name__, url_prefix='/meaning')


# Route to th main page with the network graph
@bp.route('/narrative_design', methods=('GET', 'POST'))
def narrative_design():

    # Create a Bokeh plot (network graph example)
    plot = create_network_graph()

    # Embed the Bokeh plot into the HTML template
    script, div = components(plot)

    return render_template("meaning/narrative_design.html", script=script, div=div, title="Narrative Design")


@bp.route("/retrieve_data_from_mysql", methods=["GET"])
def retrieve_data_from_mysql():
    if request.method == "GET":
        print('I am in ajax')
        # Perform MySQL queries to extract necessary data
        # Replace these queries with your actual database querying logic
        cursor = mysql.get_db().cursor()
        cursor.execute("select modality from ideation_media")
        modality_data = cursor.fetchone()[0]
        cursor.execute("select tool_text from ideation_media")
        tool_text_data = cursor.fetchone()[0]
        cursor.execute("select tool_visual from ideation_media")
        tool_visual_data = cursor.fetchone()[0]
        cursor.execute("select tools from ideation_general_settings")
        external_tools = cursor.fetchone()[0]

        # Create a dictionary to store the retrieved data
        data = {
            'modality': modality_data,
            'tool_text': tool_text_data,
            'tool_visual': tool_visual_data,
            'external_tools': external_tools
        }
        print('data from ajax is: ')
        print(data)
        cursor.close()
        return jsonify(data)


def create_network_graph():

    # Prepare Data
    #G = nx.gnr_graph(5, 0.4)
    #G = nx.complete_graph(6)
    G = nx.Graph()
    # Retrieve data from ideation_content_structure_elements table
    cursor = mysql.get_db().cursor()
    # for now run the script to truncate and repopulate manually
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT element_id, element_type, element_name, element_desc FROM meaning_making_content_structure_elements")
    elements = cursor.fetchall()

    # Populate nodes in the graph based on the retrieved data
    for element_id, element_type, element_name, element_desc in elements:
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
        G.add_node(element_id, marker=marker, index=element_id, type=element_type, name=element_name, desc=element_desc)
    # Retrieve data from ideation_content_structure_element_relationships table
    cursor.execute("SELECT element_id, related_element_id FROM meaning_making_content_structure_element_relationships")
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

    #
    weight_labels = nx.get_edge_attributes(G, 'weight')
    # Render the plot
    #spring_layout is also possible
    graph_renderer = from_networkx(G, nx.circular_layout, scale=0.95, center=(0, 0))

    graph_renderer.node_renderer.glyph = Scatter(marker="marker", size=40, fill_color="#003C43")
    graph_renderer.node_renderer.selection_glyph = Scatter(marker="marker", size=40, fill_color="#E3FEF7")

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#003C43", line_alpha=1, line_width=1)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color="#E3FEF7", line_width=1)
    #graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color="#135D66", line_width=1)

    #graph_renderer.selection_policy = NodesAndLinkedEdges()
    #graph_renderer.inspection_policy = EdgesAndLinkedNodes()
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
    node_data = dict(x=source.data['x'], y=source.data['y'], index=source.data['index'],
                     name=source.data['name'], type=source.data['type'], desc=source.data['desc'])

    print("node_data is ")
    print(node_data)
    node_source = ColumnDataSource(data=node_data)
    callback = CustomJS(args=dict(source=node_source), code="""
    // Get the index of the tapped node
    var index = cb_data.source.selected.indices[0];
    console.log("Node tapped:", index);
    
    //Access the data from the source
    var data = source.data;
    console.log('data is: ')
    console.log(data);
    var node_name=data.name[index];
    var node_type = data.type[index];  
    var node_desc = data.desc[index]; 
    // Set data attributes of the modal elements
    //document.getElementById('nodeModalLabel').innerText = node_data[node_type] + ' ' + node_data['node_name'];
    document.getElementById('node_name_modal').innerText = node_type + ': ' + node_name;
    document.getElementById('node_desc_modal').value= node_desc;
    // Show Bootstrap modal
    $('#nodeModal').modal('show');
    
    // Bind event handler for shown.bs.modal event after the modal is shown
    $('#nodeModal').on('shown.bs.modal', function() {
        console.log('Modal is shown');
        var element = document.getElementById("node_name_modal");
        
        // Only show data for hardcoded element - location
        var value = "Location: Bedroom"; // Specific value to check against
        var myDiv = document.getElementById("div-location");
        if (element.innerHTML.trim() === value) {
            myDiv.style.display = "block";} 
            else {
            myDiv.style.display = "none";}
        
        // Only show data for hardcoded element - char
        var value = "Character: The Office Manager"; // Specific value to check against
        var myDiv = document.getElementById("div-char");
        if (element.innerHTML.trim() === value) {
            myDiv.style.display = "block";} 
            else {
            myDiv.style.display = "none";}
        
        //Only show data for hardcoded element - event
        var value = "Event: Neglect"; // Specific value to check against
        var myDiv = document.getElementById("div-event");
        if (element.innerHTML.trim() === value) {
            myDiv.style.display = "block";} 
            else {
            myDiv.style.display = "none";}
        
        
        //  Adaptable interface         
         $.ajax({       
         url: '/meaning/retrieve_data_from_mysql', // Flask route to retrieve data
         type: 'GET',
        success: function(data){
            console.log(data);
            
            // Update button text based on data
            $('.import_text').text("Import Text Component (" + data.tool_text + ")");
            $('.import_visual').text("Import Visual Component (" + data.tool_visual + ")");
        
            
            // hide by default
            $('.use_fig_lang').hide();
            $('.use_content_gen').hide();
            $('.use_ind_sup').hide();
            switchInterface(data);
            }});
        
        function switchInterface(data) {
         if (data.modality === '2.text') {
            console.log('text');
            handleTextModality(data);
            } 
        else if (data.modality === '3.text+visual') {
            console.log('text and visual');
            handleTextVisualModality(data);
            }
        else {
        console.log('other');
        handleOtherModality(data);
            }
        }
        
        
        // Define the handleTextModality function
        function handleTextModality(data) {
            $('#col2').hide();
            $('#col2-char').hide();
            $('#col2-event').hide();
            $('#col3').show(); // Show the specified div
            $('#col3-char').show();
            $('#col3-event').show();
            $('.import_visual').hide(); // Hide the specified button
            handleExternalTools(data);
    }
       function handleTextVisualModality(data) {
            $('#col2').show();
            $('#col2-char').show();
            $('#col2-event').show();
            $('#col3').show(); // Show the specified div
            $('#col3-char').show();
            $('#col3-event').show();
            $('.import_text').show(); // Show the specified button
            $('.import_visual').show();
            handleExternalTools(data);
       }
       
        function handleOtherModality(data) {
            $('#col2').hide();
            $('#col2-char').hide();
            $('#col2-event').hide();
            $('#col3').hide();// Show the specified div
            $('#col3-char').hide();
            $('#col3-event').hide();
            $('.delete_comp').hide();// Show the specified button
            $('.import_text').hide(); 
            $('.import_visual').hide();
            handleExternalTools(data);
       }
   
   function handleExternalTools(data) {
    // Hide all buttons first
    $('.use_fig_lang').hide();
    $('.use_content_gen').hide();
    $('.use_ind_sup').hide();

    // Check which external tools are used and show corresponding buttons
    var tools = data.external_tools.split(',');
    tools.forEach(function(tool) {
        switch (tool) {
            case '1.Figurative':
                console.log('Figurative');
                $('.use_fig_lang').show();
                break;
            case '2.Content':
                console.log('Content');
                $('.use_content_gen').show();
                break;
            case '3.Socio_Cultural':
                console.log('Socio-Cultural');
                $('.use_ind_sup').show();
                break;
        }
    });
}

   
   
        
        
    });
    
""")



    plot.add_tools(TapTool(callback=callback))

    # Save the plot as an HTML file
    output_file(filename="static/bokeh_plot.html", title="Static HTML file")
    save(plot)

    return plot



@bp.route('/element_components_save', methods=['GET', 'POST'])
def element_components_save():
    data = request.args.get("data")
    print('i am in save handler')
    #create a table for element components. Do not populate because it is hardcoded now
    cursor = mysql.get_db().cursor()  # creating variable for connection
    cursor.execute("CREATE TABLE if not exists meaning_making_content_structure_element_components(structure_id varchar(50),"
                   "element_id varchar(50), component_id varchar(50), component_type varchar(50),"
                   "component_tool varchar(50), component_object binary, inserted_ts datetime)")
    mysql.get_db().commit()
    cursor.close()
    return redirect(url_for('meaning.narrative_design'))


