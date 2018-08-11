const ellipsize = (text, max_length=56) => {
  if(text.length > max_length)
    return text.slice(0,max_length) + ' ...';

  return text;
}

export default ellipsize;
