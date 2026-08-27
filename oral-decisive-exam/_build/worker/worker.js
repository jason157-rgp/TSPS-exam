/**
 * 口試作戰室・筆記同步
 *
 * 部署在 Cloudflare Workers，綁一個 KV namespace（變數名稱 NOTES）。
 * 網頁把筆記 PUT 上來，這裡與既有內容依「每則的時間戳」合併後存回，
 * 並把合併結果回傳，所以兩台裝置同時改不同節不會互相蓋掉。
 *
 * 金鑰（?k=）是網頁把通關密語做 SHA-256 之後的 64 位十六進位字串，
 * 密語本身不會離開你的瀏覽器。
 *
 * 刪除以「空字串 + 較新的時間戳」表示（墓碑），這樣某台裝置刪掉的筆記
 * 不會被另一台的舊資料復活。
 */

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,PUT,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
};

const KEY_RE = /^[0-9a-f]{64}$/;
const MAX_BODY = 2 * 1024 * 1024;   // 2 MB，筆記遠遠用不到

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...CORS, "Content-Type": "application/json; charset=utf-8" },
  });
}

function mergeNotes(base, incoming) {
  const out = { ...base };
  let changed = 0;
  for (const id of Object.keys(incoming)) {
    const n = incoming[id];
    if (!n || typeof n.t !== "string") continue;
    const u = Number(n.u) || 0;
    const old = out[id];
    if (!old || u > (Number(old.u) || 0)) {
      out[id] = { t: n.t, u };          // t 為空字串＝已刪除的墓碑
      changed++;
    }
  }
  return { notes: out, changed };
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
      return json(cur || { notes: {}, at: 0 });
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
      const incoming = body && body.notes;
      if (!incoming || typeof incoming !== "object" || Array.isArray(incoming)) {
        return json({ error: "缺少 notes" }, 400);
      }

      const cur = (await env.NOTES.get(id, "json")) || { notes: {} };
      const { notes, changed } = mergeNotes(cur.notes || {}, incoming);
      const out = { notes, at: Date.now() };
      if (changed) await env.NOTES.put(id, JSON.stringify(out));
      return json(out);
    }

    return json({ error: "不支援的方法" }, 405);
  },
};
