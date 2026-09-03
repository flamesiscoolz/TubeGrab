(() => {
  const ID = "tubegrab-actions";
  let inserting = false;

  function toast(text, error = false) {
    document.querySelector(".tubegrab-toast")?.remove();
    const node = document.createElement("div");
    node.className = `tubegrab-toast${error ? " error" : ""}`;
    node.textContent = text;
    document.body.append(node);
    requestAnimationFrame(() => node.classList.add("show"));
    setTimeout(() => { node.classList.remove("show"); setTimeout(() => node.remove(), 180); }, 4200);
  }

  function poll(jobId) {
    setTimeout(() => chrome.runtime.sendMessage({ type: "status", jobId }, response => {
      if (!response?.ok) return toast(response?.error || "Could not read download status", true);
      if (response.state === "working") return poll(jobId);
      toast(response.message || (response.state === "done" ? "Download finished" : "Download failed"), response.state === "error");
      document.querySelectorAll(`#${ID} button`).forEach(button => button.disabled = false);
    }), 1000);
  }

  function download(kind, button) {
    const id = new URL(location.href).searchParams.get("v");
    if (!id) return toast("Open a YouTube video first", true);
    document.querySelectorAll(`#${ID} button`).forEach(item => item.disabled = true);
    button.classList.add("loading");
    chrome.runtime.sendMessage({
      type: "download",
      payload: { kind, url: `https://www.youtube.com/watch?v=${id}` }
    }, response => {
      button.classList.remove("loading");
      if (!response?.ok) {
        document.querySelectorAll(`#${ID} button`).forEach(item => item.disabled = false);
        return toast(response?.error || "Could not start download", true);
      }
      toast(`Downloading highest-quality ${kind.toUpperCase()}…`);
      poll(response.jobId);
    });
  }

  function insert() {
    if (inserting || document.getElementById(ID)) return;
    const row = document.querySelector("ytd-watch-metadata ytd-menu-renderer #top-level-buttons-computed");
    const like = row?.querySelector("segmented-like-dislike-button-view-model");
    if (!row || !like) return;
    inserting = true;
    const group = document.createElement("div");
    group.id = ID;
    group.innerHTML = `
      <button type="button" data-kind="mp3" aria-label="Download highest-quality MP3">
        <span>MP3</span>
      </button>
      <button type="button" data-kind="mp4" aria-label="Download highest-quality MP4">
        <span>MP4</span>
      </button>`;
    group.querySelectorAll("button").forEach(button =>
      button.addEventListener("click", () => download(button.dataset.kind, button))
    );
    row.insertBefore(group, like);
    inserting = false;
  }

  new MutationObserver(insert).observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener("yt-navigate-finish", () => { document.getElementById(ID)?.remove(); insert(); });
  insert();
})();
