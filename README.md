# 🚀 Screen-Searcher - OCR屏幕搜索工具

![演示截图](./index.png)

📌 一款基于OCR技术的桌面应用程序，可通过截图快速搜索屏幕上的任意题目。

## ✨ 功能特性

- 📷 **一键截图** - 使用 `自定义` 快捷键捕获屏幕区域
- 🔍 **即时OCR识别** - 通过各类OCR引擎提取文字内容
- 🖥️ **图形界面** - 基于Tkinter开发的跨平台界面
- ⚡ **快捷键支持** - 可在 `UI界面` 中自定义快捷键
- 🈶 **多语言支持** - 支持100+种语言的OCR识别
- ~~📚 **搜索历史** - 自动保存最近20条搜索记录~~
- 🌐 **API集成** - 内置LIKE知识库查询功能

## 🛠️ 安装指南

```bash
# 克隆仓库
git clone https://github.com/yourusername/screen-searcher.git
cd screen-searcher

# 安装依赖
pip install -r requirements.txt

# 安装 paddleocr 依赖
pip install paddlepaddle paddle-ocr

# 运行程序
python src/main.py
```

## 🚦 快速开始

1. 启动应用程序：
```bash
python src/main.py
```

2. 按下 `win+shift+q` 截取屏幕区域
3. 识别文字将自动填入搜索框
4. 选择操作：搜索

PaddleOCR
> 💡 中文用户提示：在OCR语言设置中添加 `ch` 可获得更好的中文识别效果

## 🤝 参与贡献

1. Fork 本项目
2. 新建功能分支 (`git checkout -b feature/新功能`)
3. 提交修改 (`git commit -m '添加了新功能'`)
4. 推送分支 (`git push origin feature/新功能`)
5. 提交Pull Request

## 📄 开源协议

本项目采用 MIT 许可证，完整内容请查看 `LICENSE` 文件。
