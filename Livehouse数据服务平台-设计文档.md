vehouse数据服务平台设计文档
1. 介绍
本文档用于内部开发使用。
系统名称：Livehouse数据服务平台
任务概述：本系统为Livehouse提供可信的票房数据管理、分析与预测；根据豆瓣音乐人数据与现场数据为Livehouse推荐能为其带来更多票房的乐队。我们将与现场POGO测量技术，与抓取的豆瓣音乐人、同城活动的数据进行整合，并通过可视化技术增强Livehouse对其业务模式的理解。在更大的范围内，实现Livehouse产业模式的量化。
2. 系统功能说明
1) 系统示意图

2) 系统功能点
a) 票房数据采集及录入（表格）

    票房数据直接来自Livehouse(MAO)的相关负责人，他们为系统提供基础数据，据此我们可以完成系统原型。之后，Livehouse将可以通过网站进行票房数据录入。
        Livehouse能够记录的票房数据如下：
            日期 / 星期 / 买票数量 / 买票收入金额 / 吧台收入金额 / 支票、刷卡 / 租金 /其他收入金额 / 总计 / 演出类别 / 演出名称 / 演出乐队
                    通过一个python脚本，可以将数据转入数据库中。
                            该数据表LivehouseRecordTable设计如下，根据已有的库进行了增删，为简化处理，不为金额设立float型数据，均为int型。活动名称与演出乐队可以通过与EventTable、EventSiteTable、SiteTable进行多表联查。
                            字段名
                            字段含义
                            数据类型
                            eventid(key)
                            活动id 唯一标示
                            varchar(100)
                            datetime
                            日期
                            varcher(255)
                            ticket
                            买票数量
                            int(10)
                            ticketincome
                            买票收入金额
                            int(10)
                            barincome
                            吧台收入金额
                            int(10)
                            checkincome
                            支票、刷卡金额
                            int(10)
                            rentincome
                            租金
                            int(10)
                            otherincome
                            其他收入金额
                            int(10)
                            totalincome
                            总计
                            int(10)
                            eventtype
                            活动类型（mao：MAO安排 siterent：场地出租 host：主办方安排 maoandhost：MAO&主办方一起 other：其他）
                            varchar(100)
                                票房数据（演出日志）管理为单独页面，进行分页及每个字段的增删改查，并且支持批量导入。
                                b) Livehouse历史票房分析（趋势图）
                                 MAO票房分析页面
                                    该功能为Livehouse提供对不同月份的票房趋势分析，形成折线的趋势图，横坐标为每月日期，纵坐标为ticket。
                                        左侧为不同的月份标签，为多选标签（按钮或复选框），并附带有图例（或在折线上标注出），点击后则可以将该月份的趋势图显示在页面中间的图中。数据从LivehouseRecordTable中查询得到。
                                            附加功能：提供更多类型的趋势图，如barincome、totalincome
                                            c) Livehouse票房预测（列表）

                                                从票房数据我们可以获得每个活动的具体票房数据，从Douban可以获得每个同城活动、参与活动的音乐人，根据pogo地毯测量的数据我们能够对每场演出的音乐人做精细的数据分析，除此以外我们还可以根据日期、票价、天气、主题等因素挖掘出票房是如何被影响，通过这个模型能够预测出下一个演出会有多少人参加。
                                                    目前我们可以依赖可靠的因素如下，通过R2作为模型解释度评价标准，目标为90%。
                                                    因变量：
                                                    买票数量ticket
                                                    自变量：
                                                    Douban活动感兴趣人数interested
                                                    Douban活动参加人数joined
                                                    日期date（工作日、周末、节假日有较大差距）
                                                    参与Douban活动的音乐人最大关注度maxfollow（看演出一般冲着大牌）
                                                    参与Douban活动的音乐人平均关注度avgfollow
                                                    票价fee
                                                        即将要加入的变量：
                                                                天气weather
                                                                        主题theme
                                                                                活动类型eventtype
                                                                                d) Douban音乐人、同城活动数据采集及录入
                                                                                利用几个Python脚本我们可以从Douban爬取页面并分析入库。

                                                                                同城活动数据爬取：
                                                                                从主页进搜索页面，搜“音乐”在全国相关的已结束活动，共有大概10万相关活动，进到每个活动中，可以得到活动的详细信息。如名称、票价、关注度、参与音乐人等。
                                                                                映射获取：
                                                                                对每个活动，都有其主办方及参与的音乐人，根据这个关系建立活动-音乐人映射表。大概有8万映射
                                                                                站点数据爬取：
                                                                                活动下的音乐人及小站的url会被记录下，并进行进一步抓取，从而获得音乐人、livehouse及厂牌的数据。另一方面通过更详尽的douban音乐人页面也能获取到更多音乐人信息。
                                                                                爬取周期：1月一次的“音乐活动”爬取
                                                                                          1周一次的MAO livehouse活动数据爬取
                                                                                          e) Pogo地毯数据收集及录入
                                                                                          Pogo地毯制备、采集等不在本文档范畴内。
                                                                                          每次在livehouse进行数据采集后，我们可以知道：每个乐队的每首歌中观众的每秒pogo数据。
                                                                                          每条pogo数据类似于：时间datetime，被触发的发射器channelid，被触发的陶瓷片index，每次数据会有15万之多，因此在预处理前并不适合存入数据库。
                                                                                          在处理后，我们将每秒的数据合并，其数据表PogoLogTable如下：
                                                                                          字段名
                                                                                          字段含义
                                                                                          数据类型
                                                                                          eventid
                                                                                          活动id
                                                                                          varchar(100)
                                                                                          songid
                                                                                          歌曲id
                                                                                          varchar(100)
                                                                                          songname
                                                                                          歌曲名
                                                                                          varchar(100)
                                                                                          singerid
                                                                                          歌手id
                                                                                          varchar(100)
                                                                                          timestamp
                                                                                          时间戳
                                                                                          varchar(100)
                                                                                          pogonum
                                                                                          该秒pogo次数
                                                                                          int(10)
                                                                                          f) 乐队及Livehouse活跃度查看（分页时间轴）
                                                                                          豆瓣乐队/Livehouse分析
                                                                                          在左侧我们建立增粉排行榜，在右侧显示出乐队对应的演出频度，该图以时间轴显示，横坐标为时间，对应12个月，点击气泡进入一个月中每次演出的平均pogo趋势图（折线图）。
                                                                                          而livehouse将以同样的形式显示。方块代表livehouse举办演出的频度，左侧也为livehouse的增粉排行榜，点击某个方块进入的是一个月内livehouse的平均pogo趋势图。
                                                                                          g) 乐队/livehouse每次演出平均pogo数据趋势图（折线图）

                                                                                            从PogoLogTable我们能获取到乐队在livehouse的现场每首歌横向比较表现的数据，我们将形成上面的折线图。
                                                                                                其横坐标为一周或一个月的活动，纵坐标为平均pogo数。
                                                                                                    该图会以弹出框或气泡形式出现，并不以页面上单独图片出现，嵌入到乐队分析页面。
                                                                                                        对于livehouse则没有歌曲的区分。
                                                                                                        h) 音乐人关注增加量排名及查看（排行榜）
                                                                                                        增粉数据库的音乐人具体数据来自SiteTable，抓取频度为一周一次，这样我们每周能够算出每个音乐人follow关注人数的增加量。根据这个量我们能够获得增粉排行榜。
                                                                                                        i) livehouse现场pogo分析
                                                                                                        MAO现场分析
                                                                                                            数据来自PogoRecorderTable。
                                                                                                                左侧可供用户选择需要查看的报告（单选或互斥按钮），下方将实时刷新出歌曲清单，折线图为每个歌手在该次演出中现场表现（每首歌pogo平均数得趋势），下方有每个歌手的图例。
                                                                                                                j) 针对演出的音乐人推荐（列表）
                                                                                                                 MAO乐队推荐页面
                                                                                                                    该页面中提供了4种不同的推荐。
                                                                                                                        第一类来自在MAO演出次数最多的5个乐队。
                                                                                                                            第二类来自于MAO相似的livehouse演出次数最多的5个乐队。
                                                                                                                                第三类来自平均pogo次数最多的5个乐队。
                                                                                                                                    第四类来自智能推荐算法，该算法从预测的线性模型反求出MAO最可能请的5个乐队。
                                                                                                                                    3. 运行环境限定
                                                                                                                                    服务器：公司服务器Ubuntu13.04 64位
                                                                                                                                    地址：222.35.20.135:8008
                                                                                                                                    技术构成：PHP + Python + Mysql + HTML + jQuery + BootStrap
