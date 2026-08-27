/**
 * 口試作戰室・筆記與已讀同步
 *
 * 部署在 Cloudflare Workers，綁一個 KV namespace（變數名稱 NOTES）。
 * 網頁把資料 PUT 上來，這裡與既有內容依「每一則的時間戳」合併後存回，
 * 並把合併結果回傳，所以兩台裝置同時改不同節不會互相蓋掉。
 *
 * 目前同步兩份資料：
 *   notes  每節的筆記   {節代號: {t: 內容, u: 時間戳}}
 *   read   每節的已讀   {節代號: {r: 0|1,  u: 時間戳}}
 *
 * 金鑰（?k=）是網頁把通關密語做 SHA-256 之後的 64 位十六進位字串，
 * 密語本身不會離開你的瀏覽器。
 *
 * 刪除／取消已讀都以「較新的時間戳 ＋ 空值」表示（墓碑），這樣某台裝置
 * 的操作不會被另一台的舊資料復活。
 */

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,PUT,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
};

const KEY_RE = /^[0-9a-f]{64}$/;
const MAX_BODY = 2 * 1024 * 1024;   // 2 MB，實際用量遠低於此
const MAX_TEXT = 20000;             // 單則筆記字數上限

/** 各份資料的欄位清洗規則；未列出的欄位一律丟棄 */
const MAPS = {
  notes: (v) => (typeof v.t === "string" ? { t: v.t.slice(0, MAX_TEXT) } : null),
  read: (v) => ({ r: v.r ? 1 : 0 }),
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...CORS, "Content-Type": "application/json; charset=utf-8" },
  });
}

function mergeMap(base, incoming, clean) {
  const out = { ...base };
  let changed = 0;
  for (const id of Object.keys(incoming)) {
    const v = incoming[id];
    if (!v || typeof v !== "object") continue;
    const fields = clean(v);
    if (!fields) continue;
    const u = Number(v.u) || 0;
    const old = out[id];
    if (!old || u > (Number(old.u) || 0)) {
      out[id] = { ...fields, u };
      changed++;
    }
  }
  return { map: out, changed };
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS });
    }
    if (!env.NOTES) {
      return json({ error: "KV namespace NOTES 未綁定" }, 500);
    }

    const url = new URL(request.url);
    const key = url.searchParams.get("k") || "";
    if (!KEY_RE.test(key)) {
      return json({ error: "金鑰格式不正確" }, 400);
    }
    const id = "notes:" + key;

    if (request.method === "GET") {
      const cur = await env.NOTES.get(id, "json");
      return json(cur || { notes: {}, read: {}, at: 0 });
    }

    if (request.method === "PUT") {
      const len = Number(request.headers.get("content-length") || 0);
      if (len > MAX_BODY) return json({ error: "內容過大" }, 413);

      let body;
      try {
        body = await request.json();
      } catch (e) {
        return json({ error: "不是合法的 JSON" }, 400);
      }
      if (!body || typeof body !== "object") {
        return json({ error: "格式不正確" }, 400);
      }

      const cur = (await env.NOTES.get(id, "json")) || {};
      const out = { at: Date.now() };
      let changed = 0;

      for (const name of Object.keys(MAPS)) {
        const base = cur[name] || {};
        const inc = body[name];
        if (inc && typeof inc === "object" && !Array.isArray(inc)) {
          const r = mergeMap(base, inc, MAPS[name]);
          out[name] = r.map;
          changed += r.changed;
        } else {
          out[name] = base;      // 這次沒帶這份資料就原樣保留
        }
      }

      if (changed) await env.NOTES.put(id, JSON.stringify(out));
      return json(out);
    }

    return json({ error: "不支援的方法" }, 405);
  },
};
