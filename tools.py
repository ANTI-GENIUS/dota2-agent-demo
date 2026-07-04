from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


API_BASE = "https://api.opendota.com/api"


FALLBACK_HEROES: list[dict[str, Any]] = [
    {
        "id": 1,
        "name": "npc_dota_hero_antimage",
        "localized_name": "Anti-Mage",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": ["Carry", "Escape", "Nuker"],
        "pro_pick": 100,
        "pro_win": 51,
    },
    {
        "id": 2,
        "name": "npc_dota_hero_axe",
        "localized_name": "Axe",
        "primary_attr": "str",
        "attack_type": "Melee",
        "roles": ["Initiator", "Durable", "Disabler", "Jungler"],
        "pro_pick": 120,
        "pro_win": 63,
    },
    {
        "id": 5,
        "name": "npc_dota_hero_crystal_maiden",
        "localized_name": "Crystal Maiden",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": ["Support", "Disabler", "Nuker"],
        "pro_pick": 180,
        "pro_win": 90,
    },
    {
        "id": 8,
        "name": "npc_dota_hero_juggernaut",
        "localized_name": "Juggernaut",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": ["Carry", "Pusher", "Escape"],
        "pro_pick": 130,
        "pro_win": 67,
    },
    {
        "id": 11,
        "name": "npc_dota_hero_nevermore",
        "localized_name": "Shadow Fiend",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": ["Carry", "Nuker"],
        "pro_pick": 150,
        "pro_win": 78,
    },
    {
        "id": 22,
        "name": "npc_dota_hero_zuus",
        "localized_name": "Zeus",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": ["Nuker"],
        "pro_pick": 110,
        "pro_win": 55,
    },
    {
        "id": 26,
        "name": "npc_dota_hero_lion",
        "localized_name": "Lion",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": ["Support", "Disabler", "Nuker", "Initiator"],
        "pro_pick": 160,
        "pro_win": 82,
    },
    {
        "id": 35,
        "name": "npc_dota_hero_sniper",
        "localized_name": "Sniper",
        "primary_attr": "agi",
        "attack_type": "Ranged",
        "roles": ["Carry", "Nuker"],
        "pro_pick": 100,
        "pro_win": 48,
    },
    {
        "id": 41,
        "name": "npc_dota_hero_faceless_void",
        "localized_name": "Faceless Void",
        "primary_attr": "agi",
        "attack_type": "Melee",
        "roles": ["Carry", "Initiator", "Disabler", "Escape", "Durable"],
        "pro_pick": 125,
        "pro_win": 64,
    },
    {
        "id": 86,
        "name": "npc_dota_hero_rubick",
        "localized_name": "Rubick",
        "primary_attr": "int",
        "attack_type": "Ranged",
        "roles": ["Support", "Disabler", "Nuker"],
        "pro_pick": 220,
        "pro_win": 108,
    },
]


CN_ALIASES = {
    "敌法": "Anti-Mage",
    "敌法师": "Anti-Mage",
    "斧王": "Axe",
    "冰女": "Crystal Maiden",
    "水晶室女": "Crystal Maiden",
    "剑圣": "Juggernaut",
    "影魔": "Shadow Fiend",
    "sf": "Shadow Fiend",
    "宙斯": "Zeus",
    "lion": "Lion",
    "莱恩": "Lion",
    "火女": "Lina",
    "lina": "Lina",
    "卡尔": "Invoker",
    "祈求者": "Invoker",
    "蓝猫": "Storm Spirit",
    "风暴之灵": "Storm Spirit",
    "火猫": "Ember Spirit",
    "灰烬之灵": "Ember Spirit",
    "紫猫": "Void Spirit",
    "虚无之灵": "Void Spirit",
    "白牛": "Spirit Breaker",
    "裂魂人": "Spirit Breaker",
    "小黑": "Drow Ranger",
    "卓尔游侠": "Drow Ranger",
    "小鱼": "Slark",
    "小鱼人": "Slark",
    "虚空": "Faceless Void",
    "虚空假面": "Faceless Void",
    "露娜": "Luna",
    "火枪": "Sniper",
    "狙击手": "Sniper",
    "拍拍": "Ursa",
    "拍拍熊": "Ursa",
    "猛犸": "Magnus",
    "马格纳斯": "Magnus",
    "拉比克": "Rubick",
    "蓝胖": "Ogre Magi",
    "海民": "Tusk",
    "军团": "Legion Commander",
    "船长": "Kunkka",
    "女王": "Queen of Pain",
    "痛苦女王": "Queen of Pain",
    "蓝杖": "Aghanim's Scepter",
}


HERO_CN_NAMES = {
    "Abaddon": "亚巴顿",
    "Alchemist": "炼金术士",
    "Ancient Apparition": "远古冰魄",
    "Anti-Mage": "敌法师",
    "Arc Warden": "天穹守望者",
    "Axe": "斧王",
    "Bane": "祸乱之源",
    "Batrider": "蝙蝠骑士",
    "Beastmaster": "兽王",
    "Bloodseeker": "血魔",
    "Bounty Hunter": "赏金猎人",
    "Brewmaster": "酒仙",
    "Bristleback": "钢背兽",
    "Broodmother": "育母蜘蛛",
    "Centaur Warrunner": "半人马战行者",
    "Chaos Knight": "混沌骑士",
    "Chen": "陈",
    "Clinkz": "克林克兹",
    "Clockwerk": "发条技师",
    "Crystal Maiden": "水晶室女",
    "Dark Seer": "黑暗贤者",
    "Dark Willow": "邪影芳灵",
    "Dawnbreaker": "破晓辰星",
    "Dazzle": "戴泽",
    "Death Prophet": "死亡先知",
    "Disruptor": "干扰者",
    "Doom": "末日使者",
    "Dragon Knight": "龙骑士",
    "Drow Ranger": "卓尔游侠",
    "Earth Spirit": "大地之灵",
    "Earthshaker": "撼地者",
    "Elder Titan": "上古巨神",
    "Ember Spirit": "灰烬之灵",
    "Enchantress": "魅惑魔女",
    "Enigma": "谜团",
    "Faceless Void": "虚空假面",
    "Grimstroke": "天涯墨客",
    "Gyrocopter": "矮人直升机",
    "Hoodwink": "森海飞霞",
    "Huskar": "哈斯卡",
    "Invoker": "祈求者",
    "Io": "艾欧",
    "Jakiro": "杰奇洛",
    "Juggernaut": "主宰",
    "Keeper of the Light": "光之守卫",
    "Kez": "凯兹",
    "Kunkka": "昆卡",
    "Largo": "拉戈",
    "Legion Commander": "军团指挥官",
    "Leshrac": "拉席克",
    "Lich": "巫妖",
    "Lifestealer": "噬魂鬼",
    "Lina": "莉娜",
    "Lion": "莱恩",
    "Lone Druid": "德鲁伊",
    "Luna": "露娜",
    "Lycan": "狼人",
    "Magnus": "马格纳斯",
    "Marci": "玛西",
    "Mars": "玛尔斯",
    "Medusa": "美杜莎",
    "Meepo": "米波",
    "Mirana": "米拉娜",
    "Monkey King": "齐天大圣",
    "Morphling": "变体精灵",
    "Muerta": "琼英碧灵",
    "Naga Siren": "娜迦海妖",
    "Nature's Prophet": "先知",
    "Necrophos": "瘟疫法师",
    "Night Stalker": "暗夜魔王",
    "Nyx Assassin": "司夜刺客",
    "Ogre Magi": "食人魔魔法师",
    "Omniknight": "全能骑士",
    "Oracle": "神谕者",
    "Outworld Devourer": "殁境神蚀者",
    "Pangolier": "石鳞剑士",
    "Phantom Assassin": "幻影刺客",
    "Phantom Lancer": "幻影长矛手",
    "Phoenix": "凤凰",
    "Primal Beast": "原初兽",
    "Puck": "帕克",
    "Pudge": "帕吉",
    "Pugna": "帕格纳",
    "Queen of Pain": "痛苦女王",
    "Razor": "剃刀",
    "Riki": "力丸",
    "Ring Master": "百戏大王",
    "Rubick": "拉比克",
    "Sand King": "沙王",
    "Shadow Demon": "暗影恶魔",
    "Shadow Fiend": "影魔",
    "Shadow Shaman": "暗影萨满",
    "Silencer": "沉默术士",
    "Skywrath Mage": "天怒法师",
    "Slardar": "斯拉达",
    "Slark": "斯拉克",
    "Snapfire": "电炎绝手",
    "Sniper": "狙击手",
    "Spectre": "幽鬼",
    "Spirit Breaker": "裂魂人",
    "Storm Spirit": "风暴之灵",
    "Sven": "斯温",
    "Techies": "工程师",
    "Templar Assassin": "圣堂刺客",
    "Terrorblade": "恐怖利刃",
    "Tidehunter": "潮汐猎人",
    "Timbersaw": "伐木机",
    "Tinker": "修补匠",
    "Tiny": "小小",
    "Treant Protector": "树精卫士",
    "Troll Warlord": "巨魔战将",
    "Tusk": "巨牙海民",
    "Underlord": "孽主",
    "Undying": "不朽尸王",
    "Ursa": "熊战士",
    "Vengeful Spirit": "复仇之魂",
    "Venomancer": "剧毒术士",
    "Viper": "冥界亚龙",
    "Visage": "维萨吉",
    "Void Spirit": "虚无之灵",
    "Warlock": "术士",
    "Weaver": "编织者",
    "Windranger": "风行者",
    "Winter Wyvern": "寒冬飞龙",
    "Witch Doctor": "巫医",
    "Wraith King": "冥魂大帝",
    "Zeus": "宙斯",
}


ROLE_PREFERENCE = {
    "carry": ["Carry", "Escape", "Pusher"],
    "mid": ["Nuker", "Carry", "Escape", "Disabler"],
    "offlane": ["Initiator", "Durable", "Disabler"],
    "soft_support": ["Support", "Disabler", "Nuker", "Initiator"],
    "hard_support": ["Support", "Disabler"],
    "flexible": [],
}


ROLE_CN_NAMES = {
    "Carry": "核心",
    "Support": "辅助",
    "Nuker": "爆发",
    "Disabler": "控制",
    "Jungler": "打野",
    "Durable": "耐久",
    "Escape": "逃生",
    "Pusher": "推进",
    "Initiator": "先手",
}


ATTACK_TYPE_CN_NAMES = {
    "Melee": "近战",
    "Ranged": "远程",
}


ITEM_NAME_TO_KEY = {
    "树之祭祀": "tango",
    "治疗药膏": "flask",
    "仙灵火": "faerie_fire",
    "铁树枝干": "branches",
    "圆环": "circlet",
    "敏捷便鞋": "slippers",
    "力量手套": "gauntlets",
    "智力斗篷": "mantle",
    "系带": "wraith_band",
    "护腕": "bracer",
    "空灵挂件": "null_talisman",
    "魔瓶": "bottle",
    "魔棒": "magic_wand",
    "魔杖": "magic_wand",
    "鞋子": "boots",
    "速度之靴": "boots",
    "凝魂之露": "infused_raindrop",
    "风灵之纹": "wind_lace",
    "加速手套": "gloves",
    "黑皇杖": "black_king_bar",
    "林肯法球": "sphere",
    "莲花宝珠": "lotus_orb",
    "漩涡": "maelstrom",
    "相位鞋": "phase_boots",
    "动力鞋": "power_treads",
    "假腿": "power_treads",
    "阿哈利姆神杖": "ultimate_scepter",
    "蓝杖": "ultimate_scepter",
    "阿哈利姆魔晶": "aghanims_shard",
    "魔晶": "aghanims_shard",
    "代达罗斯之殇": "greater_crit",
    "大炮": "greater_crit",
    "希瓦的守护": "shivas_guard",
    "冰甲": "shivas_guard",
    "金箍棒": "monkey_king_bar",
    "跳刀": "blink",
    "闪烁匕首": "blink",
    "风杖": "cyclone",
    "原力法杖": "force_staff",
    "推推棒": "force_staff",
    "洞察烟斗": "pipe",
    "微光披风": "glimmer_cape",
    "黯灭": "desolator",
    "强袭": "assault",
    "强袭胸甲": "assault",
    "斯嘉蒂之眼": "skadi",
    "冰眼": "skadi",
    "否决坠饰": "nullifier",
    "补刀斧": "quelling_blade",
    "血榴弹": "blood_grenade",
    "侦查守卫": "ward_observer",
    "假眼": "ward_observer",
    "岗哨守卫": "ward_sentry",
    "真眼": "ward_sentry",
    "芒果": "enchanted_mango",
    "魔法芒果": "enchanted_mango",
    "小净化": "clarity",
    "净化药水": "clarity",
    "先锋盾": "vanguard",
    "魂戒": "soul_ring",
    "刃甲": "blade_mail",
    "赤红甲": "crimson_guard",
    "奥术鞋": "arcane_boots",
    "静谧之鞋": "tranquil_boots",
    "以太透镜": "aether_lens",
    "炎阳纹章": "solar_crest",
    "飓风长戟": "hurricane_pike",
    "隐刀": "invis_sword",
    "蝴蝶": "butterfly",
    "撒旦之邪力": "satanic",
    "深渊之刃": "abyssal_blade",
    "狂战斧": "bfury",
    "狂战": "bfury",
    "分身斧": "manta",
    "散夜对剑": "sange_and_yasha",
    "魔龙枪": "dragon_lance",
    "烟雾": "smoke_of_deceit",
    "诡计之雾": "smoke_of_deceit",
    "盘子": "aeon_disk",
    "永恒之盘": "aeon_disk",
}


GENERIC_ITEM_EXPANSIONS = {
    "属性小件": ["圆环", "铁树枝干"],
    "护腕配件": ["力量手套", "圆环"],
    "续航补给": ["树之祭祀", "治疗药膏"],
    "补给": ["树之祭祀", "治疗药膏"],
    "小件抗压装": ["魔棒", "凝魂之露"],
    "发育装": ["狂战斧", "漩涡"],
    "节奏装": ["魔瓶", "漩涡"],
    "机动装": ["跳刀", "飓风长戟"],
    "输出装": ["代达罗斯之殇", "金箍棒"],
    "输出大件": ["代达罗斯之殇", "金箍棒"],
    "团队装": ["洞察烟斗", "赤红甲"],
    "团队保护装": ["微光披风", "原力法杖"],
    "风灵之纹/加速手套类小件": ["风灵之纹", "加速手套"],
}


class OpenDotaClient:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_hero_stats(self) -> list[dict[str, Any]]:
        data = self._get_json("/heroStats", "hero_stats.json", ttl_seconds=12 * 3600)
        if isinstance(data, list) and data:
            return data
        return FALLBACK_HEROES

    def get_matchups(self, hero_id: int) -> list[dict[str, Any]]:
        data = self._get_json(
            f"/heroes/{hero_id}/matchups",
            f"matchups_{hero_id}.json",
            ttl_seconds=7 * 24 * 3600,
        )
        if isinstance(data, list):
            return data
        return []

    def get_item_constants(self) -> dict[str, Any]:
        data = self._get_json("/constants/items", "items.json", ttl_seconds=7 * 24 * 3600)
        if isinstance(data, dict):
            return data
        return {}

    def _get_json(self, path: str, cache_name: str, ttl_seconds: int) -> Any:
        cache_path = self.cache_dir / cache_name
        cached = self._read_cache(cache_path)
        if cached is not None and time.time() - cache_path.stat().st_mtime < ttl_seconds:
            return cached

        url = f"{API_BASE}{path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "dota2-agent-demo/1.0"})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
            cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return data
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if cached is not None:
                return cached
            return None

    @staticmethod
    def _read_cache(path: Path) -> Any:
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None


def normalize_name(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("npc_dota_hero_", "")
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", value)
    return value


def build_hero_index(heroes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    by_english = {hero.get("localized_name", ""): hero for hero in heroes}

    for hero in heroes:
        localized = hero.get("localized_name", "")
        internal = hero.get("name", "")
        if localized:
            index[normalize_name(localized)] = hero
            cn_name = HERO_CN_NAMES.get(localized)
            if cn_name:
                index[normalize_name(cn_name)] = hero
        if internal:
            index[normalize_name(internal)] = hero
        if localized:
            parts = localized.split()
            if len(parts) > 1:
                index[normalize_name("".join(parts))] = hero

    for alias, english_name in CN_ALIASES.items():
        hero = by_english.get(english_name)
        if hero:
            index[normalize_name(alias)] = hero

    return index


def parse_hero_names(raw: str, hero_index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    if not raw:
        return []

    chunks = re.split(r"[,，、/|;；\n]+", raw)
    found: list[dict[str, Any]] = []
    seen_ids: set[int] = set()

    for chunk in chunks:
        key = normalize_name(chunk)
        if not key:
            continue
        hero = hero_index.get(key)
        if not hero:
            hero = fuzzy_match_hero(key, hero_index)
        if hero and hero.get("id") not in seen_ids:
            found.append(hero)
            seen_ids.add(hero["id"])

    return found


def fuzzy_match_hero(key: str, hero_index: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    if len(key) < 3:
        return None
    for alias, hero in hero_index.items():
        if key in alias or alias in key:
            return hero
    return None


def estimate_win_rate(hero: dict[str, Any]) -> tuple[float | None, str]:
    pro_pick = int(hero.get("pro_pick") or 0)
    pro_win = int(hero.get("pro_win") or 0)
    if pro_pick >= 20:
        return pro_win / pro_pick, "pro"

    wins = 0
    picks = 0
    for i in range(1, 9):
        wins += int(hero.get(f"{i}_win") or 0)
        picks += int(hero.get(f"{i}_pick") or 0)
    if picks > 0:
        return wins / picks, "ranked"
    return None, "unknown"


def display_hero_name(hero: dict[str, Any] | None) -> str:
    if not hero:
        return "未知英雄"
    english_name = str(hero.get("localized_name") or "")
    return HERO_CN_NAMES.get(english_name, english_name)


def display_role_name(role: str) -> str:
    return ROLE_CN_NAMES.get(role, role)


def display_attack_type(attack_type: str | None) -> str:
    if not attack_type:
        return "未知"
    return ATTACK_TYPE_CN_NAMES.get(attack_type, attack_type)


def hero_display(hero: dict[str, Any]) -> dict[str, Any]:
    win_rate, source = estimate_win_rate(hero)
    img = hero.get("img") or ""
    icon = hero.get("icon") or ""
    cdn = "https://cdn.cloudflare.steamstatic.com"
    return {
        "id": hero.get("id"),
        "name": display_hero_name(hero),
        "english_name": hero.get("localized_name"),
        "image": f"{cdn}{img}" if img.startswith("/") else img,
        "icon": f"{cdn}{icon}" if icon.startswith("/") else icon,
        "primary_attr": hero.get("primary_attr"),
        "attack_type": display_attack_type(hero.get("attack_type")),
        "roles": [display_role_name(role) for role in hero.get("roles", [])],
        "win_rate": round(win_rate * 100, 1) if win_rate is not None else None,
        "win_rate_source": source,
        "pro_pick": int(hero.get("pro_pick") or 0),
    }


def analyze_role_balance(allies: list[dict[str, Any]]) -> dict[str, Any]:
    role_count: dict[str, int] = {}
    attr_count: dict[str, int] = {}
    attack_count: dict[str, int] = {}

    for hero in allies:
        for role in hero.get("roles", []):
            role_count[role] = role_count.get(role, 0) + 1
        attr = hero.get("primary_attr") or "unknown"
        attr_count[attr] = attr_count.get(attr, 0) + 1
        attack = hero.get("attack_type") or "unknown"
        attack_count[attack] = attack_count.get(attack, 0) + 1

    risks: list[str] = []
    if allies and role_count.get("Disabler", 0) == 0:
        risks.append("控制不足：阵容缺少稳定先手/反手，团战容易留不住人。")
    if allies and role_count.get("Initiator", 0) == 0:
        risks.append("开团不足：需要补能主动开视野、先手或逼团的英雄。")
    if allies and role_count.get("Support", 0) == 0 and len(allies) >= 3:
        risks.append("辅助属性不足：如果已经选了多个核心，后续要补视野、保护和控制。")
    if allies and role_count.get("Carry", 0) >= 3:
        risks.append("经济点过多：多个吃资源核心会压缩发育空间。")
    if allies and attack_count.get("Melee", 0) >= 4:
        risks.append("近战过多：容易被拉扯，建议补远程消耗或稳定控制。")
    if not risks:
        risks.append("当前阵容没有明显结构性短板，重点看对线强度和敌方克制。")

    return {
        "role_count": role_count,
        "attr_count": attr_count,
        "attack_count": attack_count,
        "risks": risks,
    }


def matchup_counter_scores(
    client: OpenDotaClient,
    heroes: list[dict[str, Any]],
    enemies: list[dict[str, Any]],
    excluded_ids: set[int],
) -> dict[int, dict[str, Any]]:
    hero_by_id = {int(hero["id"]): hero for hero in heroes if hero.get("id") is not None}
    scores: dict[int, dict[str, Any]] = {}

    for enemy in enemies:
        enemy_id = int(enemy["id"])
        enemy_name = display_hero_name(enemy)
        for row in client.get_matchups(enemy_id):
            candidate_id = int(row.get("hero_id") or 0)
            games = int(row.get("games_played") or 0)
            wins = int(row.get("wins") or 0)
            if candidate_id in excluded_ids or candidate_id not in hero_by_id or games < 30:
                continue

            enemy_win_rate = wins / games if games else 0.5
            candidate_counter_rate = 1 - enemy_win_rate
            entry = scores.setdefault(
                candidate_id,
                {
                    "hero": hero_by_id[candidate_id],
                    "matchup_rates": [],
                    "details": [],
                    "games": 0,
                },
            )
            entry["matchup_rates"].append(candidate_counter_rate)
            entry["details"].append(
                {
                    "enemy": enemy_name,
                    "counter_win_rate": round(candidate_counter_rate * 100, 1),
                    "games": games,
                }
            )
            entry["games"] += games

    for entry in scores.values():
        rates = entry["matchup_rates"]
        entry["counter_score"] = sum(rates) / len(rates) if rates else 0.5

    return scores


def recommend_heroes(
    client: OpenDotaClient,
    heroes: list[dict[str, Any]],
    allies: list[dict[str, Any]],
    enemies: list[dict[str, Any]],
    desired_role: str,
    limit: int = 6,
) -> list[dict[str, Any]]:
    excluded_ids = {int(hero["id"]) for hero in allies + enemies if hero.get("id") is not None}
    role_targets = ROLE_PREFERENCE.get(desired_role, [])
    counter_scores = matchup_counter_scores(client, heroes, enemies, excluded_ids) if enemies else {}

    candidates: list[dict[str, Any]] = []
    for hero in heroes:
        hero_id = int(hero.get("id") or 0)
        if not hero_id or hero_id in excluded_ids:
            continue

        win_rate, win_source = estimate_win_rate(hero)
        win_component = win_rate if win_rate is not None else 0.5
        roles = hero.get("roles", [])
        role_component = 0.0
        if role_targets:
            role_hits = len(set(roles).intersection(role_targets))
            role_component = min(role_hits / max(len(role_targets), 1), 1.0)
        else:
            role_component = 0.45

        counter_entry = counter_scores.get(hero_id)
        counter_component = counter_entry["counter_score"] if counter_entry else 0.5
        pro_pick = int(hero.get("pro_pick") or 0)
        popularity_component = min(pro_pick / 300, 1.0)

        score = (
            counter_component * 0.45
            + role_component * 0.25
            + win_component * 0.2
            + popularity_component * 0.1
        )

        reasons = []
        if counter_entry:
            best = sorted(counter_entry["details"], key=lambda x: x["counter_win_rate"], reverse=True)[:2]
            reason_text = "，".join(
                f"对 {item['enemy']} 约 {item['counter_win_rate']}% 胜率"
                for item in best
            )
            reasons.append(reason_text)
        if role_targets and set(roles).intersection(role_targets):
            matched_roles = [display_role_name(role) for role in set(roles).intersection(role_targets)]
            reasons.append(f"符合位置偏好：{', '.join(matched_roles)}")
        if win_rate is not None:
            reasons.append(f"{win_source} 样本胜率约 {round(win_rate * 100, 1)}%")

        candidates.append(
            {
                "hero": hero_display(hero),
                "score": round(score * 100, 1),
                "reasons": reasons[:3] or ["数据不足，作为备选英雄，需要结合熟练度判断。"],
                "matchups": counter_entry["details"][:4] if counter_entry else [],
            }
        )

    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates[:limit]


def generate_advice(
    allies: list[dict[str, Any]],
    enemies: list[dict[str, Any]],
    desired_role: str,
    balance: dict[str, Any],
) -> list[str]:
    enemy_roles = {}
    for enemy in enemies:
        for role in enemy.get("roles", []):
            enemy_roles[role] = enemy_roles.get(role, 0) + 1

    advice: list[str] = []
    if enemy_roles.get("Disabler", 0) >= 2:
        advice.append("敌方控制多：核心位优先考虑 BKB、分身/林肯等解控或防先手装备。")
    if enemy_roles.get("Nuker", 0) >= 2:
        advice.append("敌方法术爆发高：辅助位考虑微光、笛子、莲花，核心位注意魔抗和切入时机。")
    if enemy_roles.get("Durable", 0) >= 2:
        advice.append("敌方前排厚：需要破甲、百分比伤害、持续输出，避免只堆一次性爆发。")
    if balance["role_count"].get("Initiator", 0) == 0:
        advice.append("己方缺先手：补英雄时优先看开团能力，打法上要依赖视野和反打。")
    if desired_role in {"soft_support", "hard_support"}:
        advice.append("辅助 Agent 建议：前 10 分钟重点服务强势路，提前布置河道/三角区视野，避免只跟着大哥挂机。")
    if desired_role == "mid":
        advice.append("中单 Agent 建议：关注 6/8/10 分钟符点和边路击杀窗口，英雄选择要能带节奏或守塔。")
    if desired_role == "carry":
        advice.append("一号位 Agent 建议：如果阵容前中期弱，优先选自保和清线能力强的核心，别只看后期上限。")
    if not advice:
        advice.append("当前信息不足以给出强约束建议，优先补控制、视野、清线和一名稳定输出点。")
    return advice


def generate_item_advice(
    client: OpenDotaClient,
    allies: list[dict[str, Any]],
    enemies: list[dict[str, Any]],
    desired_role: str,
    question: str = "",
) -> dict[str, Any]:
    focus_hero = allies[0] if allies else None
    focus_name = focus_hero.get("localized_name", "") if focus_hero else ""
    enemy_names = {enemy.get("localized_name", "") for enemy in enemies}
    enemy_roles: dict[str, int] = {}
    for enemy in enemies:
        for role in enemy.get("roles", []):
            enemy_roles[role] = enemy_roles.get(role, 0) + 1

    build = base_item_plan(desired_role)
    notes: list[str] = []
    lane_notes: list[str] = []
    avoid: list[str] = []

    if focus_name:
        hero_plan = hero_item_plan(focus_name, desired_role)
        for key in ["starting", "lane", "core", "situational"]:
            if hero_plan.get(key):
                build[key] = merge_unique(hero_plan[key], build.get(key, []))
        notes.extend(hero_plan.get("notes", []))
        avoid.extend(hero_plan.get("avoid", []))

    if enemy_roles.get("Nuker", 0) >= 1:
        build["lane"] = merge_unique(["凝魂之露", "魔棒"], build["lane"])
        build["situational"] = merge_unique(["黑皇杖", "洞察烟斗/微光披风"], build["situational"])
        lane_notes.append("敌方法术消耗明显，对线期优先补凝魂之露和魔棒，先保证不被一套压出经验区。")
    if enemy_roles.get("Disabler", 0) >= 1:
        build["situational"] = merge_unique(["黑皇杖", "林肯法球", "莲花宝珠"], build["situational"])
        notes.append("敌方有稳定控制时，核心位不要把 BKB/林肯拖得太晚。")
    if enemy_roles.get("Durable", 0) >= 2:
        build["situational"] = merge_unique(["黯灭/强袭", "斯嘉蒂之眼", "否决坠饰"], build["situational"])
        notes.append("敌方前排多时，装备要补持续输出或破甲，避免只做一次性爆发。")
    if enemy_names.intersection({"Shadow Fiend", "Sniper", "Drow Ranger", "Lina"}):
        build["lane"] = merge_unique(["鞋子", "风灵之纹/加速手套类小件"], build["lane"])
        build["situational"] = merge_unique(["跳刀", "风杖/推推棒", "黑皇杖"], build["situational"])
        lane_notes.append("面对长手高爆发英雄，核心是先活住和抢符，不要为了贪刀连续吃满技能。")

    if focus_name == "Ember Spirit" and "Shadow Fiend" in enemy_names:
        build["starting"] = ["树之祭祀", "仙灵火", "铁树枝干", "属性小件"]
        build["lane"] = ["魔瓶", "魔棒", "鞋子", "凝魂之露"]
        build["core"] = ["相位鞋/动力鞋", "漩涡", "黑皇杖", "阿哈利姆神杖/代达罗斯之殇"]
        build["situational"] = merge_unique(["林肯法球", "希瓦的守护", "金箍棒"], build["situational"])
        lane_notes.extend(
            [
                "火猫打影魔不要站在同一直线连续吃三炮，补刀优先用无影拳和残焰保血量。",
                "3 分钟后凝魂之露价值很高；如果被压，先鞋瓶魔棒稳住，不要裸憋大件。",
                "6 级后看边路和符点节奏，别在中路和影魔无限对刷让他安全叠魂。",
            ]
        )
        avoid.extend(["裸狂战/裸大电锤", "没 BKB 就强行先手进五个人"])

    if "对线" in question or "线期" in question:
        lane_notes.append("你的问题偏对线期，所以优先看小件、补给、抗压和符点节奏，不要只看六神装。")

    item_constants = client.get_item_constants()
    starting = build_item_icons(build["starting"], item_constants, limit=6)
    lane = build_item_icons(build["lane"], item_constants, limit=6)
    core = build_item_icons(build["core"], item_constants, limit=6)
    situational = build_item_icons(build["situational"], item_constants, limit=8)

    return {
        "focus_hero": display_hero_name(focus_hero) if focus_hero else "未指定",
        "focus_hero_english": focus_name or "",
        "role": desired_role,
        "starting": starting,
        "lane": lane,
        "core": core,
        "situational": situational,
        "lane_notes": merge_unique(lane_notes, notes)[:6],
        "avoid": merge_unique(avoid, default_avoid_items(desired_role))[:5],
        "data_level": "rule_based",
    }


def base_item_plan(desired_role: str) -> dict[str, list[str]]:
    plans = {
        "carry": {
            "starting": ["补刀斧", "树之祭祀", "敏捷便鞋/力量手套", "铁树枝干"],
            "lane": ["魔棒", "系带/护腕", "鞋子", "续航补给"],
            "core": ["发育装", "黑皇杖", "分身斧/散夜对剑", "输出大件"],
            "situational": ["林肯法球", "蝴蝶", "撒旦之邪力", "深渊之刃"],
        },
        "mid": {
            "starting": ["树之祭祀", "仙灵火", "铁树枝干", "属性小件"],
            "lane": ["魔瓶", "魔棒", "鞋子", "凝魂之露"],
            "core": ["节奏装", "黑皇杖", "机动装", "输出装"],
            "situational": ["林肯法球", "风杖", "跳刀", "否决坠饰"],
        },
        "offlane": {
            "starting": ["补刀斧", "树之祭祀", "护腕配件", "铁树枝干"],
            "lane": ["魔棒", "护腕", "鞋子", "先锋盾/魂戒"],
            "core": ["跳刀", "刃甲", "黑皇杖", "团队装"],
            "situational": ["赤红甲", "洞察烟斗", "莲花宝珠", "希瓦的守护"],
        },
        "soft_support": {
            "starting": ["侦查守卫", "岗哨守卫", "血榴弹", "树之祭祀", "芒果"],
            "lane": ["魔棒", "速度之靴", "风灵之纹", "小净化"],
            "core": ["奥术鞋/静谧之鞋", "微光披风", "原力法杖", "以太透镜"],
            "situational": ["跳刀", "莲花宝珠", "炎阳纹章", "黑皇杖"],
        },
        "hard_support": {
            "starting": ["侦查守卫", "岗哨守卫", "血榴弹", "树之祭祀", "芒果"],
            "lane": ["魔棒", "速度之靴", "补给", "烟雾"],
            "core": ["静谧之鞋/奥术鞋", "微光披风", "原力法杖", "团队保护装"],
            "situational": ["莲花宝珠", "洞察烟斗", "盘子", "跳刀"],
        },
    }
    return plans.get(
        desired_role,
        {
            "starting": ["树之祭祀", "铁树枝干", "属性小件", "补给"],
            "lane": ["魔棒", "鞋子", "小件抗压装"],
            "core": ["黑皇杖", "机动装", "输出/团队装"],
            "situational": ["林肯法球", "莲花宝珠", "微光披风", "原力法杖"],
        },
    )


def hero_item_plan(hero_name: str, desired_role: str) -> dict[str, list[str]]:
    plans = {
        "Ember Spirit": {
            "starting": ["树之祭祀", "仙灵火", "铁树枝干", "属性小件"],
            "lane": ["魔瓶", "魔棒", "鞋子", "凝魂之露"],
            "core": ["相位鞋/动力鞋", "漩涡", "黑皇杖", "阿哈利姆神杖"],
            "situational": ["代达罗斯之殇", "希瓦的守护", "林肯法球", "金箍棒"],
            "notes": ["火猫优先保证节奏和进场安全，BKB 时机通常比纯输出大件更关键。"],
            "avoid": ["只刷不动边路", "没有保命装就先手冲后排"],
        },
        "Shadow Fiend": {
            "starting": ["树之祭祀", "仙灵火", "铁树枝干", "属性小件"],
            "lane": ["魔瓶", "魔棒", "鞋子", "系带"],
            "core": ["动力鞋", "黑皇杖", "飓风长戟/隐刀", "输出大件"],
            "situational": ["蝴蝶", "撒旦之邪力", "代达罗斯之殇", "金箍棒"],
            "notes": ["影魔怕被先手，BKB 和站位优先级很高。"],
            "avoid": ["魂少时强接团", "被抓多还继续裸输出"],
        },
        "Axe": {
            "lane": ["魔棒", "先锋盾", "速度之靴"],
            "core": ["跳刀", "刃甲", "黑皇杖"],
            "situational": ["希瓦的守护", "莲花宝珠", "赤红甲"],
            "notes": ["斧王装备核心是跳刀时机，太晚会失去主动权。"],
        },
        "Lion": {
            "lane": ["魔棒", "速度之靴", "小净化"],
            "core": ["静谧之鞋/奥术鞋", "跳刀", "以太透镜"],
            "situational": ["微光披风", "原力法杖", "阿哈利姆魔晶"],
            "notes": ["莱恩不要只憋跳，劣势局先做保命和视野装。"],
        },
        "Juggernaut": {
            "lane": ["魔棒", "系带", "鞋子"],
            "core": ["相位鞋", "漩涡/狂战斧", "分身斧", "黑皇杖"],
            "situational": ["蝴蝶", "深渊之刃", "斯嘉蒂之眼", "金箍棒"],
            "notes": ["剑圣要根据局势选发育装，劣势不要贪慢速大件。"],
        },
        "Sniper": {
            "lane": ["系带", "鞋子", "魔棒"],
            "core": ["动力鞋", "魔龙枪", "漩涡", "黑皇杖"],
            "situational": ["飓风长戟", "撒旦之邪力", "金箍棒", "蝴蝶"],
            "notes": ["火枪最怕被切，长戟/BKB 的优先级经常高于纯输出。"],
        },
        "Crystal Maiden": {
            "lane": ["魔棒", "速度之靴", "补给"],
            "core": ["静谧之鞋", "微光披风", "原力法杖"],
            "situational": ["跳刀", "黑皇杖", "阿哈利姆魔晶"],
            "notes": ["冰女装备以活着放技能和救人为核心，不要过早追求大件。"],
        },
    }
    plan = plans.get(hero_name, {})
    if desired_role in {"soft_support", "hard_support"} and hero_name not in plans:
        plan = {
            "notes": ["辅助位出装优先级是视野、保人、救自己，其次才是贪功能大件。"],
            "avoid": ["裸大件不买眼", "没有保命装就站位过深"],
        }
    return plan


def default_avoid_items(desired_role: str) -> list[str]:
    if desired_role in {"soft_support", "hard_support"}:
        return ["裸大件不补眼", "劣势局跳过微光/推推"]
    if desired_role == "mid":
        return ["对线崩了还裸贪输出", "没有 BKB/林肯就硬冲控制阵容"]
    if desired_role == "carry":
        return ["无视敌方控制只做输出", "该参战时继续刷野"]
    return ["只看固定攻略，不根据敌方控制和爆发调整"]


def merge_unique(primary: list[str], secondary: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in primary + secondary:
        if item and item not in seen:
            result.append(item)
            seen.add(item)
    return result


def build_item_icons(
    raw_items: list[str],
    item_constants: dict[str, Any],
    limit: int,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw_item in raw_items:
        for item_name in expand_item_name(raw_item):
            key = ITEM_NAME_TO_KEY.get(item_name)
            if not key or key in seen:
                continue
            seen.add(key)
            items.append(item_icon_payload(item_name, key, item_constants))
            if len(items) >= limit:
                return items
    return items


def expand_item_name(raw_item: str) -> list[str]:
    if raw_item in GENERIC_ITEM_EXPANSIONS:
        return GENERIC_ITEM_EXPANSIONS[raw_item]

    result: list[str] = []
    for part in re.split(r"[/／、]", raw_item):
        item_name = part.strip()
        item_name = re.sub(r"^(裸|先出|补)", "", item_name)
        if item_name in GENERIC_ITEM_EXPANSIONS:
            result.extend(GENERIC_ITEM_EXPANSIONS[item_name])
        else:
            result.append(item_name)
    return [item for item in result if item]


def item_icon_payload(item_name: str, item_key: str, item_constants: dict[str, Any]) -> dict[str, Any]:
    cdn = "https://cdn.cloudflare.steamstatic.com"
    item_data = item_constants.get(item_key, {}) if isinstance(item_constants, dict) else {}
    image_path = item_data.get("img") or f"/apps/dota2/images/dota_react/items/{item_key}.png"
    icon_url = f"{cdn}{image_path}" if str(image_path).startswith("/") else str(image_path)
    return {
        "name": item_name,
        "key": item_key,
        "english_name": item_data.get("dname") or item_key,
        "icon": icon_url,
    }
