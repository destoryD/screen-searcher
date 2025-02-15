# 🚀 屏幕即时搜 - OCR屏幕搜索工具

![演示截图](./index.png)

📌 一款基于OCR技术的桌面应用程序，可通过快捷键快速搜索屏幕上任意可见文字。

## ✨ 功能特性

- 📷 **一键截图** - 使用 `Ctrl+Shift+S` 快捷键捕获屏幕区域
- 🔍 **即时OCR识别** - 通过Tesseract OCR引擎提取文字内容
- 🖥️ **图形界面** - 基于Tkinter开发的跨平台界面
- ⚡ **快捷键支持** - 可在 `config.json` 中自定义快捷键
- 🈶 **多语言支持** - 支持100+种语言的OCR识别
- 📚 **搜索历史** - 自动保存最近20条搜索记录
- 🌐 **API集成** - 内置翻译和词典查询功能

## 🛠️ 安装指南

```bash
# 克隆仓库
git clone https://github.com/yourusername/screen-searcher.git
cd screen-searcher

# 安装依赖
pip install -r requirements.txt

# 安装 paddleocr 依赖
pip install paddlepaddle paddle-ocr

```

## 📖 使用说明

1. 运行 `main.py` 启动应用程序
2. 按下 `Ctrl+Shift+S` 截取屏幕区域
3. 识别文字将自动填入搜索框

```

## 🚦 快速开始

1. 启动应用程序：
```bash
python src/main.py
```
2. 按下 `Ctrl+Shift+S` 截取屏幕区域
3. 识别文字将自动填入搜索框
4. 选择操作：复制/翻译/保存/分享

> 💡 中文用户提示：在OCR语言设置中添加 `ch` 可获得更好的中文识别效果


## 🤝 参与贡献
1. Fork 本项目
2. 新建功能分支 (`git checkout -b feature/新功能`)
3. 提交修改 (`git commit -m '添加了新功能'`)
4. 推送分支 (`git push origin feature/新功能`)
5. 提交Pull Request

## 📄 开源协议
本项目采用 MIT 许可证，完整内容请查看 `LICENSE` 文件。
