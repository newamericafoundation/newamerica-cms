import $ from 'jquery';

// Cache result so no further DOM search is required.
let jQueryObjectCache = null;

export default function getJQueryObjects() {

  if (!jQueryObjectCache) {
    let jQueryObjects = {
      $body: $(document.body),
    	$window: $(window),
    	$wrapper: $('.wrapper'),
    	$header: $('.header')
    }
    jQueryObjectCache = jQueryObjects
  }

  return jQueryObjectCache;

}
