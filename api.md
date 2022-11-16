
# API文档 v1.0.0

## 1 规范说明

### 1.1 通信协议

HTTPS协议

### 1.2 请求方法

详见每个端口的文档。


### 1.3 响应报文结构
#### 1.3.1 结构说明
所有接口响应均采用JSON格式，如无特殊说明，每次请求的返回值中，都包含下列字段：

| 参数名称    | 类型	           | 出现要求 | 描述                         |
|:--------|:--------------|:-----|:---------------------------|
| code    | int           | R			 | 响应码，代码定义请见“附录A 响应吗说明”      |
| message | string        | R			 | 响应描述                       |
| data    | object (dict) | R			 | 部分接口有特定参数，详见每个接口定义。无则为null |

#### 1.3.2 响应报文示例

```
{
    "Code":200,
    "Msg":"调用成功",
    "Data":{
        "uid":"142857"
    }
}
```


## 2. 接口定义

### 2.1 技能列表
- **接口说明：** 获取技能列表
- **接口地址：** /actions
- **接口方法：** GET


#### 2.1.1 请求参数
无


#### 2.1.2 返回结果

| 参数名称                      | 类型     | 描述                    |
|:--------------------------|:-------|:----------------------|
| code                      | int    | 响应码，代码定义请见“附录A 响应吗说明” |
| message                   | string | &nbsp;                |
| data                      | object | &nbsp;                |
| &emsp;ActionList          | Object | 技能列表                  |
| &emsp;&emsp;\<ActionName> | int    | 技能名与对应id              |

示例：

```
{
    "Code":200,
    "Msg":"Success",
    "Data":{
        "ActionList"{<action_name:string>:<id:int>}
    }
}
```



### 2.2 初始化会话
- **接口说明：** 初始化会话并获取会话id，需在大部分接口中用到
- **接口地址：** /initiate
- **接口方法：** GET

#### 2.2.1 请求参数
  
无


#### 2.2.2 返回结果

| 参数名称      | 类型     | 描述                    |
|:----------|:-------|:----------------------|
| code      | int    | 响应码，代码定义请见“附录A 响应吗说明” |
| message   | string | &nbsp;                |
| data      | object | &nbsp;                |
| &emsp;uid | int    | 会话id                  |


示例：

```
{
    "code":200,
    "message":"Success",
    "data":{
        "uid":"142857",
    }
}
```

### 2.3 初始化模拟
- **接口说明：** 输入状态参数以初始化引擎
- **接口地址：** /engine/\<uid>/start
- **接口方法：** POST

#### 2.3.1 请求参数
  
| 参数名称               | 类型  | 描述       |
|:-------------------|:----|:---------|
| ProgressEfficiency | int | 制作精度     |
| QualityEfficiency  | int | 加工精度     |
| TotalCP            | int | 制作力      |
| TotalDurability    | int | 配方总耐久    |
| TotalProgress      | int | 配方总进度    |
| TotalQuality       | int | 配方总品质    |
| ProgressDivider*   | int | 配方作业难度系数 |
| QualityDivider*    | int | 配方加工难度系数 |
| ProgressModifier*  | int | 配方作业压制系数 |
| QualityModifier*   | int | 配方加工压制系数 |
| Mode**             | int | 模式       |

 /*  这四项数据如果是满级配方应该是有个固定值的，专家配方应该为(13, 11.5, 0.7, 0.6) 可能需要更多数据测试一下

 /** 专家模式为2

示例：

```
{
  "ProgressEfficiency": 2552,
  "QualityEfficiency": 2662,
  "TotalCP": 605,
  "TotalDurability": 80,
  "TotalProgress": 3000,
  "TotalQuality": 25565,
  "ProgressDivider": 13,
  "QualityDivider": 11.5,
  "ProgressModifier": 1,
  "QualityModifier": 1,
  "Mode": 2
}

```

#### 2.3.2 返回结果

| 参数名称    | 类型     | 描述                    |
|:--------|:-------|:----------------------|
| code    | int    | 响应码，代码定义请见“附录A 响应吗说明” |
| message | string | &nbsp;                |
| data    | object | &nbsp;                |


示例：

```
{
    "code":200,
    "message":"Success",
    "data":null
}
```


### 2.4 使用技能
- **接口说明：** 使用特定技能
- **接口地址：** /engine/\<uid>/use-action
- **接口方法：** POST

#### 2.4.1 请求参数
  
| 参数名称   | 类型  | 描述   |
|:-------|:----|:-----|
| Action | int | 目标技能 |

```
{
  "Action": 2
}
```

#### 2.4.2 返回结果

| 参数名称                | 类型     | 描述                    |
|:--------------------|:-------|:----------------------|
| code                | int    | 响应码，代码定义请见“附录A 响应吗说明” |
| message             | string | &nbsp;                |
| data                | object | &nbsp;                |
| &emsp;Action Result | int    | 技能使用结果                |

2.4.2.1 技能使用结果

| 代码  | 描述          |
|:----|:------------|
| 100 | 制作继续，技能使用成功 |
| 101 | 制作继续，技能使用失败 |
| 200 | 制作成功        |
| -1  | 制作失败        |

示例：

```
{
    "code":200,
    "message":"Success",
    "data":null
}
```


### 2.5 获取当前状态
- **接口说明：** 获取当前制作状态
- **接口地址：** /engine/\<uid>/start
- **接口方法：** GET

#### 2.5.1 请求参数
  
无


#### 2.5.2 返回结果

| 参数名称              | 类型     | 描述                    |
|:------------------|:-------|:----------------------|
| code              | int    | 响应码，代码定义请见“附录A 响应吗说明” |
| message           | string | &nbsp;                |
| data              | object | &nbsp;                |
| CurrentProgress   | int    | 当前进展                  |
| CurrentQuality    | int    | 当前品质                  |
| CurrentCP         | int    | 当前cp                  |
| CurrentDurability | int    | 当前耐久                  |
| Buffs             | ditc   | buff列表 {<名字>:<剩余时间>}  |
| InnerQuiet        | int    | 内静层数                  |


示例：

```
{
    "code":200,
    "message":"Success",
    "data": 
    {
        "CurrentProgress": 1023,
        "CurrentQuality": 3214,
        "CurrentCP": 24,
        "CurrentDurability": 15,
        "Buffs": [0, 0, 0, 0, 0, 0, 0, 0, 0]
}
}
```

## 3 附录A 响应码说明

| 响应码	  | 说明               | 是否包含详细内容（返回在data中） |
|:------|:-----------------|:-------------------|
| 200		 | Success          | N                  |
| 301		 | Missing Key      | Y                  |
| 302		 | Missing Action   | N                  |
| 310		 | Finished         | N                  |
| 311		 | Not 1st turn     | N                  |
| 312		 | Not HQ           | N                  |
| 310		 | Inner Quiet < 10 | N                  |
| 311		 | No enough CP     | N                  |
| 312		 | Already Used     | N                  |
