const loadExternalScript = (id) => {
  let scriptEl = document.getElementById('data-viz-external-script');
  if(scriptEl) scriptEl.parentNode.removeChild(scriptEl);
  scriptEl = document.createElement('script');
  scriptEl.src = `https://na-data-projects.s3.amazonaws.com/projects/${id}`;
  scriptEl.setAttribute('id', 'data-viz-external-script');
  document.body.appendChild(scriptEl);
}

export default loadExternalScript;
