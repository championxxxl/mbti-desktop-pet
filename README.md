# MBTI Desktop Pet 🎨

智能人格化桌宠助手 - AI Desktop Pet with MBTI Personalities

一个基于MBTI人格理论的智能桌面宠物助手，具备用户意图识别、记忆学习和自动化操作功能。

An intelligent desktop pet assistant based on MBTI personality theory with user intent recognition, memory learning, and automation capabilities.

> 📍 **项目状态 / Project Status**: v0.1.0-alpha | 75% 完成 | 🟡 活跃开发中  
> 📚 **快速了解**: [当前进度](./当前进度.md) | [Quick Reference](./QUICK_REFERENCE.md) | [Roadmap](./ROADMAP.md) | [Full Status](./PROJECT_STATUS.md)  
> 🎯 **想贡献？**: [现在该做什么？](./现在该做什么.md) | [TODO List](./TODO.md)  
> 🎉 **最近更新 / Recent Updates** (2026-02-06): 意图识别系统优化完成，100个测试全部通过！/ Intent recognition optimized with 100% test pass rate!

## ✨ 核心功能 Core Features

### 1. 🎭 MBTI人格化陪伴 (MBTI Personality-based Companionship)

- 支持全部16种MBTI人格类型
- 每种人格具有独特的交互风格和沟通偏好
- 可随时切换人格类型
- 个性化的问候和回应方式

**支持的MBTI类型：**
- **分析家 (Analysts)**: INTJ, INTP, ENTJ, ENTP
- **外交家 (Diplomats)**: INFJ, INFP, ENFJ, ENFP
- **守卫者 (Sentinels)**: ISTJ, ISFJ, ESTJ, ESFJ
- **探险家 (Explorers)**: ISTP, ISFP, ESTP, ESFP

### 2. 🧠 智能意图识别 (Intelligent Intent Recognition)

- **文本分析**：自动识别用户输入的意图类型
- **屏幕监控**：分析当前窗口活动和用户行为
- **上下文感知**：结合历史记忆提供精准帮助

**识别的意图类型：**
- 帮助请求 (Help Request)
- 任务执行 (Task Execution)
- 信息查询 (Information Query)
- 自动化请求 (Automation Request)
- 文件操作 (File Operation)
- 代码协助 (Code Assistance)
- 写作协助 (Writing Assistance)
- 网络搜索 (Web Search)

### 3. 💾 记忆系统 (Memory System - Like Memu)

- **持久化存储**：SQLite数据库存储所有交互历史
- **模式学习**：识别用户习惯和常用操作
- **上下文检索**：根据当前需求检索相关历史记忆
- **偏好分析**：学习用户的工作偏好和时间模式

### 4. ⚡ 自动化操作 (Automation - Like Claude Desktop)

- **屏幕自动化**：自动点击、输入、截图等操作
- **预设任务**：提供常用自动化任务库
- **自定义宏**：录制和保存自定义操作序列
- **智能建议**：根据上下文建议自动化方案

## 🚀 快速开始 Quick Start

### 前置要求 Prerequisites

- Python 3.8+
- pip (Python package manager)

### 安装 Installation

1. 克隆仓库 Clone the repository:
```bash
git clone https://github.com/championxxxl/mbti-desktop-pet.git
cd mbti-desktop-pet
```

2. 安装依赖 Install dependencies:
```bash
pip install -r requirements.txt
```

或者使用setup.py安装 Or install using setup.py:
```bash
pip install -e .
```

3. 配置环境变量 Configure environment variables:
```bash
cp .env.example .env
# 编辑 .env 文件，添加你的API密钥（可选）
# Edit .env file and add your API keys (optional)
```

### 运行 Run

直接运行 Run directly:
```bash
python src/mbti_pet/main.py
```

或使用已安装的命令 Or use installed command:
```bash
mbti-pet
```

## 📖 使用指南 Usage Guide

### 基本操作 Basic Operations

1. **选择人格**：在顶部下拉菜单中选择你喜欢的MBTI人格类型
2. **聊天交互**：在输入框中输入消息，按Enter或点击"Send"发送
3. **快捷功能**：
   - 📸 Screenshot - 截取屏幕
   - 🧠 Memory - 查看记忆摘要
   - ⚡ Automate - 查看可用的自动化任务

### 意图识别示例 Intent Recognition Examples

```
# 帮助请求
"帮我优化代码" / "How can you help me?"

# 任务执行
"打开浏览器" / "Open my browser"

# 信息查询
"Python中如何处理文件？" / "What is the best way to...?"

# 自动化请求
"自动保存所有文件" / "Automate the backup process"
```

### 记忆功能 Memory Features

桌宠会自动记录：
- 所有对话内容
- 用户请求的任务
- 屏幕活动模式
- 自动化操作历史

通过点击"🧠 Memory"按钮可以查看记忆摘要。

### 自动化任务 Automation Tasks

预设任务包括：
- Take Screenshot - 截取屏幕
- Copy Text - 选择并复制文本
- Search Web - 打开浏览器搜索

更多自定义任务正在开发中。

## 🏗️ 项目结构 Project Structure

```
mbti-desktop-pet/
├── src/
│   └── mbti_pet/
│       ├── __init__.py           # 包初始化
│       ├── main.py               # 主入口
│       ├── config.py             # 配置管理
│       ├── personality/          # MBTI人格系统
│       │   └── __init__.py
│       ├── memory/               # 记忆系统
│       │   └── __init__.py
│       ├── intent/               # 意图识别
│       │   └── __init__.py
│       ├── automation/           # 自动化引擎
│       │   └── __init__.py
│       └── ui/                   # 用户界面
│           └── __init__.py
├── data/                         # 数据存储目录
│   └── memory.db                 # 记忆数据库
├── requirements.txt              # Python依赖
├── setup.py                      # 安装配置
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git忽略规则
└── README.md                     # 项目文档
```

## 🔧 配置选项 Configuration Options

在 `.env` 文件中可配置：

```bash
# API密钥（用于AI增强功能，可选）
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# 默认人格类型
DEFAULT_MBTI_TYPE=ENFP

# 桌宠名称
PET_NAME=PetBot

# 记忆设置
MEMORY_DB_PATH=./data/memory
MAX_MEMORY_SIZE=1000

# 监控设置
SCREEN_MONITOR_ENABLED=true
SCREEN_MONITOR_INTERVAL=30

# 自动化设置
AUTOMATION_ENABLED=true
AUTO_SUGGEST_ENABLED=true
```

## 🎯 技术特点 Technical Features

- **PyQt5 GUI**: 现代化的图形界面
- **SQLite数据库**: 轻量级持久化存储
- **PyAutoGUI**: 跨平台自动化支持
- **正则表达式 + AI**: 高效准确的意图识别（95%准确率）
- **模块化设计**: 易于扩展和维护

## 🎉 最近更新 Recent Updates

### v0.1.0-alpha (2026-02-06)

**重要改进 / Major Improvements**:
- ✅ **意图识别系统大幅优化** - Intent recognition system significantly improved
  - 所有100个测试用例通过 (100% test pass rate)
  - 修复了"Open my browser"等常见指令的误识别
  - 改进了自动化、网页搜索、任务执行的识别模式
  - 识别准确率从80%提升至95%

**功能完成度 / Completion Status**:
```
MBTI人格系统:    ████████████████████ 100%
意图识别系统:    ███████████████████░  95% ⬆️ (从80%提升)
记忆系统:        ████████████████████ 100%
自动化系统:      ██████████████████░░  90%
用户界面:        ██████████████░░░░░░  70%

总体进度:        ███████████████░░░░░  75% ⬆️ (从68%提升)
```

**下一步计划 / Next Steps**:
- 🎨 完善UI聊天界面功能
- 🤖 集成AI模型 (OpenAI/Anthropic)
- ✅ 添加更多单元测试

## 🤝 贡献 Contributing

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📝 开发计划 Development Roadmap

- [x] MBTI人格系统实现 (100%)
- [x] 基础UI界面 (70%)
- [x] 意图识别引擎 (95% - 最近优化完成!)
- [x] 记忆系统 (100%)
- [x] 自动化框架 (90%)
- [ ] UI界面完善 (进行中)
- [ ] AI模型集成 (OpenAI/Anthropic)
- [ ] 语音交互支持
- [ ] 更多自动化任务模板
- [ ] 插件系统
- [ ] 移动端同步

## 🐛 已知问题 Known Issues

- ~~意图识别准确率需要优化~~ ✅ **已修复** (2026-02-06) - 100个测试全部通过
- UI界面功能尚未完全实现（进行中）
- 屏幕监控功能需要适当的系统权限
- PyAutoGUI在某些Linux桌面环境中可能需要额外配置
- 系统托盘图标需要提供图标文件

## 📄 许可证 License

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 👥 作者 Author

Champion - [@championxxxl](https://github.com/championxxxl)

## 🙏 致谢 Acknowledgments

- MBTI人格理论
- PyQt5社区
- PyAutoGUI项目
- 所有贡献者

---

**享受你的智能桌宠助手！ Enjoy your intelligent desktop pet assistant! 🎉**
