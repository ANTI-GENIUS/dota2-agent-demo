const form = document.querySelector("#agent-form");
const sampleButton = document.querySelector("#sample-button");
const emptyState = document.querySelector("#empty-state");
const loadingState = document.querySelector("#loading-state");
const result = document.querySelector("#result");
const allyCount = document.querySelector("#ally-count");
const enemyCount = document.querySelector("#enemy-count");
const recommendCount = document.querySelector("#recommend-count");
const recommendations = document.querySelector("#recommendations");
const itemBuild = document.querySelector("#item-build");
const risks = document.querySelector("#risks");
const answer = document.querySelector("#answer");

const CDN = "https://cdn.cloudflare.steamstatic.com";

const HERO_CN_NAMES = {
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
};

const CN_ALIASES = {
  "敌法": "Anti-Mage",
  "敌法师": "Anti-Mage",
  "斧王": "Axe",
  "冰女": "Crystal Maiden",
  "水晶室女": "Crystal Maiden",
  "剑圣": "Juggernaut",
  "主宰": "Juggernaut",
  "影魔": "Shadow Fiend",
  "sf": "Shadow Fiend",
  "宙斯": "Zeus",
  "莱恩": "Lion",
  "lion": "Lion",
  "火女": "Lina",
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
};

const ROLE_PREFERENCE = {
  carry: ["Carry", "Escape", "Pusher"],
  mid: ["Nuker", "Carry", "Escape", "Disabler"],
  offlane: ["Initiator", "Durable", "Disabler"],
  soft_support: ["Support", "Disabler", "Nuker", "Initiator"],
  hard_support: ["Support", "Disabler"],
  flexible: [],
};

const ROLE_CN_NAMES = {
  Carry: "核心",
  Support: "辅助",
  Nuker: "爆发",
  Disabler: "控制",
  Jungler: "打野",
  Durable: "耐久",
  Escape: "逃生",
  Pusher: "推进",
  Initiator: "先手",
};

const ATTACK_TYPE_CN_NAMES = {
  Melee: "近战",
  Ranged: "远程",
};

const ITEM_NAME_TO_KEY = {
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
  "阿哈利姆神杖": "ultimate_scepter",
  "阿哈利姆魔晶": "aghanims_shard",
  "代达罗斯之殇": "greater_crit",
  "希瓦的守护": "shivas_guard",
  "金箍棒": "monkey_king_bar",
  "跳刀": "blink",
  "风杖": "cyclone",
  "原力法杖": "force_staff",
  "推推棒": "force_staff",
  "洞察烟斗": "pipe",
  "微光披风": "glimmer_cape",
  "黯灭": "desolator",
  "强袭": "assault",
  "斯嘉蒂之眼": "skadi",
  "否决坠饰": "nullifier",
  "补刀斧": "quelling_blade",
  "血榴弹": "blood_grenade",
  "侦查守卫": "ward_observer",
  "岗哨守卫": "ward_sentry",
  "芒果": "enchanted_mango",
  "小净化": "clarity",
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
  "分身斧": "manta",
  "散夜对剑": "sange_and_yasha",
  "魔龙枪": "dragon_lance",
  "烟雾": "smoke_of_deceit",
  "盘子": "aeon_disk",
};

const GENERIC_ITEM_EXPANSIONS = {
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
};

let appDataPromise = null;
const matchupCache = new Map();

sampleButton.addEventListener("click", () => {
  form.elements.allies.value = "Axe, Lion, 剑圣";
  form.elements.enemies.value = "影魔, Sniper, Crystal Maiden";
  form.elements.role.value = "offlane";
  form.elements.question.value = "这把我该补什么英雄，团战怎么打？";
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    allies: form.elements.allies.value,
    enemies: form.elements.enemies.value,
    role: form.elements.role.value,
    question: form.elements.question.value,
  };

  setLoading(true);
  try {
    const data = await runAgent(payload);
    renderResult(data);
  } catch (error) {
    renderError(error);
  } finally {
    setLoading(false);
  }
});

async function loadAppData() {
  if (!appDataPromise) {
    appDataPromise = Promise.all([
      fetchJson("./data/hero_stats.json"),
      fetchJson("./data/items.json"),
    ]).then(([heroes, items]) => ({ heroes, items }));
  }
  return appDataPromise;
}

async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`无法加载数据文件：${path}`);
  }
  return response.json();
}

async function runAgent(payload) {
  const { heroes, items } = await loadAppData();
  const heroIndex = buildHeroIndex(heroes);
  const allies = parseHeroNames(payload.allies || "", heroIndex);
  const enemies = parseHeroNames(payload.enemies || "", heroIndex);
  const role = payload.role || "flexible";
  const balance = analyzeRoleBalance(allies);
  const recommendations = await recommendHeroes(heroes, allies, enemies, role);
  const itemAdvice = generateItemAdvice(items, allies, enemies, role, payload.question || "");
  const advice = generateAdvice(allies, enemies, role, balance);
  const answerMd = buildAnswer(allies, enemies, role, payload.question || "", balance, recommendations, advice);

  return {
    recognized: {
      allies: allies.map(heroDisplay),
      enemies: enemies.map(heroDisplay),
    },
    balance,
    recommendations,
    item_advice: itemAdvice,
    advice,
    answer_md: answerMd,
  };
}

function normalizeName(value) {
  return String(value)
    .toLowerCase()
    .trim()
    .replace("npc_dota_hero_", "")
    .replace(/[^a-z0-9\u4e00-\u9fff]+/g, "");
}

function buildHeroIndex(heroes) {
  const index = new Map();
  const byEnglish = new Map(heroes.map((hero) => [hero.localized_name, hero]));

  for (const hero of heroes) {
    if (hero.localized_name) {
      index.set(normalizeName(hero.localized_name), hero);
      index.set(normalizeName((HERO_CN_NAMES[hero.localized_name] || "")), hero);
      index.set(normalizeName(hero.localized_name.replaceAll(" ", "")), hero);
    }
    if (hero.name) index.set(normalizeName(hero.name), hero);
  }

  for (const [alias, englishName] of Object.entries(CN_ALIASES)) {
    const hero = byEnglish.get(englishName);
    if (hero) index.set(normalizeName(alias), hero);
  }
  return index;
}

function parseHeroNames(raw, heroIndex) {
  const chunks = String(raw).split(/[,，、/|;；\n]+/);
  const found = [];
  const seen = new Set();
  for (const chunk of chunks) {
    const key = normalizeName(chunk);
    if (!key) continue;
    let hero = heroIndex.get(key);
    if (!hero) hero = fuzzyMatchHero(key, heroIndex);
    if (hero && !seen.has(hero.id)) {
      found.push(hero);
      seen.add(hero.id);
    }
  }
  return found;
}

function fuzzyMatchHero(key, heroIndex) {
  if (key.length < 3) return null;
  for (const [alias, hero] of heroIndex.entries()) {
    if (key.includes(alias) || alias.includes(key)) return hero;
  }
  return null;
}

function displayHeroName(hero) {
  if (!hero) return "未知英雄";
  return HERO_CN_NAMES[hero.localized_name] || hero.localized_name || "未知英雄";
}

function displayRoleName(role) {
  return ROLE_CN_NAMES[role] || role;
}

function displayAttackType(type) {
  return ATTACK_TYPE_CN_NAMES[type] || type || "未知";
}

function estimateWinRate(hero) {
  const proPick = Number(hero.pro_pick || 0);
  const proWin = Number(hero.pro_win || 0);
  if (proPick >= 20) return { rate: proWin / proPick, source: "pro" };
  let wins = 0;
  let picks = 0;
  for (let i = 1; i <= 8; i += 1) {
    wins += Number(hero[`${i}_win`] || 0);
    picks += Number(hero[`${i}_pick`] || 0);
  }
  if (picks > 0) return { rate: wins / picks, source: "ranked" };
  return { rate: null, source: "unknown" };
}

function heroDisplay(hero) {
  const { rate, source } = estimateWinRate(hero);
  const image = hero.img?.startsWith("/") ? `${CDN}${hero.img}` : hero.img || "";
  const icon = hero.icon?.startsWith("/") ? `${CDN}${hero.icon}` : hero.icon || "";
  return {
    id: hero.id,
    name: displayHeroName(hero),
    english_name: hero.localized_name,
    image,
    icon,
    primary_attr: hero.primary_attr,
    attack_type: displayAttackType(hero.attack_type),
    roles: (hero.roles || []).map(displayRoleName),
    win_rate: rate == null ? null : Math.round(rate * 1000) / 10,
    win_rate_source: source,
    pro_pick: Number(hero.pro_pick || 0),
  };
}

function analyzeRoleBalance(allies) {
  const roleCount = {};
  const attrCount = {};
  const attackCount = {};
  for (const hero of allies) {
    for (const role of hero.roles || []) roleCount[role] = (roleCount[role] || 0) + 1;
    attrCount[hero.primary_attr || "unknown"] = (attrCount[hero.primary_attr || "unknown"] || 0) + 1;
    attackCount[hero.attack_type || "unknown"] = (attackCount[hero.attack_type || "unknown"] || 0) + 1;
  }
  const riskList = [];
  if (allies.length && !roleCount.Disabler) riskList.push("控制不足：阵容缺少稳定先手/反手，团战容易留不住人。");
  if (allies.length && !roleCount.Initiator) riskList.push("开团不足：需要补能主动开视野、先手或逼团的英雄。");
  if (allies.length >= 3 && !roleCount.Support) riskList.push("辅助属性不足：如果已经选了多个核心，后续要补视野、保护和控制。");
  if (allies.length && (roleCount.Carry || 0) >= 3) riskList.push("经济点过多：多个吃资源核心会压缩发育空间。");
  if (allies.length && (attackCount.Melee || 0) >= 4) riskList.push("近战过多：容易被拉扯，建议补远程消耗或稳定控制。");
  if (!riskList.length) riskList.push("当前阵容没有明显结构性短板，重点看对线强度和敌方克制。");
  return { role_count: roleCount, attr_count: attrCount, attack_count: attackCount, risks: riskList };
}

async function loadMatchups(heroId) {
  if (matchupCache.has(heroId)) return matchupCache.get(heroId);
  try {
    const rows = await fetchJson(`./data/matchups_${heroId}.json`);
    matchupCache.set(heroId, rows);
    return rows;
  } catch {
    matchupCache.set(heroId, []);
    return [];
  }
}

async function matchupCounterScores(heroes, enemies, excludedIds) {
  const heroById = new Map(heroes.map((hero) => [Number(hero.id), hero]));
  const scores = new Map();

  for (const enemy of enemies) {
    const rows = await loadMatchups(Number(enemy.id));
    for (const row of rows) {
      const candidateId = Number(row.hero_id || 0);
      const games = Number(row.games_played || 0);
      const wins = Number(row.wins || 0);
      if (excludedIds.has(candidateId) || !heroById.has(candidateId) || games < 30) continue;
      const candidateCounterRate = 1 - wins / games;
      if (!scores.has(candidateId)) {
        scores.set(candidateId, { hero: heroById.get(candidateId), rates: [], details: [] });
      }
      const entry = scores.get(candidateId);
      entry.rates.push(candidateCounterRate);
      entry.details.push({
        enemy: displayHeroName(enemy),
        counter_win_rate: Math.round(candidateCounterRate * 1000) / 10,
        games,
      });
    }
  }

  for (const entry of scores.values()) {
    entry.counter_score = entry.rates.reduce((sum, item) => sum + item, 0) / entry.rates.length;
  }
  return scores;
}

async function recommendHeroes(heroes, allies, enemies, desiredRole, limit = 6) {
  const excludedIds = new Set([...allies, ...enemies].map((hero) => Number(hero.id)));
  const roleTargets = ROLE_PREFERENCE[desiredRole] || [];
  const counterScores = await matchupCounterScores(heroes, enemies, excludedIds);
  const candidates = [];

  for (const hero of heroes) {
    const heroId = Number(hero.id || 0);
    if (!heroId || excludedIds.has(heroId)) continue;
    const { rate, source } = estimateWinRate(hero);
    const winComponent = rate == null ? 0.5 : rate;
    const roles = hero.roles || [];
    let roleComponent = 0.45;
    if (roleTargets.length) {
      const roleHits = roles.filter((role) => roleTargets.includes(role)).length;
      roleComponent = Math.min(roleHits / roleTargets.length, 1);
    }
    const counterEntry = counterScores.get(heroId);
    const counterComponent = counterEntry?.counter_score || 0.5;
    const popularityComponent = Math.min(Number(hero.pro_pick || 0) / 300, 1);
    const score = counterComponent * 0.45 + roleComponent * 0.25 + winComponent * 0.2 + popularityComponent * 0.1;
    const reasons = [];
    if (counterEntry) {
      const best = [...counterEntry.details].sort((a, b) => b.counter_win_rate - a.counter_win_rate).slice(0, 2);
      reasons.push(best.map((item) => `对 ${item.enemy} 约 ${item.counter_win_rate}% 胜率`).join("，"));
    }
    const matchedRoles = roles.filter((role) => roleTargets.includes(role)).map(displayRoleName);
    if (matchedRoles.length) reasons.push(`符合位置偏好：${matchedRoles.join(", ")}`);
    if (rate != null) reasons.push(`${source} 样本胜率约 ${Math.round(rate * 1000) / 10}%`);
    candidates.push({
      hero: heroDisplay(hero),
      score: Math.round(score * 1000) / 10,
      reasons: reasons.slice(0, 3),
      matchups: counterEntry?.details?.slice(0, 4) || [],
    });
  }

  return candidates.sort((a, b) => b.score - a.score).slice(0, limit);
}

function generateAdvice(allies, enemies, desiredRole, balance) {
  const enemyRoles = {};
  for (const enemy of enemies) {
    for (const role of enemy.roles || []) enemyRoles[role] = (enemyRoles[role] || 0) + 1;
  }
  const advice = [];
  if ((enemyRoles.Disabler || 0) >= 2) advice.push("敌方控制多：核心位优先考虑 BKB、分身/林肯等解控或防先手装备。");
  if ((enemyRoles.Nuker || 0) >= 2) advice.push("敌方法术爆发高：辅助位考虑微光、笛子、莲花，核心位注意魔抗和切入时机。");
  if ((enemyRoles.Durable || 0) >= 2) advice.push("敌方前排厚：需要破甲、百分比伤害、持续输出，避免只堆一次性爆发。");
  if (!balance.role_count.Initiator) advice.push("己方缺先手：补英雄时优先看开团能力，打法上要依赖视野和反打。");
  if (desiredRole === "mid") advice.push("中单建议：关注 6/8/10 分钟符点和边路击杀窗口，英雄选择要能带节奏或守塔。");
  if (desiredRole === "carry") advice.push("一号位建议：如果阵容前中期弱，优先选自保和清线能力强的核心。");
  if (!advice.length) advice.push("当前信息不足以给出强约束建议，优先补控制、视野、清线和一名稳定输出点。");
  return advice;
}

function generateItemAdvice(items, allies, enemies, desiredRole, question) {
  const focusHero = allies[0] || null;
  const focusName = focusHero?.localized_name || "";
  const enemyNames = new Set(enemies.map((hero) => hero.localized_name));
  const enemyRoles = {};
  for (const enemy of enemies) {
    for (const role of enemy.roles || []) enemyRoles[role] = (enemyRoles[role] || 0) + 1;
  }

  const build = structuredClone(baseItemPlan(desiredRole));
  let notes = [];
  const laneNotes = [];
  let avoid = [];
  const heroPlan = heroItemPlan(focusName, desiredRole);
  for (const key of ["starting", "lane", "core", "situational"]) {
    if (heroPlan[key]) build[key] = mergeUnique(heroPlan[key], build[key] || []);
  }
  notes = notes.concat(heroPlan.notes || []);
  avoid = avoid.concat(heroPlan.avoid || []);

  if ((enemyRoles.Nuker || 0) >= 1) {
    build.lane = mergeUnique(["凝魂之露", "魔棒"], build.lane);
    build.situational = mergeUnique(["黑皇杖", "洞察烟斗/微光披风"], build.situational);
    laneNotes.push("敌方法术消耗明显，对线期优先补凝魂之露和魔棒，先保证不被一套压出经验区。");
  }
  if ((enemyRoles.Disabler || 0) >= 1) {
    build.situational = mergeUnique(["黑皇杖", "林肯法球", "莲花宝珠"], build.situational);
    notes.push("敌方有稳定控制时，核心位不要把 BKB/林肯拖得太晚。");
  }
  if (["Shadow Fiend", "Sniper", "Drow Ranger", "Lina"].some((name) => enemyNames.has(name))) {
    build.lane = mergeUnique(["鞋子", "风灵之纹/加速手套类小件"], build.lane);
    build.situational = mergeUnique(["跳刀", "风杖/推推棒", "黑皇杖"], build.situational);
    laneNotes.push("面对长手高爆发英雄，核心是先活住和抢符，不要为了贪刀连续吃满技能。");
  }
  if (focusName === "Ember Spirit" && enemyNames.has("Shadow Fiend")) {
    build.starting = ["树之祭祀", "仙灵火", "铁树枝干", "属性小件"];
    build.lane = ["魔瓶", "魔棒", "鞋子", "凝魂之露"];
    build.core = ["相位鞋/动力鞋", "漩涡", "黑皇杖", "阿哈利姆神杖/代达罗斯之殇"];
    build.situational = mergeUnique(["林肯法球", "希瓦的守护", "金箍棒"], build.situational);
    laneNotes.push("火猫打影魔不要站在同一直线连续吃三炮，补刀优先用无影拳和残焰保血量。");
    laneNotes.push("3 分钟后凝魂之露价值很高；如果被压，先鞋瓶魔棒稳住，不要裸憋大件。");
    avoid = avoid.concat(["裸狂战/裸大电锤", "没 BKB 就强行先手进五个人"]);
  }
  if (question.includes("对线") || question.includes("线期")) {
    laneNotes.push("你的问题偏对线期，所以优先看小件、补给、抗压和符点节奏，不要只看六神装。");
  }

  return {
    focus_hero: focusHero ? displayHeroName(focusHero) : "未指定",
    role: desiredRole,
    starting: buildItemIcons(build.starting, items, 6),
    lane: buildItemIcons(build.lane, items, 6),
    core: buildItemIcons(build.core, items, 6),
    situational: buildItemIcons(build.situational, items, 8),
    lane_notes: mergeUnique(laneNotes, notes).slice(0, 6),
    avoid: mergeUnique(avoid, defaultAvoidItems(desiredRole)).slice(0, 5),
  };
}

function baseItemPlan(role) {
  const plans = {
    carry: {
      starting: ["补刀斧", "树之祭祀", "敏捷便鞋/力量手套", "铁树枝干"],
      lane: ["魔棒", "系带/护腕", "鞋子", "续航补给"],
      core: ["发育装", "黑皇杖", "分身斧/散夜对剑", "输出大件"],
      situational: ["林肯法球", "蝴蝶", "撒旦之邪力", "深渊之刃"],
    },
    mid: {
      starting: ["树之祭祀", "仙灵火", "铁树枝干", "属性小件"],
      lane: ["魔瓶", "魔棒", "鞋子", "凝魂之露"],
      core: ["节奏装", "黑皇杖", "机动装", "输出装"],
      situational: ["林肯法球", "风杖", "跳刀", "否决坠饰"],
    },
    offlane: {
      starting: ["补刀斧", "树之祭祀", "护腕配件", "铁树枝干"],
      lane: ["魔棒", "护腕", "鞋子", "先锋盾/魂戒"],
      core: ["跳刀", "刃甲", "黑皇杖", "团队装"],
      situational: ["赤红甲", "洞察烟斗", "莲花宝珠", "希瓦的守护"],
    },
    soft_support: {
      starting: ["侦查守卫", "岗哨守卫", "血榴弹", "树之祭祀", "芒果"],
      lane: ["魔棒", "速度之靴", "风灵之纹", "小净化"],
      core: ["奥术鞋/静谧之鞋", "微光披风", "原力法杖", "以太透镜"],
      situational: ["跳刀", "莲花宝珠", "炎阳纹章", "黑皇杖"],
    },
    hard_support: {
      starting: ["侦查守卫", "岗哨守卫", "血榴弹", "树之祭祀", "芒果"],
      lane: ["魔棒", "速度之靴", "补给", "烟雾"],
      core: ["静谧之鞋/奥术鞋", "微光披风", "原力法杖", "团队保护装"],
      situational: ["莲花宝珠", "洞察烟斗", "盘子", "跳刀"],
    },
  };
  return plans[role] || {
    starting: ["树之祭祀", "铁树枝干", "属性小件", "补给"],
    lane: ["魔棒", "鞋子", "小件抗压装"],
    core: ["黑皇杖", "机动装", "输出/团队装"],
    situational: ["林肯法球", "莲花宝珠", "微光披风", "原力法杖"],
  };
}

function heroItemPlan(heroName, role) {
  const plans = {
    "Ember Spirit": {
      starting: ["树之祭祀", "仙灵火", "铁树枝干", "属性小件"],
      lane: ["魔瓶", "魔棒", "鞋子", "凝魂之露"],
      core: ["相位鞋/动力鞋", "漩涡", "黑皇杖", "阿哈利姆神杖"],
      situational: ["代达罗斯之殇", "希瓦的守护", "林肯法球", "金箍棒"],
      notes: ["火猫优先保证节奏和进场安全，BKB 时机通常比纯输出大件更关键。"],
      avoid: ["只刷不动边路", "没有保命装就先手冲后排"],
    },
    "Axe": {
      lane: ["魔棒", "先锋盾", "速度之靴"],
      core: ["跳刀", "刃甲", "黑皇杖"],
      situational: ["希瓦的守护", "莲花宝珠", "赤红甲"],
      notes: ["斧王装备核心是跳刀时机，太晚会失去主动权。"],
    },
    "Lion": {
      lane: ["魔棒", "速度之靴", "小净化"],
      core: ["静谧之鞋/奥术鞋", "跳刀", "以太透镜"],
      situational: ["微光披风", "原力法杖", "阿哈利姆魔晶"],
      notes: ["莱恩不要只憋跳，劣势局先做保命和视野装。"],
    },
    "Juggernaut": {
      lane: ["魔棒", "系带", "鞋子"],
      core: ["相位鞋", "漩涡/狂战斧", "分身斧", "黑皇杖"],
      situational: ["蝴蝶", "深渊之刃", "斯嘉蒂之眼", "金箍棒"],
      notes: ["剑圣要根据局势选发育装，劣势不要贪慢速大件。"],
    },
    "Sniper": {
      lane: ["系带", "鞋子", "魔棒"],
      core: ["动力鞋", "魔龙枪", "漩涡", "黑皇杖"],
      situational: ["飓风长戟", "撒旦之邪力", "金箍棒", "蝴蝶"],
      notes: ["火枪最怕被切，长戟/BKB 的优先级经常高于纯输出。"],
    },
    "Crystal Maiden": {
      lane: ["魔棒", "速度之靴", "补给"],
      core: ["静谧之鞋", "微光披风", "原力法杖"],
      situational: ["跳刀", "黑皇杖", "阿哈利姆魔晶"],
      notes: ["冰女装备以活着放技能和救人为核心，不要过早追求大件。"],
    },
  };
  if (plans[heroName]) return plans[heroName];
  if (["soft_support", "hard_support"].includes(role)) {
    return {
      notes: ["辅助位出装优先级是视野、保人、救自己，其次才是贪功能大件。"],
      avoid: ["裸大件不买眼", "没有保命装就站位过深"],
    };
  }
  return {};
}

function buildItemIcons(rawItems, itemConstants, limit) {
  const items = [];
  const seen = new Set();
  for (const rawItem of rawItems || []) {
    for (const itemName of expandItemName(rawItem)) {
      const key = ITEM_NAME_TO_KEY[itemName];
      if (!key || seen.has(key)) continue;
      seen.add(key);
      const itemData = itemConstants[key] || {};
      const imagePath = itemData.img || `/apps/dota2/images/dota_react/items/${key}.png`;
      items.push({
        name: itemName,
        key,
        english_name: itemData.dname || key,
        icon: imagePath.startsWith("/") ? `${CDN}${imagePath}` : imagePath,
      });
      if (items.length >= limit) return items;
    }
  }
  return items;
}

function expandItemName(rawItem) {
  if (GENERIC_ITEM_EXPANSIONS[rawItem]) return GENERIC_ITEM_EXPANSIONS[rawItem];
  const result = [];
  for (const part of String(rawItem).split(/[/／、]/)) {
    const itemName = part.trim().replace(/^(裸|先出|补)/, "");
    if (GENERIC_ITEM_EXPANSIONS[itemName]) result.push(...GENERIC_ITEM_EXPANSIONS[itemName]);
    else result.push(itemName);
  }
  return result.filter(Boolean);
}

function defaultAvoidItems(role) {
  if (["soft_support", "hard_support"].includes(role)) return ["裸大件不补眼", "劣势局跳过微光/推推"];
  if (role === "mid") return ["对线崩了还裸贪输出", "没有 BKB/林肯就硬冲控制阵容"];
  if (role === "carry") return ["无视敌方控制只做输出", "该参战时继续刷野"];
  return ["只看固定攻略，不根据敌方控制和爆发调整"];
}

function mergeUnique(primary, secondary) {
  const result = [];
  const seen = new Set();
  for (const item of [...(primary || []), ...(secondary || [])]) {
    if (item && !seen.has(item)) {
      result.push(item);
      seen.add(item);
    }
  }
  return result;
}

function buildAnswer(allies, enemies, role, question, balance, recs, advice) {
  const lines = [];
  if (question) lines.push(`### 问题\n${question}`);
  lines.push("### 阵容识别");
  lines.push(`- 己方：${allies.length ? allies.map(displayHeroName).join(", ") : "未提供"}`);
  lines.push(`- 敌方：${enemies.length ? enemies.map(displayHeroName).join(", ") : "未提供"}`);
  lines.push(`- 位置偏好：${role}`);
  lines.push("\n### 主要风险");
  for (const risk of balance.risks) lines.push(`- ${risk}`);
  lines.push("\n### 推荐候选");
  for (const [idx, item] of recs.slice(0, 5).entries()) {
    lines.push(`${idx + 1}. ${item.hero.name}，综合分 ${item.score}`);
    for (const reason of item.reasons) lines.push(`   - ${reason}`);
  }
  lines.push("\n### 打法建议");
  for (const item of advice) lines.push(`- ${item}`);
  return lines.join("\n");
}

function setLoading(isLoading) {
  form.querySelectorAll("button, input, textarea, select").forEach((item) => {
    item.disabled = isLoading;
  });
  loadingState.classList.toggle("hidden", !isLoading);
  if (isLoading) {
    emptyState.classList.add("hidden");
    result.classList.add("hidden");
  }
}

function renderResult(data) {
  loadingState.classList.add("hidden");
  result.classList.remove("hidden");
  allyCount.textContent = data.recognized.allies.length;
  enemyCount.textContent = data.recognized.enemies.length;
  recommendCount.textContent = data.recommendations.length;
  recommendations.innerHTML = data.recommendations.map((item) => renderHeroCard(item)).join("");
  itemBuild.innerHTML = renderItemBuild(data.item_advice);
  risks.innerHTML = data.balance.risks.map((risk) => `<li>${escapeHtml(risk)}</li>`).join("");
  answer.innerHTML = markdownToHtml(data.answer_md);
}

function renderHeroCard(item) {
  const hero = item.hero;
  const image = hero.image || hero.icon || "";
  const fallback = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='120'%3E%3Crect width='180' height='120' fill='%2310141b'/%3E%3Ctext x='14' y='66' fill='%23d6a84f' font-size='16' font-family='Arial'%3EDota2%3C/text%3E%3C/svg%3E";
  return `
    <article class="hero-card">
      <img src="${escapeAttribute(image || fallback)}" alt="${escapeAttribute(hero.name)}" onerror="this.src='${fallback}'" />
      <div class="hero-card-body">
        <div class="hero-title-row">
          <h3 class="hero-name">${escapeHtml(hero.name)}</h3>
          <span class="score">${escapeHtml(String(item.score))}</span>
        </div>
        <div class="hero-meta">${escapeHtml(hero.attack_type || "未知")} · ${escapeHtml((hero.roles || []).slice(0, 3).join(", "))}</div>
        <ul class="reason-list">${item.reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join("")}</ul>
      </div>
    </article>
  `;
}

function renderItemBuild(itemAdvice) {
  if (!itemAdvice) return `<div class="item-empty">暂无出装建议。</div>`;
  const groups = [
    ["出门装", itemAdvice.starting || []],
    ["对线期", itemAdvice.lane || []],
    ["核心装", itemAdvice.core || []],
    ["针对装", itemAdvice.situational || []],
  ];
  const itemGroups = groups
    .filter(([, items]) => items && items.length)
    .map(([title, items]) => `
      <section class="item-group">
        <h3>${escapeHtml(title)}</h3>
        <div class="item-icons">${items.map(renderItemIcon).join("")}</div>
      </section>
    `)
    .join("");
  const textGroups = [
    ["注意事项", itemAdvice.lane_notes || []],
    ["不建议", itemAdvice.avoid || []],
  ]
    .filter(([, items]) => items && items.length)
    .map(([title, items]) => `
      <section class="item-group item-text-group">
        <h3>${escapeHtml(title)}</h3>
        <ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      </section>
    `)
    .join("");
  return `
    <section class="item-group item-meta-group">
      <h3>参考</h3>
      <div class="item-meta-line">${escapeHtml(itemAdvice.focus_hero || "未指定")} · ${escapeHtml(itemAdvice.role || "")}</div>
    </section>
    ${itemGroups}
    ${textGroups}
  `;
}

function renderItemIcon(item) {
  const name = item.name || item.english_name || item.key || "装备";
  if (!item.icon) return `<span class="item-text-chip">${escapeHtml(name)}</span>`;
  return `
    <span class="item-icon" title="${escapeAttribute(name)}" aria-label="${escapeAttribute(name)}">
      <img src="${escapeAttribute(item.icon)}" alt="${escapeAttribute(name)}" loading="lazy" />
    </span>
  `;
}

function renderError(error) {
  loadingState.classList.add("hidden");
  result.classList.remove("hidden");
  recommendations.innerHTML = "";
  itemBuild.innerHTML = "";
  risks.innerHTML = `<li>${escapeHtml(error.message)}</li>`;
  answer.innerHTML = "<h3>请求失败</h3><p>请刷新页面后重试。</p>";
}

function markdownToHtml(markdown) {
  const lines = markdown.split("\n");
  const html = [];
  let listOpen = false;
  let orderedOpen = false;
  for (const line of lines) {
    if (line.startsWith("### ")) {
      if (listOpen) {
        html.push("</ul>");
        listOpen = false;
      }
      if (orderedOpen) {
        html.push("</ol>");
        orderedOpen = false;
      }
      html.push(`<h3>${escapeHtml(line.slice(4))}</h3>`);
    } else if (/^\d+\.\s/.test(line)) {
      if (listOpen) {
        html.push("</ul>");
        listOpen = false;
      }
      if (!orderedOpen) {
        html.push("<ol>");
        orderedOpen = true;
      }
      html.push(`<li>${escapeHtml(line.replace(/^\d+\.\s/, ""))}</li>`);
    } else if (line.startsWith("- ") || line.startsWith("   - ")) {
      if (orderedOpen) {
        html.push("</ol>");
        orderedOpen = false;
      }
      if (!listOpen) {
        html.push("<ul>");
        listOpen = true;
      }
      html.push(`<li>${escapeHtml(line.replace(/^\s*-\s/, ""))}</li>`);
    } else if (line.trim()) {
      if (listOpen) {
        html.push("</ul>");
        listOpen = false;
      }
      if (orderedOpen) {
        html.push("</ol>");
        orderedOpen = false;
      }
      html.push(`<p>${escapeHtml(line)}</p>`);
    }
  }
  if (listOpen) html.push("</ul>");
  if (orderedOpen) html.push("</ol>");
  return html.join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}
