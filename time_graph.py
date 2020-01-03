from main import data_frame
from bokeh.plotting import  show, output_file, figure
from bokeh.models import HoverTool, ColumnDataSource

#converting datetime types of the frame to string
data_frame["Start_str"]=data_frame["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
data_frame["End_str"]=data_frame["End"].dt.strftime("%Y-%m-%d %H:%M:%S")


#converting datas to the ColumnDataSource object to enable bokeh_plotting to acces them
cds=ColumnDataSource(data_frame)

plot=figure(x_axis_type='datetime', height=300, width=1000, title='Motion_Detector Graph')

plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "navy"

plot.yaxis.minor_tick_line_color=None
plot.ygrid[0].ticker.desired_num_ticks=1

quad=plot.quad(bottom=0, top=1, left="Start", right="End", color="grey", source=cds)

hover=HoverTool(tooltips=[("Start","@Start_str"),("End","@End_str")])
plot.add_tools(hover)

output_file("motion_graph.html")
show(plot)