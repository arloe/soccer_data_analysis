### Korean Society of Science and Football
visualization of soccer players' abilities and predict future national player

### Introduction
In baseball, there are several cases of success by analyzing data by quantifying the player's performance and ability(eg. Sabermetrics). In other words, this study attempts to discover insights using data in soccer as well. A model that predicts the players who will become national teams in the future by position is presented by quantifying their abilities by using the players' game events, and using variable abbreviations and visualizations.

### Data
The data was used for Korean soccer player records from 1986 to 2016. The source of the data is [KFA MATCH](http://www.kfamatch.or.kr/svc/man/selectMainInfo.do), and data was collected through crawling.

### Usage of Crawling data
```bash
python main.py -d ./chrome_driver/chromedriver -o dataset -f data.csv
```
`-d` is the location of the chrome driver, `-o` is the location where the crawled files will be saved. Finally, `-f` specifies the name of the file to be saved. At this time, the file is saved in csv format.

### The result of analysis

1. Quantifying and visualizing players' abilities

![visualization](https://github.com/arloe/soccer_data_analysis/blob/main/img/visualization.PNG)

2. A model for predicting the possibility of future national team advancement of youth soccer players

![prediction_model](https://github.com/arloe/soccer_data_analysis/blob/main/img/prediction_model.PNG)

### Conclusion
The Football Science Society is a newly established society with the goal of integrating data or data analysis into the field of soccer. Therefore, at first, rather than approaching with a complex methodology, a method that can be interpreted or a visualization with good readability is a good method. So, in this poster, an analysis that can induce people's interest was conducted.