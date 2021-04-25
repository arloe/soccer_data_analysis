### soccer data analysis

### Introduction
In baseball, there are several cases of success by analyzing data by quantifying the player's performance and ability(eg. Sabermetrics). In other words, this study attempts to discover insights using data in soccer as well. A model that predicts the players who will become national teams in the future by position is presented by quantifying their abilities by using the players' game events, and using variable abbreviations and visualizations.

### Data
The data was used for Korean soccer player records from 1986 to 2016. The source of the data is [KFA MATCH](http://www.kfamatch.or.kr/svc/man/selectMainInfo.do), and data was collected through crawling.

### Usage of Crawling data
```bash
python main.py -d ./chrome_driver/chromedriver -o dataset -f data.csv
```
`-d` is the location of the chrome driver, `-o` is the location where the crawled files will be saved. Finally, `-f` specifies the name of the file to be saved. At this time, the file is saved in csv format.

### Analysis

