## Matplotlib - https://www.matplotlib-journey.com/module1/matplotlib-pattern
## 1. Matplotlib: The Most Popular Option
## 2.Endless customization
## 3.Matplotlib: Supercharged
#### 1. maps - Geopandas,cartopy,prettymaps,ridge_maps
#### 2. Specialtypes - networkx,pywaffle,wordcloud,squarify
#### 3. Annotations - Highlight_text,pyfonts,draw_arrow
#### 4 . stats/ML - seaborn, scikit learn

from pyfonts import load_google_font

import matplotlib.pyplot as plt

# fig as the overall canvas where everything is drawn,
# ax as the area or section within that canvas where the actual graph or plot appears.

## Line chart
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [2, 3, 1, 4, 5])
plt.show()

fig, ax = plt.subplots()
ax.scatter([1, 2, 3, 4, 5], [2, 3, 1, 4, 5], color="red")
plt.show()

### pyplot vs axes ---
###  Pyplot interface often requires "hacks"
### the Axes interface is much more consistent and eliminates the need for such workarounds.


### Figure and Axes
###
# The Axes is where the actual data visualization happens—it contains the plot elements such as lines, bars,
# scatter points, and more.
# Every plot lives inside an Axes, and each figure can contain multiple Axes to organize different visualizations.

# A Figure is the top-level container for everything in a Matplotlib chart. Think of it as the canvas where all
# elements are drawn, including one or more Axes.
# It also holds additional components such as titles, legends, or global labels that are not tied to a specific Axes.


fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [2, 3, 1, 4, 5], color="red")
fig.text(
    0.5, 0.5, "Hello"
)  # We can use fig to add text to plot. Since figure center at 0.5 , 0.5
plt.show()

# TO do it with Axes
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [2, 3, 1, 4, 5], color="red")
ax.text(
    3, 3, "Hello"
)  # We can use fig to add text to plot. Since figure center at 0.5 , 0.5
plt.show()


# Type of charts and category :  https://www.data-to-viz.com

# Correlation: Scatterplot, Heatmap, Correlogran,Bubble,2D Density, Connected Scatter
# Distributiob: Density, Violin, Histogram,boxplot, Ridgeline
# Ranking : Barplot, Wordcloud, Parallel,lollipop, Circular barplot, Radar
# Part of a whole: Piechart, Donut, Treemap, Dendrogram,Voronai,Circular Packing
# Evolution: Line chart, Area chart, stacked chart, Streamgraph,
# Maps : MAps, Hexon chart , bubble chart, choropleth,Connection
# Flow : Chord Diagram, Networkk,Sankey , Arc Diagram ,Edge Bungling

# Chart examples


y = ["France", "Spain", "Canada", "UK", "Australia"]
values = [2, 5, 3, 4, 5]

fig, ax = plt.subplots()
ax.barh(y, values)
plt.show()
