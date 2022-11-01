## **I. Data**

**Research**

- Most Data (nav/dividend/split ratio/asset allocation) : `CSMAR`
- Fund classification : `JoinQuant`
- Fund start date: `JoinQuant`

**Validation**

- `AMAC` : [2020 yearly report, page 15](https://www.amac.org.cn/researchstatistics/publication/zgzqtzjjynb/202104/t20210419_11390.html), for market statistic
- `Win.d` : classification/share/nav, for market statistic; stock fund adjusted net asset value (2005/6-2019/6)

**Data is sound, carefully verified and available to fetch**

## **II. Market Statistic**

### 2022-10, proportion of funds

![proportion](image/README/proportion.png)

### statistic at the end of June

![market-statistic](image/README/market-statistic.png)

## **III. Market Return**

### return formula definition

$$
R_t^{real}=\frac{\left(NAV_t+Div_t\right)*s_t}{NAV_{t-1}}\tag{2}
$$

$NAV_t$ denotes net asset value of month t

$Div_t$ denotes dividend payout in month t

$s_t$ denotes split ratio in month t

### cumulative return

![market-value-weighted-fund-portfolio](image/README/market-value-weighted-fund-portfolio.png)

### return description

Volatility

![funds_volatility_description](image/README/funds_volatility_description.png)

Return

![funds_mean_return_description](image/README/funds_mean_return_description.png)

### regress with market

| 2005/6-2022/9       | α    | t     | p     | annual α |
| ------------------- | ----- | ----- | ----- | --------- |
| stock_naïve        | 1.09% | 2.328 | 0.021 | 13.91%    |
| blend_naïve        | 1.08% | 2.93  | 0.004 | 13.71%    |
| stock_naïve_excess | 0.90% | 1.921 | 0.056 | 11.36%    |
| blend_naïve_excess | 0.89% | 2.41  | 0.017 | 11.17%    |

| 2005/6-2022/9 | α             | mktrf          | smb             | vmg             | r^2      | annual α |
| ------------- | -------------- | -------------- | --------------- | --------------- | -------- | --------- |
| stock_capm    | 0.154% (1.052) | 0.826 (44.307) |                 |                 | 0.905032 | 0.0186    |
| blend_capm    | 0.325% (2.128) | 0.62 (31.82)   |                 |                 | 0.830937 | 0.0397    |
| stock_svc     | 0.323% (2.165) | 0.838 (46.938) | -0.179 (-5.55)  | -0.024 (-0.569) | 0.919562 | 0.0395    |
| blend_svc     | 0.67% (4.294)  | 0.592 (31.72)  | -0.063 (-1.867) | -0.263 (-5.967) | 0.856929 | 0.0835    |

## **III. Overall Performance**

## **Note**

### weakness: fund split day

condition 1: we do not have `Win.d` adjusted NAV

condition 2: adjusted NAV needs fund split ratio to calculate

condition 3: fund split ratio is exclusively available in `CSMAR`

condition 4: fund split ratio in `CSMAR` is sometimes one month ahead or lag than real split month

check `fund split day.xlsx` for more detailed discuss

solution 1: buy `Win.d` data

solution 2: manually check all split day and correct the data

### weakness: actively managed fund

`JoinQuant` does not provide `active or not` signal

here we did not strictly follow the paper

### more about formula

if a fund payed dividend multiple times in one month, $Div_t=Div_{t,1}+Div_{t,2}+...$

if a fund was split multiple times in one month, $s_t=s_{t,1}×s_{t,2}×...$

## **Appendix**

### errata: report standard

*problem*: annual report or semi-annual report not available before 2008

*reason*: regulation rule changed

*solve*: use second quarter report if annual of semi-annual report not available

![annual-or-semi-report-proportion](image/README/annual-or-semi-report-proportion.png)

<img src="image/README/2008_search.png" alt="drawing" width="400"/> <img src="image/README/2009_search.png" alt="drawing" width="405"/>

[中国证券监督管理委员会公告〔2008〕第4号](http://www.gov.cn/zwgk/2008-02/21/content_896020.htm)

### errata: share data quality

*problem*: 2004 share data lacks

*reason*: data source insufficient

*solve*: use 2005-6 and later data

![full-market-non-NA-count](image/README/full-market-non-NA-count.png)

### verification: market value statistic

![sum-of-all-mixed-fund-market-value](image/README/sum-of-all-mixed-fund-market-value.png)

![sum-of-all-stock-fund-market-value](image/README/sum-of-all-stock-fund-market-value.png)

![sum-of-all-stock-fund-&&-mixed-fund-market-value](image/README/sum-of-all-stock-fund-&&-mixed-fund-market-value.png)

### size effect in funds

![cumulative-return-in-long-short-stock-funds-3-groups](image/README/cumulative-return-in-long-short-stock-funds-3-groups.png)

stock fund, long-short yield > 0, one-sided t-test result

`Ttest_1sampResult(statistic=-0.3712326871145363, pvalue=0.6445771294168032)`

![cumulative-return-in-long-short-mixed-funds-3-groups](image/README/cumulative-return-in-long-short-mixed-funds-3-groups.png)

blend fund, long-short yield > 0, one-sided t-test result

`Ttest_1sampResult(statistic=-1.025866442813339, pvalue=0.8469542508537611)`

### all funds have positive return

2016-3, all stock fund have positive return. An error?

double check `Win.d` stock fund adjusted NAV, and calculate 2016-3 return. It's an anomaly only

![all-funds-positive-return](image/README/all-funds-positive-return.png)
