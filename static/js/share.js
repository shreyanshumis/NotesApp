(() => {
  document.querySelectorAll('[data-share-file]').forEach((link) => {
    link.addEventListener('click', async (event) => {
      if (!navigator.share || !navigator.canShare) return;
      event.preventDefault();
      try {
        const response = await fetch(link.href);
        if (!response.ok) throw new Error('Could not prepare file');
        const blob = await response.blob();
        const file = new File([blob], link.dataset.fileName, { type: link.dataset.fileType });
        if (!navigator.canShare({ files: [file] })) {
          window.location.href = link.href;
          return;
        }
        await navigator.share({ title: document.title, files: [file] });
      } catch (error) {
        if (error.name !== 'AbortError') window.location.href = link.href;
      }
    });
  });
})();
