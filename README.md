# Dota2 Draft Agent

一个可本地运行、也可通过 GitHub Pages 免费公开访问的 Dota2 AI Agent Demo。用户输入己方英雄、敌方英雄和位置偏好后，Agent 会调用 OpenDota 公开数据，完成英雄识别、阵容结构分析、克制候选推荐和打法建议生成。

## 适合放在简历里的说法

- 构建 Dota2 BP 辅助 Agent，集成 OpenDota public API，实现英雄数据缓存、阵容解析、matchup 克制分析和推荐结果可视化。
- 设计 Agent 工具链：`load_hero_data -> parse_draft_input -> analyze_team_balance -> recommend_heroes -> compose_answer`。
- 使用 Python 标准库实现本地 Web 服务，前端使用原生 JavaScript 展示候选英雄、阵容风险、出装建议和完整回答。

## 功能

- 支持英文英雄名和部分中文简称，例如 `影魔`、`剑圣`、`Lion`。
- 页面和回答中的英雄显示名统一使用中文，内部仍保留英文名用于 OpenDota 数据匹配。
- 支持选择玩家段位，打法建议会按段位调整执行重点。
- 根据己方阵容判断控制、开团、辅助属性、经济点和攻击类型短板。
- 根据敌方英雄 matchup 数据推荐候选英雄。
- 根据己方主英雄、位置偏好和敌方英雄类型生成出门装、对线装、核心装、针对装，并在页面中使用 Dota2 装备图标展示。
- 根据敌方控制、爆发、前排厚度给出装备和打法建议。
- 支持 `data/playbook.json` 个人理解/实战样本库，命中当前阵容后会单独展示“实战样本与个人理解”。
- 所有 OpenDota 数据会缓存在 `data/`，避免每次请求都访问网络。

## 攻略内容维护

推荐英雄和胜率只作为候选参考，不应直接当作攻略结论。真正想体现游戏理解，优先维护：

```text
data/playbook.json
```

每条内容建议包含：

- `source_type`：个人理解、天梯样本、职业样本、复盘样本。
- `match_id`：真实对局 ID，没有就不要冒充样本。
- `roles`、`allies`、`enemies`、`keywords`：用于决定什么场景下引用。
- `summary`、`points`：写清楚具体时间点、兵线/视野/装备节奏，以及不适用的情况。

GitHub Pages 静态版对应文件是：

```text
docs/data/playbook.json
```

## 运行

```powershell
python app.py
```

浏览器打开：

```text
http://127.0.0.1:8770
```

## 免费公开访问

项目已提供静态版页面，放在 `docs/` 目录，可直接用 GitHub Pages 部署，不需要 Render，也不需要绑卡。

仓库推送到 GitHub 后，在 GitHub 仓库里打开：

```text
Settings -> Pages -> Source -> Deploy from a branch
```

然后选择：

```text
Branch: main
Folder: /docs
```

保存后等待 GitHub Pages 构建完成。公开访问地址通常是：

```text
https://anti-genius.github.io/dota2-agent-demo/
```

`http://127.0.0.1:8770` 只能在本机打开，不能直接发给别人。要临时分享本机服务，可以使用 ngrok、cloudflared tunnel 等内网穿透工具；要长期公开访问，优先使用 GitHub Pages。

## 云服务部署

项目也支持云平台常见的 `PORT` 环境变量。如果平台分配了端口，服务会自动监听 `0.0.0.0:$PORT`；本地运行时仍默认使用 `127.0.0.1:8770`。

Render 当前可能要求账号填写支付信息。若不想绑卡，建议使用上面的 GitHub Pages 静态部署方案。

Start Command：

```text
python app.py
```

Health Check Path：

```text
/healthz
```

## API

```http
POST /api/analyze
Content-Type: application/json
```

示例：

```json
{
  "allies": "Axe, Lion, 剑圣",
  "enemies": "影魔, Sniper, Crystal Maiden",
  "role": "offlane",
  "rank": "legend",
  "question": "这把我该补什么英雄，团战怎么打？"
}
```

## 数据说明

英雄统计和 matchup 数据来自 OpenDota public API。推荐逻辑是工程启发式，实战结论应优先来自个人复盘、真实 match id 和高质量样本；如果要做成更强的 Agent，可以继续接入：

- 当前版本 patch 数据和英雄改动。
- STRATZ/Dotabuff 等更细粒度数据源。
- 大模型总结模块：把工具输出交给 LLM 生成更自然的中文教练建议。
- 个人比赛录像解析：根据 match id 获取 picks、items、lane、GPM/XPM、团战和死亡原因。
