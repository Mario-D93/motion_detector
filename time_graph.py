from main import data_frame
from bokeh.plotting import  show, output_file, figure

plot=figure(x_axis_type='datetime', height=300, width=1000, title='Motion_Detector Graph')

plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "navy"

plot.yaxis.minor_tick_line_color=None
plot.ygrid[0].ticker.desired_num_ticks=1

quad=plot.quad(bottom=0, top=1, left=data_frame["Start"], right=data_frame["End"], color="grey")

output_file("motion_graph.html")
show(plot)