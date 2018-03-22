// convert slug to title
export default titlefy(slug) {
  var words = slug.split('-');

  for(var i = 0; i < words.length; i++) {
    var word = words[i];
    words[i] = word.charAt(0).toUpperCase() + word.slice(1);
  }

  return words.join(' ');
}
