/**
  * get absolute offset of element
**/

const getOffset = (el, relativeTo=document.body) => {
  let top = 0, left = 0;
  do {
    top += el.offsetTop  || 0;
    left += el.offsetLeft || 0;
    if(el==relativeTo) el = null;
    else el = el.offsetParent;
  } while(el);

  return { top, left };
}

export default getOffset;
