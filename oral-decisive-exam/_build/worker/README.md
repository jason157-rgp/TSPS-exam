# 筆記同步：Cloudflare Worker 部署步驟

只需要做一次，約五分鐘。全部在 Cloudflare 的網頁後台點選，不必安裝任何東西。

## 一、建立存放筆記的空間（KV）

1. 登入 <https://dash.cloudflare.com>
2. 左側選單 **Storage & Databases** → **KV**
3. 按 **Create instance**（或 Create a namespace）
4. 名稱填 `psoral-notes` → 建立

## 二、建立 Worker

1. 左側選單 **Compute (Workers)** → **Workers & Pages**
2. 按 **Create** → 選 **Start with Hello World!** → **Get started**
3. 名稱填 `psoral-notes`（這會決定網址）→ **Deploy**
4. 部署完成後按 **Edit code**（或 **Continue to project** → **Edit code**）
5. 把編輯器裡原有的內容**全部刪掉**，貼上本資料夾的 `worker.js`
6. 右上角 **Deploy**

## 三、把 KV 接上 Worker

1. 回到這個 Worker 的頁面 → **Settings** → **Bindings**
2. **Add binding** → 選 **KV namespace**
3. **Variable name** 填 `NOTES`（**必須完全一樣，區分大小寫**）
4. **KV namespace** 選剛才建立的 `psoral-notes`
5. **Deploy** / **Save**

## 四、取得網址

在 Worker 頁面上會看到類似這樣的網址：

```
https://psoral-notes.<你的帳號代號>.workers.dev
```

**把這個網址複製起來。**

## 五、在網頁上啟用

1. 開 <https://jason157-rgp.github.io/TSPS-exam/oral-decisive-exam/>
2. 左欄筆記那一列按 **同步**
3. 貼上剛才的網址，並自己想一組**通關密語**
4. 按 **啟用**

其他裝置（手機、平板）重複第五步，填**同樣的網址與同樣的密語**，筆記就會互通。

## 檢查是否正常

在瀏覽器打開這個網址（把 `<網址>` 換成你的）：

```
<網址>?k=0000000000000000000000000000000000000000000000000000000000000000
```

正常會看到 `{"notes":{},"at":0}`。若看到 `KV namespace NOTES 未綁定`，表示第三步沒設定成功。

## 幾件該知道的事

- **密語不會離開你的瀏覽器。** 網頁只把密語的 SHA-256 雜湊值送出去當作存取金鑰。
- **但這是弱保護。** 知道網址又猜中密語的人就能讀寫你的筆記。密語請不要用生日或 `1234`，也不要與其他服務共用。
- **免費額度**：每天 10 萬次讀取、1 千次寫入。這個用途一天大概用掉個位數次寫入。
- **要停用**：在網頁上按同步 → 停用，或直接把 Cloudflare 上的 Worker 刪掉。
- 刪掉某則筆記時，系統會留下一個「已刪除」的標記再同步出去，避免另一台裝置的舊資料把它復活。
