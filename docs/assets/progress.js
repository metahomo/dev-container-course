// 진도 조감도 — 주차 쪽의 체크리스트를 이 브라우저(localStorage)에 저장하고, 조감도 쪽에서 모아 보여 준다.
// 서버로 보내는 것은 없다. 키: dcc:<주차 경로>:<체크리스트 문구>
(function () {
  var PREFIX = "dcc:";
  var WEEKS = [];
  for (var i = 0; i <= 12; i++) WEEKS.push("week" + (i < 10 ? "0" + i : i));

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { return null; } }
  function pageKey(path) { var m = /weeks\/(week\d\d)/.exec(path); return m ? m[1] : null; }
  function itemsOf(root) { return Array.prototype.slice.call(root.querySelectorAll("h2#_1 ~ ul.task-list li.task-list-item, ul.task-list li.task-list-item")); }
  function textOf(li) { return (li.textContent || "").replace(/\s+/g, " ").trim(); }

  // 주차 쪽: 체크 상자를 켜고 저장
  function wirePage() {
    var week = pageKey(location.pathname);
    if (!week) return;
    itemsOf(document).forEach(function (li) {
      var box = li.querySelector("input[type=checkbox]");
      if (!box) return;
      var key = PREFIX + week + ":" + textOf(li);
      box.disabled = false;
      box.checked = store(key) === "1";
      box.addEventListener("change", function () { store(key, box.checked ? "1" : null); });
    });
  }

  // 조감도 쪽: 주차 쪽들을 읽어 체크리스트를 모은다
  function renderBoard() {
    var box = document.getElementById("course-progress");
    if (!box) return;
    var base = new URL("../../weeks/", location.href);
    Promise.all(WEEKS.map(function (w) {
      return fetch(new URL(w + "/", base)).then(function (r) { return r.ok ? r.text() : ""; }).catch(function () { return ""; })
        .then(function (html) {
          var doc = new DOMParser().parseFromString(html, "text/html");
          var h1 = doc.querySelector("article h1"); if (h1) h1.querySelectorAll(".headerlink").forEach(function (a) { a.remove(); });
          var title = (h1 || {}).textContent || w;
          var items = itemsOf(doc).map(textOf);
          return { week: w, title: title.trim(), items: items };
        });
    })).then(function (weeks) {
      var total = 0, done = 0;
      var rows = weeks.map(function (w) {
        var d = w.items.filter(function (t) { return store(PREFIX + w.week + ":" + t) === "1"; }).length;
        total += w.items.length; done += d;
        var pct = w.items.length ? Math.round(d * 100 / w.items.length) : 0;
        return '<tr><td><a href="' + new URL(w.week + "/", base).href + '">' + w.title + '</a></td>' +
          '<td><div class="bar"><span style="width:' + pct + '%"></span></div></td><td>' + d + " / " + w.items.length + '</td></tr>';
      }).join("");
      var all = total ? Math.round(done * 100 / total) : 0;
      box.innerHTML = '<p class="overall">전체 진도 <b>' + all + '%</b> (' + done + " / " + total + ' 항목)</p>' +
        '<div class="bar big"><span style="width:' + all + '%"></span></div>' +
        '<table><thead><tr><th>주차</th><th>진도</th><th>항목</th></tr></thead><tbody>' + rows + '</tbody></table>';
    });
    var ex = document.getElementById("progress-export");
    if (ex) ex.onclick = function () {
      var data = {};
      try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k.indexOf(PREFIX) === 0) data[k] = localStorage.getItem(k); } } catch (e) {}
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 1)], { type: "application/json" }));
      a.download = "dev-container-progress.json"; a.click();
    };
    var im = document.getElementById("progress-import");
    if (im) im.onchange = function () {
      var f = im.files[0]; if (!f) return;
      f.text().then(function (t) { var d = JSON.parse(t); Object.keys(d).forEach(function (k) { if (k.indexOf(PREFIX) === 0) store(k, d[k]); }); location.reload(); });
    };
    var rs = document.getElementById("progress-reset");
    if (rs) rs.onclick = function () {
      if (!confirm("이 브라우저에 저장된 진도를 모두 지울까요?")) return;
      try { Object.keys(localStorage).forEach(function (k) { if (k.indexOf(PREFIX) === 0) localStorage.removeItem(k); }); } catch (e) {}
      location.reload();
    };
  }

  document.addEventListener("DOMContentLoaded", function () { wirePage(); renderBoard(); });
})();
