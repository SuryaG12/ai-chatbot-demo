/* Embeddable AI chat widget. A client adds ONE script tag to their site.
   Configure with window.CHATBOT_CONFIG = { apiUrl, businessName } */
(function () {
  var cfg = window.CHATBOT_CONFIG || {};
  var apiUrl = cfg.apiUrl || "/chat";
  var businessName = cfg.businessName || "us";
  var sessionId = "s" + Math.random().toString(36).slice(2);

  var css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = (cfg.widgetBase || "/widget") + "/chat-widget.css";
  document.head.appendChild(css);

  var btn = document.createElement("button");
  btn.id = "cb-launcher";
  btn.textContent = "\uD83D\uDCAC";
  btn.setAttribute("aria-label", "Chat with us");
  document.body.appendChild(btn);

  var panel = document.createElement("div");
  panel.id = "cb-panel";
  panel.innerHTML =
    '<div id="cb-header">Chat with ' + businessName + "</div>" +
    '<div id="cb-messages"></div>' +
    '<div id="cb-inputrow"><input id="cb-input" type="text" placeholder="Ask a question..." autocomplete="off"/>' +
    '<button id="cb-send">Send</button></div>';
  panel.style.display = "none";
  document.body.appendChild(panel);

  var msgs = panel.querySelector("#cb-messages");
  var input = panel.querySelector("#cb-input");

  function addMsg(text, who) {
    var d = document.createElement("div");
    d.className = "cb-msg cb-" + who;
    d.textContent = text;
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function send() {
    var text = input.value.trim();
    if (!text) return;
    addMsg(text, "user");
    input.value = "";
    fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId })
    })
      .then(function (r) { return r.json(); })
      .then(function (data) { addMsg(data.reply, "bot"); })
      .catch(function () { addMsg("Sorry, something went wrong. Please try again.", "bot"); });
  }

  btn.onclick = function () {
    var open = panel.style.display !== "none";
    panel.style.display = open ? "none" : "flex";
    if (!open && !msgs.children.length) {
      addMsg("Hi! Ask me about hours, services, pricing, or booking.", "bot");
    }
  };
  panel.querySelector("#cb-send").onclick = send;
  input.addEventListener("keydown", function (e) { if (e.key === "Enter") send(); });
})();
