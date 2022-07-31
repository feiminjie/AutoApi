# autoapi 自动生成测试用例及测试数据
由于本人Python代码能力比较一般，所以写的不是很好，目前已经在我就职的公司实现了接口自动化，所以将主体抽出来发布上来，给大家做参考
tips：
1、代码中所用的测试地址为个人服务器，请不要大量测试
2、如果要用到自己的公司项目，需要改一定的写死的参数，比如抓取参数的路径，及ini的配置文件，当然初次调试后就不会再出现了
3、如果有更好的实现方式请联系13537847218，直接加微信。

设计思想：
目前我接触的接口文档大部分都是swagger，所以就考虑去请求api文档，获取到接口的每一个参数，再根据这些参数可以预设的正确和错误的参数，去生成测试用例和测试数据，最后批量运行，回收数据

使用手册：
第一步： 拉取代码到本地
第二步： 修改.ini配置文件中的地址
第三步： 修改generate.py的参数路径， 可以一步一步运行，根据报错提示去修改代码
第四步： 需要添加create_test_data.py和set_params.py针对每一个参数的范围值，目前将数据分为三层，第一层基础数据比如gener_basedata.py字符类型，第二层是参数要求set_params，比如必填，长短,
        第三层是接口的参数数据要求create_test_data.py,根据参数的要求去分为正确值和错误值
