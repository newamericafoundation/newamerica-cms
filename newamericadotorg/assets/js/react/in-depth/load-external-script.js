const loadExternalScript = (id) => {
  let scriptEl = document.getElementById('data-viz-external-script');
  if(scriptEl) scripEl.parentNode.removeChild(scriptEl);
  scriptEl = document.createElement('script');
  scriptEl.src = `https://na-data-projects.s3.amazonaws.com/projects/${id}`;
  document.body.appendChild(scriptEl);
}

export default loadExternalScript;
