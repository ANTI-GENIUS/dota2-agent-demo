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
const playbook = document.querySelector("#playbook");
const answer = document.querySelector("#answer");

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
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Agent request failed");
    }
    renderResult(data);
  } catch (error) {
    renderError(error);
  } finally {
    setLoading(false);
  }
});

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

  recommendations.innerHTML = data.recommendations
    .map((item) => renderHeroCard(item))
    .join("");

  itemBuild.innerHTML = renderItemBuild(data.item_advice);

  risks.innerHTML = data.balance.risks
    .map((risk) => `<li>${escapeHtml(risk)}</li>`)
    .join("");

  playbook.innerHTML = renderPlaybook(data.playbook || []);
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
        <div class="hero-meta">
          ${escapeHtml(hero.attack_type || "Unknown")} · ${escapeHtml((hero.roles || []).slice(0, 3).join(", "))}
        </div>
        <ul class="reason-list">
          ${item.reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join("")}
        </ul>
      </div>
    </article>
  `;
}

function renderItemBuild(itemAdvice) {
  if (!itemAdvice) {
    return `<div class="item-empty">暂无出装建议。</div>`;
  }
  const groups = [
    ["出门装", itemAdvice.starting || []],
    ["对线期", itemAdvice.lane || []],
    ["核心装", itemAdvice.core || []],
    ["针对装", itemAdvice.situational || []],
  ];
  const itemGroups = groups
    .filter(([, items]) => items && items.length)
    .map(([title, items]) => {
      return `
        <section class="item-group">
          <h3>${escapeHtml(title)}</h3>
          <div class="item-icons">
            ${items.map((item) => renderItemIcon(item)).join("")}
          </div>
        </section>
      `;
    })
    .join("");

  const notes = itemAdvice.lane_notes || [];
  const avoid = itemAdvice.avoid || [];
  const textGroups = [
    ["注意事项", notes],
    ["不建议", avoid],
  ]
    .filter(([, items]) => items && items.length)
    .map(([title, items]) => {
      return `
        <section class="item-group item-text-group">
          <h3>${escapeHtml(title)}</h3>
          <ul>
            ${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </section>
      `;
    })
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
  if (typeof item === "string") {
    return `<span class="item-text-chip">${escapeHtml(item)}</span>`;
  }
  const name = item.name || item.english_name || item.key || "装备";
  const icon = item.icon || "";
  if (!icon) {
    return `<span class="item-text-chip">${escapeHtml(name)}</span>`;
  }
  return `
    <span class="item-icon" title="${escapeAttribute(name)}" aria-label="${escapeAttribute(name)}">
      <img src="${escapeAttribute(icon)}" alt="${escapeAttribute(name)}" loading="lazy" />
    </span>
  `;
}

function renderPlaybook(entries) {
  if (!entries.length) {
    return `<div class="playbook-empty">暂无命中的个人样本。可以在 data/playbook.json 中补充真实 match id 和复盘结论。</div>`;
  }
  return entries
    .map((entry) => {
      const meta = [
        entry.source_type,
        entry.source,
        entry.match_id ? `Match ${entry.match_id}` : "",
        entry.patch ? `Patch ${entry.patch}` : "",
      ].filter(Boolean);
      const tags = entry.tags || [];
      return `
        <article class="playbook-card">
          <div class="playbook-meta">${escapeHtml(meta.join(" · "))}</div>
          <h3>${escapeHtml(entry.title || "未命名理解")}</h3>
          <p>${escapeHtml(entry.summary || "")}</p>
          <ul>
            ${(entry.points || []).slice(0, 3).map((point) => `<li>${escapeHtml(point)}</li>`).join("")}
          </ul>
          <div class="tag-row">
            ${tags.map((tag) => `<span>${escapeHtml(tag)}</span>`).join("")}
          </div>
        </article>
      `;
    })
    .join("");
}

function renderError(error) {
  loadingState.classList.add("hidden");
  result.classList.remove("hidden");
  recommendations.innerHTML = "";
  itemBuild.innerHTML = "";
  playbook.innerHTML = "";
  risks.innerHTML = `<li>${escapeHtml(error.message)}</li>`;
  answer.innerHTML = "<h3>请求失败</h3><p>请检查本地服务是否正常运行，或稍后重试 OpenDota 数据源。</p>";
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
