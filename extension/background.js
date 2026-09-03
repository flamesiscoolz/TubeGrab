async function request(path, options = {}) {
  const response = await fetch(`http://127.0.0.1:${globalThis.TUBEGRAB_CONFIG.port}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", "X-Frog-Token": globalThis.TUBEGRAB_CONFIG.token }
  });
  const body = await response.json().catch(() => ({}));
  return { ok: response.ok, ...body };
}

chrome.runtime.onMessage.addListener((message, _sender, reply) => {
  if (message?.type === "download") {
    request("/download", { method: "POST", body: JSON.stringify(message.payload) })
      .then(reply).catch(() => reply({ ok: false, error: "FrogGrab backend is not running" }));
    return true;
  }
  if (message?.type === "status") {
    request(`/status?id=${encodeURIComponent(message.jobId)}`)
      .then(reply).catch(() => reply({ ok: false, error: "Backend connection lost" }));
    return true;
  }
});
