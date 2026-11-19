# 剪贴板助手

元扫雷第三方插件。使用带 GitHub 插件发现功能的新版元扫雷。

## 安装

1. 在插件管理器中打开「插件」→「插件市场」。
2. 搜索 `metasweeper-clipboard-replay`，选择版本并安装，然后重启插件管理器。

也可以选择「从仓库 URL 安装」，输入 <https://github.com/ljzloser/metasweeper-clipboard-replay>。此仓库使用 GitHub 主题 `metasweeper-plugin` 和以 `metasweeper-v` 开头的版本标签。插件运行依赖由宿主提供。

原有监听设置会继续从元扫雷数据目录读取。启用插件后，复制受支持的录像下载链接或 95 经典扫雷小程序分享码即可打开回放。可用格式见插件说明。

[插件使用说明](clipboard_replay/README.md)

## 开发与测试

在已按主仓说明安装开发依赖的环境中，设置元扫雷源码路径，再从本仓库根目录运行测试：

```powershell
$env:PYTHONPATH = 'D:\work\Python\Solvable-Minesweeper\src'
$env:QT_QPA_PLATFORM = 'offscreen'
& 'D:\work\Python\Solvable-Minesweeper\.venv\Scripts\python.exe' -m pytest
```

Qt 翻译的 `.ts` 和 `.qm` 都随包分发。修改翻译源文件后，用 `pyside6-lrelease` 重新生成对应的 `.qm`。

本仓库的原创插件代码采用 [MIT 许可证](LICENSE)。第三方代码及素材遵循各自的许可证或授权条款。
