# WeChatWarning
**别水成了工作群！**

基于[wxauto](https://github.com/cluic/wxauto)编写的一个简单程序，实现对微信重点群聊/联系人的弹窗提示，避免「危险发言」。

## 开箱即用

1. 下载[release](https://github.com/SouthernHU/WeChatWarning/releases)中的[WeChatWarning.exe](https://github.com/SouthernHU/WeChatWarning/releases/download/release-v1.0.0/WeChatWarning.exe)文件
2. 在`WeChatWarning.exe`同一目录下新建`warningList.txt`，在该txt中输入你想要设置提醒的联系人/群组的备注
3. 在登录微信之后双击运行`WeChatWarning.exe`，软件将会每2秒获取一次微信的窗口信息，并与`warningList.txt`中的列表比对。
4. 如果检测到当前对话框存在于`warningList.txt`中，将会弹窗报警。
5. 软件将始终保持在后台运行，你可以在任务栏托盘中找到他，右键点击即可退出。
6. 注意，txt文件以换行为分隔符，中每一行是一个联系人/群组。

## 项目思路

- 通过[wxauto](https://github.com/cluic/wxauto)获取微信当前对话框的标题
- 与`warningList.txt`中的列表进行比对
- 使用[win32gui](https://pypi.org/project/win32gui/)判断前台窗口是否是微信，避免空循环以节约系统资源