# COVID dashboard

### Project aim
- Build simple dashboard to monitor trends in actual covid cases and rates by country
- Provide dynmaic projections to visualise dynamics over 2020 using simple modelling approaches
- Note that this analysis is for illustrative purposes only - I have no expertise in epidemic modelling


### Modelling approach
1) Simple SIR modelling approach to forecast from reported figures on 01/03/20 with dynamic input to vary beta and max population affected
2) Panel regression on confirmed cases with country dummies and policy change dates


### Data sources
- John Hopkins dashboard daily feeds for confirmed cases, deaths and recoveries
- Data on hopistal beds sourced from WHO
- Policy response captured via "Stringency Index" produced by Oxford School of Government


#### Dashboard
- Built on flask using dash library to cover 50 countries with most confirmed cases


![](images/dashboard_visual.png)