# Serial Plotter
This is a window application that displays serial data in real time. The application is written in Python with PyQt5 and PySerial.

# Screenshots
![Stem_Light_Background.png](screenshot\Stem_Light_Background.png)
![Plot_Dark_Background.png](screenshot\Plot_Dark_Background.png)

# Installation
The application is written in Python 3.11.0. 
<br>
To installed required packages, simply do:
```
python -m pip install -r requirements.txt
```
# Quick Start
### Filter Configuration
Serial Plotter reads in serial data in real time and extracts meaningful data from it. The "Start String" would be the starting point of the data to be extracted and the "End String" would be the ending point. The delimiter allows user to extract multiple data. 
<br>
<br>
![Filter Config](screenshot\filter_config.png)
In default, the user can simply do
```
printf("$$$%f, %f, %f, %f###\n", data1, data2, data3);
```
and the graph would be shown. 
<br>

### Console Tab
The console tab would display the reads in seral data. 
![Console](screenshot\console_tab.png)

### Graph Config
The graph config allows user to change the representation of the data in real time. <br>
![Graph Config](screenshot\graph_config.png)

