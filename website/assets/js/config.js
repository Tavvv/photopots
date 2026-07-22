/* ==========================================================================
   PhotoPots — Site Configuration
   Loaded BEFORE main.js on every page.
   IMPORTANT: appStoreUrl is a placeholder until the App Store listing is
   final. Update this ONE string and every download button / link on the
   site (any element with [data-appstore]) follows automatically.
   ========================================================================== */

const PHOTOPOTS = {
  appStoreUrl: "https://apps.apple.com/app/photopots/id6740000000", // TODO: replace with final App Store URL
  siteUrl: "https://www.photopots.com",
  supportEmail: "support@photopots.com",
  appName: "PhotoPots",
  tagline: "Keep work and life photos apart."
};

/**
 * Wires every [data-appstore] element to PHOTOPOTS.appStoreUrl.
 * - <a data-appstore>            → href set to the App Store URL
 * - <button data-appstore> etc.  → click navigates to the App Store URL
 * Called automatically on DOMContentLoaded; safe to call again after
 * injecting markup dynamically.
 */
function wireAppStoreLinks() {
  document.querySelectorAll("[data-appstore]").forEach(function (el) {
    if (el.tagName === "A") {
      el.setAttribute("href", PHOTOPOTS.appStoreUrl);
    } else if (!el.dataset.appstoreWired) {
      el.addEventListener("click", function () {
        window.location.href = PHOTOPOTS.appStoreUrl;
      });
      el.dataset.appstoreWired = "true";
    }
  });
}

document.addEventListener("DOMContentLoaded", wireAppStoreLinks);
