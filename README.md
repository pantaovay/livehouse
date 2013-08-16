## App架构
1. 每个大的业务需求对应一个app，比如对于`douban`的数据采集、分析和展示全部放在django工程下的`douban`这个app里；
2. 不同业务可以访问所有model中的数据，用来应对交互性的业务需求。

## 爬虫架构
1. 爬虫放到相应的app下，比如`douban`站点的爬虫全部规划到`douban`这个app下；
2. 使用`cron`定时调用爬虫；
3. 调用爬虫可以有两种方式：
    * `curl`访问django工程的url；
    * 直接在`crontab`中调用运行命令。

## 前端架构
1. 采用`bootstrap3`；
2. 使用django自带的模板引擎。

## 后台管理
1. django自带比较优秀的amin，需要统计界面。
