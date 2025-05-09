数据来源：[国泰安数据](https://cn.gtadata.com "国泰安数据库")

**基金市场系列 —** **公募基金**

**基金概况 —** **基金主体信息表**

`FUND_MainInfo`

`1998-03-27 --> 2022-09-28`


| 1          | 2        | 3        |
| ------------ | ---------- | ---------- |
| 基金主代码 | 基金全称 | 成立日期 |

* [X] update
* [X] upload

**基金概况 —** **费率变动文件**

`FUND_FeesChange`

`2001-09-04 --> 2022-10-31`


| 1        | 2        |    3    | 4        | 5           |
| ---------- | ---------- | :--------: | ---------- | ------------- |
| 基金代码 | 公告日期 | 费率类型 | 费率名称 | 费率比例(%) |

* [X] update
* [X] upload

**基金概况 —** **基金申购赎回状态变更表**

`FUND_PurchRedChg`

`2015-04-10 --> 2023-03-16`


| 1      | 2              | 3        | 4        | 5        | 6        | 7        |
| -------- | ---------------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| 基金ID | 基金份额类别ID | 基金代码 | 公告日期 | 变更日期 | 申购状态 | 赎回状态 |

* [X] update
* [X] upload

**基金概况 —** **基金代码信息表**

`FUND_FundCodeInfo`

`time range not applicable, last update: 2022-11-1`


| 1        | 2            | 3            | 4          |
| ---------- | -------------- | -------------- | ------------ |
| 基金代码 | 基金相关代码 | 代码类型编码 | 基金主代码 |

* [X] update

**基金概况 —** **份额变动文件**

`Fund_ShareChange`

`1992-03-31 --> 2022-06-30`


| 1        | 2                | 3        | 4          |
| ---------- | ------------------ | ---------- | ------------ |
| 基金代码 | 定期报告类别编码 | 截止日期 | 期末总份额 |

* [X] update

**基金表现 —** **基金日净值文件**

`Fund_NAV`

`注意，一次仅能提取一年`

`2021-09-30 --> 2022-09-29`
`2020-09-30 --> 2021-09-29`
`2019-09-30 --> 2020-09-29`
...
...
`2002-09-30 --> 2003-09-29`
`2001-09-30 --> 2002-09-29`
`2000-09-30 --> 2001-09-29`


| 1        | 2        | 3            |
| ---------- | ---------- | -------------- |
| 交易日期 | 基金代码 | 基金份额净值 |

* [X] update

**收益分配与拆分 —** **基金分配文件**

`Fund_FundDividend`

`1999-03-29 --> 2022-09-29`


| 1        | 2                | 3          | 4          | 5          |
| ---------- | ------------------ | ------------ | ------------ | ------------ |
| 基金代码 | 分配方案公告日期 | 场内除息日 | 场外除息日 | 每份分红数 |

* [X] update

**收益分配与拆分 —** **基金拆分信息文件**

`Fund_Resolution`

`2005-02-17 --> 2022-09-03`


| 1        | 2        | 3                |
| ---------- | ---------- | ------------------ |
| 基金代码 | 公告日期 | 基金份额分拆比例 |

* [X] update

**基金投组 —** **资产配置文件**

`Fund_Allocation`

`1998-06-30 --> 2022-06-30`


| 1          | 2                | 3        | 4        | 5        | 6          | 7              | 8            |
| ------------ | ------------------ | ---------- | ---------- | ---------- | ------------ | ---------------- | -------------- |
| 基金主代码 | 定期报告类别编码 | 截止日期 | 横表编码 | 横表名称 | 权益类投资 | 固定收益类投资 | 资产组合合计 |

* [X] update

**基金投组 —** **按品种分类的债券投资组合**

`Fund_Ptf_BondSpe`

`2004-06-30 --> 2022-09-30`


| 1          | 2                | 3        | 4        | 5                     |
| ------------ | ------------------ | ---------- | ---------- | ----------------------- |
| 基金主代码 | 定期报告类别编码 | 截止日期 | 债券品种 | 占基金资产净值比例(%) |

* [X] update

**基金投组 —** **股票投资明细表**

`Fund_Portfolio_Stock`

`1998-06-30 --> 2022-09-30`


| 1          | 2                | 3        | 4        | 5            | 6    |    7    | 8        | 9             |
| ------------ | ------------------ | ---------- | ---------- | -------------- | ------ | :--------: | ---------- | --------------- |
| 基金主代码 | 定期报告类别编码 | 开始日期 | 截止日期 | 投资类型分类 | 排名 | 股票代码 | 股票名称 | 占净值比例(%) |

* [X] update

**股票市场系列 —** **股票市场交易**

**个股交易数据 —** **日个股回报率文件**

`TRD_Dalyr`

`1990-12-19 --> 2022-12-20`

| 1          | 2                | 3        | 4        | 5            | 6    |    7    |
| ------------ | ------------------ | ---------- | ---------- | -------------- | ------ | ------ |
| 证券代码 | 交易日期 | 日收盘价 | 日个股流通市值 | 日个股总市值 | 考虑现金红利再投资的日个股回报率 | 涨跌幅 |

* [X] update

**个股交易数据 —** **月个股回报率文件**

`TRD_Mnth`

`1990-12 --> 2022-09`


| 1        | 2        | 3            | 4                                |
| ---------- | ---------- | -------------- | ---------------------------------- |
| 证券代码 | 交易月份 | 月个股总市值 | 考虑现金红利再投资的月个股回报率 |

* [X] update

**基本数据 —** **公司文件**

`TRD_Co`

`1990-12-10 --> 2022-10-14`


| 1        | 2        | 3        | 4         |
| ---------- | ---------- | ---------- | ----------- |
| 证券代码 | 证券简称 | 上市日期 | 行业名称A |

* [X] update

**股票市场系列 —** **市场指数**

**成分股信息 —** **指数成分股权重文件**

`IDX_Smprat`

`2005-01-04 --> 2022-10-31`


| 1        | 2        | 3            | 4            | 5       |
| ---------- | ---------- | -------------- | -------------- | --------- |
| 指数代码 | 截止日期 | 成份证券代码 | 成份证券简称 | 权重(%) |

* [X] update
