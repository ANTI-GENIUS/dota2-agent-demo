from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools import (
    OpenDotaClient,
    analyze_role_balance,
    build_hero_index,
    display_hero_name,
    generate_advice,
    generate_item_advice,
    hero_display,
    load_playbook,
    parse_hero_names,
    recommend_heroes,
    select_playbook_entries,
)


@dataclass
class AgentStep:
    name: str
    purpose: str
    output: Any


class Dota2DraftAgent:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.client = OpenDotaClient(data_dir)

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        steps: list[AgentStep] = []

        allies_raw = str(payload.get("allies", "")).strip()
        enemies_raw = str(payload.get("enemies", "")).strip()
        desired_role = str(payload.get("role", "flexible")).strip() or "flexible"
        question = str(payload.get("question", "")).strip()

        heroes = self.client.get_hero_stats()
        hero_index = build_hero_index(heroes)
        steps.append(
            AgentStep(
                name="load_hero_data",
                purpose="加载 OpenDota 英雄统计数据，并构建中英文英雄名索引。",
                output={"hero_count": len(heroes), "index_size": len(hero_index)},
            )
        )

        allies = parse_hero_names(allies_raw, hero_index)
        enemies = parse_hero_names(enemies_raw, hero_index)
        steps.append(
            AgentStep(
                name="parse_draft_input",
                purpose="从用户输入中识别己方和敌方英雄。",
                output={
                    "allies": [display_hero_name(hero) for hero in allies],
                    "enemies": [display_hero_name(hero) for hero in enemies],
                    "unparsed_hint": self._unparsed_hint(allies_raw, enemies_raw, allies, enemies),
                },
            )
        )

        balance = analyze_role_balance(allies)
        steps.append(
            AgentStep(
                name="analyze_team_balance",
                purpose="检查己方阵容的控制、开团、经济点和攻击类型结构。",
                output=balance,
            )
        )

        recommendations = recommend_heroes(
            self.client,
            heroes,
            allies,
            enemies,
            desired_role,
            limit=6,
        )
        steps.append(
            AgentStep(
                name="recommend_heroes",
                purpose="结合敌方 matchup、位置偏好、英雄胜率和职业局出场热度给出候选英雄。",
                output={
                    "count": len(recommendations),
                    "top": recommendations[0]["hero"]["name"] if recommendations else None,
                },
            )
        )

        advice = generate_advice(allies, enemies, desired_role, balance)
        item_advice = generate_item_advice(self.client, allies, enemies, desired_role, question)
        playbook = select_playbook_entries(
            load_playbook(self.data_dir),
            allies,
            enemies,
            desired_role,
            question,
        )
        steps.append(
            AgentStep(
                name="generate_item_advice",
                purpose="根据己方主英雄、位置偏好、敌方英雄类型和用户问题生成出装建议。",
                output={
                    "focus_hero": item_advice["focus_hero"],
                    "lane_items": item_advice["lane"],
                    "core_items": item_advice["core"],
                },
            )
        )

        answer_md = self._build_answer(
            allies=allies,
            enemies=enemies,
            desired_role=desired_role,
            question=question,
            balance=balance,
            recommendations=recommendations,
            advice=advice,
            item_advice=item_advice,
            playbook=playbook,
        )
        steps.append(
            AgentStep(
                name="compose_answer",
                purpose="把工具输出整理成可执行的 BP 和打法建议。",
                output={"answer_chars": len(answer_md)},
            )
        )

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "agent": "Dota2 Draft Agent",
            "input": {
                "allies": allies_raw,
                "enemies": enemies_raw,
                "role": desired_role,
                "question": question,
            },
            "recognized": {
                "allies": [hero_display(hero) for hero in allies],
                "enemies": [hero_display(hero) for hero in enemies],
            },
            "balance": balance,
            "recommendations": recommendations,
            "advice": advice,
            "item_advice": item_advice,
            "playbook": playbook,
            "answer_md": answer_md,
            "steps": [asdict(step) for step in steps],
            "data_note": "Hero statistics are only references. Practical conclusions are pulled from the local playbook when matched.",
        }

    @staticmethod
    def _unparsed_hint(
        allies_raw: str,
        enemies_raw: str,
        allies: list[dict[str, Any]],
        enemies: list[dict[str, Any]],
    ) -> str:
        total_input = [item for item in [allies_raw, enemies_raw] if item.strip()]
        total_found = len(allies) + len(enemies)
        if not total_input:
            return "未输入阵容，Agent 会按通用强度和位置偏好推荐。"
        if total_found == 0:
            return "没有识别到英雄名，请尝试输入英文名或常见中文简称，例如 影魔、剑圣、Lion。"
        return "已识别部分或全部英雄；未识别项不会参与计算。"

    @staticmethod
    def _build_answer(
        allies: list[dict[str, Any]],
        enemies: list[dict[str, Any]],
        desired_role: str,
        question: str,
        balance: dict[str, Any],
        recommendations: list[dict[str, Any]],
        advice: list[str],
        item_advice: dict[str, Any],
        playbook: list[dict[str, Any]],
    ) -> str:
        lines: list[str] = []
        if question:
            lines.append(f"### 问题\n{question}")

        lines.append("### 阵容识别")
        lines.append(
            f"- 己方：{', '.join(display_hero_name(hero) for hero in allies) if allies else '未提供'}"
        )
        lines.append(
            f"- 敌方：{', '.join(display_hero_name(hero) for hero in enemies) if enemies else '未提供'}"
        )
        lines.append(f"- 位置偏好：{desired_role}")

        lines.append("\n### 主要风险")
        for risk in balance["risks"]:
            lines.append(f"- {risk}")

        lines.append("\n### 推荐候选")
        if recommendations:
            for idx, item in enumerate(recommendations[:5], start=1):
                hero = item["hero"]
                lines.append(f"{idx}. {hero['name']}，综合分 {item['score']}")
                for reason in item["reasons"]:
                    lines.append(f"   - {reason}")
        else:
            lines.append("- 暂无推荐。请补充敌方英雄或检查网络数据源。")

        lines.append("\n### 打法建议")
        for item in advice:
            lines.append(f"- {item}")

        lines.append("\n### 实战样本与个人理解")
        if playbook:
            for entry in playbook[:4]:
                source = entry.get("source") or entry.get("source_type") or "playbook"
                lines.append(f"- {entry['title']}（{source}）")
                if entry.get("summary"):
                    lines.append(f"  - {entry['summary']}")
                for point in entry.get("points", [])[:2]:
                    lines.append(f"  - {point}")
        else:
            lines.append("- 当前没有命中的 playbook 样本。可以在 data/playbook.json 添加 match_id、英雄、位置和复盘结论。")

        return "\n".join(lines)
